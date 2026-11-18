"""Render the Cyber AI Command Center GitHub README assets.

This creates original artwork with Pillow. No external images, tracking, model
calls, fabricated GitHub activity, or secret credentials are needed.
All numeric labels are verified engineering portfolio facts, not live analytics.
"""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"assets"
OUT.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG=(7,14,27)
MINT=(119,246,218)
CYAN=(111,196,252)
PURPLE=(175,154,255)
ORANGE=(255,184,124)
WHITE=(240,247,255)
MUTED=(146,172,198)
EDGE=(43,76,105)

def ft(n,bold=False,mono=False):
    return ImageFont.truetype(MONO if mono else (BOLD if bold else FONT),n)

def centered(draw,xy,label,face,fill):
    bounds=draw.textbbox((0,0),label,font=face)
    draw.text((xy[0]-(bounds[2]-bounds[0])/2,xy[1]),label,font=face,fill=fill)

def base(w,h):
    im=Image.new("RGB",(w,h),BG)
    d=ImageDraw.Draw(im)
    for y in range(h):
        q=y/max(1,h-1)
        d.line((0,y,w,y),fill=(int(7+7*q),int(14+15*q),int(27+23*q)))
    for x in range(30,w,45):
        for y in range(20,h,45):
            d.ellipse((x,y,x+2,y+2),fill=(35,62,87))
    return im

def aura(im,x,y,r,c,alpha=120):
    over=Image.new("RGBA",im.size,(0,0,0,0))
    ImageDraw.Draw(over).ellipse((x-r,y-r,x+r,y+r),fill=(*c,alpha))
    blur=over.filter(ImageFilter.GaussianBlur(max(1,r/2.8)))
    im.paste(blur,(0,0),blur)

