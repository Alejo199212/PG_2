from django.shortcuts import render
from .models import Clientes
from vehiculos.models import Vehiculos
from inventarioAPP.models import Inventario
from .models import Evento, elemntos_reservados
from facturacion.utils import renderPDF
from django.db.models import Q
from django.db.models import Sum
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
import json
# Create your views here.

@login_required
def decoraciones(request):
    return render(request, 'decoraciones.html')

@login_required
def enproceso(request):
    return render(request, 'enproceso.html')

@login_required
def completados(request):
    return render(request, 'completadas.html')

@login_required
def validarNit(request):
    if request.method == 'POST':
        try:
            _nit = str(request.POST.get('nitCod')).upper()
            if not _nit:
                respuesta = {
                    "mensaje": "Todos los campos de deben de llenar", "flag": False}
                return JsonResponse(respuesta)
            cliente = Clientes.objects.get(nit=_nit)

            if not cliente:
                respuesta = {"mensaje": "No existe el cliente", "flag": False}
                return JsonResponse(respuesta)
            else:
                respuesta = {"mensaje": "Encontrado", "flag": True,"cod":cliente.cod_cliente}
                return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)

@login_required
def listVehiculosActivos(request):
    vehiculo = Vehiculos.objects.filter(activo=1)
    datos = [{'id': item.id_vehiculo, 'tipo': item.tipo_vehiculo, 'modelo': item.modelo,
              'marca': item.marca, 'placa': item.placas, "activo": item.activo} for item in vehiculo]
    return JsonResponse(datos, safe=False)

@login_required
def insertEvento(request):
    if request.method == 'POST':
        try:
            _nit = request.POST.get('nit')
            _nombreEvento = request.POST.get('nombreEvento')
            _vehiculo = request.POST.get("vehiculo")
            _precio = request.POST.get('precio')
            _direccion = request.POST.get('direccion')
            _fechaEntrega = request.POST.get('fechaEntrega')
            _fechaInicio = request.POST.get('fechaInicio')
            _fechaFin = request.POST.get('fechaFin')
            _descripcion = request.POST.get('descripcion')
            _abono = request.POST.get('abono')
            _estado = 'proceso'
            evt = Evento.objects.filter(Q(estado='completado') | Q(estado='proceso'),id_vehiculo=_vehiculo)
        
            if validar(_nit, _nombreEvento, _vehiculo, _precio, _direccion, _fechaEntrega, _fechaInicio, _fechaFin) == False:
                respuesta = {
                    "mensaje": "Verificar los campos no pueden ser nulos", "flag": False}
                return JsonResponse(respuesta)
            if _fechaEntrega > _fechaInicio:
                respuesta = {
                    "mensaje": "La fecha de entrega no puede ser mayor a la fecha de Inicio", "flag": False}
                return JsonResponse(respuesta)
            if _fechaEntrega > _fechaFin:
                respuesta = {
                    "mensaje": "La fecha de entrega no puede ser mayor a la fecha de fin", "flag": False}
                return JsonResponse(respuesta)
            if _fechaInicio > _fechaFin:
                respuesta = {
                    "mensaje": "La fecha de inicio no puede ser mayor a la fecha de fin", "flag": False}
                return JsonResponse(respuesta)
            if float(_abono) > float(_precio):
                respuesta = {
                    "mensaje": "El valor a abonar no puede ser mayor a el precio", "flag": False}
                return JsonResponse(respuesta)
            if evt.count() > 0:
                respuesta = {
                    "mensaje": "Este vehiculo ya se encuetra asignado para otro evento", "flag": False}
                return JsonResponse(respuesta)
            if not _abono:
                _abono = 0.00
    
            vehiculo = Vehiculos.objects.get(id_vehiculo=_vehiculo)
            cliente = Clientes.objects.get(cod_cliente=_nit)
            evento = Evento(cod_cliente=cliente, nombre_evento=_nombreEvento, id_vehiculo=vehiculo, precio=_precio, direccion=_direccion,
                            fecha_entrega=_fechaEntrega, fecha_inicio=_fechaInicio, fecha_fin=_fechaFin, descripcion=_descripcion, abono=_abono, estado=_estado)
            evento.save()
            respuesta = {"mensaje": "Generado con exito",
                         "flag": True, 'id': evento.id_evento}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)


