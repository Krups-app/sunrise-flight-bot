import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_KEY = os.getenv("AVIATION_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✈️ Привіт! Я SunriseFlightBot. Напиши /flight TK3261 — і я скажу, де твій літак!")

async def flight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("🔎 Використовуй: /flight TK3261")
        return

    flight_number = context.args[0]
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_iata={flight_number}"

    response = requests.get(url)
    data = response.json()

    if not data.get("data"):
        await update.message.reply_text("❌ Рейс не знайдено.")
        return

    flight_info = data["data"][0]
    status = flight_info.get("flight_status", "невідомо")
    dep = flight_info["departure"]
    arr = flight_info["arrival"]

    message = (
        f"📡 Рейс: {flight_number.upper()}\n"
        f"✈️ Статус: *{status}*\n"
        f"🛫 {dep['airport']} ({dep['scheduled']})\n"
        f"🛬 {arr['airport']} ({arr['scheduled']})"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("flight", flight))

if __name__ == "__main__":
    app.run_polling()
