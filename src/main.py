from summarize import summarize_sample_news
from send_email import send_email


def main():
    html_body = summarize_sample_news()
    subject = "AI in Education Daily Brief - Test OpenAI Version"
    send_email(subject, html_body)
    print("OpenAI-generated email sent successfully.")


if __name__ == "__main__":
    main()
