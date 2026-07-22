import os, json

base_dir = os.path.dirname(os.path.abspath(__file__))

team_ids = sorted([f.replace(".png", "") for f in os.listdir(os.path.join(base_dir, "team")) if f.endswith(".png")])
league_ids = sorted([f.replace(".png", "") for f in os.listdir(os.path.join(base_dir, "league")) if f.endswith(".png")])
country_names = sorted([f.replace(".png", "") for f in os.listdir(os.path.join(base_dir, "country")) if f.endswith(".png")])
cricket_names = sorted([f.replace(".png", "") for f in os.listdir(os.path.join(base_dir, "cricket")) if f.endswith(".png")])

mapping_path = os.path.join(base_dir, "mapping.json")
team_names = {}
league_names = {}
if os.path.exists(mapping_path):
    with open(mapping_path) as f:
        mapping = json.load(f)
        team_names = mapping.get("teams", {})
        league_names = mapping.get("leagues", {})

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FotMob Images - Logo Browser</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f0f; color: #e0e0e0; min-height: 100vh; }
.container { max-width: 1400px; margin: 0 auto; padding: 20px; }
h1 { font-size: 24px; margin-bottom: 8px; color: #fff; }
.subtitle { color: #888; margin-bottom: 24px; font-size: 14px; }
.search-bar { display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
.search-bar input { flex: 1; min-width: 200px; padding: 10px 16px; border: 1px solid #333; border-radius: 8px; background: #1a1a1a; color: #e0e0e0; font-size: 14px; }
.search-bar input:focus { outline: none; border-color: #555; }
.search-bar select { padding: 10px 16px; border: 1px solid #333; border-radius: 8px; background: #1a1a1a; color: #e0e0e0; font-size: 14px; }
.tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.tab { padding: 8px 20px; border: 1px solid #333; border-radius: 8px; cursor: pointer; background: #1a1a1a; color: #888; font-size: 14px; }
.tab.active { background: #333; color: #fff; border-color: #555; }
.stats { color: #666; font-size: 13px; margin-bottom: 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 12px; }
.card { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 12px; text-align: center; transition: border-color 0.2s; }
.card:hover { border-color: #555; }
.card img { width: 64px; height: 64px; object-fit: contain; display: block; margin: 0 auto 8px; }
.card .name { font-size: 11px; color: #aaa; word-break: break-all; line-height: 1.3; }
.card .id { font-size: 10px; color: #555; margin-top: 4px; }
.card .copy-link { display: block; font-size: 10px; color: #666; cursor: pointer; margin-top: 4px; text-decoration: none; }
.card .copy-link:hover { color: #4a9eff; text-decoration: underline; }
.no-results { text-align: center; padding: 40px; color: #666; font-size: 16px; }
</style>
</head>
<body>
<div class="container">
  <h1>FotMob Images</h1>
  <p class="subtitle">Browse team logos, league logos, country flags, and cricket logos</p>

  <div class="search-bar">
    <input type="text" id="search" placeholder="Search by name or ID..." oninput="filter()">
    <select id="category" onchange="filter()">
      <option value="all">All</option>
      <option value="team">Teams</option>
      <option value="league">Leagues</option>
      <option value="country">Countries</option>
      <option value="cricket">Cricket</option>
    </select>
  </div>

  <div class="tabs">
    <div class="tab active" data-cat="all" onclick="switchTab('all',this)">All</div>
    <div class="tab" data-cat="team" onclick="switchTab('team',this)">Teams</div>
    <div class="tab" data-cat="league" onclick="switchTab('league',this)">Leagues</div>
    <div class="tab" data-cat="country" onclick="switchTab('country',this)">Countries</div>
    <div class="tab" data-cat="cricket" onclick="switchTab('cricket',this)">Cricket</div>
  </div>

  <div class="stats" id="stats"></div>
  <div class="grid" id="grid"></div>
</div>

<script>
const TEAM_IDS = __TEAM_IDS__;
const LEAGUE_IDS = __LEAGUE_IDS__;
const COUNTRY_NAMES = __COUNTRY_NAMES__;
const CRICKET_NAMES = __CRICKET_NAMES__;
const TEAM_NAMES = __TEAM_NAMES__;
const LEAGUE_NAMES = __LEAGUE_NAMES__;

let currentTab = 'all';

function formatName(name) {
  return name.replace(/_/g, ' ').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function getItems() {
  const q = document.getElementById('search').value.toLowerCase().trim();
  const cat = document.getElementById('category').value;
  const tab = currentTab;
  let items = [];

  const addItems = (ids, type, namesMap) => {
    for (const id of ids) {
      const name = namesMap[id] || '';
      const searchStr = `${id} ${name}`.toLowerCase();
      if (q && !searchStr.includes(q)) continue;
      const itemName = name || id;
      const displayName = (type === 'country' || type === 'cricket') ? formatName(id) : (name || `ID: ${id}`);
      items.push({ id, type, name: itemName, displayName });
    }
  };

  if ((tab === 'all' || tab === 'team') && (cat === 'all' || cat === 'team'))
    addItems(TEAM_IDS, 'team', TEAM_NAMES);
  if ((tab === 'all' || tab === 'league') && (cat === 'all' || cat === 'league'))
    addItems(LEAGUE_IDS, 'league', LEAGUE_NAMES);
  if ((tab === 'all' || tab === 'country') && (cat === 'all' || cat === 'country'))
    addItems(COUNTRY_NAMES, 'country', {});
  if ((tab === 'all' || tab === 'cricket') && (cat === 'all' || cat === 'cricket'))
    addItems(CRICKET_NAMES, 'cricket', {});

  return items;
}

function render() {
  const items = getItems();
  const grid = document.getElementById('grid');
  const stats = document.getElementById('stats');

  if (items.length === 0) {
    grid.innerHTML = '<div class="no-results">No logos found</div>';
    stats.textContent = '0 results';
    return;
  }

  stats.textContent = `${items.length} result${items.length !== 1 ? 's' : ''}`;

  grid.innerHTML = items.map(item => {
    const src = item.type === 'team' ? `team/${item.id}.png`
      : item.type === 'league' ? `league/${item.id}.png`
      : item.type === 'country' ? `country/${item.name}.png`
      : `cricket/${item.name}.png`;
    const displayName = item.type === 'team' || item.type === 'league'
      ? (item.displayName || `ID: ${item.id}`)
      : formatName(item.name);
    return `<div class="card">
      <img src="${src}" alt="${displayName}" loading="lazy" onerror="this.style.display='none'">
      <div class="name">${displayName}</div>
      <div class="id">${item.type}${item.type === 'team' || item.type === 'league' ? ' #' + item.id : ''}</div>
      <a class="copy-link" onclick="copyUrl('${src}', event)" href="#">Copy URL</a>
    </div>`;
  }).join('');
}

function copyUrl(src, event) {
  event.preventDefault();
  const url = window.location.origin + '/' + src;
  navigator.clipboard.writeText(url).then(() => {
    const link = event.target;
    const orig = link.textContent;
    link.textContent = 'Copied!';
    setTimeout(() => link.textContent = orig, 1500);
  });
}

function filter() {
  render();
}

function switchTab(tab, el) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  document.getElementById('category').value = 'all';
  render();
}

render();
</script>
</body>
</html>'''

html = html.replace("__TEAM_IDS__", json.dumps(team_ids))
html = html.replace("__LEAGUE_IDS__", json.dumps(league_ids))
html = html.replace("__COUNTRY_NAMES__", json.dumps(country_names))
html = html.replace("__CRICKET_NAMES__", json.dumps(cricket_names))
html = html.replace("__TEAM_NAMES__", json.dumps(team_names))
html = html.replace("__LEAGUE_NAMES__", json.dumps(league_names))

with open(os.path.join(base_dir, "index.html"), "w") as f:
    f.write(html)

print(f"Generated index.html with {len(team_ids)} teams, {len(league_ids)} leagues, {len(country_names)} countries, {len(cricket_names)} cricket logos")
