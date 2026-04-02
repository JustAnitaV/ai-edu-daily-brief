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

Return valid HTML only. Do not wrap output in markdown fences.

Rules:
1. Create section heading: <h2>🌍 World news</h2>
2. Include 3–5 world items if available. If fewer are available, use only what is provided.
3. Create section heading: <h2>🇱🇻 Latvijas jaunumi</h2>
4. Include 1–3 Latvia items only if available. If none are available, write one short Latvian sentence saying that no new Latvia-specific items were found today.
5. Each news item must:
   - start with a bold theme sentence that is a clear statement
   - be written as one paragraph
   - end with: Avots: and a clickable HTML link
6. World news: for each item, first write the English paragraph, then the Latvian paragraph.
7. Latvian news: perfect Latvian only.
8. Keep tone concise, factual, professional.
9. Use only the provided items. Do not invent details.

WORLD NEWS INPUT:
{format_items(world_items)}

LATVIA NEWS INPUT:
{format_items(latvia_items)}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    raise RuntimeError(f"OpenAI response did not include output_text: {response}")
