/* ---------------- INVITACIÓN PERSONALIZADA (por link) ---------------- */
const params = new URLSearchParams(window.location.search);
const invitadoNombre = params.get('invitado');

const welcomeGate = document.getElementById('welcomeGate');
if(welcomeGate){
  document.body.style.overflow = 'hidden';
  welcomeGate.addEventListener('click', () => {
    welcomeGate.classList.add('wg-hidden');
    document.body.style.overflow = '';
    forzarReproduccion();
  }, { once:true });
}

function activarEntradaHero(){
  document.querySelectorAll('.hero-in').forEach(el=>el.classList.add('hero-in-active'));
}

activarEntradaHero();

const store = {
  async set(key, value, shared){
    if(window.storage) return window.storage.set(key, value, shared);
    localStorage.setItem(key, value);
    return {key, value, shared};
  },
  async get(key, shared){
    if(window.storage) return window.storage.get(key, shared);
    const value = localStorage.getItem(key);
    if(value === null) throw new Error('not found');
    return {key, value, shared};
  },
  async list(prefix, shared){
    if(window.storage) return window.storage.list(prefix, shared);
    const keys = Object.keys(localStorage).filter(k => !prefix || k.startsWith(prefix));
    return {keys, prefix, shared};
  }
};

const nav = document.querySelector('.topbar');
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelectorAll('.main-nav a');
const progressBar = document.getElementById('scrollProgress');

function updateScrollProgress(){
  const scrollTop = window.scrollY;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
  const percent = maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;
  if(progressBar) progressBar.style.width = `${percent}%`;
}

if(navToggle){
  navToggle.addEventListener('click', ()=>{
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('nav-open');
  });
}

navLinks.forEach(link => {
  link.addEventListener('click', ()=>{
    if(nav) nav.classList.remove('nav-open');
    if(navToggle) navToggle.setAttribute('aria-expanded', 'false');
  });
});

function updateActiveNav(){
  const sections = Array.from(document.querySelectorAll('section[id]'));
  const scrollPosition = window.scrollY + 140;

  sections.forEach(section => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    const id = section.getAttribute('id');
    const menuLink = document.querySelector(`.main-nav a[href="#${id}"]`);
    if(!menuLink) return;

    const inView = scrollPosition >= top && scrollPosition < top + height;
    menuLink.classList.toggle('active', inView);
  });
}

window.addEventListener('scroll', ()=>{
  updateScrollProgress();
  updateActiveNav();
}, {passive:true});
window.addEventListener('load', ()=>{
  updateScrollProgress();
  updateActiveNav();
});

