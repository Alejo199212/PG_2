"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventarioAPP.views import bases
from inventarioAPP.views import inventario
from inventarioAPP.views import listInventario,insertarInventario,actualizarInventario,actualizarCantidad,bajaArticulo,desactivar
from clientes.views import index
from clientes.views import getClient
from clientes.views import insertClient
from clientes.views import updateClient
from clientes.views import deleteClient
from login.views import sesion
from login.views import cerrar_sesion
from categoria import views
from evento.views import decoraciones,validarNit,listVehiculosActivos,insertEvento,listArticulos, reservarArticulo,quitarArticulo,completarOrden,enproceso,listadoEventoProceso,anularEvento,listaArticulosReservados,completados \
,listadoEventoCompletado,marcarEntregado,verDetalles
from vehiculos.views import vehiculos,listVehiculos,insertarVehiculo,actualizarVehiculo,activoInactivo
from dashboard.views import indexDashboard
from facturacion.views import facturarEvento,listadoEntregados,validarReservados,facturar,eventosFacturados,listadoFacturados,verFact
from reportes.views import returnReport,articulosDeBajaReporte,compraArticulos,articulosInventario
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',sesion,name="login"),
    path('cliente/',index, name='cliente'),
    path('cliente/listClient/',getClient,name='listClient'),
    path('cliente/insertClient/',insertClient,name='insertClient'),
    path('cliente/updateClient/',updateClient,name="updateClient"),
    path('cliente/deleteClient/',deleteClient,name="deleteClient"),
    path('bases/', bases,name="bases"),
    path('cerrar_sesion/',cerrar_sesion,name='logout'),
    path('categoria/',views.IndexCategoria,name="categoria"),
    path('categoria/listCategorias/',views.ListCategoria,name='listCategorias'),
    path('inventario/listCategorias/',views.ListCategoria,name='inventarioListCategorias'),
    path('categoria/insertCategoria/',views.insertCategoria,name='insertCategoria'),
    path('categoria/updateCategoria/',views.updateCategoria,name= 'updateCategoria'),
    path('categoria/eliminarCategoria/',views.eliminarCategoria,name='eliminarCategoria'),
    path('inventario/',inventario,name="inventario"),
    path('inventario/listInventario/',listInventario,name='listInventario'),
    path('inventario/insertarInventario/',insertarInventario,name='insertarInventario'),
    path('inventario/actualizarInventario/',actualizarInventario,name='actualizarInventario'),
    path('inventario/actualizarCantidad/',actualizarCantidad,name='actualizarCantidad'),
    path('inventario/bajaArticulo/',bajaArticulo,name='bajaArticulo'),
    path('inventario/desactivar/',desactivar,name='desactivar'),
    path('evento/',decoraciones,name="decoraciones"),
    path('vehiculos/',vehiculos,name="vehiculos"),
    path('vehiculos/listVehiculos/',listVehiculos,name='listVehiculos'),
    path('vehiculos/insertarVehiculo/',insertarVehiculo,name='insertarVehiculo'),
    path('vehiculos/actualizarVehiculo/',actualizarVehiculo,name='actualizarVehiculo'),
    path('vehiculos/activoInactivo/',activoInactivo,name='activoInactivo'),
    path('evento/validarNit/',validarNit,name='validarNit'),
    path('evento/listVehiculosActivos/',listVehiculosActivos,name='listVehiculosActivos'),
    path('evento/insertEvento/',insertEvento,name='insertEvento'),
    path('evento/listArticulos/',listArticulos,name='listArticulos'),
    path('evento/reservarArticulo/',reservarArticulo,name='reservarArticulo'),
    path('evento/quitarArticulo/',quitarArticulo,name='quitarArticulo'),
    path('evento/completarOrden/',completarOrden,name='completarOrden'),
    path('evento/enproceso/',enproceso,name='enproceso'),
    path('evento/enproceso/listadoEventoProceso/',listadoEventoProceso,name='listadoEventoProceso'),
    path('evento/enproceso/anularEvento/',anularEvento,name='anularEvento'),
    path('evento/listaArticulosReservados/',listaArticulosReservados,name='listaArticulosReservados'),
    path('evento/completados/',completados,name='completados'),
    path('evento/completados/listadoEventoCompletado/',listadoEventoCompletado,name='listadoEventoCompletado'),
    path('evento/completados/marcarEntregado/',marcarEntregado,name='marcarEntregado'),
    path('evento/completados/verDetalles/',verDetalles,name='verDetalles'),
    path('dashboard/',indexDashboard,name='indexDashboard'),
    path('facturarEvento/',facturarEvento,name="facturarEvento"),
    path('facturarEvento/listadoEntregados/',listadoEntregados,name="listadoEntregados"),
    path('facturarEvento/validarReservados/',validarReservados,name="validarReservados"),
    path('facturarEvento/facturar/',facturar,name="facturar"),
    path('eventosFacturados/',eventosFacturados,name="eventosFacturados"),
    path('eventosFacturados/listadoFacturados/',listadoFacturados,name="listadoFacturados"),
    path('eventosFacturados/verFact/',verFact,name="verFact"),
    path('returnReport/',returnReport,name="returnReport"),
    path('returnReport/articulosDeBajaReporte/',articulosDeBajaReporte,name="articulosDeBajaReporte"),
    path('returnReport/compraArticulos/',compraArticulos,name="compraArticulos"),
    path('returnReport/articulosInventario/',articulosInventario,name="articulosInventario"),
]
