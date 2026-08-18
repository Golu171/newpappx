import json

def json_to_html(json_raw_data, title="Test Series", created_by="Ram"):
    json_str = json.dumps(json_raw_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title}</title>

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
    -webkit-tap-highlight-color:transparent;
}}

:root {{
    --primary:#6366F1;
    --secondary:#EC4899;
    --accent:#8B5CF6;
    --success:#10B981;
    --success-bg:rgba(16,185,129,.15);
    --danger:#EF4444;
    --danger-bg:rgba(239,68,68,.15);
    --warning:#F59E0B;
    --bg-light:#F0FDF4;
    --bg-white:#FFFFFF;
    --text-dark:#1E293B;
    --text-light:#64748B;
    --border:#D1D5DB;
    --shadow-sm:0 2px 8px rgba(0,0,0,.08);
    --shadow-md:0 4px 20px rgba(0,0,0,.12);
    --shadow-lg:0 10px 40px rgba(0,0,0,.15);
    --content-zoom:1;
}}

[data-theme="dark"] {{
    --bg-light:#071A12;
    --bg-white:#10261C;
    --text-dark:#F1F5F9;
    --text-light:#B6C5BE;
    --border:#315443;
}}

body {{
    font-family:'Noto Sans Devanagari',sans-serif;
    font-size:20px;
    line-height:1.6;
    background:linear-gradient(135deg,#DCFCE7,#BBF7D0,#D1FAE5);
    min-height:100vh;
    overflow-y:auto;
    color:var(--text-dark);
    -webkit-font-smoothing:antialiased;
    text-rendering:optimizeLegibility;
}}

[data-theme="dark"] body {{
    background:linear-gradient(135deg,#071A12,#0B2B1C,#10261C);
}}

#modeSelection {{
    position:fixed;
    inset:0;
    background:inherit;
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:9999;
    padding:20px;
    overflow-y:auto;
}}

.mode-container {{
    background:rgba(255,255,255,.96);
    backdrop-filter:blur(20px);
    border-radius:28px;
    padding:26px 24px 32px;
    max-width:520px;
    width:100%;
    box-shadow:var(--shadow-lg);
    text-align:center;
}}

[data-theme="dark"] .mode-container {{
    background:#10261C;
    color:#F1F5F9;
}}

