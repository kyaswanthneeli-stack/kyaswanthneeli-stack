"""Render a factual public GitHub activity heatmap from GitHub REST public events.

Not an official contribution calendar. Shows public push events in a recent
30-day window; missing or private events are not represented as contributions.
"""
import json
import urllib.request
from collections import Counter
from datetime import date, timedelta, datetime, timezone
from html import escape
from pathlib import Path

LOGIN="kyaswanthneeli-stack"
OUT=Path("assets/github-contributions.svg")
url=f"https://api.github.com/users/{LOGIN}/events/public?per_page=100"
req=urllib.request.Request(url,headers={
  "Accept":"application/vnd.github+json",
  "User-Agent":"NYK-github-activity-graph",
  "X-GitHub-Api-Version":"2022-11-28"
})
with urllib.request.urlopen(req,timeout=30) as response:
    events=json.loads(response.read().decode("utf-8"))
if not isinstance(events,list):
    raise SystemExit("GitHub REST public events did not return an array")
today=datetime.now(timezone.utc).date()
first=today-timedelta(days=34)
days=[first+timedelta(days=i) for i in range(35)]
counts=Counter()
for event in events:
    if event.get("type")!="PushEvent":
        continue
    parsed=date.fromisoformat(event["created_at"][:10])
    if first<=parsed<=today:
        counts[parsed]+=1
total=sum(counts.values())
W,H=1120,240
ox,oy=230,78
cell=23;gap=5
colors=["#1c2836","#155549","#197b68","#27b498","#80edd1"]
def color(n):
    return colors[0] if n==0 else colors[min(4,n)]
p=[
f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Recent public push events from GitHub: {total} in the last 35 days">',
'<rect width="100%" height="100%" rx="18" fill="#0d1117"/>',
'<rect x="1" y="1" width="1118" height="238" rx="17" stroke="#34435a" fill="none"/>',
'<text x="35" y="42" fill="#e3ecf6" font-family="Arial,sans-serif" font-size="23" font-weight="700">Public GitHub activity</text>',
'<text x="35" y="67" fill="#9cbbc9" font-family="Arial,sans-serif" font-size="13">Recent public push events, not total contributions</text>',
f'<text x="1060" y="46" fill="#7ee2ce" text-anchor="end" font-family="Arial,sans-serif" font-size="17">{total} pushes / recent 35 days</text>',
]
for i,day in enumerate(days):
    x=ox+(i//7)*(cell+gap)*2 + (i%7)*(cell+gap) # 5 blocks of 7 days, groups visible
    # Instead of GitHub weekly grid, show a clear 35-day horizontal strip with 35 truthful counts.
    x=49+i*29
    y=99
    n=counts.get(day,0)
    p.append(f'<rect x="{x}" y="{y}" width="20" height="62" rx="4" fill="{color(n)}"><title>{day.isoformat()}: {n} public push events</title></rect>')
    if i%7==0:
        p.append(f'<text x="{x}" y="183" fill="#9bb0c5" font-family="Arial,sans-serif" font-size="12">{day.strftime("%d %b")}</text>')
p.append('<text x="35" y="220" fill="#a0b1c2" font-family="Arial,sans-serif" font-size="12">Source: GitHub public Events API · excludes private activity and non-push contribution types</text>')
p.append('</svg>')
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text("\n".join(p)+"\n",encoding="utf-8")
print("Verified public push events:",len(events),"records,",total,"pushes; output",OUT)
