# Generated by Django 3.1.14 on 2022-03-15 11:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0029_dynamicgroup"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="webhook",
            unique_together=set(),
        ),
    ]
