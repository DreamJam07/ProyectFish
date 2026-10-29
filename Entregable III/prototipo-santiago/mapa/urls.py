from django.urls import path

from . import views

app_name = "mapa"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("zona/<int:zona_id>/", views.inicio, name="zona"),
    path("comentarios/", views.comentarios, name="comentarios"),
    path("lugar/", views.lugar, name="lugar"),
]
