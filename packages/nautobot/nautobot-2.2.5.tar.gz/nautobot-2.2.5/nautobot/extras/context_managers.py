from contextlib import contextmanager
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.test.client import RequestFactory

from nautobot.extras.choices import ObjectChangeEventContextChoices
from nautobot.extras.constants import CHANGELOG_MAX_CHANGE_CONTEXT_DETAIL
from nautobot.extras.models import ObjectChange
from nautobot.extras.signals import change_context_state, get_user_if_authenticated
from nautobot.extras.webhooks import enqueue_webhooks


class ChangeContext:
    """
    ChangeContext is used to describe a single transaction that may be related
    to one or more object changes. A unique id can be provided, otherwise
    one will be generated to relate any changes to this transaction. Convenience
    classes are provided for each context.

    :param user: User object
    :param request: WSGIRequest object to retrieve user from django rest framework after authentication is performed
    :param context: Context of the transaction, must match a choice in nautobot.extras.choices.ObjectChangeEventContextChoices
    :param context_detail: Optional extra details about the transaction (ex: the plugin name that initiated the change)
    :param change_id: Optional uuid object to uniquely identify the transaction. One will be generated if not supplied
    """

    defer_object_changes = False  # advanced usage, for creating object changes in bulk

    def __init__(self, user=None, request=None, context=None, context_detail="", change_id=None):
        self.request = request
        self.user = user
        self.reset_deferred_object_changes()

        if self.request is None and self.user is None:
            raise TypeError("Either user or request must be provided")

        if self.request is not None and self.user is not None:
            raise TypeError("Request and user cannot be used together")

        if context is not None:
            self.context = context
        if self.context not in ObjectChangeEventContextChoices.values():
            raise ValueError("Context must be a choice within ObjectChangeEventContextChoices")

        self.context_detail = context_detail

        self.change_id = change_id
        if self.change_id is None:
            self.change_id = uuid.uuid4()

    def get_user(self, instance=None):
        """Return self.user if set, otherwise return self.request.user"""
        if self.user is not None:
            return get_user_if_authenticated(self.user, instance)
        return get_user_if_authenticated(self.request.user, instance)

    def as_dict(self, instance=None):
        """
        Return ChangeContext attributes in dictionary format
        """
        context = {
            "user": self.get_user(instance),
            "change_id": self.change_id,
            "context": self.context,
        }
        return context

    def _object_change_batch(self, n):
        # Return first n keys from the self.deferred_object_changes dict
        keys = []
        for i, k in enumerate(self.deferred_object_changes.keys()):
            if i >= n:
                return keys
            keys.append(k)
        return keys

    def reset_deferred_object_changes(self):
        self.deferred_object_changes = {}

    def flush_deferred_object_changes(self, batch_size=1000):
        if self.defer_object_changes:
            self.create_object_changes(batch_size=batch_size)

    def create_object_changes(self, batch_size=1000):
        while self.deferred_object_changes:
            create_object_changes = []
            for key in self._object_change_batch(batch_size):
                for entry in self.deferred_object_changes[key]:
                    objectchange = entry["instance"].to_objectchange(entry["action"])
                    objectchange.user = entry["user"]
                    objectchange.user_name = objectchange.user.username
                    objectchange.request_id = self.change_id
                    objectchange.change_context = self.context
                    objectchange.change_context_detail = self.context_detail[:CHANGELOG_MAX_CHANGE_CONTEXT_DETAIL]
                    if not objectchange.changed_object_id:
                        objectchange.changed_object_id = entry.get("changed_object_id")
                    create_object_changes.append(objectchange)
                self.deferred_object_changes.pop(key, None)
            ObjectChange.objects.bulk_create(create_object_changes, batch_size=batch_size)


class JobChangeContext(ChangeContext):
    """ChangeContext for changes made by jobs"""

    context = ObjectChangeEventContextChoices.CONTEXT_JOB


class JobHookChangeContext(ChangeContext):
    """ChangeContext for changes made by job hooks"""

    context = ObjectChangeEventContextChoices.CONTEXT_JOB_HOOK


