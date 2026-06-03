from . import constantes
from . import imprimir


def pedir_entero(mensaje):
    while True:
        try:
            entrada = input(f"{mensaje}: ").strip()

            if not entrada:
                raise ValueError("El campo no puede estar vacío.")

            try:
                return int(entrada)
            except ValueError:
                raise ValueError("Debes introducir un número entero válido.")

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def pedir_entero_en_rango(mensaje, minimo, maximo):
    while True:
        try:
            numero = pedir_entero(mensaje)

            if numero is None:
                continue
            if numero < minimo or numero > maximo:
                raise ValueError(
                    f"El número debe ser mayor o igual a {minimo} y menor o igual a {maximo}."
                )

            return numero

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def pedir_entero_positivo(mensaje):
    while True:
        try:
            numero = pedir_entero(mensaje)

            if numero is None:
                continue

            if numero <= 0:
                raise ValueError("El número debe ser mayor a 0.")

            return numero

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def pedir_texto_no_vacio(mensaje):
    while True:
        try:
            entrada = input(f"{mensaje}: ").strip()

            if not entrada:
                raise ValueError(
                    "El campo no puede estar vacío. Por favor, escribe algo."
                )

            return entrada

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def pedir_texto(mensaje):
    while True:
        try:
            entrada = input(f"{mensaje}: ").strip()
            return entrada

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def pedir_opcion_booleana(mensaje):
    while True:
        try:
            imprimir.lineas()
            print(mensaje)
            print("1. Sí / Confirmar")
            print("2. No / Cancelar")
            imprimir.lineas()

            # Usamos input directamente para evaluar las opciones fijas 1 y 2
            entrada = input("Seleccione una opción (1-2): ").strip()

            if entrada == "1":
                return True
            elif entrada == "2":
                return False
            else:
                raise ValueError("Debe elegir estrictamente la opción 1 o la opción 2.")

        except ValueError as error:
            print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")
