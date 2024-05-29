import logging

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    FieldDoesNotExist,
    ImproperlyConfigured,
    ObjectDoesNotExist,
    ValidationError,
)
from django.db import transaction
from django.db.models import ManyToManyField, ProtectedError
from django.forms import Form, ModelMultipleChoiceField, MultipleHiddenInput
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import select_template, TemplateDoesNotExist
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.encoding import iri_to_uri
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.edit import FormView
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, mixins
from rest_framework.decorators import action as drf_action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from nautobot.core.api.views import BulkDestroyModelMixin, BulkUpdateModelMixin
from nautobot.core.forms import (
    BootstrapMixin,
    ConfirmationForm,
    CSVDataField,
    CSVFileField,
    restrict_form_fields,
)
from nautobot.core.utils import lookup, permissions
from nautobot.core.utils.requests import get_filterable_params_from_filter_params
from nautobot.core.views.renderers import NautobotHTMLRenderer
from nautobot.core.views.utils import (
    get_csv_form_fields_from_serializer_class,
    handle_protectederror,
    import_csv_helper,
    prepare_cloned_fields,
)
from nautobot.extras.context_managers import deferred_change_logging_for_bulk_operation
from nautobot.extras.forms import NoteForm
from nautobot.extras.models import ExportTemplate
from nautobot.extras.tables import NoteTable, ObjectChangeTable
from nautobot.extras.utils import bulk_delete_with_bulk_change_logging, remove_prefix_from_cf_key

PERMISSIONS_ACTION_MAP = {
    "list": "view",
    "retrieve": "view",
    "destroy": "delete",
    "create": "add",
    "update": "change",
    "bulk_create": "add",  # 3.0 TODO: remove, replaced by system Job
    "bulk_destroy": "delete",
    "bulk_update": "change",
    "changelog": "view",
    "notes": "view",
}


class ContentTypePermissionRequiredMixin(AccessMixin):
    """
    Similar to Django's built-in PermissionRequiredMixin, but extended to check model-level permission assignments.
    This is related to ObjectPermissionRequiredMixin, except that is does not enforce object-level permissions,
    and fits within Nautobot's custom permission enforcement system.

    additional_permissions: An optional iterable of statically declared permissions to evaluate in addition to those
                            derived from the object type
    """

    additional_permissions = []

    def get_required_permission(self):
        """
        Return the specific permission necessary to perform the requested action on an object.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement get_required_permission()")

    def has_permission(self):
        user = self.request.user
        permission_required = self.get_required_permission()

        # Check that the user has been granted the required permission(s).
        if user.has_perms((permission_required, *self.additional_permissions)):
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):
    """
    Allows access only to admin users.
    """

    def has_permission(self):
        return bool(
            self.request.user
            and self.request.user.is_active
            and (self.request.user.is_staff or self.request.user.is_superuser)
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ObjectPermissionRequiredMixin(AccessMixin):
    """
    Similar to Django's built-in PermissionRequiredMixin, but extended to check for both model-level and object-level
    permission assignments. If the user has only object-level permissions assigned, the view's queryset is filtered
    to return only those objects on which the user is permitted to perform the specified action.

    additional_permissions: An optional iterable of statically declared permissions to evaluate in addition to those
                            derived from the object type
    """

    additional_permissions = []

    def get_required_permission(self):
        """
        Return the specific permission necessary to perform the requested action on an object.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement get_required_permission()")

    def has_permission(self):
        user = self.request.user
        permission_required = self.get_required_permission()

        # Check that the user has been granted the required permission(s).
        if user.has_perms((permission_required, *self.additional_permissions)):
            # Update the view's QuerySet to filter only the permitted objects
            action = permissions.resolve_permission(permission_required)[1]
            self.queryset = self.queryset.restrict(user, action)

            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "queryset"):
            raise ImproperlyConfigured(
                (
                    f"{self.__class__.__name__} has no queryset defined. "
                    "ObjectPermissionRequiredMixin may only be used on views which define a base queryset"
                )
            )

        if not self.has_permission():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class GetReturnURLMixin:
    """
    Provides logic for determining where a user should be redirected after processing a form.
    """

    default_return_url = None

    def get_return_url(self, request, obj=None, default_return_url=None):
        # First, see if `return_url` was specified as a query parameter or form data. Use this URL only if it's
        # considered safe.
        query_param = request.GET.get("return_url") or request.POST.get("return_url")
        if url_has_allowed_host_and_scheme(url=query_param, allowed_hosts=request.get_host()):
            return iri_to_uri(query_param)

        # Next, check if the object being modified (if any) has an absolute URL.
        # Note that the use of both `obj.present_in_database` and `obj.pk` is correct here because this conditional
        # handles all three of the create, update, and delete operations. When Django deletes an instance
        # from the DB, it sets the instance's PK field to None, regardless of the use of a UUID.
        try:
            if obj is not None and obj.present_in_database and obj.pk:
                return obj.get_absolute_url()
        except AttributeError:
            # Model has no get_absolute_url() method or no reverse match
            pass

        if default_return_url is not None:
            return reverse(default_return_url)

        # Fall back to the default URL (if specified) for the view.
        if self.default_return_url is not None:
            return reverse(self.default_return_url)

        # Attempt to dynamically resolve the list view for the object
        if hasattr(self, "queryset"):
            try:
                return reverse(lookup.get_route_for_model(self.queryset.model, "list"))
            except NoReverseMatch:
                pass

        # If all else fails, return home. Ideally this should never happen.
        return reverse("home")


