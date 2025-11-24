from .base_llm import call_llm
from observability.tracer import trace_span


@trace_span("EditorAgent")
def editor_node(state):
    text = state.emotional_draft

    prompt = f"""
    You are a text-processing engine. You are NOT an assistant.

    INPUT TEXT:
    {text}

    TASK: 
    1. Fix grammar and typos.
    2. Ensure Markdown formatting (headers, bolding) is correct.
    3. Do NOT summarize. Keep the length.

    CRITICAL OUTPUT RULES:
    - Output ONLY the edited text.
    - DO NOT say "Here is the edited version".
    - DO NOT add "I made minor changes".
    - DO NOT add a preamble or postscript.
    - Start the output immediately with the first word of the text.
    """

    final_polish = call_llm([{"role": "user", "content": prompt}], agent_role="editor")


    clean_lines = []
    lines = final_polish.split('\n')

    start_collecting = False

    for line in lines:
        stripped = line.strip().lower()

        if stripped.startswith("here is the") or stripped.startswith("i have reviewed") or stripped.startswith(
                "sure, here"):
            continue
        if stripped.startswith("i hope this") or stripped.startswith("let me know"):
            continue

        if stripped.startswith("#"):
            start_collecting = True

        if not start_collecting and not stripped:
            continue

        clean_lines.append(line)

    if clean_lines:
        state.final_output = "\n".join(clean_lines)
    else:
        # If our filter deleted everything (oops), just use raw output
        state.final_output = final_polish

    return state