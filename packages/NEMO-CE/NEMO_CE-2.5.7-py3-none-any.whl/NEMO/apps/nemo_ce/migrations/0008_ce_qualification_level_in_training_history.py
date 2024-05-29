# Generated by Django 3.2.19 on 2023-05-25 20:21

from django.db import migrations, models

from NEMO.apps.nemo_ce.migration_utils import NEMOMigration


class Migration(NEMOMigration):

    dependencies = [
        ("NEMO", "0045_version_4_5_5"),
        ("nemo_ce", "0007_ce_recording_training_events"),
    ]

    operations = [
        migrations.AddField(
            model_name="traininghistory",
            name="qualification_level",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
