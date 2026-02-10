from ddgs import DDGS  # <--- UPDATED IMPORT

def search_web(query):
    """Searches DuckDuckGo and returns the top 3 results."""
    try:
        # Force the print to show up immediately
        print(f"\n🔎 Searching for: {query}", flush=True)
        
        # The new DDGS library works exactly the same way
        results = DDGS().text(query, max_results=3)
        
        if not results:
            return "I couldn't find anything on that."
            
        summary = "Here is what I found:\n"
        for r in results:
            summary += f"- {r['title']}: {r['body']}\n"
            
        return summary
        
    except Exception as e:
        print(f"❌ Search Error: {e}", flush=True)
        return f"Search failed: {e}"