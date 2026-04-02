from send_email import send_email


def main():
    subject = "Test email from AI Education Daily Brief"
    html_body = """
    <html>
      <body>
        <h2>Test email</h2>
        <p>This is a test email from your GitHub Actions workflow.</p>
      </body>
    </html>
    """
    send_email(subject, html_body)
    print("Test email sent successfully.")


if __name__ == "__main__":
    main()
