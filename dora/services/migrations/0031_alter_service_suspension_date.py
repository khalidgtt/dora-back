# Generated by Django 3.2.8 on 2021-11-24 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0030_auto_20211124_1609"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="suspension_date",
            field=models.DateField(
                blank=True, db_index=True, null=True, verbose_name="À partir d’une date"
            ),
        ),
    ]
