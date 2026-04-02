import os
from openai import OpenAI


def summarize_news(world_items, latvia_items):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_items(items):
        return "\n".join([
            f"- {i['title']} ({i['url']})"
            for i in items
        ])

    prompt = f"""
You generate a daily email briefing about artificial intelligence in education.

Return valid HTML only.

Rules:
1. 🌍 World news: 3–5 items
2. 🇱🇻 Latvijas jaunumi: 1–3 items (only if available)
3. Each item:
   - bold theme sentence
   - one paragraph
   - end with: Avots: clickable link
4. World news must be in English + Latvian
5. Latvia news must be perfect Latvian
6. Do not repeat titles

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
