"""Generate a real contribution-calendar SVG from GitHub GraphQL.

Only GitHub's own contributionsCollection data is used. The script fails on
missing data, so the workflow cannot publish invented contribution activity.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

LOGIN="kyaswanthneeli-stack"
OUT=Path("assets/github-contributions.svg")
TOKEN=os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("GITHUB_TOKEN is required")
QUERY="""query($login:String!) {
 user(login:$login) {
   contributionsCollection {
     contributionCalendar {
       totalContributions
       weeks {
         contributionDays { date contributionCount }
       }
     }
   }
 }
}"""
req=urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query":QUERY,"variables":{"login":LOGIN}}).encode(),
    headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+TOKEN,"User-Agent":"NYK-profile-graph","X-GitHub-Api-Version":"2022-11-28"},
)
with urllib.request.urlopen(req,timeout=30) as response:
    result=json.loads(response.read().decode())
if result.get("errors"):
    raise SystemExit("GitHub GraphQL returned errors: "+str(result["errors"]))
user=result.get("data",{}).get("user")
if not user:
    raise SystemExit("GitHub user not found")
data=user["contributionsCollection"]["contributionCalendar"]
weeks=data["weeks"]
if not weeks:
    raise SystemExit("No contribution weeks returned")
W,H=1152,265
CELL=12
GAP=4
OX,OY=53,86
colors=["#1e2733","#0e534b","#127e6c","#26b69a","#79e6cb"]
def color(count):
    if count==0:return colors[0]
    if count<=2:return colors[1]
    if count<=5:return colors[2]
    if count<=10:return colors[3]
    return colors[4]
parts=[
f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Real GitHub contributions for {LOGIN} in the last year: {data["totalContributions"]} contributions">',
'<rect width="100%" height="100%" rx="18" fill="#0d1117"/>',
'<rect x="1" y="1" width="1150" height="263" rx="17" fill="none" stroke="#33404e"/>',
'<text x="35" y="41" fill="#e5edf6" font-family="Arial,sans-serif" font-weight="700" font-size="23">Contribution activity</text>',
f'<text x="1113" y="40" text-anchor="end" fill="#89e8d4" font-family="Arial,sans-serif" font-size="15">{data["totalContributions"]} contributions / last year</text>',
'<text x="35" y="60" fill="#8b9eb1" font-family="Arial,sans-serif" font-size="12">Source: GitHub contribution calendar · updated from GitHub Actions</text>',
]
max_weeks=min(len(weeks),66)
for wi,week in enumerate(weeks[-max_weeks:]):
    for di,day in enumerate(week["contributionDays"]):
        if di>6:continue
        x=OX+wi*(CELL+GAP)
        y=OY+di*(CELL+GAP)
        v=int(day["contributionCount"])
        parts.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color(v)}"><title>{escape(day["date"])}: {v} contributions</title></rect>')
parts.append('<text x="35" y="242" fill="#a4b9c8" font-family="Arial,sans-serif" font-size="12">GitHub public/profile activity, not a fabricated heatmap</text>')
parts.append('<text x="1114" y="242" fill="#a4b9c8" text-anchor="end" font-family="Arial,sans-serif" font-size="12">Less</text>')
for i,c in enumerate(colors):
    parts.append(f'<rect x="{1043+i*14}" y="250" width="9" height="9" fill="{c}"/>')
parts.append('</svg>')
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text("\n".join(parts)+"\n",encoding="utf-8")
print(f"Saved {OUT} with {max_weeks} weeks and total={data['totalContributions']}")
