# Generated by Django 3.1.7 on 2021-11-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0003_prospectosclientes_identificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='nombreCompleto',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]