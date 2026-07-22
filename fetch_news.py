import urllib.request, json, os, sys
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

def fetch_news(page=1):
    url = f"https://www.fotmob.com/api/worldnews?page={page}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def fetch_trending():
    req = urllib.request.Request("https://www.fotmob.com/api/trendingnews", headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

news = fetch_news(1)
trending = fetch_trending()

output = {
    "updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "total": len(news),
    "trending": trending,
    "articles": news,
}

with open(os.path.join(base_dir, "news.json"), "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(news)} articles + {len(trending)} trending stories to news.json")
