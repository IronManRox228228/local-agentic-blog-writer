from .base_llm import call_llm
from observability.tracer import trace_span
import time


@trace_span("WriterAgent")
def writer_node(state):
    plan = state.plan
    full_draft_accumulated = ""

    total_sections = len(plan)
    print(f"  ...Drafting {total_sections} chapters in 'Human/Frank' Mode...")

    for i, section in enumerate(plan):
        print(f"  ...Writing Chapter {i + 1}/{total_sections}: {section}")

        context_prompt = ""
        if full_draft_accumulated:
            context_prompt = f"PREVIOUS CONTEXT:\n{full_draft_accumulated[-2000:]}..."

        # 🧠 THE HUMAN VIBE PROMPT
        prompt = f"""
        Role: You are a Senior Feature Writer for a top-tier magazine.
        Tone: Intellectual but conversational. Frank. Engaging.
        Topic: {state.initial_input}
        Chapter: {section}

        {context_prompt}

        TASK: Write the content for "{section}".

        STYLE RULES (CRITICAL):
        1. **Be Frank**: Speak directly to the reader. Use "we" or "you" sparingly but effectively.
        2. **No Fluff**: Do not use empty words like "testament," "tapestry," "delve," "crucial," or "realm."
        3. **Variable Sentence Length**: Mix very short sentences with longer explanations. This creates rhythm.
        4. **Nuance**: Don't just list facts. Offer a perspective or an opinion on them.
        5. **Avoid Robot-Speak**: Never say "In conclusion," "It is important to note," or "Furthermore." Just say it.

        Length: Write ~400 words of high-quality, flowy prose.
        """

        content = call_llm([{"role": "user", "content": prompt}], agent_role="writer")

        full_draft_accumulated += f"\n\n## {section}\n\n{content}"
        state.draft_sections[section] = content

        time.sleep(0.2)

    state.full_draft = full_draft_accumulated
    return state