# Generated by Django 3.1.7 on 2024-10-22 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdrp_productos', '0002_auto_20241022_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='fecha_confirmacion',
            field=models.DateTimeField(null=True),
        ),
    ]