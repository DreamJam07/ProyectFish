from django.test import TestCase
from django.urls import reverse

from .busqueda import dentro_de_las_regiones, normalizar
from .models import Comentario, Zona


class BusquedaTests(TestCase):
    """Las zonas de las tres regiones vienen precargadas por las migraciones 0002 y 0004."""

    def test_normalizar_quita_tildes_apostrofos_y_mayusculas(self):
        self.assertEqual(normalizar("  Maipú "), "maipu")
        self.assertEqual(normalizar("O'Higgins"), "ohiggins")

    def test_caso_1_buscar_zona_muestra_su_estado(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "Paine"})
        self.assertContains(respuesta, "Laguna de Aculeo")
        self.assertContains(respuesta, "Pesca con cuidado")
        self.assertContains(respuesta, "Mejor ve a estas zonas")

    def test_caso_2_lugar_fuera_de_las_regiones_avisa_que_no_hay_info(self):
        respuesta = self.client.get(reverse("mapa:inicio"), {"q": "Concepción"})
        self.assertContains(respuesta, "Todavía no tenemos información")
        self.assertContains(respuesta, "Valparaíso, Metropolitana y O&#x27;Higgins")

    def test_valparaiso_y_ohiggins_ya_tienen_informacion(self):
        for lugar, zona in [("Quintero", "Bahía de Quintero"), ("Pichilemu", "Laguna Cáhuil")]:
            respuesta = self.client.get(reverse("mapa:inicio"), {"q": lugar})
            self.assertNotContains(respuesta, "Todavía no tenemos información")
            nombres = [z.nombre for z in respuesta.context["resultado"]["zonas"]]
            self.assertIn(zona, nombres)

    def test_comuna_de_las_regiones_sin_zonas(self):
        for lugar in ["Maipu", "Viña del Mar", "Rengo"]:
            respuesta = self.client.get(reverse("mapa:inicio"), {"q": lugar})
            self.assertContains(respuesta, "aún no tiene zonas revisadas")

    def test_buscar_una_region_muestra_todas_sus_zonas(self):
        for texto, clave in [("santiago", "metropolitana"), ("Región de O'Higgins", "ohiggins"),
                             ("región de valparaíso", "valparaiso")]:
            respuesta = self.client.get(reverse("mapa:inicio"), {"q": texto})
            zonas = respuesta.context["resultado"]["zonas"]
            self.assertEqual(len(zonas), Zona.objects.filter(region=clave).count())
            self.assertTrue(all(z.region == clave for z in zonas))

    def test_contorno_de_las_regiones(self):
        self.assertTrue(dentro_de_las_regiones(-33.45, -70.66))   # Santiago
        self.assertTrue(dentro_de_las_regiones(-33.04, -71.61))   # Valparaíso
        self.assertTrue(dentro_de_las_regiones(-34.17, -70.74))   # Rancagua
        self.assertFalse(dentro_de_las_regiones(-36.83, -73.05))  # Concepción
        self.assertFalse(dentro_de_las_regiones(-29.91, -71.25))  # La Serena


class PantallasTests(TestCase):
    def test_entrada_simple_sin_elegir_comuna(self):
        respuesta = self.client.get(reverse("mapa:inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "¿Dónde quieres pescar?")
        for region in ["Región de Valparaíso", "Región Metropolitana", "Región de O&#x27;Higgins"]:
            self.assertContains(respuesta, region)
        self.assertNotContains(respuesta, "Yo elijo mi comuna")
        self.assertNotContains(respuesta, "Estás en")
        self.assertEqual(self.client.get("/lugar/").status_code, 404)

    def test_no_hay_pantalla_de_zonas_ni_boton_escuchar(self):
        self.assertEqual(self.client.get("/zonas/").status_code, 404)
        respuesta = self.client.get(reverse("mapa:inicio"))
        self.assertNotContains(respuesta, "Escuchar")
        self.assertNotContains(respuesta, ">Zonas<")

    

    def test_zona_muestra_fecha_de_ultima_revision(self):
        zona = Zona.objects.get(nombre="Laguna de Aculeo")
        respuesta = self.client.get(reverse("mapa:zona", args=[zona.pk]))
        self.assertContains(respuesta, "Así estaba el agua el 5 de octubre de 2026")

    def test_pescadito_segun_la_contaminacion(self):
        casos = {
            "Embalse El Yeso": ("sano", "Pescado sano"),
            "Laguna de Aculeo": ("medio", "Pescado a medias"),
            "Río Mapocho - Centro": ("esqueleto", "Esqueleto de pescado"),
        }
        for nombre, (pez, texto) in casos.items():
            zona = Zona.objects.get(nombre=nombre)
            self.assertEqual(zona.pez, pez)
            respuesta = self.client.get(reverse("mapa:zona", args=[zona.pk]))
            self.assertContains(respuesta, f'aria-label="{texto}')

    def test_cada_zona_tiene_region(self):
        self.assertEqual(
            set(Zona.objects.values_list("region", flat=True)),
            {"valparaiso", "metropolitana", "ohiggins"},
        )


class ComentarioTests(TestCase):
    def setUp(self):
        self.zona = Zona.objects.get(nombre="Embalse El Yeso")

    def test_publicar_comentario(self):
        datos = {"tipo": "bien", "zona": self.zona.pk, "nombre": "Juan", "texto": "Agua limpia hoy."}
        respuesta = self.client.post(reverse("mapa:comentarios"), datos, follow=True)
        self.assertEqual(Comentario.objects.filter(zona=self.zona).count(), 1)
        self.assertContains(respuesta, "Agua limpia hoy.")
        self.assertContains(respuesta, "Tu comentario fue publicado")

    def test_comentar_en_una_zona_de_otra_region(self):
        zona = Zona.objects.get(nombre="Laguna Cáhuil")
        datos = {"tipo": "peces", "zona": zona.pk, "nombre": "Ana"}
        self.client.post(reverse("mapa:comentarios"), datos)
        self.assertEqual(Comentario.objects.get().zona, zona)

    def test_zonas_agrupadas_por_region(self):
        respuesta = self.client.get(reverse("mapa:comentarios"))
        self.assertEqual([g["nombre"] for g in respuesta.context["grupos"]],
                         ["Región de Valparaíso", "Región Metropolitana", "Región de O'Higgins"])

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
