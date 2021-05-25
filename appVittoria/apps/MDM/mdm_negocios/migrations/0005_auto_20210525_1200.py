# Generated by Django 3.1.7 on 2021-05-25 17:00

import apps.MDM.mdm_negocios.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_negocios', '0004_auto_20210525_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='negocios',
            name='foto',
        ),
        migrations.AddField(
            model_name='negocios',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to=apps.MDM.mdm_negocios.models.upload_path),
        ),
    ]
