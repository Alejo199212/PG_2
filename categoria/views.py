from django.shortcuts import render
from django.http import JsonResponse
from .models import Categorias
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def IndexCategoria(request):
    return render(request,'indexCategoria.html')
@login_required
def ListCategoria(request):
    categoria = Categorias.objects.all()
    datos = [ {'id_categoria':item.id_categoria,'nombre_categoria': item.nombre_categoria, 'descripcion': item.descripcion_categoria, 'fecha_registro': item.fechaRegistro.strftime('%d-%m-%Y')} for item in categoria]
    return JsonResponse(datos,safe=False)
@login_required
def insertCategoria(request):
    if request.method == 'POST':
       
        try:
            _nombre = request.POST.get('nombre')
            _descripcion = request.POST.get('descripcion')
            if not _nombre or not _descripcion:
                respuesta = {"mensaje":str("Verifica los campos no pueden ser nulos"),"flag":False}
                return JsonResponse(respuesta,status=400)
            categoria = Categorias(nombre_categoria = _nombre,  descripcion_categoria = _descripcion)
            categoria.save()
            respuesta = {"mensaje":"Guardado con exito","flag":True}
            return JsonResponse(respuesta)

        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
        
@login_required
def updateCategoria(request):
    if request.method == 'POST':
        try:
            _id = request.POST.get('id')
            _nombre = request.POST.get('nombre')
            _descripcion = request.POST.get('descripcion')
            
            if not _id or not _nombre or not _descripcion:
                respuesta = {"mensaje":str("Verifica los campos no pueden ser nulos"),"flag":False}
                return JsonResponse(respuesta,status=400)
            categoria = Categorias.objects.get(pk=_id)
            categoria.nombre_categoria = _nombre
            categoria.descripcion_categoria = _descripcion
            categoria.save()
            respuesta = {"mensaje": "Se actualizo con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
        
@login_required
def eliminarCategoria(request):
    if request.method == 'POST':
           try:
                _id = request.POST.get('id')
                if not _id:
                    respuesta = {"mensaje":str("Verifica los campos no pueden ser nulos"),"flag":False}
                    return JsonResponse(respuesta,status=400)
                categoria = Categorias.objects.get(pk=_id)
                categoria.delete()
                respuesta = {"mensaje":"Eliminado con exito","flag":True}
                return JsonResponse(respuesta)
           except Exception as ex:
               respuesta = {"mensaje":str(ex),"flag":False}
               return JsonResponse(respuesta,status=400)

