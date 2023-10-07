from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehiculos
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def vehiculos(request):
    return render(request,'indexVehiculos.html')
@login_required
def listVehiculos(request):
    vehiculo = Vehiculos.objects.all()
    datos = [{'id': item.id_vehiculo,'tipo':item.tipo_vehiculo,'modelo':item.modelo,'marca':item.marca, 'placa':item.placas,"activo":item.activo } for item in vehiculo]
    return JsonResponse(datos,safe=False)
@login_required
def insertarVehiculo(request):
    if request.method == 'POST':
        try:
            tipo = str(request.POST.get('tipov')).upper()
            modelo = str(request.POST.get('modelo')).upper()
            marca = str(request.POST.get('marca')).upper()
            placa = str(request.POST.get('placa')).upper()
            
            if not tipo or not modelo or not marca or not placa:
                respuesta = {"mensaje":"Todos los campos de deben de llenar","flag":False}
                return JsonResponse(respuesta)
            vehiculo = Vehiculos(tipo_vehiculo = tipo,modelo = modelo,marca=marca,placas=placa,activo= 1)
            vehiculo.save()
            respuesta = {"mensaje":"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required
def actualizarVehiculo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            tipo = str(request.POST.get('tipov')).upper()
            modelo = str(request.POST.get('modelo')).upper()
            marca = str(request.POST.get('marca')).upper()
            placa = str(request.POST.get('placa')).upper()
            
            if not tipo or not modelo or not marca or not placa:
                respuesta = {"mensaje":"Todos los campos de deben de llenar","flag":False}
                return JsonResponse(respuesta)
            vehiculo = Vehiculos.objects.get(id_vehiculo=id)
            vehiculo.tipo_vehiculo = tipo
            vehiculo.modelo = modelo
            vehiculo.marca = marca
            vehiculo.placas = placa
            vehiculo.save()
            respuesta = {"mensaje":"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required
def activoInactivo(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id')
            if not id:
                respuesta = {"mensaje":"Todos los campos de deben de llenar","flag":False}
                return JsonResponse(respuesta)
            vehiculo = Vehiculos.objects.get(id_vehiculo=id)
            if vehiculo.activo == 0:
             vehiculo.activo = 1
            else:
             vehiculo.activo = 0
            vehiculo.save()
            respuesta = {"mensaje":"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
