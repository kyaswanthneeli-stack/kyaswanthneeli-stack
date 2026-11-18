"""Render refined, accurate GitHub-compatible portfolio visuals.

Visual system: midnight navy #091421, cloud white #F3F7FD, mint #69E6CA,
ice blue #84BFFF, and restrained lavender #B5A8F8. All animation is GIF,
because GitHub profile READMEs disallow JavaScript and dynamic CSS.
No model calls, fake GitHub stats or unverifiable performance metrics.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets"
OUT.mkdir(exist_ok=True)
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG = (9, 20, 33)
PANEL = (20, 39, 57)
PANEL2 = (26, 49, 68)
WHITE = (243, 248, 254)
SOFT = (180, 202, 221)
MUTED = (132, 163, 187)
MINT = (105, 230, 202)
ICE = (132, 191, 255)
LAVENDER = (181, 168, 248)
LINE = (55, 94, 116)

def font(size, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else REGULAR, size)

def txt(draw,xy,s,size,color=WHITE,bold=False,mono=False):
    draw.text(xy,s,font=font(size,bold=bold,mono=mono),fill=color)

def centered(draw,cx,y,s,size,color=WHITE,bold=False,mono=False):
    face=font(size,bold=bold,mono=mono)
    bbox=draw.textbbox((0,0),s,font=face)
    draw.text((cx-(bbox[2]-bbox[0])/2,y),s,font=face,fill=color)

def rounded(d,box,fill=PANEL,r=14,stroke=LINE,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=stroke,width=width)

def base(w,h):
    im=Image.new("RGB",(w,h))
    d=ImageDraw.Draw(im)
    for y in range(h):
        q=y/max(1,h-1)
        d.line((0,y,w,y),fill=(round(8+5*q),round(18+12*q),round(32+17*q)))
    return im

def bloom(im,x,y,rgb,rad=125,opacity=70):
    overlay=Image.new("RGBA",im.size)
    ImageDraw.Draw(overlay).ellipse((x-rad,y-rad,x+rad,y+rad),fill=(*rgb,opacity))
    overlay=overlay.filter(ImageFilter.GaussianBlur(rad/2.6))
    im.paste(overlay,(0,0),overlay)

def thin_grid(d,w,h):
    for x in range(21,w,36):
        for y in range(18,h,36):
            if (x+y)//36%3==0:
                d.ellipse((x,y,x+1,y+1),fill=(40,68,84))

def ellipse_points(cx,cy,rx,ry,rotation,steps=95):
    result=[]
    for i in range(steps+1):
        a=math.tau*i/steps
        x,y=rx*math.cos(a),ry*math.sin(a)
        result.append((cx+x*math.cos(rotation)-y*math.sin(rotation),
                       cy+x*math.sin(rotation)+y*math.cos(rotation)))
    return result

def hud(d,x,y,name,detail,color):
    rounded(d,(x,y,x+152,y+74),(20,43,61),12,(61,112,127),2)
    d.line((x+13,y+17,x+44,y+17),fill=color,width=3)
    txt(d,(x+13,y+25),name,12,color,mono=True)
    txt(d,(x+13,y+47),detail,11,SOFT)

def hero_frame(index,n=28):
    w,h=1280,410
    t=math.tau*index/n
    im=base(w,h)
    bloom(im,1046+int(13*math.sin(t)),201,MINT,202,75)
    bloom(im,1187,73,LAVENDER,116,46)
    bloom(im,275,392,ICE,189,37)
    d=ImageDraw.Draw(im)
    thin_grid(d,w,h)
    rounded(d,(1,1,w-2,h-2),fill=None,r=22,stroke=(63,101,120),width=2)
    d.line((30,61,1250,61),fill=(43,79,99),width=1)
    d.ellipse((31,25,40,34),fill=MINT)
    txt(d,(49,22),"NYK   //   AI SYSTEMS ENGINEERING",15,MINT,mono=True)
    txt(d,(594,23),"BUILT  •  TESTED  •  DEMONSTRABLE",12,MUTED,mono=True)
    txt(d,(42,91),"Generative AI",65,WHITE,bold=True)
    txt(d,(39,171),"Engineer",82,MINT,bold=True)
    txt(d,(44,273),"NEELI YASWANTH KUMAR",22,WHITE,bold=True)
    txt(d,(45,310),"Python  ·  FastAPI  ·  RAG  ·  MCP  ·  Agent workflows",16,SOFT)
    rounded(d,(42,347,242,383),(20,53,58),17,(65,133,125))
    rounded(d,(253,347,419,383),(23,47,74),17,(70,109,152))
    rounded(d,(430,347,626,383),(38,38,69),17,(102,96,154))
    txt(d,(63,356),"LOCAL MCP TOOL",13,MINT,mono=True)
    txt(d,(278,356),"2 HOSTED APIs",13,ICE,mono=True)
    txt(d,(453,356),"53 CI TESTS",13,LAVENDER,mono=True)
    # Airy central orb: conceptual engineering graphic, not a live trace.
    cx=1043
    cy=198+int(7*math.sin(t))
    for radius,color in ((129,(43,106,129)),(103,(46,116,134)),(76,(41,98,117))):
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=color,width=2)
    for rotation,color in [(-.37,MINT),(.63,ICE),(1.45,LAVENDER)]:
        pts=ellipse_points(cx,cy,158,53,rotation)
        d.line(pts,fill=color,width=2,joint="curve")
    for j in range(10):
        a=math.tau*j/10+t*.20
        x,y=cx+73*math.cos(a),cy+62*math.sin(a)
        d.line((cx,cy,x,y),fill=(48,106,125),width=1)
        d.ellipse((x-2,y-2,x+2,y+2),fill=ICE if j%2 else MINT)
    # Layered low-poly brain/glass glyph.
    nodes=[(-36,-16),(-23,-39),(12,-36),(38,-13),(36,26),(6,45),(-29,31)]
    coords=[(cx+x,cy+y) for x,y in nodes]
    d.line(coords+[coords[0]],fill=(148,244,230),width=3,joint="curve")
    for a,b in [(0,3),(1,4),(2,6),(3,5)]:
        d.line((*coords[a],*coords[b]),fill=(90,171,188),width=2)
    for x,y in coords:
        d.ellipse((x-3,y-3,x+3,y+3),fill=MINT)
    txt(d,(cx-16,cy-13),"AI",23,WHITE,bold=True)
    for phase,rad,color in ((0,151,MINT),(2.2,145,ICE),(4.4,155,LAVENDER)):
        x=cx+rad*math.cos(t+phase)
        y=cy+48*math.sin(t+phase)
        d.ellipse((x-5,y-5,x+5,y+5),fill=color)
    hud(d,784,94+round(7*math.sin(t)),"CODE INTEL","AST / SQLite",MINT)
    hud(d,1102,82+round(6*math.sin(t+2)),"AGENT POLICY","Checks / Approval",ICE)
    hud(d,1102,287+round(6*math.sin(t+4)),"ROUTEWISE","Heuristic / Demo",LAVENDER)
    d.ellipse((891,329,1184,367),outline=(53,134,151),width=2)
    d.ellipse((936,340,1141,362),outline=MINT,width=2)
    for col in range(9,w,22):
        a=col/61
        y=385+math.sin(a+t)*5
        d.ellipse((col,y,col+2,y+2),fill=(38,104,106))
    return im

def save_hero():
    imgs=[hero_frame(i) for i in range(28)]
    target=OUT/"floating-hero-v2.gif"
    imgs[0].save(target,save_all=True,append_images=imgs[1:],duration=110,
                 loop=0,optimize=True,disposal=2)
    print("hero",target.name,target.stat().st_size)

PROJECTS=[
    ("codeatlas", "01  /  SOURCE CODE INTELLIGENCE","CodeAtlas MCP",
     "AST index  ·  static call candidates", ["PARSE PYTHON","BUILD INDEX","QUERY MCP"],
     MINT,"LOCAL MCP TOOL / SAMPLE BROWSER GRAPH"),
    ("agentgate", "02  /  AGENT TOOL POLICY","AgentGate",
     "Allowlist  ·  redaction  ·  approvals", ["REQUEST","POLICY CHECK","DEMO TOOL"],
     ICE,"HOSTED API / SIMULATED TOOL ADAPTERS"),
    ("routewise", "03  /  MODEL REQUEST ROUTING","RouteWise",
     "Heuristic routing  ·  retryable failover", ["PROMPT","SELECT ROUTE","FALLBACK"],
     LAVENDER,"HOSTED API / NO-PROVIDER DEMO"),
]

def card_frame(spec,i,frames=22):
    slug,head,title,description,nodes,color,scope=spec
    t=math.tau*i/frames
    im=base(520,282)
    bloom(im,444,74,color,105,60)
    d=ImageDraw.Draw(im)
    thin_grid(d,520,282)
    rounded(d,(2,2,518,280),(15,33,48),r=18,stroke=(62,103,125),width=2)
    txt(d,(21,19),head,12,color,mono=True)
    txt(d,(19,57),title,34,WHITE,bold=True)
    txt(d,(21,112),description,15,SOFT)
    d.line((20,148,498,148),fill=LINE,width=1)
    for j,label in enumerate(nodes):
        x=19+j*169
        y=159+round(3*math.sin(t+j*1.3))
        rounded(d,(x,y,x+153,y+52),(25,50,69),11,(59,107,132))
        centered(d,x+76,y+17,label,12,color,mono=True)
        if j<2:
            d.line((x+154,y+26,x+166,y+26),fill=color,width=2)
    txt(d,(21,240),scope,11,MUTED,mono=True)
    # The signals animate; accurately conceptual, no fake live data.
    x=24+466*i/(frames-1)
    d.line((21,268,499,268),fill=(45,84,99),width=2)
    d.ellipse((x-5,263,x+5,273),fill=color)
    for radius in (15,24,34):
        d.arc((450-radius,88-radius,450+radius,88+radius),
              (i*13)%360,(i*13+260)%360 if (i*13+260)<360 else (i*13+260),
              fill=color,width=2)
    return im

def save_cards():
    for spec in PROJECTS:
        frames=[card_frame(spec,i) for i in range(22)]
        target=OUT/(spec[0]+"-v2.gif")
        frames[0].save(target,save_all=True,append_images=frames[1:],
                       duration=125,loop=0,optimize=True,disposal=2)
        print("card",target.name,target.stat().st_size)

def save_metrics():
    im=base(1280,228)
    bloom(im,1000,190,ICE,165,55)
    d=ImageDraw.Draw(im)
    items=[("03","FEATURED SYSTEMS",MINT),
           ("02","HOSTED DEMO APIs",ICE),
           ("53","AUTOMATED TESTS",LAVENDER),
           ("05","LOCAL MCP TOOLS",MINT)]
    for i,(number,label,color) in enumerate(items):
        x=8+319*i
        rounded(d,(x,7,x+305,218),(19,41,58),18,(58,99,119),2)
        d.line((x+22,33,x+87,33),fill=color,width=4)
        txt(d,(x+22,55),number,79,color,bold=True)
        txt(d,(x+22,161),label,15,WHITE,mono=True)
        txt(d,(x+22,191),"PROJECT EVIDENCE  /  NOT STARS",10,MUTED,mono=True)
    target=OUT/"verified-metrics-v2.png"
    im.save(target,optimize=True)
    print("metrics",target.name,target.stat().st_size)

def save_system_strip():
    im=base(1280,128)
    d=ImageDraw.Draw(im)
    rounded(d,(2,2,1278,126),(16,35,51),17,(50,94,113),2)
    items=[
        ("01", "CodeAtlas", "LOCAL MCP", MINT),
        ("02", "AgentGate", "HOSTED DEMO", ICE),
        ("03", "RouteWise", "HOSTED DEMO", LAVENDER)
    ]
    for i,(number,name,scope,color) in enumerate(items):
        x=23+i*419
        rounded(d,(x,20,x+395,109),(25,48,66),13,(52,94,115))
        txt(d,(x+17,39),number,32,color,bold=True,mono=True)
        txt(d,(x+86,39),name,20,WHITE,bold=True)
        txt(d,(x+86,74),scope,12,color,mono=True)
        d.ellipse((x+363,56,x+375,68),fill=color)
    target=OUT/"system-strip-v2.png"
    im.save(target,optimize=True)
    print("strip",target.name,target.stat().st_size)

if __name__ == "__main__":
    save_hero()
    save_cards()
    save_metrics()
    save_system_strip()