def pill(d,box,label,tint=MINT,size=15):
    d.rounded_rectangle(box,radius=12,fill=(19,41,60),outline=tuple(int(v*.54) for v in tint),width=2)
    x1,y1,x2,y2=box
    centered(d,((x1+x2)//2,y1+(y2-y1-size)/2-2),label,ft(size,mono=True),tint)

def line(d,points,color=EDGE,width=2):
    d.line(points,fill=color,width=width,joint="curve")

def hero_frame(i,total=24):
    w,h=1200,435
    theta=2*math.pi*i/total
    im=base(w,h)
    aura(im,980,210,250,(29,202,190),115)
    aura(im,350,390,240,(120,85,244),74)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((12,12,w-13,h-13),radius=26,outline=(55,116,131),width=2)
    d.rounded_rectangle((40,34,1160,72),radius=12,fill=(17,37,56),outline=(52,97,113),width=1)
    for j,color in enumerate(((246,143,128),(254,206,119),(105,225,177))):
        x=62+j*20; d.ellipse((x,46,x+9,55),fill=color)
    d.text((155,44),"NYK / AI ENGINEERING COMMAND CENTER",font=ft(16,mono=True),fill=MINT)
    d.text((1040,44),"v2.0  //",font=ft(15,mono=True),fill=PURPLE)
    d.text((59,98),"NEELI YASWANTH",font=ft(56,bold=True),fill=WHITE)
    d.text((54,167),"KUMAR",font=ft(90,bold=True),fill=MINT)
    d.text((60,289),"GENERATIVE AI  /  PYTHON BACKENDS  /  AGENTIC SYSTEMS",font=ft(18,mono=True),fill=(190,218,237))
    pill(d,(59,342,222,384),"MCP • RAG",MINT,16)
    pill(d,(237,342,416,384),"FASTAPI",CYAN,16)
    pill(d,(431,342,660,384),"LIVE API x2",ORANGE,16)
    # Decorative computational ring: visual metaphor, not a live network graph.
    cx,cy=973,222
    for radius,color in ((151,(47,107,134)),(127,(75,137,158)),(98,(48,99,130)),(65,(78,112,137))):
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=color,width=2)
    for k in range(20):
        t=math.pi*2*k/20
        r=160
        a=(cx+int(math.cos(t)*r),cy+int(math.sin(t)*r))
        b=(cx+int(math.cos(t)*(r-10)),cy+int(math.sin(t)*(r-10)))
        d.line((*a,*b),fill=(48,126,143),width=2)
    pts=[]
    for k in range(6):
        a=math.pi*2*k/6+theta*(1 if k%2 else -1)
        radius=105 if k%2 else 123
        pts.append((cx+int(math.cos(a)*radius),cy+int(math.sin(a)*radius)))
    for k in range(6):
        line(d,(*pts[k],*pts[(k+2)%6]),(55,122,139),2)
    for k,(x,y) in enumerate(pts):
        tint=(MINT,CYAN,PURPLE)[k%3]
        d.ellipse((x-8,y-8,x+8,y+8),fill=tint)
        d.ellipse((x-14,y-14,x+14,y+14),outline=tuple(int(v*.6) for v in tint))
    d.rounded_rectangle((921,168,1025,274),radius=22,fill=(10,29,47),outline=MINT,width=3)
    centered(d,(973,196),"{AI}",ft(30,mono=True),WHITE)
    d.text((809,382),"CONCEPTUAL SYSTEM MAP  •  NOT LIVE TELEMETRY",font=ft(12,mono=True),fill=(132,166,189))
    # Scanning line and glowing progress indicator.
    sweep=765+int(399*(i/total))
    d.line((765,397,1164,397),fill=(34,72,95),width=3)
    d.line((max(765,sweep-73),397,sweep,397),fill=MINT,width=4)
    return im

def make_hero():
    frames=[hero_frame(i) for i in range(24)]
    path=OUT/"cyber-command-center.gif"
    frames[0].save(path,save_all=True,append_images=frames[1:],
                   duration=120,loop=0,disposal=2,optimize=True)
    print("HERO",path.stat().st_size)

def make_dashboard():
    w,h=1200,600
    im=base(w,h)
    aura(im,1050,480,240,(73,112,220),65)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((12,12,w-13,h-13),radius=24,outline=(41,92,115),width=2)
    d.text((40,32),"SYS.MONITOR / ENGINEERING EVIDENCE",font=ft(19,mono=True),fill=MINT)
    d.text((40,67),"Verified project capabilities, not fabricated GitHub activity",font=ft(15),fill=MUTED)
    metrics=[
        ("03","FEATURED REPOS",MINT),
        ("02","DEPLOYED APIs",CYAN),
        ("44","DOCUMENTED TESTS",PURPLE),
        ("05","CODEATLAS MCP TOOLS",ORANGE),
    ]
    for j,(number,label,color) in enumerate(metrics):
        x=40+j*287
        d.rounded_rectangle((x,112,x+267,258),radius=18,fill=(17,36,57),outline=(49,91,113),width=2)
        d.rectangle((x+16,129,x+22,160),fill=color)
        d.text((x+37,123),number,font=ft(58,bold=True),fill=color)
        d.text((x+19,213),label,font=ft(13,mono=True),fill=(189,217,228))
    d.text((40,292),"WORKFLOW TOPOLOGY  /  PORTFOLIO DOMAINS",font=ft(17,mono=True),fill=MINT)
    nodes=[
        ("01", "CODE CONTEXT","AST • SQLITE",MINT),
        ("02", "TOOL POLICY","APPROVALS",CYAN),
        ("03", "MODEL ROUTING","FAILOVER",ORANGE),
    ]
    centers=[214,598,982]
    for j,(n,heading,subtitle,c) in enumerate(nodes):
        cx=centers[j]
        x0=cx-170;x1=cx+170
        d.rounded_rectangle((x0,336,x1,502),radius=19,fill=(15,34,54),outline=tuple(int(v*.7) for v in c),width=2)
        d.rounded_rectangle((x0+15,351,x0+69,382),radius=9,fill=(24,54,68))
        centered(d,(x0+42,356),n,ft(16,mono=True),c)
        centered(d,(cx,393),heading,ft(23,bold=True),WHITE)
        centered(d,(cx,448),subtitle,ft(16,mono=True),c)
    for a,b in ((384,426),(768,810)):
        d.line((a,415,b,415),fill=(89,174,172),width=4)
        d.polygon([(b-10,406),(b,415),(b-10,424)],fill=MINT)
    d.text((41,541),"API STATUS  /  DEPLOYED SERVICES REQUIRE AUTHENTICATION FOR PROTECTED CALLS",font=ft(13,mono=True),fill=MUTED)
    d.text((41,568),"PROJECTS ARE SEPARATE IMPLEMENTATIONS; CONNECTORS ABOVE ARE A VISUAL CATEGORY MAP.",font=ft(12,mono=True),fill=(112,151,174))
    path=OUT/"cyber-system-dashboard.png"
    im.save(path,optimize=True)
    print("DASH",path.stat().st_size)

def make_skill_matrix():
    w,h=1200,356
    im=base(w,h)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((12,12,1188,344),radius=25,outline=(42,88,106),width=2)
    d.text((43,32),"TECH.STACK / CORE CAPABILITIES",font=ft(19,mono=True),fill=MINT)
    d.text((43,68),"Backend engineering  •  retrieval  •  agent tooling  •  delivery",font=ft(16),fill=MUTED)
    groups=[
        ("BACKEND",("PYTHON","FASTAPI","REST APIs","SQL"),MINT),
        ("GEN AI",("RAG","LANGGRAPH","MCP","LLM APIs"),PURPLE),
        ("DATA / CLOUD",("AZURE","BIGQUERY","VECTOR SEARCH","DOCKER"),CYAN),
    ]
    for i,(title,items,c) in enumerate(groups):
        x=40+390*i
        d.rounded_rectangle((x,117,x+365,309),radius=18,fill=(17,36,56),outline=(46,88,111),width=2)
        d.line((x+19,164,x+339,164),fill=(45,81,106),width=1)
        d.text((x+22,132),title,font=ft(18,mono=True),fill=c)
        for k,label in enumerate(items):
            col=k%2;row=k//2
            left=x+20+col*172;top=181+row*56
            d.rounded_rectangle((left,top,left+158,top+43),radius=11,fill=(28,53,73),outline=(55,91,113),width=1)
            centered(d,(left+79,top+11),label,ft(12,mono=True),WHITE)
    path=OUT/"cyber-tech-matrix.png"
    im.save(path,optimize=True)
    print("SKILL",path.stat().st_size)

def make_project_tiles():
    spec=[
        ("codeatlas","CODEATLAS","MCP / CODE CONTEXT",MINT,
         ("AST PARSER","SQLITE","MCP"),"Local tool • static call graph"),
        ("agentgate","AGENTGATE","AGENT POLICY API",CYAN,
         ("REQUEST","GUARD","APPROVAL"),"Live API • demo tool adapters"),
        ("routewise","ROUTEWISE","LLM ROUTING API",ORANGE,
         ("PROMPT","ROUTE","FALLBACK"),"Live API • no-provider demo"),
    ]
    w,h=750,370
    for name,title,subtitle,accent,flow,caveat in spec:
        im=base(w,h)
        aura(im,620,112,155,accent,87)
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((9,9,w-10,h-10),radius=22,outline=tuple(int(v*.68) for v in accent),width=3)
        d.rounded_rectangle((32,32,377,67),radius=11,fill=(20,46,64))
        d.text((45,40),subtitle,font=ft(17,mono=True),fill=accent)
        d.text((31,89),title,font=ft(49,bold=True),fill=WHITE)
        # Visual pipeline within the card.
        d.rounded_rectangle((31,180,720,271),radius=16,fill=(14,32,50),outline=(52,87,112),width=2)
        for j,node in enumerate(flow):
            x=49+j*222
            d.rounded_rectangle((x,203,x+187,249),radius=11,fill=(27,52,73),outline=(65,113,133),width=1)
            centered(d,(x+93,216),node,ft(15,mono=True),accent)
            if j!=2:
                d.line((x+187,227,x+211,227),fill=accent,width=2)
        d.text((37,315),caveat,font=ft(17),fill=MUTED)
        path=OUT/(name+"-cyber.png")
        im.save(path,optimize=True)
        print("CARD",path.name,path.stat().st_size)

if __name__=="__main__":
    make_hero()
    make_dashboard()
    make_skill_matrix()
    make_project_tiles()
