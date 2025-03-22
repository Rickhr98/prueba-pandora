import argparse
from modes import run_sequential, run_multithreaded, run_multiprocessing
import time
import logging

# Configuración del logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def compare_modes(photo_limit):
    """Compara el tiempo de ejecución de los tres modos."""
    print("Iniciando la comparación de tiempos...")

    # Modo Secuencial
    start_time = time.time()
    run_sequential(photo_limit)
    sequential_time = time.time() - start_time
    print(f"\nTiempo en modo secuencial: {sequential_time:.3f} segundos")

    # Modo Multihilos
    start_time = time.time()
    run_multithreaded(photo_limit)
    multithreaded_time = time.time() - start_time
    print(f"\nTiempo en modo multihilos: {multithreaded_time:.3f} segundos")

    # Modo Multiprocesos
    start_time = time.time()
    run_multiprocessing(photo_limit)
    multiprocessing_time = time.time() - start_time
    print(f"\nTiempo en modo multiprocesos: {multiprocessing_time:.3f} segundos")

    # Comparación
    print("\nComparativa de tiempos:")
    print(f"Secuencial: {sequential_time:.3f} segundos")
    print(f"Multihilos: {multithreaded_time:.3f} segundos")
    print(f"Multiprocesos: {multiprocessing_time:.3f} segundos")
    logging.info(f"\nCOMPARATIVA DE TIEMPOS:\n Secuencial: {sequential_time:.3f} segundos\n Multihilos: {multithreaded_time:.3f} segundos\n Multiprocesos: {multiprocessing_time:.3f} segundos")

    # Determinar cuál es el más rápido
    fastest_mode = min(sequential_time, multithreaded_time, multiprocessing_time)
    if fastest_mode == sequential_time:
        print("\nEl modo más rápido fue: Secuencial")
        logging.info("El modo más rápido fue: Secuencial")
    elif fastest_mode == multithreaded_time:
        print("\nEl modo más rápido fue: Multihilos")
        logging.info("El modo más rápido fue: Multihilos")
    else:
        print("\nEl modo más rápido fue: Multiprocesos")
        logging.info("El modo más rápido fue: Multiprocesos")

def main():
    # Configurar argumentos de la CLI
    parser = argparse.ArgumentParser(description="CLI para obtener fotos y sus álbumes usando diferentes métodos.")
    parser.add_argument("--mode", choices=["secuencial", "multihilos", "multiprocesos", "comparar"], required=True,
                        help="Modo de ejecución: secuencial, multihilos, multiprocesos, comparar (todos)")
    parser.add_argument("--photos", type=int, default=None,
                        help="Cantidad de fotos a obtener (por defecto, todas)")

    # Parsear argumentos
    args = parser.parse_args()

    # Imprimir los argumentos
    # print(f"Modo seleccionado: {args.mode}")
    # print(f"Número de fotos: {args.photos if args.photos else 'Todas'}")
    if args.mode == "secuencial":
        run_sequential(args.photos)
    elif args.mode == "multihilos":
        run_multithreaded(args.photos)
    elif args.mode == "multiprocesos":
        run_multiprocessing(args.photos)
    elif args.mode == "comparar":
        compare_modes(args.photos)

if __name__ == "__main__":
    main()
    