class ORMChangeContext(ChangeContext):
    """ChangeContext for changes made with web_request_context context manager"""

    context = ObjectChangeEventContextChoices.CONTEXT_ORM


class WebChangeContext(ChangeContext):
    """ChangeContext for changes made through the web interface"""

    context = ObjectChangeEventContextChoices.CONTEXT_WEB


@contextmanager
def change_logging(change_context):
    """
    Enable change logging by connecting the appropriate signals to their receivers before code is run, and
    disconnecting them afterward.

    :param change_context: ChangeContext instance
    """

    # Set change logging state
    prev_state = change_context_state.set(change_context)

    try:
        yield
    finally:
        # Reset change logging state. This is necessary to avoid recording any errant
        # changes during test cleanup.
        change_context_state.reset(prev_state)


@contextmanager
def web_request_context(
    user, context_detail="", change_id=None, context=ObjectChangeEventContextChoices.CONTEXT_ORM, request=None
):
    """
    Emulate the context of an HTTP request, which provides functions like change logging and webhook processing
    in response to data changes. This context manager is for use with low level utility tooling, such as the
    'nautobot-server nbshell' management command.

    By default, when working with the Django ORM, neither change logging nor webhook processing occur
    unless manually invoked and this context manager handles those functions. A valid User object must be provided.

    Example usage:

    >>> from nautobot.extras.context_managers import web_request_context
    >>> user = User.objects.get(username="admin")
    >>> with web_request_context(user, context_detail="manual-fix"):
    ...     lt = Location.objects.get(name="Root")
    ...     lax = Location(name="LAX", location_type=lt)
    ...     lax.validated_save()

    :param user: User object
    :param context_detail: Optional extra details about the transaction (ex: the plugin name that initiated the change)
    :param change_id: Optional uuid object to uniquely identify the transaction. One will be generated if not supplied
    :param context: Optional string value of the generated change log entries' "change_context" field, defaults to ObjectChangeEventContextChoices.CONTEXT_ORM.
        Valid choices are in nautobot.extras.choices.ObjectChangeEventContextChoices
    :param request: Optional web request instance, one will be generated if not supplied
    """
    from nautobot.extras.jobs import enqueue_job_hooks  # prevent circular import

    valid_contexts = {
        ObjectChangeEventContextChoices.CONTEXT_JOB: JobChangeContext,
        ObjectChangeEventContextChoices.CONTEXT_JOB_HOOK: JobHookChangeContext,
        ObjectChangeEventContextChoices.CONTEXT_ORM: ORMChangeContext,
        ObjectChangeEventContextChoices.CONTEXT_WEB: WebChangeContext,
    }

    if context not in valid_contexts:
        raise TypeError(f"{context} is not a valid context")

    if not isinstance(user, (get_user_model(), AnonymousUser)):
        raise TypeError(f"{user} is not a valid user object")

    if request is None:
        request = RequestFactory().request(SERVER_NAME="web_request_context")
        request.user = user
    change_context = valid_contexts[context](request=request, context_detail=context_detail, change_id=change_id)
    try:
        with change_logging(change_context):
            yield request
    finally:
        # enqueue jobhooks and webhooks, use change_context.change_id in case change_id was not supplied
        for object_change in ObjectChange.objects.filter(request_id=change_context.change_id).iterator():
            enqueue_job_hooks(object_change)
            enqueue_webhooks(object_change)


@contextmanager
def deferred_change_logging_for_bulk_operation():
    """
    Defers change logging until the end of the context manager to improve performance. For use with bulk edit views. This
    context manager is wrapped in an atomic transaction.
    """

    change_context = change_context_state.get()
    if change_context is None:
        raise ValueError("Change logging must be enabled before using deferred_change_logging_for_bulk_operation")

    with transaction.atomic():
        try:
            change_context.defer_object_changes = True
            yield
            change_context.flush_deferred_object_changes()
        finally:
            change_context.defer_object_changes = False
            change_context.reset_deferred_object_changes()
