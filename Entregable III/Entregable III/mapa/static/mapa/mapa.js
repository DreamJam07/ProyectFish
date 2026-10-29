// Dibuja el mapa de Santiago con una marca de color por cada zona (funcionalidad corazón).
(function () {
  const leer = (id) => JSON.parse(document.getElementById(id).textContent);
  const zonas = leer("datos-zonas");
  const resaltadas = leer("datos-resaltadas");
  const contorno = leer("datos-contorno");
  const zonaActual = leer("datos-zona-actual");
  const lugar = leer("datos-lugar");

  // Dibujo blanco que va dentro de cada marca: visto bueno, signo de exclamación o cruz.
  const DIBUJO = {
    si: '<path d="M6 12.4l3.6 3.6L18 7.6" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>',
    ojo: '<path d="M12 5.5v8" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><circle cx="12" cy="18" r="1.9" fill="#fff"/>',
    no: '<path d="M7 7l10 10M17 7L7 17" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>',
  };
  const svg = (nivel, tam) =>
    `<svg width="${tam}" height="${tam}" viewBox="0 0 24 24" aria-hidden="true">${DIBUJO[nivel]}</svg>`;

  const mapa = L.map("mapa", { zoomControl: false }).setView([-33.45, -70.66], 9);
  // Mapa de calles parecido a Google Maps (Esri World Street Map, no pide clave).
  // OpenStreetMap y CARTO bloquean o piden clave, por eso no se usan.
  const TESELAS = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}";
  L.tileLayer(TESELAS, {
    maxZoom: 19,
    attribution: "Mapa &copy; Esri",
  }).addTo(mapa);
  mapa.attributionControl.setPrefix(false);

  // Sin internet no llega el mapa de calles: dibujamos uno simple de Santiago
  // (región, ríos y algunas ciudades) para que el mapa nunca quede vacío.
  const prueba = new Image();
  prueba.onerror = dibujarMapaSimple;
  prueba.src = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/9/309/155";

  function dibujarMapaSimple() {
    document.querySelector(".credito").textContent =
      "Mapa simple de Santiago (sin internet no se ven las calles) · ríos y ciudades aproximados";
    const estilo = getComputedStyle(document.documentElement);
    const color = (nombre) => estilo.getPropertyValue(nombre).trim();
    L.polygon(contorno, {
      stroke: false, fillColor: color("--tierra"), fillOpacity: 1, interactive: false,
    }).addTo(mapa);
    const RIOS = [
      // Río Mapocho
      [[-33.33, -70.35], [-33.39, -70.55], [-33.42, -70.60], [-33.432, -70.652], [-33.43, -70.72],
       [-33.45, -70.80], [-33.55, -70.90], [-33.62, -71.00], [-33.70, -71.08]],
      // Río Maipo
      [[-33.90, -70.00], [-33.70, -70.25], [-33.62, -70.36], [-33.59, -70.47], [-33.65, -70.62],
       [-33.70, -70.75], [-33.745, -70.90], [-33.70, -71.08], [-33.68, -71.20], [-33.70, -71.45],
       [-33.75, -71.70]],
    ];
    RIOS.forEach((rio) => L.polyline(rio, {
      color: color("--mar-hondo"), weight: 5, interactive: false,
    }).addTo(mapa));
    const CIUDADES = [
      ["Santiago", -33.45, -70.66], ["Puente Alto", -33.61, -70.58], ["Melipilla", -33.69, -71.21],
      ["Colina", -33.20, -70.67], ["Talagante", -33.66, -70.93], ["Buin", -33.73, -70.74],
      ["San José de Maipo", -33.64, -70.35], ["Tiltil", -33.08, -70.93],
    ];
    CIUDADES.forEach(([nombre, lat, lng]) => L.marker([lat, lng], {
      icon: L.divIcon({ className: "icono-yo", html: `<span class="ciudad">${nombre}</span>` }),
      interactive: false, zIndexOffset: -1000,
    }).addTo(mapa));
  }

  const destacados = [];
  zonas.forEach((z) => {
    const elegida = z.id === zonaActual;
    const resaltada = resaltadas.includes(z.id);
    const clases = ["insignia-zona", "i-z-" + z.nivel];
    if (elegida) clases.push("elegida");
    if (resaltada && !elegida) clases.push("resaltada");

    const marca = L.marker([z.lat, z.lng], {
      icon: L.divIcon({ className: clases.join(" "), html: svg(z.nivel, elegida ? 32 : 23) }),
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

  // "Aquí estás tú": solo si la persona eligió una comuna o usó su ubicación.
  if (lugar && lugar.nombre !== "Todo Santiago") {
    const corto = lugar.nombre === "Donde estás ahora" ? "Tú" : "Tú · " + lugar.nombre;
    L.marker([lugar.lat, lugar.lon], {
      icon: L.divIcon({
        className: "icono-yo",
        html: `<span class="pin-yo"><span class="globo">${corto}</span><span class="punta"></span><span class="bolita"></span></span>`,
      }),
      interactive: false,
    }).addTo(mapa);
  }

  function verTodo() {
    const puntos = zonas.map((z) => [z.lat, z.lng]);
    if (puntos.length) mapa.fitBounds(puntos, { padding: [40, 40] });
  }

  if (destacados.length === 1) {
    mapa.setView(destacados[0], 11);
  } else if (destacados.length > 1) {
    mapa.fitBounds(destacados, { padding: [50, 50] });
  } else {
    verTodo();
  }

  document.getElementById("btn-mas").addEventListener("click", () => mapa.zoomIn());
  document.getElementById("btn-menos").addEventListener("click", () => mapa.zoomOut());
  document.getElementById("btn-todo").addEventListener("click", verTodo);

  // Misma regla que dentro_de_santiago() en busqueda.py.
  function dentroDeSantiago(lat, lng) {
    let dentro = false;
    contorno.forEach(([lat1, lng1], i) => {
      const [lat2, lng2] = contorno[(i + 1) % contorno.length];
      if ((lat1 > lat) !== (lat2 > lat) && lng < lng1 + (lat - lat1) * (lng2 - lng1) / (lat2 - lat1)) {
        dentro = !dentro;
      }
    });
    return dentro;
  }

  // Línea punteada con el borde de Santiago, para que se vea hasta dónde hay datos.
  L.polygon(contorno, {
    color: "#0C6873", weight: 3, dashArray: "8 8", fill: false, interactive: false,
  }).addTo(mapa);

  // Si tocan fuera de Santiago, avisamos que aún no hay información.
  mapa.on("click", (e) => {
    if (!dentroDeSantiago(e.latlng.lat, e.latlng.lng)) {
      L.popup()
        .setLatLng(e.latlng)
        .setContent("<b>Aún no tenemos información de este lugar.</b><br>Por ahora solo hay datos de Santiago.")
        .openOn(mapa);
    }
  });
})();
