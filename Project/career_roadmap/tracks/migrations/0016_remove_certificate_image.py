# Generated by Django 4.1.7 on 2023-05-04 01:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tracks", "0015_certificate_image_alter_certificate_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="certificate",
            name="image",
        ),
    ]