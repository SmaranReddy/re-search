import feedparser

url = "https://export.arxiv.org/api/query?search_query=all:Attention+is+all+you+need&start=0&max_results=5"
feed = feedparser.parse(url)

for entry in feed.entries:
    print("Title:", entry.title)
    print("Authors:", [author.name for author in entry.authors])
    print("Published:", entry.published)
    print("Summary:", entry.summary[:200], "...")
    print("Link:", entry.link)
    print("-" * 80)
