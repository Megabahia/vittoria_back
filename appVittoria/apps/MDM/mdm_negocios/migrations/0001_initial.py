# Generated by Django 3.1.7 on 2021-05-17 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Negocios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoNegocio', models.CharField(max_length=150, null=True)),
                ('ruc', models.CharField(max_length=150, null=True)),
                ('razonSocial', models.CharField(max_length=150, null=True)),
                ('nombreComercial', models.CharField(max_length=150, null=True)),
                ('nacionalidad', models.CharField(max_length=150, null=True)),
                ('fechaCreacionNegocio', models.DateField(max_length=150, null=True)),
                ('edadNegocio', models.CharField(max_length=150, null=True)),
                ('paisOrigen', models.CharField(max_length=150, null=True)),
                ('paisResidencia', models.CharField(max_length=150, null=True)),
                ('provinciaResidencia', models.CharField(max_length=150, null=True)),
                ('ciudadResidencia', models.CharField(max_length=150, null=True)),
                ('numeroEmpleados', models.CharField(max_length=150, null=True)),
                ('segmentoActividadEconomica', models.CharField(max_length=150, null=True)),
                ('provincia', models.CharField(max_length=150, null=True)),
                ('actividadEcomica', models.CharField(max_length=150, null=True)),
                ('llevarContabilidad', models.SmallIntegerField(default=1)),
                ('ingresosPromedioMensual', models.CharField(max_length=150, null=True)),
                ('gastosPromedioMensual', models.CharField(max_length=150, null=True)),
                ('numeroEstablecimientos', models.CharField(max_length=20, null=True)),
                ('telefonoOficina', models.CharField(max_length=150, null=True)),
                ('celularOficina', models.CharField(max_length=150, null=True)),
                ('celularPersonal', models.CharField(max_length=150, null=True)),
                ('whatsappPersonal', models.CharField(max_length=150, null=True)),
                ('whatsappSecundario', models.CharField(max_length=150, null=True)),
                ('correoPersonal', models.CharField(max_length=150, null=True)),
                ('correoOficina', models.CharField(max_length=150, null=True)),
                ('googlePlus', models.CharField(max_length=150, null=True)),
                ('twitter', models.CharField(max_length=150, null=True)),
                ('facebook', models.CharField(max_length=150, null=True)),
                ('instagram', models.CharField(max_length=150, null=True)),
                ('foto', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalNegocios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoContacto', models.CharField(max_length=10, null=True)),
                ('cedula', models.CharField(max_length=10, null=True)),
                ('nombres', models.CharField(max_length=150, null=True)),
                ('apellidos', models.CharField(max_length=150, null=True)),
                ('telefonoFijo', models.CharField(max_length=15, null=True)),
                ('extension', models.CharField(max_length=15, null=True)),
                ('celularEmpresa', models.CharField(max_length=15, null=True)),
                ('whatsappEmpresa', models.CharField(max_length=15, null=True)),
                ('celularPersonal', models.CharField(max_length=15, null=True)),
                ('whatsappPersonal', models.CharField(max_length=15, null=True)),
                ('correoEmpresa', models.CharField(max_length=150, null=True)),
                ('correoPersonal', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('idNegocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_negocios.negocios')),
            ],
        ),
        migrations.CreateModel(
            name='DireccionesEstablecimientosNegocios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoDireccion', models.CharField(max_length=150, null=True)),
                ('pais', models.CharField(max_length=150, null=True)),
                ('provincia', models.CharField(max_length=150, null=True)),
                ('ciudad', models.CharField(max_length=150, null=True)),
                ('callePrincipal', models.CharField(max_length=150, null=True)),
                ('numero', models.CharField(max_length=20, null=True)),
                ('calleSecundaria', models.CharField(max_length=150, null=True)),
                ('edificio', models.CharField(max_length=150, null=True)),
                ('piso', models.CharField(max_length=150, null=True)),
                ('oficina', models.CharField(max_length=150, null=True)),
                ('referencia', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('idNegocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mdm_negocios.negocios')),
            ],
        ),
    ]
