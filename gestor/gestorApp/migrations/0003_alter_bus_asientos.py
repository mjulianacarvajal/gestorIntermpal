# Generated by Django 4.0.3 on 2023-08-02 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestorApp', '0002_alter_despachado_asientos_alter_programado_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='asientos',
            field=models.IntegerField(default=0),
        ),
    ]