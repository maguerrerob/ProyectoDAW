# Generated by Django 4.2.11 on 2024-03-10 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFutbol', '0008_alter_recinto_latitud_alter_recinto_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosusuario',
            name='amigos',
            field=models.ManyToManyField(to='appFutbol.cliente'),
        ),
    ]
