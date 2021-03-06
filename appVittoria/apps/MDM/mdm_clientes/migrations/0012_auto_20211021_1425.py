# Generated by Django 3.1.7 on 2021-10-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0011_auto_20211021_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='correo',
            field=models.EmailField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='nombreCompleto',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='datosfisicosclientes',
            name='piso',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datosvirtualesclientes',
            name='informacion',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
    ]
