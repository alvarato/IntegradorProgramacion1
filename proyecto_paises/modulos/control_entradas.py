import constantes


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
