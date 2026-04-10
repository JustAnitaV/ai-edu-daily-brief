import json
import os
import re
from datetime import datetime, timedelta, timezone
import email.utils


HISTORY_FILE = "data/sent_history.json"
RECENT_HOURS = 48
HISTORY_RETENTION_DAYS = 30


def parse_pub_date(pub_date_str):
    if not pub_date_str:
        return None
    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        if dt is None:
            return None
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except Exception:
        return None


def is_recent(pub_date_str, hours=RECENT_HOURS):
    dt = parse_pub_date(pub_date_str)
    if dt is None:
        return False
    return datetime.utcnow() - dt < timedelta(hours=hours)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def normalize_title(text):
    text = (text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r'\s*-\s*(edsurge|edutopia|google news|news)\s*$', "", text)
    return text


def make_item_keys(item):
    url = (item.get("url") or "").strip()
    title = normalize_title(item.get("title", ""))
    return url, title


def build_seen_set(history):
    seen = set()
    for item in history:
        url, title = make_item_keys(item)
        if url:
            seen.add(("url", url))
        if title:
            seen.add(("title", title))
    return seen


def filter_and_dedupe(items, history, seen, limit=5, recent_hours=RECENT_HOURS):
    new_items = []

    for item in items:
        if not is_recent(item.get("published"), hours=recent_hours):
            continue

        url, title = make_item_keys(item)

        if url and ("url", url) in seen:
            continue
        if title and ("title", title) in seen:
            continue

        new_items.append(item)

        if url:
            seen.add(("url", url))
        if title:
            seen.add(("title", title))

        if len(new_items) >= limit:
            break

    return new_items


def prune_history(history, retention_days=HISTORY_RETENTION_DAYS):
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    pruned = []

    for item in history:
        sent_at = item.get("sent_at")
        if not sent_at:
            continue

        try:
            sent_dt = datetime.fromisoformat(sent_at)
            if sent_dt >= cutoff:
                pruned.append(item)
        except Exception:
            continue

    return pruned


def update_history(selected_items, history):
    now_iso = datetime.utcnow().isoformat()

    for item in selected_items:
        history.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "published": item.get("published", ""),
            "source": item.get("source", ""),
            "sent_at": now_iso
        })

    history = prune_history(history)
    save_history(history)
