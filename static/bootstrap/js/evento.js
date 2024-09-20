const total_evento_activos = JSON.parse(document.getElementById('total_evento_activos').textContent)
const evento_meta = JSON.parse(document.getElementById('evento_meta').textContent)


//porcentajes evento
const backgroundColorsEvento = evento_meta.map((meta, index) => {
    const resultado = total_evento_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorEvento = evento_meta.map((meta, index) => {
    const resultado = total_evento_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})



const evento = document.getElementById('evento').getContext('2d');



new Chart(evento, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_evento_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsEvento,
            borderColor: borderColorEvento
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false // Ocultar la leyenda
            },
            title: {
                display: true, // Mostrar el título
                text: 'Evento', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


