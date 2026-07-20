import urllib.request, urllib.error, concurrent.futures, os

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clogo")
os.makedirs(out_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

logos = [
    # International teams - Full Members
    "india", "australia", "england", "pakistan", "srilanka", "newzealand",
    "southafrica", "westindies", "bangladesh", "zimbabwe", "afghanistan",
    "ireland", "scotland",
    # International teams - Associate Members
    "netherlands", "namibia", "oman", "uae", "nepal", "hongkong",
    "papuanewguinea", "usa", "canada", "bermuda", "kenya", "uganda",
    "jersey", "malaysia", "singapore",
    # Other associate nations
    "argentina", "austria", "bahamas", "bahrain", "barbados", "belgium",
    "belize", "botswana", "bulgaria", "caymanislands", "china", "croatia",
    "cyprus", "czechrepublic", "denmark", "egypt", "eswatini", "estonia",
    "fiji", "finland", "france", "germany", "ghana", "greece", "guernsey",
    "guyana", "hungary", "isleofman", "italy", "jamaica", "japan",
    "kuwait", "luxembourg", "malawi", "mali", "malta", "mozambique",
    "nigeria", "norway", "panama", "poland", "portugal", "qatar",
    "romania", "rwanda", "saudiarabia", "serbia", "sierraleone", "spain",
    "sweden", "switzerland", "tanzania", "trinidad", "turkey",
    # Women's international teams
    "australiawomen", "bangladeshwomen", "canadawomen", "englandwomen",
    "hongkongwomen", "irelandwomen", "malaysiawomen", "namibiawomen",
    "netherlandswomen", "newzealandwomen", "omanwomen", "pakistanwomen",
    "papuanewguineawomen", "scotlandwomen", "southafricawomen",
    "srilankawomen", "thailandwomen", "ugandawomen", "westindieswomen",
    "zimbabwewomen",
    # IPL teams
    "chennaisuperkings", "mumbaiindians", "kolkataknightriders",
    "royalchallengersbangalore", "sunrisershyderabad", "delhicapitals",
    "punjabkings", "rajasthanroyals", "lucknowsupergiants", "gujarattitans",
    # BBL teams
    "sydneysixers", "sydneythunder", "melbournestars", "melbournerenegades",
    "perthscorchers", "brisbaneheat", "adelaidestrikers", "hobarthurricanes",
    # PSL teams
    "karachikings", "lahoreqalandars", "islamabadunited", "multansultans",
    "peshawarzalmi", "hyderabadkingsmen",
    # SA20 teams
    "sunriserseasterncape", "pretoriacapitals", "joburgsuperkings",
    "paarlroyals", "durbansupergiants",
    # ILT20 teams
    "abudhabi", "dubaicapitals", "dubai", "sharjahwarriors", "gulfgiants",
    "desertvipers",
    # The Hundred teams
    "londonspirit", "ovalinvincibles", "birminghamphoenix",
    "northernsuperchargers", "trentrockets", "manchesteroriginals",
    "welshfire",
    # Pakistan domestic
    "balochistan", "sindh", "khyberpakhtunkhwa",
    # New Zealand domestic
    "northern", "otagovolts",
    # South African domestic
    "lions", "warriors", "dolphins", "titans", "knightriders",
    "westernprovince",
    # English county teams
    "surrey", "yorkshire", "lancashire", "sussex", "kent", "essex",
    "warwickshire", "hampshire", "nottinghamshire", "somerset",
    "derbyshire", "glamorgan", "gloucestershire", "durham",
    "northamptonshire", "leicestershire", "worcestershire", "middlesex",
    # Special logos
    "icc-n-lgo", "bbl-lgo", "wbbl-lgo", "hbl-psl", "strr-lgo", "ipl",
    "worldxi",
]

def download(name):
    url = f"https://aimages.willow.tv/teamLogos/{name}.png"
    fp = os.path.join(out_dir, f"{name}.png")
    if os.path.exists(fp):
        return name, "exists"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 100:
                with open(fp, "wb") as f:
                    f.write(data)
                return name, "ok"
            return name, "small"
    except urllib.error.HTTPError as e:
        return name, f"http{e.code}"
    except Exception as e:
        return name, f"err{type(e).__name__}"

total = len(logos)
done = 0
ok = 0
errors = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(download, n): n for n in logos}
    for future in concurrent.futures.as_completed(futures):
        name, status = future.result()
        done += 1
        if status == "ok":
            ok += 1
        elif status == "exists":
            pass
        else:
            errors += 1
        if done % 20 == 0 or done == total:
            print(f"Progress: {done}/{total} | Downloaded: {ok} | Errors: {errors}", flush=True)

print(f"\nDone! Total: {total}, Downloaded: {ok}, Skipped (exist): {total - ok - errors}, Errors: {errors}")
