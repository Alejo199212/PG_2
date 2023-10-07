const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
async function getEventosFacturados() {
    try {
        activateLoading();
        let response = await fetch("listadoFacturados/", { method: "GET" });

        if (response.ok) {
            const responseJson = await response.json();
            
            $("#tableFacturados").DataTable({
                data: responseJson,
                columns: [
                    { data: "id_evento" },
                    { data: "nit" },
                    { data: "nombreFact" },
                    {data:"numI"},
                    { data: "num" },
                    { data: "serie" },
                    {
                        defaultContent:
                            '<button class="btn mx-1 btn-outline-danger btn-fact" data-toggle="tooltip" data-placement="top" title="Ver"><i class="fa-regular fa-file-pdf"></i></button>'

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
    getEventosFacturados()
});


$(document).on("click", ".btn-fact", function () {
    const parentBtn = $(this).closest("tr");
    const tabla = $("#tableFacturados").DataTable();
    const dataRow = tabla.row(parentBtn).data();
    verFactura(dataRow.numI)
});

function verFactura(numInterno) {
    activateLoading();
    
    const formData = new FormData();
    formData.append("numInterno", numInterno);
   
    fetch('verFact/', {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": token.value },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.flag) {
                alertify.success(data.mensaje)
                let pdfContenido = atob(data.pdf);
                let blob = new Blob([pdfContenido], { type: 'application/pdf' });
                let url = URL.createObjectURL(blob)
                window.open(url,'_blank');
               
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