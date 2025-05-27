# 🌦️ MausamAurKhabarBot

**MausamAurKhabarBot** एक स्मार्ट Telegram बॉट है जो आपको रोज़ाना आपके चुने हुए शहर का मौसम, चेतावनियाँ और ताज़ा खबरें भेजता है — हिंदी में!

## 📲 Bot के Features:

- 🌤️ **Weather Updates** – किसी भी भारतीय शहर का वर्तमान मौसम
- 📰 **Top News** – टॉप 3 ब्रेकिंग न्यूज़ (Google, BBC, TOI Feeds से)
- 🔔 **Weather Alerts** – बारिश, तूफान, गर्मी, ठंड, बर्फबारी जैसी चेतावनियाँ
- 📅 **Fun Today** – आज की तारीख और एक मजेदार जानकारी
- ⚙️ **Custom Alerts** – आप alert preferences भी सेट कर सकते हैं
- 📍 **City Selection via Inline Buttons** – हर कमांड पर सिटी चुनने की सुविधा

## 🛠 Commands:

| Command          | Description                                |
|------------------|--------------------------------------------|
| `/start`         | Bot का स्वागत संदेश                        |
| `/weather`       | अपने शहर का मौसम                          |
| `/news`          | टॉप 3 हिंदी खबरें                          |
| `/today`         | आज की तारीख + मजेदार तथ्य                 |
| `/subscribe`     | रोज़ाना सुबह अपने शहर का अपडेट पाएं       |
| `/updatecity`    | सब्सक्रिप्शन का शहर बदलें                 |
| `/unsubscribe`   | बॉट से सब्सक्रिप्शन हटाएं                  |
| `/alert`         | अपने शहर की मौसम चेतावनी देखें           |
| `/setalert`      | चुनें कौन-कौन से alert on/off होने चाहिए |
| `/help`          | सभी कमांड्स की सूची                        |

## 🧠 टेक्नोलॉजीज़:

- Python + [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- OpenWeatherMap API
- Google News, BBC, TOI RSS Feeds
- ShrinkMe.io (URL shortener)
- Flask (for Render health check)
- JSON files for local storage (`subscribers.json`, `fun_facts.json`)

## 🧪 Local Setup

```bash
git clone https://github.com/yourusername/MausamAurKhabarBot.git
cd MausamAurKhabarBot
pip install -r requirements.txt
