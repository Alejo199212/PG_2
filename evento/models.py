from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from clientes.models import Clientes
from inventarioAPP.models import Inventario
from vehiculos.models import Vehiculos
# Create your models here.

class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    nombre_evento = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=300)
    direccion = models.CharField(max_length=300,blank=True)
    fecha_entrega = models.DateField(max_length=300)
    cod_cliente = models.ForeignKey(Clientes,on_delete=models.CASCADE,blank=True)
    estado = models.CharField(max_length=30,blank=True)
    abono = models.DecimalField(max_digits=10,decimal_places=2)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    id_vehiculo = models.ForeignKey(Vehiculos,on_delete=models.CASCADE,blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_entregado = models.DateField(null=True)
    fecha_completada = models.DateField(null=True)
    fecha_anulada = models.DateField(null=True)

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey(Evento,on_delete=models.CASCADE)
    nit_cliente = models.ForeignKey(Clientes,on_delete=models.CASCADE)
    fecha_registro = models.DateField()

class elemntos_reservados(models.Model):
    id_elemento = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey(Evento,on_delete=models.CASCADE)
    cod_producto = models.ForeignKey(Inventario,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=30)
