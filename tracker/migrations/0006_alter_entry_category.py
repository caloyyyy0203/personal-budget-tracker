# Generated by Django 5.2 on 2025-04-28 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0005_alter_entry_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entry",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tracker.category",
            ),
        ),
    ]
