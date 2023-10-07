const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const id = document.getElementById('id');
const marca = document.getElementById('marca');
const tipov = document.getElementById('tipov');
const modelo = document.getElementById('modelo');
const placa = document.getElementById('placa');
const tipo = document.getElementById('tipo');
const id_label = document.getElementById('id_label');
const labelmodelo = document.getElementById("labelmodelo");
const divLeyendaEliminar = document.getElementById('divLeyendaEliminar');
const headerMondal = document.getElementById('headerMondal');
const btnConfirmar = document.getElementById('btnConfirmar');
const btnTitulo = document.getElementById('btnTitulo');
const datosID = document.getElementById('datosID');
const inputs = document.getElementById('inputs');
const leyenda = document.getElementById('leyenda');

async function getVehiculos() {

    try {
        activateLoading();
        let response = await fetch('listVehiculos/', { method: 'GET' });
        if (response.ok) {
            const responseJson = await response.json();

            $('#table').DataTable({
                data: responseJson,
                columns: [
                    { data: 'id' },
                    { data: 'tipo' },
                    { data: 'modelo' },
                    { data: 'marca' },
                    { data: 'placa' },
                    {
                        data: 'activo',
                        render: function (data, type, row) {
                            if (data <= 0) {
                                return "<span class='text-danger p-1 font-weight-bold'><i class='fa-solid fa-truck'></i></span>"
                            } else {
                                return "<span class='text-success p-1 font-weight-bold'><i class='fa-solid fa-truck'></i></span>"
                            }
                        }
                    },
                    {
                        'defaultContent': '<button class="btn mx-1 btn-outline-primary btn-edit"><i class="fa-regular fa-pen-to-square"></i></button>' +
                            '<button class="btn mx-1 btn-outline-danger btn-delete"><i class="fa-solid fa-delete-left"></i></button>'
                    }
                ],

                ordering: false
            });
            desactivateLoading();
        } else {
            desactivateLoading();
        }
    } catch (error) {
        alertify.error(error)
        desactivateLoading();
    }
    desactivateLoading();
}

document.addEventListener('DOMContentLoaded', () => {
    getVehiculos();
});


$(document).on('click', '.btn-edit', function () {
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    id.disabled = true;
    id.value = dataRow.id;
    marca.value = dataRow.marca;
    tipov.value = dataRow.tipo;
    modelo.value = dataRow.modelo;
    inputs.style.display = 'block';
    placa.value = dataRow.placa;
    abrirModal('U')
});

$(document).on('click', '.btn-delete', function () {
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    id.disabled = true;
    tipov.disabled = true;
    modelo.style.display = 'none';
    placa.style.display = 'none';
    id.value = dataRow.id;
    inputs.style.display = 'none';
    if (dataRow.activo == 1) {
        btnTitulo.innerHTML = 'Desactivar';
        leyenda.innerHTML = `Esta seguro de desactivar este vehiculo?`;
    } else {
        leyenda.innerHTML = `Esta seguro de activar este vehiculo?`;
        btnTitulo.innerHTML = 'Activar';
    }
    divLeyendaEliminar.style.display = 'block'
    abrirModal('D')
});

function modificarVehiculo() {
    activateLoading();
    const formData = new FormData()
    formData.append("id", id.value);
    formData.append("tipov", tipov.value);
    formData.append("modelo", modelo.value);
    formData.append("marca", marca.value);
    formData.append("placa", placa.value);

    const url = tipo.value == 'I' ? "insertarVehiculo/" : tipo.value == 'U' ? "actualizarVehiculo/" : 'activoInactivo/';

    fetch(url, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value }
    }).then(response => response.json())
        .then(data => {
            if (data.flag) {
                limpiar();
                cerrarModal();
                $('#table').DataTable().destroy();
                getVehiculos();
                desactivateLoading();
                alertify.success(data.mensaje);
            } else {
                desactivateLoading();
                alertify.error(data.mensaje);
            }
        })
        .catch(error => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
    desactivateLoading();
}

function abrirModal(flag) {
    tipo.value = flag;
    if (flag == 'I') {
        datosID.style.display = 'none';
        tipov.disabled = false;
        inputs.style.display = 'block';
        modelo.style.display = 'block';
        placa.style.display = 'block';
        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#157347';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor = '#157347';
        btnTitulo.innerHTML = 'Guardar';
    } else if (flag == 'U') {
        id.disabled = true;
        datosID.style.display = 'block';
        tipov.disabled = false;
        modelo.style.display = 'block';
        placa.style.display = 'block';

        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#0b5ed7';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor = '#0b5ed7';
        btnTitulo.innerHTML = 'Actualizar';
    } else if (flag == 'D') {
        id.disabled = true;

        tipov.disabled = true;
        modelo.style.display = 'none';
        placa.style.display = 'none';


        divLeyendaEliminar.style.display = 'block'
        headerMondal.style.backgroundColor = '#d53545';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor = '#d53545';

    }
    $("#modalClientes").modal('show')
}

function cerrarModal(flag) {
    $("#modalClientes").modal('hide');
    limpiar();
}

function limpiar() {
    id.value = '';
    marca.value = '';
    tipov.value = '';
    modelo.value = '';
    placa.value = '';
    tipo.value = '';
}
