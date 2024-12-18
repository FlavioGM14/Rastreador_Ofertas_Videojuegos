# Rastreador_Ofertas_Videojuegos

## Introducción:

En este proyecto se desarrolló una solución para recopilar y centralizar información sobre ofertas de videojuegos en tres plataformas principales: **Steam**, **GOG** y **Epic Games**. Los usuarios pueden elegir la categoría para obtener datos como precios actuales, descuentos, y las plataformas donde están disponibles. El sistema facilita el acceso a ofertas de videojuegos, ayudando a los usuarios a tomar decisiones de compra informadas. 

## Motivación:

La motivación detrás de este proyecto se centra en resolver un problema común para los jugadores y consumidores de videojuegos: la búsqueda de las mejores ofertas en juegos deseados. Los precios de los videojuegos pueden variar significativamente entre plataformas, y muchas veces las promociones son temporales y dispersas, lo que dificulta a los usuarios identificar rápidamente la mejor opción de compra.

## Objetivo general:
Desarrollar un sistema que permita buscar y/o comparar precios de videojuegos en múltiples plataformas en línea, proporcionando información actualizada sobre descuentos y promociones disponibles.

### Objetivos específicos:

1. Desarrollar un sistema de recopilación de datos automatizado:
    - Utilizar web scraping para obtener información actualizada sobre precios y descuentos de videojuegos en las plataformas seleccionadas.
    - Implementar técnicas de scraping con `BeautifulSoup`, `requests`, `playwright` en Python para extraer datos como el nombre del juego, precio, descuento.

2. Integrar y estructurar los datos extraídos:

    - Organizar los datos obtenidos en un DataFrame en `pandas` para su fácil análisis y comparación.

3. Desarrollar un sistema de filtrado de juegos:

    - Permitir que el usuario seleccione la categoría y obtener una lista de juegos disponibles en diferentes plataformas.

4. Construir una interfaz de usuario:

    - Crear una interfaz sencilla que permita al usuario seleccionar la categoría y ver los resultados en un formato fácil de leer. Implementando un servidor web con `Flask` para visualizar las ofertas de manera interactiva a través de un diseño en `HTML`

5. Mostrar resultados de manera clara y visual:
    - Presentar los resultados extraídos en una tabla ordenada con nombre del juego, descuento, precio original, precio con descuento y plataforma.

## Desarrollo del proyecto

### 1. Web Scraping

Se realizaron tres scripts de web scraping independientes, uno para cada plataforma:

**Steam**
- **Librerías utilizadas:** `pandas`, `requests`, `BeautifulSoup`.
- **Datos extraídos:** Título del videojuego, precio original, precio con descuento, porcentaje de descuento.
- **URL base utilizada:** `https://store.steampowered.com/search/?specials=1&ndl=1`.

**GOG**
- **Librerías utilizadas:** `pandas`, `requests`, `BeautifulSoup`.
- **Datos extraídos:** Título del videojuego, precio original, precio con descuento, porcentaje de descuento.
- **URL base utilizada:** `https://www.gog.com/en/games?order=desc:discount`.

**Epic Games**
- **Librerías utilizadas:** `playwright`, `requests`.
- **Datos extraídos:** Título del videojuego, precio original, precio con descuento, porcentaje de descuento.
- **URL base utilizada:** `https://store.epicgames.com/es-ES/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&category=Game&count=40&start=0`

#### Código Base de Web Scraping

