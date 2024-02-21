# Generated by Django 3.1.7 on 2024-02-20 20:58

import apps.MDP.mdp_gestionInventario.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivosFacturas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(blank=True, null=True, upload_to=apps.MDP.mdp_gestionInventario.models.upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoBarras', models.CharField(blank=True, max_length=255, null=True)),
                ('nombreProducto', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('precioAdquisicion', models.CharField(blank=True, max_length=255, null=True)),
                ('cantidad', models.IntegerField(blank=True, default=0, null=True)),
                ('imagen', models.FileField(blank=True, null=True, upload_to=apps.MDP.mdp_gestionInventario.models.upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
