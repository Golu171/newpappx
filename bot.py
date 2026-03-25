import os
import asyncio
import logging
import threading
import zipfile
import shutil
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from telegram import *
from telegram.ext import *

import cloudscraper
from jupiter import json_to_html

# ===== CONFIG ===== #

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 123456789  # 👈 apna id daal
FORCE_CHANNEL = "@MOCK_TEST18"

MAX_WORKERS = 40
DAILY_LIMIT = 5

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

scraper = cloudscraper.create_scraper()

logging.basicConfig(level=logging.INFO)

API, CREATOR, TYPE, ITEM, UPLOAD = range(5)

# ===== DATABASE (simple) ===== #

users = {}
# format: user_id: {"count":0, "paid":False}

# ===== SERVER ===== #

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "LEGEND BOT RUNNING", 200

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

# ===== UTILS ===== #

def clean(t, l=40):
    return "".join(c for c in t if c.isalnum() or c in " _-")[:l]

def save_html(data, title, path, creator):
    try:
        html = json_to_html(data, title, creator)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    except:
        return False

async def check_join(bot, uid):
    try:
        m = await bot.get_chat_member(FORCE_CHANNEL, uid)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

# ===== USER SYSTEM ===== #

def get_user(uid):
    if uid not in users:
        users[uid] = {"count": 0, "paid": False}
    return users[uid]

# ===== BOT ===== #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    get_user(uid)

    await update.message.reply_text(
        "🔥 LEGEND BOT\n\n"
        "Free limit: 5/day\n"
        "Use /extract"
    )

# ===== ADMIN ===== #

async def add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    uid = int(context.args[0])
    get_user(uid)["paid"] = True

    await update.message.reply_text("✅ User premium bana diya")

# ===== EXTRACT FLOW ===== #

async def extract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user(uid)

    # limit check
    if not user["paid"] and user["count"] >= DAILY_LIMIT:
        await update.message.reply_text("🚫 Daily limit khatam\nPremium le 😎")
        return ConversationHandler.END

    await update.message.reply_text("🔗 API bhej:")
    return API

async def get_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['api'] = update.message.text
    await update.message.reply_text("✍️ Creator:")
    return CREATOR

async def get_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['creator'] = update.message.text

    kb = [
        [InlineKeyboardButton("📚 Course", callback_data="type_course")],
        [InlineKeyboardButton("🎯 Series", callback_data="type_series")]
    ]

    await update.message.reply_text("Mode:", reply_markup=InlineKeyboardMarkup(kb))
    return TYPE

async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    # force join
    if not await check_join(context.bot, q.from_user.id):
        await q.message.reply_text("🚫 Join channel first")
        return TYPE

    context.user_data['mode'] = q.data
    await q.message.reply_text("🎯 Enter ID manually:")
    return ITEM

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = context.user_data['api']
    item_id = update.message.text

    tests = []

    r = scraper.get(f"{api}/get/folder_contentsv3?course_id={item_id}&parent_id=-1&start=0").json()

    for i in r.get("data", []):
        if i.get("material_type") == "TEST":
            if i.get("test_questions_url"):
                tests.append({
                    "title": i["title"],
                    "link": i["test_questions_url"],
                    "folder": "Main"
                })

    context.user_data['tests'] = tests

    kb = [
        [InlineKeyboardButton("ZIP", callback_data="up_zip")],
        [InlineKeyboardButton("HTML", callback_data="up_html")]
    ]

    await update.message.reply_text(f"{len(tests)} tests", reply_markup=InlineKeyboardMarkup(kb))
    return UPLOAD

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    user = get_user(uid)
    user["count"] += 1  # usage++

    tests = context.user_data['tests']
    creator = context.user_data['creator']

    out = f"work_{uid}"
    os.makedirs(out, exist_ok=True)

    msg = await q.message.reply_text("⚡ Running...")

    loop = asyncio.get_running_loop()

    async def worker(t):
        try:
            folder = clean(t['folder'])
            path = os.path.join(out, folder)
            os.makedirs(path, exist_ok=True)

            name = clean(t['title'])
            file = os.path.join(path, f"{name}.html")

            data = await loop.run_in_executor(
                executor,
                lambda: scraper.get(t['link']).json()
            )

            ok = await loop.run_in_executor(
                executor,
                lambda: save_html(data, t['title'], file, creator)
            )

            return file if ok else None
        except:
            return None

    tasks = [worker(t) for t in tests]

    files = []
    done = 0

    for coro in asyncio.as_completed(tasks):
        res = await coro
        done += 1

        if res:
            files.append(res)

        if done % 5 == 0:
            await msg.edit_text(f"{done}/{len(tests)}")

    # ZIP
    zipname = "result.zip"

    with zipfile.ZipFile(zipname, 'w') as z:
        for f in files:
            z.write(f, os.path.relpath(f, out))

    with open(zipname, "rb") as f:
        await q.message.reply_document(f)

    shutil.rmtree(out)
    os.remove(zipname)

    await msg.edit_text("✅ Done")

    return ConversationHandler.END

# ===== MAIN ===== #

def main():
    threading.Thread(target=run_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("extract", extract)],
        states={
            API: [MessageHandler(filters.TEXT, get_api)],
            CREATOR: [MessageHandler(filters.TEXT, get_creator)],
            TYPE: [CallbackQueryHandler(choose)],
            ITEM: [MessageHandler(filters.TEXT, select)],
            UPLOAD: [CallbackQueryHandler(upload)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpremium", add_premium))
    app.add_handler(conv)

    app.run_polling()

if __name__ == "__main__":
    main()
