// Archivo: script.js

// Le decimos a la web que busque el archivo que generó tu bot de Python
fetch('datos.json')
    .then(respuesta => respuesta.json())
    .then(datos => {
        //Cambiamos el texto "Cargando radar..." por el nombre del jefe
        document.getElementById('nombre-pokemon').innerText = datos.jefe_actual;

        // Creamos las etiquetas visuales para los tipos del Pokémon
        const contenedorTipos = document.getElementById('tipos-pokemon');
        datos.tipos.forEach(tipo => {
            const spanTipo = document.createElement('span');
            spanTipo.className = 'tipo';
            spanTipo.innerText = tipo;
            contenedorTipos.appendChild(spanTipo);
        });
    })
    .catch(error => {
        document.getElementById('nombre-pokemon').innerText = "Error al cargar datos ❌";
        console.error("Hubo un problema:", error);
    });