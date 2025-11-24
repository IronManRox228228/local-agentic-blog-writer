def compact_context(history: list, max_tokens: int = 2048):
    """
    Naive compaction: keeps system prompt + first 2 user interactions
    + last N interactions to fit context.
    """
    # Approximate token count (1 word ~= 1.3 tokens)
    estimated_tokens = sum([len(m['content'].split()) * 1.3 for m in history])

    if estimated_tokens < max_tokens:
        return history

    # Keep system prompt
    system = [h for h in history if h['role'] == 'system']
    others = [h for h in history if h['role'] != 'system']

    # If still too big, take the last 5 messages
    compacted = system + others[-5:]
    return compacted