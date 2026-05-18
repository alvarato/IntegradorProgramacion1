# control_entradas.py


def pedir_entero_en_rango(mensaje, minimo=None, maximo=None):
    """
    Pide un número entero por consola y valida que esté dentro de un rango.
    Si el usuario se equivoca, muestra un error y vuelve a preguntar.
    """
    while True:
        entrada = input(f"{mensaje}: ")

        try:
            numero = int(entrada)
            if (minimo is not None and numero < minimo) or (
                maximo is not None and numero > maximo
            ):
                print(
                    f"❌ Error: El número tiene que estar entre {minimo} y {maximo}.\n"
                )
                continue
            return numero
        except ValueError:
            print("❌ Error: Debes introducir un número entero válido.\n")


# control_entradas.py


def pedir_texto_no_vacio(mensaje):
    while True:
        entrada = input(f"{mensaje}: ")

        texto_limpio = entrada.strip()

        if not texto_limpio:
            print("❌ Error: El campo no puede estar vacío. Por favor, escribe algo.\n")
            continue

        return texto_limpio
