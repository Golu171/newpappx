import json

def json_to_html(json_raw_data, title="Test Series", created_by="Ram"):
    json_str = json.dumps(json_raw_data)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        :root {{
            --primary: #6366F1; --primary-dark: #4F46E5; --primary-glow: rgba(99, 102, 241, 0.3);
            --secondary: #EC4899; --secondary-dark: #DB2777; --accent: #8B5CF6;
            --success: #10B981; --success-bg: rgba(16, 185, 129, 0.15);
            --danger: #EF4444; --danger-bg: rgba(239, 68, 68, 0.15);
            --warning: #F59E0B; --warning-bg: rgba(245, 158, 11, 0.15);
            --info: #3B82F6; --bg-light: #F8FAFC; --bg-white: #FFFFFF;
            --text-dark: #1E293B; --text-light: #64748B; --border: #E2E8F0;
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.08); --shadow-md: 0 4px 20px rgba(0,0,0,0.12);
            --shadow-lg: 0 10px 40px rgba(0,0,0,0.15);
        }}
        [data-theme="dark"] {{
            --bg-light: #0F172A; --bg-white: #1E293B; --text-dark: #F1F5F9; --text-light: #94A3B8; --border: #334155;
        }}
        body {{ font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%); min-height: 100vh; overflow: hidden; transition: all 0.3s ease; }}
        .scrollable::-webkit-scrollbar {{ width: 6px; }}
        .scrollable::-webkit-scrollbar-thumb {{ background: var(--primary); border-radius: 10px; }}

        /* Mode Selection */
        #modeSelection {{ position: fixed; inset: 0; background: inherit; display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 20px; }}
        .mode-container {{ background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 28px; padding: 40px 30px; max-width: 520px; width: 100%; box-shadow: var(--shadow-lg); text-align: center; }}
        .mode-header-icon {{ width: 80px; height: 80px; margin: 0 auto 20px; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: white; animation: float 3s ease-in-out infinite; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
        .mode-card {{ background: var(--bg-light); border: 3px solid var(--border); border-radius: 18px; padding: 18px; cursor: pointer; transition: 0.3s; display: flex; align-items: center; gap: 15px; text-align: left; margin-bottom: 15px; }}
        .mode-card.selected {{ border-color: var(--primary); background: rgba(99,102,241,0.1); }}
        
        /* Main Quiz Container */
        #quizContainer {{ display: none; position: fixed; inset: 0; background: var(--bg-light); overflow: hidden; }}
        .quiz-header {{ position: fixed; top: 0; left: 0; right: 0; background: var(--bg-white); box-shadow: var(--shadow-sm); z-index: 100; padding: 12px 20px; }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
        .timer-display {{ background: var(--primary-glow); padding: 6px 12px; border-radius: 10px; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 6px; font-size: 14px; }}
        
        /* Section & Lang Controls */
        .controls-row {{ display: flex; gap: 10px; margin-bottom: 10px; align-items: center; }}
        .lang-switch {{ background: var(--primary); color: white; border: none; padding: 5px 15px; border-radius: 20px; font-weight: 600; cursor: pointer; font-size: 13px; }}
        .section-badge {{ background: var(--bg-light); border: 1px solid var(--border); padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; color: var(--primary); }}

        .progress-bar-container {{ height: 6px; background: var(--border); border-radius: 10px; overflow: hidden; }}
        .progress-bar {{ height: 100%; background: linear-gradient(90deg, var(--primary), var(--secondary)); transition: width 0.4s ease; }}
        
        .question-section {{ position: fixed; top: 155px; left: 0; right: 0; bottom: 85px; overflow-y: auto; padding: 20px; }}
        .question-card {{ background: var(--bg-white); border-radius: 24px; padding: 25px; box-shadow: var(--shadow-md); max-width: 850px; margin: 0 auto; }}
        .question-text {{ font-size: 16px; font-weight: 600; color: var(--text-dark); line-height: 1.7; margin-bottom: 20px; }}
        
        .option-btn {{ width: 100%; padding: 15px 18px; background: var(--bg-light); border: 2px solid var(--border); border-radius: 14px; text-align: left; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: 0.2s; margin-bottom: 12px; }}
        .option-btn.selected {{ border-color: var(--primary); background: var(--primary-glow); }}
        .option-btn.correct {{ border-color: var(--success); background: var(--success-bg); }}
        .option-btn.incorrect {{ border-color: var(--danger); background: var(--danger-bg); }}
        .option-indicator {{ width: 30px; height: 30px; border-radius: 50%; border: 2px solid var(--border); display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }}
        
        .nav-controls {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-white); padding: 15px 20px; box-shadow: 0 -4px 15px rgba(0,0,0,0.05); display: flex; gap: 10px; z-index: 90; }}
        .nav-btn {{ flex: 1; padding: 14px; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }}
        .nav-btn.primary {{ background: var(--primary); color: white; }}
        .nav-btn.secondary {{ background: var(--bg-light); color: var(--text-dark); border: 1px solid var(--border); }}

        /* Navigator Panel */
        .question-nav-toggle {{ position: fixed; bottom: 95px; right: 20px; width: 55px; height: 55px; background: var(--primary); color: white; border: none; border-radius: 50%; font-size: 20px; z-index: 85; box-shadow: var(--shadow-md); }}
        .question-nav-panel {{ position: fixed; bottom: 0; left: 0; right: 0; height: 50vh; background: var(--bg-white); border-radius: 28px 28px 0 0; box-shadow: 0 -10px 40px rgba(0,0,0,0.15); z-index: 95; transform: translateY(110%); transition: 0.3s; padding: 20px; visibility: hidden; }}
        .question-nav-panel.open {{ transform: translateY(0); visibility: visible; }}
        .section-filter {{ width: 100%; padding: 12px; border-radius: 10px; border: 2px solid var(--border); margin-bottom: 15px; font-family: inherit; }}
        .question-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; overflow-y: auto; max-height: calc(50vh - 100px); }}
        .q-item {{ aspect-ratio: 1; border: 2px solid var(--border); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; cursor: pointer; font-size: 14px; }}
        .q-item.active {{ border-color: var(--primary); color: var(--primary); }}
        .q-item.done {{ background: var(--primary); color: white; border: none; }}
        
        #resultsContainer {{ display: none; position: fixed; inset: 0; background: var(--bg-light); overflow-y: auto; padding: 25px; z-index: 1000; text-align: center; }}
        img {{ max-width: 100%; border-radius: 10px; margin: 10px 0; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body>
    <div id="modeSelection">
        <div class="mode-container">
            <div class="mode-header">
                <div class="mode-header-icon"><i class="fas fa-rocket"></i></div>
                <h2 style="margin-bottom:10px;">{title}</h2>
            </div>
            <div class="mode-cards">
                <div class="mode-card" onclick="setMode('exam', this)">
                    <div style="background:#EF4444; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-stopwatch"></i></div>
                    <div><h4 style="font-size:16px;">Exam Mode</h4><p style="font-size:12px; color:var(--text-light);">Show results at the end</p></div>
                </div>
                <div class="mode-card" onclick="setMode('practice', this)">
                    <div style="background:#10B981; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-lightbulb"></i></div>
                    <div><h4 style="font-size:16px;">Practice Mode</h4><p style="font-size:12px; color:var(--text-light);">Instant feedback & explanation</p></div>
                </div>
            </div>
            <button class="nav-btn primary" id="startBtn" disabled onclick="startQuiz()" style="width:100%; margin-top:15px;">Start Preparation</button>
        </div>
    </div>

    <div id="quizContainer">
        <div class="quiz-header">
            <div class="header-top">
                <span id="currentSectionName" class="section-badge">General</span>
                <div style="display:flex; gap:8px;">
                    <button class="lang-switch" id="langBtn" onclick="toggleLang()">HI / EN</button>
                    <div class="timer-display"><i class="fas fa-clock"></i> <span id="timeText">00:00</span></div>
                </div>
            </div>
            <div class="controls-row">
                <span id="qCountText" style="font-size:12px; font-weight:600;">Question 1/0</span>
                <div class="progress-bar-container" style="flex:1;"><div class="progress-bar" id="pBar"></div></div>
            </div>
        </div>

        <div class="question-section scrollable" id="qArea"></div>

        <div class="nav-controls">
            <button class="nav-btn secondary" onclick="prevQ()"><i class="fas fa-chevron-left"></i> Prev</button>
            <button class="nav-btn secondary" onclick="toggleNav()"><i class="fas fa-th"></i> Grid</button>
            <button class="nav-btn primary" id="nextBtn" onclick="nextQ()">Next <i class="fas fa-chevron-right"></i></button>
        </div>

        <div class="question-nav-panel" id="navPanel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <h3 style="font-size:18px;">Navigator</h3>
                <button onclick="toggleNav()" style="background:none; border:none; font-size:20px;"><i class="fas fa-times"></i></button>
            </div>
            <select class="section-filter" id="sectionFilter" onchange="filterGrid(this.value)">
                <option value="all">All Sections</option>
            </select>
            <div class="question-grid" id="qGrid"></div>
        </div>
    </div>

    <div id="resultsContainer">
        <div style="background:var(--bg-white); padding:30px; border-radius:24px; box-shadow:var(--shadow-lg); max-width:500px; margin:0 auto;">
            <h1 id="resScore" style="font-size:48px; color:var(--primary);">0/0</h1>
            <p id="resPercent" style="font-weight:700; color:var(--text-light); margin-bottom:20px;">0%</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:25px;">
                <div style="background:var(--success-bg); padding:15px; border-radius:15px; color:var(--success);"><b>Correct</b><br><span id="sCorrect">0</span></div>
                <div style="background:var(--danger-bg); padding:15px; border-radius:15px; color:var(--danger);"><b>Wrong</b><br><span id="sWrong">0</span></div>
            </div>
            <button class="nav-btn primary" onclick="reviewMode()" style="width:100%; margin-bottom:10px;">Review Answers</button>
            <button class="nav-btn secondary" onclick="location.reload()" style="width:100%;">Restart</button>
        </div>
    </div>

    <script>
        const rawData = {json_str};
        const state = {{ 
            current: 0, 
            qs: [], 
            ans: [], 
            mode: null, 
            time: 3600, 
            isSub: false, 
            lang: 'en',
            sections: {{}},
            activeFilter: 'all'
        }};

        function setMode(m, el) {{
            state.mode = m;
            document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('startBtn').disabled = false;
        }}

        function toggleLang() {{
            state.lang = state.lang === 'en' ? 'hi' : 'en';
            renderQ();
        }}

        function startQuiz() {{
            const data = Array.isArray(rawData) ? rawData : (rawData.data || []);
            state.qs = data.map((q, idx) => {{
                // Detect Section
                const sec = q.section_name || q.section || "General";
                if(!state.sections[sec]) state.sections[sec] = [];
                state.sections[sec].push(idx);

                return {{
                    en: {{
                        text: q.question || q.question_en || "",
                        opts: [q.option_1, q.option_2, q.option_3, q.option_4, q.option_5].filter(Boolean),
                        sol: q.solution_text || q.solution || "No explanation."
                    }},
                    hi: {{
                        text: q.question_hi || q.question || "",
                        opts: [q.option_hi_1 || q.option_1, q.option_hi_2 || q.option_2, q.option_hi_3 || q.option_3, q.option_hi_4 || q.option_4, q.option_hi_5 || q.option_5].filter(Boolean),
                        sol: q.solution_hi || q.solution_text || q.solution || ""
                    }},
                    correct: (parseInt(q.answer) || 1) - 1,
                    img: q.image_url || q.question_image || null,
                    section: sec
                }};
            }});

            // Init Section Filter
            const filter = document.getElementById('sectionFilter');
            Object.keys(state.sections).forEach(s => {{
                filter.innerHTML += `<option value="${{s}}">${{s}}</option>`;
            }});

            state.ans = new Array(state.qs.length).fill(null);
            document.getElementById('modeSelection').classList.add('hidden');
            document.getElementById('quizContainer').style.display = 'block';
            
            renderQ();
            renderGrid();
            setInterval(() => {{ if(!state.isSub) {{ state.time--; updateTimer(); }} }}, 1000);
        }}

        function renderQ() {{
            const q = state.qs[state.current];
            const content = state.lang === 'en' ? q.en : q.hi;
            
            document.getElementById('currentSectionName').innerText = q.section;
            document.getElementById('qCountText').innerText = `Question ${{state.current + 1}} / ${{state.qs.length}}`;
            document.getElementById('pBar').style.width = `${{((state.current+1)/state.qs.length)*100}}%`;

            let h = `<div class="question-card">
                <div class="question-text">${{content.text}}</div>`;
            
            if(q.img) h += `<img src="${{q.img}}">`;
            
            h += `<div class="options-container">`;
            content.opts.forEach((o, i) => {{
                let cls = "option-btn";
                const isSel = state.ans[state.current] === i;
                const showRes = (state.mode === 'practice' && state.ans[state.current] !== null) || state.isSub;
                
                if(isSel) cls += " selected";
                if(showRes) {{
                    cls += " disabled";
                    if(i === q.correct) cls += " correct";
                    else if(isSel) cls += " incorrect";
                }}

                h += `<button class="${{cls}}" onclick="selectOpt(${{i}})">
                    <div class="option-indicator">${{String.fromCharCode(65+i)}}</div>
                    <div style="flex:1">${{o}}</div>
                </button>`;
            }});
            h += `</div>`;

            if((state.mode === 'practice' && state.ans[state.current] !== null) || state.isSub) {{
                h += `<div style="margin-top:20px; padding:15px; border-left:4px solid var(--warning); background:var(--bg-light); border-radius:0 12px 12px 0;">
                    <b style="color:var(--warning)">Explanation:</b><br>
                    <div style="font-size:13px; margin-top:5px;">${{content.sol}}</div>
                </div>`;
            }}

            h += `</div>`;
            document.getElementById('qArea').innerHTML = h;
            if(window.MathJax) MathJax.typeset();
        }}

        function selectOpt(i) {{
            if(state.ans[state.current] !== null || state.isSub) return;
            state.ans[state.current] = i;
            renderQ();
            updateGrid();
        }}

        function nextQ() {{
            if(state.current < state.qs.length - 1) {{
                state.current++;
                renderQ();
                updateGrid();
            }} else submitQuiz();
        }}

        function prevQ() {{
            if(state.current > 0) {{
                state.current--;
                renderQ();
                updateGrid();
            }}
        }}

        function renderGrid() {{
            const grid = document.getElementById('qGrid');
            grid.innerHTML = state.qs.map((q, i) => `
                <div class="q-item" id="q-${{i}}" onclick="jumpTo(${{i}})">${{i+1}}</div>
            `).join('');
            updateGrid();
        }}

        function updateGrid() {{
            state.qs.forEach((_, i) => {{
                const el = document.getElementById(`q-${{i}}`);
                if(!el) return;
                el.className = "q-item";
                if(i === state.current) el.classList.add('active');
                if(state.ans[i] !== null) el.classList.add('done');
                
                // Filter Visibility
                if(state.activeFilter !== 'all' && state.qs[i].section !== state.activeFilter) {{
                    el.classList.add('hidden');
                }}
            }});
        }}

        function filterGrid(val) {{
            state.activeFilter = val;
            updateGrid();
        }}

        function jumpTo(i) {{
            state.current = i;
            renderQ();
            toggleNav();
            updateGrid();
        }}

        function toggleNav() {{ document.getElementById('navPanel').classList.toggle('open'); }}

        function updateTimer() {{
            let m = Math.floor(state.time/60), s = state.time%60;
            document.getElementById('timeText').innerText = `${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}`;
            if(state.time <= 0) submitQuiz();
        }}

        function submitQuiz() {{
            if(!state.isSub && !confirm("Khatam karein?")) return;
            state.isSub = true;
            let c = state.ans.filter((a, i) => a === state.qs[i].correct).length;
            document.getElementById('quizContainer').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'block';
            document.getElementById('resScore').innerText = `${{c}} / ${{state.qs.length}}`;
            document.getElementById('resPercent').innerText = `${{((c/state.qs.length)*100).toFixed(1)}}%`;
            document.getElementById('sCorrect').innerText = c;
            document.getElementById('sWrong').innerText = state.ans.filter(a => a !== null).length - c;
        }}

        function reviewMode() {{
            document.getElementById('resultsContainer').style.display = 'none';
            document.getElementById('quizContainer').style.display = 'block';
            state.current = 0;
            renderQ();
        }}
    </script>
</body>
</html>'''
    return html