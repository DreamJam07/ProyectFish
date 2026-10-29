"""Carga zonas de ejemplo de Santiago (Región Metropolitana).

Los estados y fechas son DATOS DE EJEMPLO para el prototipo; no son
resultados oficiales de monitoreo.
"""

from datetime import date

from django.db import migrations

ZONAS = [
    {
        "nombre": "Embalse El Yeso", "comuna": "San José de Maipo",
        "tipo_cuerpo_agua": "Embalse", "latitud": -33.676, "longitud": -70.088,
        "estado": "segura", "tipo_contaminacion": "",
        "ultimo_monitoreo": date(2026, 10, 20),
        "descripcion": "Agua de deshielo, sin alertas en el último monitoreo.",
    },
    {
        "nombre": "Laguna Lo Encañado", "comuna": "San José de Maipo",
        "tipo_cuerpo_agua": "Laguna", "latitud": -33.659, "longitud": -70.131,
        "estado": "segura", "tipo_contaminacion": "",
        "ultimo_monitoreo": date(2026, 10, 15),
        "descripcion": "Laguna de cordillera, sin alertas.",
    },
    {
        "nombre": "Río Maipo - Las Vertientes", "comuna": "San José de Maipo",
        "tipo_cuerpo_agua": "Río", "latitud": -33.590, "longitud": -70.470,
        "estado": "segura", "tipo_contaminacion": "",
        "ultimo_monitoreo": date(2026, 10, 18),
        "descripcion": "Tramo alto del río, sin alertas.",
    },
    {
        "nombre": "Río Clarillo", "comuna": "Pirque",
        "tipo_cuerpo_agua": "Río", "latitud": -33.716, "longitud": -70.474,
        "estado": "segura", "tipo_contaminacion": "",
        "ultimo_monitoreo": date(2026, 10, 10),
        "descripcion": "Río dentro de reserva nacional, sin alertas.",
    },
    {
        "nombre": "Laguna de Aculeo", "comuna": "Paine",
        "tipo_cuerpo_agua": "Laguna", "latitud": -33.838, "longitud": -70.918,
        "estado": "precaucion", "tipo_contaminacion": "Exceso de algas y bajo nivel de agua",
        "ultimo_monitoreo": date(2026, 10, 5),
        "descripcion": "Se observan algas en la orilla. Revisar antes de extraer.",
    },
    {
        "nombre": "Laguna Carén", "comuna": "Pudahuel",
        "tipo_cuerpo_agua": "Laguna", "latitud": -33.429, "longitud": -70.849,
        "estado": "precaucion", "tipo_contaminacion": "Exceso de algas",
        "ultimo_monitoreo": date(2026, 9, 28),
        "descripcion": "Aumento de algas por altas temperaturas.",
    },
    {
        "nombre": "Río Maipo - Isla de Maipo", "comuna": "Isla de Maipo",
        "tipo_cuerpo_agua": "Río", "latitud": -33.745, "longitud": -70.900,
        "estado": "precaucion", "tipo_contaminacion": "Restos de agroquímicos",
        "ultimo_monitoreo": date(2026, 10, 1),
        "descripcion": "Zona agrícola. Se recomienda no consumir lo extraído.",
    },
    {
        "nombre": "Río Mapocho - Centro", "comuna": "Santiago",
        "tipo_cuerpo_agua": "Río", "latitud": -33.432, "longitud": -70.652,
        "estado": "prohibida", "tipo_contaminacion": "Contaminación bacteriológica (aguas servidas)",
        "ultimo_monitoreo": date(2026, 10, 12),
        "descripcion": "Tramo urbano. No pescar ni consumir nada extraído aquí.",
    },
    {
        "nombre": "Estero Puangue", "comuna": "María Pinto",
        "tipo_cuerpo_agua": "Estero", "latitud": -33.520, "longitud": -71.130,
        "estado": "prohibida", "tipo_contaminacion": "Agroquímicos y residuos",
        "ultimo_monitoreo": date(2026, 9, 30),
        "descripcion": "Se detectaron peces muertos en el último monitoreo.",
    },
    {
        "nombre": "Embalse Rungue", "comuna": "Tiltil",
        "tipo_cuerpo_agua": "Embalse", "latitud": -33.017, "longitud": -70.893,
        "estado": "prohibida", "tipo_contaminacion": "Metales pesados (relaves mineros)",
        "ultimo_monitoreo": date(2026, 9, 25),
        "descripcion": "Cercano a depósitos de relaves. Extracción prohibida.",
    },
]


def cargar_zonas(apps, schema_editor):
    Zona = apps.get_model("mapa", "Zona")
    for datos in ZONAS:
        Zona.objects.get_or_create(nombre=datos["nombre"], defaults=datos)


def borrar_zonas(apps, schema_editor):
    Zona = apps.get_model("mapa", "Zona")
    Zona.objects.filter(nombre__in=[z["nombre"] for z in ZONAS]).delete()


class Migration(migrations.Migration):
    dependencies = [("mapa", "0001_initial")]

    operations = [migrations.RunPython(cargar_zonas, borrar_zonas)]