if('IntersectionObserver' in window){
  const revealObserver = new IntersectionObserver((entries)=>{
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, {threshold:.2, rootMargin:'0px 0px -30px 0px'});
  document.querySelectorAll('.tc-reveal, .reveal').forEach(el=>revealObserver.observe(el));
} else {
  document.querySelectorAll('.tc-reveal, .reveal').forEach(el=>el.classList.add('in-view'));
}

const WEDDING_DATE = new Date('2026-10-10T19:30:00');

function setCountdownValue(id, value){
  const el = document.getElementById(id);
  if(el.textContent !== value){
    el.textContent = value;
    el.classList.remove('tick');
    void el.offsetWidth;
    el.classList.add('tick');
  }
}

function tickCountdown(){
  const now = new Date();
  let diff = WEDDING_DATE - now;
  if(diff < 0) diff = 0;
  const d = Math.floor(diff/(1000*60*60*24));
  const h = Math.floor((diff/(1000*60*60))%24);
  const m = Math.floor((diff/(1000*60))%60);
  const s = Math.floor((diff/1000)%60);
  setCountdownValue('cd-days', String(d).padStart(2,'0'));
  setCountdownValue('cd-hours', String(h).padStart(2,'0'));
  setCountdownValue('cd-min', String(m).padStart(2,'0'));
  setCountdownValue('cd-sec', String(s).padStart(2,'0'));
}
tickCountdown();
setInterval(tickCountdown, 1000);

function makeKeyActivatable(id, handler){
  const el = document.getElementById(id);
  if(!el) return;
  el.addEventListener('keydown', (e)=>{
    if(e.key === 'Enter' || e.key === ' '){
      e.preventDefault();
      handler();
    }
  });
}

/* ---------------- RSVP: envío manual a Formspree vía fetch ---------------- */
const rsvpButtons = document.querySelectorAll('.rsvp-btn');
let asistenciaElegida = null;

if(invitadoNombre){
  const nombreInput = document.getElementById('nombre');
  if(nombreInput) nombreInput.value = invitadoNombre;
}

rsvpButtons.forEach(btn=>{
  btn.addEventListener('click', ()=>{
    rsvpButtons.forEach(b=>b.classList.remove('selected'));
    btn.classList.add('selected');
    asistenciaElegida = btn.dataset.value;
    const asistenciaInput = document.getElementById('asistencia');
    if(asistenciaInput){
      asistenciaInput.value = asistenciaElegida === 'si' ? 'Sí asistirá' : 'No asistirá';
    }
  });
});

const rsvpForm = document.getElementById('rsvpForm');
if(rsvpForm){
  rsvpForm.addEventListener('submit', async (e)=>{
    e.preventDefault(); // SIEMPRE se detiene el envío nativo del navegador

    const errorDiv = document.getElementById('fs-error');
    const successDiv = document.getElementById('fs-success');
    const submitBtn = document.getElementById('submitBtn');

    if(errorDiv){ errorDiv.style.display = 'none'; errorDiv.textContent = ''; }
    if(successDiv) successDiv.style.display = 'none';

    if(!asistenciaElegida){
      if(errorDiv){
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Por favor indica si asistirás o no.';
      }
      return;
    }

    const formData = new FormData(rsvpForm);

    if(submitBtn){
      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando...';
    }

    try {
      const response = await fetch(rsvpForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'Accept': 'application/json' }
      });

      if(response.ok){
        if(successDiv) successDiv.style.display = 'block';
        rsvpForm.reset();
        rsvpButtons.forEach(b=>b.classList.remove('selected'));
        asistenciaElegida = null;
      } else {
        const data = await response.json().catch(()=>null);
        const message = (data && data.errors && data.errors.length)
          ? data.errors.map(err => err.message).join(', ')
          : 'Ocurrió un error al enviar. Intenta de nuevo.';
        if(errorDiv){
          errorDiv.style.display = 'block';
          errorDiv.textContent = message;
        }
      }
    } catch (err) {
      if(errorDiv){
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'No se pudo conectar. Revisa tu internet e intenta de nuevo.';
      }
    } finally {
      if(submitBtn){
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar confirmación';
      }
    }
  });
}

/* ---------------- MÚSICA: reproducción continua sin opción de pausa ---------------- */
const MUSIC_FILE = 'audio/musica-boda.mp3';
const audio = document.getElementById('weddingAudio');
const musicFab = document.getElementById('musicFab');
const musicState = {
  ready: false
};

function updateMusicFab() {
  if (!musicFab) return;
  const reproduciendo = audio && !audio.paused;
  musicFab.setAttribute('aria-label', reproduciendo ? 'Reproduciendo' : 'Cargando música');
  musicFab.title = reproduciendo ? 'Reproduciendo' : 'Cargando música';
  musicFab.classList.toggle('paused', !reproduciendo);
  musicFab.innerHTML = '<div class="bars"><i></i><i></i><i></i></div>';
}

async function loadSavedMusic() {
  if (!audio) return;

  audio.volume = 0.8;
  audio.preload = 'auto';
  audio.loop = true;

  try {
    const res = await store.get('ambient-music-url', true);
    if (res && res.value && res.value.trim()) {
      audio.src = res.value.trim();
      audio.load();
      musicState.ready = true;
      updateMusicFab();
      return;
    }
  } catch (err) {
    // No hay música guardada; usa el valor por defecto.
  }

  audio.src = MUSIC_FILE;
  audio.load();
  musicState.ready = true;
  updateMusicFab();
}

async function forzarReproduccion() {
  if (!audio || !musicState.ready) return;
  try {
    audio.muted = false;
    audio.volume = 0.8;
    if (audio.paused) {
      await audio.play();
    }
    updateMusicFab();
  } catch (error) {
    // El navegador bloqueó el intento; se reintentará con la próxima interacción.
  }
}

if (audio) {
  loadSavedMusic();

  audio.addEventListener('play', updateMusicFab);
  audio.addEventListener('pause', () => {
    forzarReproduccion();
  });

  audio.addEventListener('error', () => {
    musicState.ready = false;
    if (musicFab) {
      musicFab.title = 'No se pudo cargar la música';
      musicFab.innerHTML = '<span class="music-icon" aria-hidden="true">🔇</span>';
    }
  });

  ['pointerdown', 'click', 'touchstart', 'keydown'].forEach(evento => {
    document.addEventListener(evento, forzarReproduccion, { passive: true });
  });

  setTimeout(forzarReproduccion, 250);
}