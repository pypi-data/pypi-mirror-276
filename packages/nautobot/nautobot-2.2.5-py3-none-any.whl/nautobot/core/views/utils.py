import datetime
from io import BytesIO
import urllib.parse

from django.contrib import messages
from django.core.exceptions import FieldError, ValidationError
from django.db.models import ForeignKey
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from rest_framework import exceptions, serializers

from nautobot.core.api.fields import ChoiceField, ContentTypeField, TimeZoneSerializerField
from nautobot.core.api.parsers import NautobotCSVParser
from nautobot.core.models.utils import is_taggable
from nautobot.core.utils.data import is_uuid
from nautobot.core.utils.filtering import get_filter_field_label
from nautobot.core.utils.lookup import get_form_for_model


def check_filter_for_display(filters, field_name, values):
    """
    Return any additional context data for the template.

    Args:
        filters (OrderedDict): The output of `.get_filters()` of a desired FilterSet
        field_name (str): The name of the filter to get a label for and lookup values
        values (list[str]): List of strings that may be PKs to look up

    Returns:
        (dict): A dict containing:
            - name: (str) Field name
            - display: (str) Resolved field name, whether that's a field label or fallback to inputted `field_name` if label unavailable
            - values: (list) List of dictionaries with the same `name` and `display` keys
    """
    values = values if isinstance(values, (list, tuple)) else [values]

    resolved_filter = {
        "name": field_name,
        "display": field_name,
        "values": [{"name": value, "display": value} for value in values],
    }

    if field_name not in filters.keys():
        return resolved_filter

    filter_field = filters[field_name]

    resolved_filter["display"] = get_filter_field_label(filter_field)

    if len(values) == 0 or not hasattr(filter_field, "queryset") or not is_uuid(values[0]):
        return resolved_filter
    else:
        try:
            new_values = []
            for value in filter_field.queryset.filter(pk__in=values):
                new_values.append({"name": str(value.pk), "display": getattr(value, "display", str(value))})
            resolved_filter["values"] = new_values
        except (FieldError, AttributeError):
            pass

    return resolved_filter


# 2.2 TODO: remove this method as it's no longer used in core.
def csv_format(data):
    """
    Convert the given list of data to a CSV row string.

    Encapsulate any data which contains a comma within double quotes.

    Obsolete, as CSV rendering in Nautobot core is now handled by nautobot.core.api.renderers.NautobotCSVRenderer.
    """
    csv = []
    for value in data:
        # Represent None or False with empty string
        if value is None or value is False:
            csv.append("")
            continue

        # Convert dates to ISO format
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.isoformat()

        # Force conversion to string first so we can check for any commas
        if not isinstance(value, str):
            value = f"{value}"

        # Double-quote the value if it contains a comma or line break
        if "," in value or "\n" in value:
            value = value.replace('"', '""')  # Escape double-quotes
            csv.append(f'"{value}"')
        else:
            csv.append(f"{value}")

    return ",".join(csv)


def get_csv_form_fields_from_serializer_class(serializer_class):
    """From the given serializer class, build a list of field dicts suitable for rendering in the CSV import form."""
    serializer = serializer_class(context={"request": None, "depth": 0})
    fields = []
    # Note lots of "noqa: S308" in this function. That's `suspicious-mark-safe-usage`, but in all of the below cases
    # we control the input string and it's known to be safe, so mark_safe() is being used correctly here.
    for field_name, field in serializer.fields.items():
        if field.read_only:
            continue
        if field_name == "custom_fields":
            from nautobot.extras.choices import CustomFieldTypeChoices
            from nautobot.extras.models import CustomField

            cfs = CustomField.objects.get_for_model(serializer_class.Meta.model)
            for cf in cfs:
                cf_form_field = cf.to_form_field(set_initial=False)
                field_info = {
                    "name": cf.add_prefix_to_cf_key(),
                    "required": cf_form_field.required,
                    "foreign_key": False,
                    "label": cf_form_field.label,
                    "help_text": cf_form_field.help_text,
                }
                if cf.type == CustomFieldTypeChoices.TYPE_BOOLEAN:
                    field_info["format"] = mark_safe("<code>true</code> or <code>false</code>")  # noqa: S308
                elif cf.type == CustomFieldTypeChoices.TYPE_DATE:
                    field_info["format"] = mark_safe("<code>YYYY-MM-DD</code>")  # noqa: S308
                elif cf.type == CustomFieldTypeChoices.TYPE_SELECT:
                    field_info["choices"] = {cfc.value: cfc.value for cfc in cf.custom_field_choices.all()}
                elif cf.type == CustomFieldTypeChoices.TYPE_MULTISELECT:
                    field_info["format"] = mark_safe('<code>"value,value"</code>')  # noqa: S308
                    field_info["choices"] = {cfc.value: cfc.value for cfc in cf.custom_field_choices.all()}
                fields.append(field_info)
            continue

        field_info = {
            "name": field_name,
            "required": field.required,
            "foreign_key": False,
            "label": field.label,
            "help_text": field.help_text,
        }
        if isinstance(field, serializers.BooleanField):
            field_info["format"] = mark_safe("<code>true</code> or <code>false</code>")  # noqa: S308
        elif isinstance(field, serializers.DateField):
            field_info["format"] = mark_safe("<code>YYYY-MM-DD</code>")  # noqa: S308
        elif isinstance(field, TimeZoneSerializerField):
            field_info["format"] = mark_safe(  # noqa: S308
                '<a href="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones">available options</a>'
            )
        elif isinstance(field, serializers.ManyRelatedField):
            if field.field_name == "tags":
                field_info["format"] = mark_safe('<code>"name,name"</code> or <code>"UUID,UUID"</code>')  # noqa: S308
            elif isinstance(field.child_relation, ContentTypeField):
                field_info["format"] = mark_safe('<code>"app_label.model,app_label.model"</code>')  # noqa: S308
            else:
                field_info["foreign_key"] = field.child_relation.queryset.model._meta.label_lower
                field_info["format"] = mark_safe('<code>"UUID,UUID"</code> or combination of fields')  # noqa: S308
        elif isinstance(field, serializers.RelatedField):
            if isinstance(field, ContentTypeField):
                field_info["format"] = mark_safe("<code>app_label.model</code>")  # noqa: S308
            else:
                field_info["foreign_key"] = field.queryset.model._meta.label_lower
                field_info["format"] = mark_safe("<code>UUID</code> or combination of fields")  # noqa: S308
        elif isinstance(field, (serializers.ListField, serializers.MultipleChoiceField)):
            field_info["format"] = mark_safe('<code>"value,value"</code>')  # noqa: S308
        elif isinstance(field, (serializers.DictField, serializers.JSONField)):
            pass  # Not trivial to specify a format as it could be a JSON dict or a comma-separated string

        if isinstance(field, ChoiceField):
            field_info["choices"] = field.choices

        fields.append(field_info)

    # Move all required fields to the start of the list
    # TODO this ordering should be defined by the serializer instead...
    fields = sorted(fields, key=lambda info: 1 if info["required"] else 2)
    return fields


