from django.test import TestCase
from django.urls import reverse

from .busqueda import normalizar
from .models import Comentario, Zona


class BusquedaTests(TestCase):
    """Las zonas de Santiago vienen precargadas por la migración 0002."""

    def test_normalizar_quita_tildes_y_mayusculas(self):
        self.assertEqual(normalizar("  Maipú "), "maipu")

    def test_caso_1_buscar_zona_de_santiago_muestra_su_estado(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "Paine"})
        self.assertContains(respuesta, "Laguna de Aculeo")
        self.assertContains(respuesta, "Pesca con cuidado")
        self.assertContains(respuesta, "Mejor ve a estas zonas")

    def test_caso_2_lugar_fuera_de_santiago_avisa_que_no_hay_info(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "Valparaíso"})
        self.assertContains(respuesta, "Todavía no tenemos información")
        self.assertContains(respuesta, "solo tiene datos de")

    def test_comuna_de_santiago_sin_zonas(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "Maipu"})
        self.assertContains(respuesta, "aún no tiene zonas revisadas")

    def test_buscar_santiago_muestra_todas_las_zonas(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "santiago"})
        self.assertEqual(len(respuesta.context["resultado"]["zonas"]), Zona.objects.count())


class LugarTests(TestCase):
    def test_primera_visita_pregunta_donde_estas(self):
        respuesta = self.client.get(reverse("mapa:inicio"))
        self.assertContains(respuesta, "¿Dónde estás?")

    def test_elegir_comuna_la_guarda_y_ordena_zonas_en_comentarios(self):
        self.client.post(reverse("mapa:lugar"), {"comuna": "Tiltil"})
        respuesta = self.client.get(reverse("mapa:comentarios"))
        self.assertContains(respuesta, "Tiltil")
        self.assertNotContains(respuesta, 'id="telon"')
        self.assertEqual(respuesta.context["zonas"][0].nombre, "Embalse Rungue")

    def test_ubicacion_fuera_de_santiago_avisa_que_no_hay_info(self):
        # Coordenadas de Valparaíso.
        respuesta = self.client.post(reverse("mapa:lugar"), {"lat": "-33.04", "lon": "-71.61"})
        self.assertContains(respuesta, "Estás fuera de Santiago")
        self.assertNotIn("lugar", self.client.session)

    def test_ubicacion_dentro_de_santiago_se_guarda(self):
        self.client.post(reverse("mapa:lugar"), {"lat": "-33.45", "lon": "-70.66"})
        self.assertEqual(self.client.session["lugar"]["nombre"], "Donde estás ahora")

    def test_escribir_lugar_fuera_de_santiago(self):
        respuesta = self.client.get(reverse("mapa:lugar"), {"q": "Concepción"})
        self.assertContains(respuesta, "Todavía no tenemos información")


class PantallasTests(TestCase):
    def test_no_hay_pantalla_de_zonas_ni_boton_escuchar(self):
        self.assertEqual(self.client.get("/zonas/").status_code, 404)
        respuesta = self.client.get(reverse("mapa:inicio"))
        self.assertNotContains(respuesta, "Escuchar")
        self.assertNotContains(respuesta, ">Zonas<")

    def test_aviso_de_prototipo_abajo(self):
        respuesta = self.client.get(reverse("mapa:inicio"))
        self.assertContains(respuesta, "Prototipo / demo")

    def test_zona_muestra_fecha_de_ultima_revision(self):
        zona = Zona.objects.get(nombre="Laguna de Aculeo")
        respuesta = self.client.get(reverse("mapa:zona", args=[zona.pk]))
        self.assertContains(respuesta, "Así estaba el agua el 5 de octubre de 2026")


class ComentarioTests(TestCase):
    def setUp(self):
        self.zona = Zona.objects.get(nombre="Embalse El Yeso")

    def test_publicar_comentario(self):
        datos = {"tipo": "bien", "zona": self.zona.pk, "nombre": "Juan", "texto": "Agua limpia hoy."}
        respuesta = self.client.post(reverse("mapa:comentarios"), datos, follow=True)
        self.assertEqual(Comentario.objects.filter(zona=self.zona).count(), 1)
        self.assertContains(respuesta, "Agua limpia hoy.")
        self.assertContains(respuesta, "Tu comentario fue publicado")

    def test_comentario_sin_texto_se_puede_publicar(self):
        datos = {"tipo": "peces", "zona": self.zona.pk, "nombre": "Ana"}
        self.client.post(reverse("mapa:comentarios"), datos)
        self.assertEqual(Comentario.objects.get().get_tipo_display(), "Peces muertos")

    def test_comentario_vacio_muestra_error(self):
        respuesta = self.client.post(reverse("mapa:comentarios"), {"nombre": ""})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Comentario.objects.count(), 0)
        self.assertContains(respuesta, "Toca un dibujo para decir qué viste")

    def test_comentario_se_ve_en_la_zona(self):
        Comentario.objects.create(zona=self.zona, tipo="basura", nombre="Rosa", texto="Bolsas en la orilla")
        respuesta = self.client.get(reverse("mapa:zona", args=[self.zona.pk]))
        self.assertContains(respuesta, "Bolsas en la orilla")
