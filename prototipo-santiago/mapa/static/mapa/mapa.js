// Dibuja el mapa de las regiones de Valparaíso, Metropolitana y O'Higgins con una marca de color
// por cada zona (funcionalidad corazón).
(function () {
  const leer = (id) => JSON.parse(document.getElementById(id).textContent);
  const zonas = leer("datos-zonas");
  const resaltadas = leer("datos-resaltadas");
  const contornos = leer("datos-contornos"); // { región: [[lat, lng], ...] }
  const peces = leer("datos-peces"); // { sano|medio|esqueleto: dibujo SVG del pescadito }
  const zonaActual = leer("datos-zona-actual");

  // Cada zona se marca con su pescadito: sano, medio esqueleto o esqueleto completo.
  // Además lleva un círculo de color con ✓ / ! / ✕ para quien no distingue colores.
  const PEZ_DE = { si: "sano", ojo: "medio", no: "esqueleto" };
  const SIMBOLO = {
    si: '<path d="M6 12.4l3.6 3.6L18 7.6" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
    ojo: '<path d="M12 5.5v8" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><circle cx="12" cy="18" r="2" fill="#fff"/>',
    no: '<path d="M7 7l10 10M17 7L7 17" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>',
  };
  let contador = 0;
  function marcaPez(nivel, ancho) {
    // Los clipPath del pez "medio" necesitan un id propio en cada marca.
    const id = "m" + (++contador);
    const dibujo = peces[PEZ_DE[nivel]].replace(/pez-carne/g, id + "c").replace(/pez-huesos/g, id + "h");
    const alto = Math.round(ancho * 34 / 56);
    return `<span class="pez-marca"><svg width="${ancho}" height="${alto}" viewBox="0 0 56 34" aria-hidden="true">${dibujo}</svg>` +
      `<svg class="simbolo" width="22" height="22" viewBox="0 0 24 24" aria-hidden="true">${SIMBOLO[nivel]}</svg></span>`;
  }

  const mapa = L.map("mapa", { zoomControl: false, zoomSnap: 0.5 }).setView([-33.6, -71.0], 8);
  // Mapa de calles parecido a Google Maps (Esri World Street Map, no pide clave).
  // OpenStreetMap y CARTO bloquean o piden clave, por eso no se usan.
  const TESELAS = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}";
  L.tileLayer(TESELAS, {
    maxZoom: 19,
    attribution: "Mapa &copy; Esri",
  }).addTo(mapa);
  mapa.attributionControl.setPrefix(false);

  // Sin internet no llega el mapa de calles: dibujamos uno simple (regiones, ríos y algunas
  // ciudades) para que el mapa nunca quede vacío.
  const prueba = new Image();
  prueba.onerror = dibujarMapaSimple;
  prueba.src = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/9/309/155";

  function dibujarMapaSimple() {
    document.querySelector(".credito").textContent =
      "Mapa simple (sin internet no se ven las calles) · ríos y ciudades aproximados";
    const estilo = getComputedStyle(document.documentElement);
    const color = (nombre) => estilo.getPropertyValue(nombre).trim();
    Object.values(contornos).forEach((puntos) => L.polygon(puntos, {
      stroke: false, fillColor: color("--tierra"), fillOpacity: 1, interactive: false,
    }).addTo(mapa));
    const RIOS = [
      // Río Aconcagua
      [[-32.83, -70.35], [-32.85, -70.60], [-32.88, -70.95], [-32.90, -71.25], [-32.93, -71.52]],
      // Río Mapocho
      [[-33.33, -70.35], [-33.39, -70.55], [-33.42, -70.60], [-33.432, -70.652], [-33.43, -70.72],
       [-33.45, -70.80], [-33.55, -70.90], [-33.62, -71.00], [-33.70, -71.08]],
      // Río Maipo
      [[-33.90, -70.00], [-33.70, -70.25], [-33.62, -70.36], [-33.59, -70.47], [-33.65, -70.62],
       [-33.70, -70.75], [-33.745, -70.90], [-33.70, -71.08], [-33.68, -71.20], [-33.70, -71.45],
       [-33.62, -71.62]],
      // Río Cachapoal
      [[-34.25, -70.40], [-34.17, -70.74], [-34.12, -71.00], [-34.05, -71.35], [-34.07, -71.55]],
      // Río Tinguiririca
      [[-34.70, -70.40], [-34.58, -70.80], [-34.58, -70.99], [-34.40, -71.35], [-34.10, -71.50]],
    ];
    RIOS.forEach((rio) => L.polyline(rio, {
      color: color("--mar-hondo"), weight: 5, interactive: false,
    }).addTo(mapa));
    const CIUDADES = [
      ["Valparaíso", -33.047, -71.613], ["Viña del Mar", -33.02, -71.55], ["Los Andes", -32.83, -70.60],
      ["San Antonio", -33.59, -71.61], ["Santiago", -33.45, -70.66], ["Puente Alto", -33.61, -70.58],
      ["Melipilla", -33.69, -71.21], ["Rancagua", -34.17, -70.74], ["San Fernando", -34.58, -70.99],
      ["Pichilemu", -34.39, -72.00],
    ];
    CIUDADES.forEach(([nombre, lat, lng]) => L.marker([lat, lng], {
      icon: L.divIcon({ className: "icono-yo", html: `<span class="ciudad">${nombre}</span>` }),
      interactive: false, zIndexOffset: -1000,
    }).addTo(mapa));
  }

  // Con el mapa muy lejos los pescaditos se achican para que no se tapen entre sí.
  function ajustarTamano() {
    const z = mapa.getZoom();
    const cont = mapa.getContainer();
    cont.classList.toggle("zoom-lejos", z < 8.5);
    cont.classList.toggle("zoom-medio", z >= 8.5 && z < 10.5);
  }
  mapa.on("zoomend", ajustarTamano);

  const destacados = [];
  zonas.forEach((z) => {
    const elegida = z.id === zonaActual;
    const resaltada = resaltadas.includes(z.id);
    const clases = ["insignia-zona", "i-z-" + z.nivel];
    if (elegida) clases.push("elegida");
    if (resaltada && !elegida) clases.push("resaltada");

    const marca = L.marker([z.lat, z.lng], {
      icon: L.divIcon({ className: clases.join(" "), html: marcaPez(z.nivel, elegida ? 76 : 56), iconSize: null }),
      title: z.nombre + ": " + z.titulo,
      alt: z.nombre + ": " + z.titulo,
      zIndexOffset: elegida ? 1000 : 0,
    }).addTo(mapa);
    marca.on("click", () => { window.location.href = z.url; });

    if (elegida) {
      L.marker([z.lat, z.lng], {
        icon: L.divIcon({ className: "icono-pastilla", html: `<span class="pastilla">${z.nombre}</span>` }),
        interactive: false,
        zIndexOffset: 2000,
      }).addTo(mapa);
    }
    if (elegida || resaltada) destacados.push([z.lat, z.lng]);
  });

  function verTodo() {
    const puntos = zonas.map((z) => [z.lat, z.lng]);
    if (puntos.length) mapa.fitBounds(puntos, { padding: [40, 40] });
  }

  // Botones grandes de región: acercan el mapa a esa región.
  function verRegion(clave) {
    const puntos = zonas.filter((z) => z.region === clave).map((z) => [z.lat, z.lng]);
    if (puntos.length) mapa.fitBounds(puntos, { padding: [50, 50], maxZoom: 10 });
    else if (contornos[clave]) mapa.fitBounds(contornos[clave]);
    document.getElementById("mapa").scrollIntoView({ behavior: "smooth", block: "center" });
  }
  document.querySelectorAll("[data-region]").forEach((boton) => {
    boton.addEventListener("click", () => verRegion(boton.dataset.region));
  });

  if (destacados.length === 1) {
    mapa.setView(destacados[0], 11);
  } else if (destacados.length > 1) {
    mapa.fitBounds(destacados, { padding: [50, 50] });
  } else {
    verTodo();
  }

  ajustarTamano();

  document.getElementById("btn-mas").addEventListener("click", () => mapa.zoomIn());
  document.getElementById("btn-menos").addEventListener("click", () => mapa.zoomOut());
  document.getElementById("btn-todo").addEventListener("click", verTodo);

  // Misma regla que dentro_de_las_regiones() en busqueda.py.
  function dentroDe(puntos, lat, lng) {
    let dentro = false;
    puntos.forEach(([lat1, lng1], i) => {
      const [lat2, lng2] = puntos[(i + 1) % puntos.length];
      if ((lat1 > lat) !== (lat2 > lat) && lng < lng1 + (lat - lat1) * (lng2 - lng1) / (lat2 - lat1)) {
        dentro = !dentro;
      }
    });
    return dentro;
  }
  const dentroDeLasRegiones = (lat, lng) =>
    Object.values(contornos).some((puntos) => dentroDe(puntos, lat, lng));

  // Línea punteada con el borde de cada región, para que se vea hasta dónde hay datos.
  Object.values(contornos).forEach((puntos) => L.polygon(puntos, {
    color: "#0C6873", weight: 3, dashArray: "8 8", fill: false, interactive: false,
  }).addTo(mapa));

  // Si tocan fuera de las regiones, avisamos que aún no hay información.
  mapa.on("click", (e) => {
    if (!dentroDeLasRegiones(e.latlng.lat, e.latlng.lng)) {
      L.popup()
        .setLatLng(e.latlng)
        .setContent("<b>Aún no tenemos información de este lugar.</b><br>Por ahora solo hay datos de las regiones de Valparaíso, Metropolitana y O'Higgins.")
        .openOn(mapa);
    }
  });
})();
