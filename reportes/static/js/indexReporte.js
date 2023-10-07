
const token = document.querySelector('input[name="csrfmiddlewaretoken"]');
const tituloLabel = document.getElementById('tituloLabel');
const url = document.getElementById('url');
const inicio = document.getElementById('inicio');
const fin = document.getElementById('hasta');
const fechas = document.getElementById('fechas');

function abrirModal(ruta,titulo,flag){
    if (flag == 'B' || flag == 'C'){
        fechas.style.display = 'block'
    }
    if(flag == 'I'){
        fechas.style.display = 'none'
    }
    tituloLabel.innerText = titulo;
    url.value = ruta;
    $('#reporte').modal('show')
}

function verReportes() {
    activateLoading();
    
    const formData = new FormData();
    formData.append("inicio", inicio.value);
    formData.append('fin',fin.value)

    fetch(url.value, {
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