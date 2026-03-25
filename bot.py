import os
import shutil
import zipfile
import asyncio
import logging
import threading
import gc
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

executor = ThreadPoolExecutor(max_workers=20)

from jupiter import json_to_html
import cloudscraper

# --- RENDER PORT BINDING ---
server = Flask(__name__)
@server.route('/')
def ping(): return "Bot is Fast & Alive!", 200
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

# --- BOT SETUP ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})

TOKEN = os.environ.get("BOT_TOKEN")
HEADERS = {
    "Client-Service": "Appx", "Auth-Key": "appxapi", "source": "website", "User-ID": "82093",
}

API_URL, CREATOR_NAME, CHOOSE_TYPE, SELECT_ITEM, UPLOAD_CHOICE = range(5)

# ---------------- WORKER FUNCTIONS ---------------- #

def save_html_sync(test_data, title, out_path, creator):
    try:
        html = json_to_html(test_data, title, creator)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    except:
        return False

async def explore_recursively(api_url, course_id, parent_id, tests_list, current_path="Main"):
    url = f"{api_url}/get/folder_contentsv3?course_id={course_id}&parent_id={parent_id}&start=0"
    try:
        loop = asyncio.get_running_loop()

        response = await loop.run_in_executor(
            executor,
            lambda: scraper.get(url, headers=HEADERS, timeout=15)
        )

        resp = response.json()

        for item in resp.get("data", []):
            if item.get("material_type") == "TEST":
                tid = item.get("quiz_title_id")
                if tid and tid != "-1":
                    t_url = f"{api_url}/get/test_title_by_id?id={tid}&userid=82093"

                    d = await loop.run_in_executor(
                        executor,
                        lambda: scraper.get(t_url, headers=HEADERS, timeout=15).json().get("data", {})
                    )

                    if d.get("test_questions_url"):
                        tests_list.append({
                            'title': d['title'],
                            'link': d['test_questions_url'],
                            'folder': current_path
                        })

            elif item.get("material_type") == "FOLDER":
                new_path = f"{current_path}/{item.get('folder_name', 'SubFolder')}"
                await explore_recursively(api_url, course_id, item.get("id"), tests_list, new_path)

    except Exception as e:
        print("ERROR:", e)

# ---------------- BOT HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 *Ram's Ultimate Extractor V7*\n\nAb Topic-wise upload aur organized ZIP ke saath! /extract maaro.")

async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 API URL bhej (e.g., revolutioneducationapi.classx.co.in):")
    return API_URL

async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['api_url'] = f"https://{update.message.text.strip()}" if not "http" in update.message.text else update.message.text.strip()
    await update.message.reply_text("✍️ Creator/Coaching Name?")
    return CREATOR_NAME

