from django.db import models
from evento.models import Evento
# Create your models here.
class facturacion(models.Model):
    id = models.AutoField(primary_key=True)
    num_interno = models.CharField(max_length=100)
    num_factura = models.CharField(max_length=100)
    num_autorizacion = models.CharField(max_length=100)
    serie_factura = models.CharField(max_length=100)
    nit_factura = models.CharField(max_length=100)
    nombre =  models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    totalFact = models.DecimalField(max_digits=10,decimal_places=2)
    fechaFacturacion = models.DateField()
    id_evento = models.ForeignKey(Evento,on_delete=models.CASCADE)


class detalleFacturacion(models.Model):
    id = models.AutoField(primary_key=True)
    num_interno = models.ForeignKey(facturacion,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    cantidad = models.DecimalField(max_digits=10,decimal_places=2)
    precioU = models.DecimalField(max_digits=10,decimal_places=2)
    tipo =  models.CharField(max_length=2)
    