# Generated by Django 3.1.7 on 2024-01-27 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdm_prospectosClientes', '0012_auto_20240126_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospectosclientes',
            name='courier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]