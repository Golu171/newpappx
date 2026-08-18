import json

def json_to_html(json_raw_data, title="Test Series", created_by="Ram"):
    json_str = json.dumps(json_raw_data, ensure_ascii=False)

    html = r"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>__TITLE__</title>

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}

:root{
 --green-bg:#dcfce7;
 --green-border:#22c55e;
 --green-dark:#15803d;
 --green-soft:#bbf7d0;
 --text-dark:#000;
 --text-light:#374151;
 --border:#bbf7d0;
 --primary:#6366f1;
 --primary-glow:rgba(99,102,241,.25);
 --success:#22c55e;
 --success-bg:#bbf7d0;
 --danger:#ef4444;
 --danger-bg:#fee2e2;
 --warning:#f59e0b;
 --shadow-sm:0 2px 8px rgba(0,0,0,.08);
 --content-zoom:1;
}

html,body{width:100%;min-height:100%}
body{
 font-family:'Noto Sans Devanagari',sans-serif;
 font-size:20px;
 line-height:1.6;
 background:var(--green-bg);
 color:#000;
 overflow-y:auto;
 -webkit-font-smoothing:antialiased;
 text-rendering:optimizeLegibility;
}
button,input{font-family:inherit}

#modeSelection{
 position:fixed;inset:0;background:var(--green-bg);
 display:flex;align-items:center;justify-content:center;
 z-index:9999;padding:20px;overflow-y:auto
}
.mode-container{
 background:#f8fff9;border-radius:28px;padding:30px 24px;
 max-width:520px;width:100%;box-shadow:0 10px 40px rgba(0,0,0,.15);
 text-align:center
}
.mode-header{text-align:center;margin-bottom:28px}
.mode-header-icon{display:none}
.mode-header h2{font-size:30px;line-height:1.25;font-weight:800;color:#111827;margin-bottom:12px}
.mode-header p{color:#374151;font-size:18px}
.mode-cards{display:grid;gap:16px;margin-bottom:18px}
.mode-card{
 background:#f8fafc;border:3px solid #dbe4e8;border-radius:18px;
 padding:18px;cursor:pointer;transition:.3s;display:flex;
 align-items:center;gap:15px;text-align:left
}
.mode-card.selected{border-color:var(--green-border);background:#dcfce7;transform:translateY(-2px)}
.mode-icon{
 width:58px;height:58px;border-radius:14px;display:flex;
 align-items:center;justify-content:center;font-size:27px;color:#fff;flex-shrink:0
}
.exam-mode .mode-icon{background:#ef4444}
.practice-mode .mode-icon{background:#10b981}
.mode-card h3{color:#111827}
.mode-card p{color:#64748b}

#customTimer{
 width:100%;padding:16px;border:3px solid #dbe4e8;border-radius:14px;
 margin-bottom:18px;font-size:18px;background:#fff;color:#000
}

.nav-btn{
 flex:1;padding:16px;border:none;border-radius:14px;font-size:18px;
 font-weight:700;cursor:pointer;display:flex;align-items:center;
 justify-content:center;gap:8px
}
.nav-btn.primary{background:#22c55e;color:#000}
.nav-btn.primary:disabled{opacity:.55;cursor:not-allowed}
.nav-btn.secondary{background:#dcfce7;color:#000;border:2px solid #86efac}

#quizContainer{
 display:none;position:fixed;inset:0;background:var(--green-bg);
 overflow-y:auto;padding-top:112px;padding-bottom:96px
}

.quiz-header{
 position:fixed;top:0;left:0;right:0;background:#dcfce7;
 box-shadow:var(--shadow-sm);z-index:100;padding:6px 10px 8px;
 border-bottom:1px solid #bbf7d0
}
.header-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:5px}
.header-title{
 font-weight:800;font-size:14px;color:#000;max-width:230px;
 overflow:hidden;white-space:nowrap;text-overflow:ellipsis
}
.header-actions{display:flex;gap:8px;align-items:center;flex-shrink:0}
.zoom-btn{
 width:40px;height:40px;border-radius:12px;border:2px solid #bbf7d0;
 background:#f0fdf4;color:#000;cursor:pointer;font-size:18px;font-weight:800
}
.timer-display{
 background:#c7d2fe;padding:5px 10px;border-radius:12px;font-weight:800;
 color:#4f46e5;display:flex;align-items:center;gap:7px;font-size:18px
}
.header-info{
 display:flex;justify-content:space-between;font-size:14px;
 margin-bottom:5px;color:#374151
}
.progress-bar-container{height:8px;background:#d1d5db;border-radius:10px;overflow:hidden}
.progress-bar{height:100%;background:linear-gradient(90deg,#6366f1,#ec4899);transition:width .4s ease}

.question-section{position:relative;padding:8px;margin:0;overflow:visible}
.question-card{
 background:#dcfce7;border:4px solid #86efac;border-radius:24px;
 padding:20px;box-shadow:none;width:100%;max-width:100%;margin:0;
 transform:scale(var(--content-zoom));transform-origin:top center
}
.question-number{
 display:inline-flex;align-items:center;gap:10px;font-size:17px;font-weight:800;
 color:#4f46e5;background:#dbeafe;padding:8px 16px;border-radius:25px;margin-bottom:20px
}
.question-text{
 font-size:22px;font-weight:800;color:#000!important;line-height:1.6;
 margin-bottom:18px;white-space:pre-wrap;word-wrap:break-word
}
.option-btn{
 width:100%;padding:16px 18px;background:#bbf7d0;border:3px solid #22c55e;
 border-radius:18px;text-align:left;font-size:22px;color:#000!important;
 font-weight:800;cursor:pointer;display:flex;align-items:flex-start;gap:14px;
 transition:.25s;margin-bottom:12px;line-height:1.5
}
.option-btn div{color:#000!important}
.option-indicator{
 min-width:38px;height:38px;border-radius:50%;background:#f0fdf4;
 border:3px solid #22c55e;color:#000!important;display:flex;
 align-items:center;justify-content:center;font-weight:800;flex-shrink:0
}
.option-btn.selected{background:#86efac;border-color:#15803d}
.option-btn.correct{background:#86efac;border-color:#15803d}
.option-btn.correct .option-indicator{background:#22c55e;color:#000!important;border:none}
.option-btn.incorrect{background:#fecaca;border-color:#ef4444}
.option-btn.incorrect .option-indicator{background:#ef4444;color:#fff!important;border:none}
.option-btn.disabled{cursor:default}

.explanation-box{
 display:none;background:#dcfce7;border-left:6px solid #22c55e;
 border-radius:0 18px 18px 0;padding:18px;margin-top:22px
}
.explanation-title{font-weight:800;color:#22c55e!important;margin-bottom:10px;font-size:24px}
.explanation-text{font-size:22px;line-height:1.65;color:#000!important;font-weight:700}
.explanation-text *{color:#000!important}

.nav-controls{
 position:fixed;bottom:0;left:0;right:0;background:#dcfce7;
 padding:14px 18px;box-shadow:0 -4px 20px rgba(0,0,0,.08);
 display:flex;gap:12px;z-index:90;border-top:1px solid #bbf7d0
}
.question-nav-toggle{
 position:fixed;bottom:105px;right:20px;width:60px;height:60px;
 background:linear-gradient(135deg,#6366f1,#ec4899);color:#fff;border:none;
 border-radius:50%;font-size:24px;cursor:pointer;z-index:85;
 box-shadow:0 8px 25px rgba(99,102,241,.3)
}
.question-nav-panel{
 position:fixed;bottom:0;left:0;right:0;height:35vh;max-height:35vh;
 overflow-y:auto;background:#dcfce7;border-radius:28px 28px 0 0;
 box-shadow:0 -8px 40px rgba(0,0,0,.2);z-index:95;
 transform:translateY(110%);transition:transform .35s ease;
 padding:18px;visibility:hidden
}
.question-nav-panel.open{transform:translateY(0);visibility:visible}
.question-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.question-nav-item{
 aspect-ratio:1;border:3px solid #86efac;border-radius:14px;
 display:flex;align-items:center;justify-content:center;font-weight:800;
 cursor:pointer;color:#000;background:#dcfce7
}
.question-nav-item.current{border-color:#6366f1;color:#4f46e5}
.question-nav-item.answered,.question-nav-item.correct{background:#22c55e;color:#000;border:none}
.question-nav-item.marked{background:#f59e0b;color:#000;border:none}
.question-nav-item.incorrect{background:#ef4444;color:#fff;border:none}

img{max-width:100%;border-radius:12px;margin-top:15px}

#resultsContainer{
 display:none;position:fixed;inset:0;background:#dcfce7;overflow-y:auto;
 padding:20px;z-index:1000;text-align:center
}
.results-card{
 background:#dcfce7;border:4px solid #86efac;border-radius:28px;
 padding:40px 30px;max-width:600px;margin:0 auto 20px
}
.results-score{font-size:56px;font-weight:800;color:#16a34a}
.stats-grid{
 display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:600px;margin:0 auto 24px
}
.stat-card{background:#dcfce7;border:3px solid #86efac;padding:24px;border-radius:20px}
.stat-val{font-size:34px;font-weight:800;color:#000}

.telegram-button{
 display:flex;align-items:center;justify-content:center;gap:10px;width:100%;
 max-width:600px;margin:16px auto;padding:18px 24px;
 background:linear-gradient(135deg,#0088cc,#229ed9);color:#fff!important;
 font-size:22px;font-weight:800;border-radius:16px;text-decoration:none;
 box-shadow:0 6px 20px rgba(0,136,204,.35)
}
.telegram-button .fab{font-size:27px}
.start-telegram{margin:0 auto 22px;padding:15px 22px;font-size:20px;max-width:430px}

@media(max-width:768px){
 .question-text,.option-btn,.explanation-text{font-size:22px!important}
 .header-title{max-width:190px}
 .timer-display{font-size:17px}
}
@media(max-width:430px){
 #quizContainer{padding-top:108px}
 .question-card{padding:16px;border-radius:20px}
 .nav-controls{padding:12px 10px}
 .nav-btn{font-size:17px;padding:14px 8px}
 .zoom-btn{width:36px;height:36px}
}
</style>
</head>

<body>

<div id="modeSelection">
 <div class="mode-container">

  <a href="https://t.me/MOCK_TEST18" target="_blank" rel="noopener noreferrer"
     class="telegram-button start-telegram">
   📢 <i class="fab fa-telegram"></i> Join Telegram Channel
  </a>

  <div class="mode-header">
   <h2>__TITLE__</h2>
   <p>Choose test mode to begin</p>
  </div>

  <div class="mode-cards">
   <div class="mode-card exam-mode" onclick="setMode('exam', this)">
    <div class="mode-icon"><i class="fas fa-file-alt"></i></div>
    <div><h3 style="font-size:17px">🎯 Exam Mode</h3><p style="font-size:13px">Results at end</p></div>
   </div>

   <div class="mode-card practice-mode" onclick="setMode('practice', this)">
    <div class="mode-icon"><i class="fas fa-book-open"></i></div>
    <div><h3 style="font-size:17px">📚 Practice Mode</h3><p style="font-size:13px">Instant feedback</p></div>
   </div>
  </div>

  <input type="number" id="customTimer" placeholder="Timer (Minutes) - Default 60">

  <button class="nav-btn primary" id="startBtn" disabled onclick="startQuiz()"
          style="width:100%;padding:18px">
   Start Quiz
  </button>

 </div>
</div>

<div id="quizContainer">

 <div class="quiz-header">
  <div class="header-top">
   <div class="header-title">__TITLE__</div>

   <div class="header-actions">
    <button class="zoom-btn" onclick="zoomOut()"><i class="fas fa-minus"></i></button>
    <button class="zoom-btn" onclick="zoomIn()"><i class="fas fa-plus"></i></button>

    <!-- Moon / Dark Theme button intentionally removed -->

    <div class="timer-display">
     <i class="fas fa-stopwatch"></i>
     <span id="timeText">60:00</span>
    </div>
   </div>
  </div>

  <div class="header-info">
   <span id="pText">Question 1</span>
   <span id="aText">Attempted: 0/0</span>
  </div>

  <div class="progress-bar-container">
   <div class="progress-bar" id="pBar"></div>
  </div>
 </div>

 <div class="question-section" id="qArea"></div>

 <div class="nav-controls">
  <button class="nav-btn secondary" onclick="prevQ()">
   <i class="fas fa-arrow-left"></i> Prev
  </button>

  <button class="nav-btn secondary" id="markBtn" onclick="toggleMark()">Mark</button>

  <button class="nav-btn primary" id="nextBtn" onclick="nextQ()">
   Next <i class="fas fa-arrow-right"></i>
  </button>
 </div>

 <button class="question-nav-toggle" onclick="toggleNav()">
  <i class="fas fa-th"></i>
 </button>

 <div class="question-nav-panel" id="navPanel">
  <div style="display:flex;justify-content:space-between;margin-bottom:20px">
   <h3 style="color:#000">Navigator</h3>
   <button onclick="toggleNav()" style="border:none;background:none;font-size:24px;color:#000">&times;</button>
  </div>
  <div class="question-grid" id="qGrid"></div>
 </div>

</div>

<div id="resultsContainer">

 <div class="results-card">
  <div style="font-size:80px">🏆</div>
  <h2 style="color:#000;font-size:30px">Quiz Completed!</h2>
  <div class="results-score" id="resScore">0/0</div>
  <div id="resPercent" style="font-size:22px;font-weight:600;color:#374151">0%</div>
 </div>

 <div class="stats-grid">
  <div class="stat-card">
   <div class="stat-val" style="color:#16a34a" id="sCorrect">0</div>
   <div style="font-size:15px;color:#000">Correct</div>
  </div>

  <div class="stat-card">
   <div class="stat-val" style="color:#dc2626" id="sWrong">0</div>
   <div style="font-size:15px;color:#000">Incorrect</div>
  </div>
 </div>

 <div style="max-width:600px;margin:0 auto;display:grid;gap:14px">

  <button class="nav-btn primary" onclick="reviewMode()" style="padding:18px">
   Review Answers
  </button>

  <button class="nav-btn secondary" onclick="location.reload()" style="padding:18px">
   Restart Quiz
  </button>

  <a href="https://t.me/MOCK_TEST18" target="_blank" rel="noopener noreferrer"
     class="telegram-button">
   📢 <i class="fab fa-telegram"></i> Join Telegram Channel
  </a>
 </div>

 <div style="text-align:center;padding:20px;color:#374151">
  Made with ❤️ by <b>__CREATED_BY__</b>
 </div>
</div>

<script>
const rawData = __RAW_DATA__;

const state = {
 current:0,
 qs:[],
 ans:[],
 marked:[],
 mode:null,
 time:3600,
 isSub:false,
 zoom:1
};

function setMode(m,el){
 state.mode=m;
 document.querySelectorAll('.mode-card').forEach(c=>c.classList.remove('selected'));
 el.classList.add('selected');
 document.getElementById('startBtn').disabled=false;
}

function zoomIn(){
 if(state.zoom<1.5){
  state.zoom=Math.min(1.5,+(state.zoom+0.1).toFixed(1));
  applyZoom();
 }
}

function zoomOut(){
 if(state.zoom>0.7){
  state.zoom=Math.max(0.7,+(state.zoom-0.1).toFixed(1));
  applyZoom();
 }
}

function applyZoom(){
 document.documentElement.style.setProperty('--content-zoom',state.zoom);
}

function startQuiz(){
 const ct=parseInt(document.getElementById('customTimer').value);
 if(ct>0) state.time=ct*60;

 const data=Array.isArray(rawData)?rawData:(rawData.data||[]);

 state.qs=data.map(q=>({
  text:(q.question||"")
   .replace(/<style.*?<\/style>/gs,"")
   .replace(/<p.*?>/g,"<div>")
   .replace(/<\/p>/g,"</div>")
   .trim(),

  opts:[
   q.option_1,q.option_2,q.option_3,q.option_4,q.option_5
  ].map(o=>o?o.replace(/<p.*?>/g,"").replace(/<\/p>/g,"").trim():null)
   .filter(Boolean),

  correct:parseInt(q.answer)-1,

  sol:(q.solution_text||q.solution||"No explanation available.")
   .replace(/<p.*?>/g,"<div>")
   .replace(/<\/p>/g,"</div>"),

  img:q.image_url||q.question_image||null
 }));

 state.ans=new Array(state.qs.length).fill(null);
 state.marked=new Array(state.qs.length).fill(false);

 document.getElementById('modeSelection').style.display='none';
 document.getElementById('quizContainer').style.display='block';

 renderQ();
 renderGrid();
 updateTimer();

 setInterval(()=>{
  if(!state.isSub){
   state.time--;
   if(state.time<0) state.time=0;
   updateTimer();
  }
 },1000);
}

function renderQ(){
 const q=state.qs[state.current];
 if(!q)return;

 let h=
 `<div class="question-card">
   <div class="question-number">
    Question ${state.current+1} of ${state.qs.length}
   </div>
   <div class="question-text">${q.text}</div>`;

 if(q.img) h+=`<img src="${q.img}" alt="Question image">`;

 h+=`<div class="options-container">`;

 q.opts.forEach((o,i)=>{
  let cls="option-btn";
  const sel=state.ans[state.current]===i;
  const rev=(state.mode==='practice'&&state.ans[state.current]!==null)||state.isSub;

  if(sel)cls+=" selected";

  if(rev){
   cls+=" disabled";
   if(i===q.correct)cls+=" correct";
   else if(sel)cls+=" incorrect";
  }

  h+=`
   <button class="${cls}" onclick="selectOpt(${i})">
    <div class="option-indicator">${String.fromCharCode(65+i)}</div>
    <div style="flex:1;color:#000!important">${o}</div>
   </button>`;
 });

 h+=`</div>`;

 if((state.mode==='practice'&&state.ans[state.current]!==null)||state.isSub){
  h+=`
   <div class="explanation-box" style="display:block">
    <div class="explanation-title">
     <i class="fas fa-lightbulb"></i> Explanation
    </div>
    <div class="explanation-text">${q.sol}</div>
   </div>`;
 }

 h+=`</div>`;

 document.getElementById('qArea').innerHTML=h;
 updateUI();
}

function selectOpt(i){
 if(state.isSub)return;
 if(state.mode==="practice"&&state.ans[state.current]!==null)return;
 state.ans[state.current]=i;
 renderQ();
 updateGrid();
}

function toggleMark(){
 state.marked[state.current]=!state.marked[state.current];
 updateGrid();
 updateUI();
}

function updateUI(){
 document.getElementById('pText').innerText=`Question ${state.current+1}`;
 document.getElementById('aText').innerText=
  `Attempted: ${state.ans.filter(a=>a!==null).length}/${state.qs.length}`;
 document.getElementById('pBar').style.width=
  `${((state.current+1)/state.qs.length)*100}%`;

 document.getElementById('markBtn').innerText=
  state.marked[state.current]?'Unmark':'Mark';

 document.getElementById('nextBtn').innerHTML=
  state.current===state.qs.length-1
  ?'Submit <i class="fas fa-paper-plane"></i>'
  :'Next <i class="fas fa-arrow-right"></i>';
}

function nextQ(){
 if(state.current<state.qs.length-1){
  state.current++;
  renderQ();
 }else submitQuiz();
}

function prevQ(){
 if(state.current>0){
  state.current--;
  renderQ();
 }
}

function toggleNav(){
 document.getElementById('navPanel').classList.toggle('open');
}

function renderGrid(){
 document.getElementById('qGrid').innerHTML=
  state.qs.map((_,i)=>
   `<div class="question-nav-item" id="nav-${i}" onclick="goTo(${i})">${i+1}</div>`
  ).join('');
 updateGrid();
}

function updateGrid(){
 state.qs.forEach((_,i)=>{
  const el=document.getElementById(`nav-${i}`);
  if(!el)return;

  el.className="question-nav-item";

  if(i===state.current)el.classList.add('current');

  if(state.isSub){
   if(state.ans[i]===state.qs[i].correct)el.classList.add('correct');
   else if(state.ans[i]!==null)el.classList.add('incorrect');
  }else{
   if(state.ans[i]!==null)el.classList.add('answered');
   else if(state.marked[i])el.classList.add('marked');
  }
 });
}

function goTo(i){
 state.current=i;
 renderQ();
 toggleNav();
}

function updateTimer(){
 let m=Math.floor(state.time/60),s=state.time%60;
 document.getElementById('timeText').innerText=
  `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;

 if(state.time<=0&&!state.isSub)submitQuiz();
}

function submitQuiz(){
 if(!state.isSub&&!confirm("Submit Quiz?"))return;

 state.isSub=true;

 let c=state.ans.filter((a,i)=>a===state.qs[i].correct).length;
 let w=state.ans.filter((a,i)=>a!==null&&a!==state.qs[i].correct).length;

 document.getElementById('quizContainer').style.display='none';
 document.getElementById('resultsContainer').style.display='block';

 document.getElementById('resScore').innerText=`${c} / ${state.qs.length}`;
 document.getElementById('resPercent').innerText=
  state.qs.length?`${((c/state.qs.length)*100).toFixed(1)}%`:'0%';

 document.getElementById('sCorrect').innerText=c;
 document.getElementById('sWrong').innerText=w;
}

function reviewMode(){
 document.getElementById('resultsContainer').style.display='none';
 document.getElementById('quizContainer').style.display='block';
 state.current=0;
 renderQ();
 updateGrid();
}
</script>
</body>
</html>"""

    html = html.replace("__TITLE__", str(title))
    html = html.replace("__CREATED_BY__", str(created_by))
    html = html.replace("__RAW_DATA__", json_str)

    return html

