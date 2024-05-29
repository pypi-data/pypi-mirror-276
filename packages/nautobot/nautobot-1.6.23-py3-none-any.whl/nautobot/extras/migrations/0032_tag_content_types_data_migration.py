# Generated by Django 3.1.14 on 2022-03-19 23:21

from django.db import migrations
import nautobot.extras.utils


def populate_existing_tags(app, schema):
    """For backwards-compatibility, any pre-existing tags must be assumed to apply to all possible content-types."""

    Tag = app.get_model("extras", "Tag")
    content_types = nautobot.extras.utils.TaggableClassesQuery().get_choices()

    for tag in Tag.objects.filter(content_types__isnull=True):
        for _, pk in content_types:
            tag.content_types.add(pk)


def reverse_populate_tags(app, schema_editor):
    Tag = app.get_model("extras", "Tag")

    for tag in Tag.objects.filter(content_types__isnull=False):
        tag.content_types.clear()


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0031_tag_content_types"),
    ]

    operations = [
        migrations.RunPython(populate_existing_tags, reverse_populate_tags),
    ]
