def wrap_email(content: str) -> str:
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f5f7fa; padding:20px;">
        <div style="max-width:700px; margin:auto; background:white; padding:30px; border-radius:10px;">

          <h1 style="margin-bottom:10px;">AI in Education Daily Brief</h1>
          <p style="color:#666; margin-top:0;">Daily curated updates on AI in education</p>

          <hr style="border:none; border-top:1px solid #eee; margin:20px 0;" />

          {content}

        </div>
      </body>
    </html>
    """
