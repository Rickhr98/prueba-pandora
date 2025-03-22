
# Prueba Técnica - Desarrollador Python

## Descripción

Este proyecto consiste en una aplicación de línea de comandos (CLI) escrita en Python que realiza solicitudes a la API pública de [JSONPlaceholder](https://jsonplaceholder.typicode.com/). La aplicación obtiene información sobre fotos y álbumes, y proporciona tres enfoques diferentes para hacer estas solicitudes de forma eficiente:

1. **Modo Secuencial**: Realiza la consulta de fotos y álbumes de manera secuencial, sin concurrencia.
2. **Modo Multihilos**: Realiza las consultas utilizando hilos concurrentes.
3. **Modo Multiprocesos**: Realiza las consultas utilizando procesos en paralelo.

Además, se incluye una opción para comparar automáticamente los tiempos de ejecución de los tres enfoques.

## Requisitos

- Python 3.6 o superior
- Paquetes de Python:
  - `requests`
  - `argparse`
  - `logging`

Puedes instalar las dependencias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

## Instalación

1. Clona este repositorio en tu máquina local:

```bash
git clone <url_del_repositorio>
cd <nombre_del_repositorio>
```

2. Crea un entorno virtual e instala las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows, usa 'venv\Scripts\activate'
pip install -r requirements.txt
```

## Uso

La aplicación se ejecuta desde la línea de comandos utilizando el siguiente formato:

```bash
python script.py --mode <modo> --photos <número_de_fotos>
```

### Modos disponibles:

- **secuencial**: Ejecuta la consulta de fotos y álbumes de manera secuencial.
  
  Ejemplo:
  ```bash
  python script.py --mode secuencial --photos 5
  ```

- **multihilos**: Ejecuta la consulta utilizando hilos concurrentes.
  
  Ejemplo:
  ```bash
  python script.py --mode multihilos --photos 5
  ```

- **multiprocesos**: Ejecuta la consulta utilizando múltiples procesos.
  
  Ejemplo:
  ```bash
  python script.py --mode multiprocesos --photos 5
  ```

- **comparar**: Compara los tiempos de ejecución de los tres modos (secuencial, multihilos y multiprocesos).
  
  Ejemplo:
  ```bash
  python script.py --mode comparar --photos 5
  ```

### Parámetros:

- **--mode**: Define el modo de ejecución. Puede ser uno de los siguientes: `secuencial`, `multihilos`, `multiprocesos` o `comparar`.
- **--photos**: Define el número de fotos a obtener. Si no se proporciona, se obtendrán todas las fotos disponibles en el endpoint.

## Resultados esperados

El programa imprimirá los siguientes datos en la consola:

- **Modo de ejecucion y fotos a obtener**
- **ID de la foto**
- **Título de la foto**
- **URL de la foto**
- **ID del álbum**
- **Título del álbum**
- **Tiempo total de ejecución** para cada modo.

Si se ejecuta en modo de comparación, también se mostrará una tabla con los tiempos de ejecución para cada modo y cuál es el más rápido.

## Manejo de Errores

El programa maneja errores comunes como problemas de red o de la API, e intenta reintentar las solicitudes cuando sea necesario. Los errores también se registran en el archivo `app.log`.

