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