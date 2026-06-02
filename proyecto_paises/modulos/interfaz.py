import funciones
import constantes
import control_entradas
import imprimir


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


def _manejar_filtro_continente(
    continentes_disponibles,
    opciones,
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
        opciones.pop(indice_opcion)


def _manejar_filtros_generales(
    opcion_seleccionada, opciones, indice_opcion, opciones_elegidas
):
    """Maneja los filtros comunes de texto/número y los remueve del menú."""
    valor = control_entradas.pedir_texto_no_vacio("Ingrese el valor")

    funciones.añadir_nuevo_filtro(
        opciones_elegidas,
        opcion_seleccionada["nombre"],
        valor,
    )
    # Eliminamos la opción para que no vuelva a aparecer
    opciones.pop(indice_opcion)


def buscar_con_filtros():
    """Función principal que controla el bucle del menú de búsqueda."""
    opciones = constantes.OPCIONES_BASE_FILTROS.copy()
    continentes_disponibles = constantes.CONTINENTES.copy()
    opciones_elegidas = []
    continentes_elegidos = []

    nueva_opcion = {"nombre": "enviar", "texto": "Realizar búsqueda"}
    opciones.insert(0, nueva_opcion)

    while True:
        imprimir.pciones(opciones)

        opcion = control_entradas.pedir_entero_en_rango(
            "Ingrese la opcion", 1, len(opciones)
        )

        # 1. Si elige "Realizar búsqueda"
        if opcion == 1:
            break

        # Guardamos el índice real de la lista (opcion - 1) y la opción seleccionada
        indice_actual = opcion - 1
        opcion_seleccionada = opciones[indice_actual]

        # 2. Derivamos a la subfunción correspondiente
        if opcion_seleccionada["nombre"] == "continente":
            _manejar_filtro_continente(
                opcion_seleccionada,
                continentes_disponibles,
                opciones,
                indice_actual,
                continentes_elegidos,
            )
        else:
            _manejar_filtros_generales(
                opcion_seleccionada, opciones, indice_actual, opciones_elegidas
            )
    filtro = {"generales": opciones_elegidas, "continentes": continentes_elegidos}
    print(filtro)
    return filtro


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

    if pedir_opcion_booleana("Confirmar Cambios"):
        funciones.modificar_pais_en_lista(pais["nombre"], pais_editado)
    else:
        print(f"Cambios no aplicados...")

    imprimir.lineas()
    imprimir.espacio()


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
        if pedir_opcion_booleana("Confirmar Cambios"):
            funciones.eliminar_pais(nombre)
        else:
            print(f"Cambios no aplicados...")

    imprimir.lineas()
    imprimir.espacio()
