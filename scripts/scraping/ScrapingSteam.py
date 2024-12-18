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
            "Categoría": categoria,
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
