# Generated by Django 3.1.7 on 2024-07-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsb_pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superbarato',
            name='productoExtra',
            field=models.JSONField(null=True),
        ),
    ]
