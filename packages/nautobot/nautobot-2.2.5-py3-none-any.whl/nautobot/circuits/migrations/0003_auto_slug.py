# Generated by Django 3.1.13 on 2021-08-05 03:23

from django.db import migrations

import nautobot.core.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("circuits", "0002_initial_part_2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="circuittype",
            name="slug",
            field=nautobot.core.models.fields.AutoSlugField(
                blank=True, max_length=100, populate_from="name", unique=True
            ),
        ),
        migrations.AlterField(
            model_name="provider",
            name="slug",
            field=nautobot.core.models.fields.AutoSlugField(
                blank=True, max_length=100, populate_from="name", unique=True
            ),
        ),
    ]
