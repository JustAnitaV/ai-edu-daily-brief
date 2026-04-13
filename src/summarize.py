import os
from openai import OpenAI


def summarize_news(world_items, europe_items, latvia_items):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def format_items(items):
        if not items:
            return "None"
        return "\n".join(
            [
                f"- Title: {i['title']} | URL: {i['url']} | Source: {i.get('source_display', i.get('source', 'Unknown source'))} | Domain: {i.get('domain', '')} | Published: {i.get('published', '')}"
                for i in items
            ]
        )

    prompt = f"""
You generate a curated daily intelligence brief about artificial intelligence in education.

Return clean HTML only.
Do not use markdown.
Do not wrap output in code fences.

EDITORIAL PRIORITIES:
This brief is primarily for tracking AI in school-age education (roughly ages 7-18, K-12, primary, lower secondary, upper secondary).
The strongest priority is student learning.
The second priority is teacher work.
The third priority is system-level developments such as policy, guidance, governance, implementation frameworks, and institutional recommendations.
There is a special interest in LLMs, chatbots, natural language processing, generative AI and related classroom or school use cases.
Higher education may appear only if it clearly signals a broader shift relevant to schools.

SELECTION PRIORITIES:
Prefer items that involve one or more of the following:
- student learning, homework, tutoring, writing, reading, feedback, classroom use
- teacher workflows, lesson planning, content generation, differentiation, assessment support
- assessment, academic integrity, exams, homework redesign
- policy, ministry guidance, school governance, safety, privacy, implementation rules
- research findings or evidence about impact
- concrete school or system implementation examples
- clear incidents, failures, restrictions, or cautionary lessons

DE-PRIORITIZE:
- generic trend language without a concrete development
- broad AI commentary without a real education link
- higher education items that do not have relevance for school education
- pure PR language without a meaningful implication

ANALYTICAL RULES:
- Use only the provided items.
- Do not invent facts, dates, locations, institutions, or outcomes.
- You may make careful, limited inferences about significance, but only if they are clearly supported by the item title/source context.
- Do not overstate certainty.
- Be concrete and specific.
- Avoid vague phrases such as "important development" unless you immediately explain why.

OUTPUT STRUCTURE:

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

TOP STORY RULES:
- Choose the single strongest item from EUROPE or WORLD.
- Prioritize in this order:
  1. school-age/K-12 relevance
  2. direct implications for student learning
  3. LLM/generative AI relevance
  4. implications for teacher work
  5. policy/system relevance
  6. only then broader education relevance
- The featured item must include:
  - one English block
  - one Latvian block
  - one short closing line: "Why this matters"
- Each language block should be 2-3 sentences.
- State the country or location if it is evident from the item.
- Explain what happened and why it matters, especially for learners, teachers, or education systems.

KEY HIGHLIGHTS RULES:
- Write exactly 3 bullet points.
- Bullet 1 should focus on learner impact or classroom learning patterns.
- Bullet 2 should focus on teacher workflow / assessment / homework / academic integrity.
- Bullet 3 should focus on system-level implications, policy, or signals relevant for Latvia.
- Keep them analytical and concise.
- Do not repeat headlines word-for-word.
- English block first - all key highlights in one block.
- Latvian block second - all key highlights in one block.

EUROPE NEWS RULES:
- Include 2-4 items if available.
- Prefer school education, LLM use, guidance, implementation, assessment, and evidence.
- For each item:
  - English block first
  - Latvian block second
  - mention location if evident
  - usually 2 sentences per language block
- Avoid generic summary language.

WORLD NEWS RULES:
- Include 2-4 items if available.
- Prefer concrete developments relevant to school education.
- Include higher education only if it clearly signals a school-relevant shift.
- For each item:
  - English block first
  - Latvian block second
  - mention location if evident
  - usually 2 sentences per language block

LATVIJAS JAUNUMI RULES:
- Include 1-3 items if available.
- Write only in excellent Latvian.
- For Latvia, you may include broader education ecosystem signals if they are clearly relevant to AI in education:
  - schools
  - ministries / agencies
  - pilot projects
  - guidance
  - professional discussions
  - implementation signals
- If there are no Latvia-specific items, write one short Latvian sentence saying that no meaningful Latvia-specific items were found today.

FOR EUROPE/WORLD ITEMS USE THIS EXACT HTML STRUCTURE:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>English theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">A precise English summary in 2-3 sentences. It should say what happened and why it matters for learners, teachers, or systems.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tags:</strong> tag1 · tag2 · tag3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source name</a></p>

  <p style="margin:14px 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Precīzs kopsavilkums latviešu valodā 2-3 teikumos. Tajā skaidri pasaki, kas noticis un kāpēc tas ir svarīgi skolēniem, skolotājiem vai sistēmai.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tēmas:</strong> tēma1 · tēma2 · tēma3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source name</a></p>
</div>

FOR LATVIA ITEMS USE THIS EXACT HTML STRUCTURE:

<div style="margin-bottom:25px; padding-bottom:15px; border-bottom:1px solid #eee;">
  <p style="margin:0 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
  <p style="margin:0 0 8px 0;">Izvērstāks un precīzs kopsavilkums latviešu valodā 2-3 teikumos, skaidri pasakot, kas noticis un kāpēc tas ir svarīgi Latvijas izglītības ekosistēmai.</p>
  <p style="margin:0 0 8px 0; font-size:12px; color:#374151;"><strong>Tēmas:</strong> tēma1 · tēma2 · tēma3</p>
  <p style="margin:0; font-size:12px; color:#666;">Avots: <a href="URL">Source name</a></p>
</div>

TOP STORY HTML REQUIREMENTS:
Use this exact structure inside the featured box:
<p style="margin:0 0 8px 0;"><strong>English theme sentence.</strong></p>
<p style="margin:0 0 10px 0;">2-3 sentence English explanation.</p>
<p style="margin:0 0 14px 0; font-size:12px; color:#374151;"><strong>Tags:</strong> tag1 · tag2 · tag3</p>
<p style="margin:0 0 8px 0;"><strong>Latvian theme sentence.</strong></p>
<p style="margin:0 0 10px 0;">2-3 sentence Latvian explanation.</p>
<p style="margin:0 0 14px 0; font-size:12px; color:#374151;"><strong>Tēmas:</strong> tēma1 · tēma2 · tēma3</p>
<p style="margin:0; font-size:13px; color:#111827;"><strong>Why this matters:</strong> One concise sentence in English.</p>
<p style="margin:6px 0 0 0; font-size:12px; color:#666;">Avots: <a href="URL">Source name</a></p>

IMPORTANT:
- Do not merge multiple items into one paragraph.
- Do not duplicate the same item in multiple sections.
- Keep the tone analytical, restrained, and useful.
- Always use the provided Source field as the visible text in the "Avots" link. Never use generic labels like "Source".
- Tags should be short and specific, for example:
  learning · homework · assessment · teacher workflow · policy · governance · safety · K-12 · schools · LLM · generative AI · exams · integrity · pilot · guidance

CORRECT TRANSLATIONS:
- In Latvian use correct terminology
- Remember: 
    - AI (artificial intelligence) = MI (mākslīgais intelekts)
    - Generative AI = Ģeneratīvais MI
    - LLM (large language model) = LVM (lielais valodu modelis)
    - chatbot = sarunbots vai čatbots

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
