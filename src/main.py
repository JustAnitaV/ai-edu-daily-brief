import traceback
from datetime import datetime
from fetch_news import fetch_news
from filter_and_dedupe import (
    filter_and_dedupe,
    update_history,
    load_history,
    build_seen_set,
)
from summarize import summarize_news
from send_email import send_email
from build_email import wrap_email


PRIMARY_HOURS = 48
FALLBACK_HOURS = 168  # 7 days
MIN_TOTAL_ITEMS = 5

def build_subject(world_items, europe_items, latvia_items):
    all_items = world_items + europe_items + latvia_items
    count = len(all_items)

    # --- base ---
    if count == 0:
        base = "No updates"
    elif count <= 3:
        base = "Light day"
    elif count <= 6:
        base = f"{count} updates"
    else:
        base = f"Heavy day ({count} updates)"

    # --- tag detection ---
    titles = " ".join([i["title"].lower() for i in all_items])

    tags = []

    # Latvia
    if latvia_items:
        tags.append("🇱🇻 Latvia")

    # LLM / generative AI
    if any(x in titles for x in ["llm", "generative ai", "chatgpt", "gpt", "ai tutor"]):
        tags.append("LLM")

    # Policy
    if any(x in titles for x in ["policy", "guidelines", "ministry", "regulation"]):
        tags.append("Policy")

    # Schools / K-12
    if any(x in titles for x in ["school", "k-12", "classroom", "students"]):
        tags.append("Schools")

    # max 2–3 tags
    tags = tags[:3]

    tag_part = f" · {' · '.join(tags)}" if tags else ""

    return f"AI in Education — {base}{tag_part}"

def collect_items(news, history, recent_hours):
    seen = build_seen_set(history)

    world_items = filter_and_dedupe(
        news["world"], history, seen, limit=5, recent_hours=recent_hours
    )
    europe_items = filter_and_dedupe(
        news["europe"], history, seen, limit=5, recent_hours=recent_hours
    )
    latvia_items = filter_and_dedupe(
        news["latvia"], history, seen, limit=5, recent_hours=recent_hours
    )

    return world_items, europe_items, latvia_items


def main():
    try:
        news = fetch_news()
        history = load_history()

        world_items, europe_items, latvia_items = collect_items(
            news, history, PRIMARY_HOURS
        )

        total_items = len(world_items) + len(europe_items) + len(latvia_items)
        print(f"Items with {PRIMARY_HOURS}h window: {total_items}")

        if total_items < MIN_TOTAL_ITEMS:
            print(
                f"Too few items in {PRIMARY_HOURS}h window, retrying with {FALLBACK_HOURS}h window."
            )
            world_items, europe_items, latvia_items = collect_items(
                news, history, FALLBACK_HOURS
            )

        print(f"World items after dedupe: {len(world_items)}")
        print(f"Europe items after dedupe: {len(europe_items)}")
        print(f"Latvia items after dedupe: {len(latvia_items)}")

        if not world_items and not europe_items and not latvia_items:
            content = """
            <h2 style="margin-top:30px;">AI in Education Daily Brief</h2>
            <p><strong>No new qualifying items were found today.</strong> No fresh AI-in-education items passed the current filters for world, Europe, or Latvia sources. Avots: <a href="https://news.google.com/">Google News</a></p>
            """
        else:
            content = summarize_news(
                world_items[:4],
                europe_items[:4],
                latvia_items[:3]
            )

        html_body = wrap_email(content)

        subject = build_subject(world_items, europe_items, latvia_items)
        send_email(subject, html_body)

        update_history(world_items[:4] + europe_items[:4] + latvia_items[:3], history)

        print("Daily news email sent successfully.")

    except Exception as e:
        print("ERROR START")
        print(type(e).__name__)
        print(str(e))
        traceback.print_exc()
        print("ERROR END")
        raise


if __name__ == "__main__":
    main()
