from django.shortcuts import render
from facturacion.utils import renderPDF
from django.http import JsonResponse
from inventarioAPP.models import articulosdeBaja,documentoCompra,Inventario
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

@login_required
def returnReport(request):
    return render(request,'reporte.html')

@login_required
def articulosDeBajaReporte(request):
    if request.method == 'POST':
        try:
            fechaInicio = request.POST.get('inicio')
            fechaFin = request.POST.get('fin')
            formato = '%d-%m-%Y'
            if not fechaInicio or not fechaFin:
                respuesta = {"mensaje": "Colocar fecha desde y hasta", "flag": False}
                return JsonResponse(respuesta)
            if  fechaInicio > fechaFin:
                respuesta = {"mensaje": "Fecha hasta no puede ser menor a fecha desde", "flag": False}
                return JsonResponse(respuesta)
            
            articulos = articulosdeBaja.objects.filter(fecha_registro__range=(fechaInicio,fechaFin))

            if not articulos:
                respuesta = {"mensaje": "No se encontro Información", "flag": False}
                return JsonResponse(respuesta)

            informacion = [{'codigo':item.cod_product.cod_product,'nombre':item.cod_product.nombre_producto,'numFact':item.num_factura,'cantidad':item.cantidad,'fecha':item.fecha_registro.strftime(formato),'usuario':item.id_usuario.username} for item in articulos]
            articulos = {
                'articulos': informacion
            }
               
            pdf = renderPDF('pdf/articulos.html', articulos)
            respuesta = {"mensaje": "Generado", "flag": True,'pdf':pdf}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)
@login_required
def compraArticulos(request):
    if request.method == 'POST':
        try:
            fechaInicio = request.POST.get('inicio')
            fechaFin = request.POST.get('fin')
            formato = '%d-%m-%Y'
            if not fechaInicio or not fechaFin:
                respuesta = {"mensaje": "Colocar fecha desde y hasta", "flag": False}
                return JsonResponse(respuesta)
            if  fechaInicio > fechaFin:
                respuesta = {"mensaje": "Fecha hasta no puede ser menor a fecha desde", "flag": False}
                return JsonResponse(respuesta)
            
            articulos = documentoCompra.objects.filter(fecha_registro__range=(fechaInicio,fechaFin))

            if not articulos:
                respuesta = {"mensaje": "No se encontro Información", "flag": False}
                return JsonResponse(respuesta)

            informacion = [{'numFact':item.num_factura,'serie':item.serie_factura,'codigo':item.cod_product.cod_product,'nombre':item.cod_product.nombre_producto,\
                            'precio':item.precio,'cantidad':item.cantidad, 'fecha':item.fecha_registro.strftime(formato),"usuario":item.id_usuario.username} for item in articulos]
            articulos = {
                'articulos': informacion
            }
               
            pdf = renderPDF('pdf/articulosCompra.html', articulos)
            respuesta = {"mensaje": "Generado", "flag": True,'pdf':pdf}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)
@login_required
def articulosInventario(request):
    if request.method == 'POST':
        try:
            inventario = Inventario.objects.all()
            if not inventario:
                respuesta = {"mensaje": "No se encontro Información", "flag": False}
                return JsonResponse(respuesta)

            inventarioList = [{'codigo':item.cod_product,'nombre':item.nombre_producto,'descripcion':item.descripcion_producto,'cantidad':item.cantidad} for item in inventario]
            articulos = {
                'inventario': inventarioList
            }
               
            pdf = renderPDF('pdf/listaInventario.html', articulos)
            respuesta = {"mensaje": "Generado", "flag": True,'pdf':pdf}
            return JsonResponse(respuesta)
        except Exception as ex:
            respuesta = {"mensaje": str(ex), "flag": False}
            return JsonResponse(respuesta)
