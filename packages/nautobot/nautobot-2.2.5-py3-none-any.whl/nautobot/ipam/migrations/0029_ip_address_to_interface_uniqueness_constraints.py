# Generated by Django 3.2.18 on 2023-05-25 19:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("virtualization", "0022_vminterface_timestamps_data_migration"),
        ("dcim", "0044_tagsfield"),
        ("ipam", "0028_tagsfield"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ipaddresstointerface",
            unique_together={("ip_address", "interface"), ("ip_address", "vm_interface")},
        ),
    ]
