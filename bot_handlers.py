# 👇 नीचे पूरा सही किया गया कोड है:
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from weather import get_weather, check_weather_alerts
from news import get_news
import random
from subscriptions import add_subscriber, update_city, unsubscribe, is_subscribed, get_user_prefs, set_alert_preference, get_all_subscribers
import datetime
import json
import zoneinfo
from subscriptions import get_user_profile
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = int(os.getenv("ADMIN_ID"))


# 🎉 Fun Facts
def load_fun_facts():
    try:
        with open('fun_facts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Fun facts लोड करने में त्रुटि: {e}")
        return ["🌟 डिफ़ॉल्ट तथ्य: सीखते रहना जारी रखें!"]

def get_fun_fact():
    return random.choice(load_fun_facts())

# 🌆 सिटी चुनने का इनलाइन कीबोर्ड (सभी कमांड्स के लिए)
def get_city_keyboard(command_type):
    keyboard = [
        [InlineKeyboardButton("📍 Mehsi", callback_data=f"{command_type}_Mehsi")],
        [InlineKeyboardButton("📍 Gaya", callback_data=f"{command_type}_Gaya")],
        [InlineKeyboardButton("📍 Patna", callback_data=f"{command_type}_Patna")],
        [InlineKeyboardButton("📍 Delhi", callback_data=f"{command_type}_Delhi")],
        [InlineKeyboardButton("📍 Mumbai", callback_data=f"{command_type}_Mumbai")],
        [InlineKeyboardButton("📍 Kolkata", callback_data=f"{command_type}_Kolkata")],
        [InlineKeyboardButton("📍 Jaipur", callback_data=f"{command_type}_Jaipur")],
        [
            InlineKeyboardButton("✏️ अपनी सिटी एंटर करें", callback_data=f"custom_{command_type}"),
            #InlineKeyboardButton("🔄 सिटी बदलें", callback_data=f"edit_{command_type}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🔄 इनलाइन बटन हैंडलर (सभी कमांड्स के लिए)
async def handle_city_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # कस्टम सिटी या एडिट मोड
    if data.startswith(('custom_', 'edit_')):
        command_type = data.split('_')[1]
        await query.edit_message_text(f"✍️ कृपया {command_type} के लिए सिटी का नाम टाइप करें:")
        context.user_data["awaiting_city_for"] = command_type
        return

    command_type, city = data.split('_', 1)
    user_id = query.from_user.id

    if command_type == "weather":
        weather = get_weather(city)
        reply = f"{weather}\n\n📰 *टॉप न्यूज़:*\n{get_news()}" if "⚠️" not in weather else weather
        await query.edit_message_text(reply, parse_mode="Markdown")

    elif command_type == "subscribe":
        if is_subscribed(user_id):
            await query.edit_message_text("ℹ️ आप पहले से सब्सक्राइब हैं! शहर बदलने के लिए /updatecity का उपयोग करें।")
        else:
            add_subscriber(user_id, city)
            await query.edit_message_text(f"✅ {city} के लिए सब्सक्राइब हो गए!\nअब आपको रोज़ाना अपडेट मिलेंगे।")

    elif command_type == "updatecity":
        if not is_subscribed(user_id):
            await query.edit_message_text("❌ पहले /subscribe करें।")
        else:
            update_city(user_id, city)
            await query.edit_message_text(f"✅ आपकी सिटी अपडेट की गई: {city}")

    elif command_type == "alert":
        alerts = check_weather_alerts(city)
        alert_msg = f"🚨 {city} के लिए अलर्ट:\n{alerts}" if alerts else f"✅ {city} में कोई चेतावनी नहीं।"
        await query.edit_message_text(alert_msg)

    elif command_type == "setalert":
        await query.edit_message_text(f"⚙️ अलर्ट सेटिंग्स के लिए /setalert <प्रकार> <on/off> का उपयोग करें।")

# ✅ START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 नमस्ते! मैं हूँ *MausamAurKhabarBot*, आपका मौसम और खबरों का साथी।\n\n"
        "📍 अब आप किसी भी कमांड (/weather, /subscribe, आदि) पर सिटी चुन सकते हैं!\n\n"
        "⚡ उपयोगी कमांड्स:\n"
        "• /weather - मौसम जानकारी\n"
        "• /news - ताज़ा खबरें\n"
        "• /today - आज की तारीख और तथ्य\n"
        "• /subscribe - रोज़ाना अपडेट\n"
        "• /updatecity - शहर बदलें\n"
        "• /unsubscribe - अनसब्सक्राइब करें\n"
        "• /alert - मौसम चेतावनी\n"
        "• /setalert - अलर्ट सेटिंग\n"
        "• /help - सभी कमांड्स",
        parse_mode="Markdown"
    )

# ✅ WEATHER
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌦️ किस शहर का मौसम चाहिए?", reply_markup=get_city_keyboard("weather"))

# ✅ SUBSCRIBE
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 रोज़ाना अपडेट के लिए सिटी चुनें:", reply_markup=get_city_keyboard("subscribe"))

# ✅ ALERT
async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 किस शहर के अलर्ट चेक करें?", reply_markup=get_city_keyboard("alert"))

# ✅ UPDATE CITY
async def update_city_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 किस शहर में बदलाव करना चाहते हैं?", reply_markup=get_city_keyboard("updatecity"))

# ✅ UNSUBSCRIBE
async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
        # ✅ नया चेक: अगर यूजर पहले से अनसब्सक्राइब है
    if not is_subscribed(user_id):
        await update.message.reply_text("ℹ️ आप पहले से ही अनसब्सक्राइब हैं! सब्सक्राइब करने के लिए /subscribe का उपयोग करें।")
        return

    keyboard = [
        [InlineKeyboardButton("✅ हाँ, अनसब्सक्राइब करें", callback_data="unsubscribe_yes")],
        [InlineKeyboardButton("❌ नहीं", callback_data="unsubscribe_no")]
    ]
    await update.message.reply_text("❌ क्या आप वाकई अनसब्सक्राइब करना चाहते हैं?", reply_markup=InlineKeyboardMarkup(keyboard))

# ✅ HANDLE TEXT INPUT
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    city = update.message.text.strip()
    command_type = context.user_data.get("awaiting_city_for")

    if command_type == "weather":
        weather = get_weather(city)
        await update.message.reply_text(weather, parse_mode="Markdown")
    elif command_type == "subscribe":
        add_subscriber(user_id, city)
        await update.message.reply_text(f"✅ {city} के लिए सब्सक्राइब हो गए!")
    elif command_type == "updatecity":
        update_city(user_id, city)
        await update.message.reply_text(f"✅ आपकी सिटी अपडेट की गई: {city}")
    elif command_type == "alert":
        alerts = check_weather_alerts(city)
        await update.message.reply_text(f"🚨 अलर्ट: {alerts}" if alerts else f"✅ {city} में कोई चेतावनी नहीं।")

    context.user_data.pop("awaiting_city_for", None)

# ✅ TODAY और NEWS
async def send_today_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ist = zoneinfo.ZoneInfo("Asia/Kolkata")
    now = datetime.datetime.now(tz=ist)
    date_str = now.strftime("%d-%m-%Y %H:%M:%S")
    await update.message.reply_text(f"📅 आज की तारीख: {date_str}\n\n{get_fun_fact()}")

async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news())

# ✅ HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 सभी कमांड्स:\n\n"
        "📍 /weather - मौसम रिपोर्ट\n"
        "📰 /news - टॉप 3 खबरें\n"
        "📅 /today - तारीख + रोचक तथ्य\n"
        "📌 /subscribe - ऑटो अपडेट\n"
        "🔄 /updatecity - लोकेशन बदलें\n"
        "❌ /unsubscribe - अनसब्सक्राइब\n"
        "🚨 /alert - मौसम चेतावनी\n"
        "⚙️ /setalert - अलर्ट सेटिंग\n"
        "📖 /help - सहायता"
    )

