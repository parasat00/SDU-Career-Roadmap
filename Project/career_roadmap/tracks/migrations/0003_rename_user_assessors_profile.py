# Generated by Django 4.1.7 on 2023-04-06 10:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tracks", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assessors",
            old_name="user",
            new_name="profile",
        ),
    ]