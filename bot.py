import os, shutil, zipfile, asyncio, logging, threading, gc
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

import cloudscraper
from jupiter import json_to_html

# --- RENDER PORT BINDING ---
server = Flask(__name__)
@server.route('/')
def ping(): return "Bot is Fast & Alive!", 200
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

# --- CONFIG & HEADERS ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})

TOKEN = os.environ.get("BOT_TOKEN")

# Global Headers Sets
HEADERS = {"Client-Service": "Appx", "Auth-Key": "appxapi", "source": "website", "User-ID": "82093"}

HSSC_HEADERS = {
    **HEADERS, "User-ID": "22997",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIyOTk3IiwiZW1haWwiOiJzYW5kaXNpcjc0MUBnbWFpbC5jb20iLCJuYW1lIjoiU2FuZGVlcCBTaGVvcmFuIiwidGltZXN0YW1wIjoxNzczMzM1OTQwLCJ0ZW5hbnRUeXBlIjoidXNlciIsInRlbmFudE5hbWUiOiJoc3NjZ3VpZGVfZGIiLCJ0ZW5hbnRJZCI6IiIsImRpc3Bvc2FibGUiOmZhbHNlfQ.uhzOeNxEcBbV0EcFNFRWaLaS-EzrPgHovjv3mQhbdv8",
    "X-Requested-With": "mark.via.gp"
}

AGG_HEADERS = {
    **HEADERS, "User-ID": "1558",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE1NTgiLCJlbWFpbCI6InNhbmRpc2lyNzQxQGdtYWlsLmNvbSIsIm5hbWUiOiJTYW5kZWVwIFNoZW9yYW4iLCJ0aW1lc3RhbXAiOjE3NzMzMzY0NjIsInRlbmFudFR5cGUiOiJ1c2VyIiwidGVuYW50TmFtZSI6Imhzc2NndXJ1a3VsX2RiIiwidGVuYW50SWQiOiIiLCJkaXNwb3NhYmxlIjpmYWxzZX0.DzdLa897zaE_MrZR_tokxpvVMNzDdV7skI_jLDoHhxQ",
    "X-Requested-With": "mark.via.gp"
}

# Conversation States
API_URL, CREATOR_NAME, CHOOSE_TYPE, HSSC_ID, SELECT_SECTION, SELECT_ITEM, UPLOAD_CHOICE = range(7)

# ---------------- HELPER FUNCTIONS ---------------- #

def save_html_sync(test_data, title, out_path, creator):
    try:
        html = json_to_html(test_data, title, creator)
        with open(out_path, "w", encoding="utf-8") as f: f.write(html)
        return True
    except: return False

async def explore_recursively(api_url, course_id, parent_id, tests_list, current_path="Main", headers=HEADERS):
    url = f"{api_url}/get/folder_contentsv3?course_id={course_id}&parent_id={parent_id}&start=0"
    try:
        resp = scraper.get(url, headers=headers, timeout=15).json()
        for item in resp.get("data", []):
            if item.get("material_type") == "TEST":
                tid = item.get("quiz_title_id")
                if tid and tid != "-1":
                    t_url = f"{api_url}/get/test_title_by_id?id={tid}&userid={headers['User-ID']}"
                    d = scraper.get(t_url, headers=headers, timeout=15).json().get("data", {})
                    if d.get("test_questions_url"):
                        tests_list.append({'title': d['title'], 'link': d['test_questions_url'], 'folder': current_path})
            elif item.get("material_type") == "FOLDER":
                new_path = f"{current_path}/{item.get('folder_name', 'Sub')}"
                await explore_recursively(api_url, course_id, item.get("id"), tests_list, new_path, headers)
    except: pass

# ---------------- BOT HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ðŸ•‰ *Jai Shree Ram*\n\nRam's Ultimate Extractor V8 (Aggregator Support). \nUse /extract to begin.")

async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ðŸ”— *API URL bhej bhai:*")
    return API_URL

async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    api_url = f"https://{url}" if "http" not in url else url
    context.user_data['api_url'] = api_url
    
    if "akamai" in api_url:
        context.user_data['is_akamai'] = True
        context.user_data['mode_headers'] = AGG_HEADERS if ("eduguru" in api_url or "hsscgurukul" in api_url) else HSSC_HEADERS
        await update.message.reply_text("ðŸ›¡ï¸ *Akamai Protection Detected!* \nâœï¸ Creator Name?")
    else:
        context.user_data['is_akamai'] = False
        context.user_data['mode_headers'] = HEADERS
        await update.message.reply_text("âœï¸ Coaching/Creator Name?")
    return CREATOR_NAME

