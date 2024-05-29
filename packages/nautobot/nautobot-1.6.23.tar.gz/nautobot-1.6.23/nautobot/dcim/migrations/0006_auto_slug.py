# Generated by Django 3.1.13 on 2021-08-05 19:24

from django.db import migrations
import nautobot.core.fields


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0005_device_local_context_schema"),
    ]

    operations = [
        migrations.AlterField(
            model_name="devicerole",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
        migrations.AlterField(
            model_name="devicetype",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="model", unique=None),
        ),
        migrations.AlterField(
            model_name="manufacturer",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
        migrations.AlterField(
            model_name="platform",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
        migrations.AlterField(
            model_name="rackgroup",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=None),
        ),
        migrations.AlterField(
            model_name="rackrole",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
        migrations.AlterField(
            model_name="region",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
        migrations.AlterField(
            model_name="site",
            name="slug",
            field=nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
        ),
    ]
