const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const indiceCantidad = document.getElementById('indiceCantidad');
const numerCantidad = document.getElementById('numerCantidad');
const ordenNo = document.getElementById('ordenNo');
const nit = document.getElementById('nit');
const nombre = document.getElementById('nombre');
const direccion = document.getElementById('direccion');
const sladerFactura = document.getElementById('sladerFactura');
const indicePrecio = document.getElementById('indicePrecio');
const numeroPrecio = document.getElementById('numeroPrecio');
const numeroPrecioCantidad = document.getElementById('numeroPrecioCantidad');
const articulosBaja = document.getElementById('articulosBaja');
const descripcionProducto = document.getElementById('descripcionProducto');
const user = document.getElementById('user');
const tipo = document.getElementById('tipo')


let asignados = $("#asignados").DataTable({
    searching: false,
    paging: false,
    ordering: false,
    info: false,
    columnDefs: [
        {
            orderable: false,
            className: 'select-checkbox',
            targets: 0
        },
    ],
    select: {
        style: 'multi',
        selector: 'td:first-child'
    },
    order: [[1, 'asc']]
});

let detalleFactura = $("#detalleFactura").DataTable({
    searching: false,
    paging: false,
    ordering: false,
    info: false,
    order: [[1, 'asc']]
});

async function getEventos() {
    try {
        activateLoading();
        let response = await fetch("listadoEntregados/", { method: "GET" });

        if (response.ok) {
            const responseJson = await response.json();

            $("#table").DataTable({
                data: responseJson,
                columns: [
                    { data: "cod" },
                    { data: "nit" },
                    { data: "nombre" },
                    { data: "eventoID" },
                    { data: "nombreEvento" },
                    {
                        defaultContent:
                            '<button class="btn mx-1 btn-outline-dark btn-fact" data-toggle="tooltip" data-placement="top" title="Facturar Evento"><i class="fas fa-file-invoice"></i></button>'

                    },
                ],

                ordering: false,
            });
            desactivateLoading();
        } else {
            desactivateLoading();
        }
    } catch (error) {
        alertify.error(error);
        desactivateLoading();
    }
    desactivateLoading();
}



document.addEventListener("DOMContentLoaded", () => {

    getEventos();
  
});

$(document).on("click", ".btn-fact", function () {
    const parentBtn = $(this).closest("tr");
    const tabla = $("#table").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    listarArticulosReservados(dataRow.eventoID)
});

$(document).on("click", ".btn-cant", function () {
    indiceCantidad.value = '';
    numerCantidad.value = '';
    const parentBtn = $(this).closest("tr");
    const tabla = $("#asignados").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    indiceCantidad.value = parentBtn.index();
    numerCantidad.value = dataRow[3];
    $('#editarCantidad').modal('show');
});

$(document).on("click", ".btn-precio", function () {
    indiceCantidad.value = '';
    numerCantidad.value = '';
    const parentBtn = $(this).closest("tr");
    const tabla = $("#detalleFactura").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    indicePrecio.value = parentBtn.index();
    numeroPrecioCantidad.value = dataRow[0];
    $('#modalPrecio').modal('show');
});

function cambiar() {
    asignados.cell(indiceCantidad.value, 3).data(numerCantidad.value).draw();
    $('#editarCantidad').modal('hide');
}

function cambiarPrecio() {
    if(numeroPrecio.value != null && tipo.selectedIndex!= 0){
        detalleFactura.cell(indicePrecio.value, 6).data(numeroPrecio.value).draw();
        detalleFactura.cell(indicePrecio.value, 7).data(numeroPrecioCantidad.value * numeroPrecio.value).draw();
        descripcion =  detalleFactura.cell(indicePrecio.value, 2).data();
        detalleFactura.cell(indicePrecio.value, 2).data(descripcion.toUpperCase() + ' ' + descripcionProducto.value.toUpperCase()).draw();
        detalleFactura.cell(indicePrecio.value, 3).data(tipo.value).draw();
        $('#modalPrecio').modal('hide');
        indicePrecio.value = '';
        numeroPrecio.value = '';
        numeroPrecioCantidad.value = '';
        descripcionProducto.value = '';
        tipo.selectedIndex = 0
    }else{
        alertify.error("Verifique que los campos Precio y Tipo no esten vacios")
    }
    

}