async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['creator'] = update.message.text.strip()
    
    if context.user_data.get('is_akamai'):
        kb = [[InlineKeyboardButton("ðŸ”¥ HSSC Mode", callback_data="type_hssc")],
              [InlineKeyboardButton("ðŸ“‚ Aggregator (EduGuru)", callback_data="type_agg")]]
    else:
        kb = [[InlineKeyboardButton("ðŸ“š Mode 1 (Course)", callback_data="type_course")],
              [InlineKeyboardButton("ðŸŽ¯ Mode 2 (Series)", callback_data="type_series")]]
    
    await update.message.reply_text("ðŸ¤” *Select Mode:*", reply_markup=InlineKeyboardMarkup(kb))
    return CHOOSE_TYPE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data['type'] = choice
    headers = context.user_data['mode_headers']

    if choice == "hssc":
        await query.edit_message_text("ðŸ”¢ *HSSC Course ID bhej (e.g. 17, 25):*")
        return HSSC_ID
    
    elif choice == "agg":
        await query.edit_message_text("ðŸ“¡ *Fetching Exam Sections...*")
        agg_api = "https://thetestpassapi.akamai.net.in"
        client_api = "https://hsscgurukulapi.akamai.net.in/"
        url = f"{agg_api}/get/get_testseries_exams?start=0&search&client_api_url={client_api}&exam_id"
        r = scraper.get(url, headers=headers).json()
        sections = [(exam["id"], exam["exam_name"]) for exam in r.get("data", [])]
        
        btns = []
        for i in range(0, len(sections), 2):
            row = [InlineKeyboardButton(sections[i][1][:20], callback_data=f"sec_{sections[i][0]}")]
            if i + 1 < len(sections):
                row.append(InlineKeyboardButton(sections[i+1][1][:20], callback_data=f"sec_{sections[i+1][0]}"))
            btns.append(row)
        
        await query.message.reply_text("ðŸ“š *Select Exam Section:*", reply_markup=InlineKeyboardMarkup(btns))
        return SELECT_SECTION

    # Normal Appx Course/Series Logic
    api_url = context.user_data['api_url']
    await query.edit_message_text(f"ðŸ“¡ Scanning {choice.upper()}...")
    try:
        if choice == "course":
            p = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
            r = scraper.post(f"{api_url}/get/search", headers=headers, json=p).json()
            items = [(c["id"], c["course_name"]) for c in r.get("courses_with_folder", [])]
        else:
            r = scraper.get(f"{api_url}/get/test_series?start=-1", headers=headers).json()
            items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]
        
        context.user_data['item_names'] = {str(i[0]): i[1] for i in items}
        btns = [[InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")] for i in items[:40]]
        await query.message.reply_text("ðŸŽ¯ *Target Select Kar:*", reply_markup=InlineKeyboardMarkup(btns))
        return SELECT_ITEM
    except: return ConversationHandler.END

async def get_hssc_course_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.text.strip()
    headers = context.user_data['mode_headers']
    api_url = context.user_data['api_url']
    r = scraper.get(f"{api_url}/get/coursenew_by_idv2?id={cid}", headers=headers).json()
    items = [(f["id"], f["folder_name"]) for f in r["data"].get("course_content", [])]
    context.user_data['item_names'] = {str(i[0]): i[1] for i in items}
    btns = [[InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")] for i in items[:40]]
    await update.message.reply_text("ðŸŽ¯ *Select Folder:*", reply_markup=InlineKeyboardMarkup(btns))
    return SELECT_ITEM

async def section_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    sid = query.data.split("_")[1]
    headers = context.user_data['mode_headers']
    # EduGuru base data API
    url = f"https://hsscgurukulapi.akamai.net.in/get/test_series?start=-1&exam_id={sid}"
    r = scraper.get(url, headers=headers).json()
    items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]
    context.user_data['item_names'] = {str(i[0]): i[1] for i in items}
    btns = [[InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")] for i in items[:40]]
    await query.edit_message_text("ðŸŽ¯ *Select Test Series:*", reply_markup=InlineKeyboardMarkup(btns))
    return SELECT_ITEM

async def item_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = str(query.data.split("_")[1])
    headers = context.user_data['mode_headers']
    mode = context.user_data['type']
    
    status_msg = await query.edit_message_text("ðŸ•µï¸ *Deep Scanning Content (Topic-Wise)...*")
    all_tests = []

    if mode == "agg":
        agg_api = "https://thetestpassapi.akamai.net.in"
        client_url = "https://hsscgurukulapi.akamai.net.in/"
        try:
            # Fetch Subjects
            sub_url = f"{agg_api}/get/testseries_subjects?testseries_id={item_id}&client_api_url={client_url}"
            sub_resp = scraper.get(sub_url, headers=headers).json()
            for s in sub_resp.get("data", []):
                # Fetch Tests inside Subject
                t_url = f"{agg_api}/get/test_titlev2?testseriesid={item_id}&subject_id={s['subjectid']}&userid=1558&start=-1&client_api_url={client_url}"
                t_resp = scraper.get(t_url, headers=headers).json()
                for t in t_resp.get("test_titles", []):
                    if t.get("test_questions_url"):
                        all_tests.append({'title': t['title'], 'link': t['test_questions_url'], 'folder': s['subject_name']})
        except: pass
    else:
        api_url = context.user_data['api_url']
        if mode in ["course", "hssc"]:
            await explore_recursively(api_url, item_id, -1, all_tests, headers=headers)
        else: # Normal Series
            subj = scraper.get(f"{api_url}/get/testseries_subjects?testseries_id={item_id}", headers=headers).json()
            for s in subj.get("data", []):
                t_url = f"{api_url}/get/test_titlev2?testseriesid={item_id}&subject_id={s['subjectid']}&userid={headers['User-ID']}&start=-1"
                t_resp = scraper.get(t_url, headers=headers).json()
                for t in t_resp.get("test_titles", []):
                    if t.get("test_questions_url"):
                        all_tests.append({'title': t['title'], 'link': t['test_questions_url'], 'folder': s['subject_name']})

    if not all_tests:
        await query.message.reply_text("âŒ No Tests found."); return ConversationHandler.END

    context.user_data['all_tests'] = all_tests
    kb = [[InlineKeyboardButton("ðŸ“¦ ZIP (Topic-Wise)", callback_data="up_zip"), 
           InlineKeyboardButton("ðŸ“„ HTMLs", callback_data="up_html")]]
    await status_msg.edit_text(f"âœ… Found {len(all_tests)} tests in {len(set(t['folder'] for t in all_tests))} topics!", reply_markup=InlineKeyboardMarkup(kb))
    return UPLOAD_CHOICE

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    all_tests, creator = context.user_data['all_tests'], context.user_data['creator']
    headers = context.user_data['mode_headers']
    out_dir = f"work_{query.from_user.id}"
    os.makedirs(out_dir, exist_ok=True)
    
    status_msg = await query.edit_message_text(f"âš¡ Downloading `0/{len(all_tests)}`...")
    
    extracted = []
    loop = asyncio.get_event_loop()
    for i, t in enumerate(all_tests):
        try:
            safe_f = "".join(c for c in t['folder'] if c.isalnum() or c in " _-")[:30]
            f_path = os.path.join(out_dir, safe_f)
            os.makedirs(f_path, exist_ok=True)
            
            safe_t = "".join(c for c in t['title'] if c.isalnum() or c in " _-")[:50]
            file_path = os.path.join(f_path, f"{safe_t}.html")
            
            resp = scraper.get(t['link'], headers=headers, timeout=10).json()
            if await loop.run_in_executor(None, save_html_sync, resp, t['title'], file_path, creator):
                extracted.append({'path': file_path, 'title': t['title'], 'folder': t['folder']})
            
            if i % 10 == 0: await status_msg.edit_text(f"â³ Progress: `{i}/{len(all_tests)}`...")
        except: continue

    if choice == "zip":
        zip_name = f"{creator[:20]}_organized.zip"
        with zipfile.ZipFile(zip_name, 'w') as z:
            for root, _, files in os.walk(out_dir):
                for f in files:
                    z.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), out_dir))
        await query.message.reply_document(document=open(zip_name, 'rb'), caption=f"ðŸš€ *{creator}* Topic-wise ZIP")
        os.remove(zip_name)
    else:
        for t in extracted:
            try:
                await query.message.reply_document(document=open(t['path'], 'rb'), caption=f"ðŸ“ {t['folder']}\nâœ… {t['title']}")
                await asyncio.sleep(0.5)
            except: continue

    shutil.rmtree(out_dir)
    return ConversationHandler.END

# --- BOT START ---
def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler('extract', extract_start)],
        states={
            API_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_url)],
            CREATOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_creator_name)],
            CHOOSE_TYPE: [CallbackQueryHandler(handle_choice, pattern="^type_")],
            HSSC_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hssc_course_id)],
            SELECT_SECTION: [CallbackQueryHandler(section_selected, pattern="^sec_")],
            SELECT_ITEM: [CallbackQueryHandler(item_selected, pattern="^sel_")],
            UPLOAD_CHOICE: [CallbackQueryHandler(start_upload, pattern="^up_")],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()
