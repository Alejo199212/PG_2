from django.db import models
from categoria.models import Categorias
from django.contrib.auth.models import User

# Create your models here.

class Inventario(models.Model):
    cod_product = models.CharField(max_length=250)
    nombre_producto = models.CharField(max_length=250,blank=False)
    descripcion_producto = models.CharField(max_length=300,blank=True)
    cantidad = models.IntegerField()
    activo = models.IntegerField()
    alerta = models.IntegerField()
    id_categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE)

class documentoCompra(models.Model):
    id_factura = models.AutoField(primary_key=True)
    num_factura = models.CharField(max_length=250)
    serie_factura = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10,decimal_places=2)
    cantidad = models.IntegerField()
    fecha_registro = models.DateField(auto_now_add=True)
    cod_product = models.ForeignKey(Inventario,on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE)

class articulosdeBaja(models.Model):
    id = models.AutoField(primary_key=True)
    num_factura = models.CharField(max_length=250,blank=True)
    serie_factura = models.CharField(max_length=250,blank=True)
    motivo = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    fecha_registro = models.DateField(auto_now_add=True)
    cod_product = models.ForeignKey(Inventario,on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE)

