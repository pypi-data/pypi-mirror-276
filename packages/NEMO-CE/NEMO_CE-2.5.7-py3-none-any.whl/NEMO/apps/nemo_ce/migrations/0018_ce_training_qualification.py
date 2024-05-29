# Generated by Django 3.2.22 on 2024-02-23 03:46

from django.db import migrations, models
import django.db.models.deletion


from NEMO.apps.nemo_ce.migration_utils import NEMOMigration


class Migration(NEMOMigration):

    dependencies = [
        ("NEMO", "0056_version_5_2_0"),
        ("nemo_ce", "0017_ce_training_request_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingsession",
            name="qualification",
            field=models.ForeignKey(
                blank=True,
                help_text="The associated qualification if applicable",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="NEMO.qualification",
            ),
        ),
    ]
