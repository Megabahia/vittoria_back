# Generated by Django 3.1.7 on 2024-01-18 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0005_auto_20211123_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='callePrincipal',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='calleSecundaria',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='comentarios',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='numeroCasa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='prospectosclientes',
            name='referencia',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
