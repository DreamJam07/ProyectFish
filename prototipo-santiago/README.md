ProyectFish

Prototipo web (Django) para que pescadores y recolectores revisen **si una zona de agua
está contaminada antes de ir a pescar**. Equipo 5, “La sociedad de los poetas vivos”

Por ahora la aplicación *solo tiene datos de Santiago (Región Metropolitana)*.
> Si se busca otro lugar, la página avisa que todavía no hay información.
> Los estados y fechas de las zonas son **datos de ejemplo**, no información oficial.

## ¿Qué hace?

| Funcionalidad | Descripción |
|---|---|
|  ¿Dónde estás? | La primera vez se pregunta dónde está la persona: con la ubicación del teléfono, eligiendo su comuna o viendo todo Santiago. Si la ubicación o el lugar escrito está fuera de Santiago, se avisa que todavía no hay información. |
|  **Mapa (funcionalidad corazón)** | Mapa de Santiago con una marca de color por zona: ✅ verde se puede pescar, ⚠️ amarillo con cuidado, ❌ rojo no pescar. Al tocar una zona se ve un cartel grande con el resultado, el tipo de contaminación, la fecha de la última revisión (con cuántos días hace), las zonas seguras más cercanas. El borde de Santiago se marca con una línea punteada; tocar fuera muestra “Aún no tenemos información”. |
|  Búsqueda | Se escribe una comuna o un lugar (ej: `Paine`, `Laguna Carén`, `Santiago`). Si el lugar no es de Santiago (ej: `Valparaíso`) aparece el aviso “Todavía no tenemos información”. |
|  **Comentarios (funcionalidad secundaria)** | En 3 pasos con dibujos: ¿qué viste? (agua de color raro, aceite, espuma, peces muertos, basura, todo bien), ¿dónde? y tu nombre (el texto es opcional). Se ven en la pantalla Comentarios y en el detalle de cada zona. |

Al final de cada página se avisa que es un prototipo / demo.

El diseño (colores, letras grandes, dibujos, modo oscuro) viene del boceto “Marea Clara”, adaptado a Santiago.

## Cómo correrlo en tu computador

Necesitas **Python 3.10 o más nuevo** y **Git**.

```bash
# 1. Descargar el proyecto
git clone https://github.com/DreamJam07/ProyectFish.git
cd ProyectFish

# 2. Crear y activar un entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# 3. Instalar Django
pip install -r requirements.txt

# 4. Crear la base de datos (también carga las 10 zonas de Santiago)
python manage.py migrate

# 5. Prender el servidor
python manage.py runserver
```

Abre **http://127.0.0.1:8000/** en el navegador. Para apagar el servidor: `Ctrl + C`.

> Con internet el mapa muestra calles (Esri World Street Map, no necesita clave). Sin internet se dibuja un mapa
> simple de Santiago (borde, ríos Mapocho y Maipo, ciudades) y todo lo demás funciona.

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
| Entrada | Buscar `Paine` | Buscar `Valparaíso` |
| Resultado esperado | Se muestra la Laguna de Aculeo en ⚠️ “Pesca con cuidado”, con tipo de contaminación, fecha de la última revisión y zonas seguras cercanas. | Aviso: “Todavía no tenemos información de Valparaíso. Por ahora solo hay datos de Santiago.” |

Otros datos para probar: `Santiago` (todas las zonas), `Tiltil` (zona prohibida),
`San José de Maipo` (varias zonas seguras), `Maipú` (comuna de Santiago sin zonas revisadas).

Las pruebas automáticas se corren con:

```bash
python manage.py test
```

## Estructura

```
proyectfish/          configuración de Django (settings, urls)
mapa/
  models.py           Zona y Comentario
  busqueda.py         decide si una búsqueda es de Santiago o no; zonas seguras cercanas
  views.py            pantallas: mapa, zonas, comentarios y elegir lugar
  migrations/0002_…   datos precargados de las zonas de Santiago
  templatetags/       dibujos (íconos SVG) usados en las páginas
  templates/mapa/     páginas HTML (base.html tiene la cabecera y el menú)
  static/mapa/        estilos, mapa.js, app.js y la librería Leaflet
  tests.py            pruebas automáticas
```
