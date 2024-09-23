  //funcionalidad para tabla, modales y filtros
  document.addEventListener('DOMContentLoaded', function() {
    

});





//verificacion de formulario metas formacion 
$(document).ready(function() {
    $(document).on('change','#id_met_id',function() {
        var id_met_id = $(this).val();
        var $modal = $(this).closest('.modal');
        var submitButton = $modal.find('#submit-second-modal_meta_formacion');


        if (id_met_id) {
            $.ajax({
                url: url_meta_formacion,
                method: 'GET',
                data: { id_met_id: id_met_id },
                success: function(data) {
                    var select = $modal.find('#id_metd_modalidad');
                    var messageDiv = $modal.find('#modalidad-message');

                    select.empty();
                    select.append('<option value="">Selecciona modalidad</option>');
                    messageDiv.empty(); // Limpiar el mensaje anterior
                    
                    if (data.length === 0) {
                        // Si no hay modalidades, mostrar un mensaje
                        messageDiv.text('No hay modalidades habilitadas para este año.');
                        submitButton.prop('disabled', true); 
                    } else {
                        $.each(data, function(index, modalidad) {
                            select.append('<option value="' + modalidad.id + '">' + modalidad.modalidad + '</option>');
                        });
                        messageDiv.hide(); // Ocultar el mensaje
                        submitButton.prop('disabled', false);
                    }
                },
                error: function() {
                    alert('Error al cargar las modalidades.');
                }
            });
        } else {
            $('#id_metd_modalidad').empty().append('<option value="">Selecciona modalidad</option>');
            $('#modalidad-message').empty(); // Limpiar el mensaje si no hay selección
        }
    });
});




//funcionalidad de eliminar meta formacion
function Delete_meta_formacion(button) {
    console.log(button)
        
    document.getElementById('deleteForm').action = `/meta_formacion/delete/${button}`;
  }
  //funcionalidad de editar meta formacion
  
  function Editar_meta_formacion(button){
    
  
    const pk = button.getAttribute('data-id');
    const id_met_formacion_operario = button.getAttribute('data-operario')
    const id_met_formacion_auxiliar = button.getAttribute('data-auxiliar')
    const id_met_formacion_tecnico = button.getAttribute('data-tecnico')
    const id_met_formacion_profundizacion_tecnica = button.getAttribute('data-profundizacion')
    const id_met_formacion_tecnologo = button.getAttribute('data-tecnologo')
    const id_met_formacion_evento = button.getAttribute('data-evento')
    const id_met_formacion_curso_especial = button.getAttribute('data-curso-especial')
    const id_met_formacion_bilinguismo = button.getAttribute('data-bilinguismo')
    const id_met_formacion_sin_bilinguismo = button.getAttribute('data-sin-bilinguismo')
    const id_met_id = button.getAttribute('data-meta')
    const id_metd_modalidad = button.getAttribute('data-modalidad')
    

    
    document.getElementById('editarFormMetaFormacion').action = `/meta_formacion/edit/${pk}`;
    document.getElementById('id_met_formacion_operario').value = id_met_formacion_operario
    document.getElementById('id_met_formacion_auxiliar').value = id_met_formacion_auxiliar
    document.getElementById('id_met_formacion_tecnico').value = id_met_formacion_tecnico
    document.getElementById('id_met_formacion_profundizacion_tecnica').value = id_met_formacion_profundizacion_tecnica
    document.getElementById('id_met_formacion_tecnologo').value = id_met_formacion_tecnologo
    document.getElementById('id_met_formacion_evento').value = id_met_formacion_evento
    document.getElementById('id_met_formacion_curso_especial').value = id_met_formacion_curso_especial
    document.getElementById('id_met_formacion_bilinguismo').value = id_met_formacion_bilinguismo
    document.getElementById('id_met_formacion_sin_bilinguismo').value = id_met_formacion_sin_bilinguismo
    document.getElementById('id_met_id').value = id_met_id
    document.getElementById('id_metd_modalidad').value = id_metd_modalidad
    
    

    
  }