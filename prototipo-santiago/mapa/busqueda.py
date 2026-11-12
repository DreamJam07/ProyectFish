"""Lógica de búsqueda: decide si lo que escribió la persona está dentro de las regiones
que tienen datos (Valparaíso, Metropolitana y O'Higgins) o no."""

import math
import unicodedata

# Por ahora el prototipo solo tiene datos de estas tres regiones.
REGIONES = {
    "valparaiso": "Región de Valparaíso",
    "metropolitana": "Región Metropolitana",
    "ohiggins": "Región de O'Higgins",
}
TEXTO_REGIONES = "las regiones de Valparaíso, Metropolitana y O'Higgins"

# Con qué nombres se puede buscar una región entera.
NOMBRES_REGION = {
    "metropolitana": {"santiago", "region metropolitana", "metropolitana", "rm", "stgo",
                      "santiago de chile", "region de santiago"},
    "valparaiso": {"region de valparaiso", "region valparaiso", "v region", "quinta region",
                   "5 region", "region v"},
    "ohiggins": {"ohiggins", "region de ohiggins", "region ohiggins", "vi region", "sexta region",
                 "6 region", "region vi", "libertador general bernardo ohiggins"},
}

COMUNAS = {
    "metropolitana": {
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
    },
    "valparaiso": {
        "valparaiso", "vina del mar", "concon", "quintero", "puchuncavi", "casablanca",
        "juan fernandez", "isla de pascua", "san antonio", "cartagena", "el tabo",
        "el quisco", "algarrobo", "santo domingo", "quilpue", "villa alemana", "limache",
        "olmue", "los andes", "san esteban", "calle larga", "rinconada", "san felipe",
        "putaendo", "santa maria", "panquehue", "llaillay", "catemu", "quillota",
        "la cruz", "la calera", "nogales", "hijuelas", "la ligua", "cabildo", "papudo",
        "zapallar", "petorca",
    },
    "ohiggins": {
        "rancagua", "codegua", "coinco", "coltauco", "donihue", "graneros", "las cabras",
        "machali", "malloa", "mostazal", "olivar", "peumo", "pichidegua", "quinta de tilcoco",
        "rengo", "requinoa", "san vicente", "pichilemu", "la estrella", "litueche",
        "marchigue", "navidad", "paredones", "san fernando", "chepica", "chimbarongo",
        "lolol", "nancagua", "palmilla", "peralillo", "placilla", "pumanque", "santa cruz",
    },
}

# Contorno aproximado de cada región (latitud, longitud), para avisar cuando la persona
# toca el mapa fuera de las regiones que tienen datos.
CONTORNOS = {
    "valparaiso": [
        (-32.05, -71.60), (-32.10, -70.50), (-32.45, -70.05), (-32.85, -69.95),
        (-33.00, -70.30), (-32.95, -70.55), (-32.92, -70.80), (-33.05, -71.05),
        (-33.20, -71.25), (-33.35, -71.45), (-33.55, -71.55), (-33.65, -71.78),
        (-33.00, -71.78), (-32.50, -71.65),
    ],
    "metropolitana": [
        (-32.92, -70.80), (-32.95, -70.55), (-33.05, -70.30), (-33.10, -70.00),
        (-33.35, -69.85), (-33.70, -69.80), (-34.00, -69.95), (-34.25, -70.30),
        (-34.15, -70.60), (-33.95, -70.75), (-34.05, -71.00), (-33.95, -71.35),
        (-34.00, -71.55), (-33.75, -71.70), (-33.55, -71.55), (-33.35, -71.45),
        (-33.20, -71.25), (-33.05, -71.05),
    ],
    "ohiggins": [
        (-33.95, -71.85), (-34.00, -71.55), (-33.95, -71.35), (-34.05, -71.00),
        (-33.95, -70.75), (-34.15, -70.60), (-34.25, -70.30), (-34.45, -70.10),
        (-34.75, -70.35), (-34.95, -70.60), (-35.00, -71.05), (-34.95, -71.60),
        (-34.65, -72.05), (-34.40, -72.05), (-34.10, -71.95),
    ],
}


def normalizar(texto):
    """Pasa a minúsculas y quita tildes, apóstrofos y espacios extra: "O'Higgins " -> "ohiggins"."""
    sin_tildes = unicodedata.normalize("NFKD", (texto or "").replace("'", "").replace("’", ""))
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return " ".join(sin_tildes.lower().split())


def region_de_comuna(consulta):
    """Región a la que pertenece una comuna (texto ya normalizado), o None."""
    for region, comunas in COMUNAS.items():
        if consulta in comunas:
            return region
    return None


def buscar(texto, zonas):
    """Clasifica la búsqueda y devuelve un diccionario con el resultado.

    tipo puede ser:
      - "vacio": no se escribió nada.
      - "region": se buscó una región completa; se muestran todas sus zonas.
      - "zonas": se encontraron zonas por nombre o comuna.
      - "comuna_sin_datos": es una comuna de las tres regiones, pero sin zonas registradas.
      - "sin_info": el lugar no es de estas regiones; todavía no hay información.
    """
    consulta = normalizar(texto)
    if not consulta:
        return {"tipo": "vacio", "zonas": []}

    for region, nombres in NOMBRES_REGION.items():
        if consulta in nombres:
            return {"tipo": "region", "region": region,
                    "zonas": [z for z in zonas if z.region == region]}

    encontradas = [
        z for z in zonas
        if consulta in normalizar(z.nombre) or consulta == normalizar(z.comuna)
    ]
    if encontradas:
        return {"tipo": "zonas", "zonas": encontradas}

    region = region_de_comuna(consulta)
    if region:
        return {"tipo": "comuna_sin_datos", "region": region, "zonas": []}

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


def dentro_de_las_regiones(lat, lon):
    """True si el punto está dentro del contorno de alguna de las tres regiones."""
    for puntos in CONTORNOS.values():
        dentro = False
        for (lat1, lon1), (lat2, lon2) in zip(puntos, puntos[1:] + puntos[:1]):
            if (lat1 > lat) != (lat2 > lat):
                corte = lon1 + (lat - lat1) * (lon2 - lon1) / (lat2 - lat1)
                if lon < corte:
                    dentro = not dentro
        if dentro:
            return True
    return False