def validar(nit, nombre, vehiculo, precio, direccion, fechaEntrega, fechaInicio, fechaFin):
    if not nit or not nombre or not vehiculo or not precio or not direccion or not fechaEntrega or not fechaInicio or not fechaFin:
        return False
    return True

@login_required
def listArticulos(request):
    inventario = Inventario.objects.filter(activo=1)
    datos = [{"cod_product": item.cod_product, 'nombre_producto': item.nombre_producto,
              'cantidad': item.cantidad} for item in inventario]
    return JsonResponse(datos, safe=False)

@login_required
def reservarArticulo(request):
    if request.method == 'POST':

        try:
            cod_producto = request.POST.get("cod_prod")
            cantidadSeleccionada = request.POST.get("cantidadSeleccionada")
            orden = request.POST.get("orden")

            if not cod_producto or not cantidadSeleccionada or not orden:
                respuesta = {
                    "mensaje": "Enviar codigo de producto, cantidad y numero de orden", "flag": False}
                return JsonResponse(respuesta)
            invent = Inventario.objects.get(cod_product=cod_producto)
            _estado = Evento.objects.get(id_evento=orden)

            if int(cantidadSeleccionada) > int(invent.cantidad):
                respuesta = {
                    "mensaje": "Cantidad es mayor a la cantidad existente", "flag": False}
                return JsonResponse(respuesta)
            elif _estado.estado != "proceso":
                respuesta = {
                    "mensaje": "Orde finalizada no se pueden agregar productos", "flag": False}
                return JsonResponse(respuesta)
            elif int(cantidadSeleccionada) == 0:
                respuesta = {
                    "mensaje": "Cantidad seleccionada no puede ser 0", "flag": False}
                return JsonResponse(respuesta)

            restaExistencia = int(invent.cantidad) - int(cantidadSeleccionada)
            existe = elemntos_reservados.objects.filter(
                cod_producto=invent.id, id_evento=orden).first()

            if not existe:
                articulo = elemntos_reservados(
                    cantidad=cantidadSeleccionada, estado="proceso", cod_producto=invent, id_evento=_estado)
                articulo.save()
            else:
                existe.cantidad = int(existe.cantidad) + \
                    int(cantidadSeleccionada)
                existe.save()

            invent.cantidad = restaExistencia
            invent.save()

            respuesta = {"mensaje": "Agregado con exito",
                         "flag": True}
            return JsonResponse(respuesta)

        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)

@login_required
def quitarArticulo(request):
    if request.method == 'POST':
        try:
            cod_producto = request.POST.get("cod_prod")
            cantidadSeleccionada = request.POST.get("cantidadSeleccionada")
            orden = request.POST.get("orden")
            invent = Inventario.objects.get(cod_product=cod_producto)
            _estado = Evento.objects.get(id_evento=orden)
            articulos = elemntos_reservados.objects.filter(
                cod_producto=invent.id, id_evento=orden).first()

            if not cod_producto or not cantidadSeleccionada or not orden:
                respuesta = {
                    "mensaje": "Enviar codigo de producto, cantidad y numero de orden", "flag": False}
                return JsonResponse(respuesta)
            if _estado.estado != "proceso":
                respuesta = {
                    "mensaje": "Orden completada no se pueden quitar elementos", "flag": False}
                return JsonResponse(respuesta)
            elif int(cantidadSeleccionada) == 0:
                respuesta = {
                    "mensaje": "Cantidad a devolver no puede ser 0", "flag": False}
                return JsonResponse(respuesta)

            if not articulos:
                respuesta = {
                    "mensaje": "No se encontro informacion con los datos proporcionados", "flag": False}
                return JsonResponse(respuesta)
            if int(cantidadSeleccionada) > int(articulos.cantidad):
                respuesta = {
                    "mensaje": "La cantidad indicada es mayor a la que tiene asignada", "flag": False}
                return JsonResponse(respuesta)

            resta = int(articulos.cantidad) - int(cantidadSeleccionada)

            if resta == 0:
                invent.cantidad = int(invent.cantidad) + \
                    int(cantidadSeleccionada)
                invent.save()
                articulos.delete()
            elif resta > 0:
                invent.cantidad = int(invent.cantidad) + \
                    int(cantidadSeleccionada)
                invent.save()
                articulos.cantidad = int(
                    articulos.cantidad) - int(cantidadSeleccionada)
                articulos.save()

            respuesta = {"mensaje": "Se removio con exito",
                         "flag": True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)


