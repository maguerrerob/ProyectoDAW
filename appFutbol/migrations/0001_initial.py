# Generated by Django 4.2.8 on 2023-12-08 18:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador_partido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('ganar', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('estado', models.CharField(choices=[('F', 'Completo'), ('A', 'Disponible')], default='A', max_length=1)),
                ('tipo', models.CharField(choices=[('Pr', 'Privada'), ('Pu', 'Pública')], max_length=2)),
                ('n_jugadores', models.IntegerField()),
                ('estilo', models.CharField(choices=[(5, 'Fútbol sala'), (7, 'Fútbol 7'), (11, 'Fútbol 11')], max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.TextField()),
                ('ubicacion', models.TextField()),
                ('telefono', models.CharField(max_length=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('nivel', models.FloatField(db_column='puntos_usuario', default=0.0)),
                ('telefono', models.CharField(max_length=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Votacion_partido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('puntuacion_numerica', models.IntegerField()),
                ('comentario', models.TextField()),
                ('fecha_votacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('creador_votacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votacion_usuario', to='appFutbol.usuario')),
                ('partido_votado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votacion_partido', to='appFutbol.partido')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('goles_local', models.IntegerField(verbose_name='Goles local')),
                ('goles_visitante', models.IntegerField(verbose_name='Goles visitante')),
                ('resultado_partido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resultado_partido', to='appFutbol.partido')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('contenido', models.TextField()),
                ('creador_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_post', to='appFutbol.usuario')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='partido',
            name='campo_reservado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.recinto'),
        ),
        migrations.AddField(
            model_name='partido',
            name='creador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_partido', to='appFutbol.usuario'),
        ),
        migrations.AddField(
            model_name='partido',
            name='usuarios_jugadores',
            field=models.ManyToManyField(related_name='jugadores_partido', through='appFutbol.Jugador_partido', to='appFutbol.usuario'),
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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('descripcion', models.TextField()),
                ('posicion', models.CharField(choices=[('GOA', 'Portero'), ('DEF', 'Defensa'), ('MID', 'Centrocampista'), ('STR', 'Delantero')], max_length=3)),
                ('ubicacion', models.TextField()),
                ('partidos_jugados', models.ManyToManyField(to='appFutbol.partido')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='datos_usuario', to='appFutbol.usuario')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cuenta_bancaria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_state', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('numero_cuenta', models.IntegerField()),
                ('banco', models.CharField(choices=[('CA', 'Caixa'), ('BB', 'BBVA'), ('UN', 'Unicaja'), ('IN', 'ING')], max_length=2)),
                ('titular_cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appFutbol.usuario')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
