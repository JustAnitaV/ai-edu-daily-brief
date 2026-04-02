def wrap_email(content: str) -> str:
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height:1.5; max-width:700px; margin:auto;">
        <h1 style="margin-bottom:20px;">AI in Education Daily Brief</h1>
        {content}
      </body>
    </html>
    """
