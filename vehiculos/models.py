from django.db import models

# Create your models here.

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    tipo_vehiculo = models.CharField(max_length=300)
    modelo = models.CharField(max_length=300)
    marca = models.CharField(max_length=300)
    placas = models.CharField(max_length=300)
    activo = models.IntegerField()