from duckduckgo_search import DDGS


def search_web(query, max_results=3):
    print(f"  ...Searching DuckDuckGo for: '{query}'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        summary = ""
        for res in results:
            summary += f"Title: {res.get('title')}\nSnippet: {res.get('body')}\nSource: {res.get('href')}\n\n"

        return summary
    except Exception as e:
        return f"Search failed: {e}"