from django.shortcuts import render
from .models import Inventario,Categorias,documentoCompra,articulosdeBaja
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def bases(request):
    return render(request,"index.html",{})

@login_required
def inventario(request):
    return render(request,"inventario.html")

@login_required
def listInventario(request):
    producto = Inventario.objects.select_related('id_categoria')
    datos = [{"codigo": item.cod_product,"nombre":item.nombre_producto,"descripcion": item.descripcion_producto,"cantidad": item.cantidad, "alerta": item.alerta, "categoria": item.id_categoria.nombre_categoria,"activo":item.activo} for item in producto]
    return JsonResponse(datos,safe=False)

@login_required
def insertarInventario(request):

   if request.method == 'POST':
        try:
            cod = request.POST.get('cod')
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            alerta = request.POST.get('alerta')
            numFact = request.POST.get('numFact')
            serie = request.POST.get('serie')
            precio = request.POST.get('precio')
            _cantidad = request.POST.get('cantidad')
            categoria = request.POST.get('categoria')
            user = request.POST.get('user')
         
            if validacionProducto(cod,nombre,descripcion,alerta,categoria) == False or validacionFactura(numFact,serie,precio,_cantidad,user) == False:
                respuesta = {'mensaje':'Verifica los campos no pueden ser nulos',"flag":False}
                return JsonResponse(respuesta,status=400)
            
            with transaction.atomic():
                instanciaCategoria = Categorias.objects.get(id_categoria = categoria)
                inventario = Inventario(cod_product = cod, alerta = alerta,nombre_producto = nombre,descripcion_producto = descripcion,cantidad = _cantidad, id_categoria = instanciaCategoria,activo=1)
                inventario.save()
                inv = Inventario.objects.get(cod_product = cod)
                usr = User.objects.get(id=user)
                fact = documentoCompra(num_factura = numFact,serie_factura = serie,precio = precio,cantidad =_cantidad,cod_product = inv,id_usuario = usr)
                fact.save()
                respuesta = {'mensaje':"Agregado con Exito","flag":True}
                return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
        
def validacionProducto(cod,nombre,descripcion,aleta,categoria):
    if not cod or not nombre or not descripcion or not aleta or not categoria:
        return False
    return True

def validacionFactura(numFact,serie,precio,cantidad,user):
      if not numFact or not serie or not precio or not cantidad or not user:
        return False
      return True
 
@login_required
def actualizarInventario(request):
    if request.method == 'POST':
        try:
            cod = request.POST.get('cod')
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            alerta = request.POST.get('alerta')
            categoria = request.POST.get('categoria')

            if validacionProducto(cod,nombre,descripcion,alerta,categoria) == False:
                respuesta = {'mensaje':'Verifica los campos no pueden ser nulos',"flag":False}
                return JsonResponse(respuesta,status=400)
            categorias = Categorias.objects.get(pk=categoria)
            inventario = Inventario.objects.get(cod_product=cod)
            inventario.nombre_producto = nombre
            inventario.descripcion_producto = descripcion
            inventario.alerta = alerta
            inventario.id_categoria = categorias
            inventario.save()
            respuesta = {'mensaje':"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required       
def actualizarCantidad(request):
    if request.method == 'POST':
        try:
            cod = request.POST.get('cod')
            numFact = request.POST.get('numFact')
            serie = request.POST.get('serie')
            precio = request.POST.get('precio')
            _cantidad = request.POST.get('cantidad')
            user = request.POST.get('user')
            if not cod or validacionFactura(numFact,serie,precio,_cantidad,user) == False:
                respuesta = {'mensaje':'Verifica los campos no pueden ser nulos',"flag":False}
                return JsonResponse(respuesta,status=400)
            
            with transaction.atomic():
                #Factura de compras
                users = User.objects.get(pk=user)
                objInventario = Inventario.objects.get(cod_product=cod)
                facturaCompra = documentoCompra(num_factura = numFact,serie_factura = serie,precio = precio,cantidad =_cantidad,cod_product = objInventario,id_usuario = users)
                facturaCompra.save()
                #Actualizacion informacion inventario
                
                objInventario.cantidad = int(objInventario.cantidad) + int(_cantidad)
                objInventario.save()
                respuesta = {'mensaje':"Actualizado con exito","flag":True}
                return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
@login_required      
def bajaArticulo(request):
    if request.method == 'POST':
        try:
            cod = request.POST.get('cod')
            _cantidad = request.POST.get('cantidad')
            _motivo = request.POST.get('motivo')
            user = request.POST.get('user')
            if not cod or not _cantidad or not user or not _motivo:
                respuesta = {'mensaje':'Verifica los campos no pueden ser nulos',"flag":False}
                return JsonResponse(respuesta,status=400)
            objInventario = Inventario.objects.get(cod_product=cod)

            if (int(objInventario.cantidad) - int(_cantidad)) < 0:
                respuesta = {'mensaje':'Verifica la cantidad no puede ser mayor a la existencia',"flag":False}
                return JsonResponse(respuesta,status=400)

            with transaction.atomic():
                #Factura de compras
                users = User.objects.get(pk=user)
                articuloBaja = articulosdeBaja(num_factura = 'N/A',serie_factura = 'N/A',motivo = _motivo,cantidad =_cantidad,cod_product = objInventario,id_usuario = users)
                articuloBaja.save()
                #Actualizacion informacion inventario
                
                objInventario.cantidad = int(objInventario.cantidad) - int(_cantidad)
                objInventario.save()
                respuesta = {'mensaje':"Actualizado con exito","flag":True}
                return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)
                
@login_required           
def desactivar(request):
    if request.method == 'POST':
        try:
            cod = request.POST.get('cod')
            if not cod:
                respuesta = {'mensaje':'Verifica los campos no pueden ser nulos',"flag":False}
                return JsonResponse(respuesta,status=400)
            inventario = Inventario.objects.get(cod_product=cod)
            if inventario.activo == 0:
                inventario.activo = 1
            else:
                inventario.activo = 0
            inventario.save()
            respuesta = {'mensaje':"Actualizado con exito","flag":True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje":str(ex),"flag":False}
            return JsonResponse(respuesta,status=400)