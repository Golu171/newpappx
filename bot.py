
import os
import threading
import logging
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

# ---------------- FLASK SERVER ---------------- #

server = Flask(__name__)

@server.route("/")
def home():
    return "Bot is Live & Healthy!", 200


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)


# ---------------- BOT SETUP ---------------- #

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.environ.get("BOT_TOKEN")

API_URL, CREATOR_NAME, CHOOSE_TYPE = range(3)


# ---------------- HANDLERS ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Ram's Ultimate Extractor V7\n\nUse /extract to begin."
    )


async def extract_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Send API URL:")
    return API_URL


async def get_api_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["api_url"] = update.message.text.strip()
    await update.message.reply_text("✍️ Send Creator Name:")
    return CREATOR_NAME


async def get_creator_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["creator"] = update.message.text.strip()

    keyboard = [
        [InlineKeyboardButton("📚 Course", callback_data="type_course")],
        [InlineKeyboardButton("🎯 Series", callback_data="type_series")],
    ]

    await update.message.reply_text(
        "Select Mode:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CHOOSE_TYPE


async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data.split("_")[1]
    await query.edit_message_text(f"✅ Mode selected: {choice.upper()}")

    return ConversationHandler.END


# ---------------- MAIN ---------------- #

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("extract", extract_start)],
        states={
            API_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_url)],
            CREATOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_creator_name)],
            CHOOSE_TYPE: [CallbackQueryHandler(handle_choice)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling(drop_pending_updates=True)


# ---------------- START ---------------- #

if __name__ == "__main__":
    # Flask background me
    threading.Thread(target=run_flask, daemon=True).start()

    # Telegram bot main thread me
    main()
