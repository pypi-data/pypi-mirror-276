# Generated by Django 3.2.16 on 2023-01-26 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0008_prefix_vlan_vlangroup_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vlan",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
