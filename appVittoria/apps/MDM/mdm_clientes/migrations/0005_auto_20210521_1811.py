# Generated by Django 3.1.7 on 2021-05-21 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0004_parientes_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='estado',
            field=models.CharField(default='ACTIVO', max_length=200),
        ),
        migrations.AddField(
            model_name='parientes',
            name='estado',
            field=models.CharField(default='ACTIVO', max_length=200),
        ),
    ]
