import json
import os


HISTORY_FILE = "data/sent_history.json"

from datetime import datetime, timedelta
import email.utils


def is_recent(pub_date_str, hours=48):
    if not pub_date_str:
        return True  # keep if unknown

    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        return datetime.utcnow() - dt.replace(tzinfo=None) < timedelta(hours=hours)
    except:
        return True


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def normalize(text):
    return text.lower().strip()


def is_duplicate(item, history):
    for h in history:
        if item["url"] == h["url"]:
            return True
        if normalize(item["title"]) == normalize(h["title"]):
            return True
    return False


def filter_and_dedupe(items):
    history = load_history()

    new_items = []
    for item in items:
        if not is_recent(item.get("published")):
            continue

        if not is_duplicate(item, history):
            new_items.append(item)

    return new_items[:5], history


def update_history(selected_items, history):
    history.extend(selected_items)
    save_history(history)
