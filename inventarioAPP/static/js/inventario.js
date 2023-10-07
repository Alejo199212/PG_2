const categoriaSelect = document.getElementById('categoriaSelect');
const cod = document.getElementById('cod');
const nombre = document.getElementById('nombre');
const descripcion = document.getElementById('descripcion');
const alerta = document.getElementById('alerta');
const numFact = document.getElementById('numFact');
const serie = document.getElementById('serie');
const precio = document.getElementById('precio');
const cantidad = document.getElementById('cantidad');
const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const user = document.getElementById('user');
const producto = document.getElementById('producto');
const bodyActualizar = document.getElementById('bodyActualizar');
const btnAgregar = document.getElementById('btnAgregar');
const btnConf = document.getElementById('btnConf');
const addFooter = document.getElementById('addFooter');
const tipo = document.getElementById('tipo');
const actualizarCantidad = document.getElementById('actualizarCantidad');
const actualizarDatos = document.getElementById('actualizarDatos');
const facturaCompras = document.getElementById('factC');
const btnCheck = document.querySelectorAll('.btn-check');
const motivo = document.getElementById('motivo');
const displayMotivo = document.getElementById('displayMotivo');

async function getInventario() {

    try {
        activateLoading();
        let response = await fetch('listInventario/', { method: 'GET' });
        if (response.ok) {
            const responseJson = await response.json();

            $('#table').DataTable({
                data: responseJson,
                columns: [
                    { data: 'codigo' },
                    { data: 'nombre' },
                    { data: 'descripcion' },
                    { data: 'cantidad' },
                    { data: 'alerta' },
                    {
                        data: 'activo',
                        render: function (data, type, row) {
                            if (data <= 0) {
                                return "<span class='text-danger p-1 font-weight-bold'>NO</span>"
                            } else {
                                return "<span class='text-success p-1 font-weight-bold'>SI</span>"
                            }
                        }

                    },
                    { data: 'categoria' },
                    {
                        'defaultContent': '<button class="btn mx-1 btn-outline-primary btn-edit" data-toggle="tooltip" data-placement="top" title="Editar Información de producto"><i class="fa-regular fa-pen-to-square"></i></button>' +
                            '<button class="btn mx-1 btn-outline-danger btn-delete" data-toggle="tooltip" data-placement="top" title="Desactivar/Activar Producto"><i class="fa-solid fa-delete-left"></i></button>' +
                            '<button class="btn mx-1 btn-dark btn-stock" data-toggle="tooltip" data-placement="top" title="Actualizar Existencia"><i class="fa-solid fa-boxes-stacked"></i></button>'
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
    getInventario();
    getCategoria();
});

function abrirModal(flag) {
    limpiar();
    addFooter.innerHTML = ``;
    tipo.value = flag;
    const footer = btnAgregar.content.cloneNode(true);
    addFooter.appendChild(footer);
    actualizarCantidad.style.display = 'none';
    actualizarDatos.style.display = 'Block'
    facturaCompras.style.display = 'Block'
    displayMotivo.style.display = 'none';
    $("#modalAgregar").modal('show')
}


function moverSiguiente() {
    let movimiento = $('input[name="tipoOperacion"]:checked').val()
    if (tipo.value === 'S' && movimiento === 'C') {
        facturaCompras.style.display = 'Block'
        displayMotivo.style.display = 'none';
        $('#carruselInventario').carousel('next');
    } else if (tipo.value == 'S' && movimiento == 'B') {
        facturaCompras.style.display = 'none'
        displayMotivo.style.display = 'Block';
        $('#carruselInventario').carousel('next');
    } else if (tipo.value != 'S') {
        $('#carruselInventario').carousel('next');
    } else {
        alertify.error("Seleccione alguna opcion")
    }


}

function moverAtras() {
    $('#carruselInventario').carousel('prev');
}

async function getCategoria() {

    try {
        activateLoading();
        categoriaSelect.innerHTML = ``;
        categoriaSelect.innerHTML = `<option selected>Seleccionar Categoria</option>`;
        //categoriaSelect.innerHTML+= `Seleccionar categoria`;
        let response = await fetch('listCategorias/', { method: 'GET' });
        if (response.ok) {
            const responseJson = await response.json();
            for (let i = 0; i < responseJson.length; i++) {
                categoriaSelect.innerHTML += `
                <option value="${responseJson[i].id_categoria}">${responseJson[i].nombre_categoria}</option>
                `;
            }
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

function cerrarModal() {
    $("#modalAgregar").modal('hide');
    limpiar();
}

function limpiar() {
    cod.value = '';
    nombre.value = '';
    descripcion.value = '';
    alerta.value = '';
    numFact.value = '';
    serie.value = '';
    precio.value = ''
    cantidad.value = '';
    categoriaSelect.selectedIndex = 0;
    tipo.value = '';
    cod.disabled = false;
    $('input[name="tipoOperacion"]').prop('checked', false);
    $('#carruselInventario').carousel(0);
}

function objCrear() {
    const formData = new FormData();
    formData.append('cod', cod.value);
    formData.append('nombre', nombre.value);
    formData.append('descripcion', descripcion.value);
    formData.append('alerta', alerta.value);
    formData.append('numFact', numFact.value);
    formData.append('serie', serie.value);
    formData.append('categoria', categoriaSelect.value == null ? null : categoriaSelect.value);
    formData.append('precio', precio.value);
    formData.append('cantidad', cantidad.value);
    formData.append('user', user.value);

    return formData;
}

function objActualizar() {
    const formData = new FormData();
    formData.append('cod', cod.value);
    formData.append('nombre', nombre.value);
    formData.append('descripcion', descripcion.value);
    formData.append('alerta', alerta.value);
    formData.append('categoria', categoriaSelect.value == null ? null : categoriaSelect.value);
    return formData;
}

function objActualizarCantidad() {
    const formData = new FormData();
    formData.append('cod', cod.value);
    formData.append('numFact', numFact.value);
    formData.append('serie', serie.value);
    formData.append('precio', precio.value);
    formData.append('cantidad', cantidad.value);
    formData.append('user', user.value);
    return formData;
}

function objBaja() {
    const formData = new FormData();
    formData.append('cod', cod.value);
    formData.append('motivo', motivo.value);
    formData.append('cantidad', cantidad.value);
    formData.append('user', user.value);
    return formData;
}

function objDesactivar() {
    const formData = new FormData();
    formData.append('cod', cod.value);
    return formData;
}

async function enviarInformacion() {
    let movimiento = $('input[name="tipoOperacion"]:checked').val()
  
    let formData = new FormData();
    let url = '';
    switch (tipo.value) {
        case 'I': formData = objCrear();
            url = 'insertarInventario/';
            break;
        case "U": formData = objActualizar();
            url = 'actualizarInventario/';
            break;
        case "S": if (movimiento == 'C') {
            formData = objActualizarCantidad()
            url = 'actualizarCantidad/';
        } else if (movimiento == 'B') {
            formData = objBaja()
            url = 'bajaArticulo/';
        } else {
            alertify.error("Opcion no encontrada")
        }
            break;
        case "D": formData = objDesactivar()
            url = 'desactivar/';
            break;
        case "A": formData = objDesactivar()
            url = 'desactivar/';
            break;
        default: alert.error('Opcion No existe');
    }

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
                getInventario();
                desactivateLoading();
                alertify.success(data.mensaje)
            } else {
                desactivateLoading();
                alertify.error(data.mensaje);
            }
        })
        .catch(error => {
            alertify.error(error.mensaje);
            desactivateLoading();
        });
}

$(document).on('click', '.btn-edit', function () {
    addFooter.innerHTML = ``;
    limpiar();
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    const footer2 = btnConf.content.cloneNode(true);
    addFooter.appendChild(footer2)
    cod.disabled = true;
    cod.value = dataRow.codigo;
    nombre.value = dataRow.nombre;
    descripcion.value = dataRow.descripcion
    alerta.value = dataRow.alerta;
    actualizarCantidad.style.display = 'none';
    actualizarDatos.style.display = 'Block'
    for (let i = 0; i < categoriaSelect.options.length; i++) {
        if (categoriaSelect.options[i].textContent === dataRow.categoria) {
            categoriaSelect.selectedIndex = i;
            break;
        }
    }
    tipo.value = 'U'

    $("#modalAgregar").modal('show')
});

$(document).on('click', '.btn-stock', function () {
    addFooter.innerHTML = ``;
    limpiar();
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    const footer = btnAgregar.content.cloneNode(true);
    addFooter.appendChild(footer)
    cod.disabled = true;
    cod.value = dataRow.codigo;
    actualizarDatos.style.display = 'none';
    actualizarCantidad.style.display = 'block';
    tipo.value = 'S'

    $("#modalAgregar").modal('show')
});

$(document).on('click', '.btn-delete', function () {
    addFooter.innerHTML = ``;
    limpiar();
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    const footer2 = btnConf.content.cloneNode(true);
    addFooter.appendChild(footer2)
    cod.disabled = true;
    cod.value = dataRow.codigo;
    actualizarDatos.style.display = 'none';
    actualizarCantidad.style.display = 'none';

    if (dataRow.activo == 1) {
        tipo.value = 'D'
    } else {
        tipo.value = 'A'
    }


    $("#modalAgregar").modal('show')
});


function enviar() {
    if (tipo.value == 'D') {
        alertify.confirm('Desactivar', 'Esta seguro que quiere desactivar este activo',
            function () {
                enviarInformacion();
            }
            , function () { alertify.error('Cancel') });
    } else {
        enviarInformacion();
    }
}