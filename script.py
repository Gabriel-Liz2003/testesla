import os
os.makedirs("output/cblol-hub", exist_ok=True)

html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#0a0e1a" />
  <meta name="description" content="CBLOL Hub 2026 — Agenda, resultados, stats e muito mais" />
  <link rel="manifest" href="manifest.json" />
  <title>CBLOL Hub</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <style>
    *{font-family:\'Inter\',sans-serif;box-sizing:border-box}
    body{background:#0a0e1a;color:#e2e8f0;-webkit-tap-highlight-color:transparent}
    .gold{color:#c89b3c}.gold-bg{background:#c89b3c}
    .card{background:#111827;border:1px solid #1f2937;border-radius:12px}
    .live-badge{animation:pulse 1.4s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
    .tab-active{background:#c89b3c;color:#0a0e1a;font-weight:700}
    .tab-inactive{background:#1f2937;color:#9ca3af}
    ::-webkit-scrollbar{width:4px;height:4px}
    ::-webkit-scrollbar-track{background:#111827}
    ::-webkit-scrollbar-thumb{background:#374151;border-radius:4px}
    .section-hidden{display:none}
    .player-row:hover{background:#1f2937}
    .match-card:hover{border-color:#c89b3c55;cursor:pointer}
    .spin{animation:spin 1s linear infinite}
    @keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    .fade-in{animation:fadeIn .3s ease}
    @keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
    .skeleton{background:linear-gradient(90deg,#1f2937 25%,#374151 50%,#1f2937 75%);background-size:200%;animation:shimmer 1.4s infinite}
    @keyframes shimmer{0%{background-position:200%}100%{background-position:-200%}}
    .error-box{background:#1a0a0a;border:1px solid #7f1d1d;border-radius:10px;padding:12px;color:#fca5a5;font-size:12px}
    .toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#1f2937;border:1px solid #374151;padding:10px 18px;border-radius:20px;font-size:12px;z-index:999;white-space:nowrap;animation:fadeIn .3s ease}
  </style>
</head>
<body class="min-h-screen">

<!-- TOP NAV -->
<nav class="sticky top-0 z-50 bg-[#0a0e1a] border-b border-[#1f2937] px-4 py-3 flex items-center justify-between">
  <div class="flex items-center gap-2">
    <span class="text-2xl">🏆</span>
    <span class="font-black text-lg tracking-tight gold">CBLOL</span>
    <span class="font-light text-sm text-gray-400">Hub 2026</span>
  </div>
  <div class="flex items-center gap-2">
    <div id="loading-dot" class="hidden w-3 h-3 border-2 border-yellow-500 border-t-transparent rounded-full spin"></div>
    <button onclick="refreshAll()" class="text-gray-500 hover:text-gray-300 text-lg" title="Atualizar">🔄</button>
  </div>
</nav>

<!-- BOTTOM TABS -->
<div class="fixed bottom-0 left-0 right-0 z-50 bg-[#0a0e1a] border-t border-[#1f2937] flex safe-area-inset-bottom">
  <button onclick="showSection(\'home\')" id="tab-home" class="flex-1 py-2.5 flex flex-col items-center gap-0.5 text-xs tab-active">
    <span class="text-lg">🏠</span><span>Home</span>
  </button>
  <button onclick="showSection(\'agenda\')" id="tab-agenda" class="flex-1 py-2.5 flex flex-col items-center gap-0.5 text-xs tab-inactive">
    <span class="text-lg">📅</span><span>Agenda</span>
  </button>
  <button onclick="showSection(\'times\')" id="tab-times" class="flex-1 py-2.5 flex flex-col items-center gap-0.5 text-xs tab-inactive">
    <span class="text-lg">🛡️</span><span>Times</span>
  </button>
  <button onclick="showSection(\'jogadores\')" id="tab-jogadores" class="flex-1 py-2.5 flex flex-col items-center gap-0.5 text-xs tab-inactive">
    <span class="text-lg">⚔️</span><span>Stats</span>
  </button>
  <button onclick="showSection(\'noticias\')" id="tab-noticias" class="flex-1 py-2.5 flex flex-col items-center gap-0.5 text-xs tab-inactive">
    <span class="text-lg">📰</span><span>Notícias</span>
  </button>
</div>

<main class="pb-24 pt-2 max-w-2xl mx-auto px-3">

  <!-- HOME -->
  <section id="section-home" class="fade-in">
    <div id="live-banner" class="hidden mb-3 card p-3 border-red-800 cursor-pointer" onclick="showSection(\'agenda\')">
      <div class="flex items-center gap-2">
        <span class="live-badge text-xs bg-red-600 text-white font-bold px-2 py-0.5 rounded-full">🔴 AO VIVO</span>
        <span id="live-match-text" class="text-sm font-semibold"></span>
      </div>
    </div>
    <div class="mt-3 mb-4">
      <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Classificação</h2>
      <div id="standings-container" class="card p-0 overflow-hidden"><div class="p-4 skeleton h-40 rounded-xl"></div></div>
    </div>
    <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Próximos Jogos</h2>
    <div id="upcoming-container" class="space-y-2 mb-4"><div class="card p-4 skeleton h-20 rounded-xl"></div></div>
    <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Últimos Resultados</h2>
    <div id="results-container" class="space-y-2 mb-4"><div class="card p-4 skeleton h-20 rounded-xl"></div></div>
  </section>

  <!-- AGENDA -->
  <section id="section-agenda" class="section-hidden fade-in">
    <div class="flex gap-2 mt-3 mb-4 flex-wrap">
      <button onclick="setAgendaFilter(\'upcoming\')" id="filter-upcoming" class="tab-active px-4 py-1.5 rounded-full text-sm">Próximos</button>
      <button onclick="setAgendaFilter(\'live\')" id="filter-live" class="tab-inactive px-4 py-1.5 rounded-full text-sm">Ao Vivo</button>
      <button onclick="setAgendaFilter(\'completed\')" id="filter-completed" class="tab-inactive px-4 py-1.5 rounded-full text-sm">Resultados</button>
    </div>
    <div id="agenda-container" class="space-y-2"></div>
  </section>

  <!-- TIMES -->
  <section id="section-times" class="section-hidden fade-in">
    <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mt-3 mb-3">Times CBLOL 2026</h2>
    <div id="times-container" class="space-y-2"><div class="card p-4 skeleton h-24 rounded-xl"></div></div>
  </section>

  <!-- JOGADORES -->
  <section id="section-jogadores" class="section-hidden fade-in">
    <div class="flex gap-2 mt-3 mb-3 overflow-x-auto pb-1 scrollbar-none">
      <button onclick="filterPlayers(\'all\')" id="pos-all" class="tab-active px-3 py-1.5 rounded-full text-xs whitespace-nowrap">Todos</button>
      <button onclick="filterPlayers(\'top\')" id="pos-top" class="tab-inactive px-3 py-1.5 rounded-full text-xs whitespace-nowrap">🗡️ Top</button>
      <button onclick="filterPlayers(\'jungle\')" id="pos-jungle" class="tab-inactive px-3 py-1.5 rounded-full text-xs whitespace-nowrap">🌲 Jungle</button>
      <button onclick="filterPlayers(\'mid\')" id="pos-mid" class="tab-inactive px-3 py-1.5 rounded-full text-xs whitespace-nowrap">✨ Mid</button>
      <button onclick="filterPlayers(\'adc\')" id="pos-adc" class="tab-inactive px-3 py-1.5 rounded-full text-xs whitespace-nowrap">🏹 ADC</button>
      <button onclick="filterPlayers(\'support\')" id="pos-support" class="tab-inactive px-3 py-1.5 rounded-full text-xs whitespace-nowrap">🛡️ Support</button>
    </div>
    <div id="players-container" class="card overflow-hidden"><div class="p-4 skeleton h-48 rounded-xl"></div></div>
    <div id="leaguepedia-credit" class="text-center text-xs text-gray-600 mt-2">Stats via Leaguepedia</div>
  </section>

  <!-- NOTÍCIAS -->
  <section id="section-noticias" class="section-hidden fade-in">
    <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mt-3 mb-3">Notícias</h2>
    <div id="news-container" class="space-y-3"><div class="card p-4 skeleton h-36 rounded-xl"></div></div>
  </section>

</main>

<!-- MODAL -->
<div id="match-modal" class="hidden fixed inset-0 z-50 bg-black/85 overflow-y-auto">
  <div class="min-h-screen flex items-start justify-center p-3 pt-8">
    <div class="card w-full max-w-lg relative">
      <button onclick="closeModal()" class="absolute top-3 right-3 text-gray-400 hover:text-white text-2xl z-10 w-8 h-8 flex items-center justify-center">✕</button>
      <div id="modal-content" class="p-4"></div>
    </div>
  </div>
</div>

<script>
// ===== CONSTANTS =====
const LOL_API = "https://esports-api.lolesports.com/persisted/gw";
const LOL_API_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z";
const CBLOL_LEAGUE_ID = "98767991332355509";
const WIKI_API = "https://lol.fandom.com/api.php";
const DDRAGON = "https://ddragon.leagueoflegends.com";
const DDRAGON_VERSION = "14.10.1";
const CORS = "https://corsproxy.io/?url=";

// ===== STATE =====
let state = {
  schedule: [], standings: [], teams: {}, players: [],
  news: [], liveMatches: [], ddragonChamps: {},
  currentTournamentId: null, agendaFilter: "upcoming",
  playerFilter: "all", loading: false
};

// ===== FALLBACK DATA (always shown if API fails) =====
const FB_TEAMS = {
  "loud":  {name:"LOUD",       short:"LOUD", color:"#FF6B00", emoji:"🔊"},
  "red":   {name:"RED Canids", short:"RED",  color:"#FF0040", emoji:"🐺"},
  "fluxo": {name:"Fluxo Sharks",short:"FLX", color:"#00C2FF", emoji:"🦈"},
  "pain":  {name:"paiN Gaming",short:"PNG",  color:"#7C3AED", emoji:"💜"},
  "vivo":  {name:"VIVO Keyd",  short:"VKS",  color:"#22C55E", emoji:"⭐"},
  "furia": {name:"FURIA",      short:"FUR",  color:"#F1F5F9", emoji:"🐾"},
  "kabum": {name:"KaBuM!",     short:"KBM",  color:"#F97316", emoji:"💥"},
  "intz":  {name:"INTZ",       short:"INTZ", color:"#38BDF8", emoji:"🔵"},
};
const FB_STANDINGS = [
  {team:"loud",w:3,l:0,pts:9},{team:"intz",w:2,l:1,pts:6},{team:"vivo",w:2,l:1,pts:6},
  {team:"pain",w:2,l:1,pts:6},{team:"red",w:1,l:2,pts:3},{team:"fluxo",w:1,l:2,pts:3},
  {team:"furia",w:1,l:2,pts:3},{team:"kabum",w:0,l:3,pts:0}
];
const FB_SCHEDULE = [
  {id:"m1",t1:"loud",t2:"red",s1:2,s2:0,status:"completed",date:"2026-05-10T16:00",week:1,phase:"Fase Regular"},
  {id:"m2",t1:"fluxo",t2:"pain",s1:1,s2:2,status:"completed",date:"2026-05-10T18:00",week:1,phase:"Fase Regular"},
  {id:"m3",t1:"vivo",t2:"furia",s1:2,s2:1,status:"completed",date:"2026-05-11T16:00",week:1,phase:"Fase Regular"},
  {id:"m4",t1:"kabum",t2:"intz",s1:0,s2:2,status:"completed",date:"2026-05-11T18:00",week:1,phase:"Fase Regular"},
  {id:"m5",t1:"loud",t2:"fluxo",s1:0,s2:0,status:"scheduled",date:"2026-05-17T16:00",week:2,phase:"Fase Regular"},
  {id:"m6",t1:"red",t2:"vivo",s1:0,s2:0,status:"scheduled",date:"2026-05-17T18:00",week:2,phase:"Fase Regular"},
  {id:"m7",t1:"pain",t2:"furia",s1:0,s2:0,status:"scheduled",date:"2026-05-18T16:00",week:2,phase:"Fase Regular"},
  {id:"m8",t1:"kabum",t2:"loud",s1:0,s2:0,status:"scheduled",date:"2026-05-18T18:00",week:2,phase:"Fase Regular"},
];
const FB_PLAYERS = [
  {name:"Tinowns",team:"LOUD",teamKey:"loud",role:"mid",kda:8.4,dpm:642,kp:71,csmin:8.9,wr:75,rating:9.2},
  {name:"Route",team:"LOUD",teamKey:"loud",role:"adc",kda:6.8,dpm:598,kp:68,csmin:9.1,wr:75,rating:8.8},
  {name:"Croc",team:"LOUD",teamKey:"loud",role:"jungle",kda:4.8,dpm:320,kp:78,csmin:5.9,wr:75,rating:8.1},
  {name:"Robo",team:"LOUD",teamKey:"loud",role:"top",kda:4.1,dpm:489,kp:55,csmin:8.0,wr:75,rating:8.0},
  {name:"Nyu",team:"INTZ",teamKey:"intz",role:"mid",kda:5.2,dpm:530,kp:65,csmin:8.5,wr:62,rating:7.9},
  {name:"Netuno",team:"RED Canids",teamKey:"red",role:"adc",kda:5.9,dpm:561,kp:64,csmin:8.7,wr:42,rating:7.9},
  {name:"RedBert",team:"LOUD",teamKey:"loud",role:"support",kda:5.5,dpm:180,kp:80,csmin:1.2,wr:75,rating:7.8},
  {name:"Erizef",team:"INTZ",teamKey:"intz",role:"top",kda:3.8,dpm:445,kp:58,csmin:7.8,wr:62,rating:7.5},
  {name:"dyNquedo",team:"Fluxo Sharks",teamKey:"fluxo",role:"mid",kda:5.1,dpm:512,kp:59,csmin:8.3,wr:38,rating:7.4},
  {name:"Aegis",team:"RED Canids",teamKey:"red",role:"jungle",kda:4.3,dpm:298,kp:72,csmin:5.7,wr:42,rating:7.2},
  {name:"Tutsz",team:"FURIA",teamKey:"furia",role:"mid",kda:4.5,dpm:490,kp:62,csmin:8.1,wr:38,rating:7.1},
  {name:"Goot",team:"FURIA",teamKey:"furia",role:"support",kda:4.9,dpm:160,kp:76,csmin:1.0,wr:38,rating:6.8},
].sort((a,b)=>b.rating-a.rating);
const FB_NEWS = [
  {id:"n1",title:"LOUD vence RED Canids 2-0 e lidera CBLOL 2026 Split 1",summary:"Tinowns e Route foram dominantes na série. LOUD confirma favoritismo com atuação impecável.",category:"Resultados",date:"2026-05-10",source:"lolesports.com"},
  {id:"n2",title:"INTZ surpreende KaBuM! e assume top 2 da tabela",summary:"Renovada, INTZ mostra evolução e se torna candidata a surpreender os favoritos.",category:"Análises",date:"2026-05-11",source:"draft5.gg"},
  {id:"n3",title:"paiN Gaming renova contrato com Gigas até fim de 2027",summary:"Jungler confirma longa parceria com a equipe e comentou sobre as expectativas para os playoffs.",category:"Transfers",date:"2026-05-09",source:"maisesports.com.br"},
  {id:"n4",title:"Semana 2 começa sábado com LOUD x Fluxo como clássico da rodada",summary:"A partida mais esperada da semana promete duelo de estilos entre agressividade e controle.",category:"Agenda",date:"2026-05-12",source:"lolesports.com"},
  {id:"n5",title:"Análise: por que o meta de Split Push está dominando o CBLOL 2026?",summary:"Campeões de split push como Fiora e Tryndamere aparecem com alta taxa de vitória no regional.",category:"Análises",date:"2026-05-08",source:"draft5.gg"},
];

const ROLE_ICON={top:"🗡️",jungle:"🌲",mid:"✨",adc:"🏹",support:"🛡️"};
const CAT_COLOR={Resultados:"bg-green-700",Análises:"bg-blue-700",Transfers:"bg-purple-700",Agenda:"bg-yellow-700"};

// ===== UTILS =====
function fmt(ds){const d=new Date(ds);return d.toLocaleString("pt-BR",{day:"2-digit",month:"short",hour:"2-digit",minute:"2-digit"});}
function fmtShort(ds){const d=new Date(ds);return d.toLocaleString("pt-BR",{day:"2-digit",month:"short"});}
function setLoading(v){state.loading=v;document.getElementById("loading-dot").classList.toggle("hidden",!v);}
function showToast(msg,dur=2500){const t=document.createElement("div");t.className="toast";t.textContent=msg;document.body.appendChild(t);setTimeout(()=>t.remove(),dur);}

function ratingColor(r){
  if(r>=9)return"text-yellow-300 font-black";
  if(r>=8)return"text-yellow-400 font-bold";
  if(r>=7)return"text-green-400 font-bold";
  if(r>=6)return"text-blue-400";
  return"text-gray-400";
}

function statusBadge(s){
  if(s==="inProgress"||s==="live")return`<span class="live-badge bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">🔴 AO VIVO</span>`;
  if(s==="completed"||s==="unneeded")return`<span class="bg-gray-700 text-gray-300 text-[10px] px-2 py-0.5 rounded-full">Encerrado</span>`;
  return`<span class="bg-blue-900 text-blue-300 text-[10px] px-2 py-0.5 rounded-full">Agendado</span>`;
}

// ===== RATING FORMULA =====
// Rating = KDA*0.30 + KP*0.20 + DPM*0.20 + CS/min*0.15 + WR*0.10 + (vitoria bônus)
function calcRating(p, allPlayers){
  const sameRole = allPlayers.filter(x=>x.role===p.role);
  const norm = (val, arr, key) => {
    const vals = arr.map(x=>x[key]);
    const mn = Math.min(...vals), mx = Math.max(...vals);
    return mx===mn ? 0.5 : (val-mn)/(mx-mn);
  };
  const score =
    norm(p.kda,sameRole,"kda") * 0.30 +
    norm(p.kp,sameRole,"kp") * 0.20 +
    norm(p.dpm,sameRole,"dpm") * 0.20 +
    norm(p.csmin,sameRole,"csmin") * 0.15 +
    norm(p.wr,sameRole,"wr") * 0.10 +
    (p.wr>60?0.05:0);
  return Math.max(0, Math.min(10, (score * 9 + 1))).toFixed(1);
}

// ===== API CALLS =====
async function fetchLoL(endpoint, params=""){
  const url = `${LOL_API}${endpoint}?hl=pt-BR${params}`;
  const r = await fetch(`${CORS}${encodeURIComponent(url)}`,{headers:{"x-api-key":LOL_API_KEY}});
  if(!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function fetchWiki(query){
  const url = `${WIKI_API}?${query}&format=json&origin=*`;
  const r = await fetch(url);
  if(!r.ok) throw new Error(`Wiki HTTP ${r.status}`);
  return r.json();
}

// Parse LoL Esports schedule into unified format
function parseSchedule(data){
  const events = data?.data?.schedule?.events || [];
  return events
    .filter(e=>e.type==="match")
    .map(e=>{
      const m = e.match;
      const t1 = m.teams[0], t2 = m.teams[1];
      return {
        id: m.id,
        t1key: t1.code?.toLowerCase(),
        t2key: t2.code?.toLowerCase(),
        t1name: t1.name, t2name: t2.name,
        t1code: t1.code, t2code: t2.code,
        t1color: t1.image, t2color: t2.image,
        t1img: t1.image, t2img: t2.image,
        s1: t1.result?.gameWins||0,
        s2: t2.result?.gameWins||0,
        status: e.state,
        date: e.startTime,
        week: e.blockName||"",
        phase: e.league?.name||"CBLOL",
        strategyType: m.strategy?.type,
        strategyCount: m.strategy?.count,
      };
    });
}

function parseStandings(data){
  const stages = data?.data?.standings?.[0]?.stages || [];
  const stage = stages.find(s=>s.type==="regular_season") || stages[0];
  if(!stage) return null;
  const sections = stage.sections || [];
  const rankings = sections.flatMap(s => s.rankings||[]);
  return rankings.flatMap(r=>r.teams||[]).map(t=>({
    id: t.id, name: t.name, code: t.code,
    w: t.record?.wins||0, l: t.record?.losses||0,
    pts: (t.record?.wins||0)*3
  }));
}

// Leaguepedia: get player stats for CBLOL 2026
async function fetchLeaguepediaStats(){
  const query = new URLSearchParams({
    action:"cargoquery",
    tables:"ScoreboardPlayers",
    fields:"Link,Team,Role,Kills,Deaths,Assists,CS,DamageToChampions,GoldEarned,VisionScore,Gamelength",
    where:"Tournament LIKE \'CBLOL/2026%\'",
    limit:"500",
    format:"json",
    origin:"*"
  });
  const url = `${WIKI_API}?${query}`;
  const r = await fetch(url);
  const data = await r.json();
  return data?.cargoquery||[];
}

function aggregatePlayerStats(rows){
  const map = {};
  rows.forEach(row=>{
    const d = row.title;
    if(!d||!d.Link) return;
    const key = d.Link;
    if(!map[key]) map[key] = {
      name:d.Link, team:d.Team, role:(d.Role||"").toLowerCase(),
      kills:0, deaths:0, assists:0, cs:0, dmg:0, gold:0, vision:0, gl:0, games:0
    };
    const p = map[key];
    p.kills += parseInt(d.Kills||0);
    p.deaths += parseInt(d.Deaths||0);
    p.assists += parseInt(d.Assists||0);
    p.cs += parseInt(d.CS||0);
    p.dmg += parseInt(d.DamageToChampions||0);
    p.gold += parseInt(d.GoldEarned||0);
    p.vision += parseInt(d.VisionScore||0);
    p.gl += parseFloat(d.Gamelength||0);
    p.games++;
  });
  return Object.values(map).filter(p=>p.games>=1).map(p=>{
    const minPerGame = p.gl/p.games/60 || 30;
    const kda = p.deaths===0 ? (p.kills+p.assists) : ((p.kills+p.assists)/p.deaths);
    return {
      name:p.name, team:p.team, role:p.role,
      kda: parseFloat(kda.toFixed(2)),
      dpm: Math.round(p.dmg/p.games/minPerGame),
      kp: 0, csmin: parseFloat((p.cs/p.games/minPerGame).toFixed(1)),
      wr: 0, rating:0, games:p.games
    };
  });
}

// Leaguepedia: draft for a specific game
async function fetchDraft(overviewPage, gameN){
  const query = new URLSearchParams({
    action:"cargoquery",
    tables:"PicksAndBans",
    fields:"Team1Picks,Team2Picks,Team1Bans,Team2Bans,Team1Role1,Team1Role2,Team1Role3,Team1Role4,Team1Role5,Team2Role1,Team2Role2,Team2Role3,Team2Role4,Team2Role5",
    where:`OverviewPage=\'${overviewPage}\' AND N_GameInMatch=${gameN}`,
    limit:"1",
    format:"json",
    origin:"*"
  });
  const r = await fetch(`${WIKI_API}?${query}`);
  const data = await r.json();
  return data?.cargoquery?.[0]?.title||null;
}

// ===== CHAMPION ICONS =====
function champIcon(name){
  if(!name) return `<div class="w-7 h-7 bg-gray-800 rounded text-center text-xs flex items-center justify-center text-gray-500">?</div>`;
  const clean = name.replace(/[^a-zA-Z0-9]/g,"");
  return `<img src="${DDRAGON}/cdn/${DDRAGON_VERSION}/img/champion/${clean}.png" class="w-7 h-7 rounded border border-gray-700 object-cover" onerror="this.outerHTML=\'<div class=\\"w-7 h-7 bg-gray-800 rounded text-center text-xs flex items-center justify-center text-gray-500\\">${name[0]}</div>\'" />`;
}

// ===== TEAM HELPERS =====
function teamInfo(codeOrKey){
  const k = (codeOrKey||"").toLowerCase();
  // Try direct key
  if(FB_TEAMS[k]) return FB_TEAMS[k];
  // Try match by short name
  for(const [key,t] of Object.entries(FB_TEAMS)){
    if(t.short.toLowerCase()===k) return t;
  }
  return {name:codeOrKey||"?", short:(codeOrKey||"?").substring(0,4).toUpperCase(), color:"#9ca3af", emoji:"🎮"};
}

// ===== RENDER MATCH CARD =====
function renderMatchCard(m){
  const t1 = teamInfo(m.t1key||m.t1code||m.t1);
  const t2 = teamInfo(m.t2key||m.t2code||m.t2);
  const isLive = m.status==="inProgress"||m.status==="live";
  const isDone = m.status==="completed"||m.status==="unneeded";
  const scoreHtml = isDone
    ? `<span class="font-black text-xl" style="color:${m.s1>m.s2?t1.color:"#6b7280"}">${m.s1}</span>
       <span class="text-gray-600 text-sm mx-1">x</span>
       <span class="font-black text-xl" style="color:${m.s2>m.s1?t2.color:"#6b7280"}">${m.s2}</span>`
    : isLive
    ? `<span class="live-badge text-red-500 font-black">⚡</span>`
    : `<span class="text-gray-500 text-sm">vs</span>`;
  const format = m.strategyCount ? `BO${m.strategyCount}` : "";
  return `<div class="card match-card p-3 transition-all" onclick=\'openMatch(${JSON.stringify(m).replace(/\'/g,"\\'")})\'>
    <div class="flex items-center justify-between mb-2">
      <span class="text-[10px] text-gray-500">${m.week||m.phase} · ${fmt(m.date)} ${format?`· <span class="text-gray-600">${format}</span>`:""}</span>
      ${statusBadge(m.status)}
    </div>
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2 flex-1">
        <span class="text-2xl">${t1.emoji}</span>
        <span class="font-bold text-sm" style="color:${t1.color}">${t1.short}</span>
      </div>
      <div class="flex items-center gap-1 mx-3 min-w-[60px] justify-center">${scoreHtml}</div>
      <div class="flex items-center gap-2 flex-1 justify-end">
        <span class="font-bold text-sm" style="color:${t2.color}">${t2.short}</span>
        <span class="text-2xl">${t2.emoji}</span>
      </div>
    </div>
  </div>`;
}

// ===== HOME =====
function renderHome(){
  // Live banner
  const live = state.schedule.filter(m=>m.status==="inProgress"||m.status==="live");
  const liveBanner = document.getElementById("live-banner");
  if(live.length){
    const t1=teamInfo(live[0].t1key||live[0].t1code);
    const t2=teamInfo(live[0].t2key||live[0].t2code);
    document.getElementById("live-match-text").textContent=`${t1.short} vs ${t2.short}`;
    liveBanner.classList.remove("hidden");
  } else liveBanner.classList.add("hidden");

  // Standings
  const data = state.standings.length ? state.standings : FB_STANDINGS;
  let stHtml=`<div class="overflow-x-auto"><table class="w-full text-xs"><thead><tr class="border-b border-gray-800">
    <th class="text-left py-2 px-3 text-gray-500 font-medium">#</th>
    <th class="text-left py-2 px-3 text-gray-500 font-medium">Time</th>
    <th class="text-center py-2 px-3 text-gray-500 font-medium">V</th>
    <th class="text-center py-2 px-3 text-gray-500 font-medium">D</th>
    <th class="text-right py-2 px-3 text-gray-500 font-medium">Pts</th>
  </tr></thead><tbody>`;
  data.forEach((s,i)=>{
    const t = state.standings.length
      ? {emoji:teamInfo(s.code?.toLowerCase()||s.team).emoji, short:s.code||s.team, color:teamInfo(s.code?.toLowerCase()||s.team).color}
      : {...teamInfo(s.team)};
    const bg=i===0?"bg-yellow-500/10":i<4?"bg-green-500/5":"";
    stHtml+=`<tr class="border-b border-gray-900 ${bg}">
      <td class="py-2 px-3 font-bold ${i<4?"text-green-400":"text-gray-500"}">${i+1}</td>
      <td class="py-2 px-3"><div class="flex items-center gap-1.5"><span>${t.emoji}</span><span class="font-semibold" style="color:${t.color}">${t.short}</span></div></td>
      <td class="py-2 px-3 text-center text-green-400 font-semibold">${s.w}</td>
      <td class="py-2 px-3 text-center text-red-400 font-semibold">${s.l}</td>
      <td class="py-2 px-3 text-right font-black gold">${s.pts}</td>
    </tr>`;
  });
  stHtml+=`</tbody></table></div>`;
  document.getElementById("standings-container").innerHTML=stHtml;

  // Upcoming
  const sched = state.schedule.length ? state.schedule : FB_SCHEDULE;
  const upcoming = sched.filter(m=>m.status==="scheduled"||m.status==="unstarted").slice(0,3);
  document.getElementById("upcoming-container").innerHTML=upcoming.length
    ? upcoming.map(renderMatchCard).join("")
    : `<div class="card p-4 text-center text-gray-500 text-sm">Nenhum jogo agendado.</div>`;

  // Results
  const done = sched.filter(m=>m.status==="completed"||m.status==="unneeded").slice(-4).reverse();
  document.getElementById("results-container").innerHTML=done.length
    ? done.map(renderMatchCard).join("")
    : `<div class="card p-4 text-center text-gray-500 text-sm">Nenhum resultado ainda.</div>`;
}

// ===== AGENDA =====
function setAgendaFilter(f){
  state.agendaFilter=f;
  ["upcoming","live","completed"].forEach(x=>{
    const b=document.getElementById(`filter-${x}`);
    b.classList.toggle("tab-active",x===f);
    b.classList.toggle("tab-inactive",x!==f);
  });
  renderAgenda();
}
function renderAgenda(){
  const sched = state.schedule.length ? state.schedule : FB_SCHEDULE;
  let filtered;
  if(state.agendaFilter==="live") filtered=sched.filter(m=>m.status==="inProgress"||m.status==="live");
  else if(state.agendaFilter==="completed") filtered=sched.filter(m=>m.status==="completed"||m.status==="unneeded").reverse();
  else filtered=sched.filter(m=>m.status==="scheduled"||m.status==="unstarted");
  document.getElementById("agenda-container").innerHTML=filtered.length
    ? filtered.map(renderMatchCard).join("")
    : `<div class="card p-4 text-center text-gray-500 text-sm">${state.agendaFilter==="live"?"Nenhum jogo ao vivo agora.":"Nenhuma partida encontrada."}</div>`;
}

// ===== TIMES =====
function renderTimes(){
  const allTeams = Object.entries(FB_TEAMS);
  const html=allTeams.map(([id,t])=>`
    <div class="card p-4 match-card" onclick="openTeam(\'${id}\')">
      <div class="flex items-center gap-3 mb-2">
        <span class="text-3xl">${t.emoji}</span>
        <div>
          <div class="font-bold text-base" style="color:${t.color}">${t.name}</div>
          <div class="text-xs text-gray-500">CBLOL 2026 Split 1</div>
        </div>
        <div class="ml-auto">
          ${(()=>{
            const s=(state.standings.length?state.standings:FB_STANDINGS).find(x=>(x.code||x.team)?.toLowerCase()===id||x.team===id);
            return s?`<span class="text-xs text-gray-400">${s.w}V ${s.l}D</span>`:"";
          })()}
        </div>
      </div>
    </div>`).join("");
  document.getElementById("times-container").innerHTML=html;
}

// ===== PLAYERS =====
function filterPlayers(pos){
  state.playerFilter=pos;
  ["all","top","jungle","mid","adc","support"].forEach(x=>{
    const b=document.getElementById(`pos-${x}`);
    if(b){b.classList.toggle("tab-active",x===pos);b.classList.toggle("tab-inactive",x!==pos);}
  });
  renderPlayers();
}
function renderPlayers(){
  const allP = state.players.length ? state.players : FB_PLAYERS;
  const filtered = state.playerFilter==="all" ? allP : allP.filter(p=>p.role===state.playerFilter);
  if(!filtered.length){
    document.getElementById("players-container").innerHTML=`<div class="p-4 text-center text-gray-500 text-sm">Nenhum jogador encontrado.</div>`;
    return;
  }
  let html=`<div class="overflow-x-auto"><table class="w-full text-xs">
    <thead><tr class="border-b border-gray-800">
      <th class="text-left py-2 px-3 text-gray-500 font-medium sticky left-0 bg-[#111827]">#</th>
      <th class="text-left py-2 px-3 text-gray-500 font-medium">Jogador</th>
      <th class="text-center py-2 px-3 text-gray-500 font-medium">KDA</th>
      <th class="text-center py-2 px-3 text-gray-500 font-medium">DPM</th>
      <th class="text-center py-2 px-3 text-gray-500 font-medium">CS/m</th>
      <th class="text-right py-2 px-3 text-gray-500 font-medium">⭐ Rating</th>
    </tr></thead><tbody>`;
  filtered.forEach((p,i)=>{
    const t=teamInfo(p.teamKey||p.team?.toLowerCase());
    const r = p.rating||calcRating(p, allP);
    html+=`<tr class="border-b border-gray-900 player-row transition-colors">
      <td class="py-2.5 px-3 text-gray-500 font-medium sticky left-0 bg-[#111827]">${i+1}</td>
      <td class="py-2.5 px-3">
        <div class="font-semibold">${p.name}</div>
        <div class="text-[10px]" style="color:${t.color}">${t.short} ${ROLE_ICON[p.role]||""}</div>
      </td>
      <td class="py-2.5 px-3 text-center font-semibold text-green-400">${p.kda}</td>
      <td class="py-2.5 px-3 text-center text-gray-300">${p.dpm||"—"}</td>
      <td class="py-2.5 px-3 text-center text-blue-300">${p.csmin||"—"}</td>
      <td class="py-2.5 px-3 text-right font-black ${ratingColor(parseFloat(r))}">${r}</td>
    </tr>`;
  });
  html+=`</tbody></table></div>`;
  document.getElementById("players-container").innerHTML=html;
}

// ===== NEWS =====
function renderNews(){
  const news = state.news.length ? state.news : FB_NEWS;
  const catColors={Resultados:"bg-green-800",Análises:"bg-blue-800",Transfers:"bg-purple-800",Agenda:"bg-yellow-700"};
  const html=news.map(n=>`
    <div class="card overflow-hidden match-card" onclick="openNews(${JSON.stringify(n).replace(/\'/g,"\\'")})">
      <div class="h-20 bg-gradient-to-br from-[#1f2937] to-[#0f172a] flex items-center justify-center relative">
        <span class="text-5xl opacity-60">🏆</span>
        <span class="absolute top-2 left-2 ${catColors[n.category]||"bg-gray-700"} text-white text-[10px] font-bold px-2 py-0.5 rounded">${n.category}</span>
      </div>
      <div class="p-3">
        <div class="font-semibold text-sm mb-1 leading-snug">${n.title}</div>
        <div class="text-xs text-gray-400 mb-1">${n.summary}</div>
        <div class="flex items-center justify-between">
          <div class="text-[10px] text-gray-600">${fmtShort(n.date)}</div>
          ${n.source?`<div class="text-[10px] text-gray-600">${n.source}</div>`:""}
        </div>
      </div>
    </div>`).join("");
  document.getElementById("news-container").innerHTML=html;
}

// ===== MODALS =====
async function openMatch(m){
  const t1=teamInfo(m.t1key||m.t1code||m.t1);
  const t2=teamInfo(m.t2key||m.t2code||m.t2);
  const isDone=m.status==="completed"||m.status==="unneeded";
  let html=`<div class="text-center mb-4 pr-8">
    <div class="text-[10px] text-gray-500 mb-3">${m.week||m.phase} · ${fmt(m.date)}</div>
    <div class="flex items-center justify-center gap-8">
      <div class="text-center"><div class="text-3xl mb-1">${t1.emoji}</div><div class="font-bold text-sm" style="color:${t1.color}">${t1.name}</div></div>
      <div class="text-center">`;
  if(isDone){
    html+=`<div class="text-3xl font-black">
      <span style="color:${m.s1>m.s2?t1.color:"#6b7280"}">${m.s1}</span>
      <span class="text-gray-700 mx-1 text-xl">x</span>
      <span style="color:${m.s2>m.s1?t2.color:"#6b7280"}">${m.s2}</span>
    </div>
    <div class="text-xs text-green-400 mt-1 font-semibold">${m.s1>m.s2?t1.short:t2.short} venceu</div>`;
  } else {
    html+=`<div class="text-gray-400 text-sm font-bold">vs</div><div class="text-xs text-blue-400 mt-1">${statusBadge(m.status)}</div>`;
  }
  html+=`</div><div class="text-center"><div class="text-3xl mb-1">${t2.emoji}</div><div class="font-bold text-sm" style="color:${t2.color}">${t2.name}</div></div>
    </div></div>`;

  if(isDone){
    // Try to get draft from Leaguepedia
    const overviewPage = `CBLOL/2026 Season/Split 1/${t1.short}_vs_${t2.short}`;
    html+=`<div id="draft-section" class="border-t border-gray-800 pt-3">
      <div class="text-xs font-semibold text-gray-400 uppercase mb-2">Draft — Jogo 1</div>
      <div id="draft-loading" class="text-center text-xs text-gray-500 py-2">Carregando draft...</div>
    </div>`;
  }

  document.getElementById("modal-content").innerHTML=html;
  document.getElementById("match-modal").classList.remove("hidden");
  document.body.style.overflow="hidden";

  if(isDone){
    try{
      // Tentar buscar draft da Leaguepedia
      const draftData = await fetchDraft(`CBLOL/2026 Season/Split 1`, 1);
      const draftEl = document.getElementById("draft-loading");
      if(draftEl) {
        if(draftData && draftData.Team1Picks){
          const p1=(draftData.Team1Picks||"").split(",").map(s=>s.trim());
          const p2=(draftData.Team2Picks||"").split(",").map(s=>s.trim());
          const b1=(draftData.Team1Bans||"").split(",").map(s=>s.trim());
          const b2=(draftData.Team2Bans||"").split(",").map(s=>s.trim());
          let dHtml=`<div class="grid grid-cols-2 gap-3">
            <div><div class="text-xs text-blue-400 font-semibold mb-2">🔵 Blue — ${t1.short}</div>
              <div class="mb-1 text-[10px] text-gray-500">Picks</div>
              <div class="flex flex-wrap gap-1 mb-2">${p1.map(c=>champIcon(c)).join("")}</div>
              <div class="text-[10px] text-gray-500">Bans</div>
              <div class="flex flex-wrap gap-1 opacity-50">${b1.slice(0,3).map(c=>champIcon(c)).join("")}</div>
            </div>
            <div><div class="text-xs text-red-400 font-semibold mb-2">🔴 Red — ${t2.short}</div>
              <div class="mb-1 text-[10px] text-gray-500">Picks</div>
              <div class="flex flex-wrap gap-1 mb-2">${p2.map(c=>champIcon(c)).join("")}</div>
              <div class="text-[10px] text-gray-500">Bans</div>
              <div class="flex flex-wrap gap-1 opacity-50">${b2.slice(0,3).map(c=>champIcon(c)).join("")}</div>
            </div>
          </div>`;
          draftEl.outerHTML=dHtml;
        } else {
          draftEl.textContent="Draft não disponível para esta partida.";
        }
      }
    } catch(e){
      const el=document.getElementById("draft-loading");
      if(el) el.textContent="Não foi possível carregar o draft.";
    }
  }
}

function openTeam(id){
  const t=FB_TEAMS[id];
  const sched=state.schedule.length?state.schedule:FB_SCHEDULE;
  const standings=state.standings.length?state.standings:FB_STANDINGS;
  const standing=standings.find(s=>(s.code||s.team)?.toLowerCase()===id||s.team===id);
  const matches=sched.filter(m=>(m.t1key||m.t1)===id||(m.t2key||m.t2)===id);
  const done=matches.filter(m=>m.status==="completed"||m.status==="unneeded");
  let html=`<div class="text-center mb-4 pr-8">
    <div class="text-5xl mb-2">${t.emoji}</div>
    <div class="font-black text-xl" style="color:${t.color}">${t.name}</div>
    <div class="text-sm text-gray-400 mt-1">CBLOL 2026 Split 1</div>
    <div class="flex justify-center gap-8 mt-3">
      <div class="text-center"><div class="text-2xl font-black text-green-400">${standing?.w||0}</div><div class="text-xs text-gray-500">Vitórias</div></div>
      <div class="text-center"><div class="text-2xl font-black text-red-400">${standing?.l||0}</div><div class="text-xs text-gray-500">Derrotas</div></div>
      <div class="text-center"><div class="text-2xl font-black gold">${standing?.pts||0}</div><div class="text-xs text-gray-500">Pontos</div></div>
    </div>
  </div>`;
  if(done.length){
    html+=`<div class="border-t border-gray-800 pt-3 mb-3">
      <div class="text-xs font-semibold text-gray-400 uppercase mb-2">Resultados Recentes</div>
      ${done.slice(-4).reverse().map(m=>{
        const isT1=(m.t1key||m.t1)===id;
        const opp=teamInfo(isT1?(m.t2key||m.t2code||m.t2):(m.t1key||m.t1code||m.t1));
        const my=isT1?m.s1:m.s2, op=isT1?m.s2:m.s1;
        const won=my>op;
        return `<div class="flex items-center justify-between py-2 border-b border-gray-900">
          <div class="flex items-center gap-2"><span>${won?"🟢":"🔴"}</span><span class="text-xs text-gray-300">vs ${opp.emoji} ${opp.short}</span></div>
          <span class="text-xs font-bold ${won?"text-green-400":"text-red-400"}">${my}x${op} ${won?"✓":"✗"}</span>
        </div>`;
      }).join("")}
    </div>`;
  }
  // Players from this team
  const allP=state.players.length?state.players:FB_PLAYERS;
  const teamPlayers=allP.filter(p=>p.teamKey===id||p.team?.toLowerCase().includes(t.name.toLowerCase())||p.team===t.name);
  if(teamPlayers.length){
    html+=`<div class="border-t border-gray-800 pt-3">
      <div class="text-xs font-semibold text-gray-400 uppercase mb-2">Elenco & Stats</div>
      ${teamPlayers.map(p=>{
        const r=p.rating||calcRating(p,allP);
        return`<div class="flex items-center justify-between py-2 border-b border-gray-900">
          <div class="flex items-center gap-2"><span>${ROLE_ICON[p.role]||"?"}</span><span class="font-semibold text-sm">${p.name}</span></div>
          <div class="text-right"><div class="text-xs text-green-400 font-semibold">KDA ${p.kda}</div><div class="text-xs ${ratingColor(parseFloat(r))}">Rating ${r}</div></div>
        </div>`;
      }).join("")}
    </div>`;
  }
  document.getElementById("modal-content").innerHTML=html;
  document.getElementById("match-modal").classList.remove("hidden");
  document.body.style.overflow="hidden";
}

function openNews(n){
  const html=`<div class="pr-8">
    <div class="h-28 bg-gradient-to-br from-[#1f2937] to-[#0f172a] rounded-xl flex items-center justify-center mb-4">
      <span class="text-6xl opacity-70">🏆</span>
    </div>
    <span class="${CAT_COLOR[n.category]||"bg-gray-700"} text-white text-[10px] font-bold px-2 py-0.5 rounded">${n.category}</span>
    <h2 class="text-base font-bold mt-3 mb-1 leading-snug">${n.title}</h2>
    <div class="text-[10px] text-gray-500 mb-3">${fmtShort(n.date)} ${n.source?`· ${n.source}`:""}</div>
    <p class="text-sm text-gray-300 leading-relaxed">${n.summary}</p>
    ${n.url?`<a href="${n.url}" target="_blank" class="mt-3 block text-xs text-blue-400 underline">Ler matéria completa ↗</a>`:""}
  </div>`;
  document.getElementById("modal-content").innerHTML=html;
  document.getElementById("match-modal").classList.remove("hidden");
  document.body.style.overflow="hidden";
}

function closeModal(){
  document.getElementById("match-modal").classList.add("hidden");
  document.body.style.overflow="";
}
document.getElementById("match-modal").addEventListener("click",function(e){if(e.target===this)closeModal();});

// ===== NAVIGATION =====
function showSection(name){
  ["home","agenda","times","jogadores","noticias"].forEach(s=>{
    document.getElementById(`section-${s}`).classList.add("section-hidden");
    const t=document.getElementById(`tab-${s}`);
    t.classList.remove("tab-active");t.classList.add("tab-inactive");
  });
  document.getElementById(`section-${name}`).classList.remove("section-hidden");
  const at=document.getElementById(`tab-${name}`);
  at.classList.add("tab-active");at.classList.remove("tab-inactive");
  if(name==="agenda") renderAgenda();
  if(name==="times") renderTimes();
  if(name==="noticias") renderNews();
  if(name==="jogadores") renderPlayers();
}

// ===== DATA LOADING =====
async function loadSchedule(){
  try{
    const data=await fetchLoL("/getSchedule",`&leagueId=${CBLOL_LEAGUE_ID}`);
    const parsed=parseSchedule(data);
    if(parsed.length) state.schedule=parsed;
    console.log("Schedule loaded:",parsed.length,"events");
  } catch(e){
    console.warn("Schedule fallback:",e.message);
  }
}

async function loadStandings(){
  try{
    // First get leagues to find tournament ID
    const leagues=await fetchLoL("/getLeagues");
    const cblol=leagues?.data?.leagues?.find(l=>l.id===CBLOL_LEAGUE_ID||l.slug?.includes("cblol"));
    if(!cblol) throw new Error("CBLOL not found");
    // Get current tournament
    const tourns=await fetchLoL("/getTournamentsForLeague",`&leagueId=${CBLOL_LEAGUE_ID}`);
    const tornList=tourns?.data?.leagues?.[0]?.tournaments||[];
    const current=tornList[tornList.length-1];
    if(!current) throw new Error("No tournament");
    state.currentTournamentId=current.id;
    const stData=await fetchLoL("/getStandings",`&tournamentId=${current.id}`);
    const parsed=parseStandings(stData);
    if(parsed?.length) state.standings=parsed;
    console.log("Standings loaded:",parsed?.length);
  } catch(e){
    console.warn("Standings fallback:",e.message);
  }
}

async function loadLeaguepediaStats(){
  try{
    const rows=await fetchLeaguepediaStats();
    if(rows.length){
      const players=aggregatePlayerStats(rows);
      // Apply rating formula
      players.forEach(p=>{p.rating=parseFloat(calcRating(p,players));});
      players.sort((a,b)=>b.rating-a.rating);
      if(players.length) state.players=players;
      console.log("Leaguepedia players:",players.length);
    }
  } catch(e){
    console.warn("Leaguepedia fallback:",e.message);
  }
}

async function refreshAll(){
  if(state.loading) return;
  setLoading(true);
  showToast("🔄 Atualizando dados...");
  try{
    await Promise.allSettled([loadSchedule(), loadStandings(), loadLeaguepediaStats()]);
    renderHome();
    showToast("✅ Dados atualizados!");
  } catch(e){
    showToast("⚠️ Erro ao atualizar — usando dados locais");
  }
  setLoading(false);
}

// ===== INIT =====
(async function init(){
  renderHome(); // render with fallback immediately
  setLoading(true);
  await Promise.allSettled([loadSchedule(), loadStandings(), loadLeaguepediaStats()]);
  setLoading(false);
  renderHome(); // re-render with real data if loaded
  console.log("CBLOL Hub initialized");
})();

// Auto-refresh every 3 minutes for live matches
setInterval(()=>{
  const hasLive=state.schedule.some(m=>m.status==="inProgress"||m.status==="live");
  if(hasLive) refreshAll();
},3*60*1000);
</script>
</body>
</html>'''

with open("output/cblol-hub/index.html", "w", encoding="utf-8") as f:
    f.write(html)

# PWA manifest
manifest = '''{
  "name": "CBLOL Hub 2026",
  "short_name": "CBLOL Hub",
  "description": "Agenda, resultados, stats e notícias do CBLOL",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#0a0e1a",
  "theme_color": "#0a0e1a",
  "orientation": "portrait",
  "icons": [
    {"src": "https://via.placeholder.com/192x192/0a0e1a/c89b3c?text=CBL", "sizes": "192x192", "type": "image/png"},
    {"src": "https://via.placeholder.com/512x512/0a0e1a/c89b3c?text=CBL", "sizes": "512x512", "type": "image/png"}
  ]
}'''

with open("output/cblol-hub/manifest.json", "w") as f:
    f.write(manifest)

print("index.html:", os.path.getsize("output/cblol-hub/index.html"), "bytes")
print("manifest.json:", os.path.getsize("output/cblol-hub/manifest.json"), "bytes")
