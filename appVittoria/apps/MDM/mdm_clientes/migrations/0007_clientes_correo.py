# Generated by Django 3.1.7 on 2021-06-08 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0006_auto_20210525_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='correo',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
