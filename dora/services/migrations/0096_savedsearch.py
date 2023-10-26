# Generated by Django 4.2.3 on 2023-10-05 08:12

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("services", "0095_remove_service_is_draft_remove_service_is_suggestion"),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedSearch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "city_code",
                    models.CharField(verbose_name="Code INSEE de la recherche"),
                ),
                ("city_label", models.CharField(verbose_name="Label de la ville")),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("NEVER", "Jamais"),
                            ("TWO_WEEKS", "Tous les 15 jours"),
                            ("MONTHLY", "Mensuel"),
                        ],
                        default="TWO_WEEKS",
                        max_length=10,
                        verbose_name="Fréquence",
                    ),
                ),
                (
                    "last_notification_date",
                    models.DateField(default=datetime.datetime.now),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.servicecategory",
                        verbose_name="Thématique",
                    ),
                ),
                (
                    "fees",
                    models.ManyToManyField(
                        blank=True,
                        to="services.servicefee",
                        verbose_name="Frais à charge",
                    ),
                ),
                (
                    "kinds",
                    models.ManyToManyField(
                        blank=True,
                        to="services.servicekind",
                        verbose_name="Type de service",
                    ),
                ),
                (
                    "subcategories",
                    models.ManyToManyField(
                        blank=True,
                        to="services.servicesubcategory",
                        verbose_name="Besoins",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Recherche sauvegardé",
                "verbose_name_plural": "Recherches sauvegardées",
            },
        ),
    ]