.telegram-start {{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:9px;
    margin:0 auto 22px;
    padding:16px 25px;
    background:linear-gradient(135deg,#0088cc,#229ED9);
    color:white;
    font-size:21px;
    font-weight:700;
    border-radius:16px;
    text-decoration:none;
    box-shadow:0 6px 20px rgba(0,136,204,.4);
}}

.telegram-start i {{
    font-size:25px;
}}

.mode-header {{
    text-align:center;
    margin-bottom:28px;
}}

.mode-header-icon {{
    width:72px;
    height:72px;
    margin:0 auto 16px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    border-radius:22px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:36px;
    color:white;
}}

.mode-cards {{
    display:grid;
    gap:16px;
    margin-bottom:18px;
}}

.mode-card {{
    background:var(--bg-light);
    border:3px solid var(--border);
    border-radius:18px;
    padding:18px;
    cursor:pointer;
    transition:.3s;
    display:flex;
    align-items:center;
    gap:15px;
    text-align:left;
}}

.mode-card.selected {{
    border-color:var(--primary);
    background:rgba(99,102,241,.1);
    transform:translateY(-2px);
}}

.mode-icon {{
    width:50px;
    height:50px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:24px;
    color:white;
    flex-shrink:0;
}}

.exam-mode .mode-icon {{ background:#EF4444; }}
.practice-mode .mode-icon {{ background:#10B981; }}

#quizContainer {{
    display:none;
    position:fixed;
    inset:0;
    background:var(--bg-light);
    overflow-y:auto;
}}

.quiz-header {{
    position:fixed;
    top:0;
    left:0;
    right:0;
    background:var(--bg-white);
    box-shadow:var(--shadow-sm);
    z-index:100;
    padding:6px 10px;
}}

.header-top {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:6px;
}}

.timer-display {{
    background:rgba(99,102,241,.18);
    padding:5px 10px;
    border-radius:12px;
    font-weight:700;
    color:var(--primary);
    display:flex;
    align-items:center;
    gap:8px;
}}

.progress-bar-container {{
    height:8px;
    background:var(--border);
    border-radius:10px;
    overflow:hidden;
}}

.progress-bar {{
    height:100%;
    background:linear-gradient(90deg,var(--primary),var(--secondary),var(--accent));
    transition:width .4s ease;
}}

.question-section {{
    position:relative;
    padding:8px;
    padding-top:112px;
    padding-bottom:105px;
    min-height:100%;
}}

.question-card {{
    background:#DCFCE7;
    border:3px solid #86EFAC;
    border-radius:18px;
    padding:18px;
    box-shadow:var(--shadow-md);
    max-width:100%;
    margin:0;
    transform:scale(var(--content-zoom));
    transform-origin:top center;
    transition:transform .2s ease;
}}

[data-theme="dark"] .question-card {{
    background:#123D2A;
    border-color:#287A4A;
}}

.question-number {{
    display:inline-flex;
    align-items:center;
    gap:10px;
    font-size:13px;
    font-weight:700;
    color:var(--primary);
    background:rgba(99,102,241,.18);
    padding:8px 16px;
    border-radius:25px;
    margin-bottom:15px;
}}

.question-text {{
    font-size:22px;
    font-weight:700;
    color:#000000;
    line-height:1.5;
    margin-bottom:14px;
    white-space:pre-wrap;
    word-wrap:break-word;
}}

[data-theme="dark"] .question-text {{
    color:#000000;
}}

.option-btn {{
    width:100%;
    padding:15px 16px;
    background:#BBF7D0;
    border:3px solid #22C55E;
    border-radius:16px;
    text-align:left;
    font-size:22px;
    color:#000000;
    font-weight:700;
    cursor:pointer;
    display:flex;
    align-items:flex-start;
    gap:12px;
    transition:.3s;
    margin-bottom:10px;
    line-height:1.45;
}}

[data-theme="dark"] .option-btn {{
    background:#14532D;
    border-color:#22C55E;
    color:#000000;
}}

.option-btn.selected {{
    background:#86EFAC;
    border-color:#15803D;
}}

[data-theme="dark"] .option-btn.selected {{
    background:#166534;
    border-color:#4ADE80;
}}

.option-btn.correct {{
    background:#86EFAC;
    border-color:#16A34A;
}}

[data-theme="dark"] .option-btn.correct {{
    background:#166534;
    border-color:#4ADE80;
}}

.option-btn.incorrect {{
    background:var(--danger-bg);
    border-color:var(--danger);
}}

.option-indicator {{
    min-width:36px;
    height:36px;
    border-radius:50%;
    background:#F0FDF4;
    border:2px solid #22C55E;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    color:#000000;
    flex-shrink:0;
}}

[data-theme="dark"] .option-indicator {{
    background:#166534;
    border-color:#4ADE80;
    color:#000000;
}}

.option-btn.correct .option-indicator {{
    background:var(--success);
    color:white;
    border:none;
}}

.option-btn.incorrect .option-indicator {{
    background:var(--danger);
    color:white;
    border:none;
}}

.explanation-box {{
    display:none;
    background:#D1FAE5;
    border-left:5px solid #16A34A;
    border-radius:0 16px 16px 0;
    padding:18px;
    margin-top:18px;
}}

[data-theme="dark"] .explanation-box {{
    background:#123D2A;
    border-left-color:#4ADE80;
}}

.explanation-title {{
    font-weight:800;
    color:#000000;
    margin-bottom:10px;
}}

[data-theme="dark"] .explanation-title {{
    color:#000000;
}}

.explanation-text {{
    font-size:22px;
    line-height:1.55;
    color:#000000;
    font-weight:700;
}}

[data-theme="dark"] .explanation-text {{
    color:#000000;
}}

.nav-controls {{
    position:fixed;
    bottom:0;
    left:0;
    right:0;
    background:var(--bg-white);
    padding:10px 14px;
    box-shadow:0 -4px 20px rgba(0,0,0,.08);
    display:flex;
    gap:10px;
    z-index:90;
}}

.nav-btn {{
    flex:1;
    padding:14px;
    border:none;
    border-radius:14px;
    font-size:15px;
    font-weight:600;
    cursor:pointer;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:8px;
}}

.nav-btn.primary {{
    background:linear-gradient(135deg,var(--primary),var(--accent));
    color:white;
}}

.nav-btn.secondary {{
    background:var(--bg-light);
    color:var(--text-dark);
    border:2px solid var(--border);
}}

#resultsContainer {{
    display:none;
    position:fixed;
    inset:0;
    background:var(--bg-light);
    overflow-y:auto;
    padding:20px;
    z-index:1000;
    text-align:center;
}}

