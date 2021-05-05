# Generated by Django 3.1.7 on 2021-04-21 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=150, null=True)),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=250, null=True)),
                ('config', models.TextField(default='{}')),
                ('permisoAdmin', models.CharField(default=0, max_length=50)),
                ('permisoMDM', models.CharField(default=0, max_length=50)),
                ('permisoMDP', models.CharField(default=0, max_length=50)),
                ('permisoMDO', models.CharField(default=0, max_length=50)),
                ('permisoGDO', models.CharField(default=0, max_length=50)),
                ('permisoGDE', models.CharField(default=0, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
