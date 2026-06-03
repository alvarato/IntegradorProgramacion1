from . import funciones
from . import constantes
from . import control_entradas
from . import imprimir


def _manejar_filtro_continente(
    continentes_disponibles,
    opciones_disponibles,
    indice_opcion,
    continentes_elegidos,
):
    if not continentes_disponibles:
        print("❌ Ya has seleccionado todos los continentes disponibles.\n")
        return

    imprimir.opciones(continentes_disponibles)

    sub_opcion = control_entradas.pedir_entero_en_rango(
        "Ingrese la opcion", 1, len(continentes_disponibles)
    )

    # Extraemos el continente y lo removemos de la lista
    continente_elegido = continentes_disponibles.pop(sub_opcion - 1)

    continentes_elegidos.append(continente_elegido)

    # Si ya no quedan continentes, removemos la opción del menú principal
    if not continentes_disponibles:
        opciones_disponibles.pop(indice_opcion)


def _manejar_filtros_generales(
    opcion_seleccionada, opciones, indice_opcion, opciones_elegidas
):
    """Maneja los filtros comunes de texto/número y los remueve del menú."""
    valor = control_entradas.pedir_texto_no_vacio("Ingrese el valor")

    opciones_elegidas.append({"nombre": opcion_seleccionada["nombre"], "valor": valor})
    # Eliminamos la opción para que no vuelva a aparecer
    opciones.pop(indice_opcion)


def buscar_con_filtros(datos, opciones_disponibles, continentes_disponibles):
    opciones_elegidas = []
    continentes_elegidos = []

    while True:
        imprimir.opciones(opciones_disponibles)

        opcion = control_entradas.pedir_entero_en_rango(
            "Ingrese la opcion", 1, len(opciones_disponibles)
        )

        # 1. Si elige "Realizar búsqueda"
        if opcion == 1:
            # Si la primera vez que ejecuto los filtros ya eligio un Continentes
            # No tiene sentido que pueda filtrar por el resto de continentes si ya se usaron
            if len(continentes_elegidos) > 0:
                opciones_disponibles.pop(1)
            break

        # Guardamos el índice real de la lista (opcion - 1) y la opción seleccionada
        indice_actual = opcion - 1
        opcion_seleccionada = opciones_disponibles[indice_actual]

        # 2. Derivamos a la subfunción correspondiente
        if opcion_seleccionada["nombre"] == "continente":
            _manejar_filtro_continente(
                continentes_disponibles,
                opciones_disponibles,
                indice_actual,
                continentes_elegidos,
            )
        else:
            _manejar_filtros_generales(
                opcion_seleccionada,
                opciones_disponibles,
                indice_actual,
                opciones_elegidas,
            )
    filtro = {"generales": opciones_elegidas, "continentes": continentes_elegidos}
    return funciones.aplicar_filtros(filtro, datos)


def obtener_datos_csv():
    return funciones.obtener_datos_csv()


###CRUD
# CREATE
def solicitar_datos_nuevo_pais():
    imprimir.espacio()
    imprimir.lineas()
    print("📋 REGISTRAR NUEVO PAÍS")
    imprimir.lineas()

    # Solicitamos los datos usando tus funciones seguras
    nombre = control_entradas.pedir_texto_no_vacio("Ingrese el nombre del país")
    print("Ingrese el Contiente")
    imprimir.opciones(constantes.CONTINENTES)
    opcion = control_entradas.pedir_entero_en_rango(
        "Ingrese la opcion", 1, len(constantes.CONTINENTES)
    )
    continente = constantes.CONTINENTES[opcion - 1]
    poblacion = control_entradas.pedir_entero_positivo("Ingrese la población")
    superficie = control_entradas.pedir_entero_positivo(
        "Ingrese la superficie (en km²)"
    )

    imprimir.lineas()
    funciones.añadir_nuevo_pais(nombre, poblacion, superficie, continente)

    imprimir.lineas()
    imprimir.espacio()


