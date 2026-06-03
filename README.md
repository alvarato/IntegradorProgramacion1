# Sistema Modular de Gestión, Análisis y Persistencia de Datos Geográficos 🌍

Este proyecto es una aplicación de consola desarrollada en **Python 3.x** diseñada para la administración, filtrado dinámico y análisis estadístico de un dataset de países leído desde un archivo CSV. El sistema aplica un enfoque riguroso de programación modular y separación de responsabilidades, garantizando la consistencia de los datos mediante un mecanismo integrado de control de integridad.

---

## 🛠️ Arquitectura del Sistema y Módulos

El proyecto organiza sus componentes de forma jerárquica para evitar el acoplamiento y facilitar el mantenimiento:

* **`main.py`**: Punto de entrada de la aplicación. Inicializa el sistema y coordina el ciclo de vida del programa.
* **`modulos/interfaz.py`**: Administra la capa de presentación y la navegación interactiva entre los menús y submenús.
* **`modulos/funciones.py`**: Aloja la lógica de negocio pura (algoritmos de ordenamiento, filtros secuenciales y cálculos de métricas).
* **`modulos/persistencia.py`**: Encargado exclusivo del acceso I/O, leyendo de `data/paises.csv` y escribiendo reportes físicos.
* **`modulos/control_entradas.py`**: Valida y sanitiza las entradas por teclado para prevenir excepciones en tiempo de ejecución.
* **`modulos/imprimir.py`**: Centraliza el formateo estético y visual de las tablas e información por pantalla.
* **`modulos/constantes.py`**: Define mensajes fijos y configuraciones globales inmutables.

---

## 🔄 Ciclo de Vida y Flujo de Operación

La aplicación implementa un diseño de flujo dividido en dos fases progresivas para proteger la consistencia de los datos analizados:

### 1. Fase de Gestión de Datos (Menú Principal)
Al iniciar el programa, el operador trabaja sobre la persistencia directa del CSV, pudiendo realizar modificaciones individuales en la base de datos activa a través de operaciones **CRUD**:
* **Alta (Create):** Registrar un nuevo país (Nombre, Población, Superficie, Continente).
* **Consulta (Read):** Búsqueda de países con coincidencia exacta o parcial.
* **Modificación (Update):** Actualización de variables demográficas y de territorio.
* **Baja (Delete):** Remoción de registros individuales.

> ⚠️ **Bloqueo de Transición (Opción 5):** Al seleccionar la opción para proceder al análisis, los datos actuales se cargan de forma estática en la memoria RAM y se "congela" la base de datos. Esto impide alteraciones accidentales sobre los registros mientras se examinan o exportan.

### 2. Fase de Explotación y Análisis (Submenú de Herramientas Avanzadas)
Una vez en el submenú principal de análisis, el usuario manipula la información en memoria a través de cuatro pilares operativos autónomos:

* **Visualización de Datos y Estadísticas:** Módulo enfocado en la salida por pantalla. Imprime el listado actual del dataset y calcula en tiempo real métricas clave (máximos, mínimos y promedios de población/superficie, junto a conteos geográficos).
* **Filtros (Submenú Dinámico y Acumulativo):** Permite segmentar el universo de países por continente, rangos de población o superficie. Este submenú trabaja de forma acumulativa: el usuario puede aplicar múltiples capas consecutivas de filtrado para refinar la información en tiempo real, inhabilitando automáticamente las opciones ya utilizadas para evitar redundancias.
* **Ordenamiento:** Conecta con una interfaz dedicada a reestructurar la lista resultante bajo criterios alfabéticos o numéricos de forma ascendente o descendente.
* **Persistencia de Reportes (Exportación):** Permite materializar de forma permanente el estado exacto de los datos recortados junto con sus estadísticas vigentes en un archivo `.txt` independiente dentro de la carpeta `reportes/`.

---

## 🔒 Mecanismo de Consistencia Interna (Control por Hash)

Para asegurar que las conclusiones del análisis sean verídicas, el sistema integra un control automatizado mediante **Hashing**. 

Si el usuario calcula las estadísticas de un set de datos y posteriormente regresa al submenú dinámico para aplicar nuevas capas de filtrado, el sistema calcula un identificador único de la lista activa y detecta el cambio de integridad instantáneamente. De forma automática, las estadísticas previamente acumuladas se invalidan y eliminan, previniendo la visualización por consola o la exportación física de métricas desactualizadas