.results-card {{
    background:var(--bg-white);
    border-radius:28px;
    padding:40px 30px;
    max-width:600px;
    margin:0 auto 20px;
    box-shadow:var(--shadow-lg);
}}

.results-score {{
    font-size:56px;
    font-weight:800;
    background:linear-gradient(135deg,var(--primary),var(--secondary),var(--accent));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}}

.stats-grid {{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
    max-width:600px;
    margin:0 auto 24px;
}}

.stat-card {{
    background:var(--bg-white);
    padding:24px;
    border-radius:20px;
    box-shadow:var(--shadow-md);
}}

.stat-val {{
    font-size:34px;
    font-weight:800;
    color:var(--text-dark);
}}

.question-nav-toggle {{
    position:fixed;
    bottom:105px;
    right:20px;
    width:60px;
    height:60px;
    background:linear-gradient(135deg,var(--primary),var(--secondary));
    color:white;
    border:none;
    border-radius:50%;
    font-size:24px;
    cursor:pointer;
    z-index:85;
    box-shadow:0 8px 25px rgba(99,102,241,.3);
}}

.question-nav-panel {{
    position:fixed;
    bottom:0;
    left:0;
    right:0;
    height:35vh;
    max-height:35vh;
    overflow-y:auto;
    background:var(--bg-white);
    border-radius:28px 28px 0 0;
    box-shadow:0 -8px 40px rgba(0,0,0,.2);
    z-index:95;
    transform:translateY(110%);
    transition:transform .35s ease;
    padding:18px;
    visibility:hidden;
}}

.question-nav-panel.open {{
    transform:translateY(0);
    visibility:visible;
}}

.question-grid {{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:12px;
}}

.question-nav-item {{
    aspect-ratio:1;
    border:3px solid var(--border);
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:700;
    cursor:pointer;
    color:var(--text-light);
}}

.question-nav-item.current {{
    border-color:var(--primary);
    color:var(--primary);
}}

.question-nav-item.answered {{
    background:var(--primary);
    color:white;
    border:none;
}}

.question-nav-item.marked {{
    background:var(--warning);
    color:white;
    border:none;
}}

.question-nav-item.correct {{
    background:var(--success);
    color:white;
    border:none;
}}

.question-nav-item.incorrect {{
    background:var(--danger);
    color:white;
    border:none;
}}

img {{
    max-width:100%;
    border-radius:12px;
    margin-top:15px;
}}

@media (max-width:768px) {{
    .question-text {{
        font-size:22px !important;
    }}

    .option-btn {{
        font-size:22px !important;
    }}

    .explanation-text {{
        font-size:22px !important;
    }}

    .question-card {{
        padding:15px;
    }}
}}
</style>
</head>

<body>

<div id="modeSelection">
    <div class="mode-container">

        <a href="https://t.me/MOCK_TEST18"
           target="_blank"
           rel="noopener noreferrer"
           class="telegram-start">
            📢 <i class="fab fa-telegram-plane"></i> Join Telegram Channel
        </a>

        <div class="mode-header">
            <div class="mode-header-icon">
                <i class="fas fa-brain"></i>
            </div>

            <h2 style="font-weight:800;color:#1E293B;">{title}</h2>
            <p>Choose test mode to begin</p>
        </div>

        <div class="mode-cards">

            <div class="mode-card exam-mode" onclick="setMode('exam',this)">
                <div class="mode-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div>
                    <h3 style="font-size:17px;">🎯 Exam Mode</h3>
                    <p style="font-size:13px;color:var(--text-light);">Results at end</p>
                </div>
            </div>

            <div class="mode-card practice-mode" onclick="setMode('practice',this)">
                <div class="mode-icon">
                    <i class="fas fa-book-open"></i>
                </div>
                <div>
                    <h3 style="font-size:17px;">📚 Practice Mode</h3>
                    <p style="font-size:13px;color:var(--text-light);">Instant feedback</p>
                </div>
            </div>

        </div>

        <input type="number"
               id="customTimer"
               style="width:100%;padding:16px;border:3px solid var(--border);border-radius:14px;margin-bottom:20px;"
               placeholder="Timer (Minutes) - Default 60">

        <button class="nav-btn primary"
                id="startBtn"
                disabled
                onclick="startQuiz()"
                style="width:100%;padding:18px;">
            Start Quiz
        </button>

    </div>
