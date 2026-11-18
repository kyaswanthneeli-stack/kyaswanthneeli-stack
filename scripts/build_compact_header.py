"""Compact dark profile banner, proportioned like the user's reference screenshot.
Pillow only; output is an animated GIF that GitHub README supports.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
OUT=Path("assets")
OUT.mkdir(exist_ok=True)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
M="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def ft(n, bold=False, mono=False):return ImageFont.truetype(M if mono else B if bold else F,n)
frames=[]
for i in range(24):
    im=Image.new("RGB",(1200,292),"#0d1117")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,10,1190,282),radius=15,fill="#303235",outline="#4b525b",width=2)
    d.text((34,27),"kyaswanthneeli-stack  /  README.md",font=ft(14,mono=True),fill="#9aa8b5")
    d.text((37,69),"Generative AI Engineer",font=ft(54,bold=True),fill="#f2f5fb")
    d.text((39,137),"Neeli Yaswanth Kumar",font=ft(25),fill="#c4d1d8")
    d.text((39,179),"Python  ·  FastAPI  ·  RAG  ·  LangGraph  ·  MCP  ·  Azure",font=ft(20,mono=True),fill="#e1e8ee")
    d.line((40,227,900,227),fill="#505b62",width=1)
    d.text((40,244),"PORTFOLIO: kyaswanthneeli-stack.github.io",font=ft(15,mono=True),fill="#91e0d0")
    d.text((565,244),"CONTACT: kyaswanthneeli@gmail.com",font=ft(15,mono=True),fill="#add3d8")
    t=2*math.pi*i/24
    # Minimal constellation at the far right of the header, preserving text readability.
    stars=[(1069,60,18),(1103,94,10),(1041,104,9)]
    for j,(x,y,r) in enumerate(stars):
        radius=r*(.85+.15*math.sin(t+j))
        d.polygon([(x,y-radius),(x+radius*.22,y-radius*.22),(x+radius,y),(x+radius*.22,y+radius*.22),(x,y+radius),(x-radius*.22,y+radius*.22),(x-radius,y),(x-radius*.22,y-radius*.22)],fill="#24b8a5")
    for n in range(4):
        x=1033+n*23;y=174+n*21
        d.polygon([(x,y),(x+31,y+9),(x+18,y+28),(x-13,y+16)],outline="#277f70",width=3)
    frames.append(im)
path=OUT/"github-reference-compact.gif"
frames[0].save(path,save_all=True,append_images=frames[1:],duration=140,loop=0,disposal=2,optimize=True)
print(path,path.stat().st_size)
