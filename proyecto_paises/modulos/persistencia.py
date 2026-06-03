import csv
import os

from pathlib import Path

from . import constantes
from . import imprimir

# Definimos las columnas exactamente como deberían estar en el CSV
columnas = ["nombre", "poblacion", "superficie", "continente"]
COLUMNAS_GLOBALES = ["nombre", "poblacion", "superficie", "continente"]

# Construimos la ruta: un nivel atrás y dentro de 'data'
RUTA = Path(__file__).parent.parent / "data" / "paises.csv"
RUTA_REPORTES = Path(__file__).parent.parent / "reportes"


def get_data_dict():
    try:
        with open(RUTA, mode="r", encoding="utf-8") as fichero:
            lector = csv.DictReader(fichero)

            # Convertimos a diccionario: el nombre es la llave
            # y el valor es el resto de la fila
            return {fila["nombre"]: fila for fila in lector}

    except FileNotFoundError:
        print(f"{constantes.TEXTO_ERROR_GENERICO}No se encontró el archivo en {RUTA}")
        return {}


def get_data_list():
    try:
        with open(RUTA, mode="r", encoding="utf-8") as fichero:
            lector = csv.DictReader(fichero)

            # Convertimos el lector directamente a una lista
            return list(lector)

    except FileNotFoundError:
        print(f"{constantes.TEXTO_ERROR_GENERICO}No se encontró el archivo en {RUTA}")
        return []  # Devolvemos lista vacía en caso de error


def añadir_nuevo_pais(nombre, poblacion, superficie, continente):

    # Creamos el diccionario con los datos del nuevo país
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }

    try:
        # Abrimos en modo "a" (append) para añadir al final
        # newline="" evita que se dejen líneas en blanco innecesarias en algunos OS
        with open(RUTA, mode="a", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=columnas)

            escritor.writerow(nuevo_pais)

            print(f"{constantes.TEXTO_EXITO_GENERICO}Datos guardados correctamente.")
            imprimir.pais_creado(nombre, poblacion, superficie, continente)

    except FileNotFoundError:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}No se pudo escribir porque no existe el archivo en {RUTA}"
        )


def guardar_lista_actualizada(paises_actualizados):

    try:
        # Abrimos en modo "w" para sobreescribir el archivo completo
        with open(RUTA, mode="w", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=columnas)

            # Volvemos a poner la cabecera
            escritor.writeheader()

            # Volcamos la lista con los datos ya modificados
            escritor.writerows(paises_actualizados)
            print(f"{constantes.TEXTO_EXITO_GENERICO}Datos guardados correctamente.")

    except FileNotFoundError:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}Error de persistencia: El archivo de datos no existe.\n"
        )
    except ValueError:
        (f"{constantes.TEXTO_ERROR_GENERICO}Algo salio mal")


def eliminar_pais_por_nombre(nombre_eliminar):
    try:
        # 1. Leemos la lista completa actual
        paises = get_data_list()

        # 2. Filtramos dejando fuera el país que queremos borrar
        paises_filtrados = [
            pais for pais in paises if pais["nombre"].lower() != nombre_eliminar.lower()
        ]

        # 3. Controlamos si realmente se filtró algo antes de escribir
        if len(paises) == len(paises_filtrados):
            raise ValueError(
                f"No se pudo eliminar: el país '{nombre_eliminar}' no se encontró en el archivo."
            )

        # 4. Reescribimos el CSV con la lista reducida
        with open(RUTA, mode="w", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(paises_filtrados)
        print(
            f"{constantes.TEXTO_EXITO_GENERICO}¡El país '{nombre_eliminar}' ha sido eliminado correctamente del sistema!"
        )

    except FileNotFoundError:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}Error de persistencia: El archivo de datos no existe.\n"
        )
        return False
    except ValueError as error:
        print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")
        return False
    except Exception as error:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}Error inesperado al escribir en el archivo: {error}\n"
        )
        return False


def guardar_datos_a_txt(nombre_archivo, pila_datos):
    # 1. Creamos la carpeta si no existe
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)

    # 2. Aseguramos la extensión .txt al nombre
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"

    # 3. Armamos la ruta final
    ruta_completa = RUTA_REPORTES / nombre_archivo

    # 4. Evaluamos si el archivo existe solo para el mensaje en consola
    if ruta_completa.exists():
        print(
            f"🔄 El archivo '{ruta_completa.name}' ya existe. ¡Sobrescribiendo por completo!"
        )
    else:
        print(f"✨ El archivo '{ruta_completa.name}' no existe. Creándolo...")

    try:
        # 5. Usamos modo 'w' siempre para reemplazar todo el contenido viejo
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            # Al ser un archivo nuevo/limpio, escribimos la cabecera siempre
            archivo.write(",".join(COLUMNAS_GLOBALES) + "\n")

            # Recorremos manteniendo el orden y protegiendo los datos en memoria
            for item in pila_datos:
                valores = [str(item.get(col, "")) for col in COLUMNAS_GLOBALES]
                archivo.write(",".join(valores) + "\n")

        print(
            f"{constantes.TEXTO_EXITO_GENERICO}Archivo guardado con éxito en reportes"
        )

    except IOError as e:
        print(f"{constantes.TEXTO_ERROR_GENERICO}al manejar el archivo: {e}")


def guardar_estadisticas_a_txt(estadisticas, nombre_archivo):
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"

    ruta_completa = RUTA_REPORTES / nombre_archivo

    # 1. LEER los países que guardó la línea anterior del menú
    contenido_paises = ""
    if ruta_completa.exists():
        try:
            with open(ruta_completa, "r", encoding="utf-8") as archivo_lectura:
                contenido_paises = archivo_lectura.read()
        except IOError as e:
            print(f"{constantes.TEXTO_ERROR_GENERICO}al leer datos previos: {e}")
            return

    # 2. ESCRIBIR todo junto (Estadísticas ARRIBA + Países ABAJO)
    try:
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            # Ponemos las estadísticas primero
            archivo.write(estadisticas)

            # Un salto de línea para separar el informe de los países
            archivo.write("\n")

            # Volvemos a pegar los países abajo
            archivo.write(contenido_paises)

        print(
            f"{constantes.TEXTO_EXITO_GENERICO}Estadísticas añadidas con éxito al archivo"
        )
    except IOError as e:
        print(f"{constantes.TEXTO_ERROR_GENERICO}al manejar el archivo: {e}")
