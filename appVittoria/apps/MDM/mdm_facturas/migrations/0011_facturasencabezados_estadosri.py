# Generated by Django 3.1.7 on 2024-02-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_facturas', '0010_facturasencabezados_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturasencabezados',
            name='estadoSRI',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]