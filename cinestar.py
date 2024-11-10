from flask import Flask, render_template
import requests

app = Flask(__name__)


def obtener_datos_api(url):
    try:
        response = requests.get(url, verify=False)  
        print(f"Estado de la respuesta: {response.status_code}")
        response.raise_for_status()  
        datos = response.json()  
        print(f"Contenido de la respuesta: {datos}")
        return datos.get('data', [])  
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return []  

@app.route("/")
def index():
    return render_template('index.html') 


@app.route("/cines", defaults={'id': None})
@app.route("/cines/<id>")
def cines(id):
    cines = obtener_datos_api('https://oaemdl.es/cinestar_sweb_php/cines') 
    if id is None:
        return render_template('cines.html', cines=cines)  
    
    cine = next((cine for cine in cines if cine['id'] == id), None)
    
    return render_template('cine.html' if cine else 'cine_no_encontrado.html', cine=cine)


@app.route("/peliculas/", defaults={'id': None})
@app.route("/peliculas/<id>")
def peliculas(id):
    
    if id == 'cartelera':
        peliculas = obtener_datos_api('https://oaemdl.es/cinestar_sweb_php/peliculas/cartelera')
    elif id == 'estrenos':
        peliculas = obtener_datos_api('https://oaemdl.es/cinestar_sweb_php/peliculas/estrenos')
    else:
        
        peliculas = obtener_datos_api('https://oaemdl.es/cinestar_sweb_php/peliculas')
        pelicula = next((pelicula for pelicula in peliculas if str(pelicula['id']) == str(id)), None)
        if pelicula is None:
            return render_template('pelicula_no_encontrada.html') 
        return render_template('pelicula.html', pelicula=pelicula)  

    return render_template('peliculas.html', peliculas=peliculas, id=id) 


@app.route("/trailer/<int:id>")
def trailer(id):
    trailer_data = obtener_datos_api(f'https://oaemdl.es/cinestar_sweb_php/trailer/{id}')
    if not trailer_data:
        return render_template('trailer_no_encontrado.html') 
    return render_template('trailer.html', trailer=trailer_data) 


if __name__ == "__main__":
    app.run(debug=True)
