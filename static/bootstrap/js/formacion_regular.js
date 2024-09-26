  //funcionalidad para tabla, modales y filtros
  document.addEventListener('DOMContentLoaded', function() {
    

});





//verificacion de formulario metas formacion 
$(document).ready(function() {
    $(document).on('change', '#id_met_id', function() {
        var id_met_id = $(this).val();  // Año seleccionado
        var $modal = $(this).closest('.modal');
        var submitButton = $modal.find('#submit-second-modal_meta_formacion');

        if (id_met_id) {
            $.ajax({
                url: url_meta_formacion, // URL que devuelve modalidades y centros
                method: 'GET',
                data: { id_met_id: id_met_id },
                success: function(data) {
                    // Limpiar y actualizar el select de centros de formación
                    var selectCentro = $modal.find('#id_met_centro_formacion');
                    var messageCentro = $modal.find('#centro-message');
                    selectCentro.empty();
                    selectCentro.append('<option value="">Selecciona centro de formación</option>');
                    messageCentro.empty();

                    if (data.centros_disponibles.length === 0) {
                        // Si no hay centros disponibles para este año, mostrar el mensaje
                        messageCentro.text('No hay más centros disponibles para este año. No se pueden registrar más metas.');
                        submitButton.prop('disabled', true);  // Deshabilitar el botón
                    } else {
                        // Si hay centros disponibles, habilitar el select y el botón
                        $.each(data.centros_disponibles, function(index, centro) {
                            selectCentro.append('<option value="' + centro.id + '">' + centro.nombre + '</option>');
                        });
                        messageCentro.hide();  // Ocultar el mensaje si hay centros
                        submitButton.prop('disabled', false);

                        // Cuando se seleccione un centro, actualizar las modalidades
                        selectCentro.on('change', function() {
                            var centro_id = $(this).val(); // Centro seleccionado

                            if (centro_id) {
                                // Buscar el centro seleccionado en los datos recibidos
                                var centroSeleccionado = data.centros_disponibles.find(c => c.id == centro_id);

                                if (centroSeleccionado) {
                                    // Limpiar y actualizar el select de modalidades
                                    var selectModalidad = $modal.find('#id_metd_modalidad');
                                    var messageModalidad = $modal.find('#modalidad-message');
                                    selectModalidad.empty();
                                    selectModalidad.append('<option value="">Selecciona modalidad</option>');
                                    messageModalidad.empty();

                                    if (centroSeleccionado.modalidades_faltantes.length === 0) {
                                        messageModalidad.text('Este centro ya tiene todas las modalidades registradas.');
                                        submitButton.prop('disabled', true); // Deshabilitar el botón si no hay modalidades faltantes
                                    } else {
                                        $.each(centroSeleccionado.modalidades_faltantes, function(index, modalidad) {
                                            selectModalidad.append('<option value="' + modalidad.id + '">' + modalidad.modalidad + '</option>');
                                        });
                                        messageModalidad.hide();
                                        submitButton.prop('disabled', false);
                                    }
                                }
                            } else {
                                // Limpiar si no se ha seleccionado un centro
                                $('#id_metd_modalidad').empty().append('<option value="">Selecciona modalidad</option>');
                                $('#modalidad-message').empty();
                            }
                        });
                    }
                },
                error: function() {
                    alert('Error al cargar los datos.');
                }
            });
        } else {
            // Limpiar selects y mensajes si no hay selección
            $('#id_metd_modalidad').empty().append('<option value="">Selecciona modalidad</option>');
            $('#id_centro_formacion').empty().append('<option value="">Selecciona centro de formación</option>');
            $('#modalidad-message').empty();
            $('#centro-message').empty();
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
    const id_met_centro_formacion = button.getAttribute('data-centro-formacion')


    
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
    document.getElementById('id_met_centro_formacion').value = id_met_centro_formacion
    
  }