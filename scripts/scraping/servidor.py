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
