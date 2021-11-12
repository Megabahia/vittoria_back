# Generated by Django 3.1.7 on 2021-11-12 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gde_gestionEntrega', '0002_auto_20211025_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='oferta',
            name='identificacion',
            field=models.CharField(max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='ofertadetalles',
            name='cantidad',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
