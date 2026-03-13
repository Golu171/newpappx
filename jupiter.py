import json

def json_to_html(json_raw_data, title="Test Series", created_by="Ram"):
    # JSON data string for injection
    json_str = json.dumps(json_raw_data)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{title}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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
        
        /* Language Toggle Classes */
        .lang-hi span {{ display: none; }} /* Default: hide hindi inside span if any */
        [data-lang="hi"] .en-txt {{ display: none; }}
        [data-lang="en"] .hi-txt {{ display: none; }}

        #modeSelection {{ position: fixed; inset: 0; background: inherit; display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 20px; }}
        .mode-container {{ background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-radius: 28px; padding: 40px 30px; max-width: 520px; width: 100%; box-shadow: var(--shadow-lg); text-align: center; }}
        .mode-header-icon {{ width: 80px; height: 80px; margin: 0 auto 20px; background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); border-radius: 24px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: white; animation: float 3s ease-in-out infinite; }}
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
        
        .mode-cards {{ display: grid; gap: 16px; margin-bottom: 24px; }}
        .mode-card {{ background: var(--bg-light); border: 3px solid var(--border); border-radius: 18px; padding: 18px; cursor: pointer; transition: 0.3s; display: flex; align-items: center; gap: 15px; text-align: left; }}
        .mode-card.selected {{ border-color: var(--primary); background: rgba(99,102,241,0.1); transform: translateY(-2px); }}
        
        #quizContainer {{ display: none; position: fixed; inset: 0; background: var(--bg-light); overflow: hidden; }}
        .quiz-header {{ position: fixed; top: 0; left: 0; right: 0; background: var(--bg-white); box-shadow: var(--shadow-sm); z-index: 100; padding: 16px 20px; }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .timer-display {{ background: var(--primary-glow); padding: 8px 15px; border-radius: 12px; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 8px; }}
        .progress-bar-container {{ height: 8px; background: var(--border); border-radius: 10px; overflow: hidden; }}
        .progress-bar {{ height: 100%; background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent)); transition: width 0.4s ease; }}
        
        /* Section Badge & Lang Toggle */
        .sec-badge {{ font-size: 10px; font-weight: 800; color: var(--primary); background: var(--primary-glow); padding: 2px 8px; border-radius: 6px; text-transform: uppercase; }}
        .lang-toggle-btn {{ background: var(--accent); color: white; border: none; padding: 6px 12px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 12px; }}

        .question-section {{ position: fixed; top: 145px; left: 0; right: 0; bottom: 85px; overflow-y: auto; padding: 20px; }}
        .question-card {{ background: var(--bg-white); border-radius: 24px; padding: 28px; box-shadow: var(--shadow-md); max-width: 800px; margin: 0 auto; }}
        .option-btn {{ width: 100%; padding: 18px 20px; background: var(--bg-light); border: 3px solid var(--border); border-radius: 16px; text-align: left; font-size: 15px; color: var(--text-dark); cursor: pointer; display: flex; align-items: flex-start; gap: 14px; transition: 0.3s; margin-bottom: 14px; line-height: 1.6; }}
        
        .nav-controls {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-white); padding: 16px 20px; box-shadow: 0 -4px 20px rgba(0,0,0,0.08); display: flex; gap: 12px; z-index: 90; }}
        .nav-btn {{ flex: 1; padding: 16px; border: none; border-radius: 14px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }}
        .nav-btn.primary {{ background: linear-gradient(135deg, var(--primary), var(--accent)); color: white; }}
        
        .question-nav-toggle {{ position: fixed; bottom: 105px; right: 20px; width: 60px; height: 60px; background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; border: none; border-radius: 50%; font-size: 24px; cursor: pointer; z-index: 85; box-shadow: 0 8px 25px var(--primary-glow); }}
        .question-nav-panel {{ position: fixed; bottom: 0; left: 0; right: 0; height: 40vh; overflow-y: auto; background: var(--bg-white); border-radius: 28px 28px 0 0; box-shadow: 0 -8px 40px rgba(0,0,0,0.2); z-index: 95; transform: translateY(110%); transition: 0.35s; padding: 18px; visibility: hidden; }}
        .question-nav-panel.open {{ transform: translateY(0); visibility: visible; }}
        .question-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }}
        .question-nav-item {{ aspect-ratio: 1; border: 3px solid var(--border); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-weight: 700; cursor: pointer; }}
        .question-nav-item.current {{ border-color: var(--primary); color: var(--primary); }}
        .question-nav-item.answered {{ background: var(--primary); color: white; border: none; }}
        
        .section-filter {{ width: 100%; padding: 12px; border-radius: 12px; border: 2px solid var(--border); margin-bottom: 15px; font-family: inherit; font-weight: 600; color: var(--text-dark); }}
        
        img {{ max-width: 100%; border-radius: 12px; margin-top: 15px; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body data-lang="en">
    <div id="modeSelection">
        <div class="mode-container">
            <div class="mode-header">
                <div class="mode-header-icon"><i class="fas fa-brain"></i></div>
                <h2 style="font-weight:800; color:#1E293B;">{title}</h2>
                <p>Choose test mode to begin</p>
            </div>
            <div class="mode-cards">
                <div class="mode-card exam-mode" onclick="setMode('exam', this)">
                    <div style="background:#EF4444; width:50px; height:50px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-file-alt"></i></div>
                    <div><h3 style="font-size:17px;">🎯 Exam Mode</h3><p style="font-size:13px; color:var(--text-light);">Results at end</p></div>
                </div>
                <div class="mode-card practice-mode" onclick="setMode('practice', this)">
                    <div style="background:#10B981; width:50px; height:50px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-book-open"></i></div>
                    <div><h3 style="font-size:17px;">📚 Practice Mode</h3><p style="font-size:13px; color:var(--text-light);">Instant feedback</p></div>
                </div>
            </div>
            <input type="number" id="customTimer" style="width:100%; padding:16px; border:3px solid var(--border); border-radius:14px; margin-bottom:20px;" placeholder="Timer (Minutes) - Default 60">
            <button class="nav-btn primary" id="startBtn" disabled onclick="startQuiz()" style="width:100%; padding:18px;">Start Quiz</button>
        </div>
    </div>

    <div id="quizContainer">
        <div class="quiz-header">
            <div class="header-top">
                <div>
                    <span id="activeSectionName" class="sec-badge">General</span>
                    <div style="font-weight:700; font-size:14px; color:var(--text-dark); max-width:180px; overflow:hidden; white-space:nowrap;">{title}</div>
                </div>
                <div class="header-actions" style="display:flex; gap:10px; align-items:center;">
                    <button class="lang-toggle-btn" onclick="toggleLang()" id="langBtn">EN</button>
                    <button onclick="toggleTheme()" style="width:40px; height:40px; border-radius:12px; border:2px solid var(--border); background:var(--bg-light); cursor:pointer;"><i class="fas fa-moon"></i></button>
                    <div class="timer-display"><i class="fas fa-stopwatch"></i> <span id="timeText">00:00</span></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:10px; color:var(--text-light);">
                <span id="pText">Question 1</span><span id="aText">Attempted: 0/0</span>
            </div>
            <div class="progress-bar-container"><div class="progress-bar" id="pBar"></div></div>
        </div>
        <div class="question-section scrollable" id="qArea"></div>
        <div class="nav-controls">
            <button class="nav-btn secondary" onclick="prevQ()"><i class="fas fa-arrow-left"></i> Prev</button>
            <button class="nav-btn secondary" id="markBtn" onclick="toggleMark()">Mark</button>
            <button class="nav-btn primary" id="nextBtn" onclick="nextQ()">Next <i class="fas fa-arrow-right"></i></button>
        </div>
        <button class="question-nav-toggle" onclick="toggleNav()"><i class="fas fa-th"></i></button>
        <div class="question-nav-panel" id="navPanel">
            <div style="display:flex; justify-content:space-between; margin-bottom:15px;"><h3>Navigator</h3><button onclick="toggleNav()" style="border:none; background:none; font-size:24px;">&times;</button></div>
            <select class="section-filter" id="sectionSelector" onchange="filterQuestions(this.value)">
                <option value="all">All Sections</option>
            </select>
            <div class="question-grid" id="qGrid"></div>
        </div>
    </div>

    <div id="resultsContainer">
        <div class="results-card" style="background:white; border-radius:28px; padding:40px; max-width:600px; margin:0 auto; box-shadow:var(--shadow-lg); text-align:center;">
            <div style="font-size:80px;">🏆</div>
            <h2 class="results-title">Quiz Completed!</h2>
            <div class="results-score" id="resScore" style="font-size:56px; font-weight:800;">0/0</div>
            <div id="resPercent" style="font-size:22px; font-weight:600; color:var(--text-light); margin-bottom:25px;">0%</div>
            <button class="nav-btn primary" onclick="reviewMode()" style="width:100%; margin-bottom:10px;">Review Answers</button>
            <button class="nav-btn secondary" onclick="location.reload()" style="width:100%;">Restart Quiz</button>
        </div>
    </div>

    <script>
        const rawData = {json_str};
        const state = {{ current: 0, qs: [], ans: [], marked: [], mode: null, time: 3600, isSub: false, theme: 'light', lang: 'en', sections: {{}}, filter: 'all' }};

        function setMode(m, el) {{
            state.mode = m;
            document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('startBtn').disabled = false;
        }}

        function toggleLang() {{
            state.lang = state.lang === 'en' ? 'hi' : 'en';
            document.body.setAttribute('data-lang', state.lang);
            document.getElementById('langBtn').innerText = state.lang.toUpperCase();
            renderQ();
        }}

        function startQuiz() {{
            const ct = parseInt(document.getElementById('customTimer').value);
            if(ct > 0) state.time = ct * 60;
            
            const data = Array.isArray(rawData) ? rawData : (rawData.data || []);
            state.qs = data.map((q, idx) => {{
                // Handle Sections
                const sName = q.section_name || q.subject || "General";
                if(!state.sections[sName]) state.sections[sName] = [];
                state.sections[sName].push(idx);

                return {{
                    text: q.question.replace(/<style.*?<\\/style>/gs, "").trim(),
                    opts: [q.option_1, q.option_2, q.option_3, q.option_4, q.option_5].map(o => o ? o.replace(/<style.*?<\\/style>/gs, "").trim() : null).filter(Boolean),
                    correct: parseInt(q.answer) - 1,
                    sol: (q.solution_text || q.solution || "No explanation.").replace(/<style.*?<\\/style>/gs, ""),
                    img: q.image_url || q.question_image || null,
                    section: sName
                }};
            }});

            // Fill Section Dropdown
            const sel = document.getElementById('sectionSelector');
            Object.keys(state.sections).forEach(s => {{
                const opt = document.createElement('option');
                opt.value = s; opt.innerText = s; sel.appendChild(opt);
            }});

            state.ans = new Array(state.qs.length).fill(null);
            state.marked = new Array(state.qs.length).fill(false);
            
            document.getElementById('modeSelection').style.display = 'none';
            document.getElementById('quizContainer').style.display = 'block';
            renderQ();
            renderGrid();
            setInterval(() => {{ if(!state.isSub) {{ state.time--; updateTimer(); }} }}, 1000);
        }}

        function renderQ() {{
            const q = state.qs[state.current];
            document.getElementById('activeSectionName').innerText = q.section;
            
            let h = `<div class="question-card">
                <div class="question-text">${{q.text}}</div>`;
            if(q.img) h += `<img src="${{q.img}}">`;
            h += `<div class="options-container">`;
            q.opts.forEach((o, i) => {{
                let cls = "option-btn";
                const sel = state.ans[state.current] === i;
                const rev = (state.mode === 'practice' && state.ans[state.current] !== null) || state.isSub;
                if(sel) cls += " selected";
                if(rev) {{
                    cls += " disabled";
                    if(i === q.correct) cls += " correct";
                    else if(sel) cls += " incorrect";
                }}
                h += `<button class="${{cls}}" onclick="selectOpt(${{i}})">
                    <div class="option-indicator">${{String.fromCharCode(65+i)}}</div><div style="flex:1">${{o}}</div>
                </button>`;
            }});
            h += `</div>`;
            if(((state.mode === 'practice' && state.ans[state.current] !== null) || state.isSub)) {{
                h += `<div style="display:block; background:#fff; border-left:5px solid #F59E0B; padding:20px; margin-top:24px; border-radius:0 16px 16px 0;">
                    <div style="font-weight:800; color:#92400E; margin-bottom:10px;"><i class="fas fa-lightbulb"></i> Explanation</div>
                    <div style="font-size:14px; line-height:1.6; color:green;">${{q.sol}}</div>
                </div>`;
            }}
            h += `</div>`;
            document.getElementById('qArea').innerHTML = h;
            updateUI();
        }}

        function filterQuestions(val) {{
            state.filter = val;
            renderGrid();
        }}

        function selectOpt(i) {{
            if(state.ans[state.current] !== null || state.isSub) return;
            state.ans[state.current] = i;
            renderQ();
            updateGrid();
        }}

        function updateUI() {{
            document.getElementById('pText').innerText = `Question ${{state.current+1}}`;
            document.getElementById('aText').innerText = `Attempted: ${{state.ans.filter(a => a !== null).length}}/${{state.qs.length}}`;
            document.getElementById('pBar').style.width = `${{((state.current+1)/state.qs.length)*100}}%`;
            document.getElementById('nextBtn').innerHTML = (state.current === state.qs.length-1) ? 'Submit <i class="fas fa-paper-plane"></i>' : 'Next <i class="fas fa-arrow-right"></i>';
        }}

        function renderGrid() {{
            const grid = document.getElementById('qGrid');
            grid.innerHTML = '';
            state.qs.forEach((q, i) => {{
                if(state.filter !== 'all' && q.section !== state.filter) return;
                const div = document.createElement('div');
                div.className = 'question-nav-item';
                div.id = `nav-${{i}}`;
                div.innerText = i + 1;
                div.onclick = () => goTo(i);
                grid.appendChild(div);
            }});
            updateGrid();
        }}

        function updateGrid() {{
            state.qs.forEach((_, i) => {{
                const el = document.getElementById(`nav-${{i}}`);
                if(!el) return;
                el.className = "question-nav-item";
                if(i === state.current) el.classList.add('current');
                if(state.ans[i] !== null) el.classList.add('answered');
            }});
        }}

        function nextQ() {{ if(state.current < state.qs.length - 1) {{ state.current++; renderQ(); }} else submitQuiz(); }}
        function prevQ() {{ if(state.current > 0) {{ state.current--; renderQ(); }} }}
        function toggleNav() {{ document.getElementById('navPanel').classList.toggle('open'); }}
        function goTo(i) {{ state.current = i; renderQ(); toggleNav(); }}
        function updateTimer() {{
            let m = Math.floor(state.time/60), s = state.time%60;
            document.getElementById('timeText').innerText = `${{m.toString().padStart(2,'0')}}:${{s.toString().padStart(2,'0')}}`;
            if(state.time <= 0) submitQuiz();
        }}
        function submitQuiz() {{
            if(!state.isSub && !confirm("Submit Quiz?")) return;
            state.isSub = true;
            let c = state.ans.filter((a, i) => a === state.qs[i].correct).length;
            document.getElementById('quizContainer').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'block';
            document.getElementById('resScore').innerText = `${{c}} / ${{state.qs.length}}`;
            document.getElementById('resPercent').innerText = `${{((c/state.qs.length)*100).toFixed(1)}}%`;
        }}
        function reviewMode() {{ document.getElementById('resultsContainer').style.display = 'none'; document.getElementById('quizContainer').style.display = 'block'; state.current = 0; renderQ(); updateGrid(); }}
        function toggleTheme() {{ state.theme = state.theme === 'light' ? 'dark' : 'light'; document.documentElement.setAttribute('data-theme', state.theme); }}
        function toggleMark() {{ state.marked[state.current] = !state.marked[state.current]; updateUI(); }}
    </script>
</body>
</html>'''
    return html