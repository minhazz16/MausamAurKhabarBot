import json
import os

SUBSCRIBERS_FILE = "subscribers.json"

def ensure_file():
    if not os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump({}, f)

def migrate_old_format(subscribers):
    """Convert old string format to new dictionary format"""
    migrated = {}
    for uid, data in subscribers.items():
        if isinstance(data, str):  # Old format
            migrated[uid] = {
                'city': data,
                'prefs': {
                    'rain': True,
                    'storm': True,
                    'heat': True,
                    'cold': True,
                    'snow': True
                }
            }
        else:  # Already in new format
            migrated[uid] = data
    return migrated

def add_subscriber(user_id, city):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
            subscribers = migrate_old_format(subscribers)
    except json.JSONDecodeError:
        subscribers = {}
    
    user_id_str = str(user_id)
    subscribers[user_id_str] = {
        'city': city,
        'prefs': {
            'rain': True,
            'storm': True,
            'heat': True,
            'cold': True,
            'snow': True
        }
    }
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f, indent=2)
    return True

def update_city(user_id, new_city):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
            subscribers = migrate_old_format(subscribers)
    except json.JSONDecodeError:
        return False
    
    user_id_str = str(user_id)
    if user_id_str in subscribers:
        subscribers[user_id_str]['city'] = new_city
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(subscribers, f, indent=2)
        return True
    return False

def unsubscribe(user_id):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
            subscribers = migrate_old_format(subscribers)
    except json.JSONDecodeError:
        return False
    
    user_id_str = str(user_id)
    if user_id_str in subscribers:
        del subscribers[user_id_str]
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(subscribers, f, indent=2)
        return True
    return False

def get_all_subscribers():
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
            subscribers = migrate_old_format(subscribers)
        return [(int(uid), data['city']) for uid, data in subscribers.items()]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def is_subscribed(user_id):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
            subscribers = migrate_old_format(subscribers)
        return str(user_id) in subscribers
    except json.JSONDecodeError:
        return False
    
def get_user_prefs(user_id):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            data = json.load(f)
            data = migrate_old_format(data)
            user_key = str(user_id)
            return data.get(user_key, {}).get('prefs', {})
    except:
        return {}
def get_user_profile(user_id):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            data = json.load(f)
            data = migrate_old_format(data)
            user_key = str(user_id)
            return data.get(user_key)
    except:
        return None
    

def set_alert_preference(user_id, alert_type, status=True):
    ensure_file()
    try:
        with open(SUBSCRIBERS_FILE, 'r+') as f:
            data = json.load(f)
            data = migrate_old_format(data)
            user_key = str(user_id)
            if user_key not in data:
                return False
            if 'prefs' not in data[user_key]:
                data[user_key]['prefs'] = {}
            data[user_key]['prefs'][alert_type] = status
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            return True
    except Exception as e:
        print(f"Prefs save error: {e}")
        return False