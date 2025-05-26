# weather.py
import requests
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def check_weather_alerts(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=hi"
        res = requests.get(url).json()
        
        if res.get("cod") != 200:
            return None
            
        weather_condition = res["weather"][0]["main"].lower()
        temp = res["main"]["temp"]
        
        # अलर्ट कंडीशन्स
        alerts = []
        if "rain" in weather_condition:
            alerts.append("⚠️ भारी बारिश की चेतावनी! छाता ले जाएँ।")
        if temp > 40:
            alerts.append("🔥 अत्यधिक गर्मी! हाइड्रेटेड रहें।")
        if "storm" in weather_condition:
            alerts.append("⚡ तूफान की चेतावनी! सुरक्षित स्थान पर रहें।")
        # 'rain' चेक के बाद ये लाइनें ऐड करें (लगभग लाइन 15 के बाद)
        if "snow" in weather_condition:
            alerts.append("❄️ बर्फबारी की चेतावनी! गाड़ी सावधानी से चलाएँ।")
        if temp < 5:
            alerts.append("🥶 कड़ाके की ठंड! गर्म कपड़े पहनें।")    
            
        return "\n".join(alerts) if alerts else None
        
    except Exception as e:
        print(f"Alert check error: {e}")
        return None

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=hi"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return "⚠️ शहर का मौसम नहीं मिला, सही नाम डालें।"

        weather_desc = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        humidity = res["main"]["humidity"]

        return (
            f"☁️ {city.title()} का मौसम:\n"
            f"• हालत: {weather_desc}\n"
            f"• तापमान: {temp}°C 🔥\n"
            f"• नमी: {humidity}%\n"
            f"• महसूस हो रहा: {feels_like}°C\n"
        )
    except Exception as e:
        return f"⚠️ मौसम फ़ेच करने में त्रुटि: {str(e)}"
