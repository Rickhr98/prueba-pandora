import time
from fetcher import fetch_photos, fetch_album, fetch_all_albums
import time
import threading
import multiprocessing
import logging
import requests
from functools import partial

def run_multithreaded_old(photo_limit):
    """Ejecuta la consulta de fotos y álbumes utilizando múltiples hilos."""
    start_time = time.time()

    photos = fetch_photos(photo_limit)
    logging.info(f"MODO MULTIHILO: {len(photos)} fotos")
    album_data = {}

    # Función para obtener álbum en un hilo y almacenarlo en un diccionario
    def fetch_album_thread(photo):
        album = fetch_album(photo["albumId"])
        album_data[photo["id"]] = album

    threads = []

    # Crear un hilo por cada foto
    for photo in photos:
        thread = threading.Thread(target=fetch_album_thread, args=(photo,))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Mostrar resultados
    for photo in photos:
        album = album_data.get(photo["id"], {"id": "N/A", "title": "Error al obtener álbum"})
        print(f"Foto ID: {photo['id']}")
        print(f"Título: {photo['title']}")
        print(f"URL: {photo['url']}")
        print(f"Álbum ID: {album['id']}")
        print(f"Álbum Título: {album['title']}")
        print("-" * 40)
        logging.info(f"Foto ID: {photo['id']} - {photo['title']} | Álbum: {album['id']} - {album['title']}")

    end_time = time.time()
    duration = end_time - start_time
    if duration < 0:
        print(f"Tiempo total de ejecución: 0 segundos")
        logging.info(f"Tiempo total de ejecución: 0 segundos")
    else:
        print(f"Tiempo total de ejecución: {duration:.3f} segundos")
        logging.info(f"Tiempo total de ejecución: {duration:.3f} segundos")

def run_multiprocessing_old(photo_limit):
    """Ejecuta la consulta de fotos y álbumes utilizando múltiples procesos."""
    start_time = time.time()

    photos = fetch_photos(photo_limit)
    logging.info(f"MODO MULTIPROCESOS: {len(photos)} fotos")

    # Limitar el número de procesos
    num_processes = min(4, multiprocessing.cpu_count())
    batch_size = 500  # Tamaño del lote para procesar
    photo_batches = [photos[i:i + batch_size] for i in range(0, len(photos), batch_size)]

    album_data = {}
    # Usamos un Pool de procesos para obtener los álbumes en paralelo
    # Crear una sesión persistente
    with requests.Session() as session:
        for batch in photo_batches:
            with multiprocessing.Pool(processes=num_processes) as pool:
                fetch_album_with_session = partial(fetch_album, session=session)
                album_results = pool.imap_unordered(fetch_album_with_session, [photo["albumId"] for photo in batch])
                # Convertir los resultados en una lista para iterar
                album_results = list(album_results) 
                # Actualizar el diccionario de álbumes
                album_data.update(dict(zip([photo["albumId"] for photo in batch], album_results)))
                
    # Mostrar resultados
    #for photo, album in zip(photos, album_results):
    for photo in photos:
        album = album_data.get(photo["albumId"], {"id": "N/A", "title": "Error al obtener álbum"})
        print(f"Foto ID: {photo['id']}")
        print(f"Título: {photo['title']}")
        print(f"URL: {photo['url']}")
        print(f"Álbum ID: {album['id']}")
        print(f"Álbum Título: {album['title']}")
        print("-" * 40)
        logging.info(f"Foto ID: {photo['id']} - {photo['title']} | Álbum: {album['id']} - {album['title']}")

    end_time = time.time()
    duration = end_time - start_time
    if duration < 0:
        print(f"Tiempo total de ejecución: 0 segundos")
        logging.info(f"Tiempo total de ejecución: 0 segundos")
    else:
        print(f"Tiempo total de ejecución: {duration:.3f} segundos")
        logging.info(f"Tiempo total de ejecución: {duration:.3f} segundos")
