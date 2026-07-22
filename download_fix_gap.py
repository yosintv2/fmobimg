import urllib.request, urllib.error, concurrent.futures, os, time

team_dir = "/Users/yosin/MyProjects/fotmob-images/team"
os.makedirs(team_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://www.fotmob.com/",
}

def download(tid):
    url = f"https://images.fotmob.com/image_resources/logo/teamlogo/{tid}.png"
    fp = os.path.join(team_dir, f"{tid}.png")
    if os.path.exists(fp):
        return tid, "exists"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            if len(data) > 100:
                with open(fp, "wb") as f:
                    f.write(data)
                return tid, "ok"
            return tid, "small"
    except urllib.error.HTTPError as e:
        return tid, f"http{e.code}"
    except Exception as e:
        return tid, "err"

start = 500001
end = 1000000
total = end - start + 1
done = 0
found = 0
batch_size = 2000

for batch_start in range(start, end + 1, batch_size):
    batch_end = min(batch_start + batch_size - 1, end)
    ids = list(range(batch_start, batch_end + 1))
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        fs = {ex.submit(download, i): i for i in ids}
        for f in concurrent.futures.as_completed(fs):
            tid, status = f.result()
            done += 1
            if status == "ok":
                found += 1
            if done % 2000 == 0 or done == total:
                elapsed = time.time() - t0 if 't0' in dir() else 0
                print(f"[{start}-{end}] {done}/{total} | Found: {found}", flush=True)
print(f"\nDone. Total new logos found in gap: {found}")
