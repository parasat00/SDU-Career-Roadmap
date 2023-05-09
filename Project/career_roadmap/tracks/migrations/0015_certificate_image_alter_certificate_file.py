# Generated by Django 4.1.7 on 2023-05-04 01:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracks", "0014_alter_certificate_file_alter_multipleimage_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="certificate",
            name="image",
            field=models.ImageField(
                default="certificate_template.jpg", upload_to="uploads/certificates"
            ),
        ),
        migrations.AlterField(
            model_name="certificate",
            name="file",
            field=models.FileField(
                default="certificate_template.jpg", upload_to="uploads/certificates"
            ),
        ),
    ]