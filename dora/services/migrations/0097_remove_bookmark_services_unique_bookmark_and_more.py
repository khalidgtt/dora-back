# Generated by Django 4.2.5 on 2023-10-19 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0096_savedsearch"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="bookmark",
            name="services_unique_bookmark",
        ),
        migrations.AddField(
            model_name="bookmark",
            name="di_id",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="bookmark",
            name="service",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="services.service",
            ),
        ),
        migrations.AddConstraint(
            model_name="bookmark",
            constraint=models.UniqueConstraint(
                condition=models.Q(("service__isnull", False)),
                fields=("user", "service"),
                name="services_unique_service_bookmark",
            ),
        ),
        migrations.AddConstraint(
            model_name="bookmark",
            constraint=models.UniqueConstraint(
                condition=models.Q(("di_id", ""), _negated=True),
                fields=("user", "di_id"),
                name="services_unique_di_bookmark",
            ),
        ),
    ]