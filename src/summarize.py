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

Return clean HTML only. Do not use markdown. Do not wrap output in code fences.

STRICT REQUIREMENTS:

1. Use this exact section header styling:
<h2 style="margin-top:30px;">🌍 World news</h2>
<h2 style="margin-top:30px;">🇱🇻 Latvijas jaunumi</h2>

2. Each news item MUST be visually separated and MUST use this exact outer container:
<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">

3. WORLD NEWS:
- Include 3–5 items if available
- For each item, write:
  a) one English block
  b) one Latvian block
- The English block must come first
- The Latvian block must come second

4. LATVIJAS JAUNUMI:
- Include 1–3 items if available
- Write only in perfect Latvian
- If there are no Latvia items, write one short Latvian sentence saying no new Latvia-specific items were found today

5. EACH LANGUAGE BLOCK MUST USE EXACTLY THIS HTML STRUCTURE:

<p style="margin:0 0 8px 0;"><strong>Theme sentence.</strong></p>
<p style="margin:0 0 8px 0;">Paragraph text.</p>
<p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source</a></p>

6. IMPORTANT:
- Do NOT merge multiple items into one paragraph
- Do NOT place all world news into one block
- Each item must have its own separate <div ...> container
- Keep tone concise, factual, professional
- Use ONLY the provided items
- Do NOT invent facts, dates, names, or sources

7. WORLD NEWS ITEM TEMPLATE:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>English theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">English paragraph.</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source</a></p>

  <p style="margin:12px 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Latvian paragraph.</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Avots</a></p>
</div>

8. LATVIA ITEM TEMPLATE:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Latvian paragraph.</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Avots</a></p>
</div>

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
