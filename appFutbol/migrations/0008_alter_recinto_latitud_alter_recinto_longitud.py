# Generated by Django 4.2.11 on 2024-03-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appFutbol", "0007_recinto_latitud_recinto_longitud"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recinto",
            name="latitud",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="recinto",
            name="longitud",
            field=models.FloatField(default=0),
        ),
    ]
