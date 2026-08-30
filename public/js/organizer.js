/* ---------------- ALMACENAMIENTO (adaptador) ----------------
   Igual que en js/script.js — window.storage solo existe dentro de Claude;
   fuera de ahí usa localStorage como respaldo (ver README.md). */
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

/* v2.1 - Link generator fix */
/* GENERADOR DE LINKS POR INVITADO */
document.getElementById('genBtn').addEventListener('click', ()=>{
  const nombre = document.getElementById('genNombre').value.trim();
  const resultBox = document.getElementById('genResult');
  const output = document.getElementById('genLinkOutput');

  if(!nombre){
    alert('Escribe el nombre del invitado primero.');
    return;
  }

  // Construye el link apuntando a la raíz usando origin
  const origen = window.location.origin;
  const nuevoLink = `${origen}/?invitado=${encodeURIComponent(nombre)}`;

  output.value = nuevoLink;
  resultBox.style.display = 'block';
});

document.getElementById('genCopyBtn').addEventListener('click', async ()=>{
  const output = document.getElementById('genLinkOutput');
  const btn = document.getElementById('genCopyBtn');
  try{
    await navigator.clipboard.writeText(output.value);
    btn.textContent = 'Copiado ✓';
  }catch(err){
    output.select();
    document.execCommand('copy');
    btn.textContent = 'Copiado ✓';
  }
  setTimeout(()=>{ btn.textContent = 'Copiar link'; }, 2000);
});

/* ---------------- GUARDAR MÚSICA ---------------- */
document.getElementById('saveMusicBtn').addEventListener('click', async ()=>{
  const url = document.getElementById('musicUrl').value.trim();
  const btn = document.getElementById('saveMusicBtn');
  if(!url){ return; }
  btn.disabled = true;
  btn.textContent = 'Guardando...';
  try{
    await store.set('ambient-music-url', url, true);
    btn.textContent = 'Música guardada ✓';
  }catch(err){
    btn.textContent = 'Error al guardar';
  }
  setTimeout(()=>{ btn.disabled = false; btn.textContent = 'Guardar música'; }, 2500);
});

/* ---------------- EXPORTAR A EXCEL ---------------- */
document.getElementById('exportBtn').addEventListener('click', async ()=>{
  const btn = document.getElementById('exportBtn');
  btn.disabled = true;
  btn.textContent = 'Preparando archivo...';
  try{
    const list = await store.list('rsvp:', true);
    const rows = [['Nombre','Asistencia','Fecha de confirmación']];
    if(list && list.keys && list.keys.length){
      for(const k of list.keys){
        try{
          const item = await store.get(k, true);
          if(item && item.value){
            const d = JSON.parse(item.value);
            const asistenciaTexto = d.tipo === 'no' ? 'No asistirá' : 'Sí asistirá';
            rows.push([
              d.nombre || '',
              asistenciaTexto,
              d.fecha ? new Date(d.fecha).toLocaleString('es-EC') : ''
            ]);
          }
        }catch(e){ /* clave individual falló, se omite */ }
      }
    }
    const ws = XLSX.utils.aoa_to_sheet(rows);
    ws['!cols'] = [{wch:28},{wch:16},{wch:22}];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Confirmaciones');
    XLSX.writeFile(wb, 'confirmaciones-boda.xlsx');
    btn.textContent = 'Descargado ✓';
  }catch(err){
    btn.textContent = 'No se pudo generar el archivo';
  }
  setTimeout(()=>{ btn.disabled = false; btn.textContent = 'Descargar respuestas (Excel)'; }, 2500);
});
