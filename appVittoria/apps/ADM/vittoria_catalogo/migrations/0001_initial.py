# Generated by Django 3.1.7 on 2021-05-11 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idPadre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vittoria_catalogo.catalogo')),
                ('nombre', models.CharField(max_length=150, null=True)),
                ('tipo', models.CharField(max_length=150)),
                ('tipoVariable', models.CharField(max_length=150)),
                ('valor', models.CharField(max_length=150)),
                ('descripcion', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                
            ],
        ),
    ]
