# Generated by Django 3.1.7 on 2024-08-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdc_gestor_contactos', '0013_contactos_numerocomprobantequeja'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactos',
            name='montoSubtotalAprobadoQueja',
            field=models.FloatField(null=True),
        ),
    ]
