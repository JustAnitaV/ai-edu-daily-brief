import os
from openai import OpenAI


def summarize_news(world_items, europe_items, latvia_items):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_items(items):
        if not items:
            return "None"
        return "\n".join(
            [f"- {i['title']} | {i['url']} | {i.get('source', 'Unknown source')}" for i in items]
        )

    prompt = f"""
You generate a premium daily intelligence brief about artificial intelligence in education.

Return clean HTML only. Do not use markdown. Do not wrap output in code fences.

STYLE GOAL:
The output should feel like a premium analyst newsletter: clear, structured, precise, concise but substantive.
Summaries should be slightly more detailed than before and explain the significance of each development more clearly.

STRICT OUTPUT STRUCTURE:

<h2 style="margin-top:30px;">🔥 Top story</h2>
<div style="margin-bottom:25px; padding:16px; background-color:#f8fafc; border:1px solid #e5e7eb; border-radius:8px;">
  ...
</div>

<h2 style="margin-top:30px;">⚡ Key highlights</h2>
<ul style="padding-left:18px;">
  <li>...</li>
  <li>...</li>
  <li>...</li>
</ul>

<h2 style="margin-top:30px;">🇪🇺 Europe news</h2>
... items ...

<h2 style="margin-top:30px;">🌍 World news</h2>
... items ...

<h2 style="margin-top:30px;">🇱🇻 Latvijas jaunumi</h2>
... items ...

RULES:

1. TOP STORY
- Choose the single most important item from EUROPE or WORLD input.
- Write it as a featured item with:
  - one English block
  - one Latvian block
  - a short tag line at the end
- Make this summary more developed: 2–3 sentences in each language paragraph.
- Be precise about what happened and why it matters for education.

2. KEY HIGHLIGHTS
- Add 3 short bullet points in English block first and Latvian block second.
- Each bullet should summarize a broader takeaway from today’s news, not repeat full headlines.
- Examples of useful angles: policy direction, classroom adoption, teacher workload, higher education strategy, governance risk.

3. EUROPE NEWS
- Include 2–4 items if available.
- Focus on European institutions, schools, universities, policy, edtech, implementation.
- For each item:
  - English block first
  - Latvian block second
- Each paragraph should be more developed than before: usually 2 sentences, sometimes 3 if needed.

4. WORLD NEWS
- Include 2–4 items if available.
- Avoid overfilling with US-only items if Europe already has enough material.
- For each item:
  - English block first
  - Latvian block second
- Each paragraph should explain the development more precisely and make the subject clear.

5. LATVIJAS JAUNUMI
- Include 1–3 items if available.
- Write only in excellent natural Latvian.
- If there are no Latvia items, write one short Latvian sentence saying that no new Latvia-specific items were found today.

6. EACH ITEM MUST USE THIS EXACT CONTAINER:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  ...
</div>

7. FOR EUROPE/WORLD ITEMS USE THIS HTML STRUCTURE EXACTLY:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>English theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">A more developed English summary of 2–3 sentences that explains the topic clearly and precisely.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tags:</strong> tag1 · tag2 · tag3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source</a></p>

  <p style="margin:14px 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Izvērstāks kopsavilkums latviešu valodā 2–3 teikumos, precīzi izskaidrojot tematu un nozīmi.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tēmas:</strong> tēma1 · tēma2 · tēma3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Avots</a></p>
</div>

8. FOR LATVIA ITEMS USE THIS HTML STRUCTURE EXACTLY:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Izvērstāks kopsavilkums latviešu valodā 2–3 teikumos, skaidri atklājot, kas noticis un kāpēc tas ir nozīmīgi.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tēmas:</strong> tēma1 · tēma2 · tēma3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Avots</a></p>
</div>

9. IMPORTANT
- Do NOT merge multiple items into one paragraph.
- Do NOT invent facts, dates, institutions, or claims.
- Use ONLY the provided items.
- Keep tone professional, factual, analytical.
- Avoid vague wording like "interesting development" unless you specify what the development is.
- Theme sentences should be specific and informative, not generic.
- Tags should be short topical labels such as: policy, higher education, teacher training, classroom tools, assessment, governance, edtech, literacy, implementation.

EUROPE NEWS INPUT:
{format_items(europe_items)}

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
