# -*- coding: utf-8 -*-
import os, shutil, zipfile, asyncio, logging, threading, gc
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

import cloudscraper
from jupiter import json_to_html

# --- RENDER/VPS PORT BINDING ---
server = Flask(__name__)

@server.route('/')
def ping():
    return "Bot is Fast & Alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host='0.0.0.0', port=port)

# --- LOGGING & SCRAPER ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)

TOKEN = os.environ.get("BOT_TOKEN")

# --- GLOBAL HEADERS CONFIG ---
HEADERS = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website",
    "User-ID": "82093"
}

HSSC_HEADERS = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website",
    "User-ID": "22997",
    "authorization": "YOUR_TOKEN",
    "X-Requested-With": "mark.via.gp",
    "Origin": "https://hsscguide.akamai.net.in",
    "Referer": "https://hsscguide.akamai.net.in/"
}

AGG_HEADERS = {
    "Client-Service": "Appx",
    "Auth-Key": "appxapi",
    "source": "website",
    "User-ID": "1558",
    "authorization": "YOUR_TOKEN",
    "X-Requested-With": "mark.via.gp",
    "Origin": "https://eduguru.akamai.net.in",
    "Referer": "https://eduguru.akamai.net.in/"
}

API_URL, CREATOR_NAME, CHOOSE_TYPE, SELECT_SECTION, SELECT_ITEM, UPLOAD_CHOICE = range(6)

# ---------------- WORKER HELPERS ---------------- #

def save_html_sync(test_data, title, out_path, creator):
    try:
        html = json_to_html(test_data, title, creator)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        return True

    except:
        return False


async def explore_recursively(
    api_url,
    course_id,
    parent_id,
    tests_list,
    current_path="Main",
    headers=HEADERS
):

    url = f"{api_url}/get/folder_contentsv3?course_id={course_id}&parent_id={parent_id}&start=0"

    try:
        resp = scraper.get(
            url,
            headers=headers,
            timeout=15
        ).json()

        print(f"Scanning Folder: {current_path}")

        for item in resp.get("data", []):

            if item.get("material_type") == "TEST":

                tid = item.get("quiz_title_id")

                if tid and str(tid) != "-1":

                    try:
                        t_url = f"{api_url}/get/test_title_by_id?id={tid}&userid={headers['User-ID']}"

                        d = scraper.get(
                            t_url,
                            headers=headers,
                            timeout=15
                        ).json().get("data", {})

                        if d.get("test_questions_url"):

                            print(f"Found Test: {d['title']}")

                            tests_list.append({
                                'title': d['title'],
                                'link': d['test_questions_url'],
                                'folder': current_path
                            })

                    except:
                        pass

            elif item.get("material_type") == "FOLDER":

                new_path = f"{current_path}/{item.get('folder_name', 'SubFolder')}"

                await explore_recursively(
                    api_url,
                    course_id,
                    item.get("id"),
                    tests_list,
                    new_path,
                    headers
                )

    except Exception as e:
        print("Recursive Error:", e)


# ---------------- BOT HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ *Jai Shree Ram*\n\n"
        "Ram's Extractor V10 Active.\n"
        "/extract - Start Extraction"
    )


async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 *API URL Bhejo bhai:*")
    return API_URL


async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text.strip()

    api_url = f"https://{url}" if "http" not in url else url

    context.user_data['api_url'] = api_url

    if "akamai" in api_url:

        context.user_data['is_akamai'] = True

        context.user_data['mode_headers'] = (
            AGG_HEADERS
            if (
                "eduguru" in api_url
                or "hsscgurukul" in api_url
                or "thetestpassapi" in api_url
            )
            else HSSC_HEADERS
        )

        await update.message.reply_text(
            "🛡️ *Akamai Detected!*\n✍️ Creator Name?"
        )

    else:

        context.user_data['is_akamai'] = False
        context.user_data['mode_headers'] = HEADERS

        await update.message.reply_text("✍️ Creator Name?")

    return CREATOR_NAME


async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data['creator'] = update.message.text.strip()

    if context.user_data.get('is_akamai'):

        kb = [
            [InlineKeyboardButton("🚀 HSSC Auto-List", callback_data="type_hssc")],
            [InlineKeyboardButton("🎓 EduGuru Courses", callback_data="type_educourse")],
            [InlineKeyboardButton("📂 EduGuru Aggregator", callback_data="type_agg")]
        ]

    else:

        kb = [
            [InlineKeyboardButton("📚 Mode 1 (Course)", callback_data="type_course")],
            [InlineKeyboardButton("🎯 Mode 2 (Series)", callback_data="type_series")]
        ]

    await update.message.reply_text(
        "🤔 *Select Extraction Mode:*",
        reply_markup=InlineKeyboardMarkup(kb)
    )

    return CHOOSE_TYPE


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    choice = query.data.split("_")[1]

    context.user_data['type'] = choice

    headers = context.user_data['mode_headers']
    api_url = context.user_data['api_url']

    # ---------------- EDUGURU ---------------- #

    if choice == "educourse":

        await query.edit_message_text(
            "📡 *Fetching EduGuru Courses... Wait bhai*"
        )

        try:

            base_api = "https://hsscgurukulapi.akamai.net.in"

            p = {
                "search_term": "",
                "user_id": "1558",
                "screen_name": "All Courses"
            }

            r = scraper.post(
                f"{base_api}/get/search",
                headers=headers,
                json=p,
                timeout=20
            ).json()

            items = []

            for c in r.get("courses_with_folder", []):

                cid = c.get("id")
                cname = c.get("course_name")

                if cid and cname:
                    items.append((cid, cname))

            context.user_data['item_names'] = {
                str(i[0]): i[1] for i in items
            }

            btns = [
                [
                    InlineKeyboardButton(
                        i[1][:40],
                        callback_data=f"sel_{i[0]}"
                    )
                ]
                for i in items[:100]
            ]

            await query.message.reply_text(
                f"🎯 *Select EduGuru Course:*\n\n✅ Total Found: {len(items)}",
                reply_markup=InlineKeyboardMarkup(btns)
            )

            return SELECT_ITEM

        except Exception as e:

            await query.message.reply_text(
                f"💥 Course API Error: {str(e)}"
            )

            return ConversationHandler.END

    # ---------------- HSSC ---------------- #

    elif choice == "hssc":

        await query.edit_message_text(
            "📡 *Fetching HSSC Guide Series... Auto-Fetch*"
        )

        try:

            r = scraper.get(
                f"{api_url}/get/test_series?start=-1",
                headers=headers,
                timeout=20
            ).json()

            items = [
                (ts["id"], ts["title"])
                for ts in r.get("data", [])
            ]

            context.user_data['item_names'] = {
                str(i[0]): i[1] for i in items
            }

            btns = [
                [InlineKeyboardButton(i[1][:40], callback_data=f"sel_{i[0]}")]
                for i in items[:40]
            ]

            await query.message.reply_text(
                "🎯 *Select HSSC Series:*",
                reply_markup=InlineKeyboardMarkup(btns)
            )

            return SELECT_ITEM

        except Exception as e:

            await query.message.reply_text(
                f"💥 HSSC API Error: {str(e)}"
            )

            return ConversationHandler.END

    await query.message.reply_text("बाकी code same rahega...")
