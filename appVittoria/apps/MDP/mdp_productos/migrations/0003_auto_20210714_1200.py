# Generated by Django 3.1.7 on 2021-07-14 17:00

import apps.MDP.mdp_productos.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0002_auto_20210709_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='variableRefil',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='ReporteStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaUltimaStock', models.DateTimeField(null=True)),
                ('montoCompra', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteRotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateTimeField(null=True)),
                ('fechaFin', models.DateTimeField(null=True)),
                ('diasPeriodo', models.IntegerField(max_length=150, null=True)),
                ('productosVendidos', models.IntegerField(max_length=150, null=True)),
                ('tipoRotacion', models.IntegerField(max_length=150, null=True)),
                ('montoVenta', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteRefil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diasRefil', models.IntegerField(max_length=150, null=True)),
                ('variableRefil', models.IntegerField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteCaducidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCaducidad', models.DateTimeField(null=True)),
                ('productosCaducados', models.IntegerField(max_length=150, null=True)),
                ('diasParaCaducar', models.IntegerField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteAbastecimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadSugeridaStock', models.CharField(max_length=150, null=True)),
                ('fechaMaximaStock', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoImagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=apps.MDP.mdp_productos.models.upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
    ]
