// Funciones comunes a todas las pantallas.
(function () {
  // "Usar mi ubicación": pide la ubicación al teléfono y la manda al servidor.
  // El servidor revisa si está dentro de Santiago.
  const botonGps = document.getElementById("btn-gps");
  if (botonGps) {
    const elegirAMano = () => { window.location.href = botonGps.form.action + "#comunas"; };
    botonGps.addEventListener("click", () => {
      if (!navigator.geolocation) return elegirAMano();
      document.getElementById("buscando").hidden = false;
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          botonGps.form.lat.value = pos.coords.latitude;
          botonGps.form.lon.value = pos.coords.longitude;
          botonGps.form.submit();
        },
        elegirAMano,
        { timeout: 8000 }
      );
    });
  }
})();
