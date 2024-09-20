const botonesMostrar = document.querySelectorAll(".mostrarFormulario");
const ventanaEmergente = document.getElementById("ventanaEmergente");
const modalContent = document.querySelector(".modal-content");
const btnCerrar = document.querySelector(".btn-danger");

// Agregar un event listener a cada botón
botonesMostrar.forEach(boton => {
    boton.addEventListener("click", () => {
        // Mostrar la ventana emergente
        ventanaEmergente.style.display = "flex";

        // Obtener el identificador de la ficha
        var identificador_ficha = boton.getAttribute('data-identificador');
        console.log("Identificador de ficha:", identificador_ficha); 

        // Realizar la solicitud AJAX para obtener los detalles de la ficha
        $.ajax({
            url: '/ficha/' + identificador_ficha + '/',
            method: 'GET',
            success: function(data) {
                console.log("Datos recibidos:", data); // Depuración

                // Mostrar los detalles de la ficha en el modal
                $('#detalleIdentificador').text(data.identificador_ficha);
                $('#detalleCampo1').text(data.campo1);
                $('#detalleCampo2').text(data.campo2);
                $('#detalleCampo3').text(data.campo3);
                $('#detalleCampo4').text(data.campo4);
                $('#detalleCampo5').text(data.campo5);
                $('#detalleCampo6').text(data.campo6);
                $('#detalleCampo7').text(data.campo7);
                $('#detalleCampo8').text(data.campo8);
                $('#detalleCampo9').text(data.campo9);
                // Añade más campos según los necesites
            },
            error: function(xhr, status, error) {
                console.error("Error en la solicitud AJAX:", status, error); // Depuración
            }
        });
    });
});

// Escuchar el evento de clic en el botón de cerrar dentro del modal
btnCerrar.addEventListener("click", function() {
    // Ocultar la ventana emergente
    ventanaEmergente.style.display = "none";
});
    