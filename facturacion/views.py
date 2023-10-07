from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from evento.models import Evento, elemntos_reservados
from inventarioAPP.models import Inventario, articulosdeBaja
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
import os
from sistema import settings
from jinja2 import Template
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET
from django.contrib.auth.models import User
from .models import facturacion, detalleFacturacion
from django.http import HttpResponse
from .utils import renderPDF
import json
from django.contrib.auth.decorators import login_required
from configparser import ConfigParser
# Create your views here.


@login_required
def facturarEvento(request):
    return render(request, 'facturarEvento.html')


@login_required
def eventosFacturados(request):
    return render(request, 'eventosFacturados.html')


@login_required
def listadoEntregados(request):

    sqlConsulta = "select clientes_clientes.cod_cliente as cod, clientes_clientes.nit as nit,concat(clientes_clientes.nombres, ' ' ,clientes_clientes.apellidos) as nombre , evento_evento.id_evento,evento_evento.nombre_evento  from evento_evento "\
                  "inner join clientes_clientes on evento_evento.cod_cliente_id = clientes_clientes.cod_cliente "\
        "inner join vehiculos_vehiculos on evento_evento.id_vehiculo_id = vehiculos_vehiculos.id_vehiculo "\
        "where estado = 'entregado'"

    with connection.cursor() as cursor:
        cursor.execute(sqlConsulta)
        resultado = cursor.fetchall()
    connection.close()

    datos = [{'cod': items[0], 'nit':items[1],
              'nombre':items[2], 'eventoID':items[3],  'nombreEvento':items[4]} for items in resultado]

    return JsonResponse(datos, safe=False)


@login_required
def listadoFacturados(request):

    fact = facturacion.objects.all()
    datos = [{'id_evento': items.id_evento.id_evento, 'nit': items.nit_factura, 'nombreFact': items.nombre,
              'numI': items.num_interno, 'num': items.num_factura, 'serie': items.serie_factura} for items in fact]

    return JsonResponse(datos, safe=False)


@login_required
def validarReservados(request):
    if request.method == 'POST':
        try:
            listaArticulosDevueltos = request.POST.get('articulos')
            orden = request.POST.get('orden')
            articulosSerializados = json.loads(listaArticulosDevueltos)
            articulosAsignados = elemntos_reservados.objects.filter(
                id_evento=orden)
            event = Evento.objects.get(id_evento=orden)
            listaArticulosAsignados = list(articulosAsignados)
            listArticulosAPagar = []
            flag = True
            mensaje = ''

            for item in articulosSerializados:
                i = 0
                for asignados in listaArticulosAsignados:
                    if item['codigo'] == asignados.cod_producto.cod_product:
                        if int(item['cantidad']) > int(asignados.cantidad):
                            flag = False
                            mensaje = item['nombre'] + \
                                " Cantidad ingresada es mayor a la asignada"
                            break
                        elif int(item['cantidad']) <= 0:
                            flag = False
                            mensaje = item['nombre'] + \
                                " No se puede devolver un producto con cantidad 0 o menor a 0"
                            break
                        elif int(item['cantidad']) < int(asignados.cantidad):
                            resta = int(asignados.cantidad) - \
                                int(item['cantidad'])
                            articulo = {
                                'codigo': item['codigo'], 'nombre': item['nombre'], 'cantidad': item['cantidad']}
                            listArticulosAPagar.append(articulo)
                            item['cantidad'] = resta
                            listaArticulosAsignados.pop(i)
                            flag = True
                            mensaje = ""
                        elif int(item['cantidad']) == int(asignados.cantidad):
                            listaArticulosAsignados.pop(i)
                            flag = True
                            mensaje = ""

                    i += 1
                if flag == False:
                    break

            if listaArticulosAsignados:
                datos = [{'codigo': str(item.cod_producto.cod_product), 'nombre': str(
                    item.cod_producto.nombre_producto), 'cantidad': str(item.cantidad)} for item in listaArticulosAsignados]
                listArticulosAPagar.extend(datos)

            infoEvento = {
                "nit": event.cod_cliente.nit,
                "nombre": event.cod_cliente.nombres + ' ' + event.cod_cliente.apellidos,
                "direccion": event.cod_cliente.direccion,
                "cantidad": 1,
                "idEvento": event.id_evento,
                "descripcion": event.nombre_evento + ' ' + event.descripcion,
                "precio": event.precio,
                "abono": event.abono
            }

            respuesta = {
                "mensaje": mensaje, "flag": flag, "cobroArticulos": listArticulosAPagar, "articulosDevueltos": articulosSerializados, "infoEvento": infoEvento}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)


