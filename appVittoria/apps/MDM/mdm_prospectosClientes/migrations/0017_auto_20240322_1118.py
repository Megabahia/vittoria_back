# Generated by Django 3.1.7 on 2024-03-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0016_prospectosclientes_articulos'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='canalOrigen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='metodoPago',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
