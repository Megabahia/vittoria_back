# Generated by Django 3.1.7 on 2021-10-27 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_fichaTecnicaProductos', '0003_auto_20211026_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichatecnicaproductos',
            name='valor',
            field=models.CharField(max_length=150),
        ),
    ]
