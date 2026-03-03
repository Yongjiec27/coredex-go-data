import requests
import json # ¡Nueva herramienta para crear archivos de datos!

pokemon = "mewtwo"
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"

print(f"Conectando a la base de datos para buscar a {pokemon}...")
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    
    nombre = datos['name'].capitalize()
    tipos = [tipo['type']['name'] for tipo in datos['types']]
    
    # 1. Preparamos el "paquete" de datos que queremos guardar
    datos_para_guardar = {
        "jefe_actual": nombre,
        "tipos": tipos
    }
    
    # 2. Creamos y guardamos la información en un archivo llamado 'datos.json'
    with open("datos.json", "w") as archivo:
        json.dump(datos_para_guardar, archivo, indent=4)
        
    print("\n¡Extracción y guardado exitoso! 🚀")
    print(f"Revisa tu menú de la izquierda, ¡se acaba de crear un archivo con los datos de {nombre}!")
else:
    print("\n Error al conectar con la base de datos.")