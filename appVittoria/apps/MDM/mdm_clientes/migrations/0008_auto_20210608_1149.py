# Generated by Django 3.1.7 on 2021-06-08 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_clientes', '0007_clientes_correo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientes',
            old_name='apellidos',
            new_name='nombreCompleto',
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='nombres',
        ),
    ]