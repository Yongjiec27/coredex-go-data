
// Diccionario de colores oficiales por tipo
const typeColors = {
    normal: '#A8A77A', fire: '#EE8130', water: '#6390F0', electric: '#F7D02C',
    grass: '#7AC74C', ice: '#96D9D6', fighting: '#C22E28', poison: '#A33EA1',
    ground: '#E2BF65', flying: '#A98FF3', psychic: '#F95587', bug: '#A6B91A',
    rock: '#B6A136', ghost: '#735797', dragon: '#6F35FC', dark: '#705746',
    steel: '#B7B7CE', fairy: '#D685AD'
};

let jefesData = [];

fetch('datos.json')
    .then(response => response.json())
    .then(data => {
        jefesData = data;
        const select = document.getElementById('poke-select');
        
        data.forEach((jefe, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${jefe.nombre} (Nivel ${jefe.nivel})`;
            select.appendChild(option);
        });
    })
    .catch(error => console.error('Error cargando los datos:', error));

// Escuchar cambios en el menú
document.getElementById('poke-select').addEventListener('change', function() {
    const card = document.getElementById('poke-card');
    
    if (this.value === "") {
        card.style.display = 'none'; 
        return;
    }

    const jefe = jefesData[this.value];
    
    // Actualizar textos e imagen
    document.getElementById('poke-name').textContent = jefe.nombre;
    document.getElementById('poke-tier').textContent = `Incursión ${jefe.nivel}`;
    document.getElementById('poke-image').src = jefe.foto;

    // Limpiar y llenar Tipos
    const typesContainer = document.getElementById('poke-types');
    typesContainer.innerHTML = '';
    jefe.tipos.forEach(tipo => {
        const span = document.createElement('span');
        span.className = 'type-badge';
        span.style.backgroundColor = typeColors[tipo] || '#777';
        span.textContent = tipo;
        typesContainer.appendChild(span);
    });

    // Limpiar y llenar Debilidades
    const weakContainer = document.getElementById('poke-weaknesses');
    weakContainer.innerHTML = '';
    jefe.debilidades.forEach(deb => {
        const span = document.createElement('span');
        span.className = 'type-badge';
        span.style.backgroundColor = typeColors[deb] || '#777';
        span.textContent = deb;
        weakContainer.appendChild(span);
    });

    // Limpiar y llenar Counters
    const countersList = document.getElementById('poke-counters');
    countersList.innerHTML = '';
    jefe.counters.forEach(counter => {
        const li = document.createElement('li');
        li.textContent = counter;
        countersList.appendChild(li);
    });

    card.style.display = 'block';
});

//Calendario de eventos
// Base de datos de eventos
const eventosMarzo = [
    { tipo: "Evento Global", nombre: "Pokémon 30th Anniversary - All Out", fechas: "7 Mar - 9 Mar", color: "#e84393" },
    { tipo: "Community Day", nombre: "Scorbunny", fechas: "14 Mar", color: "#e17055" },
    { tipo: "Evento Global", nombre: "Bug Out (Debut Blipbug)", fechas: "17 Mar - 23 Mar", color: "#A6B91A" },
    { tipo: "Incursión Nivel 5", nombre: "Articuno, Zapdos, Moltres", fechas: "4 Mar - 10 Mar", color: "#0984e3" },
    { tipo: "Incursión Nivel 5", nombre: "Zacian (Héroe)", fechas: "11 Mar - 17 Mar", color: "#0984e3" },
    { tipo: "Incursión Nivel 5", nombre: "Zamazenta (Héroe)", fechas: "18 Mar - 24 Mar", color: "#0984e3" },
    { tipo: "Incursión Nivel 5", nombre: "Regieleki", fechas: "25 Mar - 31 Mar", color: "#0984e3" },
    { tipo: "Mega Incursión", nombre: "Mega Pinsir", fechas: "4 Mar - 10 Mar", color: "#fdcb6e" },
    { tipo: "Mega Incursión", nombre: "Mega Steelix", fechas: "11 Mar - 17 Mar", color: "#fdcb6e" },
    { tipo: "Mega Incursión", nombre: "Mega Slowbro", fechas: "18 Mar - 24 Mar", color: "#fdcb6e" },
    { tipo: "Mega Incursión", nombre: "Mega Houndoom", fechas: "25 Mar - 31 Mar", color: "#fdcb6e" },
    { tipo: "Combate Max", nombre: "Pikachu Gigamax", fechas: "9 Mar - 15 Mar", color: "#d63031" },
    { tipo: "Combate Max", nombre: "Regice Dynamax", fechas: "23 Mar - 29 Mar", color: "#d63031" }
];

function renderizarCalendario() {
    const grid = document.getElementById('events-grid');
    grid.innerHTML = ''; 

    eventosMarzo.forEach(evento => {
        const card = document.createElement('div');
        card.className = 'event-card';
        card.style.borderLeftColor = evento.color; 

        card.innerHTML = `
            <div>
                <div class="event-type" style="color: ${evento.color}">${evento.tipo}</div>
                <h3 class="event-name">${evento.nombre}</h3>
            </div>
            <div class="event-dates">
                🗓️ ${evento.fechas}
            </div>
        `;
        
        grid.appendChild(card);
    });
}

// Dibujamos el calendario al abrir la página
renderizarCalendario();
