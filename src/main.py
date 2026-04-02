import traceback
from summarize import summarize_sample_news
from send_email import send_email


def main():
    try:
        html_body = summarize_sample_news()
        subject = "AI in Education Daily Brief - Test OpenAI Version"
        send_email(subject, html_body)
        print("OpenAI-generated email sent successfully.")
    except Exception as e:
        print("ERROR START")
        print(type(e).__name__)
        print(str(e))
        traceback.print_exc()
        print("ERROR END")
        raise


if __name__ == "__main__":
    main()
