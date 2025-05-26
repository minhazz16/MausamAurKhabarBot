import feedparser
import random
import requests
import urllib.parse
import os

from dotenv import load_dotenv

load_dotenv()

S_API_KEY = os.getenv("Shrink_API_KEY")

def shorten_url(long_url):
    try:
        encoded_url = urllib.parse.quote(long_url, safe='')
        api_url = f"https://shrinkme.io/api?api={S_API_KEY}&url={encoded_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json()
            if "shortenedUrl" in result:
                return result["shortenedUrl"]
            else:
                print("❌ ShrinkMe API error:", result)
        else:
            print(f"❌ HTTP Error {response.status_code}")
        return long_url  # fallback: return original URL
    except Exception as e:
        print(f"❌ Exception during shortening: {e}")
        return long_url

def get_news():
    try:
        news_sources = [
            "https://news.google.com/rss?hl=hi-IN&gl=IN&ceid=IN:hi",
            "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
            "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        ]
        feed_url = random.choice(news_sources)
        feed = feedparser.parse(feed_url)
        all_entries = feed.entries[:10]
        random.shuffle(all_entries)
        headlines = []

        for entry in all_entries[:3]:
            short_url = shorten_url(entry.link)
            headlines.append(f"📰 {entry.title}\n🔗 {short_url}")

        return "\n\n".join(headlines) if headlines else "⚠️ आज के लिए न्यूज़ नहीं मिली"
    except Exception as e:
        return f"⚠️ न्यूज़ फ़ेच करने में त्रुटि: {str(e)}"
    
