# Generated by Django 3.2.11 on 2022-02-07 11:04

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("admin_express", "0003_auto_20220207_1111"),
    ]

    operations = [
        TrigramExtension(),
    ]
