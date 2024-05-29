# Generated by Django 3.2.18 on 2023-03-15 17:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0073_job__unique_name_data_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="job",
            unique_together={("module_name", "job_class_name")},
        ),
        migrations.RemoveField(
            model_name="job",
            name="git_repository",
        ),
        migrations.RemoveField(
            model_name="job",
            name="slug",
        ),
        migrations.RemoveField(
            model_name="job",
            name="source",
        ),
    ]
