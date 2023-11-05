# Generated by Django 3.2.23 on 2023-11-04 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localia', models.CharField(choices=[('LO', 'Local'), ('VI', 'Visitante')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Jugador_partido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ganar', models.CharField(choices=[('S', 'Sí'), ('N', 'No')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('estilo', models.CharField(choices=[(5, 'Fútbol sala'), (7, 'Fútbol 7'), (11, 'Fútbol 11')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('ubicacion', models.TextField()),
                ('telefono', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellidos', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('nivel', models.FloatField(db_column='puntos_usuario', default=0.0)),
                ('telefono', models.CharField(max_length=9)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Torneo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.equipo')),
                ('partidos', models.ManyToManyField(to='appFutbol.Partido')),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goles_local', models.IntegerField(verbose_name='Goles local')),
                ('goles_visitante', models.IntegerField(verbose_name='Goles visitante')),
                ('resultado_partido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.partido')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('estado', models.CharField(choices=[('F', 'Completo'), ('A', 'Disponible')], max_length=1)),
                ('tipo', models.CharField(choices=[('Pr', 'Privada'), ('Pu', 'Pública')], max_length=2)),
                ('n_jugadores', models.IntegerField()),
                ('campo_reservado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.recinto')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('creador_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='partido',
            name='reserva_partido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.reserva'),
        ),
        migrations.AddField(
            model_name='partido',
            name='usuarios_jugadores',
            field=models.ManyToManyField(through='appFutbol.Jugador_partido', to='appFutbol.Usuario'),
        ),
        migrations.AddField(
            model_name='jugador_partido',
            name='partido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.partido'),
        ),
        migrations.AddField(
            model_name='jugador_partido',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.usuario'),
        ),
        migrations.CreateModel(
            name='DatosUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('posicion', models.CharField(choices=[('GOA', 'Portero'), ('DEF', 'Defensa'), ('MID', 'Centrocampista'), ('STR', 'Delantero')], max_length=3)),
                ('ubicacion', models.TextField()),
                ('partidos_jugados', models.ManyToManyField(to='appFutbol.Partido')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.usuario')),
            ],
        ),
    ]
