import feedparser
import requests
from urllib.parse import quote_plus


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIEduDailyBrief/1.0)"
}


def fetch_feed(url: str, source_name: str) -> list[dict]:
    print(f"Fetching: {source_name} -> {url}")

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    feed = feedparser.parse(response.content)

    items = []
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "").strip()

        if title and link:
            items.append({
                "title": title,
                "url": link,
                "published": published,
                "source": source_name
            })

    print(f"Fetched {len(items)} items from {source_name}")
    return items


def google_news_rss(query: str, lang: str = "en", country: str = "US") -> str:
    q = quote_plus(query)
    return (
        f"https://news.google.com/rss/search?"
        f"q={q}&hl={lang}&gl={country}&ceid={country}:{lang}"
    )


def fetch_news() -> dict:
    # ===== WORLD (K-12 + LLM focus) =====
    world_queries = [
        "generative AI K-12 education",
        "LLM classroom school students AI learning",
        "AI homework school students generative AI",
        "AI tutoring school students chatbot learning",
        "AI literacy schools generative AI",
        "AI assessment school generative AI grading",
        "AI cheating school policy generative AI",
        "AI teachers lesson planning generative AI classroom"
    ]

    world_sources = [
        (f"Google World: {q}", google_news_rss(q, "en", "US"))
        for q in world_queries
    ]

    # ===== EUROPE =====
    europe_queries = [
        "generative AI schools Europe policy",
        "AI education Europe schools guidelines AI",
        "LLM classroom Europe school education",
        "AI teaching Europe schools generative AI",
        "AI assessment schools Europe policy",
    ]

    europe_sources = [
        (f"Google Europe: {q}", google_news_rss(q, "en", "GB"))
        for q in europe_queries
    ]

    # ===== LATVIA =====
    latvia_queries = [
        "mākslīgais intelekts skolās Latvijā",
        "MI izglītībā Latvijā skolas",
        "ģeneratīvais MI skolēniem Latvijā",
        "izglītības tehnoloģijas Latvijā MI",
        "mākslīgais intelekts mācībās Latvija",
        "MI vadlīnijas izglītībā Latvijā",
    ]

    latvia_sources = [
        (f"Google Latvia: {q}", google_news_rss(q, "lv", "LV"))
        for q in latvia_queries
    ]

    world = []
    for source_name, url in world_sources:
        try:
            world.extend(fetch_feed(url, source_name))
        except Exception as e:
            print(f"Warning: failed world source {source_name}: {e}")

    europe = []
    for source_name, url in europe_sources:
        try:
            europe.extend(fetch_feed(url, source_name))
        except Exception as e:
            print(f"Warning: failed Europe source {source_name}: {e}")

    latvia = []
    for source_name, url in latvia_sources:
        try:
            latvia.extend(fetch_feed(url, source_name))
        except Exception as e:
            print(f"Warning: failed Latvia source {source_name}: {e}")

    print(f"Total world items: {len(world)}")
    print(f"Total Europe items: {len(europe)}")
    print(f"Total Latvia items: {len(latvia)}")

    return {
        "world": world,
        "europe": europe,
        "latvia": latvia
    }
