# backend/prompts/base_templates.py

"""
Shared textual pieces for parameter-evaluation prompts.
No logic, just reusable text blocks.
"""

# backend/prompts/base_templates.py

SUMMARY_SYSTEM_PROMPT = """
You are a seasoned development executive writing a clear, concise
coverage-style summary for a film/series project based on parameter-level
evaluations.

Your goals:
- Explain the project's strengths and weaknesses in craft terms.
- Reference specific parameters (story engine, goal/stakes, momentum,
  protagonist arc, relationships, emotional/social truth, world specificity,
  theme/cinema, hook/recall, audience/market fit) where relevant.
- Be honest but constructive, like internal notes for producers.

Style:
- Professional, concrete, no fluff.
- Avoid repeating the full synopsis.
- Assume the reader already knows the basic premise.
""".strip()


SUMMARY_USER_PROMPT = """
Project title: {title}
Logline: {logline}
Genre: {genre}

Parameter evaluations:
{parameter_block}

Overall evaluation:
{overall_block}

Write:
1. A short overall verdict paragraph (1–3 sentences).
2. A "Strengths" section (bullet points).
3. A "Risks / Weaknesses" section (bullet points).
4. A "Practical notes" section with 2–4 concrete next-step suggestions
   the writer could act on.

Keep it under ~400 words.
Do NOT include numeric scores in the text (they are already handled in the UI).
""".strip()


SCORING_GUIDANCE = """
### Scoring calibration (1–10)

- **1–2 (Broken / Amateur)**  
  The parameter is fundamentally not working. Confusing, generic, or contradictory.
- **3–4 (Weak)**  
  Some intent is visible but execution is below professional spec; big gaps or clichés.
- **5 (Baseline Professional)**  
  Technically serviceable, readable, but familiar / safe / generic.
- **6–7 (Good)**  
  Clearly working, interesting choices, some specificity; still has notable issues.
- **8–9 (Strong / Premium)**  
  Distinctive, emotionally or commercially compelling, above industry average.
- **10 (Exceptional)**  
  Rare, best-in-class, the kind of element that would excite top-tier producers.
"""

OUTPUT_JSON_INSTRUCTIONS = """
### Output JSON

Return **STRICT JSON** with this exact shape and keys:

{
  "score": 0.0,
  "confidence": 1.0,
  "reasoning": "Short analytical paragraph grounded in the rubric.",
  "evidence": [
    "1–4 short bullet-style phrases or fragments quoted from the synopsis."
  ]
}

Rules:
- `score` must be a number between **0 and 10**.
- `confidence` between **0 and 1** (how sure you are).
- `reasoning` should reference concrete story choices, not vague adjectives.
- `evidence` must be a JSON array of strings, not a single string.
- Do **not** include any extra top-level keys.
"""
