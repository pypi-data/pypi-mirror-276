# Generated by Django 3.1.13 on 2021-08-20 02:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0012_healthchecktestmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="computedfield",
            name="fallback_value",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
