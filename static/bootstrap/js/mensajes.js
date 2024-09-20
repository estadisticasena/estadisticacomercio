document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('profileImage').addEventListener('click', function() {
        document.getElementById('fileUpload').click();
    });

    document.getElementById('fileUpload').addEventListener('change', function(event) {
        const [file] = event.target.files;
        if (file) {
            document.getElementById('profileImage').src = URL.createObjectURL(file);
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        setTimeout(function () {
            messageContainer.style.opacity = '0';
            setTimeout(function () {
                messageContainer.style.display = 'none';
            }, 500); // Tiempo adicional para la transición de opacidad
        }, 3000); // Tiempo de visualización en milisegundos
    }
});

