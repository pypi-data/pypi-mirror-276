# Generated by Django 3.1.14 on 2022-03-19 23:21

from django.db import migrations

from nautobot.extras.management import clear_status_choices, populate_status_choices


def populate_location_status(apps, schema_editor):
    """Create/link default Status records for the Location content-type."""
    populate_status_choices(apps, schema_editor, models=["dcim.Location"])


def clear_location_status(apps, schema_editor):
    """De-link/delete all Status records from the Location content-type."""
    clear_status_choices(apps, schema_editor, models=["dcim.Location"])


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0013_location_location_type"),
    ]

    operations = [
        migrations.RunPython(populate_location_status, clear_location_status),
    ]
