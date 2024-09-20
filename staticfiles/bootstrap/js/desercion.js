function filtros_desercion() {
    const id_modalidad = document.getElementById('id_modalidad').value;
    const municipio = document.getElementById('id_municipio').value;
    const regional = document.getElementById('id_regional').value;
    const centro_de_formacion = document.getElementById('id_centro_de_formacion').value;
    const fecha_inicio_ficha = document.getElementById('filtroFechaInicio').value;
    const fecha_terminacion_ficha = document.getElementById('filtroFechaFin').value;



    if (fecha_inicio_ficha) {
        url_filtro += `fecha_inicio_ficha=${fecha_inicio_ficha}&`;
    }

    if (fecha_terminacion_ficha) {
        url_filtro += `fecha_terminacion_ficha=${fecha_terminacion_ficha}&`;
    } else {
        const today = new Date().toISOString().split('T')[0];
        url_filtro += `fecha_terminacion_ficha=${today}&`;
    }

    if (id_modalidad) {
        url_filtro += `id_modalidad=${id_modalidad}&`;
    }

    if (municipio) {
        url_filtro += `municipio=${municipio}&`;
    }

    if (regional) {
        url_filtro += `regional=${regional}&`;
    }

    if (centro_de_formacion) {
        url_filtro += `centro_de_formacion=${centro_de_formacion}&`;
    }

    window.location.href = url_filtro;
}

document.getElementById('filtroFechaInicio').addEventListener('change', filtros_desercion);
document.getElementById('filtroFechaFin').addEventListener('change', filtros_desercion);




