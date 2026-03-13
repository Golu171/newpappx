# -*- coding: utf-8 -*-
import os, shutil, zipfile, asyncio, logging, threading, gc
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

import cloudscraper
from jupiter import json_to_html

# --- SERVER ---
server = Flask(__name__)
@server.route('/')
def ping(): return "Bot is Alive!", 200
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

# --- CONFIG & HEADERS ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})

TOKEN = os.environ.get("BOT_TOKEN")

# Original Headers for Normal Appx
HEADERS = {"Client-Service": "Appx", "Auth-Key": "appxapi", "source": "website", "User-ID": "82093"}

# Akamai Specialized Headers
HSSC_HEADERS = {
    "Client-Service": "Appx", "Auth-Key": "appxapi", "source": "website", "User-ID": "22997",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIyOTk3IiwiZW1haWwiOiJzYW5kaXNpcjc0MUBnbWFpbC5jb20iLCJuYW1lIjoiU2FuZGVlcCBTaGVvcmFuIiwidGltZXN0YW1wIjoxNzczMzM1OTQwLCJ0ZW5hbnRUeXBlIjoidXNlciIsInRlbmFudE5hbWUiOiJoc3NjZ3VpZGVfZGIiLCJ0ZW5hbnRJZCI6IiIsImRpc3Bvc2FibGUiOmZhbHNlfQ.uhzOeNxEcBbV0EcFNFRWaLaS-EzrPgHovjv3mQhbdv8",
    "X-Requested-With": "mark.via.gp", "Origin": "https://hsscguide.akamai.net.in", "Referer": "https://hsscguide.akamai.net.in/"
}

AGG_HEADERS = {
    "Client-Service": "Appx", "Auth-Key": "appxapi", "source": "website", "User-ID": "1558",
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE1NTgiLCJlbWFpbCI6InNhbmRpc2lyNzQxQGdtYWlsLmNvbSIsIm5hbWUiOiJTYW5kZWVwIFNoZW9yYW4iLCJ0aW1lc3RhbXAiOjE3NzMzMzY0NjIsInRlbmFudFR5cGUiOiJ1c2VyIiwidGVuYW50TmFtZSI6Imhzc2NndXJ1a3VsX2RiIiwidGVuYW50SWQiOiIiLCJkaXNwb3NhYmxlIjpmYWxzZX0.DzdLa897zaE_MrZR_tokxpvVMNzDdV7skI_jLDoHhxQ",
    "X-Requested-With": "mark.via.gp", "Origin": "https://eduguru.akamai.net.in", "Referer": "https://eduguru.akamai.net.in/"
}

API_URL, CREATOR_NAME, CHOOSE_TYPE, SELECT_SECTION, SELECT_ITEM, UPLOAD_CHOICE = range(6)

# ---------------- WORKER FUNCTIONS (ORIGINAL V7) ---------------- #

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
        tasks = []
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
                tasks.append(explore_recursively(api_url, course_id, item.get("id"), tests_list, new_path, headers))
        if tasks: await asyncio.gather(*tasks)
    except: pass

# ---------------- BOT HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✨ *Jai Shree Ram*\n\nBot V17 Ready. Use /extract.")

async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 *API URL Bhejo bhai:*")
    return API_URL

async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_input = update.message.text.strip().lower()
    api_url = f"https://{url_input}" if "http" not in url_input else url_input
    context.user_data['api_url'] = api_url
    context.user_data['is_akamai'] = "akamai" in api_url
    await update.message.reply_text("✍️ Creator Name?")
    return CREATOR_NAME

