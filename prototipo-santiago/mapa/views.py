from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .busqueda import CONTORNOS, REGIONES, TEXTO_REGIONES, buscar, zonas_seguras_cercanas
from .forms import ComentarioForm
from .templatetags.iconos import PECES
from .models import Comentario, Zona

ORDEN_REGIONES = ["valparaiso", "metropolitana", "ohiggins"]


def inicio(request, zona_id=None):
    """Pantalla del mapa (funcionalidad corazón): mapa de las tres regiones y detalle de la zona."""
    zonas = list(Zona.objects.all())
    texto = request.GET.get("q", "").strip()
    resultado = buscar(texto, zonas)

    zona = None
    if zona_id is not None:
        zona = get_object_or_404(Zona, pk=zona_id)
    elif len(resultado["zonas"]) == 1:
        # Si la búsqueda encontró una sola zona, la mostramos directamente.
        zona = resultado["zonas"][0]

    contexto = {
        "vista": "mapa",
        "texto": texto,
        "resultado": resultado,
        "region_buscada": REGIONES.get(resultado.get("region")),
        "zona": zona,
        "zonas_mapa": [
            {
                "id": z.pk,
                "nombre": z.nombre,
                "comuna": z.comuna,
                "region": z.region,
                "lat": z.latitud,
                "lng": z.longitud,
                "nivel": z.nivel,
                "titulo": z.titulo,
                "url": reverse("mapa:zona", args=[z.pk]) + "#detalle",
            }
            for z in zonas
        ],
        "resaltadas": [z.pk for z in resultado["zonas"]],
        "contornos": CONTORNOS,
        "peces": PECES,
        "regiones": [
            {"clave": clave, "nombre": REGIONES[clave],
             "zonas": sum(z.region == clave for z in zonas)}
            for clave in ORDEN_REGIONES
        ],
        "texto_regiones": TEXTO_REGIONES,
        "cuantas": {
            "si": sum(z.nivel == "si" for z in zonas),
            "ojo": sum(z.nivel == "ojo" for z in zonas),
            "no": sum(z.nivel == "no" for z in zonas),
        },
    }
    if zona:
        contexto["comentarios"] = zona.comentarios.all()[:3]
        contexto["total_comentarios"] = zona.comentarios.count()
        if zona.estado != Zona.ESTADO_SEGURA:
            contexto["cercanas"] = zonas_seguras_cercanas(zona, zonas)
    return render(request, "mapa/inicio.html", contexto)


def comentarios(request):
    """Funcionalidad secundaria: avisar qué se vio en el agua y leer lo que avisaron otros."""
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Listo! Tu comentario fue publicado.")
            return redirect(reverse("mapa:comentarios") + "#lista")
    else:
        form = ComentarioForm(initial={"zona": request.GET.get("zona")})

    zonas = list(Zona.objects.all())
    grupos = [
        {"nombre": REGIONES[clave], "zonas": [z for z in zonas if z.region == clave]}
        for clave in ORDEN_REGIONES
    ]
    contexto = {
        "vista": "comentarios",
        "form": form,
        "tipos": [
            {"valor": valor, "nombre": nombre, "dibujo": Comentario.DIBUJOS[valor][0],
             "nivel": Comentario.DIBUJOS[valor][1]}
            for valor, nombre in Comentario.TIPOS
        ],
        "grupos": grupos,
        "elegido_tipo": form["tipo"].value() or "",
        "elegida_zona": str(form["zona"].value() or ""),
        "comentarios": Comentario.objects.select_related("zona")[:30],
    }
    return render(request, "mapa/comentarios.html", contexto)
