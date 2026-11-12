# 🐟 ProyectFish

Prototipo web (Django) para que pescadores y recolectores revisen **si una zona de agua
está contaminada antes de ir a pescar**. Equipo 5, “La sociedad de los poetas vivos”,
IWG400 – Proyecto Inicial.

> 📁 Todo el proyecto Django (la funcionalidad corazón y los comentarios) está en esta carpeta,
> `prototipo-santiago/`. Los comandos de abajo se ejecutan dentro de ella.

> ⚠️ Por ahora la aplicación **solo tiene datos de las regiones de Valparaíso, Metropolitana (Santiago)
> y O'Higgins**. Si se busca otro lugar, la página avisa que todavía no hay información.
> Los estados y fechas de las zonas son **datos de ejemplo**, no información oficial.

## Qué hace

| Funcionalidad | Descripción |
|---|---|
| 🚪 Entrada simple | Se entra directo al mapa, sin preguntar nada. Arriba hay tres botones grandes (Valparaíso, Metropolitana, O'Higgins) que acercan el mapa a esa región, y un buscador para escribir un lugar. |
| ⭐ **Mapa (funcionalidad corazón)** | Mapa de las tres regiones con una marca de color por zona: ✅ verde se puede pescar, ⚠️ amarillo con cuidado, ❌ rojo no pescar. Al tocar una zona se ve un cartel grande con el resultado, el tipo de contaminación, la fecha de la última revisión (con cuántos días hace) y las zonas seguras más cercanas. El borde de cada región se marca con una línea punteada; tocar fuera muestra “Aún no tenemos información”. |
| 🐟 Pescadito | Cada zona muestra un pescadito según la contaminación: pescado sano (agua limpia), medio esqueleto (con cuidado) o esqueleto completo (agua contaminada). |
| 🔍 Búsqueda | Se escribe una comuna, un lugar o una región (ej: `Paine`, `Pichilemu`, `Quintero`, `Región de O'Higgins`). Si el lugar no es de las tres regiones (ej: `Concepción`) aparece el aviso “Todavía no tenemos información”. |
| 💬 **Comentarios (funcionalidad secundaria)** | En 3 pasos con dibujos: ¿qué viste? (agua de color raro, aceite, espuma, peces muertos, basura, todo bien), ¿dónde? y tu nombre (el texto es opcional). Las zonas aparecen agrupadas por región. Se ven en la pantalla Comentarios y en el detalle de cada zona. |

Al final de cada página se avisa que es un prototipo / demo.

El diseño (colores, letras grandes, dibujos, modo oscuro) viene del boceto “Marea Clara”, adaptado a la pesca artesanal (con fondo de pesca y pescadito).

## Cómo correrlo en tu computador

Necesitas **Python 3.10 o más nuevo** y **Git**.

```bash
# 1. Descargar el proyecto
git clone https://github.com/DreamJam07/ProyectFish.git
cd ProyectFish
cd prototipo-santiago

# 2. Crear y activar un entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# 3. Instalar Django
pip install -r requirements.txt

# 4. Crear la base de datos (también carga las 23 zonas de ejemplo de las tres regiones)
python manage.py migrate

# 5. Prender el servidor
python manage.py runserver
```

Abre **http://127.0.0.1:8000/** en el navegador. Para apagar el servidor: `Ctrl + C`.

> Con internet el mapa muestra calles (Esri World Street Map, no necesita clave). Sin internet se dibuja un mapa
> simple (borde de las regiones, ríos y ciudades) y todo lo demás funciona.

### Verla desde el celular (misma red WiFi)

```bash
python manage.py runserver 0.0.0.0:8000
```

Busca la IP del computador (`ipconfig`, línea "Dirección IPv4", por ejemplo `192.168.1.23`) y en el
celular abre `http://192.168.1.23:8000`. Si Windows pregunta por el firewall, permite el acceso en redes privadas.

### Panel de administración (opcional)

Para agregar o cambiar zonas sin tocar código:

```bash
python manage.py createsuperuser
```

Luego entra a **http://127.0.0.1:8000/admin/**.

## Casos de prueba

| | Caso 1 (principal) | Caso 2 (alternativo) |
|---|---|---|
| Entrada | Buscar `Paine` | Buscar `Concepción` |
| Resultado esperado | Se muestra la Laguna de Aculeo en ⚠️ “Pesca con cuidado”, con tipo de contaminación, fecha de la última revisión y zonas seguras cercanas. | Aviso: “Todavía no tenemos información de Concepción. Por ahora solo hay datos de las regiones de Valparaíso, Metropolitana y O'Higgins.” |

Otros datos para probar: `Santiago` (todas las zonas de la Región Metropolitana), `Quintero` (zona prohibida),
`Pichilemu` (zonas seguras en O'Higgins), `Región de Valparaíso` (todas sus zonas) y `Maipú` o `Rengo`
(comunas sin zonas revisadas).

Las pruebas automáticas se corren con:

```bash
python manage.py test
```

## Estructura

```
proyectfish/          configuración de Django (settings, urls)
mapa/
  models.py           Zona y Comentario
  busqueda.py         decide si una búsqueda está en las tres regiones o no; contornos; zonas seguras cercanas
  views.py            pantallas: mapa, zonas, comentarios y elegir lugar
  migrations/0002_…   datos precargados de las zonas de ejemplo (0002 Santiago, 0004 Valparaíso y O'Higgins)
  templatetags/       dibujos (íconos SVG) usados en las páginas
  templates/mapa/     páginas HTML (base.html tiene la cabecera y el menú)
  static/mapa/        estilos, mapa.js, app.js y la librería Leaflet
  tests.py            pruebas automáticas
```
