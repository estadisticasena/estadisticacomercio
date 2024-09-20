document.addEventListener('DOMContentLoaded', function() {
    // Solo permitir números en los campos de documento y teléfono
    document.querySelectorAll('input[name="per_documento"], input[name="per_telefono"]').forEach(function(input) {
        input.addEventListener('keypress', function(event) {
            if (!/[0-9]/.test(event.key)) {
                event.preventDefault();
            }
        });
    });

    var emailInput = document.getElementById('email');
    var documentoInput = document.getElementById('per_documento');
    var password1Input = document.getElementById('password1');
    var password2Input = document.getElementById('password2');

    var errorEmailFormat = document.getElementById('error_email_format');
    var errorEmailNotFound = document.getElementById('error_email_not_found');
    var errorPasswordMatch = document.getElementById('error_password_match');
    var errorPasswordStrength = document.getElementById('error_password_strength');
    var errorDocumentoExists = document.getElementById('error_documento_exists');

    var submitButton = document.querySelector('.boton_registro');

    // Agregar event listeners para las validaciones
    emailInput.addEventListener('input', validateEmail);
    documentoInput.addEventListener('input', validateDocumento);
    password1Input.addEventListener('input', validatePasswords);
    password2Input.addEventListener('input', validatePasswords);

    // Función para validar el correo electrónico
    function validateEmail() {
        var isValidEmailFormat = /\S+@\S+\.\S+/.test(emailInput.value);
        if (!isValidEmailFormat) {
            errorEmailFormat.style.display = 'block';
        } else {
            errorEmailFormat.style.display = 'none';
            // Verificación de existencia del correo electrónico en la base de datos
            var url = validarEmailURL + '?email=' + emailInput.value;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        errorEmailNotFound.style.display = 'block';
                    } else {
                        errorEmailNotFound.style.display = 'none';
                    }
                    updateSubmitButton();
                })
                .catch(error => {
                    console.error('Error al verificar el correo electrónico:', error);
                    updateSubmitButton();
                });
        }
        updateSubmitButton();
    }

    // Función para validar el documento
    function validateDocumento() {
        var documentoValue = documentoInput.value.trim();
        // Verificación de existencia del documento en la base de datos
        var url = validarDocumentoURL + '?documento=' + documentoValue;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    errorDocumentoExists.style.display = 'block';
                } else {
                    errorDocumentoExists.style.display = 'none';
                }
                updateSubmitButton();
            })
            .catch(error => {
                console.error('Error al verificar el documento:', error);
                updateSubmitButton();
            });
    }

    // Función para validar las contraseñas
    function validatePasswords() {
        var password1 = password1Input.value;
        var password2 = password2Input.value;

        // Validar longitud mínima y combinación de números y letras
        var hasNumber = /\d/.test(password1);
        var hasLetter = /[a-zA-Z]/.test(password1);
        var isValidLength = password1.length >= 8;

        if (!isValidLength || !(hasNumber && hasLetter)) {
            errorPasswordStrength.style.display = 'block';
        } else {
            errorPasswordStrength.style.display = 'none';
        }

        // Validar coincidencia entre las contraseñas
        if (password1 !== password2) {
            errorPasswordMatch.style.display = 'block';
        } else {
            errorPasswordMatch.style.display = 'none';
        }

        updateSubmitButton();
    }

    // Función para actualizar el estado del botón de enviar
    function updateSubmitButton() {
        var errors = [
            errorEmailFormat.style.display === 'block',
            errorEmailNotFound.style.display === 'block',
            errorPasswordMatch.style.display === 'block',
            errorPasswordStrength.style.display === 'block',
            errorDocumentoExists.style.display === 'block'
        ];
        var isValid = !errors.some(error => error);
        submitButton.disabled = !isValid;
    }

    // Evitar que el formulario se envíe al hacer clic en enviar si hay errores
    submitButton.addEventListener('click', function(event) {
        if (submitButton.disabled) {
            event.preventDefault();
            // Aquí podrías mostrar algún mensaje o indicación al usuario de que debe corregir los errores.
        }
    });
});
