# Generated by Django 3.2.23 on 2023-11-05 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFutbol', '0005_auto_20231105_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultado',
            name='resultado_partido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resultado_partido', to='appFutbol.partido'),
        ),
    ]
