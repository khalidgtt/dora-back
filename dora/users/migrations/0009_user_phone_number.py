# Generated by Django 3.2.12 on 2022-02-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_user_is_bizdev"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]