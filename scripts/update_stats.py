"""Refresh a small, timestamped card using GitHub's public REST API."""
from pathlib import Path
from urllib.request import Request, urlopen
import os, json
from datetime import datetime, timezone

def get(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'leemaxyum-profile'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/'+path, headers=headers), timeout=30) as response:
        return json.load(response)

user = get('users/leemaxyum')
repos=[]
for page in range(1, 100):
    batch=get(f'users/leemaxyum/repos?per_page=100&page={page}')
    repos.extend(batch)
    if len(batch)<100: break
stars=sum(r['stargazers_count'] for r in repos if not r['fork'])
date=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="145" viewBox="0 0 495 145" role="img" aria-labelledby="title desc">
<title id="title">GitHub public statistics</title><desc id="desc">{user['public_repos']} public repositories, {stars} stars on owned non-fork repositories, {user['followers']} followers. Snapshot {date}.</desc>
<rect width="495" height="145" rx="6" fill="#080808"/>
<g font-family="monospace" fill="#aaa"><text x="22" y="28" font-size="12">PUBLIC SIGNAL / LEEMAXYUM</text>
<g fill="#eee" font-size="28"><text x="22" y="74">{user['public_repos']}</text><text x="186" y="74">{stars}</text><text x="345" y="74">{user['followers']}</text></g>
<g font-size="11"><text x="22" y="95">PUBLIC REPOS</text><text x="186" y="95">REPO STARS</text><text x="345" y="95">FOLLOWERS</text><text x="22" y="126" fill="#777">SNAPSHOT / {date}</text></g></g></svg>'''
(Path(__file__).resolve().parents[1]/'assets/github-stats.svg').write_text(svg,encoding='utf-8')
print(f'Statistics refreshed: {date}')