</div>

<div id="quizContainer">

    <div class="quiz-header">

        <div class="header-top">

            <div style="font-weight:700;font-size:14px;color:var(--text-dark);max-width:180px;overflow:hidden;white-space:nowrap;">
                {title}
            </div>

            <div style="display:flex;gap:8px;align-items:center;">

                <button onclick="zoomOut()"
                        style="width:36px;height:36px;border-radius:10px;border:2px solid var(--border);background:var(--bg-light);cursor:pointer;">
                    <i class="fas fa-minus"></i>
                </button>

                <button onclick="zoomIn()"
                        style="width:36px;height:36px;border-radius:10px;border:2px solid var(--border);background:var(--bg-light);cursor:pointer;">
                    <i class="fas fa-plus"></i>
                </button>

                <button onclick="toggleTheme()"
                        style="width:40px;height:40px;border-radius:12px;border:2px solid var(--border);background:var(--bg-light);cursor:pointer;">
                    <i class="fas fa-moon"></i>
                </button>

                <div class="timer-display">
                    <i class="fas fa-stopwatch"></i>
                    <span id="timeText">00:00</span>
                </div>

            </div>
        </div>

        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;color:var(--text-light);">
            <span id="pText">Question 1</span>
            <span id="aText">Attempted: 0/0</span>
        </div>

        <div class="progress-bar-container">
            <div class="progress-bar" id="pBar"></div>
        </div>

    </div>

    <div class="question-section scrollable" id="qArea"></div>

    <div class="nav-controls">

        <button class="nav-btn secondary" onclick="prevQ()">
            <i class="fas fa-arrow-left"></i> Prev
        </button>

        <button class="nav-btn secondary" id="markBtn" onclick="toggleMark()">
            Mark
        </button>

        <button class="nav-btn primary" id="nextBtn" onclick="nextQ()">
            Next <i class="fas fa-arrow-right"></i>
        </button>

    </div>

    <button class="question-nav-toggle" onclick="toggleNav()">
        <i class="fas fa-th"></i>
    </button>

    <div class="question-nav-panel" id="navPanel">

        <div style="display:flex;justify-content:space-between;margin-bottom:20px;">
            <h3>Navigator</h3>
            <button onclick="toggleNav()" style="border:none;background:none;font-size:24px;">
                &times;
            </button>
        </div>

        <div class="question-grid" id="qGrid"></div>

    </div>

</div>

<div id="resultsContainer">

    <div class="results-card">

        <div style="font-size:80px;">🏆</div>

        <h2>Quiz Completed!</h2>

        <div class="results-score" id="resScore">0/0</div>

        <div id="resPercent"
             style="font-size:22px;font-weight:600;color:var(--text-light);">
            0%
        </div>

    </div>

    <div class="stats-grid">

        <div class="stat-card">
            <div class="stat-val" style="color:var(--success);" id="sCorrect">0</div>
            <div style="font-size:13px;">Correct</div>
        </div>

        <div class="stat-card">
            <div class="stat-val" style="color:var(--danger);" id="sWrong">0</div>
            <div style="font-size:13px;">Incorrect</div>
        </div>

    </div>

    <div style="max-width:600px;margin:0 auto;display:grid;gap:14px;">

        <button class="nav-btn primary"
                onclick="reviewMode()"
                style="padding:18px;">
            Review Answers
        </button>

        <button class="nav-btn secondary"
                onclick="location.reload()"
                style="padding:18px;">
            Restart Quiz
        </button>

    </div>

    <div style="text-align:center;">

        <a href="https://t.me/MOCK_TEST18"
           target="_blank"
           rel="noopener noreferrer"
           style="display:inline-flex;align-items:center;justify-content:center;gap:9px;margin:15px auto;padding:18px 25px;background:linear-gradient(135deg,#0088cc,#229ED9);color:white;font-size:22px;font-weight:700;border-radius:16px;text-decoration:none;box-shadow:0 6px 20px rgba(0,136,204,.4);">

            📢 <i class="fab fa-telegram-plane"></i> Join Telegram Channel

        </a>

    </div>

    <div style="text-align:center;padding:20px;color:var(--text-light);">
        Made with ❤️ by <b>{created_by}</b>
    </div>