@login_required
def facturar(request):
    if request.method == 'POST':
        try:
            detalleFact = request.POST.get('detalle')
            orden = request.POST.get('orden')
            nit = request.POST.get('nit')
            nombre = request.POST.get('nombre')
            direccion = request.POST.get('direccion')
            articulosBaja = request.POST.get('articulosBaja')
            user = request.POST.get('user')
            detalleFactJson = json.loads(detalleFact)
            paths = os.path.join(settings.MEDIA_ROOT, 'archivo.j2')
            horaUTC = datetime.now(pytz.UTC)
            restaHoras = timedelta(hours=6)
            resultadoResta = horaUTC - restaHoras
            formatoHora = "%Y%m%d%H"
            resultadoFechaGT = resultadoResta.strftime(formatoHora)
            formatoFechaFact = "%d/%m/%Y"
            resultadoFechaFactGt = resultadoResta.strftime(formatoFechaFact)
            evento = Evento.objects.get(id_evento=orden)
            devAsignados = elemntos_reservados.objects.filter(id_evento=orden)
            infoFactDetalle, totalFactura, flagPrecio = detalleDeProductos(
                detalleFactJson)
            infoFact = infoFactura(nit, nombre, direccion, infoFactDetalle,
                                   totalFactura, resultadoFechaFactGt, resultadoFechaGT+orden)
            
            if not nit or not nombre or not direccion:
                respuesta = {
                    "mensaje": 'Verificar datos de facturacion Nit,Nombre,Direccion', "flag": False}
                return JsonResponse(respuesta)

            if flagPrecio == True:
                respuesta = {
                    "mensaje": 'Verificar precios no pueden ser 0', "flag": False}
                return JsonResponse(respuesta)

            userId = User.objects.get(id=user)
            articuloSerializado = []
            if articulosBaja:
                articuloSerializado = json.loads(articulosBaja)

            with open(paths, 'r') as temp:
                templateFact = temp.read()
            resultadoTemplate = Template(templateFact)

            respuesta = enviarFactura(resultadoTemplate.render(infoFact))

            if respuesta:
                raiz = ET.fromstring(str(respuesta))
                nodo = raiz.find('.//Serie')

                if nodo is not None:
                    referencia = raiz.find('.//Referencia')
                    numero = raiz.find('.//Preimpreso')
                    nombreFact = raiz.find('.//Nombre')
                    direccionFact = raiz.find('.//Direccion')
                    numeroAutorizacionFact = raiz.find('.//NumeroAutorizacion')

                    infoFact.update({"serie": nodo.text})
                    infoFact.update({"numero": numero.text})
                    infoFact.update({"nombreFact": nombreFact.text})
                    infoFact.update({"direccionFact": direccionFact.text})
                    infoFact.update(
                        {"numeroAutorizacionFact": numeroAutorizacionFact.text})
                    evento.estado = 'facturado'
                    evento.save()

                    fact = facturacion(num_interno=referencia.text, num_factura=numero.text, serie_factura=nodo.text, nit_factura=nit, nombre=nombreFact.text,
                                       direccion=direccionFact.text, totalFact=totalFactura, fechaFacturacion=resultadoResta.strftime('%Y-%m-%d'), id_evento=evento, num_autorizacion=numeroAutorizacionFact.text)
                    fact.save()

                    for item in detalleFactJson:
                        detFact = detalleFacturacion(num_interno=fact, descripcion=item['descripcion'], cantidad=float(
                            item['cant']), precioU=float(item['precioUnidad']), tipo=item['tipo'])
                        detFact.save()

                    for itemDev in devAsignados:
                        inventario = Inventario.objects.get(
                            id=itemDev.cod_producto.id)
                        inventario.cantidad += itemDev.cantidad
                        inventario.save()
                        itemDev.estado = 'devuelto'
                        itemDev.save()

                    if articuloSerializado:
                        for item in articuloSerializado:
                            inventario = Inventario.objects.get(
                                cod_product=int(item['codigo']))
                            inventario.cantidad -= int(item['cantidad'])
                            inventario.save()
                            docBaja = articulosdeBaja(num_factura=referencia.text, cantidad=int(
                                item['cantidad']), cod_product=inventario, id_usuario=userId)
                            docBaja.save()

                    pdf = renderPDF('pdf/factura.html', infoFact)
                    respuesta = {
                        "mensaje": "Factura Generada con Exito", "flag": True, "pdf": pdf}
                    return JsonResponse(respuesta)
                else:
                    respuesta = {"mensaje": respuesta, "flag": False}
                    return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)


