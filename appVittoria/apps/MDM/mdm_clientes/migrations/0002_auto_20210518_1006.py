# Generated by Django 3.1.7 on 2021-05-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
