from django.contrib import admin

from .models import Comentario, Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "region", "comuna", "estado", "tipo_contaminacion", "ultimo_monitoreo"]
    list_filter = ["region", "estado", "comuna"]
    search_fields = ["nombre", "comuna"]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "zona", "fecha"]
    list_filter = ["zona"]
