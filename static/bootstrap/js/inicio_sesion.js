
document.addEventListener('DOMContentLoaded', (event) => {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 5000); // Ocultar el mensaje después de 5 segundos
    }
});

document.getElementById('id_per_documento').addEventListener('input', function(event) {
    var documento = this.value;
    var errorMessage = document.getElementById('error_per_documento');

    if (!/^\d*$/.test(documento)) {
        errorMessage.style.display = 'block'; // Muestra el mensaje de error
    } else {
        errorMessage.style.display = 'none'; // Oculta el mensaje de error si es válido
    }
});

document.getElementById('id_password1').addEventListener('input', function(event) {
    var password = this.value;
    var errorMessage = document.getElementById('error_password1');

    if (password.length < 8 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
        errorMessage.style.display = 'block'; // Muestra el mensaje de error
    } else {
        errorMessage.style.display = 'none'; // Oculta el mensaje de error si es válido
    }
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    var documento = document.getElementById('id_per_documento').value;
    var password = document.getElementById('id_password1').value;

    // Validación para el campo documento (solo números)
    if (!/^\d*$/.test(documento)) {
        event.preventDefault(); // Evita que se envíe el formulario
        document.getElementById('error_per_documento').style.display = 'block'; // Muestra el mensaje de error
    } else {
        document.getElementById('error_per_documento').style.display = 'none'; // Oculta el mensaje de error si es válido
    }

    // Validación para el campo contraseña (mínimo 8 caracteres y al menos un número y una letra)
    if (password.length < 8 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
        event.preventDefault(); // Evita que se envíe el formulario
        document.getElementById('error_password1').style.display = 'block'; // Muestra el mensaje de error
    } else {
        document.getElementById('error_password1').style.display = 'none'; // Oculta el mensaje de error si es válido
    }
});