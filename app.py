from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


def render_public_page() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Luis &amp; Verónica — 10 de octubre de 2026</title>
  <meta name="description" content="Acompáñanos a celebrar la boda de Luis y Verónica, el 10 de octubre de 2026 en Guayaquil." />
  <meta property="og:title" content="Luis & Verónica — Nos casamos" />
  <meta property="og:description" content="10 de octubre de 2026 · Guayaquil. Confirma tu asistencia aquí." />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Manrope:wght@300;400;500;600;700&family=Pinyon+Script&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/style.css" />
</head>
<body>
  <div id="welcomeGate" aria-live="polite">
    <div class="welcome-envelope-wrap">
      <div class="welcome-texts">
        <div class="welcome-couple">LUIS &amp; VERÓNICA</div>
        <div class="welcome-invitan">Invitan a:</div>
        <div class="welcome-guest" id="guestNameDisplay">INVITADO</div>
      </div>

      <div class="welcome-envelope" aria-label="Sobre de invitación de boda">
        <div class="envelope-shadow"></div>
        <div class="envelope-back"></div>
        <div class="envelope-flap"></div>
        <div class="envelope-seal"></div>
      </div>

      <div class="wg-tap">Toca para abrir tu invitación</div>
    </div>
  </div>

  <div class="scroll-progress" aria-hidden="true"><span id="scrollProgress"></span></div>

  <section class="hero" style="padding-top:0;max-width:100%;">
    <div class="hero-floral floral-corner floral-top-left floral-slow"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-corner floral-top-right floral-fast"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-side floral-left floral-medium"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-side floral-right floral-slow"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-bottom floral-bottom-left floral-fast"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-bottom floral-bottom-right floral-medium"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-name-left floral-tiny"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-name-right floral-tiny"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-date-left floral-slow"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-date-right floral-fast"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-lower-left floral-medium"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-floral floral-mini floral-lower-right floral-slow"><img src="/images/flores-decoracion.png" alt="" /></div>
    <div class="hero-vine vine-left"></div>
    <div class="hero-vine vine-right"></div>
    <div class="hero-bloom bloom-top-left"></div>
    <div class="hero-bloom bloom-top-right"></div>
    <div class="hero-bloom bloom-name-left"></div>
    <div class="hero-bloom bloom-name-right"></div>
    <div class="hero-bloom bloom-date-left"></div>
    <div class="hero-bloom bloom-date-right"></div>
    <div class="hero-bloom bloom-lower-left"></div>
    <div class="hero-bloom bloom-lower-right"></div>
    <div class="hero-leaf leaf-left-one"></div>
    <div class="hero-leaf leaf-left-two"></div>
    <div class="hero-leaf leaf-right-one"></div>
    <div class="hero-leaf leaf-right-two"></div>
    <div class="hero-leaf leaf-bottom-left"></div>
    <div class="hero-leaf leaf-bottom-right"></div>
    <div class="eyebrow hero-in">Nos casamos</div>
    <h1 class="hero-names hero-in">Luis<span class="amp">&amp;</span>Verónica</h1>
    <div class="hero-sub hero-in">10 · OCTUBRE · 2026 — GUAYAQUIL</div>

    <div class="hero-badges hero-in">
      <div class="hero-badge"><span>10</span> Oct</div>
      <div class="hero-badge"><span>7:30</span> PM</div>
      <div class="hero-badge"><span>Guayaquil</span> Ecuador</div>
    </div>

    <div class="seal hero-in">
      <div class="countdown" id="countdown">
        <div class="cd-unit"><div class="cd-num" id="cd-days">00</div><div class="cd-label">Días</div></div>
        <div class="cd-unit"><div class="cd-num" id="cd-hours">00</div><div class="cd-label">Horas</div></div>
        <div class="cd-unit"><div class="cd-num" id="cd-min">00</div><div class="cd-label">Min</div></div>
        <div class="cd-unit"><div class="cd-num" id="cd-sec">00</div><div class="cd-label">Seg</div></div>
      </div>
    </div>
    <div class="save-date hero-in">Guarda la fecha</div>
  </section>

  <section id="esencia">
    <div class="section-head">
      <div class="eyebrow">Nuestra esencia</div>
      <h2 class="section-title">El viaje hasta este momento</h2>
    </div>
    <div class="story-card reveal">
      <div class="story-text">
        Desde la primera mirada hasta este gran sí, nuestro amor ha crecido en cada
        instante compartido. Una historia silenciosa que hoy se convierte en
        celebración y destino.
      </div>
    </div>
  </section>

  <section id="compromiso">
    <div class="section-head">
      <div class="eyebrow">Un nuevo capítulo comienza</div>
      <h2 class="section-title">Nuestro compromiso</h2>
    </div>
    <div class="story-card story-reverse reveal">
      <div class="story-text">
        Entre pétalos de ternura y ramas que susurran promesas, queremos celebrar
        cada instante junto a ti. Este día es nuestra historia, y tu presencia lo
        hará eterno.
      </div>
    </div>
  </section>

  <section id="itinerario">
    <div class="section-head">
      <div class="eyebrow">La celebración</div>
      <h2 class="section-title">Itinerario</h2>
    </div>
    <div class="timeline-cards">
      <div class="tc-row tc-left tc-reveal" style="transition-delay:0.00s;">
        <div class="tc-card">
          <div class="tc-icon">⛪</div>
          <h3>Misa</h3>
          <span class="tc-time">7:30 PM</span>
          <p>Ceremonia religiosa.</p>
        </div>
        <div class="tc-dot"></div>
        <div class="tc-empty"></div>
      </div>
      <div class="tc-row tc-right tc-reveal" style="transition-delay:0.12s;">
        <div class="tc-empty"></div>
        <div class="tc-dot"></div>
        <div class="tc-card">
          <div class="tc-icon">🥂</div>
          <h3>Recepción</h3>
          <span class="tc-time">9:00 PM</span>
          <p>Casa de los novios.</p>
        </div>
      </div>
      <div class="tc-row tc-left tc-reveal" style="transition-delay:0.24s;">
        <div class="tc-card">
          <div class="tc-icon">💃</div>
          <h3>Baile</h3>
          <span class="tc-time">10:00 PM</span>
          <p>A bailar hasta que el cuerpo aguante.</p>
        </div>
        <div class="tc-dot"></div>
        <div class="tc-empty"></div>
      </div>
      <div class="tc-row tc-right tc-reveal" style="transition-delay:0.36s;">
        <div class="tc-empty"></div>
        <div class="tc-dot"></div>
        <div class="tc-card">
          <div class="tc-icon">🍽️</div>
          <h3>Cena</h3>
          <span class="tc-time">12:00 AM</span>
          <p>Brindis y cena de celebración.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="ubicaciones">
    <div class="section-head">
      <div class="eyebrow">Cómo llegar</div>
      <h2 class="section-title">Ubicaciones</h2>
    </div>
    <div class="letter-page reveal">
      <div class="location-card">
        <div class="loc-label">Ceremonia</div>
        <h3>Iglesia Nuestra Señora de La Consolata</h3>
        <p class="loc-address">Guayaquil</p>
        <div class="loc-actions">
          <a class="btn btn-ghost loc-btn" target="_blank" rel="noopener" href="https://maps.app.goo.gl/o9K2PA2fikoo2BNC6">Abrir en Google Maps</a>
        </div>
        <div class="loc-map">
          <iframe src="https://www.google.com/maps?q=Iglesia+Cat%C3%B3lica+Nuestra+Se%C3%B1ora+de+La+Consolata+Guayaquil&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>

      <div class="location-card">
        <div class="loc-label">Recepción</div>
        <h3>Casa de los novios</h3>
        <p class="loc-address">Guayaquil</p>
        <div class="loc-actions">
          <a class="btn btn-ghost loc-btn" target="_blank" rel="noopener" href="https://maps.app.goo.gl/Cr4bxacg7Rm7yaYM9">Abrir en Google Maps</a>
        </div>
        <div class="loc-map">
          <iframe src="https://www.google.com/maps?q=-2.112769,-79.959674&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  </section>

  <section id="dresscode">
    <div class="section-head">
      <div class="eyebrow">Etiqueta</div>
      <h2 class="section-title">Vestimenta</h2>
    </div>
    <div class="dresscode-grid reveal">
      <div class="dc-card">
        <div class="tc-icon" style="margin:0 auto 12px;">👗</div>
        <h3>Para Ella</h3>
        <p class="dc-label">Colores sugeridos <span class="dc-note">(evita el blanco)</span>:</p>
        <div class="swatches">
          <div class="sw" style="background:#7A4A42"></div>
          <div class="sw" style="background:#B08D4F"></div>
          <div class="sw" style="background:#5B4636"></div>
          <div class="sw" style="background:#8C6A52"></div>
          <div class="sw" style="background:#C41E3A"></div>
          <div class="sw" style="background:#1B3A6B"></div>
          <div class="sw" style="background:#2D5016"></div>
          <div class="sw" style="background:#4B0082"></div>
          <div class="sw" style="background:#FF6B6B"></div>
          <div class="sw" style="background:#2E8B57"></div>
        </div>
      </div>
      <div class="dc-card">
        <div class="tc-icon" style="margin:0 auto 12px;">🎩</div>
        <h3>Para Él</h3>
        <p class="dc-label">Colores sugeridos <span class="dc-note">(cualquier color)</span>:</p>
        <div class="swatches">
          <div class="sw" style="background:#000000"></div>
          <div class="sw" style="background:#1C1C1C"></div>
          <div class="sw" style="background:#2E2420"></div>
          <div class="sw" style="background:#404040"></div>
          <div class="sw" style="background:#5B4636"></div>
          <div class="sw" style="background:#7A4A42"></div>
          <div class="sw" style="background:#1B3A6B"></div>
          <div class="sw" style="background:#FFFFFF"></div>
        </div>
      </div>
    </div>
  </section>

  <section id="obsequio">
    <div class="gift-card reveal">
      <div class="gift-envelope" aria-hidden="true">
        <span></span>
      </div>
      <div class="eyebrow">Obsequio</div>
      <h2 class="gift-title">En sobre cerrado</h2>
      <p>El regalo debe venir en un sobre cerrado.</p>
    </div>
  </section>

  <section id="info">
    <div class="notice reveal">
      <div class="eyebrow" style="color:var(--burgundy);">Un aviso con cariño</div>
      <h3 style="font-family:var(--script);font-size:2rem;margin-top:10px;font-weight:400;">Es una celebración solo para adultos</h3>
      <p>
        Queremos que esta noche sea una velada elegante y tranquila, con un aforo cuidadosamente
        planificado y una recepción que se extiende hasta la madrugada. Por eso, con mucho cariño,
        pedimos que los más pequeños de la casa se queden con un cuidador esa noche. Sabemos que
        implica una organización extra de tu parte y te lo agradecemos de corazón.
      </p>
    </div>
  </section>

  <section id="contacto">
    <div class="letter-page contacto-card reveal">
      <div class="eyebrow" style="color:var(--gold);">Por si acaso</div>
      <h3 class="contacto-title">Contacto de emergencia</h3>
      <p class="contacto-nombre">Luis Avilés Lucas</p>
      <p class="contacto-tel">096 995 1379</p>
      <div class="contacto-actions">
        <a class="btn btn-ghost loc-btn" href="tel:+593969951379">Llamar</a>
        <a class="btn btn-ghost loc-btn" target="_blank" rel="noopener" href="https://wa.me/593969951379">WhatsApp</a>
      </div>
    </div>
  </section>

  <section id="rsvp">
    <div class="section-head">
      <div class="eyebrow">Confirmación</div>
      <h2 class="section-title">Confirma tu asistencia</h2>
    </div>

    <div class="letter-page reveal">
      <div id="fs-success" class="msg ok" style="display:none; margin-bottom:20px;">¡Gracias por confirmar! Te esperamos con mucha ilusión.</div>
      <div id="fs-error" class="msg err" style="display:none; margin-bottom:20px;"></div>

      <form id="rsvpForm" data-fs-form action="https://formspree.io/f/xvkoojdo" method="POST">
        <div class="field">
          <label for="nombre">Tu nombre completo</label>
          <input type="text" id="nombre" name="Nombre" placeholder="Nombre y apellido" required data-fs-field />
          <span data-fs-error="Nombre" class="field-error" style="display:none;"></span>
        </div>

        <div class="field">
          <label>¿Nos acompañarás?</label>
          <div class="rsvp-toggle" id="rsvpToggle">
            <button type="button" class="rsvp-btn" data-value="si">
              <span class="rsvp-radio"></span>
              <span class="rsvp-btn-text">
                <b>Sí, asistiré</b>
                <span>Confirmo mi asistencia</span>
              </span>
            </button>
            <button type="button" class="rsvp-btn" data-value="no">
              <span class="rsvp-radio"></span>
              <span class="rsvp-btn-text">
                <b>No podré asistir</b>
                <span>Lamentablemente no podré estar presente</span>
              </span>
            </button>
          </div>
          <input type="hidden" id="asistencia" name="Asistencia" required />
          <span data-fs-error="Asistencia" class="field-error" style="display:none;"></span>
        </div>

        <button type="submit" class="btn" id="submitBtn" data-fs-submit-btn>Enviar confirmación</button>
      </form>
      <div class="deadline">Por favor confirma antes del 25 de septiembre de 2026</div>
    </div>
  </section>

  <section id="gracias">
    <div class="story-card reveal">
      <div class="story-text">
        <div class="eyebrow" style="margin-bottom:8px;">Para siempre</div>
        <h3 style="font-family:var(--script);font-size:1.9rem;font-weight:400;color:var(--ink);margin-bottom:12px;">Gracias por formar parte de nuestra historia</h3>
        Te esperamos para celebrar nuestro amor con una velada llena de magia, flores
        y momentos inolvidables.
      </div>
    </div>
  </section>

  <div class="music-fab paused" id="musicFab" role="button" tabindex="0" title="Reproducir música" aria-label="Reproducir o pausar música de fondo">
    <div class="bars"><i></i><i></i><i></i></div>
  </div>
  <audio id="weddingAudio" loop preload="auto"></audio>

  <footer>Con todo nuestro cariño — Luis &amp; Verónica</footer>

  <script src="https://unpkg.com/@formspree/ajax@1" defer></script>
  <script src="/js/script.js"></script>
