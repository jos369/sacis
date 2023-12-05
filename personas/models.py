from django.db import models
from academia.models import Programa, Dependencia
from django.urls import reverse

# Create your models here.


class Persona(models.Model):
    tiposDocID = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('PA', 'Pasaporte'),
        ('CD', 'Carnet Diplomático'),
        ('PP', 'Permiso por Protección Temporal'),
    ]
    tipoDocIdentidad = models.CharField(verbose_name='Tipo de Documento de Identidad',
                                        max_length=2, choices=tiposDocID, default='CC')
    numDocIdentidad = models.CharField(verbose_name='Número de Documento de Identidad', max_length=14)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    email = models.EmailField()

    class Meta:
        abstract = True


class Estudiante(Persona):
    semestres = [
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
        (6, 'VI'),
        (7, 'VII'),
        (8, 'VIII'),
        (9, 'IX'),
        (10, 'X'),
        #        (11, 'XI'),
        #        (12, 'XII'),
    ]
    codigo = models.CharField(verbose_name='Código', max_length=16, unique=True)
    promedio = models.DecimalField(max_digits=3, decimal_places=2)
    semestre = models.PositiveSmallIntegerField(choices=semestres)
    activo = models.BooleanField(default=True)
    graduado = models.BooleanField(default=False)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)

    class Meta:
        ordering = ["codigo"]

    def get_absolute_url(self):
        return reverse('Estudiante-detail', args=[str(self.id)])

    def full_name(self):
        return self.__str__()

    def __str__(self):
        return self.apellidos+', '+self.nombres


class Administrativo(Persona):
    email = models.EmailField(unique=True)
    roles = [
        ('Profesor', 'Profesor'),
        ('Secretario/a', 'Secretario/a'),
        ('Director/a de Programa', 'Director/a de Programa'),
        ('Director/a de Dependencia', 'Director/a de Dependencia'),
    ]
    codigo = models.CharField(verbose_name='Código', max_length=16, unique=True)
    rol = models.CharField(max_length=40, choices=roles)
    activo = models.BooleanField(default=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, null=True, blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)

    class Meta:
        ordering = ["apellidos"]

    def __str__(self):
        return self.apellidos + ', ' + self.nombres
