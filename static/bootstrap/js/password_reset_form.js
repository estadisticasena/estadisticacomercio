document.addEventListener('DOMContentLoaded', function() {
    var emailInput = document.getElementById('id_email');
    var errorEmailFormat = document.getElementById('error_email_format');
    var errorEmailNotFound = document.getElementById('error_email_not_found');

    emailInput.addEventListener('input', function(event) {
        var isValidEmailFormat = /\S+@\S+\.\S+/.test(emailInput.value);
        if (!isValidEmailFormat) {
            errorEmailFormat.style.display = 'block';
            errorEmailNotFound.style.display = 'none';
        } else {
            errorEmailFormat.style.display = 'none';
        }
    });

    document.getElementById('password_reset_form').addEventListener('submit', function(event) {
        var isValidEmailFormat = /\S+@\S+\.\S+/.test(emailInput.value);
        if (!isValidEmailFormat) {
            errorEmailFormat.style.display = 'block';
            errorEmailNotFound.style.display = 'none';
            event.preventDefault();
        } else {
            errorEmailFormat.style.display = 'none';

            var url = validarEmailURL + '?email=' + emailInput.value;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        errorEmailNotFound.style.display = 'none';
                    } else {
                        errorEmailNotFound.style.display = 'block';
                        event.preventDefault();
                    }
                })
                .catch(error => {
                    console.error('Error al verificar el correo electrónico:', error);
                });
        }
    });
});