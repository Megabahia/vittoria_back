# Generated by Django 3.1.7 on 2024-02-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_gestionInventario', '0002_productos_fechaadquisicion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductosImagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(blank=True, max_length=255, null=True)),
                ('imagen', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
