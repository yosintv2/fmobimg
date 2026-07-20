import urllib.request
import urllib.error
import concurrent.futures
import os
import sys

team_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "team")
os.makedirs(team_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.fotmob.com/",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "image",
}

def download_image(team_id):
    url = f"https://images.fotmob.com/image_resources/logo/teamlogo/{team_id}.png"
    filepath = os.path.join(team_dir, f"{team_id}.png")
    if os.path.exists(filepath):
        return team_id, "exists"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 100:
                with open(filepath, "wb") as f:
                    f.write(data)
                return team_id, "ok"
            return team_id, "small"
    except urllib.error.HTTPError as e:
        return team_id, f"http{e.code}"
    except Exception as e:
        return team_id, f"err{type(e).__name__}"

ids = list(range(1, 10001))
total = len(ids)
done = 0
ok = 0
errors = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(download_image, i): i for i in ids}
    for future in concurrent.futures.as_completed(futures):
        tid, status = future.result()
        done += 1
        if status == "ok":
            ok += 1
        elif status in ("exists", "small"):
            pass
        else:
            errors += 1
        if done % 500 == 0 or done == total:
            print(f"Progress: {done}/{total} | Downloaded: {ok} | Errors: {errors}", flush=True)

print(f"\nDone! Total: {total}, Downloaded: {ok}, Errors: {errors}")
