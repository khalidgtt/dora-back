# Generated by Django 4.0.6 on 2022-08-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("structures", "0047_alter_structure_modification_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="structure",
            name="moderation_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
