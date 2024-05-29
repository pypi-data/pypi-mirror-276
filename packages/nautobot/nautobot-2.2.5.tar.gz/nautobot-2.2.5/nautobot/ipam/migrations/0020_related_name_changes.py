# Generated by Django 3.2.18 on 2023-02-23 21:44

from django.db import migrations
import django.db.models.deletion

import nautobot.extras.models.roles
import nautobot.extras.models.statuses


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0069_created_datetime"),
        ("ipam", "0019_created_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ipaddress",
            name="role",
            field=nautobot.extras.models.roles.RoleField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ip_addresses",
                to="extras.role",
            ),
        ),
        migrations.AlterField(
            model_name="ipaddress",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="ip_addresses", to="extras.status"
            ),
        ),
        migrations.AlterField(
            model_name="prefix",
            name="role",
            field=nautobot.extras.models.roles.RoleField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="prefixes",
                to="extras.role",
            ),
        ),
        migrations.AlterField(
            model_name="prefix",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="prefixes", to="extras.status"
            ),
        ),
        migrations.AlterField(
            model_name="vlan",
            name="role",
            field=nautobot.extras.models.roles.RoleField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="vlans",
                to="extras.role",
            ),
        ),
        migrations.AlterField(
            model_name="vlan",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                null=True, on_delete=django.db.models.deletion.PROTECT, related_name="vlans", to="extras.status"
            ),
        ),
    ]
