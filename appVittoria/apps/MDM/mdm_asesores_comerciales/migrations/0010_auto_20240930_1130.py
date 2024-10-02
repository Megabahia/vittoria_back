# Generated by Django 3.1.7 on 2024-09-30 16:30

import apps.MDM.mdm_asesores_comerciales.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_asesores_comerciales', '0009_asesorescomerciales_tipoidentificacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asesorescomerciales',
            name='movimientos',
        ),
        migrations.CreateModel(
            name='MovimientosAsesores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_movimiento', models.CharField(blank=True, max_length=250, null=True)),
                ('saldo', models.FloatField(null=True)),
                ('observaciones', models.CharField(blank=True, max_length=400, null=True)),
                ('archivo_comprobante', models.FileField(blank=True, null=True, upload_to=apps.MDM.mdm_asesores_comerciales.models.upload_path)),
                ('numero_transaccion', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('asesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdm_asesores_comerciales.asesorescomerciales')),
            ],
        ),
    ]