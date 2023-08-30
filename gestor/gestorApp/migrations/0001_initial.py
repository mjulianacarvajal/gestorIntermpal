# Generated by Django 4.0.3 on 2023-07-23 22:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_bus', models.CharField(max_length=10)),
                ('asientos', models.FloatField(default=0, max_length=2)),
                ('estado', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default=1, max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('caracteristicas', models.TextField()),
                ('estado', models.CharField(choices=[('1', 'Activa'), ('2', 'Sin servicio')], default=1, max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sede', models.CharField(max_length=250)),
                ('tipo', models.CharField(choices=[('1', 'Terminal'), ('2', 'Oficina'), ('3', 'Paradero')], default='1', max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('programado', models.DateTimeField()),
                ('precio', models.IntegerField()),
                ('estado', models.CharField(choices=[('1', 'Programado'), ('2', 'Cancelado'), ('3', 'Abordando')], default=1, max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizado', models.DateTimeField(auto_now=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestorApp.bus')),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino', to='gestorApp.sede')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origen', to='gestorApp.sede')),
            ],
        ),
        migrations.CreateModel(
            name='Despachado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=250)),
                ('asientos', models.IntegerField()),
                ('estado', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Despachado')], default=1, max_length=2)),
                ('fecha_creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_actualizado', models.DateTimeField(auto_now=True)),
                ('programado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestorApp.programado')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestorApp.empresa'),
        ),
    ]