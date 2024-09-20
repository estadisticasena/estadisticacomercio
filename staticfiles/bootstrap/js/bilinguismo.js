const total_bilinguismo_activos = JSON.parse(document.getElementById('total_bilinguismo_activos').textContent)
const bilinguismo_meta = JSON.parse(document.getElementById('bilinguismo_meta').textContent)

const bilinguismo = document.getElementById('bilinguismo').getContext('2d');


//porcentajes bilinguismo
const backgroundColorsBilinguismo = bilinguismo_meta.map((meta, index) => {
    const resultado = total_bilinguismo_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorBilinguismo = bilinguismo_meta.map((meta, index) => {
    const resultado = total_bilinguismo_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


new Chart(bilinguismo, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_bilinguismo_activos,
            borderWidth: 1,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
             'rgba(75, 192, 192, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ]
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
                text: 'Bilingüismo', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});

