# ProyectFish

Prototipo web (Django) para que pescadores y recolectores revisen **si una zona de agua está contaminada antes de ir a pescar**. Equipo 5, “La sociedad de los poetas vivos”.

Por ahora la aplicación *solo tiene datos de Santiago (Región Metropolitana)*.
Si se busca otro lugar, la página avisa que todavía no hay información. Los estados y fechas de las zonas son **datos de ejemplo**, no información oficial.

## ¿Qué hace?

| Funcionalidad | Descripción |
|---|---|
| ¿Dónde estás? | La primera vez se pregunta dónde está la persona: con la ubicación del teléfono, eligiendo su comuna o viendo todo Santiago. Si la ubicación o el lugar escrito está fuera de Santiago, se avisa que todavía no hay información. |
| **Mapa (funcionalidad corazón)** | Mapa de Santiago con una marca de color por zona: ✅ verde se puede pescar, ⚠️ amarillo con cuidado, ❌ rojo no pescar. Al tocar una zona se ve un cartel grande con el resultado, el tipo de contaminación, la fecha de la última revisión (con cuántos días hace) y las zonas seguras más cercanas. El borde de Santiago se marca con una línea punteada; tocar fuera muestra “Aún no tenemos información”. |
| Búsqueda | Se escribe una comuna o un lugar (ej.: `Paine`, `Laguna Carén`, `Santiago`). Si el lugar no es de Santiago (ej.: `Valparaíso`), aparece el aviso “Todavía no tenemos información”. |
| **Comentarios (funcionalidad secundaria)** | En 3 pasos con dibujos: ¿qué viste? (agua de color raro, aceite, espuma, peces muertos, basura, todo bien), ¿dónde? y tu nombre (el texto es opcional). Se ven en la pantalla Comentarios y en el detalle de cada zona. |

Al final de cada página se avisa que es un prototipo/demo.
El diseño (colores, letras grandes, dibujos y modo oscuro) viene del boceto “Marea Clara”, adaptado a Santiago.

## Cómo correrlo en tu computador

Necesitas **Python** y **Git** instalados.

> **Importante para ayudantes en Windows:** no se debe clonar el proyecto dentro de `C:\Windows\System32`, porque esa carpeta está protegida. Se recomienda usar el Escritorio, Documentos u otra carpeta del usuario.

### 1. Abrir PowerShell en una carpeta con permisos

Ejemplo usando una carpeta llamada `carpeta51` en el Escritorio:

```powershell
cd $HOME\Desktop\carpeta51
```

Si la carpeta todavía no existe:

```powershell
mkdir $HOME\Desktop\carpeta51
cd $HOME\Desktop\carpeta51
```

La consola debería quedar en una ruta parecida a:

```text
PS C:\Users\nombre_usuario\Desktop\carpeta51>
```

### 2. Descargar el proyecto

Ejecutar cada comando por separado:

```powershell
git clone https://github.com/DreamJam07/ProyectFish.git
cd ProyectFish
```

El proyecto Django está dentro de la subcarpeta `prototipo-santiago`, por lo que también se debe ejecutar:

```powershell
cd prototipo-santiago
```

Para comprobar que se está en la carpeta correcta:

```powershell
dir
```

Deben aparecer, entre otros, estos elementos:

```text
manage.py
requirements.txt
mapa
proyectfish
```

### 3. Crear el entorno virtual

El entorno virtual se creará en la carpeta superior del repositorio:

```powershell
python -m venv ..\venv
```

#### Opción recomendada en Windows PowerShell

Para evitar el error *“la ejecución de scripts está deshabilitada en este sistema”*, no es obligatorio activar el entorno. Se puede usar directamente su Python:

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Todos los siguientes comandos de Windows usan `..\venv\Scripts\python.exe` porque el entorno `venv` está un nivel arriba de `prototipo-santiago`.

#### Opción alternativa: activar el entorno virtual

Si PowerShell permite ejecutar scripts:

```powershell
..\venv\Scripts\Activate.ps1
```

Si aparece el error de ejecución de scripts, se puede continuar con la opción recomendada anterior. No es necesario cambiar las políticas de seguridad del computador.

#### Mac/Linux

Desde la carpeta `ProyectFish`, crear y activar el entorno antes de entrar a `prototipo-santiago`:

```bash
python3 -m venv venv
source venv/bin/activate
cd prototipo-santiago
pip install -r requirements.txt
```

### 4. Instalar las dependencias

En Windows PowerShell, estando dentro de `ProyectFish\prototipo-santiago`:

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Crear la base de datos

