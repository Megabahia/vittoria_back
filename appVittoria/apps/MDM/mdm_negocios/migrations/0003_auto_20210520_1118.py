# Generated by Django 3.1.7 on 2021-05-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_negocios', '0002_auto_20210518_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalnegocios',
            name='cedula',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]