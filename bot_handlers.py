from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from weather import get_weather, check_weather_alerts
from news import get_news
import random
from subscriptions import add_subscriber, update_city, unsubscribe, is_subscribed, get_user_prefs, set_alert_preference
import datetime
import json

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

# ✅ START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙏 नमस्ते! मैं हूँ *MausamAurKhabarBot*, आपका मौसम और खबरों का साथी।\n\n"
        "📍 अपने शहर का मौसम जानिए\n"
        "📰 देश-दुनिया की टॉप न्यूज़ पढ़िए\n"
        "🎉 रोज़ाना मजेदार तथ्य पाइए!\n\n"
        "⚡ उपयोगी कमांड्स:\n"
        "• /weather [शहर] - मौसम जानकारी\n"
        "• /news - ताज़ा खबरें\n"
        "• /today - आज की तारीख और तथ्य\n"
        "• /subscribe [शहर] - रोज़ाना अपडेट\n"
        "• /updatecity [नया शहर] - शहर बदलें\n"
        "• /unsubscribe - अनसब्सक्राइब करें\n"
        "• /alert [शहर] - मौसम चेतावनी\n"
        "• /setalert [प्रकार] [on/off] - अलर्ट सेटिंग\n"
        "• /selectcity - शहर चुनें बटन से\n"
        "• /help - सभी कमांड्स\n\n"
        "🚀 नए फीचर्स आने वाले हैं!",
        parse_mode="Markdown"
    )

# ✅ WEATHER + NEWS
async def send_weather_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("कृपया शहर का नाम लिखें।\nउदाहरण: /weather Mehsi")
        return
    city = " ".join(context.args)
    weather = get_weather(city)
    if "⚠️" in weather:
        await update.message.reply_text(weather)
    else:
        reply = (
            f"{weather}\n\n"
            f"{get_fun_fact()}\n\n"
            f"📰 *टॉप न्यूज़:*\n{get_news()}"
        )
        await update.message.reply_text(reply, parse_mode="Markdown")

# ✅ NEWS
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = get_news()
    await update.message.reply_text(news)

# ✅ TODAY
async def send_today_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now()
    date_str = now.strftime("%d-%m-%Y %H:%M:%S")
    await update.message.reply_text(
        f"📅 आज की तारीख: {date_str}\n\n{get_fun_fact()}"
    )

# ✅ HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 सभी कमांड्स:\n\n"
        "📍 /weather [शहर] - मौसम रिपोर्ट\n"
        "📰 /news - टॉप 3 खबरें\n"
        "📅 /today - तारीख + रोचक तथ्य\n"
        "📌 /subscribe [शहर] - ऑटो अपडेट\n"
        "🔄 /updatecity [नया शहर] - लोकेशन बदलें\n"
        "❌ /unsubscribe - अनसब्सक्राइब\n"
        "🚨 /alert [शहर] - मौसम चेतावनी\n"
        "⚙️ /setalert [प्रकार] [on/off] - अलर्ट सेटिंग\n"
        "📍 /selectcity - शहर चयन बटन\n"
        "📖 /help - सहायता"
    )

# ✅ SUBSCRIBE
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("कृपया शहर का नाम बताएं।\nउदाहरण: /subscribe Patna")
        return
    city = " ".join(context.args)
    if is_subscribed(user_id):
        await update.message.reply_text("ℹ️ आप पहले से सब्सक्राइब हैं!\nशहर बदलने के लिए /updatecity का उपयोग करें।")
        return
    if add_subscriber(user_id, city):
        await update.message.reply_text(
            f"✅ {city} के लिए सब्सक्राइब हो गए!\nअब आपको रोज़ाना:\n• मौसम\n• खबरें\n• रोचक तथ्य"
        )
    else:
        await update.message.reply_text("⚠️ त्रुटि: सब्सक्रिप्शन असफल")

# ✅ UPDATE CITY
async def update_city_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("कृपया नया शहर बताएं।\nउदाहरण: /updatecity Gaya")
        return
    new_city = " ".join(context.args)
    if not is_subscribed(user_id):
        await update.message.reply_text("❌ आप सब्सक्राइब नहीं हैं!\nपहले /subscribe करें।")
        return
    if update_city(user_id, new_city):
        await update.message.reply_text(f"✅ अब आपको {new_city} का मौसम मिलेगा।")
    else:
        await update.message.reply_text("⚠️ त्रुटि: अपडेट असफल")

# ✅ UNSUBSCRIBE
async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_subscribed(user_id):
        await update.message.reply_text("ℹ️ आप पहले से अनसब्सक्राइब हैं।")
        return
    if unsubscribe(user_id):
        await update.message.reply_text("✅ सफलतापूर्वक अनसब्सक्राइब हो गए!")
    else:
        await update.message.reply_text("⚠️ त्रुटि: अनसब्सक्राइब असफल")

# ✅ ALERT CHECK
async def check_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("कृपया शहर का नाम लिखें। उदाहरण: /alert Muzaffarpur")
        return
    city = " ".join(context.args)
    alerts = check_weather_alerts(city)
    if alerts:
        await update.message.reply_text(f"🚨 {city} के लिए अलर्ट:\n{alerts}")
    else:
        await update.message.reply_text(f"✅ {city} में कोई विशेष चेतावनी नहीं है।")

# ✅ SET ALERT PREFERENCE
async def set_alert_prefs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_subscribed(user_id):
        await update.message.reply_text("❌ पहले /subscribe करें")
        return
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ उपयोग: /setalert <alert_type> <on/off>\n"
            "उदाहरण: /setalert rain on\n\n"
            "उपलब्ध अलर्ट:\n- rain\n- storm\n- heat\n- cold\n- snow"
        )
        return
    alert_type = context.args[0].lower()
    status = context.args[1].lower() == 'on'
    valid_alerts = ['rain', 'storm', 'heat', 'cold', 'snow']
    if alert_type not in valid_alerts:
        await update.message.reply_text("❌ अमान्य अलर्ट टाइप।")
        return
    if set_alert_preference(user_id, alert_type, status):
        status_hi = "चालू" if status else "बंद"
        await update.message.reply_text(f"✅ {alert_type} अलर्ट {status_hi} किया गया")
    else:
        await update.message.reply_text("⚠️ सेटिंग सेव नहीं हुई")

# ✅ NEW: SELECT CITY (INLINE BUTTON)
async def select_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌆 Patna", callback_data='city_Patna')],
        [InlineKeyboardButton("🏙️ Muzaffarpur", callback_data='city_Muzaffarpur')],
        [InlineKeyboardButton("🏞️ Gaya", callback_data='city_Gaya')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("कृपया अपना शहर चुनें:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith('city_'):
        city = data.split('_')[1]
        await query.edit_message_text(
            text=f"✅ आपने चुना: *{city}*\nअब आप `/weather {city}` से मौसम जान सकते हैं।",
            parse_mode="Markdown"
        )
