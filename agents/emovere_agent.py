from .base_llm import call_llm
from observability.tracer import trace_span


@trace_span("EmovereAgent")
def emovere_node(state):
    print(f"  ...Emovere: Applying 'Humanizing' pass to the text.")

    original_text = state.full_draft

    prompt = f"""
    You are a Ghostwriter and Editor.
    Your job is to make AI-generated text sound strictly HUMAN.

    INPUT TEXT:
    {original_text}

    INSTRUCTIONS:
    1. **Remove AI Clichés**: Delete words/phrases like:
       - "In conclusion"
       - "It is worth noting"
       - "A testament to"
       - "Delve into"
       - "Embark on a journey"
       - "In today's world"

    2. **Fix the Flow**: 
       - If a sentence is too formal, loosen it up.
       - If it sounds too robotic, make it frank and direct.
       - Use contractions (e.g., use "It's" instead of "It is").

    3. **The 'Not Too Frank' Rule**:
       - Keep it professional. Do not use slang.
       - Be authoritative but not arrogant.

    OUTPUT:
    Return the rewritten text. Do not add comments.
    """

    humanized_text = call_llm([{"role": "user", "content": prompt}], agent_role="emovere")

    state.emotional_draft = humanized_text
    state.metadata['tone'] = "Human/Frank"

    return state