function listarArticulosReservados(flagOrden) {
    const formData = new FormData();
    formData.append("orden", flagOrden);
    asignados.clear().draw();
    fetch(listReservados, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                for (let i = 0; i < data.info.length; i++) {
                    asignados.row
                        .add([
                            '',
                            data.info[i].cod_producto,
                            data.info[i].nombre,
                            data.info[i].cantidad,
                            '<button class="btn mx-1 btn-outline-dark btn-cant" data-toggle="tooltip" data-placement="top" title="Editar Cantidad"><i class="fas fa-file-invoice"></i></button>'
                        ])
                        .draw(false);
                    ordenNo.value = flagOrden;
                }
                limpiar();
                $('#modalEvento').modal('show')
            } else {
                desactivateLoading();
                alertify.error(data.mensaje);
            }
        })
        .catch((error) => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}


function listaArticulosDevueltos() {
    const formData = new FormData();
    let informacionDevueltos = asignados.rows({ selected: true }).data();
    let datos = []

    for (let i = 0; i < informacionDevueltos.length; i++) {

        datos.push({
            codigo: informacionDevueltos[i][1],
            nombre: informacionDevueltos[i][2],
            cantidad: informacionDevueltos[i][3]
        })
    }

    articulosJson = JSON.stringify(datos)
    formData.append('articulos', articulosJson);
    formData.append('orden', ordenNo.value);

    fetch('validarReservados/', {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            limpiar();
            if (data.flag) {

                nit.value = data.infoEvento.nit;
                nombre.value = data.infoEvento.nombre;
                direccion.value = data.infoEvento.direccion;
                articulosBaja.value = data.cobroArticulos.length > 0? JSON.stringify(data.cobroArticulos):'';
                detalleFactura.row
                    .add([
                        data.infoEvento.cantidad,
                        data.infoEvento.idEvento,
                        data.infoEvento.descripcion,
                        'S',
                        data.infoEvento.abono,
                        data.infoEvento.precio - data.infoEvento.abono,
                        data.infoEvento.precio,
                        data.infoEvento.precio * data.infoEvento.cantidad,
                        '<button class="btn mx-1 btn-outline-dark " data-toggle="tooltip" data-placement="top" title="Editar Cantidad" disabled><i class="fas fa-file-invoice"></i></button>'

                    ])
                    .draw(false);
                for (let i = 0; i < data.cobroArticulos.length; i++) {
                    
                    detalleFactura.row
                        .add([
                            data.cobroArticulos[i].cantidad,
                            data.cobroArticulos[i].codigo,
                            data.cobroArticulos[i].nombre,
                            '',
                            0.00,
                            0.00,
                            0.00,
                            0.00,
                            '<button class="btn mx-1 btn-outline-dark btn-precio" data-toggle="tooltip" data-placement="top" title="Editar Precio"><i class="fas fa-file-invoice"></i></button>'
                        ])
                        .draw(false);

                }

                $('#sladerFactura').carousel('next')

            } else {
                desactivateLoading();
                alertify.error(data.mensaje);
            }
        })
        .catch((error) => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}

function limpiar() {
    nit.value = '';
    nombre.value = '';
    direccion.value = '';
    articulosBaja.value = '';
    detalleFactura.clear().draw();
}

modalEvento.addEventListener('hidden.bs.modal', function () {
    limpiar();
    $('#sladerFactura').carousel(0)
});


function facturar() {
    activateLoading();
    let detalleFact = []
    const formData = new FormData();
    formData.append("orden", ordenNo.value);
    formData.append('nit',nit.value);
    formData.append('nombre',nombre.value);
    formData.append('direccion',direccion.value);
    formData.append('articulosBaja',articulosBaja.value);
    formData.append('user',user.value);
    let obtenerDetalles = detalleFactura.rows().data();

    for(let i = 0; i< obtenerDetalles.length;i++){
          detalleFact.push({
                cant : obtenerDetalles[i][0],
                cod : obtenerDetalles[i][1],
                descripcion : obtenerDetalles[i][2],
                tipo : obtenerDetalles[i][3],
                abono : obtenerDetalles[i][4],
                pendiente : obtenerDetalles[i][5],
                precioUnidad: obtenerDetalles[i][6],
                total: obtenerDetalles[i][7],
          });
    }

    detalleFactJson = JSON.stringify(detalleFact);
    formData.append("detalle",detalleFactJson)

    fetch('facturar/', {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                $('#modalEvento').modal('hide')
               
                alertify.success(data.mensaje)
                let pdfContenido = atob(data.pdf);
                let blob = new Blob([pdfContenido], { type: 'application/pdf' });
                let url = URL.createObjectURL(blob)
                window.open(url,'_blank');
                $("#table").DataTable().destroy();
                getEventos();
            } else {
                desactivateLoading();
                alertify.error(data.mensaje);
            }
        })
        .catch((error) => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}