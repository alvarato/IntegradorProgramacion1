import persistencia
import constantes


def obtener_todos():
    return persistencia.get_data_list()


def _filtrar_por_contiene_nombre(datos, texto):
    # Pasamos el texto a minúsculas para que no importe si escriben "AR" o "ar"
    texto = texto.lower()
    return [p for p in datos if texto in p["nombre"].lower()]


def _filtrar_por_igual_nombre(datos, texto):
    # Pasamos el texto a minúsculas para que no importe si escriben "AR" o "ar"
    texto = texto.lower()
    return [p for p in datos if texto == p["nombre"].lower()]


def _filtrar_por_contientes(datos, contientes):
    return [p for p in datos if p["continente"] in contientes]


def _filtrar_por_superficie_mayor_igual_que(datos, superficie):
    return [p for p in datos if superficie <= int(p["superficie"])]


def _filtrar_por_superficie_menor_igual_que(datos, superficie):
    return [p for p in datos if superficie >= int(p["superficie"])]


def _filtrar_por_poblacion_mayor_igual_que(datos, poblacion):
    return [p for p in datos if poblacion <= int(p["poblacion"])]


def _filtrar_por_poblacion_menor_igual_que(datos, poblacion):
    return [p for p in datos if poblacion >= int(p["poblacion"])]


def aplicar_filtros(filtros):
    datos = persistencia.get_data_list()
    print(filtros)

    if len(filtros["continentes"]) != 0:
        datos = _filtrar_por_contientes(datos, filtros["continentes"])

    for filtro in filtros["generales"]:
        nombre_filtro, valor = list(filtro.items())[0]

        match nombre_filtro:
            case "contiene_nombre":
                datos = _filtrar_por_contiene_nombre(datos, valor)
            case "poblacion_mayor":
                datos = _filtrar_por_poblacion_mayor_igual_que(datos, valor)
            case "poblacion_menor":
                datos = _filtrar_por_poblacion_menor_igual_que(datos, valor)
            case "superficie_mayor":
                datos = _filtrar_por_superficie_mayor_igual_que(datos, valor)
            case "superficie_menor":
                datos = _filtrar_por_superficie_menor_igual_que(datos, valor)

    return datos


def buscar_pais_por_nombre(nombre):
    paises = persistencia.get_data_list()

    # Recorremos la lista buscando coincidencia exacta ignorando mayúsculas/minúsculas
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais

    return None  # Si termina el ciclo y no lo encuentra, devuelve None


def formatear_nombre_compuesto(texto):
    return texto.strip().title()


def añadir_nuevo_pais(nombre, poblacion, superficie, continente):
    try:
        if buscar_pais_por_nombre(nombre) != None:
            raise ValueError("Nombre de país duplicado.")
        nombre = formatear_nombre_compuesto(nombre)
        persistencia.añadir_nuevo_pais(nombre, poblacion, superficie, continente)

    except ValueError as error:
        print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


def modificar_pais_en_lista(nombre_buscar, nuevos_datos):
    paises = persistencia.get_data_list()

    for pais in paises:
        if pais["nombre"].lower() == nombre_buscar.lower():
            # Se hace el intercambio de datos aquí
            pais.update(nuevos_datos)
            break

    # Mandamos la lista a persistencia para que solo haga el guardado
    return persistencia.guardar_lista_actualizada(paises)


def eliminar_pais(nombre):
    persistencia.eliminar_pais_por_nombre(nombre)
