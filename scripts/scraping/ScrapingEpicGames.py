from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_epic_games(categoria_usuario):
    url_base = f'https://store.epicgames.com/es-ES/browse?q={categoria_usuario}&sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&category=Game&count=40&start=0'
    
    with sync_playwright() as p:
        # Inicia un navegador Chromium
        browser = p.chromium.launch(headless=False)  # Usamos headless=False para ver el navegador
        page = browser.new_page()

        # Abre la página web
        page.goto(url_base)

        # Asegúrate de que la página haya cargado completamente
        page.wait_for_selector('.css-1a6kj04', timeout=90000)  # Esperar el selector de los juegos

        # Ahora, obtén todos los juegos listados
        juegos = page.query_selector_all('.css-1a6kj04')

        if not juegos:
            print("No se encontraron juegos. Verifica los selectores.")
            return pd.DataFrame()

        data = []
        for juego in juegos[:5]:  # Limitar a los primeros 5 juegos
            try:
                nombre = juego.query_selector('.css-rgqwpc').inner_text()
                descuento = juego.query_selector('.eds_1xxntt819').inner_text() if juego.query_selector('.eds_1xxntt819') else 'No Disponible'
                precio_original = juego.query_selector('.css-4jky3p').inner_text()
                precio_descuento = juego.query_selector('.eds_1ypbntdc').inner_text()

                # Almacena los datos en una lista
                data.append({
                    'Nombre del Juego': nombre.strip(),
                    'Descuento (%)': descuento.strip(),
                    'Precio Original (S/.)': precio_original.strip(),
                    'Precio con Descuento (S/.)': precio_descuento.strip(),
                    'Plataforma': 'Epic Games'
                })
            except Exception as e:
                print(f"Error con un juego: {e}")
        
        # Cierra el navegador
        browser.close()

        # Crear un DataFrame con los datos obtenidos
        df = pd.DataFrame(data)
        return df

# Función para ser llamada con el input de la categoría
def obtener_datos_epic(categoria_usuario):
    return scrape_epic_games(categoria_usuario)

if __name__ == "__main__":
    categoria_usuario = input("Ingresa la categoría (ejemplo: accion, rpg, etc.): ").lower()
    df_epic = obtener_datos_epic(categoria_usuario)

    if not df_epic.empty:
        print(df_epic)
    else:
        print("No se pudo obtener datos.")