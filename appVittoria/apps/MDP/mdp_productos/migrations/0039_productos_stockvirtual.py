# Generated by Django 3.1.7 on 2024-06-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0038_auto_20240618_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='stockVirtual',
            field=models.JSONField(null=True),
        ),
    ]
