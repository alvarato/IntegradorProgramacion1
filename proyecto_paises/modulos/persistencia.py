import csv
from pathlib import Path

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
        print(f"Error: No se encontró el archivo en {RUTA}")
        return {}


def get_data_list():
    try:
        with open(RUTA, mode="r", encoding="utf-8") as fichero:
            lector = csv.DictReader(fichero)

            # Convertimos el lector directamente a una lista
            return list(lector)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {RUTA}")
        return []  # Devolvemos lista vacía en caso de error
