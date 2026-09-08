"""Build a self-contained activity chart from GitHub's public contribution calendar."""
from urllib.request import Request, urlopen
from pathlib import Path
from datetime import datetime, timezone
import re, html

with urlopen(Request('https://github.com/users/leemaxyum/contributions', headers={'User-Agent':'leemaxyum-profile'}),timeout=30) as r:
    source=r.read().decode()
dates={}
for tag in re.findall(r'<td\b[^>]+>',source):
    a=dict(re.findall(r'([\w-]+)="([^"]*)"',tag))
    if 'data-date' in a: dates[a['id']]=a['data-date']
days=[]
for tag,body in re.findall(r'<tool-tip\b([^>]+)>(.*?)</tool-tip>',source,re.S):
    a=dict(re.findall(r'([\w-]+)="([^"]*)"',tag)); key=a.get('for')
    if key not in dates: continue
    match=re.match(r'(No|[\d,]+) contributions? on ',html.unescape(body).strip())
    if not match: raise ValueError('Contribution tooltip format changed')
    count=0 if match[1]=='No' else int(match[1].replace(',',''))
    days.append((dates[key],count))
assert len(days)>350, 'Calendar incomplete; preserve the last good chart'
days=sorted(days)[-84:]
weeks=[days[i:i+7] for i in range(0,84,7)]
values=[sum(n for _,n in week) for week in weeks]; top=max(max(values),1)
points=[(45+i*73,155-n/top*90) for i,n in enumerate(values)]
path='M'+' L'.join(f'{x},{y:.2f}' for x,y in points)
stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="215" viewBox="0 0 900 215" role="img" aria-labelledby="title desc">',f'<title id="title">Public activity / twelve weeks</title><desc id="desc">Weekly public contribution counts from {days[0][0]} to {days[-1][0]}: {", ".join(map(str,values))}. Snapshot {stamp} UTC.</desc>','<rect width="900" height="215" rx="6" fill="#080808"/>','<g font-family="monospace" font-size="12" fill="#aaa"><text x="24" y="27">ACTIVITY / 12 WEEKS / PUBLIC CONTRIBUTIONS</text>',f'<text x="24" y="197" fill="#777">{days[0][0]} — {days[-1][0]} · SNAPSHOT {stamp} UTC</text></g>','<path d="M45 155H848M45 110H848M45 65H848" stroke="#252525"/>',f'<path d="{path} L848,155 L45,155Z" fill="#ffffff" opacity=".04"/>',f'<path d="{path}" fill="none" stroke="#bbb" stroke-width="2"/>']
for (x,y),week,value in zip(points,weeks,values):
    svg.append(f'<circle cx="{x}" cy="{y:.2f}" r="3" fill="#eee"><title>{week[0][0]} to {week[-1][0]}: {value} contributions</title></circle><text x="{x}" y="{y-10:.2f}" text-anchor="middle" font-size="11" font-family="monospace" fill="#aaa">{value}</text>')
svg.append('</svg>')
(Path(__file__).resolve().parents[1]/'assets/activity-graph.svg').write_text('\n'.join(svg),encoding='utf-8')
print('Activity graph refreshed from',len(days),'days')
