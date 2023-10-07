from django.db import models

# Create your models here.

class Clientes(models.Model):
    cod_cliente = models.AutoField(primary_key=True)
    nit = models.CharField(max_length=20)
    nombres = models.CharField(max_length=300)
    apellidos = models.CharField(max_length=300)
    direccion = models.CharField(max_length=300)
    fechaRegistro = models.DateTimeField(auto_now_add=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=12)