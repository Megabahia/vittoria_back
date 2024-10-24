# Generated by Django 3.1.7 on 2024-10-24 14:35

import apps.MDP.mdp_proveedores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=150, null=True)),
                ('apellido', models.CharField(blank=True, max_length=150, null=True)),
                ('pais', models.CharField(blank=True, max_length=150, null=True)),
                ('provincia', models.CharField(blank=True, max_length=150, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('codigo', models.CharField(blank=True, max_length=15, null=True)),
                ('imagen', models.FileField(blank=True, null=True, upload_to=apps.MDP.mdp_proveedores.models.upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
