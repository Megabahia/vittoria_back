# Generated by Django 3.1.7 on 2021-07-07 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_facturas', '0005_auto_20210628_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturasdetalles',
            name='codigo',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
