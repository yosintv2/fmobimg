import urllib.request, urllib.error, concurrent.futures, os, time

team_dir = "/Users/yosin/MyProjects/fotmob-images/team"
league_dir = "/Users/yosin/MyProjects/fotmob-images/league"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://www.fotmob.com/",
}

def download(base_url, out_dir, tid):
    url = f"{base_url}/{tid}.png"
    fp = os.path.join(out_dir, f"{tid}.png")
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
        return tid, f"err"

def run_batch(base_url, out_dir, id_range, label):
    total = len(id_range)
    done = 0
    found = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        fs = {ex.submit(download, base_url, out_dir, i): i for i in id_range}
        for f in concurrent.futures.as_completed(fs):
            tid, status = f.result()
            done += 1
            if status == "ok":
                found += 1
            if done % 1000 == 0 or done == total:
                print(f"[{label}] {done}/{total} | Found: {found}", flush=True)
    return found

# Team logos 15001-30000
print("=== Scanning team logos 15001-30000 ===")
found_teams = run_batch(
    "https://images.fotmob.com/image_resources/logo/teamlogo",
    team_dir,
    range(15001, 30001),
    "Teams"
)
print(f"Found {found_teams} new team logos")

# League logos 1-5000
print("\n=== Downloading league logos 1-5000 ===")
found_leagues = run_batch(
    "https://images.fotmob.com/image_resources/logo/leaguelogo",
    league_dir,
    range(1, 5001),
    "Leagues"
)
print(f"Downloaded {found_leagues} league logos")
