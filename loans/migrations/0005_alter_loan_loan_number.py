# Generated by Django 4.2.6 on 2023-10-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("loans", "0004_loan_loan_number_alter_amortizationschedule_loan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="loan_number",
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]