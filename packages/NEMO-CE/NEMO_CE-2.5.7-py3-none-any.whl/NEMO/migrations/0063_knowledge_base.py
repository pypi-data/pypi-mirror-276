# Generated by Django 3.2.23 on 2024-03-03 03:41

import django.db.models.deletion
from django.db import migrations, models

import NEMO.utilities


class Migration(migrations.Migration):
    dependencies = [
        ("NEMO", "0062_migrate_email_upcoming_reservation"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffKnowledgeBaseCategory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The unique name for this item", max_length=200, unique=True)),
                (
                    "display_order",
                    models.IntegerField(
                        help_text="The display order is used to sort these items. The lowest value category is displayed first."
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Staff knowledge base categories",
                "ordering": ["display_order", "name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StaffKnowledgeBaseItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The item name.", max_length=200)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="The description for this item. HTML can be used.", null=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        help_text="The category for this item.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="NEMO.staffknowledgebasecategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserKnowledgeBaseCategory",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The unique name for this item", max_length=200, unique=True)),
                (
                    "display_order",
                    models.IntegerField(
                        help_text="The display order is used to sort these items. The lowest value category is displayed first."
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "User knowledge base categories",
                "ordering": ["display_order", "name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserKnowledgeBaseItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The item name.", max_length=200)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="The description for this item. HTML can be used.", null=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        help_text="The category for this item.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="NEMO.userknowledgebasecategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserKnowledgeBaseItemDocuments",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=NEMO.utilities.document_filename_upload,
                        verbose_name="Document",
                    ),
                ),
                ("url", models.CharField(blank=True, max_length=200, null=True, verbose_name="URL")),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="The optional name to display for this document",
                        max_length=200,
                        null=True,
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "item",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="NEMO.userknowledgebaseitem"),
                ),
            ],
            options={
                "verbose_name_plural": "User knowledge base item documents",
                "ordering": ["-uploaded_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StaffKnowledgeBaseItemDocuments",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        max_length=255,
                        null=True,
                        upload_to=NEMO.utilities.document_filename_upload,
                        verbose_name="Document",
                    ),
                ),
                ("url", models.CharField(blank=True, max_length=200, null=True, verbose_name="URL")),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="The optional name to display for this document",
                        max_length=200,
                        null=True,
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "item",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="NEMO.staffknowledgebaseitem"),
                ),
            ],
            options={
                "verbose_name_plural": "Staff knowledge base item documents",
                "ordering": ["-uploaded_at"],
                "abstract": False,
            },
        ),
    ]
