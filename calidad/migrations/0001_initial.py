# Generated by Django 4.2.7 on 2023-12-04 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personas', '0001_initial'),
        ('academia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CriterioDeCalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoCriterio', models.CharField(choices=[('RC', 'Registro Calificado'), ('AC', 'Acreditación de Alta Calidad')], max_length=2, verbose_name='Tipo de Acreditación')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(verbose_name='Descripción')),
            ],
            options={
                'verbose_name_plural': 'Criterios De Calidad',
                'ordering': ['tipoCriterio', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='CriterioCalidadPrograma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Cumplido', 'Cumplido'), ('Pendiente', 'Pendiente'), ('Planeado', 'Planeado'), ('Cumplimiento Parcial', 'Cumplimiento Parcial')], max_length=20)),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calidad.criteriodecalidad')),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.programa')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personas.administrativo')),
            ],
        ),
        migrations.CreateModel(
            name='Acreditacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoAcreditacion', models.CharField(choices=[('RC', 'Registro Calificado'), ('AC', 'Acreditación de Alta Calidad')], max_length=2, verbose_name='Tipo de Acreditación')),
                ('numResolucion', models.CharField(max_length=100, verbose_name='Rsolución N°')),
                ('fechaObtencion', models.DateField(verbose_name='Fecha de Obtención')),
                ('fechaVencimiento', models.DateField(verbose_name='Fecha de Vencimiento')),
                ('estado', models.CharField(choices=[('En trámite', 'En trámite'), ('Vigente', 'Vigente'), ('Expirada', 'Expirada'), ('Revocada', 'Revocada'), ('Ampliada', 'Ampliada'), ('Renovada', 'Renovada')], max_length=20)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academia.programa')),
            ],
            options={
                'verbose_name': 'Acreditación',
                'verbose_name_plural': 'Acreditaciones',
                'ordering': ['tipoAcreditacion', '-fechaObtencion'],
            },
        ),
    ]
