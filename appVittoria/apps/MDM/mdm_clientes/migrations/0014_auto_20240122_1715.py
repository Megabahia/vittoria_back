# Generated by Django 3.1.7 on 2024-01-22 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0013_auto_20211025_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
