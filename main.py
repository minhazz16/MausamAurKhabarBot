from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from bot_handlers import (
    start, help_command, send_news, send_today_info,
    weather, subscribe, update_city_command, unsubscribe_command,
    alert, set_alert_prefs, handle_city_selection,
    handle_unsubscribe_confirmation, handle_text_input,
    status_command, broadcast_command, count_command, aqi_command
)
from subscriptions import get_all_subscribers, get_user_prefs
from weather import get_weather, check_weather_alerts
from news import get_news
from dotenv import load_dotenv
from flask import Flask
import threading
import os
import logging
from datetime import time
from zoneinfo import ZoneInfo

# Logging setup
logging.basicConfig(
    filename='bot_errors.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask server for Render health check
app_flask = Flask(__name__)

@app_flask.route("/healthz")
def health_check():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render se port milega
    app_flask.run(host="0.0.0.0", port=port)

# Telegram Bot notify function
async def notify_subscribers(context: ContextTypes.DEFAULT_TYPE):
    users = get_all_subscribers()
    for user_id, city in users:
        try:
            # Agar get_weather, get_news async hain toh await karo
            weather = get_weather(city)  # synchronous assume kar raha hu
            news = get_news()            # synchronous assume kar raha hu
            alerts = check_weather_alerts(city)
            user_prefs = get_user_prefs(user_id)

            message = f"{weather}\n"
            
            if alerts:
                filtered_alerts = []
                for alert in alerts.split('\n'):
                    alert_type = None
                    if 'बारिश' in alert: alert_type = 'rain'
                    elif 'तूफान' in alert: alert_type = 'storm'
                    elif 'गर्मी' in alert: alert_type = 'heat'
                    elif 'ठंड' in alert: alert_type = 'cold'
                    elif 'बर्फबारी' in alert: alert_type = 'snow'
                    
                    if not alert_type or user_prefs.get(alert_type, True):
                        filtered_alerts.append(alert)

                if filtered_alerts:
                    message += f"\n🚨 *Alert:*\n" + '\n'.join(filtered_alerts)
            
            message += f"\n📰 *टॉप न्यूज़:*\n{news}"
            
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Error notifying {user_id}: {e}")

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", send_news))
    app.add_handler(CommandHandler("today", send_today_info))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("updatecity", update_city_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(CommandHandler("setalert", set_alert_prefs))
    app.add_handler(CommandHandler(["status", "profile"], status_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("count", count_command))
    app.add_handler(CommandHandler("aqi", aqi_command))

    # कॉलबैक और मैसेज हैंडलर्स
    app.add_handler(CallbackQueryHandler(handle_city_selection, pattern="^(weather|subscribe|updatecity|alert)_"))
    app.add_handler(CallbackQueryHandler(handle_unsubscribe_confirmation, pattern="^unsubscribe_"))
    app.add_handler(CallbackQueryHandler(handle_city_selection, pattern="^custom_|edit_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    
    # Timezone aware scheduling with zoneinfo
    ist = ZoneInfo("Asia/Kolkata")
    app.job_queue.run_daily(
        notify_subscribers,
        time=time(hour=8, minute=0, second=0, tzinfo=ist)
    )

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    # Flask ko thread me chalu karo taaki Render ka health check ho sake
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Telegram bot chalu karo (main thread me)
    start_bot()
