const total_tecnico_activos = JSON.parse(document.getElementById('total_tecnico_activos').textContent)
const tecnico_meta = JSON.parse(document.getElementById('tecnico_meta').textContent)

const var_tecnico = document.getElementById('tecnico').getContext('2d');

//porcentajes tecnico
const backgroundColorsTecnico = tecnico_meta.map((meta, index) => {
    const resultado = total_tecnico_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorTecnico = tecnico_meta.map((meta, index) => {
    const resultado = total_tecnico_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


new Chart(var_tecnico, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_tecnico_activos,
            borderWidth: 1,
            backgroundColor:backgroundColorsTecnico,
            borderColor:borderColorTecnico
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
                text: 'Técnico', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


