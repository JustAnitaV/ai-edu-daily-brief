import feedparser
import requests
from urllib.parse import quote_plus, urlparse


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIEduDailyBrief/1.0)"
}


SOURCE_NAME_MAP = {
    "edsurge.com": "EdSurge",
    "edutopia.org": "Edutopia",
    "openai.com": "OpenAI",
    "blogs.google": "Google",
    "edu.google.com": "Google for Education",
    "blog.google": "Google",
    "googleblog.com": "Google",
    "oecd.org": "OECD",
    "unesco.org": "UNESCO",
    "unicef.org": "UNICEF",
    "weforum.org": "World Economic Forum",
    "gov.uk": "UK Government",
    "europa.eu": "European Union",
    "ec.europa.eu": "European Commission",
    "consilium.europa.eu": "Council of the European Union",
    "parlament.com": "European Parliament",
    "nature.com": "Nature",
    "science.org": "Science",
    "lse.ac.uk": "LSE",
    "brookings.edu": "Brookings",
    "rand.org": "RAND",
    "theguardian.com": "The Guardian",
    "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post",
    "bbc.com": "BBC",
    "bbc.co.uk": "BBC",
    "reuters.com": "Reuters",
    "apnews.com": "AP News",
    "forbes.com": "Forbes",
    "techcrunch.com": "TechCrunch",
    "axios.com": "Axios",
    "hechingerreport.org": "The Hechinger Report",
    "insidehighered.com": "Inside Higher Ed",
    "chalkbeat.org": "Chalkbeat",
    "lsm.lv": "LSM",
    "leta.lv": "LETA",
    "delfi.lv": "Delfi",
    "tvnet.lv": "TVNET",
    "nra.lv": "Neatkarīgā",
    "izglitiba.gov.lv": "IZM",
    "visc.gov.lv": "VISC",
    "liis.lv": "LIIS",
}


def normalize_domain(netloc: str) -> str:
    domain = (netloc or "").lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def prettify_domain_name(domain: str) -> str:
    base = domain.split(".")[0]
    parts = [p for p in base.replace("-", " ").replace("_", " ").split() if p]
    return " ".join(part.capitalize() for part in parts) if parts else domain


def smart_source_name_from_url(url: str) -> tuple[str, str]:
    try:
        parsed = urlparse(url)
        domain = normalize_domain(parsed.netloc)
    except Exception:
        return "Unknown source", ""

    if not domain:
        return "Unknown source", ""

    if domain in SOURCE_NAME_MAP:
        return SOURCE_NAME_MAP[domain], domain

    # Fallback: try parent domain match
    domain_parts = domain.split(".")
    for i in range(len(domain_parts) - 1):
        candidate = ".".join(domain_parts[i:])
        if candidate in SOURCE_NAME_MAP:
            return SOURCE_NAME_MAP[candidate], domain

    return prettify_domain_name(domain), domain


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
            source_display, domain = smart_source_name_from_url(link)
            items.append({
                "title": title,
                "url": link,
                "published": published,
                "source": source_name,
                "source_display": source_display,
                "domain": domain,
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
        "AI teachers lesson planning generative AI classroom",
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
