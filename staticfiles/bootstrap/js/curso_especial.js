const total_curso_especial_activos = JSON.parse(document.getElementById('total_curso_especial_activos').textContent)
const curso_especial_meta = JSON.parse(document.getElementById('curso_especial_meta').textContent)
console.log(curso_especial_meta)
console.log(total_curso_especial_activos)


//porcentajescurso especial
const backgroundColorsEventoCurso= curso_especial_meta.map((meta, index) => {
    const resultado = total_curso_especial_activos[index];
    return Estado_de_color(resultado, meta)
})
const borderColorEventoCurso = curso_especial_meta.map((meta, index) => {
    const resultado = total_curso_especial_activos[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


const curso_especial = document.getElementById('curso_especial').getContext('2d');

new Chart(curso_especial, {
    type: 'bar',
    data: {
        labels: ['Presencial', 'Virtual'],
        datasets: [{
            data: total_curso_especial_activos,
            borderWidth: 1,
            backgroundColor: backgroundColorsEventoCurso,
            borderColor: borderColorEventoCurso
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
                text: 'Curso especial', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    }
});


