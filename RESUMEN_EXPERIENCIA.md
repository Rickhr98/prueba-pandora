# Resumen de la experiencia
## Lógica de evaluación de problema, explica tu solución y cómo llegaste a ella
    - Analicé los requerimientos principales de la tarea, entendiendo las principales y las de menor peso.
    - 
## Con qué problemas te has encontrado y cómo los has resuelto.
Al principio obtuve el script con las funcionalidades principales para cierta cantidad de datos; al momento de incrementar la data a buscar me encontré con problemas de optimización y tiempos de respuestas, entonces tuve que analizar lo que habia ya realizado y evaluar que partes podrian estar afectando la obtencion de respuesta; una de ellas era la redundancia al momento de buscar los albums por lo cual se utilizo un diccionario de albums id para no duplicar las busquedas de albums y disminuir las peticiones al servicio.

## Cuándo y por qué se debería usar secuencial, multihilo o multiproceso.

### Secuencial

**Cuándo usar:**
- Con pocos registros
- Cuando las operaciones son simples/rápidas
- Cuando los datos tienen alta dependencia entre sí
- Para APIs con límites estrictos de tasa

**Por qué:**
- Evita sobrecarga de gestión de hilos/procesos
- Más fácil de implementar y depurar
- Flujo de ejecución predecible
- Menor complejidad de código

## Multihilo

**Cuándo usar:**
- Para operaciones limitadas por I/O (red, disco)
- Con muchas solicitudes independientes a APIs
- Cuando necesitas mantener un estado compartido

**Por qué:**
- Los hilos comparten memoria y son más ligeros
- Ideal para operaciones donde se espera respuesta de servicios externos
- Permite gestionar múltiples conexiones concurrentemente
- Aprovecha el tiempo de espera de I/O

## Multiproceso

**Cuándo usar:**
- Para operaciones intensivas en CPU
- Cuando tienes muchos núcleos disponibles
- Para tareas que se pueden dividir en bloques independientes
- Si necesitas eludir el GIL de Python

**Por qué:**
- Utiliza múltiples núcleos del procesador
- Evita las limitaciones del GIL (Global Interpreter Lock)
- Proporciona aislamiento entre procesos
- Mayor eficiencia para cálculos intensivos

La elección debe basarse en la naturaleza de la tarea, los recursos disponibles y las características específicas de la API que estás consultando.