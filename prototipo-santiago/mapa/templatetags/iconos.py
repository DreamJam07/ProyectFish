"""Dibujos simples (SVG) para que la página se entienda sin tener que leer mucho."""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Colores por nivel: si = verde, ojo = amarillo, no = rojo.
COLORES = {
    "si": "var(--si)", "ojo": "var(--ojo)", "no": "var(--no)",
    "marca": "var(--marca)", "suave": "var(--tinta-2)", "fondo": "var(--superficie)",
    "actual": "currentColor",
}

DIBUJOS = {
    "si": '<circle cx="12" cy="12" r="10" fill="{c}"/><path d="M7 12.4l3.4 3.4L17 8.8" fill="none" stroke="{i}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    "ojo": '<path d="M12 3l10 18H2z" fill="{c}"/><path d="M12 10v4.6" stroke="{i}" stroke-width="2.6" stroke-linecap="round"/><circle cx="12" cy="18" r="1.5" fill="{i}"/>',
    "no": '<circle cx="12" cy="12" r="10" fill="{c}"/><path d="M8 8l8 8M16 8l-8 8" fill="none" stroke="{i}" stroke-width="2.8" stroke-linecap="round"/>',
    "agua": '<path d="M12 3c4 5.5 6.5 8.7 6.5 11.6A6.5 6.5 0 015.5 14.6C5.5 11.7 8 8.5 12 3z" fill="{c}"/>',
    "reloj": '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M12 6.5V12l4 2.4" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    "pin": '<path d="M12 22s8-7.4 8-12.6A8 8 0 004 9.4C4 14.6 12 22 12 22z" fill="{c}"/><circle cx="12" cy="9.4" r="3.2" fill="{i}"/>',
    "altavoz": '<path d="M4 9h4l5-4v14l-5-4H4z" fill="{c}"/><path d="M17 8.5a5 5 0 010 7M19.6 6a9 9 0 010 12" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>',
    "pez": '<path d="M2 12c4-6 11-6 15 0-4 6-11 6-15 0z" fill="{c}"/><path d="M17 12l5-4v8z" fill="{c}"/><circle cx="7" cy="11" r="1.3" fill="{i}"/>',
    "mancha": '<path d="M4 15c0-4 3-4 4-7s6-4 8 0 4 3 4 7-4 5-8 5-8-1-8-5z" fill="{c}"/>',
    "espuma": '<circle cx="8" cy="10" r="4" fill="{c}"/><circle cx="15" cy="8.5" r="3" fill="{c}"/><circle cx="17" cy="13" r="4" fill="{c}"/><path d="M3 18h18" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>',
    "basura": '<path d="M5 7h14l-1.4 13H6.4z" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/><path d="M3 7h18M9.5 4.5h5" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>',
    "roja": '<circle cx="12" cy="12" r="9" fill="{c}"/><path d="M6 13.5c2.4 0 2.4-2.4 4.8-2.4S13.2 13.5 15.6 13.5 18 11.1 18 11.1" fill="none" stroke="{i}" stroke-width="2.2" stroke-linecap="round"/>',
    "bien": '<circle cx="12" cy="12" r="9" fill="{c}"/><path d="M8.4 13.6c1.8 2.2 5.4 2.2 7.2 0" fill="none" stroke="{i}" stroke-width="2.2" stroke-linecap="round"/><circle cx="9" cy="9.6" r="1.3" fill="{i}"/><circle cx="15" cy="9.6" r="1.3" fill="{i}"/>',
    "persona": '<circle cx="12" cy="8" r="4" fill="{c}"/><path d="M4.5 20c1.4-4 4-6 7.5-6s6.1 2 7.5 6z" fill="{c}"/>',
    "lista": '<path d="M4 7h16M4 12h16M4 17h16" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>',
    "mapa": '<path d="M9 4L4 6v14l5-2 6 2 5-2V4l-5 2-6-2z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M9 4v14M15 6v14" stroke="{c}" stroke-width="2"/>',
    "globo": '<path d="M4 5h16v11H9l-5 4z" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "lupa": '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="{c}" stroke-width="2.4"/><path d="M15.5 15.5L21 21" stroke="{c}" stroke-width="2.6" stroke-linecap="round"/>',
    "check": '<path d="M4 12l5 5L20 6" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "atras": '<path d="M14 6l-6 6 6 6" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "cerro": '<path d="M2 20l7-11 4 6 3-4 6 9z" fill="{c}"/>',
}


@register.simple_tag
def icono(nombre, tam=28, color="actual", interior="fondo"):
    """Uso: {% icono "si" 40 "si" %} -> círculo verde con un visto bueno."""
    c = COLORES.get(color, color)
    i = COLORES.get(interior, interior)
    trazo = DIBUJOS.get(nombre, "").format(c=c, i=i)
    return mark_safe(
        f'<svg width="{tam}" height="{tam}" viewBox="0 0 24 24" aria-hidden="true">{trazo}</svg>'
    )


