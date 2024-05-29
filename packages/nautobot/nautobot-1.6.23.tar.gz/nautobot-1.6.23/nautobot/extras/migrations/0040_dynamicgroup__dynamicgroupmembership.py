# Generated by Django 3.2.13 on 2022-06-09 16:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0039_objectchange__add_change_context"),
    ]

    operations = [
        migrations.CreateModel(
            name="DynamicGroupMembership",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("operator", models.CharField(max_length=12)),
                ("weight", models.PositiveSmallIntegerField()),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="extras.dynamicgroup",
                    ),
                ),
                (
                    "parent_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dynamic_group_memberships",
                        to="extras.dynamicgroup",
                    ),
                ),
            ],
            options={
                "ordering": ["parent_group", "weight", "group"],
            },
        ),
        migrations.AddField(
            model_name="dynamicgroup",
            name="children",
            field=models.ManyToManyField(
                related_name="parents", through="extras.DynamicGroupMembership", to="extras.DynamicGroup"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="dynamicgroupmembership",
            unique_together={("group", "parent_group", "operator", "weight")},
        ),
    ]
