from django.db import models
from academia.models import Programa, Dependencia
from calidad.models import CriterioDeCalidad
from personas.models import Administrativo, Estudiante

# Create your models here.


class Planeacion(models.Model):
    periodos = [
        (1, 'Mensual'),
        (2, 'Bimestral'),
        (3, 'Trimestral'),
        (4, 'Cuatrimestral'),
        (6, 'Semestral'),
        (12, 'Anual'),
    ]
    periodicidad = models.PositiveSmallIntegerField(choices=periodos)
    fechaInicio = models.DateField('Fecha de Inicio')
    fechaFin = models.DateField('Fecha de Finalización')
    estados = [
        ('Planeado', 'Planeado'),
        ('Ejecutado', 'Ejecutado'),
        ('En Ejecución', 'En Ejecución'),
        ('Ejecutado Parcialmente', 'Ejecutado Parcialmente'),
        ('Cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=25, choices=estados)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Planeación'
        verbose_name_plural = 'Planeaciones'
        ordering = ["-fechaInicio"]

    def __str__(self):
        return 'Planeación: ' + str(self.fechaInicio) + ' - ' + str(self.fechaFin)


class Actividad(models.Model):
    nombre = models.CharField(max_length=160)
    objetivo = models.TextField()
    descripcion = models.TextField('Descripción')
    duracion = models.PositiveIntegerField(verbose_name='Duración', help_text='Duración en días')
    lugar = models.CharField(max_length=100)
    fechaIniProgramada = models.DateTimeField('Fecha de Inicio Programada')
    fechaFinProgramada = models.DateTimeField('Fecha de Finalización Programada')
    fechaIniEjecutada = models.DateTimeField('Fecha de Inicio Ejecutada', null=True, blank=True)
    fechaFinEjecutada = models.DateTimeField('Fecha de Finalización Ejecutada', null=True, blank=True)
    presupuestoProgramado = models.PositiveIntegerField('Presupuesto Programado')
    presupuestoEjecutado = models.PositiveIntegerField('Presupuesto Ejecutado', null=True, blank=True)
    modalidades = [
        ('Presencial', 'Presencial'),
        ('Semipresencial', 'Semipresencial'),
        ('Virtual', 'Virtual'),
    ]
    modalidad = models.CharField(max_length=20, choices=modalidades)
    estados = [
        ('Planeada', 'Planeada'),
        ('Ejecutada', 'Ejecutada'),
        ('En Ejecución', 'En Ejecución'),
        ('Ejecutada Parcialmente', 'Ejecutada Parcialmente'),
        ('Cancelada', 'Cancelada'),
    ]
    cupo = models.PositiveIntegerField(default=0)
    asistencia = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=25, choices=estados)
    observaciones = models.TextField(blank=True, help_text='Novedades presentadas que afectaron la ejecución de la '
                                                           'actividad')
    responsable = models.ForeignKey(Administrativo, on_delete=models.CASCADE)
    planeacion = models.ForeignKey(Planeacion, on_delete=models.CASCADE, verbose_name='Planeación', blank=True, null=True)
    programas = models.ManyToManyField(Programa)
    dependencias = models.ManyToManyField(Dependencia)
    criterios = models.ManyToManyField(CriterioDeCalidad, verbose_name='Criterios de Calidad')

    class Meta:
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.nombre


class Evidencia(models.Model):
    tipos = [
        ('Lista de Asistencia', 'Lista de Asistencia'),
        ('Acta de Reunión', 'Acta de Reunión'),
        ('Otras Actas', 'Otras Actas'),
        ('Oficio Administrativo', 'Oficio Administrativo'),
        ('Proyecto de Aula', 'Proyecto de Aula'),
        ('Proyecto de Investigación', 'Proyecto de Investigación'),
        ('Otro', 'Otro'),
    ]
    tipo = models.CharField(max_length=30, choices=tipos)
    fechaEv = models.DateTimeField(verbose_name='Fecha')
    fechaReg = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    descripcion = models.TextField('Descripción')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    soporte = models.FileField(upload_to='evidencias/'+str(actividad)+'/')
    estudiantes = models.ManyToManyField(Estudiante)
    docentes = models.ManyToManyField(Administrativo)

    def __str__(self):
        return self.tipo + ' - ' + self.actividad.nombre
