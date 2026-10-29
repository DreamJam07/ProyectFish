from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .busqueda import (
    CENTRO_SANTIAGO, CONTORNO_SANTIAGO, buscar, dentro_de_santiago, lugares,
    ordenar_por_cercania, zonas_seguras_cercanas,
)
from .forms import ComentarioForm
from .models import Comentario, Zona


def lugar_actual(request):
    """El lugar que eligió la persona (se guarda en la sesión). Si no eligió, todo Santiago."""
    return request.session.get("lugar") or CENTRO_SANTIAGO


def contexto_base(request, vista):
    return {
        "vista": vista,
        "lugar": lugar_actual(request),
        "elegir_lugar": "lugar" not in request.session,
    }


def inicio(request, zona_id=None):
    """Pantalla del mapa (funcionalidad corazón): mapa de Santiago y detalle de la zona elegida."""
    zonas = list(Zona.objects.all())
    texto = request.GET.get("q", "").strip()
    resultado = buscar(texto, zonas)

    zona = None
    if zona_id is not None:
        zona = get_object_or_404(Zona, pk=zona_id)
    elif len(resultado["zonas"]) == 1:
        # Si la búsqueda encontró una sola zona, la mostramos directamente.
        zona = resultado["zonas"][0]

    contexto = contexto_base(request, "mapa")
    contexto.update({
        "texto": texto,
        "resultado": resultado,
        "zona": zona,
        "zonas_mapa": [
            {
                "id": z.pk,
                "nombre": z.nombre,
                "comuna": z.comuna,
                "lat": z.latitud,
                "lng": z.longitud,
                "nivel": z.nivel,
                "titulo": z.titulo,
                "url": reverse("mapa:zona", args=[z.pk]) + "#detalle",
            }
            for z in zonas
        ],
        "resaltadas": [z.pk for z in resultado["zonas"]],
        "contorno": CONTORNO_SANTIAGO,
        "cuantas": {
            "si": sum(z.nivel == "si" for z in zonas),
            "ojo": sum(z.nivel == "ojo" for z in zonas),
            "no": sum(z.nivel == "no" for z in zonas),
        },
    })
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

    contexto = contexto_base(request, "comentarios")
    contexto.update({
        "form": form,
        "tipos": [
            {"valor": valor, "nombre": nombre, "dibujo": Comentario.DIBUJOS[valor][0],
             "nivel": Comentario.DIBUJOS[valor][1]}
            for valor, nombre in Comentario.TIPOS
        ],
        "zonas": ordenar_por_cercania(list(Zona.objects.all()), contexto["lugar"]),
        "elegido_tipo": form["tipo"].value() or "",
        "elegida_zona": str(form["zona"].value() or ""),
        "comentarios": Comentario.objects.select_related("zona")[:30],
    })
    return render(request, "mapa/comentarios.html", contexto)


def lugar(request):
    """Elegir dónde está la persona: con el GPS, tocando su comuna o escribiendo un lugar."""
    todas = list(Zona.objects.all())
    comunas = lugares(todas)
    aviso = None
    texto = ""

    if request.method == "POST":
        if request.POST.get("todo"):
            return guardar_lugar(request, CENTRO_SANTIAGO)
        if request.POST.get("comuna"):
            for c in comunas:
                if c["nombre"] == request.POST["comuna"]:
                    return guardar_lugar(request, c)
        if request.POST.get("lat") and request.POST.get("lon"):
            try:
                lat, lon = float(request.POST["lat"]), float(request.POST["lon"])
            except ValueError:
                lat = lon = None
            if lat is not None and dentro_de_santiago(lat, lon):
                return guardar_lugar(request, {"nombre": "Donde estás ahora", "lat": lat, "lon": lon})
            aviso = {"tipo": "fuera_gps"}
    else:
        texto = request.GET.get("q", "").strip()
        resultado = buscar(texto, todas)
        if resultado["tipo"] == "santiago":
            return guardar_lugar(request, CENTRO_SANTIAGO)
        if resultado["tipo"] == "zonas":
            nombres = {z.comuna for z in resultado["zonas"]}
            if len(nombres) == 1:
                comuna = nombres.pop()
                return guardar_lugar(request, next(c for c in comunas if c["nombre"] == comuna))
        if resultado["tipo"] in ("sin_info", "comuna_sin_datos"):
            aviso = {"tipo": resultado["tipo"]}

    contexto = contexto_base(request, "lugar")
    contexto.update({"comunas": comunas, "aviso": aviso, "texto": texto})
    return render(request, "mapa/lugar.html", contexto)


def guardar_lugar(request, datos):
    request.session["lugar"] = {"nombre": datos["nombre"], "lat": datos["lat"], "lon": datos["lon"]}
    return redirect("mapa:inicio")
