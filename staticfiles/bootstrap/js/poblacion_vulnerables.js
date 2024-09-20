
//GRAFICA POBLACION
//datos poblacion vulnerabls

const datos_grafica = JSON.parse(document.getElementById('datos_grafica').textContent)
const meta_grafica = JSON.parse(document.getElementById('meta_grafica').textContent)


//GRAFICA  TIPO POBLACION
//datos poblacion vulnerabls
const data_tipo_poblaciones = JSON.parse(document.getElementById('data_tipo_poblaciones').textContent)
const meta_tipo_poblaciones = JSON.parse(document.getElementById('meta_tipo_poblaciones').textContent)












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
    const porcentaje = (value / max) * 100;
    if(porcentaje >= 43.7 && porcentaje <= 96){
        return 'rgba(50, 200, 192, 0.2)';
    } else if(porcentaje >= 29.2 && porcentaje < 43.6) {
        return 'rgba(255, 230, 86, 0.2)';
    } else if(porcentaje >= 0 && porcentaje < 29.1){
        return 'rgba(255, 99, 132, 0.2)';
    }else if(porcentaje > 100){
        return 'rgba(255, 87, 34, 0.2)';
    }
    return 'rgba(75, 192, 192, 0.2)'
    
}


//porcentajes metas poblacion
const backgroundColorsPoblacion = meta_grafica.map((meta, index) => {
    const resultado = datos_grafica[index];
    return Estado_de_color(resultado, meta)
})
const borderColorPoblacion = meta_grafica.map((meta, index) => {
    const resultado = datos_grafica[index];
    return Estado_de_color(resultado, meta).replace('0.2','1.0')
})


//porcentaje metas tipo poblacion
const backgroundColorsTipoPoblacion = meta_tipo_poblaciones.map((meta_tipo_poblacion, index) => {
    const resultado = data_tipo_poblaciones[index];
    return Estado_de_color(resultado, meta_tipo_poblacion)
})
const borderColorTipoPoblacion = meta_tipo_poblaciones.map((meta_tipo_poblacion, index) => {
    const resultado = data_tipo_poblaciones[index];
    return Estado_de_color(resultado, meta_tipo_poblacion).replace('0.2','1.0')
})


const poblaciones = document.getElementById('poblaciones').getContext('2d');

new Chart(poblaciones, {
    type: 'bar',
    data: { 
        labels: ['Cupos Desplazados por la violencia','Cupos Hechos Victimizantes','Cupos Victimas (*)','Cupos Otras Poblaciones Vulnerables','Cupos Total Poblaciones Vulnerables','Aprendices Desplazados por la violencia','Aprendices Hechos Victimizantes','Aprendices Victimas (*)','Aprendices Otras Poblaciones Vulnerables','Aprendices Total Poblaciones Vulnerables'],
        datasets: [{
            label: '# de Aprendices',
            data: datos_grafica,
            borderWidth: 1,
            backgroundColor: backgroundColorsPoblacion,
            borderColor:borderColorPoblacion ,
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
            
          
        },
        plugins: {
            legend: {
                display: false // Ocultar la leyenda
            },
            title: {
                display: true, // Mostrar el título
                text: 'Poblacion', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            },
            
        }
    }
});





//COMPLEMENTARIA
const tipo_poblacion = document.getElementById('tipo_poblacion').getContext('2d');

new Chart(tipo_poblacion, {
    width: 100,
    type: 'bar',
    data:  {
    
        labels: ['Cupos Indígenas', 'Cupos INPEC','Cupos Jóvenes Vulnerables','Cupos Adolescente en Conflicto con la Ley Penal','Cupos Mujer Cabeza de Hogar','Cupos Persona con Discapacidad','Cupos Negritudes (Negros)','Cupos Afrocolombianos','Cupos Raizales','Cupos Palenqueros','Cupos NARP','Cupos Proceso de Reintegración y Adolescentes desvinculados...','Cupos Tercera Edad','Cupos Adolescente Trabajador','Cupos Rroom','Aprendices Indígenas', 'Aprendices INPEC','Aprendices Jóvenes Vulnerables','Aprendices Adolescente en Conflicto con la Ley Penal','Aprendices Mujer Cabeza de Hogar','Aprendices Persona con Discapacidad','Aprendices Negritudes (Negros)','Aprendices Afrocolombianos','Aprendices Raizales','Aprendices Palenqueros','Aprendices NARP','Aprendices Proceso de Reintegración y Adolescentes desvinculados...','Aprendices Tercera Edad','Aprendices Adolescente Trabajador','Aprendices Rroom'],
     
        datasets: [{
            label: '# of Votes',
            data: data_tipo_poblaciones,
            borderWidth: 1,
            backgroundColor: backgroundColorsTipoPoblacion,
            borderColor: borderColorTipoPoblacion,
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
                text: 'Tipo de poblaciones', // Título de la gráfica
                font: {
                    size: 14 // Tamaño de la fuente del título
                }
            }
        }
    },
  
});