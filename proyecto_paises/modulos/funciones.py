from . import constantes
from . import persistencia
import hashlib


def calcular_hash_datos(datos):
    if not datos:
        return ""

    # Convertimos la lista de diccionarios a un string único y estable
    # Usamos str(datos) o json.dumps para representar el estado actual en texto
    datos_string = str(datos)

    # Creamos el hash MD5 a partir de ese texto codificado en bytes
    return hashlib.md5(datos_string.encode("utf-8")).hexdigest()


def obtener_lista_de_datos():
    return persistencia.obtener_lista_de_datos()


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


def obtener_datos_csv():
    return persistencia.get_data_list()


def aplicar_filtros(filtros, datos):
    if len(filtros["continentes"]) != 0:
        datos = _filtrar_por_contientes(datos, filtros["continentes"])

    for filtro in filtros["generales"]:

        match filtro["nombre"]:

            case "contiene_nombre":
                datos = _filtrar_por_contiene_nombre(datos, filtro["valor"])
            case "poblacion_mayor":
                datos = _filtrar_por_poblacion_mayor_igual_que(datos, filtro["valor"])
            case "poblacion_menor":
                datos = _filtrar_por_poblacion_menor_igual_que(datos, filtro["valor"])
            case "superficie_mayor":
                datos = _filtrar_por_superficie_mayor_igual_que(datos, filtro["valor"])
            case "superficie_menor":
                datos = _filtrar_por_superficie_menor_igual_que(datos, filtro["valor"])

    return datos


def formatear_nombre_compuesto(texto):
    return texto.strip().title()


###CRUD
# READ
def buscar_pais_por_nombre(nombre):
    paises = persistencia.get_data_list()

    # Recorremos la lista buscando coincidencia exacta ignorando mayúsculas/minúsculas
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais

    return None  # Si termina el ciclo y no lo encuentra, devuelve None


# CREATE
def añadir_nuevo_pais(nombre, poblacion, superficie, continente):
    try:
        if buscar_pais_por_nombre(nombre) != None:
            raise ValueError("Nombre de país duplicado.")
        nombre = formatear_nombre_compuesto(nombre)
        persistencia.añadir_nuevo_pais(nombre, poblacion, superficie, continente)

    except ValueError as error:
        print(f"{constantes.TEXTO_ERROR_GENERICO}{error}\n")


# UPDATE
def modificar_pais_en_lista(nombre_buscar, nuevos_datos):
    paises = persistencia.get_data_list()

    for pais in paises:
        if pais["nombre"].lower() == nombre_buscar.lower():
            # Se hace el intercambio de datos aquí
            pais.update(nuevos_datos)
            break

    # Mandamos la lista a persistencia para que solo haga el guardado
    return persistencia.guardar_lista_actualizada(paises)


# DELETE
def eliminar_pais(nombre):
    persistencia.eliminar_pais_por_nombre(nombre)


###CRUD


def guardar_datos_a_txt(nombre, datos, estadisticas):
    persistencia.guardar_datos_a_txt(nombre, datos)
    if len(estadisticas) != 0:
        persistencia.guardar_estadisticas_a_txt(estadisticas, nombre)


def ordenar_datos_por_nombre(pila_datos, reverse):
    return pila_datos.sort(key=lambda x: x["nombre"].lower(), reverse=reverse)


def ordenar_datos_por_numero(pila_datos, columna_num, reverse):
    pila_datos.sort(key=lambda x: int(x.get(columna_num, 0) or 0), reverse=reverse)


def generar_bloque_informe(pila_datos):
    if not pila_datos:
        return "⚠️ La lista de datos está vacía. No se puede generar el informe.\n"

    # 1. Inicializamos variables de control apuntando al primer elemento
    pais_mas_poblado = pila_datos[0]
    pais_menos_poblado = pila_datos[0]
    pais_mas_grande = pila_datos[0]
    pais_mas_chico = pila_datos[0]

    total_poblacion = 0
    total_superficie = 0
    total_paises = len(pila_datos)

    # 2. Calculamos las métricas recorriendo la lista
    for item in pila_datos:
        pob_actual = int(item.get("poblacion", 0) or 0)
        sup_actual = int(item.get("superficie", 0) or 0)

        total_poblacion += pob_actual
        total_superficie += sup_actual

        # Evaluamos Población
        if pob_actual > int(pais_mas_poblado.get("poblacion", 0) or 0):
            pais_mas_poblado = item
        if pob_actual < int(pais_menos_poblado.get("poblacion", 0) or 0):
            pais_menos_poblado = item

        # Evaluamos Superficie
        if sup_actual > int(pais_mas_grande.get("superficie", 0) or 0):
            pais_mas_grande = item
        if sup_actual < int(pais_mas_chico.get("superficie", 0) or 0):
            pais_mas_chico = item

    # 3. Calculamos promedios
    prom_poblacion = total_poblacion / total_paises
    prom_superficie = total_superficie / total_paises

    # 4. Construimos el bloque de texto (string)
    lineas = [
        "\n" + "=" * 55,
        "📊 INFORMACIÓN BÁSICA DEL INFORME",
        "=" * 55,
        f"🥇 Pais con mas poblacion:   {pais_mas_poblado['nombre']} ({int(pais_mas_poblado['poblacion']):,} hab.)",
        f"🔻 Pais con menos poblacion: {pais_menos_poblado['nombre']} ({int(pais_menos_poblado['poblacion']):,} hab.)",
        f"👥 Promedio de poblacion:    {prom_poblacion:,.2f} hab.",
        "-" * 55,
        f"🌍 Pais con mayor tamano:    {pais_mas_grande['nombre']} ({int(pais_mas_grande['superficie']):,} km²)",
        f"🔎 Pais con menor tamano:    {pais_mas_chico['nombre']} ({int(pais_mas_chico['superficie']):,} km²)",
        f"📐 Promedio de superficie:   {prom_superficie:,.2f} km²",
        "=" * 55 + "\n",
    ]
    print(
        f"{constantes.TEXTO_EXITO_GENERICO}Estadísticas del informe creadas exitosamente"
    )
    # Juntamos todas las líneas con saltos de página
    return "\n".join(lineas)
