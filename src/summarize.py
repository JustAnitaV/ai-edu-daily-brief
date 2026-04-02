import os
from openai import OpenAI


def summarize_sample_news() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    prompt = """
You generate a daily email briefing about artificial intelligence in education.

Return valid HTML only.

Rules:
1. Create section heading: 🌍 World news
2. Include exactly 3 world news items
3. Create section heading: 🇱🇻 Latvijas jaunumi
4. Include exactly 2 Latvia news items
5. For each item:
   - Start with a bold theme sentence that is a clear statement
   - Write one concise factual paragraph
   - End with: Avots: followed by a clickable HTML link
6. For World news, each item must contain:
   - first the English version
   - then the Latvian version
7. For Latvijas jaunumi, write only in perfect Latvian
8. Tone must be concise, factual, professional

Use these sample items:

WORLD:
1. UNESCO released new guidance on responsible use of generative AI in schools.
   Source: https://www.unesco.org
2. A major university expanded an AI tutoring pilot for first-year students.
   Source: https://www.example.com/university-ai-pilot
3. An edtech company launched a classroom tool for automated feedback.
   Source: https://www.example.com/edtech-feedback-tool

LATVIA:
1. A Latvian school launched a teacher workshop on AI literacy.
   Source: https://www.example.com/latvia-school-ai
2. A Latvian education organization discussed AI use in learning materials.
   Source: https://www.example.com/latvia-education-ai
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    raise RuntimeError(f"OpenAI response did not include output_text: {response}")
