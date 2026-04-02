import os
from openai import OpenAI


def summarize_news(world_items, latvia_items):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_items(items):
        if not items:
            return "None"
        return "\n".join(
            [f"- {i['title']} | {i['url']} | {i.get('source', 'Unknown source')}" for i in items]
        )

    prompt = f"""
You generate a daily email briefing about artificial intelligence in education.

Return clean HTML only. No markdown.

STRICT STRUCTURE:

- Use <h2> for section titles
- Each news item MUST be inside its own <div style="margin-bottom:20px;">
- Each language block must be a separate <p>
- Add spacing for readability

FORMAT EXACTLY LIKE THIS:

<h2>🌍 World news</h2>

<div>
  <p><strong>English theme sentence.</strong> English paragraph. Avots: <a href="URL">Source</a></p>
  <p><strong>Latvian theme sentence.</strong> Latvian paragraph. Avots: <a href="URL">Avots</a></p>
</div>

(repeat per item)

<h2>🇱🇻 Latvijas jaunumi</h2>

<div>
  <p><strong>Latvian theme sentence.</strong> Latvian paragraph. Avots: <a href="URL">Avots</a></p>
</div>

RULES:

1. 🌍 World news → 3–5 items
2. 🇱🇻 Latvijas jaunumi → 1–3 items (or 1 short sentence if none)
3. EACH item:
   - MUST be inside <div style="margin-bottom:20px;">
   - MUST NOT merge multiple items into one paragraph
4. World news:
   - English paragraph FIRST
   - Latvian paragraph SECOND
5. Latvian section:
   - Latvian only
6. Keep tone concise and factual
7. Use ONLY provided items

WORLD NEWS INPUT:
{format_items(world_items)}

LATVIA NEWS INPUT:
{format_items(latvia_items)}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
