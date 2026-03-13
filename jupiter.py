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
        
        .lang-btn {{ background: var(--accent); color: white; border: none; padding: 8px 15px; border-radius: 12px; font-weight: 700; cursor: pointer; }}
        .section-name {{ font-size: 11px; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; display: block; }}

        .question-section {{ position: fixed; top: 155px; left: 0; right: 0; bottom: 85px; overflow-y: auto; padding: 20px; }}
        .question-card {{ background: var(--bg-white); border-radius: 24px; padding: 28px; box-shadow: var(--shadow-md); max-width: 800px; margin: 0 auto; }}
        .option-btn {{ width: 100%; padding: 18px 20px; background: var(--bg-light); border: 3px solid var(--border); border-radius: 16px; text-align: left; font-size: 15px; color: var(--text-dark); cursor: pointer; display: flex; align-items: flex-start; gap: 14px; transition: 0.3s; margin-bottom: 14px; line-height: 1.6; }}
        .option-indicator {{ min-width: 36px; height: 36px; border-radius: 50%; background: var(--bg-white); border: 2px solid var(--border); display: flex; align-items: center; justify-content: center; font-weight: 700; }}
        .option-btn.selected {{ background: var(--primary-glow); border-color: var(--primary); }}
        
        /* Navigator Panel styles from your original */
        .nav-controls {{ position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-white); padding: 16px 20px; box-shadow: 0 -4px 20px rgba(0,0,0,0.08); display: flex; gap: 12px; z-index: 90; }}
        .nav-btn {{ flex: 1; padding: 16px; border: none; border-radius: 14px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }}
        .nav-btn.primary {{ background: linear-gradient(135deg, var(--primary), var(--accent)); color: white; }}
        .nav-btn.secondary {{ background: var(--bg-light); color: var(--text-dark); border: 2px solid var(--border); }}
        .question-nav-toggle {{ position: fixed; bottom: 105px; right: 20px; width: 60px; height: 60px; background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; border: none; border-radius: 50%; font-size: 24px; cursor: pointer; z-index: 85; box-shadow: 0 8px 25px var(--primary-glow); }}
        .question-nav-panel {{ position: fixed; bottom: 0; left: 0; right: 0; height: 35vh; overflow-y: auto; background: var(--bg-white); border-radius: 28px 28px 0 0; box-shadow: 0 -8px 40px rgba(0,0,0,0.2); z-index: 95; transform: translateY(110%); transition: transform 0.35s ease; padding: 18px; visibility: hidden; }}
        .question-nav-panel.open {{ transform: translateY(0); visibility: visible; }}
        .question-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }}
        .question-nav-item {{ aspect-ratio: 1; border: 3px solid var(--border); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-weight: 700; cursor: pointer; color: var(--text-light); }}
        .question-nav-item.current {{ border-color: var(--primary); color: var(--primary); }}
        .question-nav-item.answered {{ background: var(--primary); color: white; border: none; }}
        
        #resultsContainer {{ display: none; position: fixed; inset: 0; background: var(--bg-light); overflow-y: auto; padding: 20px; text-align: center; }}
        img {{ max-width: 100%; border-radius: 12px; margin-top: 15px; }}
    </style>
