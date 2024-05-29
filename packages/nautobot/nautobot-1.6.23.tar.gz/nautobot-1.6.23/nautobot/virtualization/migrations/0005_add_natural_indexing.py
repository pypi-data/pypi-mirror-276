# Generated by Django 3.2.12 on 2022-04-15 17:39

from django.db import migrations, models
import nautobot.utilities.fields
import nautobot.utilities.ordering


class Migration(migrations.Migration):
    dependencies = [
        ("virtualization", "0004_auto_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="virtualmachine",
            name="name",
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name="vminterface",
            name="_name",
            field=nautobot.utilities.fields.NaturalOrderingField(
                "name",
                blank=True,
                db_index=True,
                max_length=100,
                naturalize_function=nautobot.utilities.ordering.naturalize_interface,
            ),
        ),
        migrations.AlterField(
            model_name="vminterface",
            name="name",
            field=models.CharField(db_index=True, max_length=64),
        ),
    ]
