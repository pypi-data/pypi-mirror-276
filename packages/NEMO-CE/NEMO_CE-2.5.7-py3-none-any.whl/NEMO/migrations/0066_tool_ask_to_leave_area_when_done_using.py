# Generated by Django 3.2.23 on 2024-03-13 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NEMO", "0065_door_adjacent_area"),
    ]

    operations = [
        migrations.AddField(
            model_name="tool",
            name="_ask_to_leave_area_when_done_using",
            field=models.BooleanField(
                db_column="ask_to_leave_area_when_done_using",
                default=False,
                help_text="Check this box to ask the user if they want to log out of the area when they are done using the tool.",
            ),
        ),
    ]