</div>

<script>
const rawData = {json_str};

const state = {{
    current:0,
    qs:[],
    ans:[],
    marked:[],
    mode:null,
    time:3600,
    isSub:false,
    theme:'light',
    zoom:1
}};

function setMode(m,el) {{
    state.mode=m;

    document.querySelectorAll('.mode-card')
        .forEach(c=>c.classList.remove('selected'));

    el.classList.add('selected');

    document.getElementById('startBtn').disabled=false;
}}

function toggleTheme() {{
    state.theme =
        state.theme==='light' ? 'dark' : 'light';

    document.documentElement.setAttribute(
        'data-theme',
        state.theme
    );
}}

function zoomIn() {{
    if(state.zoom<1.5) {{
        state.zoom+=0.1;
        applyZoom();
    }}
}}

function zoomOut() {{
    if(state.zoom>0.7) {{
        state.zoom-=0.1;
        applyZoom();
    }}
}}

function applyZoom() {{
    document.documentElement.style.setProperty(
        '--content-zoom',
        state.zoom
    );
}}

function startQuiz() {{

    const ct=parseInt(
        document.getElementById('customTimer').value
    );

    if(ct>0) state.time=ct*60;

    const data=
        Array.isArray(rawData)
        ? rawData
        : (rawData.data||[]);

    state.qs=data.map(q=>({{
        text:
            (q.question||'')
            .replace(/<style.*?<\\/style>/gs,"")
            .replace(/<p.*?>/g,"<div>")
            .replace(/<\\/p>/g,"</div>")
            .trim(),

        opts:[
            q.option_1,
            q.option_2,
            q.option_3,
            q.option_4,
            q.option_5
        ]
        .map(o=>
            o
            ? o
                .replace(/<p.*?>/g,"")
                .replace(/<\\/p>/g,"")
                .trim()
            : null
        )
        .filter(Boolean),

        correct:parseInt(q.answer)-1,

        sol:
            (
                q.solution_text ||
                q.solution ||
                "No explanation available."
            )
            .replace(/<p.*?>/g,"<div>")
            .replace(/<\\/p>/g,"</div>"),

        img:q.image_url||q.question_image||null
    }}));

    state.ans=new Array(state.qs.length).fill(null);
    state.marked=new Array(state.qs.length).fill(false);

    document.getElementById('modeSelection').style.display='none';
    document.getElementById('quizContainer').style.display='block';

    renderQ();
    renderGrid();
    updateTimer();

    setInterval(()=>{{
        if(!state.isSub) {{
            state.time--;
            updateTimer();
        }}
    }},1000);
}}

function renderQ() {{

    const q=state.qs[state.current];

    if(!q) return;

    let h=
        `<div class="question-card">
            <div class="question-number">
                Question ${{state.current+1}} of ${{state.qs.length}}
            </div>`;

    h+=`<div class="question-text">${{q.text}}</div>`;

    if(q.img)
        h+=`<img src="${{q.img}}" alt="Question Image">`;

    h+=`<div class="options-container">`;

    q.opts.forEach((o,i)=>{{

        let cls="option-btn";

        const sel=state.ans[state.current]===i;

        const rev=
            (
                state.mode==='practice' &&
                state.ans[state.current]!==null
            ) ||
            state.isSub;

        if(sel) cls+=" selected";

        if(rev) {{

            cls+=" disabled";

            if(i===q.correct)
                cls+=" correct";
            else if(sel)
                cls+=" incorrect";
        }}

        h+=`
            <button class="${{cls}}" onclick="selectOpt(${{i}})">
                <div class="option-indicator">
                    ${{String.fromCharCode(65+i)}}
                </div>
                <div style="flex:1;">
                    ${{o}}
                </div>
            </button>`;
    }});

    h+=`</div>`;

    if(
        (
            state.mode==='practice' &&
            state.ans[state.current]!==null
        ) ||
        state.isSub
    ) {{

        h+=`
            <div class="explanation-box" style="display:block;">

                <div class="explanation-title">
                    <i class="fas fa-lightbulb"></i>
                    Explanation
                </div>

                <div class="explanation-text">
                    ${{q.sol}}
                </div>

            </div>`;
    }}

    h+=`</div>`;

    document.getElementById('qArea').innerHTML=h;
    document.getElementById('qArea').scrollTop=0;

    updateUI();
}}

