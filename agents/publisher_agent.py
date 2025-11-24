from tools.markdown_export import save_markdown
from observability.tracer import trace_span
import time


@trace_span("PublisherAgent")
def publisher_node(state):
    filename = state.initial_input.replace(" ", "_").lower()[:20] + f"_{int(time.time())}"

    path = save_markdown(filename, state.final_output)
    print(f"  ✓ Published to: {path}")

    meta_content = f"Plan: {state.plan}\nTone: {state.metadata.get('tone')}\nContext: {state.metadata.get('search_context')}"
    save_markdown(f"{filename}_meta", meta_content)

    return state