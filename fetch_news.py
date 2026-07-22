import urllib.request, json, os, re
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def to_slug(text):
    s = text.lower().replace("'", "").replace(":", "")
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:100]

def transform_article(a):
    slug = to_slug(a.get("title", ""))
    source = a.get("sourceStr", "FotMob")
    pub = a.get("gmtTime", "").replace("Z", "") if a.get("gmtTime") else ""
    lead = a.get("lead", "")

    return {
        "slug": slug,
        "title": a.get("title", ""),
        "snippet": lead or f"{a.get('title', '')} - Read more on FotMob.",
        "content": [lead] if lead else [a.get("title", "")],
        "publishedAt": pub[:10] if pub else "",
        "updatedAt": pub[:10] if pub else "",
        "author": source,
        "labels": [],
        "metaTitle": f"{a.get('title', '')} | FotMob News",
        "metaDescription": lead or a.get("title", ""),
    }

news_raw = fetch_json("https://www.fotmob.com/api/worldnews?page=1")
trending_raw = fetch_json("https://www.fotmob.com/api/trendingnews")

articles = [transform_article(a) for a in news_raw]
trending = [transform_article(a) for a in trending_raw]

output = {
    "updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "total": len(articles),
    "trending": trending,
    "articles": articles,
}

path = os.path.join(base_dir, "news.json")
with open(path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved {len(articles)} articles + {len(trending)} trending to news.json")