</body>
</html>
"""


def render_organizer_page() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Panel del organizador</title>
  <link rel="stylesheet" href="/css/style.css" />
  <script src="https://cdn.sheetjs.com/xlsx-0.18.5/package/dist/xlsx.full.min.js"></script>
</head>
<body class="organizer-body">
  <main class="organizer-shell">
    <section class="organizer-panel">
      <div class="eyebrow">Organizador</div>
      <h1 class="section-title">Generador de links</h1>
      <label class="field-label" for="genNombre">Nombre del invitado</label>
      <input id="genNombre" type="text" placeholder="Ej. Carlos Narváez y Esposa" />
      <div class="organizer-actions">
        <button id="genBtn" class="btn">Generar link</button>
        <button id="genCopyBtn" class="btn btn-ghost">Copiar link</button>
      </div>
      <div id="genResult" class="result-box">
        <label for="genLinkOutput">Link generado</label>
        <textarea id="genLinkOutput" readonly></textarea>
      </div>
    </section>

    <section class="organizer-panel">
      <div class="eyebrow">Música</div>
      <h2 class="section-title small">Guardar pista</h2>
      <label class="field-label" for="musicUrl">URL de música</label>
      <input id="musicUrl" type="text" placeholder="https://..." />
      <div class="organizer-actions">
        <button id="saveMusicBtn" class="btn">Guardar música</button>
      </div>
    </section>

    <section class="organizer-panel">
      <div class="eyebrow">RSVP</div>
      <h2 class="section-title small">Exportar respuestas</h2>
      <div class="organizer-actions">
        <button id="exportBtn" class="btn">Descargar respuestas (Excel)</button>
      </div>
    </section>
  </main>

  <script src="/js/organizer.js?v=3"></script>
</body>
</html>
"""


class AppHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        # Deshabilitar caché para archivos estáticos durante desarrollo
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def translate_path(self, path: str) -> str:
        return str((ROOT / "public" / urlparse(path).path.lstrip("/")).resolve())

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(render_public_page().encode("utf-8"))))
            self.end_headers()
            self.wfile.write(render_public_page().encode("utf-8"))
            return

        if path == "/organizador":
            content = render_organizer_page().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        static_root = (ROOT / "public").resolve()
        static_path = (static_root / path.lstrip("/")).resolve()
        if static_path.exists() and static_root in static_path.parents or static_path == static_root:
            try:
                super().do_GET()
                return
            except Exception:
                pass

        self.send_error(404, "Página no encontrada")

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    address = ("0.0.0.0", 8000)
    server = ThreadingHTTPServer(address, AppHandler)
    print("Servidor de invitación activo en http://localhost:8000")
    print("Presiona Ctrl+C para detenerlo.")
    server.serve_forever()


if __name__ == "__main__":
    run()