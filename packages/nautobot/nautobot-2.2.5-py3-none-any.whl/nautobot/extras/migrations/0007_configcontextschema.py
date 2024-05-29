# Generated by Django 3.1.12 on 2021-06-16 02:40

import uuid

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion

import nautobot.extras.utils


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0006_graphqlquery"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConfigContextSchema",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("description", models.CharField(max_length=200, blank=True)),
                ("slug", models.SlugField()),
                ("data_schema", models.JSONField()),
                ("owner_object_id", models.UUIDField(blank=True, default=None, null=True)),
                (
                    "owner_content_type",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        limit_choices_to=nautobot.extras.utils.FeatureQuery("config_context_owners"),
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="configcontext",
            name="schema",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="extras.configcontextschema"
            ),
        ),
    ]
