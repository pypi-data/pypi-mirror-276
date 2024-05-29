# Generated by Django 3.2.19 on 2023-09-26 19:08

from django.db import migrations, models

from NEMO.apps.nemo_ce.migration_utils import NEMOMigration


class Migration(NEMOMigration):

    dependencies = [
        ("NEMO", "0050_consumable_add_self_checkout_and_notes"),
        ("nemo_ce", "0009_ce_add_tool_grant_qualification_levels"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingevent",
            name="invitation_only",
            field=models.BooleanField(
                default=False, help_text="If checked, users can only register if they have been invited"
            ),
        ),
        migrations.AlterField(
            model_name="trainingevent",
            name="recorded",
            field=models.BooleanField(
                default=False, help_text="Indicates this training event has completed and training session was recorded"
            ),
        ),
    ]
