import requests
import xml.etree.ElementTree as ET


def fetch_rss(url):
    response = requests.get(url, timeout=10)
    root = ET.fromstring(response.content)

    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title")
        link = item.findtext("link")
        pub_date = item.findtext("pubDate")

        if title and link:
            items.append({
                "title": title.strip(),
                "url": link.strip(),
                "published": pub_date
            })

    return items


def fetch_news():
    world_sources = [
        "https://news.google.com/rss/search?q=AI+education",
        "https://www.edutopia.org/rss.xml"
    ]

    latvia_sources = [
        "https://news.google.com/rss/search?q=AI+education+Latvia&hl=lv"
    ]

    world = []
    for url in world_sources:
        world.extend(fetch_rss(url))

    latvia = []
    for url in latvia_sources:
        latvia.extend(fetch_rss(url))

    return {
        "world": world,
        "latvia": latvia
    }
