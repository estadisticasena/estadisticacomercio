document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('id_new_password1').addEventListener('input', function(event) {
        validatePassword();
    });

    document.getElementById('id_new_password2').addEventListener('input', function(event) {
        validatePassword();
    });

    function validatePassword() {
        var password1 = document.getElementById('id_new_password1').value;
        var password2 = document.getElementById('id_new_password2').value;
        var errorMessage1 = document.getElementById('error_new_password1');
        var errorMessage2 = document.getElementById('error_new_password2');
        var valid = true;

        // Validación de longitud y contenido de contraseña
        if (password1.length < 8 || !/\d/.test(password1) || !/[a-zA-Z]/.test(password1)) {
            errorMessage1.style.display = 'block';
            valid = false;
        } else {
            errorMessage1.style.display = 'none';
        }

        // Validación de coincidencia de contraseñas
        if (password1 !== password2) {
            errorMessage2.style.display = 'block';
            valid = false;
        } else {
            errorMessage2.style.display = 'none';
        }

        // Devolver si el formulario es válido
        return valid;
    }
});
