from django.shortcuts import render
from clientes.models import Clientes
from inventarioAPP.models import Inventario
from evento.models import Evento
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from django.db import connection
import json
# Create your views here.

def indexDashboard(request):
    fecha_actual = timezone.now()
    clientes = Clientes.objects.count()
    inventario = Inventario.objects.count()
    entregasMes = Evento.objects.filter(Q(estado = 'entregado') | Q(estado='facturado'),fecha_entregado__year=fecha_actual.year,fecha_entregado__month=fecha_actual.month)
    cantidadEntrega = entregasMes.count()

    anuladosMes = Evento.objects.filter(estado = 'anulado',fecha_anulada__year=fecha_actual.year,fecha_anulada__month=fecha_actual.month)
    cantidadAnulados = anuladosMes.count()
    
    consultaSQL = "select "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '1' then 1 else 0 END) as ENE, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '2' then 1 else 0 END) as FEB, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '3' then 1 else 0 END) as MAR, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '4' then 1 else 0 END) as ABR , "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '5' then 1 else 0 END) as MAY , "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '6' then 1 else 0 END) as Jun, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '7' then 1 else 0 END) as Jul, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '8' then 1 else 0 END) as AGO, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '9' then 1 else 0 END) as SEP, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '10' then 1 else 0 END) as OCT, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '11' then 1 else 0 END) as NOV, "\
    "sum(case when coalesce(month(fecha_entregado),month(fecha_completada),month(fecha_entrega)) = '12' then 1 else 0 END) as DIC "\
    "from evento_evento "\
    "where estado != 'anulado' and estado != 'proceso' and year(coalesce(fecha_entregado,fecha_completada,fecha_entrega)) = %s"
    with connection.cursor() as cursor:
        cursor.execute(consultaSQL,[fecha_actual.year])
        resultado = cursor.fetchall()
    connection.close()

    try:
        datos = [int(resultado[0][0]),int(resultado[0][1]),int(resultado[0][2]),int(resultado[0][3]),int(resultado[0][4]),int(resultado[0][5]),int(resultado[0][6]),int(resultado[0][7]),int(resultado[0][8]),int(resultado[0][9]),int(resultado[0][10]),int(resultado[0][11])]
    except Exception:
        datos = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    dataJson = json.dumps(datos) 
    return render(request,'index.html',{
        'clientes':clientes,
        'inventario':inventario,
        'cantidadEntrega':cantidadEntrega,
        'cantidadAnulados':cantidadAnulados,
        "graficaLineal": dataJson
    })