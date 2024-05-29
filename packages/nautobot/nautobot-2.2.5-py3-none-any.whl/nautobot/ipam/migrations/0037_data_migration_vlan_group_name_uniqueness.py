# Generated by Django 3.2.18 on 2023-06-07 16:31

from django.db import migrations

from nautobot.ipam.utils.migrations import increment_names_of_records_with_similar_names

DEFAULT_VLAN_GROUP_BASENAME = "Default VLAN Group"


def vlan_group_name_uniqueness_constraints(apps, schema_editor):
    VLANGroup = apps.get_model("ipam", "vlangroup")

    increment_names_of_records_with_similar_names(VLANGroup)


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0036_add_uniqueness_constraints_to_service"),
    ]

    operations = [
        migrations.RunPython(
            vlan_group_name_uniqueness_constraints,
            migrations.operations.special.RunPython.noop,
        )
    ]
