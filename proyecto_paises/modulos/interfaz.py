import funciones
import constantes
import control_entradas


def imprimir(datos):
    for fila in datos:
        pais = fila["nombre"]
        poblacion = fila["poblacion"]
        continente = fila["continente"]
        print(f"{pais} ({continente}): {poblacion} habitantes.")


def imprimir_lineas():
    print("---------------------------------")


def imprimir_espacio():
    print("\n")


def imprimir_opciones(lista):
    if not lista:
        return "La lista está vacía"
    # Miramos el primer elemento
    primer_elemento = lista[0]
    imprimir_lineas()
    if isinstance(primer_elemento, dict):
        for i, dato in enumerate(lista):
            print(f"{i+1}. {dato['texto']}")
    elif isinstance(primer_elemento, str):
        for i, dato in enumerate(lista):
            print(f"{i+1}. {dato}")
    imprimir_lineas()
    imprimir_espacio()


def buscar_con_filtros():
    opciones = constantes.OPCIONES_BASE_FILTROS
    opciones_elegidas = []
    nueva_opcion = {"nombre": "enviar", "texto": "Realiar busqueda"}
    opciones.insert(0, nueva_opcion)

    while True:
        imprimir_opciones(opciones)

        opcion = control_entradas.pedir_entero_en_rango(
            "Ingrese la opcion", 1, len(opciones)
        )

        if opcion == 1:
            break
            ## si elije contienente mostramos la opciones de este
        if opcion == 6:
            imprimir_opciones(constantes.CONTINENTES)
            sub_opcion = control_entradas.pedir_entero_en_rango(
                "Ingrese la opcion", 1, len(constantes.CONTINENTES)
            )
            funciones.añadir_nuevo_filtro(
                opciones_elegidas,
                constantes.OPCIONES_BASE_FILTROS[opcion - 1]["nombre"],
                constantes.CONTINENTES[sub_opcion - 1],
            )
        else:
            valor = control_entradas.pedir_texto_no_vacio("Ingrese el texto")
            print(opcion - 1)
            funciones.añadir_nuevo_filtro(
                opciones_elegidas,
                opciones[opcion - 1]["nombre"],
                valor,
            )
    print(opciones_elegidas)
    return opciones_elegidas


filtros = [
    {"contiene_nombre": "ia"},
    {"mayor": 40000000},
    {"menor": 60000000},
    {"continente": "América"},
    # {"continente": "Europa"},
]
imprimir(funciones.aplicar_filtros(buscar_con_filtros()))
# buscar_con_filtros()
# imprimir(funciones.aplicar_filtros(filtros))
