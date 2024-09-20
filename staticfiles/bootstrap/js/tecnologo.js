const total_tecnologo_activos = JSON.parse(document.getElementById('total_tecnologo_activos').textContent)
const tecnologo_meta = JSON.parse(document.getElementById('tecnologo_meta').textContent)

const tecnologo = document.getElementById('tecnologo').getContext('2d');

//porcentajes tecnologo
const backgroundColorsTecnologo = tecnologo_meta.map((meta, index) => {
    const resultado = total_tecnologo_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorTecnologo = tecnologo_meta.map((meta, index) => {
    const resultado = total_tecnologo_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})

new Chart(tecnologo, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_tecnologo_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsTecnologo,
            borderColor:borderColorTecnologo
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
                text: 'Tecnólogo', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});



