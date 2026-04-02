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

    if feed.bozo:
        print(f"Warning: feed parsing issue for {source_name}: {feed.bozo_exception}")

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
    world_sources = [
        ("Google News: AI in education", google_news_rss("artificial intelligence in education", "en", "US")),
        ("Google News: generative AI schools", google_news_rss("generative AI schools education", "en", "US")),
        ("Edutopia", "https://www.edutopia.org/rss.xml"),
    ]

    latvia_sources = [
        ("Google News Latvia: AI education", google_news_rss("mākslīgais intelekts izglītībā Latvija", "lv", "LV")),
        ("Google News Latvia: education technology Latvia", google_news_rss("izglītības tehnoloģijas Latvija", "lv", "LV")),
    ]

    world = []
    for source_name, url in world_sources:
        try:
            world.extend(fetch_feed(url, source_name))
        except Exception as e:
            print(f"Warning: failed to fetch world source {source_name}: {e}")

    latvia = []
    for source_name, url in latvia_sources:
        try:
            latvia.extend(fetch_feed(url, source_name))
        except Exception as e:
            print(f"Warning: failed to fetch Latvia source {source_name}: {e}")

    print(f"Total world items: {len(world)}")
    print(f"Total Latvia items: {len(latvia)}")

    return {
        "world": world,
        "latvia": latvia
    }
