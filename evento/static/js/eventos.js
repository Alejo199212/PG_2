const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const nit = document.getElementById("nit");
const nitc = document.getElementById("nitc");
const selectVehiculos = document.getElementById("selectVehiculos");
const nombreEvento = document.getElementById("nombreEvento");
const precio = document.getElementById("precio");
const direccion = document.getElementById("direccion");
const fechaEntrega = document.getElementById("fechaEntrega");
const fechaInicio = document.getElementById("fechaInicio");
const fechaFin = document.getElementById("fechaFin");
const descripcion = document.getElementById("descripcion");
const abono = document.getElementById("abono");
const orden = document.getElementById("orden");
const cantidadSeleccionada = document.getElementById("cantidadSeleccionada");



const reservado = $("#tablaReservados").DataTable({
    searching: true,
    paging: false,
    ordering: false,
    lengthChange: false,
    info: false,
    select: true,
});

const seleccionar = $("#seleccionarArticulos").DataTable({
    searching: true,
    paging: false,
    ordering: false,
    lengthChange: false,
    info: false,
    select: true,
});



function validarCliente() {
    const formData = new FormData();
    formData.append("nitCod", nit.value);

    fetch("validarNit/", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                nitc.value = data.cod;
                listVehiculosActivos();
                $("#generarEvento").carousel("next");
            } else {
                desactivateLoading();
                alertify.confirm(
                    "Cliente no encontrado",
                    "Desea registrarlo?",
                    function () {
                        window.location.href = "/cliente/";
                    },
                    function () {
                        alertify.error("Cancel");
                    }
                );
            }
        })
        .catch((error) => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}

function retroceder() {
    $("#generarEvento").carousel("prev");
}

async function listVehiculosActivos() {
    selectVehiculos.innerHTML = ``;
    try {
        activateLoading();
        let response = await fetch("listVehiculosActivos/", { method: "GET" });
        if (response.ok) {
            const responseJson = await response.json();
            selectVehiculos.innerHTML =
                "<option selected>Seleccione Vehiculo</option>";
            for (let i = 0; i < responseJson.length; i++) {
                selectVehiculos.innerHTML += `<option value="${responseJson[i].id}">${responseJson[i].tipo}-${responseJson[i].modelo}-${responseJson[i].marca}-${responseJson[i].placa}</option>`;
            }
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

function enviarEvento() {
    let formData = new FormData();
    formData.append("nit", nitc.value);
    formData.append("nombreEvento", nombreEvento.value);
    formData.append("vehiculo", selectVehiculos.value);
    formData.append("precio", precio.value);
    formData.append("direccion", direccion.value);
    formData.append("fechaEntrega", fechaEntrega.value);
    formData.append("fechaInicio", fechaInicio.value);
    formData.append("fechaFin", fechaFin.value);
    formData.append("descripcion", descripcion.value);
    formData.append("abono", abono.value);

    fetch("insertEvento/", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                reservado.clear().draw(false);
                seleccionar.clear().draw(false);
                $("#agregarArticulo").modal("show");
                retroceder();
                alertify.success(data.mensaje);
                limpiar();
                listArticulos();
                orden.value = data.id;
                desactivateLoading();
            } else {
                alertify.error(data.mensaje);
                desactivateLoading();
            }
        })
        .catch((error) => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}

function limpiar() {
    nitc.value = "";
    nombreEvento.value = "";
    selectVehiculos.selectedIndex = 0;
    precio.value = "";
    direccion.value = "";
    abono.value = "";
    descripcion.value = "";
}

async function listArticulos() {
    seleccionar.clear();
    try {
        activateLoading();
        let response = await fetch(urlArticulos, { method: "GET" });
        if (response.ok) {
            const responseJson = await response.json();
            for (let i = 0; i < responseJson.length; i++) {
                seleccionar.row
                    .add([
                        responseJson[i].cod_product,
                        responseJson[i].nombre_producto,
                        responseJson[i].cantidad,
                    ])
                    .draw(false);
            }
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

function enviarArticulo(flag) {
    let url = "";

    if (
        (flag == "R" && seleccionar.row({ selected: true }).data() == undefined) ||
        (flag == "D" && reservado.row({ selected: true }).data() == undefined)
    ) {
        alertify.error("Seleccionar un articulo");
    } else {
        let formData = new FormData();

        formData.append("cantidadSeleccionada", cantidadSeleccionada.value);
        formData.append("orden", orden.value);

        if (flag == "R") {
            formData.append(
                "cod_prod",
                seleccionar.row({ selected: true }).data()[0]
            );
            url = reservarArticulo;
        } else if (flag == "D") {
            formData.append("cod_prod", reservado.row({ selected: true }).data()[0]);
            url = quitarArticulo;
        }

        fetch(url, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": token.value },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.flag == true) {
                    listArticulos();
                    alertify.success(data.mensaje);
                    listarArticulosReservados(orden.value);
                    cantidadSeleccionada.value = "";
                    desactivateLoading();
                } else {
                    listarArticulosReservados(orden.value);
                    alertify.error(data.mensaje);
                    desactivateLoading();
                }
            })
            .catch((error) => {
                alertify.error(error);
                desactivateLoading();
            });

        desactivateLoading();
    }
}

function completarEvento() {
    const formData = new FormData();
    formData.append("orden", orden.value);

    fetch(completar, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                $("#agregarArticulo").modal("hide");
                reservado.clear().draw(false);
                seleccionar.clear().draw(false);
                orden.value = "";
                if (flagVentana === 'evento') {
                    
                } else if (flagVentana === 'proceso') {
                    $("#table").DataTable().destroy();
                    getEventos();
                }

                alertify.success(data.mensaje);
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

function abrirModalBtn(flagOrden) {
    orden.value = flagOrden;
    listArticulos();
    listarArticulosReservados(flagOrden)
    $("#agregarArticulo").modal("show");
}

function listarArticulosReservados(flagOrden) {
    const formData = new FormData();
    formData.append("orden", flagOrden);
    reservado.clear().draw();
    fetch(listReservados, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                for (let i = 0; i < data.info.length; i++) {
                    reservado.row
                        .add([
                            data.info[i].cod_producto,
                            data.info[i].nombre,
                            data.info[i].cantidad,
                        ])
                        .draw(false);
                }
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


async function getClientes() {

    try{
        activateLoading();
        let response = await fetch(clientes,{ method:'GET'});
        if(response.ok){
            const responseJson = await response.json();
            
            $('#tableClientes').DataTable({
                data: responseJson,
                columns:[
                    {data:'cod_cliente'},
                    {data:'nit'},
                    {data:'nombres'},
                    {data:'apellidos'},
                ],
                ordering: false,
                select: true,
            });
            desactivateLoading();
        }else{
            desactivateLoading();
        }
    }catch(error){
      alertify.error(error)
      desactivateLoading();
    }
    desactivateLoading();
}

document.addEventListener('DOMContentLoaded',()=>{
    if (flagVentana === 'evento') {
        getClientes();      
    } 
   
});


function cambiarSiguiente(){
    let info = $('#tableClientes').DataTable().row({ selected: true }).data();
    
    if(info != undefined ){
        nitc.value = info.cod_cliente;
        listVehiculosActivos();
        $("#generarEvento").carousel("next");
    }else{
        alertify.error("Debe de seleccionar un cliente")
    }
}

