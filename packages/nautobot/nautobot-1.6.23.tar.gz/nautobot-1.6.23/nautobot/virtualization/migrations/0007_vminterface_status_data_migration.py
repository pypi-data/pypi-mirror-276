# Generated by Django 3.1.14 on 2022-03-19 23:21

from django.db import migrations
from nautobot.extras.management import clear_status_choices, populate_status_choices
from nautobot.virtualization.choices import VMInterfaceStatusChoices


def populate_vminterface_status(apps, schema_editor):
    """
    Create/link default Status records for the VMInterface content-type; default all VMInterfaces to "active" status.
    """
    # Create VMInterface Statuses and add dcim.VMInterface to its content_types
    populate_status_choices(apps, schema_editor, models=["virtualization.VMInterface"])

    Status = apps.get_model("extras.Status")
    VMInterface = apps.get_model("virtualization.VMInterface")

    # populate existing interfaces status
    active_status = Status.objects.get(slug=VMInterfaceStatusChoices.STATUS_ACTIVE)
    for interface in VMInterface.objects.all():
        interface.status = active_status
        interface.save()


def clear_vminterface_status(apps, schema_editor):
    """
    Clear the status field on all VMInterfaces; de-link/delete all Status records from the VMInterface content-type.
    """
    VMInterface = apps.get_model("virtualization.VMInterface")

    for interface in VMInterface.objects.filter(status__isnull=False):
        interface.status = None
        interface.save()

    clear_status_choices(apps, schema_editor, models=["virtualization.VMInterface"])


class Migration(migrations.Migration):
    dependencies = [
        ("virtualization", "0006_vminterface_status"),
    ]

    operations = [
        migrations.RunPython(populate_vminterface_status, clear_vminterface_status),
    ]