# READ
def solicitar_busqueda_pais():
    imprimir.espacio()
    imprimir.lineas()
    print("🔍 BUSCAR PAÍS POR NOMBRE")
    imprimir.lineas()

    # 1. Pedimos el nombre asegurando que no vaya vacío
    nombre_buscar = control_entradas.pedir_texto_no_vacio(
        "Ingrese el nombre del país que busca"
    )

    # 2. Llamamos a tu función de búsqueda en la capa de funciones
    pais_encontrado = funciones.buscar_pais_por_nombre(nombre_buscar)

    imprimir.lineas()

    if pais_encontrado is not None:
        print(f"{constantes.TEXTO_EXITO_GENERICO}¡País encontrado con éxito!")
        imprimir.lineas()

        # Mostramos la ficha del país
        imprimir.pais(
            nombre=pais_encontrado["nombre"],
            continente=pais_encontrado["continente"],
            poblacion=pais_encontrado["poblacion"],
            superficie=pais_encontrado["superficie"],
        )
    else:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}El país '{nombre_buscar}' no se encuentra registrado."
        )

    imprimir.lineas()
    imprimir.espacio()


# UPDATE
def solicitar_edicion_pais():
    imprimir.espacio()
    imprimir.lineas()
    print("📝 EDITAR PAÍS EXISTENTE")
    imprimir.lineas()

    nombre = control_entradas.pedir_texto_no_vacio("Ingrese el nombre del país")
    pais = funciones.buscar_pais_por_nombre(nombre)

    if pais == None:
        print(f"{constantes.TEXTO_ERROR_GENERICO}país no encontrado.")
        return

    print(f"Ingrese el Contiente (Actual: '{pais["continente"]}')")
    imprimir.opciones(constantes.CONTINENTES)

    opcion = control_entradas.pedir_entero_en_rango(
        "Ingrese la opcion", 1, len(constantes.CONTINENTES)
    )
    continente = constantes.CONTINENTES[opcion - 1]

    poblacion = control_entradas.pedir_entero_positivo(
        f"Ingrese la población (Actual:'{pais["poblacion"]}')"
    )
    superficie = control_entradas.pedir_entero_positivo(
        f"Ingrese la superficie (en km²) (Actual: '{pais["superficie"]})'"
    )

    pais_editado = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }

    imprimir.espacio()
    imprimir.mostrar_comparacion_edicion(pais, pais_editado)

    if control_entradas.pedir_opcion_booleana("Confirmar Cambios"):
        funciones.modificar_pais_en_lista(pais["nombre"], pais_editado)
    else:
        print(f"Cambios no aplicados...")

    imprimir.lineas()
    imprimir.espacio()


# DELETE
def solicitar_eliminacion_pais():
    imprimir.espacio()
    imprimir.lineas()
    print("❌ ELIMINAR PAÍS")
    imprimir.lineas()

    # 1. Pedimos el nombre del país a eliminar
    nombre = control_entradas.pedir_texto_no_vacio(
        "Ingrese el nombre del país que desea eliminar"
    )
    pais_encontrado = funciones.buscar_pais_por_nombre(nombre)

    imprimir.lineas()

    if not pais_encontrado:
        print(
            f"{constantes.TEXTO_ERROR_GENERICO}El país '{nombre}' no existe en el sistema."
        )
    else:
        imprimir.pais(
            nombre=pais_encontrado["nombre"],
            continente=pais_encontrado["continente"],
            poblacion=pais_encontrado["poblacion"],
            superficie=pais_encontrado["superficie"],
        )
        if control_entradas.pedir_opcion_booleana("Confirmar Cambios"):
            funciones.eliminar_pais(nombre)
        else:
            print(f"Cambios no aplicados...")

    imprimir.lineas()
    imprimir.espacio()


###CRUD


def guardar_datos_a_txt(datos, estadisticas):
    nombre = control_entradas.pedir_texto_no_vacio("Ingrese el nombre del archivo")
    funciones.guardar_datos_a_txt(nombre, datos, estadisticas)


def ordenar_datos_por_nombre(pila_datos, reverse):
    funciones.ordenar_datos_por_nombre(pila_datos, reverse)


def ordenar_datos_por_numero(pila_datos, columna_num, reverse):
    funciones.ordenar_datos_por_numero(pila_datos, columna_num, reverse)


def calcular_hash_datos(datos):
    return funciones.calcular_hash_datos(datos)


def generar_bloque_informe(datos):
    return funciones.generar_bloque_informe(datos)
