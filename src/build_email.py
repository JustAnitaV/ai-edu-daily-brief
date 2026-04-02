def wrap_email(content: str) -> str:
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f3f6fb; padding:24px; color:#111827;">
        <div style="max-width:760px; margin:auto; background:white; padding:32px; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">

          <h1 style="margin:0 0 8px 0; font-size:28px;">AI in Education Daily Brief</h1>
          <p style="margin:0 0 20px 0; color:#6b7280; font-size:14px;">
            Premium daily intelligence on AI in education: top story, regional signals, global developments, and Latvia updates.
          </p>

          <hr style="border:none; border-top:1px solid #e5e7eb; margin:20px 0;" />

          {content}

        </div>
      </body>
    </html>
    """
