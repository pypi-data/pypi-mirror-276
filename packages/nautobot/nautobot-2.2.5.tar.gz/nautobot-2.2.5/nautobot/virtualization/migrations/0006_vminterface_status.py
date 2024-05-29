# Generated by Django 3.2.13 on 2022-05-04 21:21

from django.db import migrations
import django.db.models.deletion

import nautobot.extras.models.statuses


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("virtualization", "0005_add_natural_indexing"),
    ]

    operations = [
        migrations.AddField(
            model_name="vminterface",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="virtualization_vminterface_related",
                to="extras.status",
            ),
        ),
    ]
