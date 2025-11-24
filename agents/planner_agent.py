from .base_llm import call_llm
from tools.web_search import search_web
from observability.tracer import trace_span


@trace_span("PlannerAgent")
def planner_node(state):
    topic = state.initial_input
    print(f"  ...Researching topic: {topic}")

    try:
        web_context = search_web(topic)
    except Exception as e:
        print(f"  [Warn] Search failed ({e}). Relying on Llama 3.1 internal knowledge.")
        web_context = "Search unavailable. Use internal training data."

    prompt = f"""
    You are a Lead Content Strategist.
    User Topic: "{topic}"
    Context: {web_context[:2000]}

    Task: Create a comprehensive Table of Contents for a deep-dive book about this topic.
    Requirements:
    - Generate exactly 8 to 10 distinct chapters.
    - Ensure a logical flow from introduction to advanced concepts to conclusion.
    - Return ONLY the numbered list of chapter titles.
    """

    response = call_llm([{"role": "user", "content": prompt}], agent_role="planner")

    sections = [line.strip() for line in response.split('\n') if line.strip() and line[0].isdigit()]


    if not sections:
        print("  ! Llama output unparseable. Retrying with stricter prompt...")

        response = call_llm([{"role": "user", "content": f"List 10 chapter titles for '{topic}'. Numbered list only."}],
                            agent_role="planner")
        sections = [line.strip() for line in response.split('\n') if line.strip() and line[0].isdigit()]

    state.plan = sections
    state.metadata['search_context'] = web_context
    return state