# 🔄 UNSUBSCRIBE कन्फर्मेशन
async def handle_unsubscribe_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "unsubscribe_yes":
        unsubscribe(query.from_user.id)
        await query.edit_message_text("✅ सफलतापूर्वक अनसब्सक्राइब हो गए!")
    else:
        await query.edit_message_text("❌ अनसब्सक्राइब कैंसल किया गया।")

# ✅ SET ALERT PREFERENCES
async def set_alert_prefs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("⚙️ उपयोग:/setalert <प्रकार> <on/off>\n\nउदाहरण: /setalert rain off\n\n उपलब्ध अलर्ट:\n-rain\n-storm\n-heat\n-colds\n-snow")
        return

    alert_type = context.args[0].lower()
    status_arg = context.args[1].lower()
    
    if alert_type not in ['rain', 'storm', 'heat', 'cold', 'snow']:
        await update.message.reply_text("⚠️ अलर्ट प्रकार अमान्य है। rain, storm, heat, cold, या snow में से चुनें।")
        return

    if status_arg not in ['on', 'off']:
        await update.message.reply_text("⚠️ कृपया on या off में से चुनें।")
        return

    status = True if status_arg == "on" else False
    success = set_alert_preference(user_id, alert_type, status)

    if success:
        await update.message.reply_text(f"✅ {alert_type} अलर्ट अब {'चालू' if status else 'बंद'} है।")
    else:
        await update.message.reply_text("❌ अलर्ट सेट करने में त्रुटि। पहले /subscribe करें।")

