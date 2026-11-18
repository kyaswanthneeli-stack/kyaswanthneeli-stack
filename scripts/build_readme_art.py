"""Generate a cinematic animated GitHub README hero and three project cover cards.

Built-in Pillow drawing only: no external images, logos, network requests or tracking.
Every project label and limitation reflects the linked public implementation.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def font(size: int, *, bold=False, mono=False):
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(path, size)

def gradient(size, a=(8, 17, 34), b=(17, 35, 62)):
    w, h = size
    image = Image.new("RGB", size)
    d = ImageDraw.Draw(image)
    for y in range(h):
        t = y / max(h - 1, 1)
        color = tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
        d.line((0, y, w, y), fill=color)
    return image

def glow(image, xy, r, color, strength=100):
    overlay = Image.new("RGBA", image.size)
    d = ImageDraw.Draw(overlay)
    x, y = xy
    d.ellipse((x-r, y-r, x+r, y+r), fill=(*color, strength))
    blurred = overlay.filter(ImageFilter.GaussianBlur(r / 2.6))
    image.paste(blurred, (0, 0), blurred)

def dotted_grid(d, w, h, step=42):
    for x in range(20, w, step):
        for y in range(20, h, step):
            d.ellipse((x, y, x+1, y+1), fill=(44, 74, 93))

def banner_frame(index, frames=30):
    w, h = 1152, 360
    t = 2 * math.pi * index / frames
    im = gradient((w, h), (6, 14, 30), (13, 26, 49))
    glow(im, (900 + int(18*math.sin(t)), 178), 158, (24, 211, 193), 86)
    glow(im, (360 + int(35*math.cos(t)), 284), 176, (122, 98, 232), 48)
    d = ImageDraw.Draw(im)
    dotted_grid(d, w, h)
    d.rounded_rectangle((15, 15, w-16, h-16), radius=27, outline=(42, 87, 111), width=2)
    d.line((62, 89, 704, 89), fill=(42, 76, 101), width=2)
    d.text((62, 43), "NYK  /  ENGINEERING PORTFOLIO", fill=(102, 241, 218), font=font(16, mono=True))
    d.text((62, 111), "NEELI YASWANTH", fill=(246, 250, 255), font=font(53, bold=True))
    d.text((60, 178), "KUMAR", fill=(132, 238, 219), font=font(77, bold=True))
    d.text((63, 285), "GENERATIVE AI   /   PYTHON   /   AGENTIC SYSTEMS", fill=(188, 206, 226), font=font(17, mono=True))
    # A moving, orbiting graph, decorative and deliberately not a runtime trace.
    cx, cy = 956, 182
    for r, c in ((120, (45, 116, 136)), (96, (52, 105, 155)), (66, (60, 130, 154))):
        d.ellipse((cx-r,cy-r,cx+r,cy+r), outline=c, width=2)
    d.line((cx-118,cy,cx+118,cy), fill=(41,87,111), width=1)
    d.line((cx,cy-118,cx,cy+118), fill=(41,87,111), width=1)
    points=[]
    for i in range(5):
        a=t*(1 if i % 2 else -1)+i*math.tau/5
        radius=(93,74,111,88,59)[i]
        x=int(cx+radius*math.cos(a)); y=int(cy+radius*math.sin(a))
        points.append((x,y))
    for i,p in enumerate(points):
        q=points[(i+2)%len(points)]
        d.line((*p,*q),fill=(47,119,143),width=2)
    for i,(x,y) in enumerate(points):
        r=5 if i<3 else 4
        d.ellipse((x-r,y-r,x+r,y+r),fill=(133,244,222) if i<3 else (178,153,255))
        d.ellipse((x-10,y-10,x+10,y+10),outline=(69,141,157))
    d.rounded_rectangle((917,143,993,220),radius=19,fill=(13,31,52),outline=(106,223,207),width=2)
    d.text((937,158), "{ }", fill=(162,252,228), font=font(24, mono=True))
    # Moving scanline in the lower glass bar.
    scan_x=62+int(600*(index/frames))
    d.line((62,335,704,335),fill=(34,67,93),width=2)
    d.line((max(62,scan_x-62),335,scan_x,335),fill=(106,228,211),width=3)
    # Sparse moving particles, not visually noisy.
    rng=random.Random(145)
    for i in range(28):
        bx=rng.randint(10,w-10);by=rng.randint(18,h-15)
        x=bx+6*math.cos(t+i);y=by+5*math.sin(t+1.3*i)
        if x<705 and y>96:
            continue
        d.ellipse((x,y,x+1.5,y+1.5),fill=(76,126,152))
    return im

def create_banner():
    frames=[banner_frame(i) for i in range(30)]
    # Global adaptive palette keeps motion crisp and compresses efficiently.
    frames[0].save(
        OUT / "nyk-animated-banner.gif",
        save_all=True,append_images=frames[1:],duration=110,
        loop=0,optimize=True,disposal=2
    )
    print(f"Banner: {(OUT/'nyk-animated-banner.gif').stat().st_size:,} bytes / 30 frames")

PROJECTS=[
    ("codeatlas","01  /  DEVELOPER TOOLING","CodeAtlas MCP","AST + SQLite + five MCP tools","Python  >  Symbols  >  Call Graph", (121,162,255)),
    ("agentgate","02  /  AGENT GOVERNANCE","AgentGate","Request validation + one-use approvals","Tool  >  Policy  >  Approval", (102,231,204)),
    ("routewise","03  /  LLM INFRASTRUCTURE","RouteWise","Heuristic routing + bounded failover","Prompt  >  Route  >  Fallback", (254,174,120)),
]

def create_cards():
    w,h=720,360
    for key,eyebrow,title,desc,flow,accent in PROJECTS:
        im=gradient((w,h),(11,23,42),(17,39,60))
        glow(im,(610,100),140,accent,58)
        d=ImageDraw.Draw(im)
        dotted_grid(d,w,h,34)
        d.rounded_rectangle((8,8,w-9,h-9),radius=24,outline=tuple(int(v*.5) for v in accent),width=2)
        d.rounded_rectangle((36,37,314,69),radius=12,fill=(30,52,70))
        d.text((48,44),eyebrow,fill=accent,font=font(15,mono=True))
        d.text((37,102),title,fill=(242,247,255),font=font(59,bold=True))
        d.text((39,192),desc,fill=(190,207,222),font=font(19))
        d.rounded_rectangle((36,261,684,315),radius=14,fill=(18,42,60),outline=(53,84,102))
        d.text((55,278),flow,fill=accent,font=font(19,mono=True))
        # Orbital icon gives structure without decorative clutter.
        d.ellipse((559,76,670,187),outline=tuple(int(v*.7) for v in accent),width=2)
        d.ellipse((576,93,652,169),outline=(70,108,123),width=2)
        d.ellipse((606,123,622,139),fill=accent)
        out=OUT/f"{key}-card.png"
        im.save(out,optimize=True)
        print(f"Card: {out.name} ({out.stat().st_size:,} bytes)")


def create_avatar():
    """Matching GitHub avatar users can choose to upload in Settings > Public profile."""
    w=h=512
    im=gradient((w,h),(6,17,32),(15,37,58))
    glow(im,(260,248),170,(27,208,191),110)
    glow(im,(120,400),112,(120,99,228),73)
    d=ImageDraw.Draw(im)
    for radius, col, thick in (
        (219,(42,111,126),3),
        (191,(85,170,176),2),
        (168,(42,92,114),2),
    ):
        d.ellipse((256-radius,256-radius,256+radius,256+radius),outline=col,width=thick)
    # Deliberately geometric: not a simulated human face.
    for i in range(10):
        angle=(i/10)*math.tau
        r=200
        x=int(256+math.cos(angle)*r)
        y=int(256+math.sin(angle)*r)
        d.ellipse((x-4,y-4,x+4,y+4),fill=(134,243,221))
    d.rounded_rectangle((88,156,424,351),radius=54,fill=(12,33,53),outline=(118,235,209),width=4)
    title_font=font(115,bold=True)
    text="NYK"
    box=d.textbbox((0,0),text,font=title_font)
    tw=box[2]-box[0]
    d.text(((w-tw)/2,175),text,font=title_font,fill=(212,255,246))
    tiny=font(20,mono=True)
    text2="AI ENGINEERING"
    box2=d.textbbox((0,0),text2,font=tiny)
    d.text(((w-(box2[2]-box2[0]))/2,310),text2,font=tiny,fill=(124,221,210))
    output=OUT/"nyk-avatar-option.png"
    im.save(output,optimize=True)
    print(f"Avatar: {output.name} ({output.stat().st_size:,} bytes)")

if __name__=="__main__":
    create_banner()
    create_cards()
    create_avatar()
