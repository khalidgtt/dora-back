# Generated by Django 4.0.7 on 2022-09-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0071_convert_history"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="can_update_categories",
            field=models.BooleanField(default=True),
        ),
    ]