# ✅ STATUS

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    profile = get_user_profile(user_id)

    if not profile:
        await update.message.reply_text("ℹ️ आप किसी भी अपडेट के लिए सब्सक्राइब नहीं हैं।")
        return

    city = profile.get('city', '❓ अज्ञात')
    alert_prefs = profile.get('prefs', {})

    alert_lines = []
    for alert_type, status in alert_prefs.items():
        emoji = "✅" if status else "❌"
        name_map = {
            "rain": "बारिश",
            "storm": "तूफान",
            "heat": "गर्मी",
            "cold": "ठंड",
            "snow": "बर्फबारी"
        }
        alert_lines.append(f"{emoji} {name_map.get(alert_type, alert_type)}")

    alert_text = "\n".join(alert_lines) if alert_lines else "❌ कोई अलर्ट प्रेफरेंस नहीं मिली।"

    await update.message.reply_text(
        f"👤 *आपकी प्रोफाइल:*\n\n"
        f"📍 शहर: *{city}*\n"
        f"🔔 अलर्ट प्रेफरेंस:\n{alert_text}",
        parse_mode="Markdown"
    )

# ✅ Brodcast

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ आपके पास यह कमांड चलाने की अनुमति नहीं है।")
        return

    if not context.args:
        await update.message.reply_text("⚠️ उपयोग:\n/broadcast <संदेश>")
        return

    message = "📢 " + " ".join(context.args)
    subscribers = get_all_subscribers()
    success_count = 0

    for uid, _ in subscribers:
        try:
            await context.bot.send_message(chat_id=uid, text=message)
            success_count += 1
        except Exception as e:
            print(f"❌ Cannot message user {uid}: {e}")

    await update.message.reply_text(f"✅ संदेश {success_count} यूज़र्स को भेजा गया।")


# ➕ HANDLERS
def add_handlers(application):
    application.add_handler(CallbackQueryHandler(handle_city_selection, pattern="^(weather|subscribe|updatecity|alert)_"))
    application.add_handler(CallbackQueryHandler(handle_unsubscribe_confirmation, pattern="^unsubscribe_"))
    application.add_handler(CallbackQueryHandler(handle_city_selection, pattern="^custom_|edit_"))
