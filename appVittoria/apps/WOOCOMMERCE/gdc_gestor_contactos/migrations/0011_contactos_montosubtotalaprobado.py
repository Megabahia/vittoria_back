# Generated by Django 3.1.7 on 2024-08-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdc_gestor_contactos', '0010_auto_20240731_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactos',
            name='montoSubtotalAprobado',
            field=models.FloatField(null=True),
        ),
    ]
