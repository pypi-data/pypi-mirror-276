# Generated by Django 3.2.18 on 2023-06-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_ensure_object_permission_names_are_unique"),
    ]

    operations = [
        migrations.AlterField(
            model_name="objectpermission",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
