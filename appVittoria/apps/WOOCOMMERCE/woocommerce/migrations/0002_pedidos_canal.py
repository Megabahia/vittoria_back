# Generated by Django 3.1.7 on 2024-03-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woocommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='canal',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
