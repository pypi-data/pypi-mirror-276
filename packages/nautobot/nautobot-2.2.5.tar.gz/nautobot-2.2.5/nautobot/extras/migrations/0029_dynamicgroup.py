# Generated by Django 3.1.13 on 2021-10-31 18:38

import uuid

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion

import nautobot.core.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0028_job_reduce_source"),
    ]

    operations = [
        migrations.CreateModel(
            name="DynamicGroup",
            fields=[
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "slug",
                    nautobot.core.models.fields.AutoSlugField(
                        blank=True, max_length=100, populate_from="name", unique=True
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "filter",
                    models.JSONField(
                        default=dict,
                        editable=False,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["content_type", "name"],
            },
        ),
    ]
