import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            username TEXT,
            code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    code = context.args[0] if context.args else ""

    conn = sqlite3.connect("users.db")
    conn.execute(
        "INSERT INTO users (telegram_id, username, code) VALUES (?, ?, ?)",
        (user.id, user.username, code)
    )
    conn.commit()
    conn.close()

    keyboard = [[
        InlineKeyboardButton("📸 Посмотреть фото", callback_data="photo")
    ]]

    await update.message.reply_text(
        "📸 Вам отправили фотографию!\n\nНажмите кнопку ниже:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📸 Здесь будет фотография."
    )

def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(photo))

    app.run_polling()

if __name__ == "__main__":
    main()