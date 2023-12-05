from django.db import models

# Create your models here.


class Universidad(models.Model):
    campusChoices = [
        ('cuc', 'Cúcuta'),
        ('buc', 'Bucaramanga'),
        ('val', 'Valledupar'),
        ('bog', 'Bogotá'),
    ]
    nit = models.CharField(max_length=14)
    nombre = models.CharField(max_length=100)
    campus = models.CharField(max_length=3, choices=campusChoices, default='cuc')
    direccion = models.CharField(verbose_name='Dirección', max_length=100)
    telefono = models.CharField(verbose_name='Teléfono', max_length=14)

    class Meta:
        verbose_name_plural = 'Universidades'
        ordering = ["nombre", "campus"]


class Programa(models.Model):
    nombre = models.CharField(max_length=100)
    semestres = [
        (1, '1 Semestre'),
        (2, '2 Semestres'),
        (3, '3 Semestres'),
        (4, '4 Semestres'),
        (5, '5 Semestres'),
        (6, '6 Semestres'),
        (7, '7 Semestres'),
        (8, '8 Semestres'),
        (9, '9 Semestres'),
        (10, '10 Semestres'),
        #   (11, '11 Semestres'),
        #   (12, '12 Semestres'),
    ]
    duracion = models.PositiveSmallIntegerField('Duración', choices=semestres, default=10)
    modalidades = [
        ("Presencial", "Presencial"),
        ("Virtual", "Virtual"),
    ]
    modalidad = models.CharField(max_length=20, choices=modalidades)
    descripcion = models.TextField('Descripción')
    url = models.URLField('URL')
    director = models.CharField(max_length=100)

    class Meta:
        ordering = ["duracion", "nombre"]

    def __str__(self):
        return f"{self.nombre} - {self.modalidad}"


class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField('Descripción')
    director = models.CharField(max_length=100)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