Ejemplo con Steam de extracción de datos:

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def obtener_ofertas_steam(categoria, orden=1, limite=5):
    # Diccionario de opciones de ordenamiento
    opciones_orden = {
        1: "Price_ASC",     # Precio más bajo
        2: "Price_DESC",    # Precio más alto
        3: "Reviews_DESC"   # Mejores reseñas
    }
    
    # Establecer el orden por defecto a "Precio más bajo" (opción 1)
    if orden not in opciones_orden:
        print(f"Orden no válido. Opciones disponibles: {list(opciones_orden.keys())}")
        return pd.DataFrame()

    # Construir la URL
    url = f"https://store.steampowered.com/search/?sort_by={opciones_orden[orden]}&term={categoria}&supportedlang=spanish%2Cenglish&specials=1&ndl=1"

    # Solicitud HTTP
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al acceder a Steam")
        return pd.DataFrame()

    # Parsear HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    juegos = []

    for i, juego in enumerate(soup.find_all('a', class_='search_result_row'), start=1):
        if i > limite:  # Limitar a los primeros 'limite' juegos
            break

        # Extraer título
        nombre = juego.find('span', class_='title').text.strip()

        # Extraer precios y descuentos
        descuento = juego.find('div', class_='discount_pct')
        precio_original = juego.find('div', class_='discount_original_price')
        precio_final = juego.find('div', class_='discount_final_price')

        # Formatear los precios
        precio_original_sin_simbolo = (
            precio_original.text.strip().lstrip("S/.").lstrip("$").strip() + " PEN"
            if precio_original else "No disponible"
        )
        precio_final_sin_simbolo = (
            precio_final.text.strip().lstrip("S/.").lstrip("$").strip() + " PEN"
            if precio_final else "Gratis"
        )

        # Formatear el descuento (agregando el espacio antes de "%")
        descuento_formateado = (
            descuento.text.strip().replace("%", " %") if descuento else "0 %"
        )

        juegos.append({
            "Nombre del Juego": nombre,
            "Descuento (%)": descuento_formateado,
            "Precio Original (S/.)": precio_original_sin_simbolo,
            "Precio con Descuento (S/.)": precio_final_sin_simbolo,
            "Plataforma": "Steam"
        })

    # Convertir a DataFrame
    return pd.DataFrame(juegos)

# Función para ser llamada con el input de la categoría
def obtener_datos_steam(categoria):
    return obtener_ofertas_steam(categoria)

if __name__ == "__main__":
    categoria = input("Ingrese la categoría de juegos: ").lower()
    df_steam = obtener_datos_steam(categoria)

    if not df_steam.empty:
        print(df_steam)
    else:
        print("No se pudieron obtener datos.")
```
Los scripts de scraping completos para GOG y Epic Games están disponibles en el repositorio del proyecto: [Enlace a la carpeta scraping en el repositorio](https://github.com/FlavioGM14/Rastreador_Ofertas_Videojuegos/blob/main/scripts/scraping).

### 2. Unificación de datos

El proceso de unificación consiste en combinar los datos obtenidos de las tres plataformas en un único DataFrame para facilitar su análisis y posterior uso. Este paso permite centralizar la información y garantizar que las ofertas de todas las plataformas estén disponibles en un mismo formato.

Para esto, se desarrolló una función que:
- Invoca los scripts de scraping para cada plataforma (Steam, GOG y Epic Games).
- Limita los resultados a los primeros 5 juegos por plataforma para mantener la información manejable.
- Verifica si alguno de los resultados está vacío.
- Combina los datos de todas las plataformas en un único DataFrame.

#### Código de unión de datos

```python
import pandas as pd
from ScrapingEpicGames import obtener_datos_epic
from ScrapingSteam import obtener_datos_steam
from ScrapingGOG import scrape_gog

def unificar_scraping(categoria_usuario):
    # Obtener los datos de Epic Games (limitando a 5 juegos)
    df_epic = obtener_datos_epic(categoria_usuario)
    print("\nDatos de Epic Games:")
    print(df_epic.head(5))  # Limitar a los 5 primeros juegos
    df_epic['Plataforma'] = 'Epic Games'  # Asegurarnos de que la columna 'Plataforma' esté definida

    # Obtener los datos de Steam (limitando a 5 juegos)
    df_steam = obtener_datos_steam(categoria_usuario)
    print("\nDatos de Steam:")
    print(df_steam.head(5))  # Limitar a los 5 primeros juegos
    df_steam['Plataforma'] = 'Steam'  # Asegurarnos de que la columna 'Plataforma' esté definida

    # Obtener los datos de GOG (limitando a 5 juegos)
    df_gog = scrape_gog(categoria_usuario)
    print("\nDatos de GOG:")
    print(df_gog.head(5))  # Limitar a los 5 primeros juegos
    df_gog['Plataforma'] = 'GOG'  # Asegurarnos de que la columna 'Plataforma' esté definida

    # Verificar si alguno de los DataFrames está vacío
    if df_epic.empty and df_steam.empty and df_gog.empty:
        print("No se han encontrado datos en ninguna plataforma.")
        return pd.DataFrame()

    # Unificar los tres DataFrames (solo los primeros 5 de cada uno)
    df_unificado = pd.concat([df_epic.head(5), df_steam.head(5), df_gog.head(5)], ignore_index=True)
    return df_unificado

