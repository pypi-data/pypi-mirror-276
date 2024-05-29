# Generated by Django 3.1.7 on 2021-04-01 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers

import nautobot.extras.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0001_initial_part_1"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="objectchange",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="changes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="jobresult",
            name="obj_type",
            field=models.ForeignKey(
                limit_choices_to=nautobot.extras.utils.FeatureQuery("job_results"),
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_results",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="jobresult",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="imageattachment",
            name="content_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
        ),
        migrations.AddField(
            model_name="gitrepository",
            name="tags",
            field=taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="exporttemplate",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=nautobot.extras.utils.FeatureQuery("export_templates"),
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="exporttemplate",
            name="owner_content_type",
            field=models.ForeignKey(
                blank=True,
                default=None,
                limit_choices_to=nautobot.extras.utils.FeatureQuery("export_template_owners"),
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="export_template_owners",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="customlink",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=nautobot.extras.utils.FeatureQuery("custom_links"),
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="customfieldchoice",
            name="field",
            field=models.ForeignKey(
                limit_choices_to=models.Q(type__in=["select", "multi-select"]),
                on_delete=django.db.models.deletion.CASCADE,
                related_name="choices",
                to="extras.customfield",
            ),
        ),
        migrations.AddField(
            model_name="customfield",
            name="content_types",
            field=models.ManyToManyField(
                limit_choices_to=nautobot.extras.utils.FeatureQuery("custom_fields"),
                related_name="custom_fields",
                to="contenttypes.ContentType",
            ),
        ),
    ]
