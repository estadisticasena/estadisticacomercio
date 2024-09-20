
//GRAFICA TITULADA
//datos del p04
const data = JSON.parse(document.getElementById('data').textContent)

const labels_virtuales = JSON.parse(document.getElementById('labels_virtuales').textContent)
const labels_presenciales = JSON.parse(document.getElementById('labels_presenciales').textContent)
// datos de las metas establecidas
const metas_valores = JSON.parse(document.getElementById('metas_valores').textContent)


//GRAFICA COMPLEMENTARIA 
const metas_complementaria = JSON.parse(document.getElementById('metas_complementaria').textContent)
const aprendices_activos_complementaria = JSON.parse(document.getElementById('aprendices_activos_complementaria').textContent)

//METAS






function showChart(chartId,tableId) {
    localStorage.setItem('chartIdGraficas', chartId)
    localStorage.setItem('tableIdGraficas', tableId)
    // Oculta todos los gráficos
    document.querySelectorAll('.chart').forEach(chart => {
        chart.style.display = 'none';
    });
    // Muestra el gráfico seleccionado
    document.getElementById(chartId).style.display = 'block';
    // Oculta todos las tablas
    document.querySelectorAll('.data-table').forEach(table => {
        table.style.display = 'none';
    });
    document.getElementById(tableId).style.display = 'block';

    

}

document.addEventListener('DOMContentLoaded', function(){
    const saveCharId  = localStorage.getItem('chartIdGraficas') 
    const saveTableId  = localStorage.getItem('tableIdGraficas') 

    showChart(saveCharId,saveTableId)
})


function Estado_de_color(value, max){
    const porcentaje = value / max;
    if(porcentaje <0.29) return 'rgba(255, 99, 132, 0.2)';
    if(porcentaje <0.49) return 'rgba(255, 159, 64, 0.2)';
    if(porcentaje <0.59) return 'rgba(255, 206, 86, 0.2)';
    return 'rgba(75, 192, 192, 0.2)';
}

//porcentajes metas titulada
const backgroundColors = metas_valores.map((meta, index) => {
    const resultado = data[index];
    return Estado_de_color(resultado, meta)
})
const borderColor = metas_valores.map((meta, index) => {
    const resultado = data[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})

//porcentaje metas complementaria
const backgroundColorsC = metas_complementaria.map((metas_complementaria, index) => {
    const resultado = aprendices_activos_complementaria[index];
    return Estado_de_color(resultado, metas_complementaria)
})
const borderColorC = metas_complementaria.map((metas_complementaria, index) => {
    const resultado = aprendices_activos_complementaria[index];
    return Estado_de_color(resultado, metas_complementaria).replace('0.2','1.0')
})



const ctx_titulada = document.getElementById('barchart_titulada').getContext('2d');

new Chart(ctx_titulada, {
    type: 'bar',
    data: { 
        labels: [labels_presenciales[0],labels_presenciales[1],labels_presenciales[2],labels_presenciales[3],labels_presenciales[4],labels_presenciales[5],labels_virtuales[0],labels_virtuales[1],labels_virtuales[2],labels_virtuales[3],labels_virtuales[4],labels_virtuales[5],labels_virtuales[6]],
        datasets: [{
            label: '# de Aprendices',
            data: data,
            borderWidth: 1,
            backgroundColor: backgroundColors,
            borderColor:borderColor ,
        }
    ],
    },
    options: {
        scales: {
            x: {
                stacked: false,
                grid: {
                    display : false
                },
                sticks: {
                    autoSkip: false,
                    maxRotation: 90

                }

            },
            y: {
                beginAtZero: true,
                min:0,
                ticks: {
                    stepSize: 20,
                    callback: function(value){
                       
                        return value 
                    }
                }
            
            },
          
        },
        plugins: {
            legend: {
                display: false // Ocultar la leyenda
            },
            title: {
                display: true, // Mostrar el título
                text: 'Titulada', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            },
            
        }
    }
});





//COMPLEMENTARIA
const ctx_complementaria = document.getElementById('barchart_complementaria').getContext('2d');

new Chart(ctx_complementaria, {
    width: 100,
    type: 'bar',
    data:  {
    
        labels: ['Bilingüismo Presencial', 'Bilingüismo Virtual', 'Sin Bilingüismo Presencial', 'Sin Bilingüismo Virtual'],
     
        datasets: [{
            label: '# of Votes',
            data: [aprendices_activos_complementaria[0],aprendices_activos_complementaria[1],aprendices_activos_complementaria[2],aprendices_activos_complementaria[3]],
            borderWidth: 1,
            backgroundColor: backgroundColorsC,
            borderColor:borderColorC ,
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
                text: 'Complementaria', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    },
  
});