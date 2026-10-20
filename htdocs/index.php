<?php // Jurnal MT5 — tema Argon Dashboard 3 Free (MIT, Creative Tim), data dari api.php
header("Cache-Control: no-store, max-age=0"); ?>
<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>MT5 Trade Journal</title>
<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet">
<link href="assets/css/argon-dashboard.css?v=2.1.0" rel="stylesheet">
<style>
.ai-text{white-space:pre-wrap;font-size:.85rem;line-height:1.6}
.ai-text strong{font-weight:700}
.ai-sec{display:block;font-weight:700;font-size:.72rem;letter-spacing:.04em;text-transform:uppercase;color:#5e72e4;margin:.85rem 0 .3rem}
.ai-sec:first-child{margin-top:0}
.ai-text ul{margin:.25rem 0 .5rem;padding-left:1.2rem}
.ai-text li{margin-bottom:.15rem}
.rep-head{cursor:pointer;border-radius:.75rem .75rem 0 0;transition:background .15s}
.rep-head:hover{background:rgba(94,114,228,.06)}
.rep-badge{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:.65rem;background:linear-gradient(135deg,#5e72e4,#825ee4);color:#fff;font-weight:700;font-size:.8rem;flex:none}
.rep-toggle{flex:none;display:inline-flex;align-items:center;gap:.35rem;border:1px solid rgba(94,114,228,.45);color:#5e72e4;background:#fff;border-radius:2rem;padding:.22rem .75rem;font-size:.75rem;font-weight:700;white-space:nowrap;transition:.15s}
.rep-head:hover .rep-toggle{background:#5e72e4;color:#fff;border-color:#5e72e4}
.pos-card{border-left:4px solid #adb5bd}
.pos-win{border-left-color:#2dce89!important}
.pos-loss{border-left-color:#f5365c!important}
.crumb{font-size:.72rem;color:rgba(255,255,255,.65);margin:0}
.hero-title{color:#fff;font-weight:700;margin:0;line-height:1.2}
.hero-sub{font-size:.8rem;color:rgba(255,255,255,.75)}
.glass{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(6px);color:#fff;border-radius:.75rem;padding:.35rem .8rem;font-size:.75rem;font-weight:600;white-space:nowrap}
.glass-dark{background:#fff;border:1px solid rgba(0,0,0,.08);box-shadow:0 2px 6px rgba(0,0,0,.06);color:#344767;border-radius:.75rem;padding:.35rem .8rem;font-size:.75rem;font-weight:600;white-space:nowrap}
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#2dce89;margin-right:6px;animation:pulse 1.6s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(45,206,137,.7)}70%{box-shadow:0 0 0 8px rgba(45,206,137,0)}100%{box-shadow:0 0 0 0 rgba(45,206,137,0)}}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.cal-dow{font-size:.65rem;text-transform:uppercase;color:#8392ab;text-align:center;font-weight:700}
.cal-cell{min-height:52px;border-radius:.5rem;padding:2px 5px;font-size:.72rem;background:#f8f9fa}
.cal-cell.has{cursor:pointer}
.cal-win{background:rgba(45,206,137,.16);border:1px solid rgba(45,206,137,.4)}
.cal-loss{background:rgba(245,54,92,.12);border:1px solid rgba(245,54,92,.35)}
.cal-dim{opacity:.45}
.cal-num{font-weight:700}
.cal-net{font-weight:700}
.cal-today{box-shadow:0 0 0 2px #5e72e4 inset}
</style>
</head>
<body class="g-sidenav-show bg-gray-100">
<div class="min-height-300 bg-primary position-absolute w-100"></div>
<aside class="sidenav bg-white navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-4" id="sidenav-main">
  <div class="sidenav-header">
    <span class="navbar-brand m-0"><span class="font-weight-bold">Jurnal MT5</span></span>
  </div>
  <hr class="horizontal dark mt-0">
  <div class="navbar-collapse w-auto" id="sidenav-collapse-main">
    <ul class="navbar-nav">
      <li class="nav-item"><span class="nav-link active"><span class="nav-link-text ms-1">Dashboard</span></span></li>
      <li class="nav-item"><span class="nav-link" style="cursor:pointer" onclick="setFilter('')"><span class="nav-link-text ms-1">Semua posisi</span></span></li>
      <li class="nav-item"><span class="nav-link" style="cursor:pointer" onclick="setFilter('TP')"><span class="nav-link-text ms-1">Hit TP</span></span></li>
      <li class="nav-item"><span class="nav-link" style="cursor:pointer" onclick="setFilter('SL')"><span class="nav-link-text ms-1">Hit SL</span></span></li>
    </ul>
  </div>
  <div class="sidenav-footer mx-3 mt-3">
    <div class="card card-plain shadow-none border"><div class="card-body p-3"><small class="text-muted">Auto-refresh 30 dtk</small></div></div>
  </div>
</aside>
<main class="main-content position-relative border-radius-lg">
  <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl" data-scroll="false">
    <div class="container-fluid py-2 px-3 d-block">
      <div class="d-flex align-items-center">
        <p class="crumb mb-0">Pages&nbsp;&nbsp;/&nbsp;&nbsp;Trade Journal</p>
        <span class="glass ms-auto"><span class="live-dot"></span>LIVE</span>
      </div>
      <div class="mt-2">
        <div>
          <h4 class="hero-title">MT5 Trade Journal</h4>
          <span class="hero-sub" id="acc-sub">menghubungkan ke MT5…</span>
        </div>
      </div>
    </div>
  </nav>
  <div class="container-fluid pb-4" style="padding-top:1.25rem">
    <div class="row">
      <div class="col-12 mb-4"><div class="d-flex gap-2 flex-nowrap" style="overflow-x:auto;max-width:100%">
        <span class="glass-dark" id="clock">--:--:--</span>
        <span class="glass-dark" id="meta">update …</span>
      </div></div>
    </div>
    <div class="row">
      <div class="col-6 col-lg-3 mb-4"><div class="card h-100 mb-0"><div class="card-body p-3"><p class="text-sm mb-0 text-uppercase font-weight-bold">Balance</p><h5 class="font-weight-bolder mb-0" id="st-bal">–</h5></div></div></div>
      <div class="col-6 col-lg-3 mb-4"><div class="card h-100 mb-0"><div class="card-body p-3"><p class="text-sm mb-0 text-uppercase font-weight-bold">Equity</p><h5 class="font-weight-bolder mb-0" id="st-eq">–</h5></div></div></div>
      <div class="col-6 col-lg-3 mb-4"><div class="card h-100 mb-0"><div class="card-body p-3"><p class="text-sm mb-0 text-uppercase font-weight-bold">Win Rate (close)</p><h5 class="font-weight-bolder mb-0" id="st-wr">–</h5></div></div></div>
      <div class="col-6 col-lg-3 mb-4"><div class="card h-100 mb-0"><div class="card-body p-3"><p class="text-sm mb-0 text-uppercase font-weight-bold">Total Net (close)</p><h5 class="font-weight-bolder mb-0" id="st-net">–</h5></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-0"><h6 class="mb-0">Posisi Open — <span id="acc">…</span></h6></div><div class="card-body p-3"><div class="table-responsive" id="open">memuat…</div></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-0 d-flex align-items-center"><h6 class="mb-0">Cumulative P&amp;L (closed)</h6><span class="badge bg-gradient-primary ms-2" id="pnl-total">+0 USD</span></div><div class="card-body p-3"><div style="height:260px"><canvas id="pnlChart"></canvas></div><p class="text-xs text-secondary mb-0 mt-2" id="pnl-empty">Belum ada data close — grafik terisi otomatis.</p></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-0 d-flex align-items-center flex-wrap gap-2"><h6 class="mb-0">Kalender Profit</h6><div class="ms-auto d-flex align-items-center gap-2"><button class="btn btn-sm btn-outline-primary mb-0" onclick="calMove(-1)">&laquo;</button><span class="text-sm font-weight-bold" id="cal-title"></span><button class="btn btn-sm btn-outline-primary mb-0" onclick="calMove(1)">&raquo;</button><button class="btn btn-sm btn-outline-secondary mb-0" onclick="calToday()">Bulan ini</button></div></div><div class="card-body p-3"><div id="cal"></div><div class="text-xs text-secondary text-end mb-0 mt-2" id="cal-sub"></div></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-0 d-flex align-items-start flex-wrap gap-2"><h6 class="mb-0">Kinerja - Pair</h6><div class="ms-auto d-flex flex-column align-items-end gap-1"><span class="text-sm text-secondary mb-0">Range Tanggal:</span><div class="d-flex align-items-center gap-2 flex-wrap"><input type="date" id="f-from" class="form-control form-control-sm" style="max-width:160px" onchange="setDate()"><span class="text-sm text-secondary mb-0">s/d</span><input type="date" id="f-to" class="form-control form-control-sm" style="max-width:160px" onchange="setDate()"><button class="btn btn-sm btn-outline-primary mb-0" onclick="resetDate()">Today</button><button class="btn btn-sm btn-outline-secondary mb-0" onclick="clearDate()">Semua</button></div></div></div><div class="card-body p-3"><div id="pairs"></div></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-2 pt-3 rep-head d-flex align-items-center" role="button" onclick="toggleReport()"><span class="rep-badge">AI</span><div class="ms-2 me-2"><h6 class="mb-0">Evaluasi AI</h6><p class="text-xs text-secondary mb-0">Analisa otomatis seluruh riwayat trading</p></div><span class="text-xs text-secondary ms-auto text-end" id="rep-meta">menunggu laporan…</span><span id="rep-caret" class="rep-toggle ms-3">Lihat &#9662;</span></div><div class="card-body pt-0 pb-3 px-3" id="rep-wrap" style="display:none"><hr class="horizontal dark my-2"><div class="ai-text" id="rep-body">Belum ada laporan — terbentuk otomatis tiap 1 jam.</div><details class="mt-3"><summary class="text-xs font-weight-bold" style="cursor:pointer">Memori &amp; pola jangka panjang</summary><div class="ai-text mt-2" id="rep-mem">Belum ada memori.</div></details></div></div></div>
    </div>
    <div class="row">
      <div class="col-12 mb-4"><div class="card mb-0"><div class="card-header pb-0 d-flex align-items-center"><h6 class="mb-0">Riwayat Transaksi</h6><span class="badge badge-sm bg-gradient-secondary ms-2" id="list-count">0</span></div><div class="card-body p-3" id="list"><p class="text-sm text-secondary mb-0">memuat…</p></div></div></div>
    </div>
    <footer class="footer pt-3 pb-3"><div class="container-fluid"><p class="text-sm text-secondary text-center">© 2026 <a href="https://t.me/sandy_airlangga" target="_blank" rel="noopener">@sandy_airlangga</a> · All rights reserved</p></div></footer>
  </div>
</main>
<script src="assets/js/core/popper.min.js"></script>
<script src="assets/js/core/bootstrap.min.js"></script>
<script src="assets/js/plugins/chartjs.min.js"></script>
<script src="assets/js/argon-dashboard.js"></script>
<script>
let curFilter='', pnlChart=null, dateFrom='', dateTo='';
function wib(d){return new Date(d*1000).toLocaleDateString('en-CA',{timeZone:'Asia/Jakarta'});}
function setDate(){dateFrom=document.getElementById('f-from').value;dateTo=document.getElementById('f-to').value;load();}
function resetDate(){const t=wib(Date.now()/1000);document.getElementById('f-from').value=t;document.getElementById('f-to').value=t;dateFrom=t;dateTo=t;load();}
function clearDate(){document.getElementById('f-from').value='';document.getElementById('f-to').value='';dateFrom='';dateTo='';load();}
let lastSig='';
function toggleReport(){const w=document.getElementById('rep-wrap'),c=document.getElementById('rep-caret');const show=w.style.display==='none';w.style.display=show?'':'none';c.innerHTML=show?'Tutup &#9652;':'Lihat &#9662;';}
function drawPnl(closed){
  const cv=document.getElementById('pnlChart');
  const empty=document.getElementById('pnl-empty');
  const seq=closed.slice().sort((a,b)=>a.close_time-b.close_time);
  let run=0;
  const labels=seq.map(x=>new Date(x.close_time*1000).toLocaleDateString('id-ID',{day:'2-digit',month:'short'}));
  const data=seq.map(x=>{run+=(+x.net||0);return Math.round(run*100)/100;});
  const last=data.length?data[data.length-1]:0;
  const badge=document.getElementById('pnl-total');
  badge.textContent=(last>=0?'+':'')+last+' USD';
  badge.className='badge ms-2 '+(last>0?'bg-gradient-success':(last<0?'bg-gradient-danger':'bg-gradient-secondary'));
  empty.style.display=seq.length?'none':'';
  cv.style.display=seq.length?'':'none';
  if(!seq.length||typeof Chart==='undefined')return;
  const up=last>=0;
  const cfg={type:'line',data:{labels:labels,datasets:[{label:'Cumulative USD',data:data,borderColor:up?'#2dce89':'#f5365c',backgroundColor:up?'rgba(45,206,137,.15)':'rgba(245,54,92,.15)',fill:true,tension:.4,pointRadius:3}]},options:{maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{ticks:{callback:v=>v+'$'}}}}};
  if(pnlChart){pnlChart.data=cfg.data;pnlChart.options=cfg.options;pnlChart.update();}
  else{pnlChart=new Chart(cv.getContext('2d'),cfg);}
}
function setFilter(v){curFilter=v;load();}
function drawPairs(rows){
  const g={};
  rows.forEach(x=>{const k=x.symbol||'?';g[k]=g[k]||{n:0,w:0,net:0};g[k].n++;if((+x.net||0)>0)g[k].w++;g[k].net+=(+x.net||0);});
  const ks=Object.keys(g).sort((a,b)=>g[b].net-g[a].net);
  if(!ks.length){document.getElementById('pairs').innerHTML='<p class="text-sm text-secondary mb-0">Tidak ada data pada rentang ini.</p>';return;}
  let h='<div class="table-responsive"><table class="table align-items-center table-hover mb-0"><thead><tr><th class="text-uppercase text-secondary text-xs font-weight-bolder text-start">Pair</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Close</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Win</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">WinRate</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Net USD</th></tr></thead><tbody>';
  ks.forEach(k=>{const s=g[k];const wr=Math.round(s.w/s.n*100);const net=Math.round(s.net*100)/100;
    h+='<tr><td class="font-weight-bold text-sm text-start">'+esc(k)+'</td><td class="text-sm text-end">'+s.n+'</td><td class="text-sm text-end">'+s.w+'</td><td class="text-sm text-end"><span class="badge badge-sm '+(wr>=50?'bg-gradient-success':(wr>=30?'bg-gradient-warning':'bg-gradient-danger'))+'">'+wr+'%</span></td><td class="text-sm text-end font-weight-bold '+(net>0?'text-success':(net<0?'text-danger':'text-secondary'))+'">'+(net>=0?'+':'')+net+'</td></tr>';});
  document.getElementById('pairs').innerHTML=h+'</tbody></table></div>';
}
let calY=0, calM=0, lastClosed=[];
const CAL_BULAN=['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
const CAL_DOW=['Min','Sen','Sel','Rab','Kam','Jum','Sab'];
function calInit(){const p=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Jakarta',year:'numeric',month:'2-digit'}).format(Date.now()).split('-');calY=+p[0];calM=+p[1];}
function calMove(d){calM+=d;if(calM<1){calM=12;calY--;}if(calM>12){calM=1;calY++;}drawCal(lastClosed);}
function calToday(){calInit();drawCal(lastClosed);}
function calDay(ds){document.getElementById('f-from').value=ds;document.getElementById('f-to').value=ds;dateFrom=ds;dateTo=ds;load();}
function calFmt(v){return (v>=0?'+':'')+(Math.round(v*100)/100);}
function drawCal(closed){
  lastClosed=closed||[];
  document.getElementById('cal-title').textContent=CAL_BULAN[calM-1]+' '+calY;
  const sums={};
  lastClosed.forEach(x=>{const d=wib(x.close_time);sums[d]=(sums[d]||0)+(+x.net||0);});
  const key=calY+'-'+(calM<10?'0'+calM:''+calM);
  let mNet=0,mW=0,mN=0;
  lastClosed.forEach(x=>{if(wib(x.close_time).indexOf(key)===0){mNet+=(+x.net||0);mN++;if((+x.net||0)>0)mW++;}});
  document.getElementById('cal-sub').textContent=mN?('Net '+calFmt(mNet)+' USD · win '+mW+'/'+mN):'Belum ada close bulan ini.';
  const dim=new Date(Date.UTC(calY,calM,0)).getUTCDate();
  const off=new Date(Date.UTC(calY,calM-1,1)).getUTCDay();
  const today=wib(Date.now()/1000);
  let h='<div class="cal-grid">';
  CAL_DOW.forEach(d=>{h+='<div class="cal-dow">'+d+'</div>';});
  for(let i=0;i<off;i++){h+='<div></div>';}
  for(let d=1;d<=dim;d++){
    const ds=key+'-'+(d<10?'0'+d:''+d);
    if(sums[ds]!==undefined){
      const v=sums[ds];
      h+='<div class="cal-cell has '+(v>0?'cal-win':(v<0?'cal-loss':''))+(ds===today?' cal-today':'')+'" onclick="calDay(\''+ds+'\')"><div class="cal-num">'+d+'</div><div class="cal-net">'+calFmt(v)+'</div></div>';
    }else{
      h+='<div class="cal-cell cal-dim'+(ds===today?' cal-today':'')+'"><div class="cal-num">'+d+'</div></div>';
    }
  }
  document.getElementById('cal').innerHTML=h+'</div>';
}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function mdInline(h){h=h.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');return h.replace(/(^|[^*\w])\*([^*\n]+?)\*/g,'$1<em>$2</em>');}
function md(s){const lines=esc(s).split('\n');let out='',inUl=false;for(const ln of lines){const t=ln.trim();const m=t.match(/^-\s+(.*)/);const hd=t.match(/^\*\*(.+?)\*\*$/);if(m){if(!inUl){out+='<ul class="mb-1 ps-3">';inUl=true;}out+='<li>'+mdInline(m[1])+'</li>';}else{if(inUl){out+='</ul>';inUl=false;}if(hd){out+='<div class="ai-sec">'+hd[1]+'</div>';}else{out+=(t?mdInline(t)+'<br>':'<br>');}}}if(inUl)out+='</ul>';return out;}
function dt(ts){return new Date(ts*1000).toLocaleString();}
async function load(){
  try{
    const r=await fetch('api.php',{headers:{'Accept':'application/json'}}).then(r=>r.json());
    try{document.getElementById('meta').textContent='update '+((r.meta||{}).updated||'-');}catch(_){}
    const sig=JSON.stringify([(r.closed||[]).map(x=>x.position_id+':'+x.net+':'+x.hasil),((r.report||{}).updated||'')+((r.memory||{}).updated||''),r.open||[],curFilter,dateFrom,dateTo]);
    if(sig===lastSig)return; lastSig=sig;
    const acc=r.account||{};
    document.getElementById('acc').textContent=(acc.login?('Akun '+acc.login+' · '+(acc.server||'')):'');
    document.getElementById('acc-sub').textContent=(acc.server||'MT5')+' · Akun '+(acc.login||'…')+' · '+(acc.currency||'USD');
    document.getElementById('st-bal').textContent=(acc.balance!=null?acc.balance+' USD':'–');
    document.getElementById('st-eq').textContent=(acc.equity!=null?acc.equity+' USD':'–');
    const closed=r.closed||[];
    const wins=closed.filter(x=>(x.net||0)>0).length;
    const net=closed.reduce((a,x)=>a+(+x.net||0),0);
    document.getElementById('st-wr').textContent=closed.length?Math.round(wins/closed.length*100)+'% ('+wins+'/'+closed.length+')':'–';
    document.getElementById('st-net').textContent=(net>=0?'+':'')+Math.round(net*100)/100+' USD';
    const rep=r.report||{};
    document.getElementById('rep-body').innerHTML=rep.eval?md(rep.eval):'Belum ada laporan — terbentuk otomatis tiap 1 jam.';
    document.getElementById('rep-meta').textContent=rep.updated?('Diperbarui '+rep.updated+' · '+(rep.n_trades||0)+' transaksi'):'menunggu laporan pertama…';
    document.getElementById('rep-mem').innerHTML=(r.memory&&r.memory.text)?md(r.memory.text):'Belum ada memori.';
    drawPnl(closed);
    drawCal(closed);
    const open=r.open||[];
    document.getElementById('open').innerHTML=open.length
      ?'<table class="table align-items-center table-hover mb-0"><thead><tr><th class="text-uppercase text-secondary text-xs font-weight-bolder text-start">Simbol</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-start">Side</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Lot</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Open</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">SL</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">TP</th><th class="text-uppercase text-secondary text-xs font-weight-bolder text-end">Floating</th></tr></thead><tbody>'
       +open.map(p=>{const buy=p.type===0;const fl=(+p.profit||0);return '<tr><td class="font-weight-bold text-sm text-start">'+esc(p.symbol)+'</td><td class="text-start"><span class="badge badge-sm '+(buy?'bg-gradient-success':'bg-gradient-danger')+'">'+(buy?'BUY':'SELL')+'</span></td><td class="text-sm text-end">'+p.volume+'</td><td class="text-sm text-end">'+p.price_open+'</td><td class="text-sm text-end">'+p.sl+'</td><td class="text-sm text-end">'+p.tp+'</td><td class="text-sm text-end font-weight-bold '+(fl>0?'text-success':(fl<0?'text-danger':'text-secondary'))+'">'+(fl>=0?'+':'')+p.profit+'</td></tr>';}).join('')+'</tbody></table>'
      :'<p class="text-sm text-secondary mb-0">Tidak ada posisi open.</p>';
    const rows=closed.filter(x=>!curFilter||(x.hasil||'').indexOf(curFilter)===0).filter(x=>{const d=wib(x.close_time);return (!dateFrom||d>=dateFrom)&&(!dateTo||d<=dateTo);});
    drawPairs(rows);
    document.getElementById('list-count').textContent=rows.length;
    document.getElementById('list').innerHTML=rows.length?rows.map((x,i)=>{
      const cls=(x.net||0)>0?'pos-win':((x.net||0)<0?'pos-loss':'');
      const badge=(x.net||0)>0?'bg-gradient-success':((x.net||0)<0?'bg-gradient-danger':'bg-gradient-secondary');
      return '<div class="card pos-card '+cls+' '+(i<rows.length-1?'mb-3':'mb-0')+'"><div class="card-body">'
        +'<h6 class="mb-1">'+esc(x.symbol)+' '+x.type+' '+x.volume+' <span class="badge '+badge+'">'+esc(x.hasil)+' '+(x.net>=0?'+':'')+x.net+' USD</span></h6>'
        +'<p class="text-xs text-secondary mb-0">open '+x.open_price+' ('+dt(x.open_time)+') → close '+x.close_price+' ('+dt(x.close_time)+') · SL:'+x.sl+' TP:'+x.tp+' · durasi:'+x.durasi_mnt+' mnt · ID:'+x.position_id+'</p>'
        +'</div></div>';
    }).join(''):'<p class="text-sm text-secondary mb-0">Tidak ada posisi close pada rentang tanggal ini.</p>';
  }catch(e){try{document.getElementById('meta').textContent='gagal memuat ('+new Date().toLocaleTimeString('id-ID',{timeZone:'Asia/Jakarta',hour12:false})+')';}catch(_){}}
}
dateFrom=wib(Date.now()/1000);dateTo=dateFrom;document.getElementById('f-from').value=dateFrom;document.getElementById('f-to').value=dateTo;
calInit();
load(); setInterval(load,10000);
function tick(){try{document.getElementById('clock').textContent=new Date().toLocaleTimeString('id-ID',{timeZone:'Asia/Jakarta',hour12:false})+' WIB';}catch(e){}}
tick(); setInterval(tick,1000);
</script>
</body>
</html>
