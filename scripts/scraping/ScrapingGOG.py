import requests
from bs4 import BeautifulSoup
import pandas as pd

# Diccionario para traducir categorías del español al inglés
categorias_traducidas = {
    "aventura": "adventure",
    "rpg": "rpg",
    "acción": "action",
    "estrategia": "strategy",
    "simulación": "simulation",
    "deportes": "sports",
    "indie": "indie",
    "carreras": "racing",
    "disparos": "shooter"
}

# Tasa de cambio de dólares a soles
TASA_CAMBIO = 3.73

def scrape_gog(categoria_esp):
    # Traducir la categoría al inglés
    categoria_eng = categorias_traducidas.get(categoria_esp.lower(), "")
    
    # Construir la URL según la categoría
    if categoria_eng:
        url = f"https://www.gog.com/en/games?genres={categoria_eng}&order=desc:discount"
    else:
        url = "https://www.gog.com/en/games?order=desc:discount"
    
    # Solicitar la página
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al acceder a GOG")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Encontrar todos los elementos de los juegos
    juegos = soup.find_all("div", class_="product-tile__info")
    
    # Extraer datos
    datos = []
    for juego in juegos[:5]:  # Limitar a los primeros 5 juegos
        # Título
        titulo = juego.find("div", class_="product-tile__title")
        titulo_texto = titulo.text.strip() if titulo else "N/A"
        
        # Excluir títulos con "DLC"
        if "DLC" in titulo_texto.upper():
            continue
        
        # Precio con descuento
        precio_descuento = juego.find("span", class_="final-value")
        precio_descuento_texto = precio_descuento.text.strip().replace("$", "").replace(",", "") if precio_descuento else "0"
        
        # Precio original
        precio_original = juego.find("span", class_="base-value")
        precio_original_texto = precio_original.text.strip().replace("$", "").replace(",", "") if precio_original else "0"
        
        # Descuento
        descuento = juego.find("price-discount")
        descuento_texto = (
            descuento.text.strip().replace("%", " %") if descuento else "0 %"
        )
        
        # Convertir precios a soles
        precio_original_soles = float(precio_original_texto) * TASA_CAMBIO if precio_original_texto else 0
        precio_descuento_soles = float(precio_descuento_texto) * TASA_CAMBIO if precio_descuento_texto else 0
        
        # Añadir a la lista
        datos.append({
            "Nombre del Juego": titulo_texto,
            "Descuento (%)": descuento_texto,
            "Precio Original (S/.)": f"{precio_original_soles:.2f} PEN",
            "Precio con Descuento (S/.)": f"{precio_descuento_soles:.2f} PEN",
            "Plataforma": "GOG"
        })
    
    # Crear un DataFrame
    return pd.DataFrame(datos)

# Función para ser llamada con el input de la categoría
def obtener_datos_gog(categoria_usuario):
    return scrape_gog(categoria_usuario)

if __name__ == "__main__":
    categoria_usuario = input("Ingrese la categoría de juegos: ").lower()
    df_gog = obtener_datos_gog(categoria_usuario)

    if not df_gog.empty:
        print(df_gog)
    else:
        print("No se encontraron juegos.")
