from django.db import models
from academia.models import Programa
from personas.models import Administrativo

# Create your models here.


class Acreditacion(models.Model):
    estados = [
        ('En trámite', 'En trámite'),
        ('Vigente', 'Vigente'),
        ('Expirada', 'Expirada'),
        ('Revocada', 'Revocada'),
        ('Ampliada', 'Ampliada'),
        ('Renovada', 'Renovada'),
    ]
    tiposAcreditacion = [
        ('RC', 'Registro Calificado'),
        ('AC', 'Acreditación de Alta Calidad'),
    ]
    tipoAcreditacion = models.CharField(verbose_name='Tipo de Acreditación',
                                        max_length=2, choices=tiposAcreditacion)
    numResolucion = models.CharField(verbose_name='Rsolución N°', max_length=100)
    fechaObtencion = models.DateField('Fecha de Obtención')
    fechaVencimiento = models.DateField('Fecha de Vencimiento')
    estado = models.CharField(max_length=20, choices=estados)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Acreditación'
        verbose_name_plural = 'Acreditaciones'
        ordering = ["tipoAcreditacion", "-fechaObtencion"]

    def __str__(self):
        return self.tipoAcreditacion+'-'+self.numResolucion


class CriterioDeCalidad(models.Model):
    tiposCriterio = [
        ('RC', 'Registro Calificado'),
        ('AC', 'Acreditación de Alta Calidad'),
    ]
    tipoCriterio = models.CharField(verbose_name='Tipo de Acreditación',
                                        max_length=2, choices=tiposCriterio)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField('Descripción')

    class Meta:
        verbose_name_plural = 'Criterios De Calidad'
        ordering = ["tipoCriterio", "nombre"]

    def __str__(self):
        return self.nombre


class CriterioCalidadPrograma(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    criterio = models.ForeignKey(CriterioDeCalidad, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Administrativo, on_delete=models.CASCADE)
    estados = [
        ('Cumplido', 'Cumplido'),
        ('Pendiente', 'Pendiente'),
        ('Planeado', 'Planeado'),
        ('Cumplimiento Parcial', 'Cumplimiento Parcial'),
    ]
    estado = models.CharField(max_length=20, choices=estados)
