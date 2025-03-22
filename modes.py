import time
from fetcher import fetch_photos, fetch_album, fetch_all_albums
import time
import threading
import multiprocessing
import logging
import requests
from functools import partial

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
    
    # Obtener solo los IDs de álbumes únicos para evitar solicitudes duplicadas
    unique_album_ids = list(set(photo["albumId"] for photo in photos))
    album_data = {}
    
    # Crear un semáforo para limitar el número máximo de hilos concurrentes
    max_threads = min(50, len(unique_album_ids))
    thread_limiter = threading.Semaphore(max_threads)

    # Función para obtener álbum en un hilo, con limitación de concurrencia
    def fetch_album_thread(album_id):
        with thread_limiter:
            album = fetch_album(album_id)
            album_data[album_id] = album
            
    threads = []
    
    # Crear un hilo por cada álbum único
    for album_id in unique_album_ids:
        thread = threading.Thread(target=fetch_album_thread, args=(album_id,))
        threads.append(thread)
        thread.start()
        
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Mostrar resultados
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
    print(f"Tiempo total de ejecución: {duration:.3f} segundos")
    logging.info(f"Tiempo total de ejecución: {duration:.3f} segundos")

def run_multiprocessing(photo_limit):
    """Ejecuta la consulta de fotos y álbumes utilizando múltiples procesos."""
    start_time = time.time()

    photos = fetch_photos(photo_limit)
    logging.info(f"MODO MULTIPROCESOS: {len(photos)} fotos")
    
    # Obtener lista única de IDs de álbumes para evitar solicitudes duplicadas
    unique_album_ids = list(set(photo["albumId"] for photo in photos))
    
    # Limitar el número de procesos a algo razonable
    num_processes = min(8, multiprocessing.cpu_count(), len(unique_album_ids))
    
    # Dividir la lista de IDs de álbumes en lotes para cada proceso
    chunks = [unique_album_ids[i::num_processes] for i in range(num_processes)]
    
    # Función para un proceso, que procesa un lote de álbumes
    def process_album_batch(album_ids):
        session = requests.Session()  # Usar una sesión persistente
        results = {}
        for album_id in album_ids:
            album = fetch_album(album_id, session=session)
            results[album_id] = album
        return results
    
    # Crear y ejecutar los procesos
    with multiprocessing.Manager() as manager:
        # Usar un diccionario compartido
        shared_results = manager.dict()
        processes = []
        
        for chunk in chunks:
            if not chunk:  # Saltar chunks vacíos
                continue
                
            # Crea un proceso para procesar un lote de álbumes, donde le paso los IDs y el diccionario compartido
            p = multiprocessing.Process(
                target=lambda ids, results: results.update(process_album_batch(ids)),
                args=(chunk, shared_results)
            )
            processes.append(p)
            p.start()
        
        # Esperar a que todos los procesos terminen
        for p in processes:
            p.join()
        
        # Convertir el resultado en un diccionario normal
        album_data = dict(shared_results)
    
    # Mostrar resultados
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
    print(f"Tiempo total de ejecución: {duration:.3f} segundos")
    logging.info(f"Tiempo total de ejecución: {duration:.3f} segundos")