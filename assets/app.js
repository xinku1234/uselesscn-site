async function loadJSON(path){
  const r=await fetch(path,{cache:'no-store'});
  if(!r.ok)throw new Error(path);
  return r.json();
}
function aliveSites(sites){const good=sites.filter(s=>s.status!=='dead');return good.length?good:sites}
function randomItem(items){return items[Math.floor(Math.random()*items.length)]}
function isMobileLike(){return /Android|iPhone|iPad|iPod|Mobile|MicroMessenger|QQ\//i.test(navigator.userAgent||'')}
function openExternal(url){
  if(isMobileLike()){
    toast('Opening…');
    window.location.href=url;
    return;
  }
  const w=window.open(url,'_blank','noopener,noreferrer');
  if(!w){
    toast('Opening in this tab…');
    window.location.href=url;
  }
}
function toast(msg){let el=document.querySelector('.toast');if(!el){el=document.createElement('div');el.className='toast';document.body.appendChild(el)}el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2200)}
function statusLabel(status){return status==='alive'?'Live':status==='dead'?'Needs review':status==='blocked'?'Bot-blocked':'Check'}
function siteCard(s){return `<article class="site-card"><h3>${s.title}</h3><p>${s.description||''}</p><div><span class="tag">${s.category||'Uncategorized'}</span>${(s.tags||[]).slice(0,2).map(t=>`<span class="tag">#${t}</span>`).join('')}</div><div class="status">Status: ${statusLabel(s.status)} · <a href="${s.url}" target="_blank" rel="noopener noreferrer">Open in new tab</a></div></article>`}
async function initHome(){
  const sites=await loadJSON('data/sites.json');
  let meta={};try{meta=await loadJSON('data/meta.json')}catch(e){}
  document.querySelector('#count').textContent=sites.length;
  const pick=sites.find(s=>s.id===meta.today_pick)||randomItem(aliveSites(sites));
  const daily=document.querySelector('#daily');
  if(daily&&pick)daily.innerHTML=`Today's pick: <strong>${pick.title}</strong>`;
  const go=document.querySelector('#go');
  go.addEventListener('click',()=>{
    const s=randomItem(aliveSites(sites));
    go.textContent='OPENING…';
    openExternal(s.url);
    setTimeout(()=>{go.textContent='PLEASE'},650);
  });
  document.querySelector('#dailyGo')?.addEventListener('click',e=>{e.preventDefault();if(pick)openExternal(pick.url)})
}
async function initSites(){
  const sites=await loadJSON('data/sites.json');
  const grid=document.querySelector('#sitesGrid');
  const filter=document.querySelector('#filter');
  function render(q=''){
    const lower=q.trim().toLowerCase();
    const list=sites.filter(s=>!lower||[s.title,s.description,s.category,...(s.tags||[])].join(' ').toLowerCase().includes(lower));
    grid.innerHTML=list.map(siteCard).join('')||'<p class="hint">No matching useless websites found.</p>';
  }
  filter.addEventListener('input',e=>render(e.target.value));
  render();
}
function initSubmit(){
  const form=document.querySelector('#submitForm');
  form?.addEventListener('submit',e=>{
    e.preventDefault();
    const data=new FormData(form);
    const subject=encodeURIComponent('UselessCN submission: '+data.get('title'));
    const body=encodeURIComponent(`Website name: ${data.get('title')}
URL: ${data.get('url')}
Category: ${data.get('category')}
Reason: ${data.get('reason')}`);
    location.href=`mailto:xie565699861@gmail.com?subject=${subject}&body=${body}`;
    toast('Opening your email app…');
  })
}
