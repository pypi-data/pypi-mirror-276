# Generated by Django 3.1.14 on 2022-03-19 23:21

from django.db import migrations
from nautobot.dcim.choices import InterfaceStatusChoices
from nautobot.extras.management import clear_status_choices, populate_status_choices


def populate_interface_status(apps, schema_editor):
    """
    Create/link default Status records for the Interface content-type, and default all Interfaces to "active" status.
    """
    # Create Interface Statuses and add dcim.Interface to its content_types
    populate_status_choices(apps, schema_editor, models=["dcim.Interface"])

    Status = apps.get_model("extras.Status")
    Interface = apps.get_model("dcim.Interface")

    # populate existing interfaces status
    active_status = Status.objects.get(slug=InterfaceStatusChoices.STATUS_ACTIVE)
    for interface in Interface.objects.all():
        interface.status = active_status
        interface.save()


def clear_interface_status(apps, schema_editor):
    """
    Clear the status field on all Interfaces, and de-link/delete all Status records from the Interface content-type.
    """
    Interface = apps.get_model("dcim.Interface")

    for interface in Interface.objects.filter(status__isnull=False):
        interface.status = None
        interface.save()

    clear_status_choices(apps, schema_editor, models=["dcim.Interface"])


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0010_interface_status"),
    ]

    operations = [
        migrations.RunPython(populate_interface_status, clear_interface_status),
    ]
