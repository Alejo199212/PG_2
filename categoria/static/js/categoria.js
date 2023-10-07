
const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const headerMondal = document.getElementById('headerMondal');
const tipo = document.getElementById('tipo');
const id = document.getElementById('id');
const nombre = document.getElementById('nombre');
const descripcion = document.getElementById('descripcion');
const divLeyendaEliminar = document.getElementById('divLeyendaEliminar');
const btnTitulo = document.getElementById('btnTitulo');
const btnConfirmar = document.getElementById('btnConfirmar');
const id_label = document.getElementById('id_label');

async function getCategoria() {

    try{
        activateLoading();
        let response = await fetch('listCategorias/',{ method:'GET'});
        if(response.ok){
            const responseJson = await response.json();
            
            $('#table').DataTable({
                data: responseJson,
                columns:[
                    {data:'id_categoria'},
                    {data:'nombre_categoria'},
                    {data:'descripcion'},
                    {data:'fecha_registro'},
                    {'defaultContent': '<button class="btn mx-1 btn-outline-primary btn-edit"><i class="fa-regular fa-pen-to-square"></i></button>' +
                    '<button class="btn mx-1 btn-outline-danger btn-delete"><i class="fa-solid fa-delete-left"></i></button>'}
                ],
               
                ordering: false
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
    getCategoria();
});

$(document).on('click','.btn-edit', function(){
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    id.disabled = true;
    id.value = dataRow.id_categoria;
    nombre.value = dataRow.nombre_categoria;
    descripcion.value = dataRow.descripcion;
    abrirModal('U')
});

$(document).on('click','.btn-delete', function(){
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    id.disabled = true;
    nombre.disabled = true;
    descripcion.disabled = true;
    id.value = dataRow.id_categoria;
    nombre.value = dataRow.nombre_categoria;
    descripcion.value = dataRow.descripcion;
    divLeyendaEliminar.style.display = 'block'
    abrirModal('D')
});


function abrirModal(flag){
    tipo.value = flag;
    if(flag == 'I'){
        id.style.display = 'none';
        id_label.style.display = 'none'
        nombre.disabled = false;
        descripcion.disabled = false;
        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#157347';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor =  '#157347';
        btnTitulo.innerHTML = 'Guardar';
    }else if(flag == 'U'){
        id.style.display = 'block';
        id_label.style.display = 'block'
        id.disabled = true;
        nombre.disabled = false;
        descripcion.disabled = false;
        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#0b5ed7';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor =  '#0b5ed7';
        btnTitulo.innerHTML = 'Actualizar';
    }else if(flag == 'D'){
        id.style.display = 'block';
        id_label.style.display = 'block'
        id.disabled = true;
        nombre.disabled = true;
        descripcion.disabled = true;
        divLeyendaEliminar.style.display = 'block'
        headerMondal.style.backgroundColor = '#d53545';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor =  '#d53545';
        btnTitulo.innerHTML = 'Eliminar';
    }
    $("#modalClientes").modal('show')
}


function cerrarModal(flag){
    $("#modalClientes").modal('hide');
    limpiar();
}

function limpiar(){
    id.value = '';
    nombre.value = '';
    descripcion.value = '';
}

function cerrarModal(flag){
    $("#modalClientes").modal('hide');
    limpiar();
}

function modificarCliente() {
    activateLoading();
    const formData = new FormData()
    formData.append("id", id.value);
    formData.append("nombre", nombre.value);
    formData.append("descripcion", descripcion.value);

    const url = tipo.value == 'I' ? "insertCategoria/" : tipo.value == 'U' ?"updateCategoria/":'eliminarCategoria/';

    fetch(url, {
        method: "POST",
        body: formData,
        headers: {"X-CSRFToken": token.value}
    }).then(response => response.json())
        .then(data => {
            if(data.flag){
                limpiar();
                cerrarModal();
                $('#table').DataTable().destroy();
                getCategoria();
                desactivateLoading();
                alertify.success(data.mensaje);
            }else{
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