async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['creator'] = update.message.text.strip()
    if context.user_data.get('is_akamai'):
        kb = [[InlineKeyboardButton("🚀 HSSC Special (Auto)", callback_data="type_hssc")],
              [InlineKeyboardButton("🎓 EduGuru Courses", callback_data="type_educourse")],
              [InlineKeyboardButton("📂 EduGuru Aggregator", callback_data="type_agg")]]
    else:
        kb = [[InlineKeyboardButton("📚 Mode 1 (Course)", callback_data="type_course")],
              [InlineKeyboardButton("🎯 Mode 2 (Series)", callback_data="type_series")]]
    await update.message.reply_text("🤔 *Select Mode:*", reply_markup=InlineKeyboardMarkup(kb))
    return CHOOSE_TYPE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    context.user_data['type'] = choice
    api_url = context.user_data['api_url']
    
    # Header Selection
    if choice == "hssc": headers = HSSC_HEADERS
    elif choice in ["agg", "educourse"]: headers = AGG_HEADERS
    else: headers = HEADERS
    context.user_data['mode_headers'] = headers

    await query.edit_message_text(f"📡 Scanning {choice.upper()}... wait bhai.")

    try:
        # --- ORIGINAL V7 LOGIC FOR NORMAL APPX ---
        if choice == "course":
            p = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
            r = scraper.post(f"{api_url}/get/search", headers=headers, json=p).json()
            items = [(c["id"], c["course_name"]) for c in r.get("courses_with_folder", [])]
        
        elif choice == "type_series" or choice == "series":
            r = scraper.get(f"{api_url}/get/test_series?start=-1", headers=headers).json()
            items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]

        # --- AKAMAI MODES ---
        elif choice == "agg":
            agg_api, client_api = "https://thetestpassapi.akamai.net.in", "https://hsscgurukulapi.akamai.net.in/"
            r = scraper.get(f"{agg_api}/get/get_testseries_exams?start=0&search&client_api_url={client_api}").json()
            sections = [(item.get("exam_id") or item.get("id"), item.get("exam_name")) for item in r.get("data", [])]
            btns = [[InlineKeyboardButton(s[1], callback_data=f"sec_{s[0]}")] for s in sections]
            await query.message.reply_text("📚 *Select Section:*", reply_markup=InlineKeyboardMarkup(btns))
            return SELECT_SECTION

        elif choice == "educourse":
            r = scraper.post("https://hsscgurukulapi.akamai.net.in/get/search", headers=headers, json={"search_term": "", "user_id": "1558"}).json()
            items = [(c["id"], c["course_name"]) for c in r.get("courses_with_folder", [])]

        elif choice == "hssc":
            r = scraper.get(f"{api_url}/get/test_series?start=-1", headers=headers).json()
            items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]

        # Button Generator
        context.user_data['item_names'] = {str(i[0]): i[1] for i in items}
        btns = [[InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")] for i in items[:40]]
        await query.message.reply_text("🎯 *Target Select Kar:*", reply_markup=InlineKeyboardMarkup(btns))
        return SELECT_ITEM

    except Exception as e:
        await query.message.reply_text(f"❌ Error: {e}"); return ConversationHandler.END

async def section_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    sid = query.data.split("_")[1]
    headers = context.user_data['mode_headers']
    agg_api, client_api = "https://thetestpassapi.akamai.net.in", "https://hsscgurukulapi.akamai.net.in/"
    r = scraper.get(f"{agg_api}/get/test_series?start=-1&exam_id={sid}&client_api_url={client_api}").json()
    items = [(ts.get("id"), ts.get("title")) for ts in (r.get("data") or [])]
    context.user_data['item_names'] = {str(i[0]): i[1] for i in items}
    btns = [[InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")] for i in items[:40]]
    await query.edit_message_text("🎯 *Select Test Series:*", reply_markup=InlineKeyboardMarkup(btns))
    return SELECT_ITEM

async def item_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = str(query.data.split("_")[1])
    headers, mode = context.user_data['mode_headers'], context.user_data['type']
    api_url = context.user_data['api_url']
    status_msg = await query.edit_message_text("🕵️ *Deep Scanning...*")
    all_tests = []
    
    try:
        if mode == "agg":
            agg_api, client_url = "https://thetestpassapi.akamai.net.in", "https://hsscgurukulapi.akamai.net.in/"
            sub_resp = scraper.get(f"{agg_api}/get/testseries_subjects?testseries_id={item_id}&client_api_url={client_url}", headers=headers).json()
            for s in sub_resp.get("data", []):
                t_resp = scraper.get(f"{agg_api}/get/test_titlev2?testseriesid={item_id}&subject_id={s['subjectid']}&userid=1558&start=-1&client_api_url={client_url}", headers=headers).json()
                for t in t_resp.get("test_titles", []):
                    if t.get("test_questions_url"): all_tests.append({'title': t['title'], 'link': t['test_questions_url'], 'folder': s['subject_name']})
        
        elif mode == "course" or mode == "educourse":
            target_api = "https://hsscgurukulapi.akamai.net.in" if mode == "educourse" else api_url
            await explore_recursively(target_api, item_id, -1, all_tests, headers=headers)
        
        else: # Normal Series & HSSC guide series fallback
            subj = scraper.get(f"{api_url}/get/testseries_subjects?testseries_id={item_id}", headers=headers).json()
            for s in subj.get("data", []):
                t_resp = scraper.get(f"{api_url}/get/test_titlev2?testseriesid={item_id}&subject_id={s['subjectid']}&userid={headers['User-ID']}&start=-1", headers=headers).json()
                for t in t_resp.get("test_titles", []):
                    if t.get("test_questions_url"): all_tests.append({'title': t['title'], 'link': t['test_questions_url'], 'folder': s['subject_name']})

    except Exception as e:
        await query.message.reply_text(f"❌ Scan Error: {e}"); return ConversationHandler.END

    if not all_tests:
        await query.message.reply_text("❌ No tests found!"); return ConversationHandler.END
    context.user_data['all_tests'] = all_tests
    kb = [[InlineKeyboardButton("📦 ZIP", callback_data="up_zip"), InlineKeyboardButton("📄 HTML", callback_data="up_html")]]
    await status_msg.edit_text(f"✅ Found {len(all_tests)} tests!\nChoose Upload:", reply_markup=InlineKeyboardMarkup(kb))
    return UPLOAD_CHOICE

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    all_tests, creator, headers = context.user_data['all_tests'], context.user_data['creator'], context.user_data['mode_headers']
    out_dir = f"work_{query.from_user.id}"
    os.makedirs(out_dir, exist_ok=True)
    status_msg = await query.edit_message_text(f"⚡ Downloading `0/{len(all_tests)}`...")
    extracted, loop = [], asyncio.get_event_loop()
    for i, t in enumerate(all_tests):
        try:
            f_path = os.path.join(out_dir, "".join(c for c in t['folder'] if c.isalnum() or c in " _-")[:30])
            os.makedirs(f_path, exist_ok=True)
            file_path = os.path.join(f_path, f"{''.join(c for c in t['title'] if c.isalnum() or c in ' _-')[:50]}.html")
            resp = scraper.get(t['link'], headers=headers).json()
            if await loop.run_in_executor(None, save_html_sync, resp, t['title'], file_path, creator): extracted.append(t)
            if i % 10 == 0: await status_msg.edit_text(f"⏳ Progress: `{i}/{len(all_tests)}`...")
        except: continue
    if choice == "zip":
        zip_name = f"{creator[:20]}.zip"
        with zipfile.ZipFile(zip_name, 'w') as z:
            for root, _, files in os.walk(out_dir):
                for f in files: z.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), out_dir))
        await query.message.reply_document(document=open(zip_name, 'rb'), caption=f"🚀 Extraction Done!"); os.remove(zip_name)
    else:
        for t in extracted:
            try:
                safe_f = "".join(c for c in t['folder'] if c.isalnum() or c in " _-")[:30]
                safe_t = "".join(c for c in t['title'] if c.isalnum() or c in ' _-')[:50]
                path = os.path.join(out_dir, safe_f, f"{safe_t}.html")
                await query.message.reply_document(document=open(path, 'rb'), caption=f"📁 {t['folder']}\n✅ {t['title']}")
                await asyncio.sleep(0.5)
            except: continue
    shutil.rmtree(out_dir); return ConversationHandler.END

def main():
    threading.Thread(target=lambda: Flask(__name__).run(host='0.0.0.0', port=8080), daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler('extract', extract_start)],
        states={
            API_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_url)],
            CREATOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_creator_name)],
            CHOOSE_TYPE: [CallbackQueryHandler(handle_choice, pattern="^type_")],
            SELECT_SECTION: [CallbackQueryHandler(section_selected, pattern="^sec_")],
            SELECT_ITEM: [CallbackQueryHandler(item_selected, pattern="^sel_")],
            UPLOAD_CHOICE: [CallbackQueryHandler(start_upload, pattern="^up_")],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )
    app.add_handler(CommandHandler("start", start)); app.add_handler(conv); app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()