def enviarFactura(xml):
    path = os.path.join(settings.MEDIA_ROOT, 'config.ini')
    config = ConfigParser()
    config.read(path)
    session = Session()
    session.auth = HTTPBasicAuth(config['Basic']['user'], config['Basic']['password'])
    clinte = Client("https://pdte.guatefacturas.com:443/webservices63/feltestSB/Guatefac?wsdl",
                    transport=Transport(session=session))
    respuesta = clinte.service.generaDocumento(
        config['Request']['user'], config['Request']['password'],  config['Request']['nit'], '1', '1', '1', config['Request']['Response'], xml)
    return respuesta


def detalleDeProductos(json):
    infoFactDetalle = []
    flagPrecio = False
    i = 0
    totalFactura = 0.0
    for item in json:
        i += 1
        cantidad = int(item['cant'])
        precioU = float(item['precioUnidad'])
        totalSinIva = float(item['total']) / 1.12
        impBruto = float(item['precioUnidad']) * float(item['cant'])
        impNeto = float(item['total']) - float(totalSinIva)
        total = float(item['total'])
        totalFactura = totalFactura + total
        infoFactDetalle.append({
            'producto': i,
            'descripcion': item['descripcion'],
            'tipo': item['tipo'],
            'medida': 1,
            'cantidad': "{:.2f}".format(cantidad),
            'precioU': "{:.2f}".format(precioU),
            'ImpBruto':  "{:.2f}".format(impBruto),
            'ImpNeto':  "{:.2f}".format(totalSinIva),
            'iva': "{:.2f}".format(impNeto),
                   'total': "{:.2f}".format(total)
        })
        if precioU <= 0:
            flagPrecio = True
    return infoFactDetalle, totalFactura, flagPrecio


def infoFactura(nit, nombre, direccion, infoFactDetalle, totalFactura, resultadoFechaFactGt, referencia):
    infoFact = {
        'nit': nit,
        'nombre': nombre,
        'direccion': direccion,
        'producto': infoFactDetalle,
        'impBruto': "{:.2f}".format(totalFactura),
        'totalFactura': "{:.2f}".format(totalFactura),
        "totalImpNeto": "{:.2f}".format(totalFactura/1.12),
        "iva": "{:.2f}".format((totalFactura/1.12) * 0.12),
        'fecha': resultadoFechaFactGt,
        "referencia": referencia
    }
    return infoFact


@login_required
def verFact(request):
    if request.method == 'POST':
        try:
            numInterno = request.POST.get('numInterno')

            fact = facturacion.objects.get(num_interno=numInterno)
            detalleFact = detalleFacturacion.objects.filter(
                num_interno=fact.id)
            formatoFechaFact = "%d/%m/%Y"
            detalle = [{'cantidad': float(item.cantidad), 'descripcion': item.descripcion, 'precioU': float(
                item.precioU), 'total': (float(item.cantidad)*float(item.precioU))} for item in detalleFact]

            informacionFact = {
                'nit': fact.nit_factura,
                'nombreFact': fact.nombre,
                'direccionFact': fact.direccion,
                'producto': detalle,
                'totalFactura': fact.totalFact,
                'fecha': fact.fechaFacturacion.strftime(formatoFechaFact),
                "referencia": fact.num_interno,
                'serie': fact.serie_factura,
                'numero': fact.num_factura,
                'numeroAutorizacionFact': fact.num_autorizacion,

            }

            pdf = renderPDF('pdf/factura.html', informacionFact)
            respuesta = {"mensaje": "Recibido", "flag": True, "pdf": pdf}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)