</head>
<body>
    <div id="modeSelection">
        <div class="mode-container">
            <div class="mode-header">
                <div class="mode-header-icon"><i class="fas fa-brain"></i></div>
                <h2 style="font-weight:800; color:#1E293B;">{title}</h2>
                <p>Choose test mode to begin</p>
            </div>
            <div class="mode-cards">
                <div class="mode-card exam-mode" onclick="setMode('exam', this)">
                    <div style="background:#EF4444; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-file-alt"></i></div>
                    <div><h3 style="font-size:17px;">🎯 Exam Mode</h3><p style="font-size:13px; color:var(--text-light);">Results at end</p></div>
                </div>
                <div class="mode-card practice-mode" onclick="setMode('practice', this)">
                    <div style="background:#10B981; width:45px; height:45px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-book-open"></i></div>
                    <div><h3 style="font-size:17px;">📚 Practice Mode</h3><p style="font-size:13px; color:var(--text-light);">Instant feedback</p></div>
                </div>
            </div>
            <button class="nav-btn primary" id="startBtn" disabled onclick="startQuiz()" style="width:100%; padding:18px;">Start Quiz</button>
        </div>
    </div>

    <div id="quizContainer">
        <div class="quiz-header">
            <div class="header-top">
                <div>
                    <span id="sectionDisplay" class="section-name">SECTION</span>
                    <div style="font-weight:700; font-size:14px; color:var(--text-dark); max-width:150px; overflow:hidden; white-space:nowrap;">{title}</div>
                </div>
                <div class="header-actions" style="display:flex; gap:10px; align-items:center;">
                    <button class="lang-btn" onclick="toggleLang()" id="langBtn">EN</button>
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
            <div style="display:flex; justify-content:space-between; margin-bottom:20px;"><h3>Navigator</h3><button onclick="toggleNav()" style="border:none; background:none; font-size:24px;">&times;</button></div>
            <div class="question-grid" id="qGrid"></div>
        </div>
    </div>

    <div id="resultsContainer">
        <div class="results-card" style="background: white; padding: 40px; border-radius: 28px; box-shadow: var(--shadow-lg); max-width: 600px; margin: 0 auto;">
            <div style="font-size:80px;">🏆</div>
            <h2 id="resScore" style="font-size:56px; font-weight:800;">0/0</h2>
            <div id="resPercent" style="font-size:22px; font-weight:600; color:var(--text-light); margin-bottom:20px;">0%</div>
            <button class="nav-btn primary" onclick="reviewMode()" style="width:100%; margin-bottom:10px;">Review Answers</button>
            <button class="nav-btn secondary" onclick="location.reload()" style="width:100%;">Restart Quiz</button>
        </div>
    </div>

    <script>
        const rawData = {json_str};
        const state = {{ current: 0, qs: [], ans: [], marked: [], mode: null, time: 3600, isSub: false, theme: 'light', lang: 'en' }};

        function setMode(m, el) {{
            state.mode = m;
            document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('selected'));
            el.classList.add('selected');
            document.getElementById('startBtn').disabled = false;
        }}

        function toggleLang() {{
            state.lang = state.lang === 'en' ? 'hi' : 'en';
            document.getElementById('langBtn').innerText = state.lang.toUpperCase();
            renderQ();
        }}

        function startQuiz() {{
            const data = Array.isArray(rawData) ? rawData : (rawData.data || []);
            state.qs = data.map(q => ({{
                section: q.section_name || q.section || "General",
                en: {{
                    text: (q.question_en || q.question || "").trim(),
                    opts: [q.option_1, q.option_2, q.option_3, q.option_4, q.option_5].filter(Boolean),
                    sol: q.solution_en || q.solution_text || q.solution || "No explanation."
                }},
                hi: {{
                    text: (q.question_hi || q.question || "").trim(),
                    opts: [q.option_hi_1 || q.option_1, q.option_hi_2 || q.option_2, q.option_hi_3 || q.option_3, q.option_hi_4 || q.option_4, q.option_hi_5 || q.option_5].filter(Boolean),
                    sol: q.solution_hi || q.solution_text || q.solution || "व्याख्या उपलब्ध नहीं है।"
                }},
                correct: parseInt(q.answer) - 1,
                img: q.image_url || q.question_image || null
            }}));
            
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
            const content = state.lang === 'en' ? q.en : q.hi;
            
            document.getElementById('sectionDisplay').innerText = q.section;
            
            let h = `<div class="question-card"><div class="question-text">${{content.text}}</div>`;
            if(q.img) h += `<img src="${{q.img}}">`;
            h += `<div class="options-container">`;
            content.opts.forEach((o, i) => {{
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
                h += `<div style="margin-top:20px; padding:15px; border-left:5px solid var(--warning); background:var(--bg-light); border-radius:12px;">
                    <b style="color:var(--warning)">Explanation:</b><br><div style="font-size:14px;">${{content.sol}}</div>
                </div>`;
            }}
            h += `</div>`;
            document.getElementById('qArea').innerHTML = h;
            if(window.MathJax) MathJax.typeset();
            updateUI();
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

        function nextQ() {{ if(state.current < state.qs.length - 1) {{ state.current++; renderQ(); }} else submitQuiz(); }}
        function prevQ() {{ if(state.current > 0) {{ state.current--; renderQ(); }} }}
        function toggleNav() {{ document.getElementById('navPanel').classList.toggle('open'); }}
        function renderGrid() {{
            document.getElementById('qGrid').innerHTML = state.qs.map((_, i) => `<div class="question-nav-item" id="nav-${{i}}" onclick="goTo(${{i}})">${{i+1}}</div>`).join('');
            updateGrid();
        }}
        function updateGrid() {{
            state.qs.forEach((_, i) => {{
                const el = document.getElementById(`nav-${{i}}`);
                el.className = "question-nav-item";
                if(i === state.current) el.classList.add('current');
                if(state.ans[i] !== null) el.classList.add('answered');
            }});
        }}
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
        function toggleMark() {{ state.marked[state.current] = !state.marked[state.current]; updateGrid(); }}
    </script>
</body>
</html>'''
    return html