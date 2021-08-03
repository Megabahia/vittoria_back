# Generated by Django 3.1.7 on 2021-07-26 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdp_productos', '0009_auto_20210721_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='lote',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='Lotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(max_length=150, null=True)),
                ('fechaElaboracion', models.DateTimeField(null=True)),
                ('fechaCaducidad', models.DateTimeField(null=True)),
                ('precioCompra', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdp_productos.productos')),
            ],
        ),
    ]