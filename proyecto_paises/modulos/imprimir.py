from . import funciones


def paises(datos):
    print(datos)
    for fila in datos:
        pais = fila["nombre"]
        poblacion = fila["poblacion"]
        continente = fila["continente"]
        superficie = fila["superficie"]
        print(f"{pais} ({continente}): {poblacion} habitantes, {superficie} km2.")


def lineas():
    print("---------------------------------")


def espacio():
    print("\n")


def opciones(lista):
    if not lista:
        return "La lista está vacía"
    # Miramos el primer elemento
    primer_elemento = lista[0]
    lineas()
    if isinstance(primer_elemento, dict):
        for i, dato in enumerate(lista):
            print(f"{i+1}. {dato['texto']}")
    elif isinstance(primer_elemento, str):
        for i, dato in enumerate(lista):
            print(f"{i+1}. {dato}")
    lineas()


def pais(nombre, poblacion, superficie, continente):
    print(f"🌍 País:         {nombre}")
    print(f"📌 Continente:   {continente}")
    print(f"👥 Población:    {poblacion} habitantes")
    print(f"📐 Superficie:   {superficie} km2.")


def mostrar_comparacion_edicion(pais_1, pais_2):
    print("🔄 COMPARATIVA DE CAMBIOS:")

    # 1. Comparamos el Nombre
    if pais_1["nombre"] != pais_2["nombre"]:
        print(
            f"🌍 País:       {pais_1['nombre']}  →  {funciones.formatear_nombre_compuesto(pais_2['nombre'])}"
        )
    else:
        print(f"🌍 País:       {pais_2['nombre']} (Sin cambios)")

    # 2. Comparamos el Continente
    if pais_1["continente"] != pais_2["continente"]:
        print(f"📌 Continente: {pais_1['continente']}  →  {pais_2['continente']}")
    else:
        print(f"📌 Continente: {pais_2['continente']} (Sin cambios)")

    # 3. Comparamos la Población
    if str(pais_1["poblacion"]) != str(pais_2["poblacion"]):
        print(f"👥 Población:  {pais_1['poblacion']}  →  {pais_2['poblacion']} hab.")
    else:
        print(f"👥 Población:  {pais_2['poblacion']} habitantes (Sin cambios)")

    # 4. Comparamos la Superficie
    if str(pais_1["superficie"]) != str(pais_2["superficie"]):
        print(f"📐 Superficie: {pais_1['superficie']}  →  {pais_2['superficie']} km2.")
    else:
        print(f"📐 Superficie: {pais_2['superficie']} km2. (Sin cambios)")
