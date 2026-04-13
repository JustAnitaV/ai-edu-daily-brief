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


def normalize_text(text):
    text = (text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("–", "-").replace("—", "-")
    return text


def normalize_title(text):
    text = normalize_text(text)
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


def contains_any(text, keywords):
    return any(keyword in text for keyword in keywords)


def has_ai_signal(text):
    text = normalize_text(text)
    ai_keywords = [
        "ai",
        "artificial intelligence",
        "machine learning",
        "generative ai",
        "genai",
        "llm",
        "large language model",
        "large language models",
        "chatgpt",
        "gpt",
        "openai",
        "copilot",
        "chatbot",
        "ai tutor",
        "mākslīgais intelekts",
        "mi ",
        " mi",
        "ģeneratīvais mi",
        "valodu model",
        "lielais valodu modelis",
        "lielie valodu modeļi",
    ]
    return contains_any(text, ai_keywords)


def has_education_signal(text):
    text = normalize_text(text)
    education_keywords = [
        "education",
        "school",
        "schools",
        "classroom",
        "classrooms",
        "student",
        "students",
        "teacher",
        "teachers",
        "learning",
        "teaching",
        "lesson",
        "homework",
        "assessment",
        "grading",
        "exam",
        "exams",
        "curriculum",
        "k-12",
        "primary school",
        "secondary school",
        "high school",
        "college",
        "university",
        "higher education",
        "izglīt",
        "skol",
        "skolēn",
        "skolot",
        "mācīb",
        "mācīšan",
        "stunda",
        "stundās",
        "vērtēšan",
        "eksāmen",
        "mājasdar",
        "klase",
        "klasē",
        "pedagog",
        "kurikuls",
    ]
    return contains_any(text, education_keywords)


def has_strong_k12_signal(text):
    text = normalize_text(text)
    k12_keywords = [
        "k-12",
        "school",
        "schools",
        "classroom",
        "classrooms",
        "student",
        "students",
        "teacher",
        "teachers",
        "primary school",
        "secondary school",
        "high school",
        "skola",
        "skolas",
        "skolēn",
        "skolot",
        "klase",
        "klasē",
    ]
    return contains_any(text, k12_keywords)


def is_ai_education_relevant(item):
    title = normalize_title(item.get("title", ""))
    source = normalize_text(item.get("source", ""))

    combined = f"{title} {source}"

    ai_signal = has_ai_signal(combined)
    education_signal = has_education_signal(combined)

    if not ai_signal:
        return False

    if not education_signal:
        return False

    return True


def score_item(item):
    title = normalize_title(item.get("title", ""))
    source = (item.get("source") or "").lower()

    score = 0

    # Hard relevance already enforced before scoring

    # --- Primary relevance: school-age / K-12 / classroom / students ---
    if contains_any(title, [
        "k-12", "school", "schools", "classroom", "classrooms",
        "student", "students", "pupil", "pupils", "secondary school",
        "primary school", "high school", "teacher", "teachers",
        "skola", "skolas", "skolēn", "skolot", "klase", "klasē"
    ]):
        score += 4

    # --- LLM / generative AI focus ---
    if contains_any(title, [
        "llm", "large language model", "large language models",
        "generative ai", "genai", "chatgpt", "gpt", "chatbot",
        "copilot", "ai tutor", "tutor",
        "mākslīgais intelekts", "ģeneratīvais mi", "lielie valodu modeļi"
    ]):
        score += 4

    # --- Student learning priority ---
    if contains_any(title, [
        "learning", "homework", "study", "tutoring", "literacy",
        "reading", "writing", "feedback", "personalized learning",
        "instruction", "mācīb", "mācīšan", "mājasdar", "lasīšan", "rakstīšan"
    ]):
        score += 4

    # --- Teacher workflow / assessment ---
    if contains_any(title, [
        "lesson planning", "lesson plan", "teacher workflow",
        "assessment", "grading", "feedback", "curriculum",
        "instructional", "classroom practice",
        "vērtēšan", "stunda", "skolot", "atgriezeniskā saite"
    ]):
        score += 3

    # --- Integrity / exams / evaluation ---
    if contains_any(title, [
        "academic integrity", "cheating", "exam", "exams",
        "testing", "evaluation", "plagiarism",
        "godīg", "eksāmen", "plaģi"
    ]):
        score += 3

    # --- Policy / system / guidance ---
    if contains_any(title, [
        "policy", "guidance", "guidelines", "ministry",
        "government", "regulation", "framework", "safety",
        "privacy", "governance",
        "vadlīnij", "ieteikum", "ministr", "politika", "regul", "droš"
    ]):
        score += 3

    # --- Strong K-12 bonus ---
    if has_strong_k12_signal(title):
        score += 2

    # --- Latvia / Europe signals ---
    if contains_any(title, ["latvia", "latvija"]):
        score += 3
    if contains_any(title, ["europe", "european", "eu", "eiropa", "eiropas"]):
        score += 1

    # --- Better sources / slight boost ---
    if contains_any(source, ["edutopia", "edsurge"]):
        score += 1

    # --- Penalties: noisy or low-value framing ---
    if contains_any(title, [
        "opinion", "commentary", "editorial", "podcast"
    ]):
        score -= 3

    if contains_any(title, [
        "launches", "launch", "unveils", "introduces", "announces"
    ]):
        score -= 1

    # Higher-ed only penalty if no school signal
    higher_ed_only = contains_any(title, [
        "university", "universities", "college", "higher education"
    ])
    school_signal = has_strong_k12_signal(title)
    if higher_ed_only and not school_signal:
        score -= 3

    # Generic wording penalty
    if contains_any(title, [
        "transforming education", "future of education", "ai in education"
    ]):
        score -= 2

    return score


def sort_key(item):
    pub_dt = parse_pub_date(item.get("published"))
    timestamp = pub_dt.timestamp() if pub_dt else 0
    return (item.get("score", 0), timestamp)


def filter_and_dedupe(items, history, seen, limit=5, recent_hours=RECENT_HOURS):
    candidates = []

    for item in items:
        if not is_recent(item.get("published"), hours=recent_hours):
            continue

        if not is_ai_education_relevant(item):
            continue

        url, title = make_item_keys(item)

        if url and ("url", url) in seen:
            continue
        if title and ("title", title) in seen:
            continue

        item_copy = dict(item)
        item_copy["score"] = score_item(item_copy)
        candidates.append(item_copy)

        if url:
            seen.add(("url", url))
        if title:
            seen.add(("title", title))

    candidates.sort(key=sort_key, reverse=True)
    return candidates[:limit]


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
            "score": item.get("score", 0),
            "sent_at": now_iso
        })

    history = prune_history(history)
    save_history(history)
