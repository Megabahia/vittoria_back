# Generated by Django 3.1.7 on 2021-05-19 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospectosclientes',
            name='precio',
            field=models.FloatField(null=True),
        ),
    ]