function selectOpt(i) {{

    if(state.isSub) return;

    if(
        state.mode==="practice" &&
        state.ans[state.current]!==null
    ) return;

    state.ans[state.current]=i;

    renderQ();
    updateGrid();
}}

function toggleMark() {{

    state.marked[state.current]=
        !state.marked[state.current];

    updateGrid();
    updateUI();
}}

function updateUI() {{

    document.getElementById('pText').innerText=
        `Question ${{state.current+1}}`;

    document.getElementById('aText').innerText=
        `Attempted: ${{state.ans.filter(a=>a!==null).length}}/${{state.qs.length}}`;

    document.getElementById('pBar').style.width=
        `${{((state.current+1)/state.qs.length)*100}}%`;

    document.getElementById('markBtn').innerText=
        state.marked[state.current]?'Unmark':'Mark';

    document.getElementById('nextBtn').innerHTML=
        state.current===state.qs.length-1
        ? 'Submit <i class="fas fa-paper-plane"></i>'
        : 'Next <i class="fas fa-arrow-right"></i>';
}}

function nextQ() {{
    if(state.current<state.qs.length-1) {{
        state.current++;
        renderQ();
    }} else {{
        submitQuiz();
    }}
}}

function prevQ() {{
    if(state.current>0) {{
        state.current--;
        renderQ();
    }}
}}

function toggleNav() {{
    document.getElementById('navPanel')
        .classList.toggle('open');
}}

function renderGrid() {{

    document.getElementById('qGrid').innerHTML=
        state.qs.map((_,i)=>
            `<div
                class="question-nav-item"
                id="nav-${{i}}"
                onclick="goTo(${{i}})">
                ${{i+1}}
            </div>`
        ).join('');

    updateGrid();
}}

function updateGrid() {{

    state.qs.forEach((_,i)=>{{

        const el=document.getElementById(`nav-${{i}}`);

        if(!el) return;

        el.className="question-nav-item";

        if(i===state.current)
            el.classList.add('current');

        if(state.isSub) {{

            if(state.ans[i]===state.qs[i].correct)
                el.classList.add('correct');

            else if(state.ans[i]!==null)
                el.classList.add('incorrect');

        }} else {{

            if(state.ans[i]!==null)
                el.classList.add('answered');

            else if(state.marked[i])
                el.classList.add('marked');
        }}
    }});
}}

function goTo(i) {{
    state.current=i;
    renderQ();
    toggleNav();
}}

function updateTimer() {{

    let m=Math.floor(state.time/60);
    let s=state.time%60;

    document.getElementById('timeText').innerText=
        `${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}`;

    if(state.time<=0)
        submitQuiz();
}}

function submitQuiz() {{

    if(!state.isSub && !confirm("Submit Quiz?"))
        return;

    state.isSub=true;

    let c=state.ans.filter(
        (a,i)=>a===state.qs[i].correct
    ).length;

    let w=state.ans.filter(
        (a,i)=>
            a!==null &&
            a!==state.qs[i].correct
    ).length;

    document.getElementById('quizContainer').style.display='none';
    document.getElementById('resultsContainer').style.display='block';

    document.getElementById('resScore').innerText=
        `${{c}} / ${{state.qs.length}}`;

    document.getElementById('resPercent').innerText=
        `${{((c/state.qs.length)*100).toFixed(1)}}%`;

    document.getElementById('sCorrect').innerText=c;
    document.getElementById('sWrong').innerText=w;
}}

function reviewMode() {{

    document.getElementById('resultsContainer').style.display='none';
    document.getElementById('quizContainer').style.display='block';

    state.current=0;

    renderQ();
    updateGrid();
}}
</script>

</body>
</html>'''

    return html

