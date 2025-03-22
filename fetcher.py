import requests
import logging
import time

PHOTO_URL = "https://jsonplaceholder.typicode.com/photos/"
ALBUM_ID_URL = "https://jsonplaceholder.typicode.com/albums/{}"
ALBUM_ALL_URL = "https://jsonplaceholder.typicode.com/albums/"

# Configuración del logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

"""
Funciones para obtener fotos y álbumes de la API JSONPlaceholder.
"""
def fetch_photos(limit=None):
    """Obtiene la lista de fotos."""
    resp = []
    try:
        response = requests.get(PHOTO_URL)
        if response.status_code == 200:
            photos = response.json()
            # Devolver la cantidad de fotos hasta el límit especificado
            resp = photos[:limit] if limit else photos
        else:
            logging.error(f"Error al obtener las fotos: {response.status_code}")
    except requests.RequestException as e:    
            logging.error(f"Error al obtener las fotos: {e}")
    
    return resp


"""
Funciones para obtener un álbum de la API JSONPlaceholder por su ID.
"""
def fetch_album(album_id):
    """Obtiene el álbum correspondiente."""
    album = {}
    try:
        response = requests.get(ALBUM_ID_URL.format(album_id))
        if response.status_code == 200:
            album = response.json()
        else:
            logging.warning(f"Error al obtener el álbum {album_id}: {response.status_code}")
    except requests.RequestException as e:
            logging.warning(f"Error al obtener el álbum {album_id}: {e}")

    return album

"""
Funciones para obtener todos los álbums de la API JSONPlaceholder.
"""
def fetch_all_albums():
    """Obtiene todos los albums."""
    albums = []
    try:
        response = requests.get(ALBUM_ALL_URL)
        if response.status_code == 200:
            albums = list(response.json())
        else:
            logging.warning(f"Error al obtener los álbums {response.status_code}")
    except requests.RequestException as e:
            logging.warning(f"Error al obtener los álbum: {e}")

    return albums