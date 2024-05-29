# Generated by Django 3.2.18 on 2023-03-14 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0030_ipam__namespaces"),
        ("virtualization", "0022_vminterface_timestamps_data_migration"),
    ]

    operations = [
        migrations.AddField(
            model_name="vminterface",
            name="vrf",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vm_interfaces",
                to="ipam.vrf",
            ),
        ),
    ]
