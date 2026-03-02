import os
import shutil
import zipfile
import asyncio
import logging
import gc
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)

from jupiter import json_to_html
import cloudscraper

# ---------------- FLASK SERVER (For Koyeb Port Binding) ---------------- #

server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is Fast & Alive!", 200

# ---------------- BOT SETUP ---------------- #

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "android", "desktop": False}
)

TOKEN = os.environ.get("BOT_TOKEN")  # 🔥 IMPORTANT (No hardcoded token)

HEADERS = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website",
    "User-ID": "82093",
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
        resp = scraper.get(url, headers=HEADERS, timeout=15).json()
        for item in resp.get("data", []):
            if item.get("material_type") == "TEST":
                tid = item.get("quiz_title_id")
                if tid and tid != "-1":
                    t_url = f"{api_url}/get/test_title_by_id?id={tid}&userid=82093"
                    d = scraper.get(t_url, headers=HEADERS, timeout=15).json().get("data", {})
                    if d.get("test_questions_url"):
                        tests_list.append(
                            {
                                "title": d["title"],
                                "link": d["test_questions_url"],
                                "folder": current_path,
                            }
                        )
            elif item.get("material_type") == "FOLDER":
                new_path = item.get("folder_name", "SubFolder")
                await explore_recursively(api_url, course_id, item.get("id"), tests_list, new_path)
    except:
        pass

# ---------------- BOT HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Ram's Ultimate Extractor V7\n\nUse /extract to start."
    )

async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 API URL bhej:")
    return API_URL

async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["api_url"] = (
        f"https://{update.message.text.strip()}"
        if "http" not in update.message.text
        else update.message.text.strip()
    )
    await update.message.reply_text("✍️ Creator Name?")
    return CREATOR_NAME

async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["creator"] = update.message.text.strip()

    kb = [
        [InlineKeyboardButton("📚 Course", callback_data="type_course")],
        [InlineKeyboardButton("🎯 Series", callback_data="type_series")],
    ]

    await update.message.reply_text(
        "Select Mode:", reply_markup=InlineKeyboardMarkup(kb)
    )
    return CHOOSE_TYPE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data.split("_")[1]
    context.user_data["type"] = choice
    api_url = context.user_data["api_url"]

    await query.edit_message_text("📡 Scanning...")

    try:
        if choice == "course":
            p = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
            r = scraper.post(f"{api_url}/get/search", headers=HEADERS, json=p).json()
            items = [(c["id"], c["course_name"]) for c in r.get("courses_with_folder", [])]
        else:
            r = scraper.get(f"{api_url}/get/test_series?start=-1", headers=HEADERS).json()
            items = [(ts["id"], ts["title"]) for ts in r.get("data", [])]

        context.user_data["item_names"] = {str(i[0]): i[1] for i in items}
        btns = [
            [InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")]
            for i in items[:30]
        ]

        await query.message.reply_text(
            "🎯 Select Target:", reply_markup=InlineKeyboardMarkup(btns)
        )
        return SELECT_ITEM

    except Exception as e:
        await query.message.reply_text(f"❌ Error: {e}")
        return ConversationHandler.END

# ---------------- MAIN FUNCTION ---------------- #

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("extract", extract_start)],
        states={
            API_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_url)],
            CREATOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_creator_name)],
            CHOOSE_TYPE: [CallbackQueryHandler(handle_choice)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
