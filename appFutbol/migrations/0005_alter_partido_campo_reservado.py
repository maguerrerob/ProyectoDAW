# Generated by Django 4.2.8 on 2023-12-11 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appFutbol', '0004_alter_partido_campo_reservado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='campo_reservado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campo_reservadoo', to='appFutbol.recinto'),
        ),
    ]
