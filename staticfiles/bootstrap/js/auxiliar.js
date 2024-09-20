
const total_auxiliar_activos = JSON.parse(document.getElementById('total_auxiliar_activos').textContent)

const auxiliar_meta= JSON.parse(document.getElementById('auxiliar_meta').textContent)

const auxiliar = document.getElementById('auxiliar').getContext('2d');


//porcentajes auxiliar
const backgroundColors = auxiliar_meta.map((meta, index) => {
    const resultado = total_auxiliar_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColor = auxiliar_meta.map((meta, index) => {
    const resultado = total_auxiliar_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})



new Chart(auxiliar, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_auxiliar_activos,
            borderWidth: 1,
            backgroundColor: backgroundColors,
            borderColor: borderColor,
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
                text: 'Auxiliar', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


