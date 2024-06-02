from django.db import models

# Create your models here.

class Propuesta(models.Model):
    nombre = models.CharField(max_length=100)
    estudiante = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    profesor = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)