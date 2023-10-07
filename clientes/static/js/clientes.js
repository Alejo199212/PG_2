const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const nit = document.getElementById('nit');
const nombres = document.getElementById('nombres');
const apellidos = document.getElementById('apellidos');
const correo = document.getElementById('correo');
const telefono = document.getElementById('telefono');
const tipo = document.getElementById('tipo');
const labelTelefono = document.getElementById('labelTelefono');
const labelCorreo = document.getElementById("labelCorreo");
const divLeyendaEliminar = document.getElementById('divLeyendaEliminar');
const headerMondal = document.getElementById('headerMondal');
const btnConfirmar = document.getElementById('btnConfirmar');
const btnTitulo = document.getElementById('btnTitulo');
const direccion = document.getElementById('direccion');
const codCliente = document.getElementById('codCliente');
const groupCodCliente = document.getElementById('groupCodCliente');
const groupDireccion = document.getElementById('groupDireccion')

async function getClientes() {

    try{
        activateLoading();
        let response = await fetch('listClient/',{ method:'GET'});
        if(response.ok){
            const responseJson = await response.json();
            
            $('#table').DataTable({
                data: responseJson,
                columns:[
                    {data:'cod_cliente'},
                    {data:'nit'},
                    {data:'nombres'},
                    {data:'apellidos'},
                    {data:'fechaRegistro'},
                    {data:'correo'},
                    {data:'telefono'},
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
    getClientes();
});


$(document).on('click','.btn-edit', function(){
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    groupDireccion.style.display = 'block'
    codCliente.disabled = true;
    codCliente.value = dataRow.cod_cliente;
    nit.value = dataRow.nit;
    nombres.value = dataRow.nombres;
    apellidos.value = dataRow.apellidos;
    correo.value =dataRow.correo;
    telefono.value = dataRow.telefono;
    abrirModal('U')
});

$(document).on('click','.btn-delete', function(){
    const parentBtn = $(this).closest('tr');
    const tabla = $('#table').DataTable();
    const dataRow = tabla.row(parentBtn).data();
    codCliente.disabled = true;
    codCliente.value = dataRow.cod_cliente;
    nit.disabled = true;
    nombres.disabled = true;
    apellidos.disabled = true;
    correo.style.display = 'none';
    telefono.style.display = 'none';
    labelTelefono.style.display = 'none';
    labelCorreo.style.display = 'none';
    nit.value = dataRow.nit;
    nombres.value = dataRow.nombres;
    apellidos.value = dataRow.apellidos;
    divLeyendaEliminar.style.display = 'block'
    groupDireccion.style.display = 'none'
    abrirModal('D')
});

function modificarCliente() {
    activateLoading();
    const formData = new FormData()
    formData.append("codCliente", codCliente.value);
    formData.append("nit", nit.value);
    formData.append("nombres", nombres.value);
    formData.append("apellidos", apellidos.value);
    formData.append("correo", correo.value);
    formData.append("telefono", telefono.value);
    formData.append("direccion", direccion.value);

    const url = tipo.value == 'I' ? "insertClient/" : tipo.value == 'U' ?"updateClient/":'deleteClient/';

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
                getClientes();
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

function abrirModal(flag){
    tipo.value = flag;
    if(flag == 'I'){
        groupDireccion.style.display = 'block'
        groupCodCliente.style.display = 'none'
        nit.disabled = false;
        nombres.disabled = false;
        apellidos.disabled = false;
        correo.style.display = 'block';
        telefono.style.display = 'block';
        labelTelefono.style.display = 'block';
        labelCorreo.style.display = 'block';
        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#157347';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor =  '#157347';
        btnTitulo.innerHTML = 'Guardar';
    }else if(flag == 'U'){
        groupCodCliente.style.display = 'block'
        nombres.disabled = false;
        apellidos.disabled = false;
        correo.style.display = 'block';
        telefono.style.display = 'block';
        labelTelefono.style.display = 'block';
        labelCorreo.style.display = 'block';
        divLeyendaEliminar.style.display = 'none'
        headerMondal.style.backgroundColor = '#0b5ed7';
        headerMondal.style.color = '#fff';
        btnConfirmar.style.backgroundColor =  '#0b5ed7';
        btnTitulo.innerHTML = 'Actualizar';
    }else if(flag == 'D'){
        groupCodCliente.style.display = 'block'
        codCliente.disabled = true;
        nit.disabled = true;
        nombres.disabled = true;
        apellidos.disabled = true;
        correo.style.display = 'none';
        telefono.style.display = 'none';
        labelTelefono.style.display = 'none';
        labelCorreo.style.display = 'none';
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
    nit.value = '';
    nombres.value = '';
    apellidos.value = '';
    correo.value = '';
    telefono.value = '';
    tipo.value= '';
}
