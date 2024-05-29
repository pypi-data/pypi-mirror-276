# Generated by Django 3.1.14 on 2022-01-20 17:12

import uuid

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers

import nautobot.core.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("dcim", "0008_increase_all_serial_lengths"),
        ("extras", "0021_customfield_changelog_data"),
        ("circuits", "0004_increase_provider_account_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="circuit",
            name="termination_a",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="circuits.circuittermination",
            ),
        ),
        migrations.AddField(
            model_name="circuit",
            name="termination_z",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="circuits.circuittermination",
            ),
        ),
        migrations.AlterField(
            model_name="circuittermination",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="circuit_terminations",
                to="dcim.site",
            ),
        ),
        migrations.CreateModel(
            name="ProviderNetwork",
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
                ("name", models.CharField(max_length=100)),
                (
                    "slug",
                    nautobot.core.models.fields.AutoSlugField(
                        blank=True, max_length=100, populate_from="name", unique=True
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="provider_networks",
                        to="circuits.provider",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ("provider", "name"),
            },
        ),
        migrations.AddField(
            model_name="circuittermination",
            name="provider_network",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="circuit_terminations",
                to="circuits.providernetwork",
            ),
        ),
        migrations.AddConstraint(
            model_name="providernetwork",
            constraint=models.UniqueConstraint(
                fields=("provider", "name"), name="circuits_providernetwork_provider_name"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="providernetwork",
            unique_together={("provider", "name")},
        ),
    ]
