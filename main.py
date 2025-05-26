from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Bot
from bot_handlers import (
    start,
    help_command,
    send_news,
    send_today_info,
    send_weather_news,
    subscribe,
    update_city_command,
    unsubscribe_command,
    check_alert,
    set_alert_prefs
)
from subscriptions import get_all_subscribers, get_user_prefs
from weather import get_weather, check_weather_alerts
from news import get_news
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def notify_subscribers(context: ContextTypes.DEFAULT_TYPE):
    users = get_all_subscribers()
    for user_id, city in users:
        try:
            weather = get_weather(city)
            news = get_news()
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
            print(f"Error notifying {user_id}: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", send_news))
    app.add_handler(CommandHandler("today", send_today_info))
    app.add_handler(CommandHandler("weather", send_weather_news))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("updatecity", update_city_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    app.add_handler(CommandHandler("alert", check_alert))
    app.add_handler(CommandHandler("setalert", set_alert_prefs))

    app.job_queue.run_repeating(notify_subscribers, interval=10, first=10)

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()