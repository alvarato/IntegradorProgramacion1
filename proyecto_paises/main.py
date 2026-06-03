import sys
from modulos import interfaz
from modulos import imprimir
from modulos import control_entradas
from modulos import constantes

import os
import sys


def esperar_tecla():
    print("\nPresione cualquier tecla para continuar...")

    # Si el sistema operativo es Windows
    if os.name == "nt":
        import msvcrt

        msvcrt.getch()  # Captura una tecla sin necesidad de pulsar Enter

    # Si el sistema operativo es Linux / Mac (Unix)
    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)  # Lee un solo carácter
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def mostrar_menu_opciones():
    imprimir.espacio()
    imprimir.lineas()

    print("=" * 40)
    print("   🌍  SISTEMA DE GESTIÓN DE PAÍSES 🌍")
    print("=" * 40)
    print("1. Alta de Nuevo País")
    print("2. Buscar País")
    print("3. Editar Información de País")
    print("4. Eliminar País")
    print("5. Filtros Avanzados y Reportes")
    print("6. Salir")
    print("=" * 40)

    imprimir.lineas()
    imprimir.espacio()


def mostrar_menu_filtros():
    imprimir.espacio()
    imprimir.lineas()

    print("=" * 40)
    print(" 🔍  SUBMENÚ: FILTROS DE BÚSQUEDA")
    print("=" * 40)
    print("1. Imprimir Paises")
    print("2. Utilizar Filtros")
    print("3. Ordenar Listado por...")
    print("4. Generar Estadisticas")
    print("5. Imprimir Estadisticas")
    print("6. Generar TXT con resultados")
    print("7. Salir")
    print("=" * 40)

    imprimir.lineas()
    imprimir.espacio()


def mostrar_menu_ordenamiento():
    imprimir.espacio()
    imprimir.lineas()

    print("=" * 40)
    print(" 📊  SUBMENÚ: ORDENAR LISTADO")
    print("=" * 40)
    print("1. Ordenar por Nombre (A-Z)")
    print("2. Ordenar por Mayor Población")
    print("3. Ordenar por Menor Población")
    print("4. Ordenar por Mayor Superficie")
    print("5. Ordenar por Menor Superficie")
    print("6. Volver al menú de filtros")
    print("=" * 40)

    imprimir.lineas()
    imprimir.espacio()


def menu_ordenamiento(datos):

    while True:
        esperar_tecla()
        mostrar_menu_ordenamiento()

        # Son 6 opciones en el submenú de ordenamiento
        opcion = control_entradas.pedir_entero_en_rango(
            "Seleccione una opción (1-6): ", 1, 6
        )

        if opcion == 1:
            # Ordenar por Nombre A-Z (se muestra A-Z, por eso reverse=False)
            interfaz.ordenar_datos_por_nombre(datos, reverse=False)
            print(
                f"{constantes.TEXTO_EXITO_GENERICO}Listado ordenado por Nombre (A-Z)."
            )
            break  # Volvemos automáticamente al menú de filtros mostrando el resultado

        elif opcion == 2:
            # Mayor Población (el más grande debe quedar arriba/primero)
            interfaz.ordenar_datos_por_numero(datos, "poblacion", reverse=True)
            print(
                f"{constantes.TEXTO_EXITO_GENERICO}Listado ordenado por Mayor Población."
            )
            break

        elif opcion == 3:
            # Menor Población (el más chico primero)
            interfaz.ordenar_datos_por_numero(datos, "poblacion", reverse=False)
            print(
                f"{constantes.TEXTO_EXITO_GENERICO}Listado ordenado por Menor Población."
            )
            break

        elif opcion == 4:
            # Mayor Superficie
            interfaz.ordenar_datos_por_numero(datos, "superficie", reverse=True)
            print(
                f"{constantes.TEXTO_EXITO_GENERICO}Listado ordenado por Mayor Superficie."
            )
            break

        elif opcion == 5:
            # Menor Superficie
            interfaz.ordenar_datos_por_numero(datos, "superficie", reverse=False)
            print(
                f"{constantes.TEXTO_EXITO_GENERICO}Listado ordenado por Menor Superficie."
            )
            break

        elif opcion == 6:
            print("\nVolviendo al submenú de filtros sin cambios...")
            break

    return datos


def menu_filtros():
    datos = interfaz.obtener_lista_de_datos()
    estadisticas = ""
    # filtros
    opciones_disponibles = constantes.OPCIONES_BASE_FILTROS.copy()
    continentes_disponibles = constantes.CONTINENTES.copy()
    nueva_opcion = {"nombre": "enviar", "texto": "Aplicar Filtros"}
    opciones_disponibles.insert(0, nueva_opcion)
    # filtros

    print(f"{constantes.TEXTO_EXITO_GENERICO}El listado de todos los paises esta listo")
    while True:
        esperar_tecla()
        mostrar_menu_filtros()

        opcion = control_entradas.pedir_entero_en_rango(
            "Seleccione una opción (1-7): ", 1, 7
        )

        if opcion == 1:
            imprimir.paises(datos)

        elif opcion == 2:
            datos, estadisticas = interfaz.manejar_busqueda_con_filtros(
                datos, estadisticas, opciones_disponibles, continentes_disponibles
            )

        elif opcion == 3:
            menu_ordenamiento(datos)

        elif opcion == 4:
            estadisticas = interfaz.generar_bloque_informe(datos)

        elif opcion == 5:
            if len(estadisticas) != 0:
                print(estadisticas)
            else:
                print("No hay Estadisticas generadas")

        elif opcion == 6:
            interfaz.guardar_datos_a_txt(datos, estadisticas)

        elif opcion == 7:
            print("\nVolviendo al menú principal...")
            break  # Rompe ESTE bucle while, haciéndote regresar al menú del main.py


def ejecutor_sistema() -> None:

    opcion = 0
    while opcion != 7:
        esperar_tecla()
        mostrar_menu_opciones()
        try:
            opcion = control_entradas.pedir_entero_en_rango(
                "Seleccione una opción (1-7): ", 1, 7
            )

            if opcion == 1:
                interfaz.solicitar_datos_nuevo_pais()
            elif opcion == 2:
                interfaz.solicitar_busqueda_pais()
            elif opcion == 3:
                interfaz.solicitar_edicion_pais()
            elif opcion == 4:
                interfaz.solicitar_eliminacion_pais()
            elif opcion == 5:
                menu_filtros()
            elif opcion == 6:
                print(
                    "¡Muchas gracias por utilizar el Sistema de Control de Inventario! Saliendo..."
                )

        except ValueError:  # Exception:
            print("Error Inesperado: Cargando el Menú principal")


# ---------------------------------------------------------------------
# MENU
# ---------------------------------------------------------------------

ejecutor_sistema()
