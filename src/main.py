import traceback
from datetime import datetime
from fetch_news import fetch_news
from filter_and_dedupe import filter_and_dedupe, update_history
from summarize import summarize_news
from send_email import send_email
from build_email import wrap_email


def main():
    try:
        news = fetch_news()

        world_items, history = filter_and_dedupe(news["world"])
        europe_items, _ = filter_and_dedupe(news["europe"])
        latvia_items, _ = filter_and_dedupe(news["latvia"])

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

        subject = f"AI in Education Daily Brief - {datetime.utcnow().date()}"
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
