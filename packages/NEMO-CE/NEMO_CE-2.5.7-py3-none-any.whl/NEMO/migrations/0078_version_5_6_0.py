# Generated by Django 3.2.25 on 2024-03-20 18:04

from django.db import migrations

from NEMO.migrations_utils import create_news_for_version


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0077_interlock_name"),
    ]

    def new_version_news(apps, schema_editor):
        create_news_for_version(apps, "5.6.0")

    operations = [
        migrations.RunPython(new_version_news),
    ]
