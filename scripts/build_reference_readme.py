"""Generate GitHub-safe reference-style README hero, skill ribbon and verified stat panels.

GitHub owns the surrounding profile page. These assets only decorate its README.
Artwork is original. It uses verified project figures, never fabricated stars or commits.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent.parent
ASSETS=ROOT/"assets"
ASSETS.mkdir(exist_ok=True)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG=(12,17,25)
PANEL=(27,34,43)
INK=(239,245,248)
MUTED=(155,178,189)
TURQ=(89,232,204)
CYAN=(101,192,235)
PURPLE=(177,147,240)
LIME=(180,224,114)

def font(sz,bold=False,mono=False):
    return ImageFont.truetype(FM if mono else (FB if bold else F),sz)

def center(d,x,y,s,ft,color):
    r=d.textbbox((0,0),s,font=ft)
    d.text((x-(r[2]-r[0])/2,y),s,font=ft,fill=color)

def rounded(d,box,fill,outline=None,radius=18,width=1):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def start(w,h):
    im=Image.new("RGB",(w,h),BG)
    d=ImageDraw.Draw(im)
    for y in range(h):
        alpha=y/h
        d.line((0,y,w,y),fill=(int(13+alpha*7),int(18+alpha*10),int(27+alpha*15)))
    for x in range(20,w,40):
        for y in range(20,h,40):
            d.ellipse((x,y,x+1,y+1),fill=(36,53,65))
    return im

def tech_label(d,x,y,w,text,color):
    rounded(d,(x,y,x+w,y+36),(36,45,55),(65,79,91),10)
    center(d,x+w//2,y+8,text,font(15,bold=True),color)

def hero_frame(n,total=26):
    w,h=1200,395
    theta=n*2*math.pi/total
    im=start(w,h)
    d=ImageDraw.Draw(im)
    # Intro panel imitates the crisp premium README card layout in the reference.
    rounded(d,(12,12,1188,383),(29,35,42),(58,75,80),19,2)
    d.text((49,30),"NYK / README.md",font=font(15,mono=True),fill=(143,169,171))
    d.line((48,63,1152,63),fill=(64,85,86),width=2)
    d.text((49,88),"GENERATIVE AI ENGINEER",font=font(42,bold=True),fill=INK)
    d.text((51,147),"NEELI YASWANTH KUMAR",font=font(24),fill=TURQ)
    d.text((50,198),"PYTHON  /  FASTAPI  /  RAG  /  LANGGRAPH  /  MCP  /  AZURE",font=font(17,mono=True),fill=(197,216,221))
    for x,size,name,color in [
        (50,124,"PYTHON",TURQ),(186,130,"FASTAPI",CYAN),(328,96,"RAG",PURPLE),
        (436,154,"LANGGRAPH",LIME),(602,92,"MCP",TURQ),(706,110,"DOCKER",CYAN)]:
        tech_label(d,x,250,size,name,color)
    d.line((49,312,824,312),fill=(61,83,87),width=1)
    d.text((49,334),"BUILDING RAG, AGENT WORKFLOWS & TESTED PYTHON APIs",font=font(15,mono=True),fill=MUTED)
    # Decorative geometric branch with animated small "spark" nodes.
    cx,cy=992,211
    for j in range(4):
        phi=(theta*.6+j*math.pi/2)
        rad=76+j*14
        ax=cx+math.cos(phi)*rad
        ay=cy+math.sin(phi)*rad*.75
        bx=cx+math.cos(phi+2.1)*(rad-14)
        by=cy+math.sin(phi+2.1)*(rad-14)*.75
        d.line((ax,ay,bx,by),fill=(59,126,126),width=3)
    for k in range(3):
        theta0=k*math.tau/3
        points=[]
        for m in range(4):
            a=theta0+m*math.pi/2
            r=108 if m%2 else 85
            points.append((cx+math.cos(a)*r,cy+math.sin(a)*r))
        d.polygon(points,outline=(52,123,105),width=3)
    d.rounded_rectangle((922,153,1062,270),radius=21,fill=(24,51,52),outline=TURQ,width=3)
    center(d,cx,177,"{ AI }",font(31,mono=True),TURQ)
    # One glowing animated dot signals motion, without bright distracting flashes.
    px=cx+142*math.cos(theta)
    py=cy+92*math.sin(theta)
    d.ellipse((px-8,py-8,px+8,py+8),fill=LIME)
    d.ellipse((px-13,py-13,px+13,py+13),outline=(91,175,133),width=2)
    d.text((908,329),"SYSTEMS / 01–03",font=font(14,mono=True),fill=(150,187,176))
    return im

def generate_hero():
    frames=[hero_frame(i) for i in range(26)]
    p=ASSETS/"profile-reference-animated.gif"
    frames[0].save(p,save_all=True,append_images=frames[1:],duration=130,loop=0,disposal=2,optimize=True)
    print("header",p.stat().st_size)

def generate_stats():
    w,h=1200,355
    im=start(w,h);d=ImageDraw.Draw(im)
    rounded(d,(12,12,w-13,h-13),(22,29,39),(58,80,89),19,2)
    d.text((41,32),"ENGINEERING STATS  /  VERIFIED PROJECT EVIDENCE",font=font(18,mono=True),fill=TURQ)
    cards=[(41,81,589,317),(608,81,1158,317)]
    for b in cards:rounded(d,b,(28,40,53),(53,85,96),15,2)
    d.text((64,104),"PROJECT TEST COVERAGE",font=font(17,bold=True),fill=INK)
    breakdown=[("CodeAtlas MCP",16,TURQ),("AgentGate",14,CYAN),("RouteWise",14,PURPLE)]
    for i,(label,count,c) in enumerate(breakdown):
        y=151+i*51
        d.text((65,y),label,font=font(16),fill=(194,213,222))
        rounded(d,(262,y+5,490,y+22),(46,63,75),radius=6)
        rounded(d,(262,y+5,262+int(228*count/16),y+22),c,radius=6)
        d.text((510,y-1),str(count),font=font(19,bold=True),fill=INK)
    d.text((66,288),"44 documented Python tests  |  CI verified",font=font(14,mono=True),fill=MUTED)
    d.text((630,104),"LIVE ENGINEERING SERVICES",font=font(17,bold=True),fill=INK)
    rows=[
        ("AGENTGATE", "PUBLIC API · POLICY SIMULATION",TURQ),
        ("ROUTEWISE", "PUBLIC API · LABELED DEMO MODE",CYAN),
        ("CODEATLAS", "LOCAL MCP · SOURCE + TESTS",PURPLE),
    ]
    for i,(title,detail,c) in enumerate(rows):
        y=150+52*i
        d.ellipse((630,y+8,640,y+18),fill=c)
        d.text((654,y),title,font=font(16,bold=True),fill=c)
        d.text((654,y+23),detail,font=font(12,mono=True),fill=MUTED)
    d.text((630,300),"Not star, follower, contribution or cost metrics.",font=font(12),fill=(137,160,170))
    p=ASSETS/"profile-reference-stats.png"
    im.save(p,optimize=True)
    print("stats",p.stat().st_size)

def generate_skillbar():
    w,h=1200,144
    im=start(w,h);d=ImageDraw.Draw(im)
    rounded(d,(12,12,1187,132),(24,34,43),(54,79,84),16,2)
    techs=[
        ("PY", "Python",TURQ),("API","FastAPI",CYAN),("LG","LangGraph",PURPLE),
        ("RAG","Retrieval",LIME),("MCP","MCP Tools",TURQ),("AZ","Azure",CYAN),
        ("SQL","SQL",PURPLE),("DK","Docker",LIME)
    ]
    for i,(icon,label,c) in enumerate(techs):
        x=30+i*146
        rounded(d,(x,38,x+134,105),(32,45,54),(57,83,91),12)
        rounded(d,(x+8,47,x+43,92),(30,66,69),radius=8)
        center(d,x+25,61,icon,font(12,bold=True,mono=True),c)
        label_sz=12 if len(label)>7 else 14
        d.text((x+50,65),label,font=font(label_sz,bold=True),fill=INK)
    p=ASSETS/"profile-reference-skills.png"
    im.save(p,optimize=True)
    print("skills",p.stat().st_size)

if __name__=="__main__":
    generate_hero()
    generate_stats()
    generate_skillbar()
