const  total_profundizacion_tecnica_activos = JSON.parse(document.getElementById('total_profundizacion_tecnica_activos').textContent)
const  profundizacion_tecnica_meta = JSON.parse(document.getElementById('profundizacion_tecnica_meta').textContent)

const profundizacion_tecnica = document.getElementById('profundizacion_tecnica').getContext('2d');



//porcentajes profundizacion_tecnica
const backgroundColorsProfundizacion_tecnica = profundizacion_tecnica_meta.map((meta, index) => {
    const resultado = total_profundizacion_tecnica_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorTecnologoProfundizacion_tecnica = profundizacion_tecnica_meta.map((meta, index) => {
    const resultado = total_profundizacion_tecnica_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})



new Chart(profundizacion_tecnica, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data:  total_profundizacion_tecnica_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsProfundizacion_tecnica,
            borderColor: borderColorTecnologoProfundizacion_tecnica
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
                text: 'Profundización Técnica', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


