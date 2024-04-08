# Generated by Django 3.1.7 on 2024-01-23 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_facturas', '0008_facturasdetalles_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturasencabezados',
            name='callePrincipal',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='calleSecundaria',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='ciudad',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='numeroCasa',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='pais',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='provincia',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='facturasencabezados',
            name='referencia',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]