const total_operario_activos = JSON.parse(document.getElementById('total_operario_activos').textContent)
const operario_meta = JSON.parse(document.getElementById('operario_meta').textContent)

//porcentajes operario
const backgroundColorsOperario = operario_meta.map((meta, index) => {
    const resultado = total_operario_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorOperario = operario_meta.map((meta, index) => {
    const resultado = total_operario_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


const operario = document.getElementById('operario').getContext('2d');

new Chart(operario, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_operario_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsOperario,
            borderColor: borderColorOperario
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
                text: 'Operario', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


