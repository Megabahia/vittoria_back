# Generated by Django 3.1.7 on 2021-04-29 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vittoria_roles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roles',
            name='permisoAdmin',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='permisoGDE',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='permisoGDO',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='permisoMDM',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='permisoMDO',
        ),
        migrations.RemoveField(
            model_name='roles',
            name='permisoMDP',
        ),
    ]
