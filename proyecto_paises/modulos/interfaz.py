import funciones
import constantes


def imprimir(datos):
    for fila in datos:
        pais = fila["nombre"]
        poblacion = fila["poblacion"]
        continente = fila["continente"]
        print(f"{pais} ({continente}): {poblacion} habitantes.")


def buscar_con_filtros():
    opciones_restantes = constantes.OPCIONES_BASE_FILTROS
    opciones_elegidas = []
    while True:

        for i, filtro in enumerate(opciones_restantes):
            print(f"{i+1}. {filtro['texto']}")

        opcion = input("Ingrese la opcion: ")
        if opcion == "0":
            break
        elif opcion.isdigit() and int(opcion) <= len(opciones_restantes):
            index = int(opcion) - 1
            valor = input(f"Ingrese el filtro {opciones_restantes[index]["nombre"]} :")
            opciones_elegidas.append({opciones_restantes[index]["nombre"]})
            opciones_restantes.pop(index)

    print(opciones_elegidas)


filtros = [
    {"contiene_nombre": "ia"},
    {"mayor": 40000000},
    {"menor": 60000000},
    {"continente": "América"},
    # {"continente": "Europa"},
]

buscar_con_filtros()
# imprimir(funciones.aplicar_filtros(filtros))
