


// funcion de modales 

document.addEventListener('DOMContentLoaded', function() {

        document. metaField =  document.getElements
        document.querySelector('#submit-second-modal_meta').addEventListener('click', function(event) {
            event.preventDefault(); // Evita el comportamiento por defecto del botón
    
            // Selecciona el formulario en el segundo modal
            var form = document.querySelector('#second-modal-form_meta');
            var formData = new FormData(form);
    
            // Envía los datos del formulario usando fetch
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Simula el clic en el botón de cerrar para cerrar el segundo modal
                    document.querySelector('#close-second-modal').click();
    
                    // Limpia el formulario después de cerrar el modal
                    form.reset();
                    
                } else {
                    // Muestra errores si la respuesta es fallida
                    console.log('Error:', data.errors);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });









//fechas inicio y fin 
document.getElementById('id_met_fecha_inicio').addEventListener('change', validateDates);
document.getElementById('id_met_fecha_fin').addEventListener('change', validateDates);

function validateDates() {
    const startDateInput = document.getElementById('id_met_fecha_inicio');
    const endDateInput = document.getElementById('id_met_fecha_fin');
    const errorDiv = document.getElementById('dateErrorMeta');
    const submitButton = document.getElementById('submit-second-modal_meta');

    const startDate = new Date(startDateInput.value);
    const endDate = new Date(endDateInput.value);

    if (startDate && endDate && startDate >= endDate) {
        errorDiv.style.display = 'block';  // Mostrar mensaje de error
        submitButton.disabled = true;      // Desactivar el botón
    } else {
        errorDiv.style.display = 'none';   // Ocultar mensaje de error
        submitButton.disabled = false;     // Activar el botón
    }
}

//validaciones para meta estrategia
$(document).ready(function() {
    $(document).on('change', '#id_estd_meta', function() {
        var id_estd_meta = $(this).val();
        var $modal = $(this).closest('.modal');
        var submitButton = $modal.find('#submit-second-modal_meta_formacion');

        if (id_estd_meta) {
            $.ajax({
                url: url_meta_verificacion, // URL que devuelve las metas
                method: 'GET',
                data: { id_estd_meta: id_estd_meta },
                success: function(data) {
                    // Limpiar y actualizar selects
                    var selectEstrategia = $modal.find('#id_est_id');
                    var selectModalidad = $modal.find('#id_estd_modalidad');
                    selectEstrategia.empty();
                    selectModalidad.empty();

                    if (data.error) {
                        // Manejar el error en la respuesta
                        alert(data.error);
                        submitButton.prop('disabled', true);
                    } else {
                        // Llenar el select de estrategias
                        $.each(data.estrategias, function(index, estrategia) {
                            selectEstrategia.append('<option value="' + estrategia.id + '">' + estrategia.nombre + '</option>');
                        });

                        // Llenar el select de modalidades
                        $.each(data.modalidades, function(index, modalidad) {
                            selectModalidad.append('<option value="' + modalidad.id + '">' + modalidad.nombre + '</option>');
                        });

                        // Habilitar el botón si hay estrategias y modalidades disponibles
                        if (data.estrategias.length > 0 && data.modalidades.length > 0) {
                            submitButton.prop('disabled', false);
                        } else {
                            submitButton.prop('disabled', true);
                        }
                    }
                },
                error: function() {
                    alert('Error al cargar los datos.');
                }
            });
        } else {
            // Limpiar selects si no hay selección
            $('#id_est_id').empty().append('<option value="">Selecciona estrategia</option>');
            $('#id_estd_modalidad').empty().append('<option value="">Selecciona modalidad</option>');
        }
    });
});


function Delete_estrategia(button) {
    const pk = button.getAttribute('data-id');
    document.getElementById('deleteForm').action = `/estrategia_institucional/delete/${pk}`;
}
function Editar_estrategia(button){
    const pk = button.getAttribute('data-id');
    const id_est_nombre = button.getAttribute('data-nombre')
 

    document.getElementById('editarForm').action = `/estrategia_institucional/edit/${pk}`;
    document.getElementById('id_est_nombre').value = id_est_nombre
  
}

function Delete_meta_estrategia(button) {
    const pk = button.getAttribute('data-id');
    document.getElementById('deleteFormMetaEstrategia').action = `/meta_estrategias_intitucionales/delete/${pk}`;
}
function Editar_meta_estrategia(button){
    const pk = button.getAttribute('data-id');
    const estd_modalidad = button.getAttribute('data-modalidad')
    const id_est_id = button.getAttribute('data-estrategia')
    const id_estd_meta = button.getAttribute('data-meta')
    console.log('kkk',id_estd_meta)

    const metaEstrategia = document.getElementById('id_est_id')
    const metaField = document.getElementById('id_estd_meta')
   
    metaField.value = id_estd_meta
    
    

    


    
    
    //preseleccion meta
    function opciones(id_estd_meta){
        fetch(`/meta_data/${id_estd_meta}`)
        .then(response => response.json())
        .then(data =>{
            console.log('dddd',data)

         
           

            if(data.meta){
                    const meta = data.meta;
                    const option = document.createElement('option');
                    option.value = meta.est_id;

                    metaEstrategia.innerHTML = '';
                 
                    option.textContent = meta.est_nombre;
                    console.log('Opción en el select:', option);
                    
                    console.log('Opción en el select:', option);
                    metaEstrategia.appendChild(option);

                    setTimeout(() => {

                    metaEstrategia.value = String(id_est_id);
                    
                },100);

            }
        })
    }
    
    if(id_estd_meta){
        opciones(id_estd_meta)

        metaField.dispatchEvent(new Event('change'))
 
     
  
    }

    
        
        

    

    const id_estd_profundizacion_tecnica_meta = button.getAttribute('data-total-profundizacion')
    const id_estd_curso_especial = button.getAttribute('data-cuso')
    const id_estd_tecnico_meta = button.getAttribute('data-tecnico')
    const id_estd_evento = button.getAttribute('data-evento')
    const id_estd_tecnologo = button.getAttribute('data-tecnologo')
    const id_estd_bilinguismo = button.getAttribute('data-bilinguismo')
    const id_estd_sin_bilinguismo = button.getAttribute('data-sin_bilinguismo')
    const id_estd_operario_meta = button.getAttribute('data-operario')
    const id_estd_auxiliar_meta = button.getAttribute('data-auxiliar')
   

  
 
    document.getElementById('editarFormMetaEstrategiaTotal').action = `/meta_estrategias_intitucionales/edit/${pk}`;
    document.getElementById('id_estd_modalidad').value = estd_modalidad
  
    document.getElementById('id_estd_profundizacion_tecnica_meta').value = id_estd_profundizacion_tecnica_meta
    document.getElementById('id_estd_curso_especial').value = id_estd_curso_especial
    document.getElementById('id_estd_tecnico_meta').value = id_estd_tecnico_meta
    document.getElementById('id_estd_evento').value = id_estd_evento
    document.getElementById('id_estd_tecnologo').value = id_estd_tecnologo
    document.getElementById('id_estd_bilinguismo').value = id_estd_bilinguismo
    document.getElementById('id_estd_sin_bilinguismo').value = id_estd_sin_bilinguismo
    document.getElementById('id_estd_operario_meta').value = id_estd_operario_meta
    document.getElementById('id_estd_auxiliar_meta').value = id_estd_auxiliar_meta
    
}
