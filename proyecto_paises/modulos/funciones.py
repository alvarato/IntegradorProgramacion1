import persistencia


def obtener_todos():
    return persistencia.get_data_list()


def filtrar_por_contiene_nombre(datos, texto):
    # Pasamos el texto a minúsculas para que no importe si escriben "AR" o "ar"
    texto = texto.lower()
    return [p for p in datos if texto in p["nombre"].lower()]


def filtrar_por_igual_nombre(datos, texto):
    # Pasamos el texto a minúsculas para que no importe si escriben "AR" o "ar"
    texto = texto.lower()
    return [p for p in datos if texto == p["nombre"].lower()]


def filtrar_por_contiente(datos, contiente):
    return [p for p in datos if contiente == p["continente"]]


def filtrar_por_poblacion_mayor_igual_que(datos, poblacion):
    return [p for p in datos if poblacion <= int(p["poblacion"])]


def filtrar_por_poblacion_menor_igual_que(datos, poblacion):
    return [p for p in datos if poblacion >= int(p["poblacion"])]


def aplicar_filtros(filtros):
    datos = persistencia.get_data_list()

    for filtro in filtros:
        nombre_filtro, valor = list(filtro.items())[0]

        match nombre_filtro:
            case "igual_nombre":
                filtrar_por_igual_nombre(datos, valor)
            case "contiene_nombre":
                datos = filtrar_por_contiene_nombre(datos, valor)
            case "continente":
                datos = filtrar_por_contiente(datos, valor)
            case "mayor":
                datos = filtrar_por_poblacion_mayor_igual_que(datos, valor)
            case "menor":
                datos = filtrar_por_poblacion_menor_igual_que(datos, valor)

    return datos
