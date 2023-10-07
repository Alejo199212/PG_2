

async function getEventos() {
    try {
        activateLoading();
        let response = await fetch("listadoEventoProceso/", { method: "GET" });

        if (response.ok) {
            const responseJson = await response.json();

            $("#table").DataTable({
                data: responseJson,
                columns: [
                    { data: "cod_cliente" },
                    { data: "nombre" },
                    { data: "id_evento" },
                    { data: "estado" },
                    {
                        defaultContent:
                            '<button class="btn mx-1 btn-outline-primary btn-edit" data-toggle="tooltip" data-placement="top" title="Completar Evento"><i class="fa-regular fa-pen-to-square"></i></button>' +
                            '<button class="btn mx-1 btn-outline-danger btn-delete" data-toggle="tooltip" data-placement="top" title="Anular Evento"><i class="fa-solid fa-delete-left"></i></button>',
                    }
                ],

                ordering: false,
            });
            desactivateLoading();
        } else {
            desactivateLoading();
        }
    } catch (error) {
        
        desactivateLoading();
    }
    desactivateLoading();
}

document.addEventListener("DOMContentLoaded", () => {
    if (listarEventos) {
        getEventos();
    }
});

$(document).on("click", ".btn-delete", function () {
    const parentBtn = $(this).closest("tr");
    const tabla = $("#table").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    alertify.confirm(
        "Anular evento",
        "Esta seguro de anular el evento " + dataRow.id_evento,
        function () {
            anularEvento(dataRow.id_evento);
        },
        function () {
            alertify.error("Cancel");
        }
    );
});

$(document).on("click", ".btn-edit", function () {
    const parentBtn = $(this).closest("tr");
    const tabla = $("#table").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    abrirModalBtn(dataRow.id_evento);
});

function anularEvento(orden) {
    const formData = new FormData();
    formData.append("orden", orden);

    fetch(ulrAnular, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                $("#table").DataTable().destroy();
                if (listarEventos) {
                    getEventos();
                } else {
                    getEventosCompletados();
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
