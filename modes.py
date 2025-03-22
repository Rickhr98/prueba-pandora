import time
from fetcher import fetch_photos, fetch_album, fetch_all_albums
import time
import threading
import multiprocessing
import logging

# Configurar logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_sequential(photo_limit):
    """Ejecuta la consulta de fotos y álbumes de forma secuencial."""
    start_time = time.time()

    photos = fetch_photos(photo_limit)
    logging.info(f"MODO SECUENCIAL: {len(photos)} fotos")
    albums = fetch_all_albums()
    # crear un diccionario de álbumes con el ID como clave
    album_dict = {album["id"]: album for album in albums}

    for photo in photos:
        # obtener el álbum correspondiente del indice creado
        album = album_dict[photo["albumId"]]
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

def run_multithreaded(photo_limit):
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

def run_multiprocessing(photo_limit):
    """Ejecuta la consulta de fotos y álbumes utilizando múltiples procesos."""
    start_time = time.time()

    photos = fetch_photos(photo_limit)
    logging.info(f"MODO MULTIPROCESOS: {len(photos)} fotos")

    # Usamos un Pool de procesos para obtener los álbumes en paralelo
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        album_results = pool.map(fetch_album, [photo["albumId"] for photo in photos])

    # Mostrar resultados
    for photo, album in zip(photos, album_results):
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