def listaReservados(orden):
    sqlConsulta = "select cod_product, nombre_producto,sum(evento_elemntos_reservados.cantidad) as cantidad from evento_elemntos_reservados " \
        "inner join inventarioapp_inventario on evento_elemntos_reservados.cod_producto_id = inventarioapp_inventario.id " \
        "where id_evento_id = %s " \
        "group by cod_product, nombre_producto "

    with connection.cursor() as cursor:
        cursor.execute(sqlConsulta, [orden])
        resultado = cursor.fetchall()

    datos = [{'cod_producto': items[0], 'nombre':items[1],
              "cantidad":items[2]} for items in resultado]
    connection.close()
    return datos

@login_required
def completarOrden(request):
    if request.method == 'POST':
        try:
            orden = request.POST.get("orden")
            date = datetime.datetime.now()

            if not orden:
                respuesta = {
                    "mensaje": "Enviar numero de evento", "flag": False}
                return JsonResponse(respuesta)
            articulos = elemntos_reservados.objects.filter(id_evento=orden)
            articulos.update(estado='asignado')
            evento = Evento.objects.get(id_evento=orden)
            evento.estado = 'completado'
            evento.fecha_completada = date.date()
            evento.save()
            respuesta = {"mensaje": "Orden completada", "flag": True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)

@login_required
def listadoEventoProceso(request):
    sqlConsulta = "select clientes_clientes.cod_cliente as cod_cliente, concat(clientes_clientes.nombres, ' ' ,clientes_clientes.apellidos) as nombre , evento_evento.id_evento, evento_evento.estado from evento_evento "\
                  "inner join clientes_clientes on evento_evento.cod_cliente_id = clientes_clientes.cod_cliente "\
                  "where estado = 'proceso'"

    with connection.cursor() as cursor:
        cursor.execute(sqlConsulta)
        resultado = cursor.fetchall()
    connection.close()

    datos = [{'cod_cliente': items[0], 'nombre':items[1],
              'id_evento':items[2], 'estado':items[3]} for items in resultado]

    return JsonResponse(datos, safe=False)

@login_required
def listadoEventoCompletado(request):
    sqlConsulta = "select clientes_clientes.cod_cliente as nit, concat(clientes_clientes.nombres, ' ' ,clientes_clientes.apellidos) as nombre , evento_evento.id_evento,evento_evento.nombre_evento ,vehiculos_vehiculos.placas as placa , evento_evento.direccion as direccion  from evento_evento " \
                  "inner join clientes_clientes on evento_evento.cod_cliente_id = clientes_clientes.cod_cliente "\
                  "inner join vehiculos_vehiculos on evento_evento.id_vehiculo_id = vehiculos_vehiculos.id_vehiculo "\
                  "where estado = 'completado'"

    with connection.cursor() as cursor:
        cursor.execute(sqlConsulta)
        resultado = cursor.fetchall()
    connection.close()

    datos = [{'nit': items[0], 'nombre':items[1],
              'id_evento':items[2], 'nombreEvento':items[3],  'placas':items[4], 'direccion':items[5]} for items in resultado]

    return JsonResponse(datos, safe=False)