# Ejemplo de uso
if __name__ == "__main__":
    # Solo pedimos la categoría una vez
    categoria_usuario = input("Ingresa la categoría de juegos (ejemplo: accion, rpg, etc.): ").lower()

    # Unificamos los datos y mostramos el resultado
    df_unificado = unificar_scraping(categoria_usuario)

    if not df_unificado.empty:
        print("\nDatos unificados (máximo 15 juegos):")
        print(df_unificado)
    else:
        print("No se encontraron juegos para la categoría ingresada.")
```

### 3. Creación del Servidor con Flask
Se desarrolló un servidor web básico utilizando Flask para mostrar las ofertas. 

Para esto se debe instalar la librería  `Flask`.

#### Código Base del Servidor Flask:

```python
from flask import Flask, render_template, request, jsonify
import pandas as pd
from UnificacionOfertas import unificar_scraping  # Asegúrate de que esta función exista y funcione correctamente

app = Flask(__name__)

# Lista de categorías disponibles
categorias_disponibles = [
    "aventura", "rpg", "acción", "estrategia", "simulación",
    "deportes", "indie", "carreras", "disparos"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    categoria = request.args.get('categoria', '').lower()

    # Verificar si la categoría es válida
    if categoria not in categorias_disponibles:
        return jsonify({
            "error": "Categoría no válida. Las categorías disponibles son: " + ", ".join(categorias_disponibles)
        }), 400

    # Llamar a la función de unificación para obtener los datos
    df_unificado = unificar_scraping(categoria)

    # Si no se encontraron resultados
    if df_unificado.empty:
        return render_template('no_results.html')

    # Convertir el DataFrame a HTML
    df_html = df_unificado.to_html(classes='table table-bordered table-striped table-hover', index=False)

    return render_template('search_results.html', categoria=categoria, df_html=df_html)

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. Diseño HTML
Se diseñó una página HTML para mejorar la presentación de las ofertas.

#### Ejemplo del Archivo HTML (`templates/index.html`):
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rastreador de Ofertas de Videojuegos</title>
    <link rel="icon" href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQM2YkZokMKX2Jk6lYlqpR81dH17_ctQHwaFA&s" type="image/x-icon">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html, body {
            height: 100%; /* Asegura que ocupen todo el alto */
        }
        body {
            font-family: 'Poppins', sans-serif;
            color: #f4f4f9;
            text-align: center;
            display: flex;
            flex-direction: column;
	        background-image: url('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/788ecb45-01a2-4da0-b919-618d045b3c48/dddb92-e4e8b560-016f-4091-ae3d-c12046b11f8a.jpg/v1/fit/w_682,h_372,q_70,strp/pacman_pattern_by_xnightholw243_dddb92-375w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MzcyIiwicGF0aCI6IlwvZlwvNzg4ZWNiNDUtMDFhMi00ZGEwLWI5MTktNjE4ZDA0NWIzYzQ4XC9kZGRiOTItZTRlOGI1NjAtMDE2Zi00MDkxLWFlM2QtYzEyMDQ2YjExZjhhLmpwZyIsIndpZHRoIjoiPD02ODIifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.alDXHdioNR7EchMR1KqHF8IcTEYIpX5ohZ66rtKhUD4');
            background-size: contain;
            background-position: center;
            background-attachment: fixed;
        }
        main {
            flex: 1; /* Hace que el contenido principal ocupe el espacio sobrante */
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }
        h1 {
            color: white;
            opacity: 0;
            transform: translateY(-20px);
            animation: fadeIn 1s ease-in-out forwards;
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .container {
            background-color: black;
            color: #f4f4f9;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            margin-top: 50px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0;
            transform: translateY(-20px);
            animation: fadeInContainer 1s ease-in-out forwards 0.5s;
        }
        @keyframes fadeInContainer {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        select, button {
            padding: 10px;
            font-size: 16px;
            margin: 10px 0;
            width: 100%;
            border-radius: 5px;
            border: none;
            background-color: white;
            color: black;
            transition: background-color 0.3s ease, transform 0.2s ease;
            opacity: 0;
            transform: translateY(10px);
            animation: fadeInButton 1s ease-in-out forwards 1s;
        }
        @keyframes fadeInButton {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        select, button {
            padding: 10px;
            font-size: 16px;
            margin: 10px 0;
            width: 100%;
            border-radius: 5px;
            border: none;
            background-color: white;
            color: black;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        button:hover {
            background-color: #1565c0;
            transform: scale(1.05);
        }
        @media (max-width: 768px) {
            .container {
                margin: 20px;
                padding: 15px;
            }
            select, button {
                font-size: 14px;
            }
        }
        footer {
            background-color: #111;
            color: #f4f4f9;
            text-align: center;
            padding: 10px 0;
            font-size: 12px;
            margin-top: auto; /* Lo envía al final */
        }

        footer a {
            color: #f4f4f9;
            text-decoration: none;
        }
        
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenido al Rastreador de Ofertas de Videojuegos</h1>
        <form action="/search" method="get">
            <select id="categoria" name="categoria" required>
                <option value="" disabled selected>Selecciona una categoría</option>
                <option value="aventura">Aventura</option>
                <option value="rpg">RPG</option>
                <option value="acción">Acción</option>
                <option value="estrategia">Estrategia</option>
                <option value="simulación">Simulación</option>
                <option value="deportes">Deportes</option>
                <option value="indie">Indie</option>
                <option value="carreras">Carreras</option>
                <option value="disparos">Disparos</option>
            </select>
            <button type="submit">Buscar Juegos</button>
        </form>
    </div>
    
    <footer style="background-color: #333; color: #fff; text-align: center; padding: 10px 0; font-size: 14px;">
        <div>
            <p>Contacto:
                <a href="20230418@lamolina.edu.pe" style="color: #fff; text-decoration: none;">20230418@lamolina.edu.pe</a> |
                <a href="20230396@lamolina.edu.pe" style="color: #fff; text-decoration: none;">20230418@lamolina.edu.pe</a>
            </p>
        </div>
        <div
            <p>&copy; 2024 Rastreador de Ofertas de Videojuegos. Todos los derechos reservados.</p>
        </div>
    </footer>    
</body>
</html>
```

El archivo HTML de la página de resultados y no se encuentra disponible se encuentran en el repositorio del proyecto: [Enlace a la carpeta templates en el repositorio](https://github.com/FlavioGM14/Rastreador_Ofertas_Videojuegos/tree/main/scripts/scraping/templates)

## Resultados y Conclusiones

- **Automatización Exitosa:** Se logró automatizar la extracción de datos de las tres plataformas seleccionadas.
- **Unificación:** Los datos de ofertas se centralizaron en un DataFrame, facilitando su análisis.
- **Servidor Interactivo:** El servidor Flask permitió visualizar las ofertas en una interfaz amigable y dinámica.
- **Aprendizaje Adicional:** El proyecto permitió profundizar en técnicas de web scraping, manejo de datos con pandas y desarrollo de aplicaciones web con Flask.

## Repositorio
El código fuente y los datos están disponibles en el siguiente enlace: [GitHub](https://github.com/FlavioGM14/Rastreador_Ofertas_Videojuegos).
