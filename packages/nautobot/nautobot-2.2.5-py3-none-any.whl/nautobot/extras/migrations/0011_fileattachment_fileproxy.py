# Generated by Django 3.1.13 on 2021-07-16 21:44

import uuid

from django.db import migrations, models

import nautobot.extras.models.models


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0010_change_cf_validation_max_min_field_to_bigint"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileAttachment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("bytes", models.BinaryField()),
                ("filename", models.CharField(max_length=255)),
                ("mimetype", models.CharField(max_length=50)),
            ],
            options={"ordering": ["filename"]},
        ),
        migrations.CreateModel(
            name="FileProxy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "file",
                    models.FileField(
                        storage=nautobot.extras.models.models.database_storage,
                        upload_to="extras.FileAttachment/bytes/filename/mimetype",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "get_latest_by": "uploaded_at",
                "ordering": ["name"],
                "verbose_name_plural": "file proxies",
            },
        ),
        migrations.AlterModelOptions(
            name="jobresult",
            options={"get_latest_by": "created", "ordering": ["-created"]},
        ),
    ]