@register.filter
def hace(fecha):
    """'recién' si fue hace menos de un minuto; si no, 'hace 3 horas', etc."""
    from django.utils import timezone
    from django.utils.timesince import timesince

    if (timezone.now() - fecha).total_seconds() < 60:
        return "recién"
    return "hace " + timesince(fecha).split(",")[0]


@register.filter
def hace_dias(fecha):
    """'hoy', 'ayer' o 'hace 17 días' para una fecha (sin hora)."""
    from django.utils import timezone

    dias = (timezone.localdate() - fecha).days
    if dias <= 0:
        return "hoy"
    if dias == 1:
        return "ayer"
    return f"hace {dias} días"


# ---------- Pescadito: cuánta contaminación hay ----------
_PEZ_CUERPO = (
    '<path d="M6 16c5-9 18-10 27-1 6-2 12-1 15 3-3 4-9 5-15 3-9 8-22 7-27-2z" '
    'fill="#4FB3D9" stroke="#1B6E94" stroke-width="1.6" stroke-linejoin="round"/>'
    '<path d="M40 14l9-6v9z" fill="#2E94BD" stroke="#1B6E94" stroke-width="1.4" stroke-linejoin="round"/>'
    '<path d="M24 14c3-5 8-6 11-4-1 3-5 5-9 5z" fill="#2E94BD"/>'
    '<path d="M13 18c3 4 8 6 15 6-3 2-9 2-15-1z" fill="#CDEBF5"/>'
    '<path d="M14 11.5c-1.2 3-1.2 7 0 10" fill="none" stroke="#1B6E94" stroke-width="1.4" stroke-linecap="round"/>'
    '<circle cx="10" cy="15" r="2.4" fill="#fff"/><circle cx="9.6" cy="15" r="1.2" fill="#0A1F27"/>'
)
_PEZ_HUESOS = (
    '<g fill="none" stroke="#5A6B73" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M16 17h26"/>'
    '<path d="M20 17c-1-5 0-8 1-9M20 17c-1 5 0 8 1 9"/>'
    '<path d="M25 17c-1-6 0-9 1-10M25 17c-1 6 0 9 1 10"/>'
    '<path d="M30 17c-1-6 0-8 1-9M30 17c-1 6 0 8 1 9"/>'
    '<path d="M35 17c-1-4 0-6 1-7M35 17c-1 4 0 6 1 7"/>'
    '<path d="M42 17l8-6M42 17l8 6M44 17h6"/></g>'
    '<path d="M5 15c0-4 5-7 10-5 2 1 3 4 3 6s-1 5-3 6c-5 2-10-1-10-5z" fill="#fff" stroke="#5A6B73" stroke-width="2"/>'
    '<circle cx="10" cy="14.5" r="2.6" fill="#5A6B73"/><circle cx="10.3" cy="14.2" r=".8" fill="#fff"/>'
    '<path d="M6 19l7 1" stroke="#5A6B73" stroke-width="1.6" stroke-linecap="round"/>'
)

PECES = {
    "sano": _PEZ_CUERPO,
    "esqueleto": _PEZ_HUESOS,
    # Mitad con carne (la cabeza) y mitad con huesos (la cola).
    "medio": (
        '<defs><clipPath id="pez-carne"><rect x="0" y="0" width="27" height="34"/></clipPath>'
        '<clipPath id="pez-huesos"><rect x="27" y="0" width="30" height="34"/></clipPath></defs>'
        f'<g clip-path="url(#pez-carne)">{_PEZ_CUERPO}</g>'
        f'<g clip-path="url(#pez-huesos)">{_PEZ_HUESOS}</g>'
    ),
}

NOMBRES_PEZ = {
    "sano": "Pescado sano: agua limpia",
    "medio": "Pescado a medias: contaminación media",
    "esqueleto": "Esqueleto de pescado: agua muy contaminada",
}


@register.simple_tag
def pescadito(estado, ancho=120):
    """Dibujo del pescadito según la contaminación: 'sano', 'medio' o 'esqueleto'."""
    alto = round(ancho * 34 / 56)
    return mark_safe(
        f'<svg width="{ancho}" height="{alto}" viewBox="0 0 56 34" role="img" '
        f'aria-label="{NOMBRES_PEZ[estado]}">{PECES[estado]}</svg>'
    )


@register.simple_tag
def pescadito_logo():
    """Pez del logo (el mismo pescadito sano, solo el dibujo interior)."""
    return mark_safe(_PEZ_CUERPO)