@extend_schema(exclude=True)
class NautobotViewSetMixin(GenericViewSet, AccessMixin, GetReturnURLMixin, FormView):
    """
    NautobotViewSetMixin is an aggregation of various mixins from DRF, Django and Nautobot to acheive the desired behavior pattern for NautobotUIViewSet
    """

    renderer_classes = [NautobotHTMLRenderer]
    logger = logging.getLogger(__name__)
    # Attributes that need to be specified: form_class, queryset, serializer_class, table_class for most mixins.
    # filterset and filter_params will be initialized in filter_queryset() in ObjectListViewMixin
    filter_params = None
    filterset = None
    filterset_class = None
    filterset_form_class = None
    form_class = None
    create_form_class = None
    update_form_class = None
    parser_classes = [FormParser, MultiPartParser]
    queryset = None
    # serializer_class has to be specified to eliminate the need to override retrieve() in the RetrieveModelMixin for now.
    serializer_class = None
    table_class = None
    notes_form_class = NoteForm

    def get_permissions_for_model(self, model, actions):
        """
        Resolve the named permissions for a given model (or instance) and a list of actions (e.g. view or add).

        :param model: A model or instance
        :param actions: A list of actions to perform on the model
        """
        model_permissions = []
        for action in actions:
            model_permissions.append(f"{model._meta.app_label}.{action}_{model._meta.model_name}")
        return model_permissions

    def get_required_permission(self):
        """
        Obtain the permissions needed to perform certain actions on a model.
        """
        queryset = self.get_queryset()
        try:
            actions = [self.get_action()]
        except KeyError:
            messages.error(
                self.request,
                "This action is not permitted. Please use the buttons at the bottom of the table for Bulk Delete and Bulk Update",
            )
        return self.get_permissions_for_model(queryset.model, actions)

    def check_permissions(self, request):
        """
        Check whether the user has the permissions needed to perform certain actions.
        """
        user = self.request.user
        permission_required = self.get_required_permission()
        # Check that the user has been granted the required permission(s) one by one.
        # In case the permission has `message` or `code`` attribute, we want to include those information in the permission_denied error.
        for permission in permission_required:
            # If the user does not have the permission required, we raise DRF's `NotAuthenticated` or `PermissionDenied` exception
            # which will be handled by self.handle_no_permission() in the UI appropriately in the dispatch() method
            # Cast permission to a list since has_perms() takes a list type parameter.
            if not user.has_perms([permission]):
                self.permission_denied(
                    request,
                    message=getattr(permission, "message", None),
                    code=getattr(permission, "code", None),
                )

    def dispatch(self, request, *args, **kwargs):
        """
        Override the default dispatch() method to check permissions first.
        Used to determine whether the user has permissions to a view and object-level permissions.
        Using AccessMixin handle_no_permission() to deal with Object-Level permissions and API-Level permissions in one pass.
        """
        # self.initialize_request() converts a WSGI request and returns an API request object which can be passed into self.check_permissions()
        # If the user is not authenticated or does not have the permission to perform certain actions,
        # DRF NotAuthenticated or PermissionDenied exception can be raised appropriately and handled by self.handle_no_permission() in the UI.
        # initialize_request() also instantiates self.action which is needed for permission checks.
        api_request = self.initialize_request(request, *args, **kwargs)
        try:
            self.check_permissions(api_request)
        # check_permissions() could raise NotAuthenticated and PermissionDenied Error.
        # We handle them by a single except statement since self.handle_no_permission() is able to handle both errors
        except (exceptions.NotAuthenticated, exceptions.PermissionDenied):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def get_table_class(self):
        # Check if self.table_class is specified in the ModelViewSet before performing subsequent actions
        # If not, display an error message
        if self.action == "notes":
            return NoteTable
        elif self.action == "changelog":
            return ObjectChangeTable

        if self.table_class is None:
            raise NotImplementedError(
                f"'{self.__class__.__name__}' should include a `table_class` attribute for bulk operations"
            )

        return self.table_class

    def _process_destroy_form(self, form):
        """
        Helper method to destroy an object after the form is validated successfully.
        """
        raise NotImplementedError("_process_destroy_form() is not implemented")

    def _process_bulk_destroy_form(self, form):
        """
        Helper method to destroy objects after the form is validated successfully.
        """
        raise NotImplementedError("_process_bulk_destroy_form() is not implemented")

    def _process_create_or_update_form(self, form):
        """
        Helper method to create or update an object after the form is validated successfully.
        """
        raise NotImplementedError("_process_create_or_update_form() is not implemented")

    def _process_bulk_update_form(self, form):
        """
        Helper method to edit objects in bulk after the form is validated successfully.
        """
        raise NotImplementedError("_process_bulk_update_form() is not implemented")

    def _process_bulk_create_form(self, form):  # 3.0 TODO: remove, replaced by system Job
        """
        Helper method to create objects in bulk after the form is validated successfully.
        """
        raise NotImplementedError("_process_bulk_create_form() is not implemented")

    def _handle_object_does_not_exist(self, form):
        msg = "Object import failed due to object-level permissions violation"
        self.logger.debug(msg)
        self.has_error = True
        form.add_error(None, msg)
        return form

    def _handle_not_implemented_error(self):
        # Blanket handler for NotImplementedError raised by form helper functions
        msg = "Please provide the appropriate mixin before using this helper function"
        messages.error(self.request, msg)
        self.has_error = True

    def _handle_validation_error(self, e):
        # For bulk_create/bulk_update view, self.obj is not set since there are multiple
        # The errors will be rendered on the form itself.
        if self.action not in ["bulk_create", "bulk_update"]:  # 3.0 TODO: remove bulk_create
            messages.error(self.request, f"{self.obj} failed validation: {e}")
        self.has_error = True

    def form_valid(self, form):
        """
        Handle valid forms and redirect to success_url.
        """
        request = self.request
        self.has_error = False
        queryset = self.get_queryset()
        try:
            if self.action == "destroy":
                self._process_destroy_form(form)
            elif self.action == "bulk_destroy":
                self._process_bulk_destroy_form(form)
            elif self.action in ["create", "update"]:
                self._process_create_or_update_form(form)
            elif self.action == "bulk_update":
                self._process_bulk_update_form(form)
            elif self.action == "bulk_create":  # 3.0 TODO: remove, replaced by system Job
                self.obj_table = self._process_bulk_create_form(form)
        except ValidationError as e:
            self._handle_validation_error(e)
        except ObjectDoesNotExist:
            form = self._handle_object_does_not_exist(form)
        except NotImplementedError:
            self._handle_not_implemented_error()

        if not self.has_error:
            self.logger.debug("Form validation was successful")
            if self.action == "bulk_create":  # 3.0 TODO: remove, replaced by system Job
                return Response(
                    {
                        "table": self.obj_table,
                        "template": "import_success.html",
                    }
                )
            return super().form_valid(form)
        else:
            # render the form with the error message.
            data = {}
            if self.action in ["bulk_update", "bulk_destroy"]:
                pk_list = self.pk_list
                table_class = self.get_table_class()
                table = table_class(queryset.filter(pk__in=pk_list), orderable=False)
                if not table.rows:
                    messages.warning(
                        request,
                        f"No {queryset.model._meta.verbose_name_plural} were selected for {self.action}.",
                    )
                    return redirect(self.get_return_url(request))

                data.update({"table": table})
            data.update({"form": form})
            return Response(data)

    def form_invalid(self, form):
        """
        Handle invalid forms.
        """
        data = {}
        request = self.request
        queryset = self.get_queryset()
        if self.action in ["bulk_update", "bulk_destroy"]:
            pk_list = self.pk_list
            table_class = self.get_table_class()
            table = table_class(queryset.filter(pk__in=pk_list), orderable=False)
            if not table.rows:
                messages.warning(
                    request,
                    f"No {queryset.model._meta.verbose_name_plural} were selected for {self.action}.",
                )
                return redirect(self.get_return_url(request))

            data = {
                "table": table,
            }
        data.update({"form": form})
        return Response(data)

    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.get_queryset()
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg not in self.kwargs:
            return queryset.model()
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj

    def get_filter_params(self, request):
        """Helper function - take request.GET and discard any parameters that are not used for queryset filtering."""
        filter_params = request.GET.copy()
        return get_filterable_params_from_filter_params(filter_params, self.non_filter_params, self.filterset_class())

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.
        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.
        Override the original `get_queryset()` to apply permission specific to the user and action.
        """
        queryset = super().get_queryset()
        return queryset.restrict(self.request.user, self.get_action())

    def get_action(self):
        """Helper method for retrieving action and if action not set defaulting to action name."""
        return PERMISSIONS_ACTION_MAP.get(self.action, self.action)

    def get_extra_context(self, request, instance=None):
        """
        Return any additional context data for the template.
        request: The current request
        instance: The object being viewed
        """
        if instance is not None:
            return {
                "active_tab": request.GET.get("tab", "main"),
            }
        return {}

    def get_template_name(self):
        # Use "<app>/<model>_<action> if available, else fall back to generic templates
        queryset = self.get_queryset()
        model_opts = queryset.model._meta
        app_label = model_opts.app_label
        action = self.action

        try:
            template_name = f"{app_label}/{model_opts.model_name}_{action}.html"
            select_template([template_name])
        except TemplateDoesNotExist:
            try:
                if action == "create":
                    # When the action is `create`, try {object}_update.html as a fallback
                    # If both are not defined, fall back to generic/object_create.html
                    template_name = f"{app_label}/{model_opts.model_name}_update.html"
                    select_template([template_name])
                elif action == "update":
                    # When the action is `update`, try {object}_create.html as a fallback
                    # If both are not defined, fall back to generic/object_update.html
                    template_name = f"{app_label}/{model_opts.model_name}_create.html"
                    select_template([template_name])
                else:
                    # No special case fallback, fall back to generic/object_{action}.html
                    raise TemplateDoesNotExist("")
            except TemplateDoesNotExist:
                template_name = f"generic/object_{action}.html"
        return template_name

    def get_form(self, *args, **kwargs):
        """
        Helper function to get form for different views if specified.
        If not, return instantiated form using form_class.
        """
        form = getattr(self, f"{self.action}_form", None)
        if not form:
            form_class = self.get_form_class()
            if not form_class:
                self.logger.debug(f"{self.action}_form_class is not defined")
                return None
            form = form_class(*args, **kwargs)
        return form

    def get_form_class(self, **kwargs):
        """
        Helper function to get form_class for different views.
        """

        if self.action in ["create", "update"]:
            if getattr(self, f"{self.action}_form_class"):
                form_class = getattr(self, f"{self.action}_form_class")
            else:
                form_class = getattr(self, "form_class", None)
        elif self.action == "bulk_create":  # 3.0 TODO: remove, replaced by system Job
            required_field_names = [
                field["name"]
                for field in get_csv_form_fields_from_serializer_class(self.serializer_class)
                if field["required"]
            ]

            class BulkCreateForm(BootstrapMixin, Form):
                csv_data = CSVDataField(required_field_names=required_field_names)
                csv_file = CSVFileField()

            form_class = BulkCreateForm
        else:
            form_class = getattr(self, f"{self.action}_form_class", None)

        if not form_class:
            if self.action == "bulk_destroy":
                queryset = self.get_queryset()

                class BulkDestroyForm(ConfirmationForm):
                    pk = ModelMultipleChoiceField(queryset=queryset, widget=MultipleHiddenInput)

                return BulkDestroyForm
            else:
                # Check for request first and then kwargs for form_class specified.
                form_class = self.request.data.get("form_class", None)
                if not form_class:
                    form_class = kwargs.get("form_class", None)
        return form_class

    def form_save(self, form, **kwargs):
        """
        Generic method to save the object from form.
        Should be overriden by user if customization is needed.
        """
        return form.save()

    def alter_queryset(self, request):
        # .all() is necessary to avoid caching queries
        queryset = self.get_queryset()
        return queryset.all()


class ObjectDetailViewMixin(NautobotViewSetMixin, mixins.RetrieveModelMixin):
    """
    UI mixin to retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a model instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        context = serializer.data
        context["use_new_ui"] = True
        return Response(context)


