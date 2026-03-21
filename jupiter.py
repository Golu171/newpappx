import json
import re

def json_to_html(json_raw_data, title="IBPS RRB Officer Prelims", created_by="Ram"):
    # Data Parsing Logic
    data = json_raw_data if isinstance(json_raw_data, list) else json_raw_data.get('data', [])
    
    # Grouping by Subject (Sections)
    sections_dict = {}
    for q in data:
        subj = q.get('subject', 'General')
        if subj not in sections_dict:
            sections_dict[subj] = []
        sections_dict[subj].append(q)

    final_sections = []
    correct_map = {}
    q_blocks_html = ""
    total_q = 0
    sec_index = 0
    sec_hindi_map = {}

    for subj, qs in sections_dict.items():
        start_q = total_q + 1
        for i, q in enumerate(qs):
            total_q += 1
            ans = int(q.get('answer', 1))
            correct_map[str(total_q)] = ans
            
            # Extract options
            opts = [q.get(f'option_{i}') for i in range(1, 6) if q.get(f'option_{i}')]
            
            # Build Question HTML
            opt_html = ""
            for idx, opt in enumerate(opts):
                opt_html += f'''
                <div class="opt-row" id="opt-{total_q}-{idx+1}" onclick="selOpt({total_q},{idx+1})">
                    <div class="radio-outer"><div class="radio-inner"></div></div>
                    <span class="opt-lbl">{chr(65+idx)}.</span>
                    <div style="flex:1">
                        <div class="opt-text-en">{opt}</div>
                        <div class="opt-text-hi"></div>
                    </div>
                </div>'''

            q_blocks_html += f'''
            <div class="qblock" id="qblock-{total_q}" data-si="{sec_index}" data-ca="{ans}" data-sec="{subj}" data-mpq="1.0" style="display:none">
                <div class="q-bilingual">
                    <div class="q-text-en">{q.get('question', '')}</div>
                    {"<img src='"+q.get('image_url')+"'>" if q.get('image_url') else ""}
                </div>
                <div style="font-size:11px;font-weight:600;color:#888;margin:4px 0 6px;padding:0 20px">Choose the correct answer:</div>
                <div class="opts" id="opts-{total_q}">{opt_html}</div>
                <div class="sol-box" id="solbox-{total_q}">
                    <div class="sol-hdr">&#128161; Solution</div>
                    <div class="sol-body">{q.get('solution_text', 'No explanation provided.')}</div>
                </div>
            </div>'''

        final_sections.append({
            "name": subj,
            "start": start_q,
            "end": total_q,
            "secs": len(qs) * 45, # 45 sec per question default
            "max_score": len(qs)
        })
        sec_hindi_map[str(sec_index)] = True
        sec_index += 1

    sections_json = json.dumps(final_sections)
    correct_map_json = json.dumps(correct_map)
    sec_hindi_json = json.dumps(sec_hindi_map)

    # Building the HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* CSS DITTO SAME AS REF FILE */
        *{{box-sizing:border-box;margin:0;padding:0}}
        body{{font-family:'Segoe UI',Arial,sans-serif;font-size:14px;background:#e8e8e8;height:100vh;display:flex;flex-direction:column;overflow:hidden}}
        #hdr{{background:linear-gradient(135deg,#1a3a5c 0%,#0d2b47 100%);color:#fff;padding:0 16px;height:54px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid #f7a800;flex-shrink:0;}}
        .ibps-logo{{background:#f7a800;color:#1a3a5c;font-weight:900;font-size:16px;padding:4px 10px;border-radius:4px;}}
        .timer-box{{background:#fff;border:2px solid #f7a800;border-radius:4px;padding:4px 12px;text-align:center;min-width:90px;}}
        .timer-val{{font-size:16px;font-weight:700;color:#c0392b;font-family:monospace;}}
        #secbar{{background:#fff;border-bottom:1px solid #ccc;display:flex;height:40px;overflow-x:auto;scrollbar-width:none;}}
        .sec-tab{{padding:0 18px;cursor:pointer;font-size:12.5px;font-weight:600;color:#555;display:flex;align-items:center;transition:all .15s;border-bottom:3px solid transparent;}}
        .sec-tab.active{{color:#1a3a5c;border-bottom-color:#1a3a5c;background:#e8f0fb;}}
        #main{{display:flex;flex:1;overflow:hidden}}
        #qarea{{flex:1;overflow-y:auto;background:#fff;display:flex;flex-direction:column}}
        .q-header{{background:#f5f7fa;padding:8px 20px;border-bottom:1px solid #ddd;display:flex;justify-content:space-between;}}
        .opt-row{{display:flex;padding:10px 14px;cursor:pointer;border-bottom:1px solid #f0f0f0;}}
        .opt-row.selected{{background:#e8f0fe;}}
        .radio-outer{{width:17px;height:17px;border-radius:50%;border:2px solid #888;margin-right:10px;}}
        .selected .radio-inner{{width:9px;height:9px;background:#1a3a5c;border-radius:50%;margin:2px auto;display:block;}}
        #qfooter{{background:#f0f0f0;padding:8px 16px;display:flex;justify-content:space-between;border-top:1px solid #ccc;}}
        .btn{{padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:600;border:1px solid transparent;}}
        .btn-save{{background:#1a7a2e;color:#fff;}}
        #palette-wrap{{width:220px;background:#f5f7fa;border-left:1px solid #ddd;overflow-y:auto;}}
        .pq{{width:35px;height:35px;margin:2px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;cursor:pointer;border:1px solid #bbb;}}
        .pq.answered{{background:#27ae60;color:#fff;border-radius:50%;}}
        .pq.not-visited{{background:#d0d0d0;}}
        .pq.current{{outline:3px solid #f7a800;}}
        #scoreScreen, #solScreen, #noticeScreen, #instrScreen {{display:none;position:fixed;inset:0;background:#e8e8e8;z-index:1000;overflow-y:auto;padding:20px;}}
        .pre-card{{background:#fff;padding:20px;border-radius:8px;max-width:600px;margin:auto;box-shadow:0 4px 10px rgba(0,0,0,0.1);}}
        .sol-box{{background:#fffde7;padding:15px;border-left:4px solid #f9a825;margin-top:15px;display:none;}}
        body.submitted .sol-box {{display:block;}}
        .submitted-correct {{background:#e8f8e8 !important;}}
        .submitted-wrong {{background:#fdecea !important;}}
        @media (max-width:600px){{ #palette-wrap{{display:none;}} }}
    </style>
</head>
<body>
    <div id="noticeScreen" style="display:flex;">
        <div class="pre-card">
            <h1 style="color:#1a3a5c">Bees_X_Mock</h1>
            <p>Welcome to {title}. This is a simulated environment.</p>
            <button class="btn btn-save" style="margin-top:20px" onclick="showInstructions()">Next</button>
        </div>
    </div>

    <div id="instrScreen">
        <div class="pre-card">
            <h2>Instructions</h2>
            <ul style="padding:20px">
                <li>Total Questions: {total_q}</li>
                <li>Marking: +1.0 for Correct, -0.25 for Wrong.</li>
            </ul>
            <button class="btn btn-save" onclick="startTest()">Start Test</button>
        </div>
    </div>

    <div id="hdr">
        <div style="display:flex;align-items:center;gap:10px">
            <div class="ibps-logo">IBPS</div>
            <span class="exam-title">{title}</span>
        </div>
        <div class="timer-box">
            <div style="font-size:9px;color:#666">TIME LEFT</div>
            <div class="timer-val" id="timerVal">00:00:00</div>
        </div>
    </div>

    <div id="secbar"></div>

    <div id="main">
        <div id="qarea">
            <div class="q-header">
                <span id="qNumDisplay" class="q-num">Question No. 1</span>
                <span id="qMarksDisplay" class="q-marks">Marks: +1.0 | -0.25</span>
            </div>
            <div id="qcontent">{q_blocks_html}</div>
            <div id="qfooter">
                <button class="btn" onclick="goQ(currentQ-1)">Back</button>
                <div>
                    <button class="btn" style="background:#7b61d6;color:#fff" onclick="markForReview()">Mark for Review</button>
                    <button class="btn btn-save" id="btnSaveNext" onclick="saveAndNext()">Save & Next</button>
                    <button class="btn" id="btnSubmitExam" style="background:#c0392b;color:#fff;display:none" onclick="submitExam()">Submit Exam</button>
                </div>
            </div>
        </div>
        <div id="palette-wrap">
            <div class="palette-hdr" style="padding:10px;background:#1a3a5c;color:#fff">Palette</div>
            <div id="palGrid" style="padding:10px"></div>
        </div>
    </div>

    <div id="scoreScreen">
        <div class="pre-card" style="text-align:center">
            <h2>Result Summary</h2>
            <h1 id="finalScore" style="font-size:48px;color:#1a3a5c">0</h1>
            <p>Total Correct: <span id="scRight">0</span></p>
            <p>Total Wrong: <span id="scWrong">0</span></p>
            <button class="btn btn-save" onclick="location.reload()">Restart</button>
        </div>
    </div>

    <script>
        var SECTIONS = {sections_json};
        var CORRECT_MAP = {correct_map_json};
        var TOTAL = {total_q};
        var answers = {{}};
        var visited = {{}};
        var marked = {{}};
        var currentQ = 1;
        var activeSec = 0;
        var submitted = false;
        var timerInt;

        function showInstructions() {{ document.getElementById("noticeScreen").style.display="none"; document.getElementById("instrScreen").style.display="flex"; }}
        
        function startTest() {{
            document.getElementById("instrScreen").style.display="none";
            initSecBar();
            startSection(0);
        }}

        function initSecBar() {{
            let html = "";
            SECTIONS.forEach((s, i) => {{
                html += `<div class="sec-tab" id="sectab-${{i}}" onclick="goQ(${{s.start}})">${{s.name}}</div>`;
            }});
            document.getElementById("secbar").innerHTML = html;
        }}

        function startSection(si) {{
            activeSec = si;
            renderPalette();
            goQ(SECTIONS[si].start);
            startTimer(SECTIONS[si].secs);
        }}

        function goQ(qn) {{
            if(qn < 1 || qn > TOTAL) return;
            document.querySelectorAll(".qblock").forEach(b => b.style.display="none");
            document.getElementById("qblock-"+qn).style.display="block";
            currentQ = qn;
            visited[qn] = true;
            document.getElementById("qNumDisplay").textContent = "Question No. " + qn;
            updatePalette();
            
            let si = SECTIONS.findIndex(s => qn >= s.start && qn <= s.end);
            document.querySelectorAll(".sec-tab").forEach((t, i) => t.classList.toggle("active", i === si));
            
            document.getElementById("btnSubmitExam").style.display = (qn === TOTAL) ? "inline-block" : "none";
        }}

        function selOpt(qn, idx) {{
            if(submitted) return;
            answers[qn] = idx;
            document.querySelectorAll("#opts-"+qn+" .opt-row").forEach((r, i) => {{
                r.classList.toggle("selected", (i+1)===idx);
            }});
            updatePalette();
        }}

        function saveAndNext() {{ if(currentQ < TOTAL) goQ(currentQ+1); }}

        function markForReview() {{ marked[currentQ] = true; saveAndNext(); }}

        function updatePalette() {{
            let html = "";
            for(let i=1; i<=TOTAL; i++) {{
                let cls = "pq ";
                if(answers[i]) cls += "answered ";
                else if(visited[i]) cls += "not-answered ";
                else cls += "not-visited ";
                if(i === currentQ) cls += "current ";
                html += `<div class="${{cls}}" onclick="goQ(${{i}})">${{i}}</div>`;
            }}
            document.getElementById("palGrid").innerHTML = html;
        }}

        function startTimer(s) {{
            clearInterval(timerInt);
            timerInt = setInterval(() => {{
                s--;
                let h = Math.floor(s/3600), m = Math.floor((s%3600)/60), sc = s%60;
                document.getElementById("timerVal").textContent = 
                    (h<10?"0":"")+h+":"+(m<10?"0":"")+m+":"+(sc<10?"0":"")+sc;
                if(s<=0) submitExam();
            }}, 1000);
        }}

        function submitExam() {{
            clearInterval(timerInt);
            submitted = true;
            document.body.classList.add("submitted");
            let score = 0, right = 0, wrong = 0;
            for(let q in CORRECT_MAP) {{
                if(answers[q] == CORRECT_MAP[q]) {{ score += 1; right++; }}
                else if(answers[q]) {{ score -= 0.25; wrong++; }}
            }}
            document.getElementById("finalScore").textContent = score.toFixed(2);
            document.getElementById("scRight").textContent = right;
            document.getElementById("scWrong").textContent = wrong;
            document.getElementById("scoreScreen").style.display = "block";
        }}

        function renderPalette() {{ updatePalette(); }}
    </script>
</body>
</html>'''
    return html
