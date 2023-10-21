# Generated by Django 4.2.6 on 2023-10-20 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "annual_interest_rate",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                ("start_date", models.DateField()),
                ("term", models.IntegerField()),
                (
                    "payment_frequency",
                    models.CharField(
                        choices=[("Monthly", "Monthly")],
                        default="Monthly",
                        max_length=10,
                    ),
                ),
                (
                    "cpr",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "monthly_interest_rate",
                    models.DecimalField(
                        decimal_places=2, editable=False, max_digits=5
                    ),
                ),
                (
                    "monthly_payment",
                    models.DecimalField(
                        decimal_places=2, editable=False, max_digits=12
                    ),
                ),
                (
                    "smm",
                    models.DecimalField(
                        decimal_places=2,
                        editable=False,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
            ],
        ),
    ]