class ObjectListViewMixin(NautobotViewSetMixin, mixins.ListModelMixin):
    """
    UI mixin to list a model queryset
    """

    action_buttons = ("add", "import", "export")
    filterset_class = None
    filterset_form_class = None
    hide_hierarchy_ui = False
    non_filter_params = (
        "export",  # trigger for CSV/export-template/YAML export # 3.0 TODO: remove, irrelevant after #4746
        "page",  # used by django-tables2.RequestConfig
        "per_page",  # used by get_paginate_count
        "sort",  # table sorting
    )

    def filter_queryset(self, queryset):
        """
        Filter a query with request querystrings.
        """
        if self.filterset_class is not None:
            self.filter_params = self.get_filter_params(self.request)
            self.filterset = self.filterset_class(self.filter_params, queryset)
            queryset = self.filterset.qs
            if not self.filterset.is_valid():
                messages.error(
                    self.request,
                    format_html("Invalid filters were specified: {}", self.filterset.errors),
                )
                queryset = queryset.none()

            # If a valid filterset is applied, we have to hide the hierarchy indentation in the UI for tables that support hierarchy indentation.
            # NOTE: An empty filterset query-param is also valid filterset and we dont want to hide hierarchy indentation if no filter query-param is provided
            #      hence `filterset.data`.
            if self.filterset.is_valid() and self.filterset.data:
                self.hide_hierarchy_ui = True
        return queryset

    # 3.0 TODO: remove, irrelevant after #4746
    def check_for_export(self, request, model, content_type):
        # Check for export template rendering
        queryset = self.filter_queryset(self.get_queryset())
        if request.GET.get("export"):
            et = get_object_or_404(
                ExportTemplate,
                content_type=content_type,
                name=request.GET.get("export"),
            )
            try:
                return et.render_to_response(queryset)
            except Exception as e:
                messages.error(
                    request,
                    f"There was an error rendering the selected export template ({et.name}): {e}",
                )

        # Check for YAML export support
        elif "export" in request.GET and hasattr(model, "to_yaml"):
            response = HttpResponse(self.queryset_to_yaml(), content_type="text/yaml")
            filename = f"nautobot_{queryset.model._meta.verbose_name_plural}.yaml"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        return None

    # 3.0 TODO: remove, irrelevant after #4746
    def queryset_to_yaml(self):
        """
        Export the queryset of objects as concatenated YAML documents.
        """
        queryset = self.filter_queryset(self.get_queryset())
        yaml_data = [obj.to_yaml() for obj in queryset]

        return "---\n".join(yaml_data)

    def list(self, request, *args, **kwargs):
        """
        List the model instances.
        """
        context = {"use_new_ui": True}
        if "export" in request.GET:  # 3.0 TODO: remove, irrelevant after #4746
            queryset = self.get_queryset()
            model = queryset.model
            content_type = ContentType.objects.get_for_model(model)
            response = self.check_for_export(request, model, content_type)
            if response is not None:
                return response
        return Response(context)