async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['creator'] = update.message.text.strip()

    kb = [
        [InlineKeyboardButton("📚 Mode 1 (Course)", callback_data="type_course")],
        [InlineKeyboardButton("🎯 Mode 2 (Series)", callback_data="type_series")]
    ]

    await update.message.reply_text(
        "🤔 Select Extraction Type:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

    return CHOOSE_TYPE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data.split("_")[1]
    context.user_data['type'] = choice
    api_url = context.user_data['api_url']

    await query.edit_message_text(f"📡 Scanning {choice.upper()}... wait kar bhai.")

    try:
        if choice == "course":
            p = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
            r = scraper.post(f"{api_url}/get/search", headers=HEADERS, json=p).json()
            items = [(c["id"], c["course_name"]) for c in r.get("courses_with_folder", [])]
        else:
            r = scraper.get(f"{api_url}/get/test_series?start=-1", headers=HEADERS).json()
            items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]

        context.user_data['item_names'] = {str(i[0]): i[1] for i in items}

        btns = [
            [InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")]
            for i in items[:30]
        ]

        await query.message.reply_text(
            "🎯 Target select kar:",
            reply_markup=InlineKeyboardMarkup(btns)
        )

        return SELECT_ITEM

    except Exception as e:
        await query.message.reply_text(f"❌ Error: {e}")
        return ConversationHandler.END

async def item_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    item_id = str(query.data.split("_")[1])
    api_url, creator, mode = context.user_data['api_url'], context.user_data['creator'], context.user_data['type']
    target_name = context.user_data['item_names'].get(item_id, "Result")
    context.user_data['target_name'] = target_name
    
    status_msg = await query.edit_message_text(f"🕵️ Deep Scanning: {target_name}...")
    
    all_tests = []
    if mode == "course":
        await explore_recursively(api_url, item_id, -1, all_tests)
    else:
        subj = scraper.get(f"{api_url}/get/testseries_subjects?testseries_id={item_id}", headers=HEADERS).json()
        for s in subj.get("data", []):
            t_url = f"{api_url}/get/test_titlev2?testseriesid={item_id}&subject_id={s['subjectid']}&userid=-1&start=-1"
            t_data = scraper.get(t_url, headers=HEADERS).json().get("test_titles", [])
            for t in t_data:
                if t.get("test_questions_url"): 
                    all_tests.append({
                        'title': t['title'], 
                        'link': t['test_questions_url'], 
                        'folder': s['subject_name']
                    })

    if not all_tests:
        await query.message.reply_text("❌ No quizes found.")
        return ConversationHandler.END

    context.user_data['all_tests'] = all_tests
    kb = [
        [InlineKeyboardButton("📦 Send organized ZIP", callback_data="up_zip")],
        [InlineKeyboardButton("📄 Send Topic-wise HTMLs", callback_data="up_html")]
    ]
    await status_msg.edit_text(f"✅ Found {len(all_tests)} tests! Ab bata kaise chahiye?", reply_markup=InlineKeyboardMarkup(kb))
    return UPLOAD_CHOICE

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data.split("_")[1]
    
    all_tests = context.user_data['all_tests']
    creator = context.user_data['creator']
    target_name = context.user_data['target_name']
    
    out_dir = f"work_{query.from_user.id}"
    os.makedirs(out_dir, exist_ok=True)
    
    status_msg = await query.edit_message_text("⚡ Processing and Downloading... please wait.")
    
    extracted_data = []
    batch_size = 30
    for i in range(0, len(all_tests), batch_size):
        batch = all_tests[i : i + batch_size]
        loop = asyncio.get_running_loop()
        
        async def fetch_and_process(test_item):
            try:
                f_name = "".join(c for c in test_item['folder'] if c.isalnum() or c in " _-")[:30]
                t_folder = os.path.join(out_dir, f_name)
                os.makedirs(t_folder, exist_ok=True)
                
                safe_title = "".join(c for c in test_item['title'] if c.isalnum() or c in " _-")[:50]
                file_path = os.path.join(t_folder, f"{safe_title}.html")
                
                resp = await loop.run_in_executor(
                    executor,
                    lambda: scraper.get(test_item['link'], headers=HEADERS, timeout=15).json()
                )

                success = await loop.run_in_executor(
                    executor,
                    lambda: save_html_sync(resp, test_item['title'], file_path, creator)
                )

                if success:
                    return {'path': file_path, 'title': test_item['title'], 'folder': test_item['folder']}
            except:
                return None

        tasks = [fetch_and_process(t) for t in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        extracted_data.extend([r for r in results if r and not isinstance(r, Exception)])
        
        await status_msg.edit_text(f"⏳ Progress: {len(extracted_data)}/{len(all_tests)} downloaded...")
        gc.collect()

    if choice == "zip":
        await status_msg.edit_text("🤐 Zipping folders... almost done!")
        zip_name = f"{target_name[:30]}.zip"

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(out_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, out_dir)
                    z.write(full_path, rel_path)

        caption = f"🚀 Extraction Complete (Organized ZIP)\n\n🏛 Coaching: {creator}\n📊 Total: {len(extracted_data)}"

        with open(zip_name, 'rb') as f:
            await query.message.reply_document(document=f, caption=caption)

        os.remove(zip_name)

    else:
        await status_msg.edit_text("🚀 Starting Topic-wise Upload...")
        
        grouped = {}
        for item in extracted_data:
            grouped.setdefault(item['folder'], []).append(item)

        for folder_name, tests in grouped.items():
            await query.message.reply_text(f"📂 Topic: {folder_name}", parse_mode=None)

            for t in tests:
                caption = (
                    f"🕉 Jai Bajrang bali\n"
                    f"🏛 Coaching: {creator}\n"
                    f"📁 Folder: {t['folder']}\n"
                    f"✅ Test: {t['title']}\n\n"
                    f"📢 https://t.me/MOCK_TEST18"
                )

                try:
                    with open(t['path'], 'rb') as f:
                        await query.message.reply_document(
                            document=f,
                            caption=caption
                        )

                    await asyncio.sleep(0.2)

                except:
                    continue

    await query.message.reply_text("✅ Mission Accomplished!", parse_mode=None)
    shutil.rmtree(out_dir)
    return ConversationHandler.END

def main():
    threading.Thread(target=run_flask, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('extract', extract_start)],
        states={
            API_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_url)],
            CREATOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_creator_name)],
            CHOOSE_TYPE: [CallbackQueryHandler(handle_choice, pattern="^type_")],
            SELECT_ITEM: [CallbackQueryHandler(item_selected, pattern="^sel_")],
            UPLOAD_CHOICE: [CallbackQueryHandler(start_upload, pattern="^up_")],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    import asyncio
    asyncio.get_event_loop().run_until_complete(
        app.bot.delete_webhook(drop_pending_updates=True)
    )

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
