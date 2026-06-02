import csv
from pathlib import Path
import constantes
import imprimir

# Definimos las columnas exactamente como deberían estar en el CSV
columnas = ["nombre", "poblacion", "superficie", "continente"]

# Construimos la ruta: un nivel atrás y dentro de 'data'
RUTA = Path(__file__).parent.parent / "data" / "paises.csv"


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
