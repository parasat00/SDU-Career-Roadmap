# Generated by Django 4.1.7 on 2023-04-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracks", "0003_rename_user_assessors_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="track",
            name="short_intro",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
