from django.db import models


class Zona(models.Model):
    """Cuerpo de agua de Santiago (Región Metropolitana) con su estado de contaminación."""

    ESTADO_SEGURA = "segura"
    ESTADO_PRECAUCION = "precaucion"
    ESTADO_PROHIBIDA = "prohibida"
    ESTADOS = [
        (ESTADO_SEGURA, "Se puede pescar"),
        (ESTADO_PRECAUCION, "Precaución"),
        (ESTADO_PROHIBIDA, "Prohibido pescar"),
    ]

    nombre = models.CharField(max_length=100)
    comuna = models.CharField(max_length=60)
    tipo_cuerpo_agua = models.CharField("tipo de cuerpo de agua", max_length=40)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    tipo_contaminacion = models.CharField(
        "tipo de contaminación", max_length=100, blank=True,
        help_text="Vacío si no se detecta contaminación.",
    )
    ultimo_monitoreo = models.DateField("fecha del último monitoreo")
    descripcion = models.TextField("descripción", blank=True)

    # Palabras e íconos que usa el diseño para cada estado.
    NIVELES = {ESTADO_SEGURA: "si", ESTADO_PRECAUCION: "ojo", ESTADO_PROHIBIDA: "no"}
    TITULOS = {
        ESTADO_SEGURA: "Se puede pescar",
        ESTADO_PRECAUCION: "Pesca con cuidado",
        ESTADO_PROHIBIDA: "No pesques aquí",
    }

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "zonas"

    def __str__(self):
        return f"{self.nombre} ({self.comuna})"

    @property
    def nivel(self):
        """'si', 'ojo' o 'no': define el color y el dibujo de la zona."""
        return self.NIVELES[self.estado]

    @property
    def titulo(self):
        return self.TITULOS[self.estado]


class Comentario(models.Model):
    """Comentario o aviso que deja una persona sobre una zona."""

    TIPOS = [
        ("color", "Agua de color raro"),
        ("aceite", "Mancha de aceite"),
        ("espuma", "Espuma o mal olor"),
        ("peces", "Peces muertos"),
        ("basura", "Basura"),
        ("bien", "Todo bien"),
    ]
    # Dibujo y color de cada tipo (ver templatetags/iconos.py).
    DIBUJOS = {
        "color": ("roja", "no"), "aceite": ("mancha", "no"), "espuma": ("espuma", "ojo"),
        "peces": ("pez", "no"), "basura": ("basura", "ojo"), "bien": ("bien", "si"),
    }

    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name="comentarios")
    tipo = models.CharField("¿qué viste?", max_length=20, choices=TIPOS)
    nombre = models.CharField("tu nombre", max_length=60)
    texto = models.TextField("¿quieres contar algo más?", max_length=500, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.nombre} en {self.zona.nombre}"

    @property
    def dibujo(self):
        return self.DIBUJOS.get(self.tipo, ("persona", "marca"))[0]

    @property
    def nivel(self):
        return self.DIBUJOS.get(self.tipo, ("persona", "marca"))[1]
