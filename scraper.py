import requests
import json
import time

print("Iniciando Motor V15 : Extracción directa desde el backend de PoGoCalendar (ScrapedDuck)...")

def extraer_raids_scrapedduck():
    jefes_encontrados = []
    # Nos conectamos directamente a PoGoCalendar
    url = "https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/raids.json"
    
    print(f"📡 Conectando a la base de datos central: {url} ...")
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            print("¡Muro superado! 🔓 Archivo JSON descargado sin bloqueos.")
            datos = resp.json()
            
            for raid in datos:
                nivel_bruto = str(raid.get('tier', ''))
                
                # Traducimos el nivel al formato de tu web
                nivel = None
                if '5' in nivel_bruto: nivel = '5'
                elif 'Mega' in nivel_bruto or 'mega' in nivel_bruto: nivel = 'Mega'
                elif '3' in nivel_bruto: nivel = '3'
                elif '1' in nivel_bruto: nivel = '1'
                
                if nivel:
                    nombre_bruto = raid.get('name', '')
                    
                    nombre_limpio = nombre_bruto.replace('Shadow', '').split('(')[0].strip()
                    
                    if len(nombre_limpio) > 2 and not any(j['nombre'] == nombre_limpio for j in jefes_encontrados):
                        jefes_encontrados.append({"nombre": nombre_limpio, "nivel": nivel})
                        print(f"👉 Detectado: {nombre_limpio} (Nivel {nivel})")
            
            return jefes_encontrados
        else:
            print(f" Error al conectar con el repositorio: {resp.status_code}")
    except Exception as e:
        print(" Falla de red al intentar descargar los datos.")
    
    return []

def adaptar_a_pokeapi(nombre):
    """Prepara el nombre para buscar sus estadísticas oficiales"""
    n = nombre.lower().replace(" ", "-").replace("'", "").replace(".", "")
    if n.startswith("mega-"): n = n.replace("mega-", "") + "-mega"
    if "alolan" in n: n = n.replace("alolan-", "") + "-alola"
    if "galarian" in n: n = n.replace("galarian-", "") + "-galar"
    for forma in ["-origin", "-therian", "-incarnate", "-altered", "-primal"]:
        if forma in n: n = n.replace(forma, "")
    return n.strip("-")

# Tu Lista Maestra de counters
top_counters = {
    "bug": ["Pheromosa (Picadura/Zumbido)", "Volcarona (Picadura/Zumbido)"],
    "dark": ["Tyranitar (Mordisco/Giro Vil)", "Hydreigon (Mordisco/Brutalillo)"],
    "ghost": ["Gengar (Lengüetazo/Bola Sombra)", "Chandelure (Infortunio/Bola Sombra)"],
    "dragon": ["Rayquaza (Cola Dragón/Enfado)", "Salamence (Cola Dragón/Cometa Draco)"],
    "electric": ["Zekrom (Rayo Carga/Voltio Cruel)", "Xurkitree (Impactrueno/Chispazo)"],
    "fighting": ["Lucario (Contraataque/Esfera Aural)", "Machamp (Contraataque/Puño Dinámico)"],
    "fire": ["Reshiram (Colmillo Ígneo/Llama Fusión)", "Darmanitan (Colmillo Ígneo/Sofoco)"],
    "grass": ["Kartana (Hoja Afilada/Hoja Aguda)", "Sceptile (Semilladora/Planta Feroz)"],
    "ground": ["Groudon (Disparo Lodo/Filo del Abismo)", "Garchomp (Disparo Lodo/Tierra Viva)"],
    "ice": ["Mamoswine (Nieve Polvo/Alud)", "Darmanitan Galar (Colmillo Hielo/Alud)"],
    "poison": ["Nihilego (Puya Nociva/Bomba Lodo)", "Roserade (Puya Nociva/Bomba Lodo)"],
    "psychic": ["Mewtwo (Confusión/Onda Mental)", "Alakazam (Confusión/Premonición)"],
    "rock": ["Rampardos (Antiaéreo/Avalancha)", "Rhyperior (Antiaéreo/Romperrocas)"],
    "steel": ["Metagross (Puño Bala/Puño Meteoro)", "Dialga (Garra Metal/Cabeza Hierro)"],
    "water": ["Kyogre (Cascada/Pulso Primigenio)", "Swampert (Pistola Agua/Hidrocañón)"],
    "flying": ["Rayquaza (Tajo Aéreo/Ascenso Draco)", "Moltres (Ataque Ala/Ataque Aéreo)"],
    "fairy": ["Togekiss (Encanto/Brillo Mágico)", "Gardevoir (Encanto/Brillo Mágico)"]
}

# --- FLUJO PRINCIPAL ---
lista_jefes = extraer_raids_scrapedduck()
jefes_procesados = []

if len(lista_jefes) > 0:
    print(f"\n¡Extracción exitosa! Cruzando datos de {len(lista_jefes)} jefes con PokeAPI...")
    for jefe in lista_jefes:
        nombre_real = jefe["nombre"]
        nivel = jefe["nivel"]
        nombre_api = adaptar_a_pokeapi(nombre_real)
        
        try:
            url_pokeapi = f"https://pokeapi.co/api/v2/pokemon/{nombre_api}"
            resp_poke = requests.get(url_pokeapi)
            
            if resp_poke.status_code == 200:
                datos = resp_poke.json()
                tipos = [t['type']['name'] for t in datos['types']]
                foto_url = datos['sprites']['other']['official-artwork']['front_default']
                
                debilidades = []
                counters_recomendados = []

                url_tipo = datos['types'][0]['type']['url']
                resp_tipo = requests.get(url_tipo).json()

                for debilidad in resp_tipo['damage_relations']['double_damage_from']:
                    tipo_debil = debilidad['name']
                    if tipo_debil not in debilidades:
                        debilidades.append(tipo_debil)
                    if tipo_debil in top_counters:
                        counters_recomendados.extend(top_counters[tipo_debil])

                counters_unicos = list(dict.fromkeys(counters_recomendados))[:4]

                jefes_procesados.append({
                    "nombre": nombre_real,
                    "nivel": nivel,
                    "foto": foto_url,
                    "tipos": tipos,
                    "debilidades": debilidades,
                    "counters": counters_unicos
                })
        except Exception as e:
            pass
        
        time.sleep(0.3)

    with open("datos.json", "w", encoding="utf-8") as archivo:
        json.dump(jefes_procesados, archivo, indent=4, ensure_ascii=False)
        
    print(f"\n¡Misión Completada! Sistema 100% automático basado en PoGoCalendar listo. Jefes guardados: {len(jefes_procesados)}")
else:
    print("\n La tubería de datos de ScrapedDuck falló o cambió de ubicación.")
