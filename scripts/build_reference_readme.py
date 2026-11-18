"""Draw original dark developer-profile graphics matching a GitHub README reference.

The README can host images and links, but cannot theme GitHub's own sidebar.
Counts are engineering evidence from repository tests, not GitHub activity.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parents[1]/"assets"
OUT.mkdir(exist_ok=True)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BACK=(13,17,23)
CHARCOAL=(51,52,54)
WHITE=(244,248,251)
DIM=(170,184,197)
MINT=(35,188,174)
EDGE=(65,82,97)

def face(sz,bold=False,mono=False):
    return ImageFont.truetype(FM if mono else (FB if bold else F),sz)

def center(d,x,y,text,font,fill):
    box=d.textbbox((0,0),text,font=font)
    d.text((x-(box[2]-box[0])/2,y),text,font=font,fill=fill)

def pill(d,xy,text,color):
    d.rounded_rectangle(xy,radius=11,fill=(28,40,51),outline=(61,83,94),width=2)
    x0,y0,x1,y1=xy
    center(d,(x0+x1)/2,y0+11,text,face(15,bold=True),color)

def background(w,h):
    im=Image.new("RGB",(w,h),BACK)
    return im

def hero_frame(i,total=26):
    W,H=1200,425
    im=background(W,H)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,10,W-11,H-11),radius=17,fill=CHARCOAL,outline=(63,73,80),width=2)
    d.text((55,43),"AI / ENGINEERING PROFILE",font=face(15,mono=True),fill=(137,175,184))
    d.text((55,76),"Generative AI Engineer",font=face(61,bold=True),fill=WHITE)
    d.text((57,152),"Neeli Yaswanth Kumar",font=face(29),fill=(207,225,231))
    d.text((58,194),"Python Backend  /  RAG  /  Agentic AI  /  MCP",font=face(20),fill=(190,201,211))
    techs=[
        ("Py","PYTHON",(85,161,229)),("F","FASTAPI",(66,216,176)),
        ("LG","LANGGRAPH",(172,154,242)),("R","RAG",(230,186,79)),
        ("M","MCP",(95,211,217)),("AZ","AZURE",(95,149,238)),
        ("D","DOCKER",(107,186,242)),
    ]
    for j,(icon,name,color) in enumerate(techs):
        left=56+j*125
        d.rounded_rectangle((left,244,left+44,288),radius=8,fill=(35,44,54),outline=color,width=2)
        center(d,left+22,253,icon,face(15,bold=True),color)
        center(d,left+47,300,name,face(11,mono=True),WHITE)
    d.line((56,340,908,340),fill=(88,99,103),width=1)
    d.ellipse((59,363,88,392),fill=(22,160,151))
    center(d,74,367,"@",face(16,bold=True),WHITE)
    d.text((101,366),"kyaswanthneeli-stack.github.io",font=face(17),fill=(207,222,227))
    d.ellipse((519,363,548,392),fill=(22,160,151))
    center(d,534,367,"@",face(16,bold=True),WHITE)
    d.text((562,366),"kyaswanthneeli@gmail.com",font=face(17),fill=(207,222,227))
    # Animated star cluster and an original abstract geometric branch, matching the reference feel.
    t=2*math.pi*i/total
    cx,cy=1065,99
    for j,(ox,oy,sz) in enumerate(((0,0,20),(-47,-27,11),(32,25,10))):
        q=0.85+0.18*math.cos(t+j*2)
        r=sz*q
        x=cx+ox;y=cy+oy
        d.polygon([(x,y-r),(x+r*.35,y-r*.35),(x+r,y),(x+r*.35,y+r*.35),(x,y+r),(x-r*.35,y+r*.35),(x-r,y),(x-r*.35,y-r*.35)],fill=(24,170,156))
    for step in range(4):
        x=1052+step*17;y=263+step*25
        d.polygon([(x,y),(x+35,y+16),(x+21,y+34),(x-12,y+18)],outline=(35,101,83),width=3)
        d.line((x+8,y+7,x+21,y+34),fill=(32,117,93),width=2)
    return im

def save_hero():
    frames=[hero_frame(i) for i in range(26)]
    dest=OUT/"profile-reference-animated.gif"
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=145,
                   loop=0,disposal=2,optimize=True)
    print("HERO",dest, dest.stat().st_size)

def save_skills():
    W,H=1200,161
    im=background(W,H);d=ImageDraw.Draw(im)
    d.rounded_rectangle((11,9,W-12,H-10),radius=15,fill=(25,31,40),outline=EDGE,width=2)
    d.text((34,19),"TECH STACK // CORE TOOLS",font=face(16,mono=True),fill=(139,207,205))
    names=[
        ("Python",(89,162,233)),("FastAPI",(69,209,173)),
        ("LangGraph",(177,155,238)),("LangChain",(183,210,124)),
        ("RAG",(220,181,96)),("MCP",(83,216,207)),
        ("Azure",(106,158,239)),("Docker",(100,176,240))]
    for j,(name,c) in enumerate(names):
        x=31+j*144
        pill(d,(x,67,x+136,129),name,c)
    dest=OUT/"profile-reference-skills.png"
    im.save(dest,optimize=True)
    print("SKILLS",dest, dest.stat().st_size)

def save_stats():
    W,H=1200,363
    im=background(W,H);d=ImageDraw.Draw(im)
    d.rounded_rectangle((9,9,W-10,H-10),radius=16,fill=(14,18,26),outline=(49,65,85),width=2)
    d.rounded_rectangle((22,22,570,342),radius=12,fill=(26,34,48),outline=(52,67,90),width=2)
    d.rounded_rectangle((583,22,1177,342),radius=12,fill=(26,34,48),outline=(52,67,90),width=2)
    d.text((49,45),"Neeli Yaswanth Kumar's Engineering Stats",font=face(19,bold=True),fill=(184,207,245))
    rows=[
        ("Documented tests in CI", "44",(143,212,198)),
        ("Featured Python projects","03",(153,187,254)),
        ("Verified hosted APIs","02",(190,157,244)),
        ("CodeAtlas MCP tools","05",(133,216,189)),
    ]
    for i,(name,value,color) in enumerate(rows):
        y=100+i*47
        d.text((49,y),name,font=face(17),fill=(185,205,221))
        d.text((490,y-2),value,font=face(19,bold=True),fill=color)
    d.text((49,305),"No fabricated GitHub stars, commits or followers",font=face(13),fill=(113,139,158))
    stats=[("02","LIVE APIs",(120,207,244)),("44","TESTS",(169,152,250)),("03","PROJECTS",(110,228,187))]
    for i,(n,label,color) in enumerate(stats):
        cx=680+i*191
        d.ellipse((cx-58,111,cx+58,227),outline=(64,91,119),width=6)
        # Arc segments to resemble the clean reference's circular metrics.
        d.arc((cx-58,111,cx+58,227),35,285,fill=color,width=7)
        center(d,cx,141,n,face(40,bold=True),color)
        center(d,cx,250,label,face(15,bold=True,mono=True),(191,210,227))
    d.text((610,50),"ENGINEERING DASHBOARD",font=face(20,bold=True),fill=(184,207,245))
    d.text((616,309),"Verified projects, not live contribution statistics",font=face(13),fill=(128,151,172))
    dest=OUT/"profile-reference-stats.png"
    im.save(dest,optimize=True)
    print("STATS",dest, dest.stat().st_size)

if __name__=="__main__":
    save_hero()
    save_skills()
    save_stats()