def import_csv_helper(*, request, form, serializer_class):
    field_name = "csv_file" if request.FILES else "csv_data"
    csvtext = form.cleaned_data[field_name]
    try:
        data = NautobotCSVParser().parse(
            stream=BytesIO(csvtext.encode("utf-8")),
            parser_context={"request": request, "serializer_class": serializer_class},
        )
        new_objs = []
        validation_failed = False
        for row, entry in enumerate(data, start=1):
            serializer = serializer_class(data=entry, context={"request": request})
            if serializer.is_valid():
                new_objs.append(serializer.save())
            else:
                validation_failed = True
                for field, err in serializer.errors.items():
                    form.add_error(field_name, f"Row {row}: {field}: {err[0]}")
    except exceptions.ParseError as exc:
        validation_failed = True
        form.add_error(None, str(exc))

    if validation_failed:
        raise ValidationError("")

    return new_objs


def handle_protectederror(obj_list, request, e):
    """
    Generate a user-friendly error message in response to a ProtectedError exception.
    """
    protected_objects = list(e.protected_objects)
    protected_count = len(protected_objects) if len(protected_objects) <= 50 else "More than 50"
    err_message = format_html(
        "Unable to delete <strong>{}</strong>. {} dependent objects were found: ",
        ", ".join(str(obj) for obj in obj_list),
        protected_count,
    )

    # Format objects based on whether they have a detail view/absolute url
    objects_with_absolute_url = []
    objects_without_absolute_url = []
    # Append dependent objects to error message
    for dependent in protected_objects[:50]:
        try:
            dependent.get_absolute_url()
            objects_with_absolute_url.append(dependent)
        except AttributeError:
            objects_without_absolute_url.append(dependent)

    err_message += format_html_join(
        ", ",
        '<a href="{}">{}</a>',
        ((dependent.get_absolute_url(), dependent) for dependent in objects_with_absolute_url),
    )
    if objects_with_absolute_url and objects_without_absolute_url:
        err_message += format_html(", ")
    err_message += format_html_join(
        ", ",
        "<span>{}</span>",
        ((dependent,) for dependent in objects_without_absolute_url),
    )

    messages.error(request, err_message)


def prepare_cloned_fields(instance):
    """
    Compile an object's `clone_fields` list into a string of URL query parameters. Tags are automatically cloned where
    applicable.
    """
    form_class = get_form_for_model(instance)
    form = form_class() if form_class is not None else None
    params = []
    for field_name in getattr(instance, "clone_fields", []):
        field = instance._meta.get_field(field_name)
        field_value = field.value_from_object(instance)

        # For foreign-key fields, if the ModelForm's field has a defined `to_field_name`,
        # use that field from the related object instead of its PK.
        # Example: Location.parent, LocationForm().fields["parent"].to_field_name = "name", so use name rather than PK.
        if isinstance(field, ForeignKey):
            related_object = getattr(instance, field_name)
            if (
                related_object is not None
                and form is not None
                and field_name in form.fields
                and hasattr(form.fields[field_name], "to_field_name")
                and form.fields[field_name].to_field_name is not None
            ):
                field_value = getattr(related_object, form.fields[field_name].to_field_name)

        # Swap out False with URL-friendly value
        if field_value is False:
            field_value = ""

        # This is likely an m2m field
        if isinstance(field_value, list):
            for fv in field_value:
                item_value = getattr(fv, "pk", str(fv))  # pk or str()
                params.append((field_name, item_value))

        # Omit empty values
        elif field_value not in (None, ""):
            params.append((field_name, field_value))

    # Copy tags
    if is_taggable(instance):
        for tag in instance.tags.all():
            params.append(("tags", tag.pk))

    # Encode the parameters into a URL query string
    param_string = urllib.parse.urlencode(params)

    return param_string
