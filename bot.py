import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8791201549:AAG-BW2OELQvcZ6SMqb3ONB9y4zQxRaJCPA"

# хранение очков (очень простое)
scores = {}

symbols = ["☀️", "🪶", "🌿", "⚡"]

# старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    scores[user_id] = 0

    keyboard = [
        [InlineKeyboardButton("🎮 Ловить знак", callback_data="play")]
    ]

    await update.message.reply_text(
        "🪶 Чӑваш игра!\nЛови знаки солнца и набирай очки!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# игра
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if user_id not in scores:
        scores[user_id] = 0

    if query.data == "play":
        symbol = random.choice(symbols)

        if symbol == "☀️":
            scores[user_id] += 1
            text = f"🔥 Ты поймал солнце {symbol}! +1 очко"
        else:
            text = f"❌ Это {symbol}, не солнце"

        keyboard = [
            [InlineKeyboardButton("🎮 Играть ещё", callback_data="play")],
            [InlineKeyboardButton("📊 Очки", callback_data="score")]
        ]

        await query.edit_message_text(
            text + f"\n\n🏆 Очки: {scores[user_id]}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "score":
        await query.edit_message_text(f"🏆 Твои очки: {scores[user_id]}")

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")
app.run_polling()
