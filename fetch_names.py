import urllib.request, urllib.error, json, os, re, concurrent.futures, time, sys

base_dir = os.path.dirname(os.path.abspath(__file__))
team_dir = os.path.join(base_dir, "team")
league_dir = os.path.join(base_dir, "league")

def get_build_id():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request("https://www.fotmob.com/", headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode()
    m = re.search(r'"buildId":"([^"]+)"', html)
    if m:
        return m.group(1)
    raise Exception("buildId not found")

build_id = get_build_id()
print(f"Build ID: {build_id}", flush=True)

team_ids = sorted([int(f.replace(".png", "")) for f in os.listdir(team_dir) if f.endswith(".png")])
league_ids = sorted([int(f.replace(".png", "")) for f in os.listdir(league_dir) if f.endswith(".png")])
print(f"Teams: {len(team_ids)}, Leagues: {len(league_ids)}", flush=True)

def fetch_team_name(tid):
    url = f"https://www.fotmob.com/_next/data/{build_id}/teams/{tid}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        fb = data.get("pageProps", {}).get("fallback", {})
        for key in fb:
            if key.startswith(f"team-{tid}"):
                val = fb[key]
                if val and isinstance(val, dict):
                    name = val.get("details", {}).get("name", "")
                    if name:
                        return tid, name
        return tid, None
    except Exception as e:
        return tid, None

def fetch_league_name(lid):
    url = f"https://www.fotmob.com/_next/data/{build_id}/leagues/{lid}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        fd = data.get("pageProps", {}).get("details", {})
        name = fd.get("name", "")
        return lid, name if name else None
    except:
        return lid, None

team_names = {}
league_names = {}

print("Fetching team names...", flush=True)
start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(fetch_team_name, tid): tid for tid in team_ids}
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        tid, name = future.result()
        if name:
            team_names[str(tid)] = name
        if i % 200 == 0 or i == len(team_ids):
            elapsed = time.time() - start
            rate = i / elapsed if elapsed else 0
            print(f"  Teams: {i}/{len(team_ids)} ({rate:.1f}/s, found {len(team_names)})", flush=True)

print(f"Found {len(team_names)} team names in {time.time()-start:.0f}s", flush=True)

print("Fetching league names...", flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(fetch_league_name, lid): lid for lid in league_ids}
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        lid, name = future.result()
        if name:
            league_names[str(lid)] = name
        if i % 100 == 0 or i == len(league_ids):
            print(f"  Leagues: {i}/{len(league_ids)}, found {len(league_names)}", flush=True)

print(f"Found {len(league_names)} league names", flush=True)
print(f"Total: {len(team_names)} teams, {len(league_names)} leagues", flush=True)

mapping = {
    "teams": team_names,
    "leagues": league_names,
}

with open(os.path.join(base_dir, "mapping.json"), "w") as f:
    json.dump(mapping, f, indent=2)

print("Saved mapping.json", flush=True)
