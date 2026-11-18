"""Generate an original animated GitHub profile: floating AI observatory.

GitHub profile READMEs cannot run JavaScript. The animation therefore lives in
GitHub-compatible GIFs. No invented GitHub statistics or external dependencies
other than Pillow. The images are a conceptual engineering illustration.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

C = {
    "bg": (6, 13, 25), "panel": (14, 29, 47),
    "text": (241, 248, 254), "muted": (167, 191, 211),
    "teal": (104, 248, 220), "cyan": (106, 198, 255),
    "violet": (184, 160, 255), "coral": (255, 180, 151),
    "outline": (51, 84, 109),
}

def ft(n: int, bold=False, mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else REG, n)

def rect(draw, box, fill, radius=13, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def glow(im, x, y, radius, color, alpha=120):
    a = Image.new("RGBA", im.size)
    d = ImageDraw.Draw(a)
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(*color, alpha))
    a = a.filter(ImageFilter.GaussianBlur(max(1, radius//3)))
    im.paste(a, (0, 0), a)

def background(w, h, a=(6,13,25), b=(9,24,44)):
    im=Image.new("RGB",(w,h))
    d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/max(1,h-1)
        d.line((0,y,w,y), fill=tuple(round(a[j]*(1-t)+b[j]*t) for j in range(3)))
    return im

def orbit(draw, cx, cy, rx, ry, theta, color, width=2, opacity=1):
    pts=[]
    for j in range(181):
        a=2*math.pi*j/180
        x=rx*math.cos(a); y=ry*math.sin(a)
        pts.append((cx+x*math.cos(theta)-y*math.sin(theta),
                    cy+x*math.sin(theta)+y*math.cos(theta)))
    draw.line(pts,fill=color,width=width,joint="curve")

def particle_wave(draw, w, h, phase, top, tint):
    for col in range(0,w,17):
        for row in range(0,8):
            y=top+row*9+math.sin(col/57+phase+row*.4)*14
            r=1 if row%3 else 2
            a=1 - abs(col-w*.5)/(w*.65)
            if a>.12:
                rgb=tuple(int(t*.25 + min(1,a)*t*.32) for t in tint)
                draw.ellipse((col,y,col+r,y+r),fill=rgb)

def floating_panel(d, xy, title, content, accent):
    x,y=xy
    rect(d,(x,y,x+156,y+78),(19,40,61),12,(62,111,137),2)
    d.line((x+14,y+18,x+40,y+18), fill=accent, width=3)
    d.text((x+14,y+30),title,font=ft(13,mono=True),fill=accent)
    d.text((x+14,y+53),content,font=ft(11),fill=(193,214,232))

def frame_hero(k, n=26):
    w,h=1280,390
    t=2*math.pi*k/n
    im=background(w,h)
    glow(im,1033+int(10*math.sin(t)),181,173,(25,194,197),124)
    glow(im,1170,90,105,(104,84,231),82)
    glow(im,430,368,240,(28,98,146),56)
    d=ImageDraw.Draw(im)
    # Fine technical grid, left side fades into negative space.
    for gx in range(12,w,36):
        for gy in range(16,h,36):
            if (gx+gy)//36%4==0:
                d.ellipse((gx,gy,gx+1,gy+1),fill=(35,64,84))
    d.rounded_rectangle((1,1,w-2,h-2),radius=22,outline=(48,110,132),width=2)
    d.line((30,63,1250,63),fill=(44,78,102),width=1)
    d.ellipse((32,29,41,38),fill=C["teal"])
    d.text((50,26),"NYK  /  AI SYSTEMS LAB",font=ft(17,mono=True),fill=C["teal"])
    d.text((619,26),"BUILD   -   TEST   -   SHIP",font=ft(14,mono=True),fill=(110,157,180))
    d.text((45,92),"Generative AI",font=ft(66,bold=True),fill=C["text"])
    d.text((41,166),"Engineer.",font=ft(84,bold=True),fill=C["teal"])
    d.text((48,267),"NEELI YASWANTH KUMAR",font=ft(21,bold=True),fill=C["text"])
    d.text((48,303),"Python APIs  /  RAG  /  MCP  /  Agent workflows",font=ft(17),fill=C["muted"])
    rect(d,(45,343,410,372),(22,53,65),14,(49,113,128),1)
    d.ellipse((57,352,68,363),fill=C["teal"])
    d.text((79,347),"2 hosted APIs   |   3 engineering projects",font=ft(13,mono=True),fill=(180,245,231))
    # Orbital core and floating HUD: clear animation across frames.
    cx=1036;cy=191+int(6*math.sin(t))
    orbit(d,cx,cy,147,49,-.33,C["teal"],2)
    orbit(d,cx,cy,151,53,.53,(122,143,237),2)
    orbit(d,cx,cy,125,126,0,(55,127,144),2)
    for r in (103,79,58):
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(42,114,139),width=2)
    # Moving longitude/latitude linework on a glass sphere.
    for j in range(-2,3):
        rr=(1-(j/3.0)**2)**.5
        ey=cy+j*29
        d.ellipse((cx-89*rr,ey-12,cx+89*rr,ey+12),outline=(43,106,129),width=1)
    for j in range(9):
        a=2*math.pi*j/9+t*.28
        x=cx+73*math.cos(a)
        y=cy+62*math.sin(a)
        d.line((cx,cy,x,y),fill=(40,98,119),width=1)
        d.ellipse((x-3,y-3,x+3,y+3),fill=C["cyan"] if j%2 else C["teal"])
    # Inner brain-like neural core diagram (deliberately conceptual).
    core=[(-25,-13),(-13,-28),(9,-21),(27,-32),(36,-7),(24,16),
          (30,31),(2,30),(-18,20),(-34,2)]
    coords=[(cx+x,cy+y) for x,y in core]
    d.line(coords+[coords[0]],fill=(149,252,235),width=3,joint="curve")
    for a,b in [(0,4),(1,6),(3,8),(2,9),(4,7)]:
        d.line((*coords[a],*coords[b]),fill=(108,204,217),width=2)
    d.text((cx-12,cy-11),"AI",font=ft(20,bold=True),fill=C["text"])
    # Rotating orbit points: actual animated movement, not a static SVG masquerading as animation.
    for offs,rad,c in [(0,144,C["teal"]),(2.1,140,C["violet"]),(4.0,152,C["cyan"])]:
        x=cx+rad*math.cos(t+offs)
        y=cy+41*math.sin(t+offs)
        d.ellipse((x-5,y-5,x+5,y+5),fill=c)
    # Animated holographic floating cards; vary y, not text position too dramatically.
    floating_panel(d,(786,104+int(7*math.sin(t))),"MCP / TOOL","AST + SQLite",C["teal"])
    floating_panel(d,(1107,77+int(8*math.sin(t+2))),"TRACE / API","FastAPI + CI",C["cyan"])
    floating_panel(d,(1114,265+int(7*math.sin(t+4))),"RAG / DATA","Grounded search",C["violet"])
    # Platform and particle ocean.
    d.ellipse((895,310,1177,349),outline=(61,166,170),width=3)
    d.ellipse((938,321,1144,343),outline=C["teal"],width=2)
    particle_wave(d,w,h,t,360,C["teal"])
    return im

def make_hero():
    images=[frame_hero(i) for i in range(26)]
    path=OUT/"floating-ai-hero.gif"
    images[0].save(path,save_all=True,append_images=images[1:],
                   duration=115,loop=0,optimize=True,disposal=2)
    print("Created",path,path.stat().st_size)

PROJECTS=[
    dict(slug="codeatlas",idx="01",tag="STRUCTURAL CODE INTELLIGENCE",
         title="CodeAtlas MCP",description="AST + SQLite code context",color=C["teal"],
         nodes=["SOURCE","INDEX","MCP"]),
    dict(slug="agentgate",idx="02",tag="AGENT TOOL POLICY",
         title="AgentGate",description="Request checks + approvals",color=C["violet"],
         nodes=["REQUEST","POLICY","APPROVAL"]),
    dict(slug="routewise",idx="03",tag="LLM REQUEST INFRASTRUCTURE",
         title="RouteWise",description="Routing + bounded fallback",color=C["cyan"],
         nodes=["PROMPT","ROUTE","FALLBACK"]),
]

def project_frame(spec,k,n=20):
    w,h=480,253
    t=2*math.pi*k/n
    accent=spec["color"]
    im=background(w,h,(8,19,32),(13,31,49))
    glow(im,402,72,120,accent,105)
    d=ImageDraw.Draw(im)
    rect(d,(2,2,w-3,h-3),(13,28,44),17,(60,103,127),2)
    d.text((21,16),spec["idx"]+" / "+spec["tag"],font=ft(11,mono=True),fill=accent)
    d.text((19,53),spec["title"],font=ft(34,bold=True),fill=C["text"])
    d.text((21,102),spec["description"],font=ft(16),fill=C["muted"])
    d.line((20,147,460,147),fill=(45,84,108),width=1)
    # Three floating mini-pipeline nodes; moving dot confirms animation on hover-independent GIF.
    for j,label in enumerate(spec["nodes"]):
        x=20+j*152;y=160+int(3*math.sin(t+j*1.1))
        rect(d,(x,y,x+136,y+51),(23,47,65),10,(66,111,129),1)
        d.text((x+10,y+17),label,font=ft(12,mono=True),fill=accent)
        if j<2:
            d.line((x+137,y+25,x+152,y+25),fill=accent,width=2)
    px=22+436*k/max(n-1,1)
    d.ellipse((px-4,231,px+4,239),fill=accent)
    d.line((21,235,460,235),fill=(44,80,96),width=1)
    # Floating signal rings top right.
    rx,ry=421,91
    for r in (18,29,40):
        d.arc((rx-r,ry-r,rx+r,ry+r),start=40+k*7,end=295+k*7,fill=accent,width=2)
    return im

def make_project_gifs():
    for spec in PROJECTS:
        frames=[project_frame(spec,i) for i in range(20)]
        path=OUT/(spec["slug"]+"-floating.gif")
        frames[0].save(path,save_all=True,append_images=frames[1:],
                       duration=140,loop=0,optimize=True,disposal=2)
        print("Created",path,path.stat().st_size)

def metrics_dashboard():
    w,h=1280,230
    im=background(w,h)
    glow(im,920,185,175,(50,108,190),75)
    d=ImageDraw.Draw(im)
    cards=[
        ("03","FEATURED PROJECTS",C["teal"]),
        ("02","HOSTED FASTAPI APIs",C["violet"]),
        ("44","DOCUMENTED TESTS",C["cyan"]),
        ("05","CODEATLAS MCP TOOLS",C["coral"]),
    ]
    for i,(number,subtitle,c) in enumerate(cards):
        x=8+i*319
        rect(d,(x,8,x+305,214),(17,36,56),18,(53,94,119),2)
        d.line((x+18,34,x+77,34),fill=c,width=4)
        d.text((x+22,60),number,font=ft(79,bold=True),fill=c)
        d.text((x+22,166),subtitle,font=ft(15,mono=True),fill=(212,230,240))
        d.text((x+22,193),"VERIFIABLE PROJECT EVIDENCE",font=ft(10,mono=True),fill=(124,154,174))
    path=OUT/"verified-metrics.png"
    im.save(path,optimize=True)
    print("Created",path,path.stat().st_size)

if __name__ == "__main__":
    make_hero()
    make_project_gifs()
    metrics_dashboard()
