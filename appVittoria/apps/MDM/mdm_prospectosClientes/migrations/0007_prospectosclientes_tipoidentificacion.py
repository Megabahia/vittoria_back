# Generated by Django 3.1.7 on 2024-01-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0006_auto_20240118_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='tipoIdentificacion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
