from fetch_news import fetch_news
from filter_and_dedupe import filter_and_dedupe, update_history
from summarize import summarize_news
from send_email import send_email


def main():
    news = fetch_news()

    world_items, history = filter_and_dedupe(news["world"])
    latvia_items, _ = filter_and_dedupe(news["latvia"])

    html_body = summarize_news(world_items[:5], latvia_items[:3])

    subject = "AI in Education Daily Brief"
    send_email(subject, html_body)

    update_history(world_items + latvia_items, history)

    print("Daily news email sent.")


if __name__ == "__main__":
    main()