class ObjectDestroyViewMixin(NautobotViewSetMixin, mixins.DestroyModelMixin):
    """
    UI mixin to destroy a model instance.
    """

    destroy_form_class = ConfirmationForm

    def _process_destroy_form(self, form):
        request = self.request
        obj = self.obj
        queryset = self.get_queryset()
        try:
            with transaction.atomic():
                obj.delete()
                msg = f"Deleted {queryset.model._meta.verbose_name} {obj}"
                self.logger.info(msg)
                messages.success(request, msg)
                self.success_url = self.get_return_url(request, obj)
        except ProtectedError as e:
            self.logger.info("Caught ProtectedError while attempting to delete object")
            handle_protectederror([obj], request, e)
            self.success_url = obj.get_absolute_url()

    def destroy(self, request, *args, **kwargs):
        """
        request.GET: render the ObjectDeleteConfirmationForm which is passed to NautobotHTMLRenderer as Response.
        request.POST: call perform_destroy() which validates the form and perform the action of delete.
        Override to add more variables to Response
        """
        context = {}
        if request.method == "POST":
            return self.perform_destroy(request, **kwargs)
        return Response(context)

    def perform_destroy(self, request, **kwargs):
        """
        Function to validate the ObjectDeleteConfirmationForm and to delete the object.
        """
        self.obj = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ObjectEditViewMixin(NautobotViewSetMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    UI mixin to create or update a model instance.
    """

    def _process_create_or_update_form(self, form):
        """
        Helper method to create or update an object after the form is validated successfully.
        """
        request = self.request
        queryset = self.get_queryset()
        with transaction.atomic():
            object_created = not form.instance.present_in_database
            obj = self.form_save(form)

            # Check that the new object conforms with any assigned object-level permissions
            queryset.get(pk=obj.pk)

            if hasattr(form, "save_note") and callable(form.save_note):
                form.save_note(instance=obj, user=request.user)

            msg = f'{"Created" if object_created else "Modified"} {queryset.model._meta.verbose_name}'
            self.logger.info(f"{msg} {obj} (PK: {obj.pk})")
            try:
                msg = format_html('{} <a href="{}">{}</a>', msg, obj.get_absolute_url(), obj)
            except AttributeError:
                msg = format_html("{} {}", msg, obj)
            messages.success(request, msg)
            if "_addanother" in request.POST:
                # If the object has clone_fields, pre-populate a new instance of the form
                if hasattr(obj, "clone_fields"):
                    url = f"{request.path}?{prepare_cloned_fields(obj)}"
                    self.success_url = url
                self.success_url = request.get_full_path()
            else:
                return_url = form.cleaned_data.get("return_url")
                if url_has_allowed_host_and_scheme(url=return_url, allowed_hosts=request.get_host()):
                    self.success_url = iri_to_uri(return_url)
                else:
                    self.success_url = self.get_return_url(request, obj)

    def create(self, request, *args, **kwargs):
        """
        request.GET: render the ObjectForm which is passed to NautobotHTMLRenderer as Response.
        request.POST: call perform_create() which validates the form and perform the action of create.
        Override to add more variables to Response.
        """
        context = {}
        if request.method == "POST":
            return self.perform_create(request, *args, **kwargs)
        return Response(context)

    # TODO: this conflicts with DRF's CreateModelMixin.perform_create(self, serializer) API
    def perform_create(self, request, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        Function to validate the ObjectForm and to create a new object.
        """
        self.obj = self.get_object()
        form_class = self.get_form_class()
        form = form_class(data=request.POST, files=request.FILES, instance=self.obj)
        restrict_form_fields(form, request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def update(self, request, *args, **kwargs):
        """
        request.GET: render the ObjectEditForm which is passed to NautobotHTMLRenderer as Response.
        request.POST: call perform_update() which validates the form and perform the action of update/partial_update of an existing object.
        Override to add more variables to Response.
        """
        context = {}
        if request.method == "POST":
            return self.perform_update(request, *args, **kwargs)
        return Response(context)

    # TODO: this conflicts with DRF's UpdateModelMixin.perform_update(self, serializer) API
    def perform_update(self, request, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        Function to validate the ObjectEditForm and to update/partial_update an existing object.
        """
        self.obj = self.get_object()
        form_class = self.get_form_class()
        form = form_class(data=request.POST, files=request.FILES, instance=self.obj)
        restrict_form_fields(form, request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ObjectBulkDestroyViewMixin(NautobotViewSetMixin, BulkDestroyModelMixin):
    """
    UI mixin to bulk destroy model instances.
    """

    bulk_destroy_form_class = None
    filterset_class = None

    def _process_bulk_destroy_form(self, form):
        request = self.request
        pk_list = self.pk_list
        queryset = self.get_queryset()
        model = queryset.model
        # Delete objects
        queryset = queryset.filter(pk__in=pk_list)

        try:
            with transaction.atomic():
                deleted_count = bulk_delete_with_bulk_change_logging(queryset)[1][model._meta.label]
                msg = f"Deleted {deleted_count} {model._meta.verbose_name_plural}"
                self.logger.info(msg)
                self.success_url = self.get_return_url(request)
                messages.success(request, msg)
        except ProtectedError as e:
            self.logger.info("Caught ProtectedError while attempting to delete objects")
            handle_protectederror(queryset, request, e)
            self.success_url = self.get_return_url(request)

    def bulk_destroy(self, request, *args, **kwargs):
        """
        Call perform_bulk_destroy().
        The function exist to keep the DRF's get/post pattern of {action}/perform_{action}, we will need it when we transition from using forms to serializers in the UI.
        User should override this function to handle any actions as needed before bulk destroy.
        """
        return self.perform_bulk_destroy(request, **kwargs)

    def perform_bulk_destroy(self, request, **kwargs):
        """
        request.POST "_delete": Function to render the user selection of objects in a table form/BulkDestroyConfirmationForm via Response that is passed to NautobotHTMLRenderer.
        request.POST "_confirm": Function to validate the table form/BulkDestroyConfirmationForm and to perform the action of bulk destroy. Render the form with errors if exceptions are raised.
        """
        queryset = self.get_queryset()
        model = queryset.model
        # Are we deleting *all* objects in the queryset or just a selected subset?
        if request.POST.get("_all"):
            filter_params = self.get_filter_params(request)
            if not filter_params:
                self.pk_list = list(model.objects.only("pk").all().values_list("pk", flat=True))
            elif self.filterset_class is None:
                raise NotImplementedError("filterset_class must be defined to use _all")
            else:
                self.pk_list = list(
                    self.filterset_class(filter_params, model.objects.only("pk")).qs.values_list("pk", flat=True)
                )
        else:
            self.pk_list = list(request.POST.getlist("pk"))
        form_class = self.get_form_class(**kwargs)
        data = {}
        if "_confirm" in request.POST:
            form = form_class(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        table_class = self.get_table_class()
        table = table_class(queryset.filter(pk__in=self.pk_list), orderable=False)
        if not table.rows:
            messages.warning(
                request,
                f"No {queryset.model._meta.verbose_name_plural} were selected for deletion.",
            )
            return redirect(self.get_return_url(request))

        data.update({"table": table})
        return Response(data)


class ObjectBulkCreateViewMixin(NautobotViewSetMixin):  # 3.0 TODO: remove, unused
    """
    UI mixin to bulk create model instances.

    Deprecated - use ImportObjects system Job instead.
    """

    bulk_create_active_tab = "csv-data"

    def _process_bulk_create_form(self, form):
        # Iterate through CSV data and bind each row to a new model form instance.
        new_objs = []
        request = self.request
        queryset = self.get_queryset()
        with transaction.atomic():
            if request.FILES:
                # Set the bulk_create_active_tab to "csv-file"
                # In case the form validation fails, the user will be redirected
                # to the tab with errors rendered on the form.
                self.bulk_create_active_tab = "csv-file"
            new_objs = import_csv_helper(request=request, form=form, serializer_class=self.serializer_class)

            # Enforce object-level permissions
            if queryset.filter(pk__in=[obj.pk for obj in new_objs]).count() != len(new_objs):
                raise ObjectDoesNotExist

        # Compile a table containing the imported objects
        table_class = self.get_table_class()
        obj_table = table_class(new_objs)
        if new_objs:
            msg = f"Imported {len(new_objs)} {new_objs[0]._meta.verbose_name_plural}"
            self.logger.info(msg)
            messages.success(request, msg)
        return obj_table

    def bulk_create(self, request, *args, **kwargs):
        context = {}
        if request.method == "POST":
            return self.perform_bulk_create(request)
        return Response(context)

    def perform_bulk_create(self, request):
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ObjectBulkUpdateViewMixin(NautobotViewSetMixin, BulkUpdateModelMixin):
    """
    UI mixin to bulk update model instances.
    """

    filterset_class = None
    bulk_update_form_class = None

    def _process_bulk_update_form(self, form):
        request = self.request
        queryset = self.get_queryset()
        model = queryset.model
        form_custom_fields = getattr(form, "custom_fields", [])
        form_relationships = getattr(form, "relationships", [])
        # Standard fields are those that are intrinsic to self.model in the form
        # Relationships, custom fields, object_note are extrinsic fields
        # PK is used to identify an existing instance, not to modify the object
        standard_fields = [
            field
            for field in form.fields
            if field not in form_custom_fields + form_relationships + ["pk"] + ["object_note"]
        ]
        nullified_fields = request.POST.getlist("_nullify")
        with deferred_change_logging_for_bulk_operation():
            updated_objects = []
            for obj in queryset.filter(pk__in=form.cleaned_data["pk"]):
                self.obj = obj
                # Update standard fields. If a field is listed in _nullify, delete its value.
                for name in standard_fields:
                    try:
                        model_field = model._meta.get_field(name)
                    except FieldDoesNotExist:
                        # This form field is used to modify a field rather than set its value directly
                        model_field = None
                    # Handle nullification
                    if name in form.nullable_fields and name in nullified_fields:
                        if isinstance(model_field, ManyToManyField):
                            getattr(obj, name).set([])
                        else:
                            setattr(obj, name, None if model_field is not None and model_field.null else "")
                    # ManyToManyFields
                    elif isinstance(model_field, ManyToManyField):
                        if form.cleaned_data[name]:
                            getattr(obj, name).set(form.cleaned_data[name])
                    # Normal fields
                    elif form.cleaned_data[name] not in (None, ""):
                        setattr(obj, name, form.cleaned_data[name])
                # Update custom fields
                for field_name in form_custom_fields:
                    if field_name in form.nullable_fields and field_name in nullified_fields:
                        obj.cf[remove_prefix_from_cf_key(field_name)] = None
                    elif form.cleaned_data.get(field_name) not in (None, "", []):
                        obj.cf[remove_prefix_from_cf_key(field_name)] = form.cleaned_data[field_name]

                obj.validated_save()
                updated_objects.append(obj)
                self.logger.debug(f"Saved {obj} (PK: {obj.pk})")

                # Add/remove tags
                if form.cleaned_data.get("add_tags", None):
                    obj.tags.add(*form.cleaned_data["add_tags"])
                if form.cleaned_data.get("remove_tags", None):
                    obj.tags.remove(*form.cleaned_data["remove_tags"])

                if hasattr(form, "save_relationships") and callable(form.save_relationships):
                    # Add/remove relationship associations
                    form.save_relationships(instance=obj, nullified_fields=nullified_fields)

                if hasattr(form, "save_note") and callable(form.save_note):
                    form.save_note(instance=obj, user=request.user)

            # Enforce object-level permissions
            if queryset.filter(pk__in=[obj.pk for obj in updated_objects]).count() != len(updated_objects):
                raise ObjectDoesNotExist
        if updated_objects:
            msg = f"Updated {len(updated_objects)} {model._meta.verbose_name_plural}"
            self.logger.info(msg)
            messages.success(self.request, msg)
        self.success_url = self.get_return_url(request)

    def bulk_update(self, request, *args, **kwargs):
        """
        Call perform_bulk_update().
        The function exist to keep the DRF's get/post pattern of {action}/perform_{action}, we will need it when we transition from using forms to serializers in the UI.
        User should override this function to handle any actions as needed before bulk update.
        """
        return self.perform_bulk_update(request, **kwargs)

    # TODO: this conflicts with BulkUpdateModelMixin.perform_bulk_update(self, objects, update_data, partial)
    def perform_bulk_update(self, request, **kwargs):  # pylint: disable=arguments-differ
        """
        request.POST "_edit": Function to render the user selection of objects in a table form/BulkUpdateForm via Response that is passed to NautobotHTMLRenderer.
        request.POST "_apply": Function to validate the table form/BulkUpdateForm and to perform the action of bulk update. Render the form with errors if exceptions are raised.
        """
        queryset = self.get_queryset()
        model = queryset.model

        # If we are editing *all* objects in the queryset, replace the PK list with all matched objects.
        if request.POST.get("_all"):
            filter_params = self.get_filter_params(request)
            if not filter_params:
                self.pk_list = list(model.objects.only("pk").all().values_list("pk", flat=True))
            elif self.filterset_class is None:
                raise NotImplementedError("filterset_class must be defined to use _all")
            else:
                self.pk_list = list(
                    self.filterset_class(filter_params, model.objects.only("pk")).qs.values_list("pk", flat=True)
                )
        else:
            self.pk_list = list(request.POST.getlist("pk"))
        data = {}
        form_class = self.get_form_class()
        if "_apply" in request.POST:
            self.kwargs = kwargs
            form = form_class(queryset.model, request.POST)
            restrict_form_fields(form, request.user)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        table_class = self.get_table_class()
        table = table_class(queryset.filter(pk__in=self.pk_list), orderable=False)
        if not table.rows:
            messages.warning(
                request,
                f"No {queryset.model._meta.verbose_name_plural} were selected to update.",
            )
            return redirect(self.get_return_url(request))
        data.update({"table": table})
        return Response(data)


class ObjectChangeLogViewMixin(NautobotViewSetMixin):
    """
    UI mixin to list a model's changelog queryset
    """

    base_template = None

    @drf_action(detail=True)
    def changelog(self, request, *args, **kwargs):
        data = {
            "base_template": self.base_template,
        }
        return Response(data)


class ObjectNotesViewMixin(NautobotViewSetMixin):
    """
    UI Mixin for an Object's Notes.
    """

    base_template = None

    @drf_action(detail=True)
    def notes(self, request, *args, **kwargs):
        data = {
            "base_template": self.base_template,
        }
        return Response(data)
