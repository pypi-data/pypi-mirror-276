# Generated by Django 3.2.25 on 2024-05-10 16:52

from django.db import migrations, models


from NEMO.apps.nemo_ce.migration_utils import NEMOMigration


class Migration(NEMOMigration):

    dependencies = [
        ("NEMO", "0079_user_active_access_expiration_verbose_names"),
        ("nemo_ce", "0019_tool_training_details_without_area_access"),
    ]

    operations = [
        migrations.AddField(
            model_name="tooltrainingdetail",
            name="auto_cancel",
            field=models.IntegerField(
                blank=True,
                help_text="The training auto-cancel time for this tool in hours. Leave blank to use the default or set to '-1' to disable auto cancel, overriding default time",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="trainingevent",
            name="auto_cancel",
            field=models.DateTimeField(
                blank=True, help_text="Deadline for automatic cancellation, if no user registered before.", null=True
            ),
        ),
    ]
