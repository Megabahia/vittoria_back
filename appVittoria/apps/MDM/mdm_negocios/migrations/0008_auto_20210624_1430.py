# Generated by Django 3.1.7 on 2021-06-24 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_negocios', '0007_auto_20210525_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='negocios',
            old_name='provincia',
            new_name='profesion',
        ),
    ]