@login_required
def anularEvento(request):
    if request.method == 'POST':
        try:
            orden = request.POST.get("orden")
            date = datetime.datetime.now()
            if not orden:
                respuesta = {
                    "mensaje": "Enviar numero de evento", "flag": False}
                return JsonResponse(respuesta)
            articulos = elemntos_reservados.objects.filter(id_evento=orden)
            evento = Evento.objects.get(id_evento=orden)
            if len(articulos) > 0:
                for item in articulos:
                    invent = Inventario.objects.get(id=item.cod_producto.id)
                    invent.cantidad = invent.cantidad + item.cantidad
                    invent.save()
                    articulos.delete()

            evento.estado = 'anulado'
            evento.fecha_anulada = date.date()
            evento.save()
            respuesta = {"mensaje": "Orden completada", "flag": True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)

@login_required
def marcarEntregado(request):
    if request.method == 'POST':
        try:
            orden = request.POST.get("orden")
            date = datetime.datetime.now()
            if not orden:
                respuesta = {
                    "mensaje": "Enviar numero de evento", "flag": False}
                return JsonResponse(respuesta)
            evento = Evento.objects.get(id_evento=orden)
            evento.estado = 'entregado'
            evento.fecha_entregado = date.date()
            evento.save()
            respuesta = {"mensaje": "Marcado como Entregado", "flag": True}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)

@login_required
def listaArticulosReservados(request):

    try:
        orden = request.POST.get("orden")
        if not orden:
            respuesta = {
                "mensaje": "Enviar numero de evento", "flag": False}
            return JsonResponse(respuesta)

        sqlConsulta = "select cod_product, nombre_producto,sum(evento_elemntos_reservados.cantidad) as cantidad from evento_elemntos_reservados " \
            "inner join inventarioapp_inventario on evento_elemntos_reservados.cod_producto_id = inventarioapp_inventario.id " \
            "where id_evento_id = %s " \
            "group by cod_product, nombre_producto "

        with connection.cursor() as cursor:
            cursor.execute(sqlConsulta, [orden])
            resultado = cursor.fetchall()
        datos = [{'cod_producto': items[0], 'nombre':items[1],
                 "cantidad":items[2]} for items in resultado]
        connection.close()
        respuesta = {"flag": True, "info": datos}
        return JsonResponse(respuesta)
    except Exception as ex:
        respuesta = {"mensaje": str(ex), "flag": False}
        return JsonResponse(respuesta)
    

def verDetalles(request):

    try:
        orden = request.POST.get("orden")
        if not orden:
            respuesta = {
                "mensaje": "Enviar numero de evento", "flag": False}
            return JsonResponse(respuesta)

        evento = Evento.objects.get(id_evento = orden)
        formatoFecha = '%d-%m-%Y'
        elementos = elemntos_reservados.objects.filter(id_evento=evento)
        articulos = [{'codigo':item.cod_producto.cod_product,'nombre':item.cod_producto.nombre_producto,'cantidad':item.cantidad} for item in elementos]

        dictEvento = {
            'cliente' : evento.cod_cliente.nombres + ' ' + evento.cod_cliente.apellidos,
            'codigo_cliente': evento.cod_cliente.cod_cliente,
            'nit': evento.cod_cliente.nit,
            'codigoEvento':evento.id_evento,
            'nombre_evento': evento.nombre_evento,
            'descripcion':evento.descripcion,
            'precio':evento.precio,
            'abonado':evento.abono,
            'entrega':evento.fecha_entrega.strftime(formatoFecha),
            'Termina':evento.fecha_fin.strftime(formatoFecha),
            'articulos': articulos
        }
        pdf = renderPDF('pdf/report.html',dictEvento)
        respuesta = {"flag": True, "mensaje": "Generado con Exito",'pdf':pdf}
        return JsonResponse(respuesta)
    except Exception as ex:
        respuesta = {"mensaje": str(ex), "flag": False}
        return JsonResponse(respuesta)

