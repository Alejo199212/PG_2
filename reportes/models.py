from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.

class permisos(models.Model):
    nombre = models.CharField(max_length=25)