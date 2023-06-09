# Generated by Django 4.1.7 on 2023-04-16 09:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
        ("tracks", "0007_category_track_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Track_review",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("body", models.TextField(blank=True, null=True)),
                ("rating", models.DecimalField(decimal_places=1, max_digits=2)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.profile"
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tracks.track"
                    ),
                ),
            ],
        ),
    ]
