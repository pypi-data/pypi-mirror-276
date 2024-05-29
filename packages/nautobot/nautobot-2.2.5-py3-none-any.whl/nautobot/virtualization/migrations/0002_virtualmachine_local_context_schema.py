# Generated by Django 3.1.12 on 2021-06-16 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0007_configcontextschema"),
        ("virtualization", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="virtualmachine",
            name="local_context_schema",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="extras.configcontextschema"
            ),
        ),
    ]
