"""Lógica de búsqueda: decide si lo que escribió la persona es de Santiago o no."""

import math
import unicodedata

# Por ahora el prototipo solo tiene datos de la Región Metropolitana (Santiago).
NOMBRES_REGION = {"santiago", "region metropolitana", "rm", "stgo", "santiago de chile"}

COMUNAS_RM = {
    "alhue", "buin", "calera de tango", "cerrillos", "cerro navia", "colina",
    "conchali", "curacavi", "el bosque", "el monte", "estacion central",
    "huechuraba", "independencia", "isla de maipo", "la cisterna", "la florida",
    "la granja", "la pintana", "la reina", "lampa", "las condes", "lo barnechea",
    "lo espejo", "lo prado", "macul", "maipu", "maria pinto", "melipilla", "nunoa",
    "padre hurtado", "paine", "pedro aguirre cerda", "penaflor", "penalolen",
    "pirque", "providencia", "pudahuel", "puente alto", "quilicura",
    "quinta normal", "recoleta", "renca", "san bernardo", "san joaquin",
    "san jose de maipo", "san miguel", "san pedro", "san ramon", "santiago",
    "talagante", "tiltil", "vitacura",
}

# Contorno aproximado de la Región Metropolitana (latitud, longitud), para avisar
# cuando la persona está o toca el mapa fuera de Santiago.
CONTORNO_SANTIAGO = [
    (-32.92, -70.80), (-32.95, -70.55), (-33.05, -70.30), (-33.10, -70.00),
    (-33.35, -69.85), (-33.70, -69.80), (-34.00, -69.95), (-34.25, -70.30),
    (-34.15, -70.60), (-33.95, -70.75), (-34.05, -71.00), (-33.95, -71.35),
    (-34.00, -71.55), (-33.75, -71.70), (-33.55, -71.55), (-33.35, -71.45),
    (-33.20, -71.25), (-33.05, -71.05),
]


def normalizar(texto):
    """Pasa a minúsculas y quita tildes y espacios extra: 'Maipú ' -> 'maipu'."""
    sin_tildes = unicodedata.normalize("NFKD", texto or "")
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return " ".join(sin_tildes.lower().split())


def buscar(texto, zonas):
    """Clasifica la búsqueda y devuelve un diccionario con el resultado.

    tipo puede ser:
      - "vacio": no se escribió nada.
      - "santiago": se buscó la región completa; se muestran todas las zonas.
      - "zonas": se encontraron zonas por nombre o comuna.
      - "comuna_sin_datos": es una comuna de Santiago, pero sin zonas registradas.
      - "sin_info": el lugar no es de Santiago; todavía no hay información.
    """
    consulta = normalizar(texto)
    if not consulta:
        return {"tipo": "vacio", "zonas": []}

    if consulta in NOMBRES_REGION:
        return {"tipo": "santiago", "zonas": list(zonas)}

    encontradas = [
        z for z in zonas
        if consulta in normalizar(z.nombre) or consulta == normalizar(z.comuna)
    ]
    if encontradas:
        return {"tipo": "zonas", "zonas": encontradas}

    if consulta in COMUNAS_RM:
        return {"tipo": "comuna_sin_datos", "zonas": []}

    return {"tipo": "sin_info", "zonas": []}


def distancia_km(lat1, lon1, lat2, lon2):
    """Distancia en línea recta entre dos puntos (fórmula de Haversine)."""
    radio_tierra = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    return radio_tierra * 2 * math.asin(math.sqrt(a))


def zonas_seguras_cercanas(zona, zonas, cantidad=3):
    """Zonas sin alerta más cercanas a una zona contaminada (HdU 2)."""
    seguras = [z for z in zonas if z.estado == z.ESTADO_SEGURA and z.pk != zona.pk]
    for z in seguras:
        z.distancia = round(distancia_km(zona.latitud, zona.longitud, z.latitud, z.longitud))
    return sorted(seguras, key=lambda z: z.distancia)[:cantidad]


# Centro de Santiago, se usa cuando la persona elige "todo Santiago".
CENTRO_SANTIAGO = {"nombre": "Todo Santiago", "lat": -33.45, "lon": -70.66}


def dentro_de_santiago(lat, lon):
    """True si el punto está dentro del contorno de la Región Metropolitana."""
    dentro = False
    puntos = CONTORNO_SANTIAGO
    for (lat1, lon1), (lat2, lon2) in zip(puntos, puntos[1:] + puntos[:1]):
        if (lat1 > lat) != (lat2 > lat):
            corte = lon1 + (lat - lat1) * (lon2 - lon1) / (lat2 - lat1)
            if lon < corte:
                dentro = not dentro
    return dentro


def lugares(zonas):
    """Comunas que tienen zonas revisadas, con un punto central para medir distancias."""
    por_comuna = {}
    for z in zonas:
        por_comuna.setdefault(z.comuna, []).append(z)
    return [
        {
            "nombre": comuna,
            "lat": sum(z.latitud for z in lista) / len(lista),
            "lon": sum(z.longitud for z in lista) / len(lista),
            "zonas": len(lista),
        }
        for comuna, lista in sorted(por_comuna.items())
    ]


def ordenar_por_cercania(zonas, lugar):
    """Agrega z.distancia (km) a cada zona y las ordena de la más cercana a la más lejana."""
    for z in zonas:
        z.distancia = round(distancia_km(lugar["lat"], lugar["lon"], z.latitud, z.longitud))
    return sorted(zonas, key=lambda z: z.distancia)
