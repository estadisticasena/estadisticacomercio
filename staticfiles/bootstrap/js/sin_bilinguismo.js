const total_sin_bilinguismo_activos = JSON.parse(document.getElementById('total_sin_bilinguismo_activos').textContent)
const sin_bilinguismo_meta = JSON.parse(document.getElementById('sin_bilinguismo_meta').textContent)

const sin_bilinguismo = document.getElementById('sin_bilinguismo').getContext('2d');

//porcentajes bilinguismo
const backgroundColorsSinBilinguismo = sin_bilinguismo_meta.map((meta, index) => {
    const resultado = total_sin_bilinguismo_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorSinBilinguismo = sin_bilinguismo_meta.map((meta, index) => {
    const resultado = total_sin_bilinguismo_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


new Chart(sin_bilinguismo, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_sin_bilinguismo_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsSinBilinguismo,
            borderColor: borderColorSinBilinguismo
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
                text: 'Sin Bilingüismo', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});




