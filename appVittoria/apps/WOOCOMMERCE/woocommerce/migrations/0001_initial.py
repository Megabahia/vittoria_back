# Generated by Django 3.1.7 on 2024-02-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=255)),
                ('envioTotal', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
                ('facturacion', models.JSONField(null=True)),
                ('envio', models.JSONField(null=True)),
                ('metodoPago', models.CharField(max_length=255)),
                ('numeroPedido', models.CharField(max_length=255)),
                ('articulos', models.JSONField(null=True)),
                ('envios', models.JSONField(null=True)),
                ('json', models.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
