import urllib.request, urllib.error, concurrent.futures, os

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "country")
os.makedirs(out_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

country_map = {
    # North & Central America
    "usa": "usa", "can": "canada", "mex": "mexico",
    "blz": "belize", "crc": "costa_rica", "slv": "el_salvador",
    "gua": "guatemala", "HON": "honduras", "nca": "nicaragua",
    "pan": "panama",
    # Caribbean
    "aia": "anguilla", "atg": "antigua_and_barbuda", "bah": "bahamas",
    "brb": "barbados", "ber": "bermuda", "vgb": "british_virgin_islands",
    "cay": "cayman_islands", "cub": "cuba", "dma": "dominica",
    "dom": "dominican_republic", "grn": "grenada", "hai": "haiti",
    "jam": "jamaica", "lca": "saint_lucia",
    "vin": "saint_vincent_and_the_grenadines", "tri": "trinidad_and_tobago",
    # South America
    "arg": "argentina", "bol": "bolivia", "bra": "brazil",
    "chi": "chile", "col": "colombia", "ecu": "ecuador",
    "guy": "guyana", "par": "paraguay", "per": "peru",
    "sur": "suriname", "uru": "uruguay", "ven": "venezuela",
    # Europe
    "alb": "albania", "and": "andorra", "arm": "armenia",
    "aut": "austria", "aze": "azerbaijan", "blr": "belarus",
    "bel": "belgium", "bih": "bosnia_and_herzegovina", "bul": "bulgaria",
    "cro": "croatia", "cyp": "cyprus", "cze": "czechia",
    "den": "denmark", "eng": "england", "est": "estonia",
    "fro": "faroe_islands", "fin": "finland", "fra": "france",
    "geo": "georgia", "ger": "germany", "gib": "gibraltar",
    "gre": "greece", "hun": "hungary", "isl": "iceland",
    "irl": "ireland", "isr": "israel", "ita": "italy",
    "kaz": "kazakhstan", "kos": "kosovo", "lat": "latvia",
    "lie": "liechtenstein", "ltu": "lithuania", "lux": "luxembourg",
    "mlt": "malta", "mda": "moldova", "mon": "monaco",
    "mne": "montenegro", "ned": "netherlands", "nir": "northern_ireland",
    "mkd": "north_macedonia", "nor": "norway", "pol": "poland",
    "por": "portugal", "rou": "romania", "rus": "russia",
    "smr": "san_marino", "sco": "scotland", "srb": "serbia",
    "svk": "slovakia", "svn": "slovenia", "esp": "spain",
    "swe": "sweden", "sui": "switzerland", "tur": "turkey",
    "ukr": "ukraine", "wal": "wales",
    # Africa
    "alg": "algeria", "ang": "angola", "ben": "benin",
    "bot": "botswana", "bfa": "burkina_faso", "bdi": "burundi",
    "cmr": "cameroon", "cpv": "cape_verde", "cha": "chad",
    "com": "comoros", "cod": "congo_drc",
    "eqg": "equatorial_guinea", "eri": "eritrea", "eth": "ethiopia",
    "gab": "gabon", "gam": "gambia", "gha": "ghana",
    "gnb": "guinea_bissau", "civ": "ivory_coast", "ken": "kenya",
    "les": "lesotho", "lbr": "liberia", "lby": "libya",
    "mad": "madagascar", "mwi": "malawi", "mli": "mali",
    "mri": "mauritania", "mar": "morocco", "moz": "mozambique",
    "nam": "namibia", "NIG": "niger", "nga": "nigeria",
    "rwa": "rwanda", "stp": "sao_tome_and_principe",
    "sen": "senegal", "sey": "seychelles", "sle": "sierra_leone",
    "som": "somalia", "rsa": "south_africa", "ssd": "south_sudan",
    "sud": "sudan", "swz": "eswatini", "tan": "tanzania",
    "tog": "togo", "tun": "tunisia", "uga": "uganda",
    "zam": "zambia", "zim": "zimbabwe",
    # Asia
    "afg": "afghanistan", "bhr": "bahrain", "ban": "bangladesh",
    "bhu": "bhutan", "brn": "brunei", "cam": "cambodia",
    "chn": "china", "tpe": "chinese_taipei", "tim": "east_timor",
    "hkg": "hong_kong", "ind": "india", "ina": "indonesia",
    "irn": "iran", "irq": "iraq", "jpn": "japan",
    "jor": "jordan", "kor": "south_korea", "prk": "north_korea",
    "kuw": "kuwait", "kgz": "kyrgyzstan", "lao": "laos",
    "lbn": "lebanon", "mac": "macau", "mas": "malaysia",
    "mdv": "maldives", "mmr": "myanmar", "nep": "nepal",
    "oma": "oman", "pak": "pakistan", "ple": "palestine",
    "phi": "philippines", "qat": "qatar", "ksa": "saudi_arabia",
    "sgp": "singapore", "sri": "sri_lanka", "syr": "syria",
    "tjk": "tajikistan", "tha": "thailand", "tkm": "turkmenistan",
    "are": "united_arab_emirates", "uzb": "uzbekistan",
    "vie": "vietnam", "yem": "yemen",
    # Oceania
    "aus": "australia", "COK": "cook_islands", "fij": "fiji",
    "gum": "guam", "kir": "kiribati", "mhl": "marshall_islands",
    "fsm": "micronesia", "nru": "nauru", "ncl": "new_caledonia",
    "nzl": "new_zealand", "plw": "palau", "png": "papua_new_guinea",
    "tah": "tahiti", "sol": "solomon_islands", "sam": "samoa",
    "tga": "tonga", "tuv": "tuvalu", "van": "vanuatu",
    # Other territories
    "mng": "mongolia",
}

def download(code, name):
    url = f"https://a1.espncdn.com/combiner/i?img=/i/teamlogos/countries/500/{code}.png"
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

items = list(country_map.items())
total = len(items)
done = 0
ok = 0
errors = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = {executor.submit(download, c, n): n for c, n in items}
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
