from django.db import models

# Create your models here.
class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(blank=False,max_length=250)
    descripcion_categoria = models.CharField(max_length=300)
    fechaRegistro = models.DateTimeField(auto_now_add=True)


