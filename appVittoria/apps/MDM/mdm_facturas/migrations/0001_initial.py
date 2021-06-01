# Generated by Django 3.1.7 on 2021-05-31 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mdm_clientes', '0006_auto_20210525_1150'),
        ('mdm_negocios', '0007_auto_20210525_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturasEncabezados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroFactura', models.CharField(max_length=150, null=True)),
                ('fecha', models.DateField(null=True)),
                ('tipoIdentificacion', models.CharField(max_length=150, null=True)),
                ('identificacion', models.CharField(max_length=150, null=True)),
                ('razonSocial', models.CharField(max_length=150, null=True)),
                ('direccion', models.CharField(max_length=150, null=True)),
                ('telefono', models.CharField(max_length=150, null=True)),
                ('correo', models.EmailField(max_length=150, null=True)),
                ('nombreVendedor', models.CharField(max_length=150, null=True)),
                ('subTotal', models.FloatField(null=True)),
                ('descuento', models.FloatField(null=True)),
                ('iva', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_clientes.clientes')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_negocios.negocios')),
            ],
        ),
        migrations.CreateModel(
            name='FacturasDetalles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=150, null=True)),
                ('valorUnitario', models.FloatField(null=True)),
                ('cantidad', models.PositiveIntegerField(null=True)),
                ('precio', models.FloatField(null=True)),
                ('informacionAdicinal', models.CharField(max_length=250, null=True)),
                ('descuento', models.FloatField(null=True)),
                ('impuesto', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('facturaEncabezado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='detalles', to='mdm_facturas.facturasencabezados')),
            ],
        ),
    ]