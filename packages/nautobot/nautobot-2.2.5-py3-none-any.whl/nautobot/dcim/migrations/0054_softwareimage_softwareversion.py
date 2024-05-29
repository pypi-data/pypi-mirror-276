# Generated by Django 3.2.23 on 2024-02-15 17:20

import uuid

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion

import nautobot.core.models.fields
import nautobot.extras.models.mixins
import nautobot.extras.models.statuses


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0104_contact_contactassociation_team"),
        ("dcim", "0053_create_device_family_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="SoftwareVersion",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("version", models.CharField(max_length=255)),
                ("alias", models.CharField(blank=True, max_length=255)),
                ("release_date", models.DateField(blank=True, null=True)),
                ("end_of_support_date", models.DateField(blank=True, null=True)),
                ("documentation_url", models.URLField(blank=True)),
                ("long_term_support", models.BooleanField(default=False)),
                ("pre_release", models.BooleanField(default=False)),
                ("platform", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="dcim.platform")),
                (
                    "status",
                    nautobot.extras.models.statuses.StatusField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="software_versions",
                        to="extras.status",
                    ),
                ),
                ("tags", nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ("platform", "version", "end_of_support_date", "release_date"),
                "unique_together": {("platform", "version")},
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="SoftwareImageFile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("image_file_name", models.CharField(max_length=255)),
                ("image_file_checksum", models.CharField(blank=True, max_length=256)),
                ("hashing_algorithm", models.CharField(blank=True, max_length=255)),
                ("image_file_size", models.PositiveBigIntegerField(blank=True, null=True)),
                ("download_url", models.URLField(blank=True)),
                ("default_image", models.BooleanField(default=False)),
                (
                    "software_version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="software_image_files",
                        to="dcim.softwareversion",
                    ),
                ),
                (
                    "status",
                    nautobot.extras.models.statuses.StatusField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="software_image_files",
                        to="extras.status",
                    ),
                ),
                ("tags", nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ("software_version", "image_file_name"),
                "unique_together": {("image_file_name", "software_version")},
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="DeviceTypeToSoftwareImageFile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "device_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="software_image_file_mappings",
                        to="dcim.devicetype",
                    ),
                ),
                (
                    "software_image_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="device_type_mappings",
                        to="dcim.softwareimagefile",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, null=True),
                ),
            ],
            options={
                "verbose_name": "device type to software image file mapping",
                "verbose_name_plural": "device type to software image file mappings",
                "unique_together": {("device_type", "software_image_file")},
            },
        ),
        migrations.AddField(
            model_name="device",
            name="software_image_files",
            field=models.ManyToManyField(blank=True, related_name="devices", to="dcim.SoftwareImageFile"),
        ),
        migrations.AddField(
            model_name="device",
            name="software_version",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="devices",
                to="dcim.softwareversion",
            ),
        ),
        migrations.AddField(
            model_name="devicetype",
            name="software_image_files",
            field=models.ManyToManyField(
                blank=True,
                related_name="device_types",
                through="dcim.DeviceTypeToSoftwareImageFile",
                to="dcim.SoftwareImageFile",
            ),
        ),
        migrations.AddField(
            model_name="inventoryitem",
            name="software_image_files",
            field=models.ManyToManyField(blank=True, related_name="inventory_items", to="dcim.SoftwareImageFile"),
        ),
        migrations.AddField(
            model_name="inventoryitem",
            name="software_version",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="inventory_items",
                to="dcim.softwareversion",
            ),
        ),
    ]
