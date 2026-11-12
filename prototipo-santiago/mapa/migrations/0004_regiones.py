"""Agrega la región a cada zona y carga zonas de ejemplo de Valparaíso y O'Higgins.

Los estados y fechas son DATOS DE EJEMPLO para el prototipo; no son
resultados oficiales de monitoreo.
"""

from datetime import date

from django.db import migrations, models

ZONAS = [
    # ---- Región de Valparaíso ----
    {"nombre": "Bahía de Valparaíso", "region": "valparaiso", "comuna": "Valparaíso",
     "tipo_cuerpo_agua": "Mar", "latitud": -33.030, "longitud": -71.630,
     "estado": "precaucion", "tipo_contaminacion": "Aguas servidas cerca de la orilla",
     "ultimo_monitoreo": date(2026, 11, 3),
     "descripcion": "Revisar antes de sacar mariscos cerca del puerto."},
    {"nombre": "Bahía de Quintero", "region": "valparaiso", "comuna": "Quintero",
     "tipo_cuerpo_agua": "Mar", "latitud": -32.770, "longitud": -71.530,
     "estado": "prohibida", "tipo_contaminacion": "Restos de petróleo y metales pesados",
     "ultimo_monitoreo": date(2026, 10, 28),
     "descripcion": "Cercana a la zona industrial. No pescar ni sacar mariscos."},
    {"nombre": "Caleta Horcón", "region": "valparaiso", "comuna": "Puchuncaví",
     "tipo_cuerpo_agua": "Mar", "latitud": -32.715, "longitud": -71.495,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 11, 5),
     "descripcion": "Agua limpia en el último monitoreo."},
    {"nombre": "Desembocadura del Aconcagua", "region": "valparaiso", "comuna": "Concón",
     "tipo_cuerpo_agua": "Río", "latitud": -32.930, "longitud": -71.520,
     "estado": "precaucion", "tipo_contaminacion": "Descargas urbanas e industriales",
     "ultimo_monitoreo": date(2026, 10, 30),
     "descripcion": "Se recomienda no consumir lo extraído."},
    {"nombre": "Embalse Los Aromos", "region": "valparaiso", "comuna": "Limache",
     "tipo_cuerpo_agua": "Embalse", "latitud": -32.960, "longitud": -71.290,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 11, 2),
     "descripcion": "Sin alertas en el último monitoreo."},
    {"nombre": "Humedal Laguna El Peral", "region": "valparaiso", "comuna": "Cartagena",
     "tipo_cuerpo_agua": "Laguna", "latitud": -33.470, "longitud": -71.630,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 10, 22),
     "descripcion": "Humedal protegido, sin alertas."},
    {"nombre": "Laguna del Inca", "region": "valparaiso", "comuna": "Los Andes",
     "tipo_cuerpo_agua": "Laguna", "latitud": -32.830, "longitud": -70.120,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 10, 18),
     "descripcion": "Laguna de cordillera, sin alertas."},
    # ---- Región de O'Higgins ----
    {"nombre": "Laguna Cáhuil", "region": "ohiggins", "comuna": "Pichilemu",
     "tipo_cuerpo_agua": "Laguna", "latitud": -34.490, "longitud": -71.980,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 11, 6),
     "descripcion": "Agua limpia en el último monitoreo."},
    {"nombre": "Punta de Lobos", "region": "ohiggins", "comuna": "Pichilemu",
     "tipo_cuerpo_agua": "Mar", "latitud": -34.430, "longitud": -72.040,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 11, 6),
     "descripcion": "Sin alertas."},
    {"nombre": "Embalse Rapel", "region": "ohiggins", "comuna": "Litueche",
     "tipo_cuerpo_agua": "Embalse", "latitud": -34.070, "longitud": -71.570,
     "estado": "precaucion", "tipo_contaminacion": "Exceso de algas",
     "ultimo_monitoreo": date(2026, 10, 29),
     "descripcion": "Aumento de algas por el calor. Revisar antes de extraer."},
    {"nombre": "Río Cachapoal - Rancagua", "region": "ohiggins", "comuna": "Rancagua",
     "tipo_cuerpo_agua": "Río", "latitud": -34.170, "longitud": -70.740,
     "estado": "precaucion", "tipo_contaminacion": "Descargas urbanas",
     "ultimo_monitoreo": date(2026, 11, 1),
     "descripcion": "Tramo urbano. No consumir lo extraído."},
    {"nombre": "Río Tinguiririca", "region": "ohiggins", "comuna": "San Fernando",
     "tipo_cuerpo_agua": "Río", "latitud": -34.580, "longitud": -70.990,
     "estado": "segura", "tipo_contaminacion": "",
     "ultimo_monitoreo": date(2026, 10, 25),
     "descripcion": "Sin alertas en el último monitoreo."},
    {"nombre": "Embalse Convento Viejo", "region": "ohiggins", "comuna": "Chimbarongo",
     "tipo_cuerpo_agua": "Embalse", "latitud": -34.680, "longitud": -71.130,
     "estado": "prohibida", "tipo_contaminacion": "Algas tóxicas y bajo nivel de agua",
     "ultimo_monitoreo": date(2026, 10, 27),
     "descripcion": "Extracción prohibida hasta nuevo aviso."},
]


def cargar_zonas(apps, schema_editor):
    Zona = apps.get_model("mapa", "Zona")
    for datos in ZONAS:
        Zona.objects.get_or_create(nombre=datos["nombre"], defaults=datos)


def borrar_zonas(apps, schema_editor):
    Zona = apps.get_model("mapa", "Zona")
    Zona.objects.filter(nombre__in=[z["nombre"] for z in ZONAS]).delete()


class Migration(migrations.Migration):
    dependencies = [("mapa", "0003_comentario_tipo")]

    operations = [
        migrations.AddField(
            model_name="zona",
            name="region",
            field=models.CharField(
                choices=[
                    ("valparaiso", "Región de Valparaíso"),
                    ("metropolitana", "Región Metropolitana"),
                    ("ohiggins", "Región de O'Higgins"),
                ],
                default="metropolitana",
                max_length=20,
            ),
        ),
        migrations.RunPython(cargar_zonas, borrar_zonas),
    ]
