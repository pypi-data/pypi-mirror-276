# Generated by Django 3.2.20 on 2023-09-14 01:54

from django.db import migrations, models

from NEMO.migrations_utils import create_news_for_version


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0048_version_4_6_3"),
    ]

    def new_version_news(apps, schema_editor):
        create_news_for_version(
            apps,
            "4.7.0",
            "The new version of the calendar allows users to view multiple tool feeds at once by checking the box next to each tool you would like to see.",
        )

    operations = [
        migrations.RunPython(new_version_news),
        migrations.AlterField(
            model_name="interlock",
            name="unit_id",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="Multiplier/Unit id/Bank"),
        ),
    ]