Este comando también carga las 10 zonas de ejemplo de Santiago:

```powershell
..\venv\Scripts\python.exe manage.py migrate
```

Si funciona correctamente, las migraciones terminarán mostrando `OK`.

### 6. Prender el servidor

```powershell
..\venv\Scripts\python.exe manage.py runserver
```

Cuando aparezca un mensaje similar a este:

```text
Starting WSGI development server at http://127.0.0.1:8000/
```

abrir en el navegador:

**http://127.0.0.1:8000/**

Para apagar el servidor, volver a PowerShell y presionar:

```text
Ctrl + C
```

> La advertencia que indica que es un servidor de desarrollo es normal para esta demostración.

Con internet, el mapa muestra calles mediante Esri World Street Map y no necesita clave. Sin internet, se dibuja un mapa simple de Santiago (borde, ríos Mapocho y Maipo, ciudades) y el resto continúa funcionando.

### Ejecuciones futuras

Después de completar la instalación una vez, no es necesario repetir todos los pasos. En Windows basta con ejecutar:

```powershell
cd $HOME\Desktop\carpeta51\ProyectFish\prototipo-santiago
..\venv\Scripts\python.exe manage.py runserver
```

## Verla desde el celular (misma red WiFi)

Detener primero el servidor con `Ctrl + C` y volver a iniciarlo con:

```powershell
..\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

En otra ventana de PowerShell, buscar la IP del computador:

```powershell
ipconfig
```

Localizar la línea **Dirección IPv4**, por ejemplo:

```text
192.168.1.23
```

En el celular, conectado a la misma red WiFi, abrir:

```text
http://192.168.1.23:8000
```

Si Windows pregunta por el firewall, permitir el acceso en redes privadas.

## Panel de administración (opcional)

Para agregar o cambiar zonas sin tocar código:

```powershell
..\venv\Scripts\python.exe manage.py createsuperuser
```

Luego entrar en:

**http://127.0.0.1:8000/admin/**

## Casos de prueba

|  | Caso 1 (principal) | Caso 2 (alternativo) |
|---|---|---|
| Entrada | Buscar `Paine` | Buscar `Valparaíso` |
| Resultado esperado | Se muestra la Laguna de Aculeo en ⚠️ “Pesca con cuidado”, con tipo de contaminación, fecha de la última revisión y zonas seguras cercanas. | Aviso: “Todavía no tenemos información de Valparaíso. Por ahora solo hay datos de Santiago”. |

Otros datos para probar:

- `Santiago`: muestra todas las zonas.
- `Tiltil`: muestra una zona prohibida.
- `San José de Maipo`: muestra varias zonas seguras.
- `Maipú`: comuna de Santiago sin zonas revisadas.

Las pruebas automáticas se ejecutan, desde `prototipo-santiago`, con:

```powershell
..\venv\Scripts\python.exe manage.py test
```

## Estructura

```text
ProyectFish/
├── Entregable III/
├── extra/
├── venv/                       entorno virtual local (se crea al instalar)
└── prototipo-santiago/         carpeta desde la que se ejecuta Django
    ├── manage.py
    ├── requirements.txt
    ├── proyectfish/            configuración de Django (settings, urls)
    └── mapa/
        ├── models.py           Zona y Comentario
        ├── busqueda.py         búsquedas de Santiago y zonas seguras cercanas
        ├── views.py            mapa, zonas, comentarios y elección de lugar
        ├── migrations/         estructura y datos precargados de Santiago
        ├── templatetags/       dibujos e íconos SVG usados en las páginas
        ├── templates/mapa/     páginas HTML
        ├── static/mapa/        estilos, mapa.js, app.js y Leaflet
        └── tests.py            pruebas automáticas
```

## Problemas comunes

### `Permission denied` al usar `git clone`

Se está intentando clonar en una carpeta protegida, como `C:\Windows\System32`. Cambiarse al Escritorio o a Documentos antes de ejecutar `git clone`.

### PowerShell indica que la ejecución de scripts está deshabilitada

No es necesario activar el entorno. Usar directamente:

```powershell
..\venv\Scripts\python.exe manage.py runserver
```

### No se encuentra `requirements.txt`

Probablemente la consola está en `ProyectFish` y no en la subcarpeta del proyecto Django. Ejecutar:

```powershell
cd prototipo-santiago
```

Luego comprobar con `dir` que aparezcan `manage.py` y `requirements.txt`.

### `No module named django`

Instalar las dependencias desde `prototipo-santiago`:

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```
