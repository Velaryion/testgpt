import {CATEGORIES, parseAmount, validateEntry, readBackup, summarize} from './core.mjs';
const $ = selector => document.querySelector(selector);
const key = 'bolsillo:data:v1';
const newId = () => typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : `entry-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,14)}`;
const currency = value => new Intl.NumberFormat('es-ES', {style: 'currency', currency: 'EUR'}).format(value / 100);
const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`; };
const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const palette = ['#73966b','#c5a476','#a1b98c','#d6bb9c','#879e9b','#b1a5bc','#d5d5bf'];
const symbols = {'Alimentación':'♧','Transporte':'↗','Hogar':'⌂','Ocio':'☆','Compras':'▱','Salud':'＋','Otros':'·','Nómina':'↙','Extra':'✧','Regalos':'◇'};
let entries = [], filter = 'all', editingId = null, toastTimer, storageBroken = false;
$('#month').value = today().slice(0,7);
try { const saved = localStorage.getItem(key); if(saved) entries = readBackup(JSON.parse(saved)); } catch { storageBroken = true; }
function notify(message) { clearTimeout(toastTimer); $('#toast').textContent = message; $('#toast').hidden = false; toastTimer = setTimeout(() => $('#toast').hidden = true, 6500); }
function backup(data) {return {version:1,currency:'EUR',entries:data};}
function persist(next) {
  if(storageBroken) throw new Error('No se puede leer el almacenamiento. Exporta los datos conservados y recupera una copia válida o revisa los permisos del navegador.');
  localStorage.setItem(key, JSON.stringify(backup(next)));
  entries = next;
  render();
}
function confirmAction(title, message) {
  const dialog = $('#confirm-dialog'); $('#confirm-title').textContent = title; $('#confirm-message').textContent = message;
  dialog.returnValue = ''; dialog.showModal();
  return new Promise(resolve => dialog.addEventListener('close', () => resolve(dialog.returnValue === 'confirm'), {once:true}));
}
function render() {
  const month = $('#month').value;
  const monthly = entries.filter(e => e.date.slice(0,7) === month);
  const totals = summarize(monthly);
  for(const field of ['income','expense','balance']) $('#'+field).textContent = currency(totals[field]);
  $('#month-count').textContent = `${monthly.length} ${monthly.length === 1 ? 'movimiento este mes' : 'movimientos este mes'}`;
  const query = $('#search').value.trim().toLocaleLowerCase('es');
  const visible = monthly.filter(e => (filter === 'all' || e.type === filter) && `${e.description} ${e.category}`.toLocaleLowerCase('es').includes(query)).sort((a,b) => b.date.localeCompare(a.date));
  $('#visible-count').textContent = visible.length;
  $('#entries').innerHTML = visible.length ? visible.map(e => `<article class="entry"><span class="entry-icon" aria-hidden="true">${symbols[e.category]}</span><div class="entry-details"><p class="entry-name">${escape(e.description)}</p><div class="entry-meta">${escape(e.category)} · ${new Intl.DateTimeFormat('es-ES',{day:'numeric',month:'short'}).format(new Date(e.date+'T12:00:00'))}</div></div><span class="entry-amount ${e.type === 'income' ? 'positive' : ''}">${e.type === 'income' ? '+' : '−'}${currency(e.amount)}</span><div class="entry-actions"><button data-edit="${e.id}" aria-label="Editar ${escape(e.description)}" title="Editar">✎</button><button data-delete="${e.id}" aria-label="Eliminar ${escape(e.description)}" title="Eliminar">×</button></div></article>`).join('') : `<div class="empty"><div class="empty-symbol" aria-hidden="true">▱</div><h3>${monthly.length ? 'Sin coincidencias' : 'Todo empieza con un apunte.'}</h3><p>${monthly.length ? 'Prueba otro concepto o cambia el filtro para encontrar tu movimiento.' : 'Añade tu primer ingreso o gasto y empieza a ver tu mes con más claridad.'}</p>${monthly.length ? '' : '<button class="text-button" id="empty-add">Añadir mi primer movimiento ＋</button>'}</div>`;
  $('#empty-add')?.addEventListener('click', () => openEntry());
  const groups = CATEGORIES.expense.map((category,index) => ({category,color:palette[index],amount:monthly.filter(e=>e.type==='expense' && e.category===category).reduce((sum,e)=>sum+e.amount,0)})).filter(g=>g.amount).sort((a,b)=>b.amount-a.amount);
  let position = 0;
  const gradient = groups.map(g => { const start=position; position+=g.amount/totals.expense*100; return `${g.color} ${start}% ${position}%`; }).join(',');
  $('#category-chart').innerHTML = `<div class="chart-empty"><div class="donut" ${groups.length ? `style="background:conic-gradient(${gradient})"` : ''} role="img" aria-label="${groups.length ? 'Distribución del gasto detallada debajo' : 'Aún no hay gastos'}"><div class="donut-label"><strong>${currency(totals.expense)}</strong><span>gastado este mes</span></div></div>${groups.length ? '' : '<p>Cuando añadas un gasto,<br>verás aquí cómo se reparte.</p>'}</div>${groups.length ? `<ul class="category-list">${groups.map(g=>`<li><i style="background:${g.color}" aria-hidden="true"></i><span>${g.category}</span><b>${currency(g.amount)}</b><small>${Math.round(g.amount/totals.expense*100)}%</small></li>`).join('')}</ul>` : ''}`;
  $('#previous-month').disabled = month === '1900-01'; $('#next-month').disabled = month === '9999-12';
}
function updateCategories() {
  const form = $('#entry-form');
  form.elements.category.replaceChildren(...CATEGORIES[form.elements.type.value].map(category => new Option(category,category)));
}
function openEntry(entry = null, type = 'expense') {
  const form = $('#entry-form'); form.reset(); editingId = entry?.id ?? null;
  form.elements.type.value = entry?.type ?? type; updateCategories();
  form.elements.date.value = entry?.date ?? today();
  form.elements.description.value = entry?.description ?? '';
  form.elements.amount.value = entry ? (entry.amount/100).toFixed(2).replace('.',',') : '';
  if(entry) form.elements.category.value = entry.category;
  $('#dialog-title').textContent = entry ? 'Editar movimiento' : 'Nuevo movimiento';
  $('#form-error').textContent = '';
  $('#entry-dialog').showModal(); form.elements.description.focus();
}
$('#add-entry').addEventListener('click', () => openEntry());
$('#quick-add').addEventListener('click', () => openEntry());
$('#close-dialog').addEventListener('click', () => $('#entry-dialog').close());
$('#entry-form').elements.type.forEach(radio => radio.addEventListener('change', updateCategories));
$('#entry-form').addEventListener('submit', event => {
  event.preventDefault(); const form=event.currentTarget;
  try {
    const entry = validateEntry({id:editingId ?? newId(),type:form.elements.type.value,amount:parseAmount(form.elements.amount.value),date:form.elements.date.value,category:form.elements.category.value,description:form.elements.description.value});
    const next = editingId ? entries.map(e=>e.id===editingId ? entry : e) : [...entries,entry];
    persist(next); $('#month').value = entry.date.slice(0,7); $('#search').value = ''; setFilter('all');
    $('#entry-dialog').close(); notify(editingId ? 'Cambios guardados.' : 'Movimiento guardado. Un paso más.');
  } catch(error) {$('#form-error').textContent = error.name === 'QuotaExceededError' ? 'No queda espacio. Exporta una copia antes de continuar.' : error.message;}
});
function setFilter(value) {filter=value;document.querySelectorAll('[data-filter]').forEach(b=>{b.classList.toggle('active',b.dataset.filter===filter);b.setAttribute('aria-pressed',String(b.dataset.filter===filter));});render();}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>setFilter(button.dataset.filter)));
$('#search').addEventListener('input',render);
let lastMonth = $('#month').value;
$('#month').addEventListener('change',()=>{if(!/^\d{4}-\d{2}$/.test($('#month').value) || $('#month').value<'1900-01' || $('#month').value>'9999-12') $('#month').value=lastMonth;lastMonth=$('#month').value;render();});
function shiftMonth(delta) {let [year,month]=$('#month').value.split('-').map(Number);month+=delta;if(month===0){year--;month=12;}if(month===13){year++;month=1;}if(year<1900||year>9999)return;$('#month').value=`${year}-${String(month).padStart(2,'0')}`;lastMonth=$('#month').value;render();}
$('#previous-month').addEventListener('click',()=>shiftMonth(-1)); $('#next-month').addEventListener('click',()=>shiftMonth(1));
$('#entries').addEventListener('click',async event=>{
  const edit=event.target.closest('[data-edit]'); const remove=event.target.closest('[data-delete]');
  if(edit) {const entry=entries.find(e=>e.id===edit.dataset.edit);if(entry)openEntry(entry);}
  if(remove){const entry=entries.find(e=>e.id===remove.dataset.delete);if(!entry)return;if(await confirmAction('¿Eliminar este movimiento?',`${entry.description} · ${currency(entry.amount)}. Esta acción no se puede deshacer.`)){try{persist(entries.filter(e=>e.id!==entry.id));notify('Movimiento eliminado.');}catch(error){notify(error.message);}}}
});
$('#export').addEventListener('click',()=>{
  if(storageBroken){notify('No se ha podido leer la copia local. No se exportará una copia incompleta.');return;}
  const blob=new Blob([JSON.stringify({...backup(entries),exportedAt:new Date().toISOString()},null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`bolsillo-${today()}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('Copia exportada. Guárdala en un lugar seguro.');
});
$('#import').addEventListener('click',()=>$('#import-file').click());
$('#import-file').addEventListener('change',async event=>{
  const file=event.target.files[0];event.target.value='';if(!file)return;
  try{
    if(file.size>10000000)throw new Error('La copia supera el límite de 10 MB.');
    const imported=readBackup(JSON.parse(await file.text()));
    if(await confirmAction('¿Restaurar esta copia?',`Se cargarán ${imported.length} movimientos y se sustituirán los ${entries.length} actuales de este navegador. Exporta antes si quieres conservarlos.`)){
      const priorBroken=storageBroken;storageBroken=false;
      try{persist(imported);}catch(error){storageBroken=priorBroken;throw error;}
      if(entries.length)$('#month').value=[...entries].sort((a,b)=>b.date.localeCompare(a.date))[0].date.slice(0,7);
      $('#search').value='';setFilter('all');notify('Copia restaurada correctamente.');
    }
  }catch(error){notify(error instanceof SyntaxError ? 'El archivo no contiene una copia JSON válida.' : error.message);}
});
window.addEventListener('storage', event=>{if(event.key!==key && event.key!==null)return;try{const saved=localStorage.getItem(key);entries=saved?readBackup(JSON.parse(saved)):[];storageBroken=false;$('#entry-dialog').close();render();notify('Datos actualizados desde otra pestaña.');}catch{storageBroken=true;notify('No se ha podido leer el cambio de otra pestaña.');}});
render();if(storageBroken)notify('No se pueden leer los datos guardados. No se sobrescribirán. Revisa el almacenamiento o importa una copia válida.');
