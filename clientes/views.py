from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from .models import Clientes
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
@login_required
def index(request):
    return render(request,'indexClientes.html')

def getClient(request):
    cliente = Clientes.objects.all()
    datos = [{'cod_cliente':item.cod_cliente,'nit':item.nit,'nombres': item.nombres,'apellidos': item.apellidos, 'fechaRegistro': item.fechaRegistro.strftime('%d-%m-%Y'), 'correo': item.correo, 'telefono':item.telefono } for item in cliente]
    return JsonResponse(datos,safe=False)

@login_required
def insertClient(request):
    if request.method == 'POST':
        try:
            _nit = request.POST.get('nit').upper()
            _nombres = request.POST.get('nombres').upper()
            _apellidos = request.POST.get('apellidos').upper()
            _correo = request.POST.get('correo').lower()
            _telefono = request.POST.get('telefono')
            _direccion = request.POST.get('direccion').upper()
           
            if not _nit or not _nombres or not _apellidos or not _correo or not _telefono:
                respuesta = {"mensaje":"Verifica los campos no pueden ser nulos","flag":False}
                return JsonResponse(respuesta,status=400,)
            
            cliente = Clientes(nit=_nit,nombres=_nombres,apellidos=_apellidos,correo=_correo,telefono=_telefono,direccion=_direccion)
            cliente.save()
            respuesta = {"mensaje":"Guardado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required
def updateClient(request):
     if request.method == 'POST':
        try:
            _codCliente = request.POST.get('codCliente')
            _nit = request.POST.get('nit').upper()
            _nombres = request.POST.get('nombres').upper()
            _apellidos = request.POST.get('apellidos').upper()
            _correo = request.POST.get('correo').lower()
            _telefono = request.POST.get('telefono')
            _direccion = request.POST.get('direccion').upper()
           
            if not _nit or not _nombres or not _apellidos or not _correo or not _telefono or not _codCliente:
                respuesta = {"mensaje":"Verifica los campos no pueden ser nulos","flag":False}
                return JsonResponse(respuesta,status=400,)
            
            cliente = Clientes.objects.get(pk=_codCliente)
            cliente.nit = _nit
            cliente.nombres = _nombres
            cliente.apellidos = _apellidos
            cliente.correo = _correo
            cliente.telefono = _telefono
            cliente.direccion = _direccion
            cliente.save()
            respuesta = {"mensaje":"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required       
def deleteClient(request):
     if request.method == 'POST':
        try:
            _codCliente = request.POST.get('codCliente')
            _nit = request.POST.get('nit')
            _nombres = request.POST.get('nombres')
            _apellidos = request.POST.get('apellidos')
           
            if not _nit or not _nombres or not _apellidos or not _codCliente :
                respuesta = {"mensaje":"Verifica los campos no pueden ser nulos","flag":False}
                return JsonResponse(respuesta,status=400,)
            
            cliente = Clientes.objects.get(pk=_codCliente)
            cliente.delete()

            respuesta = {"mensaje":"Eliminado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)