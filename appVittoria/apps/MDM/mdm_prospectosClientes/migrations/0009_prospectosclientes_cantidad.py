# Generated by Django 3.1.7 on 2024-01-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0008_auto_20240120_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
