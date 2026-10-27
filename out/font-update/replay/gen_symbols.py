import math, xml.etree.ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from clean import write
def ds(f): return [p.get("d") for p in ET.parse(f).getroot().iter("{http://www.w3.org/2000/svg}path")]
def xform(d, m):
    pen = SVGPathPen(None); parse_path(d, TransformPen(pen, m)); return pen.getCommands()
MIRROR = (-1, 0, 0, 1, 35, 0)
def poly(pts): return "M" + "L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + "Z"
def ellipse(cx, cy, rx, ry, a0, a1, n=48):
    return [(cx + rx*math.cos(math.radians(a0 + (a1-a0)*i/n)), cy + ry*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]
def ring(cx, cy, rx, ry, rxi, ryi):   # 바깥 + 안쪽(구멍) 윤곽을 한 path에
    return poly(ellipse(cx, cy, rx, ry, 0, 360)[:-1]) + poly(ellipse(cx, cy, rxi, ryi, 360, 0)[:-1])
def arc_band(cx, cy, rx, ry, rxi, ryi, a0, a1):
    return poly(ellipse(cx, cy, rx, ry, a0, a1) + ellipse(cx, cy, rxi, ryi, a1, a0))
def bar(cx, cy, length, w, deg):
    t = math.radians(deg); ux, uy = math.sin(t), -math.cos(t); vx, vy = -uy, ux
    h, k = length/2, w/2
    return poly([(cx+ux*h+vx*k, cy+uy*h+vy*k), (cx+ux*h-vx*k, cy+uy*h-vy*k), (cx-ux*h-vx*k, cy-uy*h-vy*k), (cx-ux*h+vx*k, cy-uy*h+vy*k)])

C = "clean"
DOT = ds(f"{C}/period.svg")[0]                                   # r 2.46, 중심 (17.5, 26.11)
TOPDOT = [d for d in ds(f"{C}/colon.svg") if "12.65" in d or "15.1" in d] or [ds(f"{C}/colon.svg")[1]]
COMMA = ("M17.5,23.65C18.95,23.65 19.96,24.8 19.96,26.35C19.96,28.75 18.55,30.75 15.95,31.95L15.55,31.3"
         "C16.95,30.45 17.65,29.55 17.75,28.55C16.25,28.5 15.04,27.45 15.04,26.11C15.04,24.75 16.14,23.65 17.5,23.65Z")
G = {}
G["comma"] = [COMMA]
G["semicolon"] = [min(ds(f"{C}/colon.svg"), key=lambda d: float(d.split(',')[1].split('c')[0].split('C')[0]))] + [COMMA]
G["quotesingle"] = [poly([(15.14,6.37),(19.86,6.37),(19.41,12.4),(15.59,12.4)])]
G["quotedbl"] = [poly([(12.1,6.37),(15.7,6.37),(15.35,12.4),(12.45,12.4)]), poly([(19.3,6.37),(22.9,6.37),(22.55,12.4),(19.65,12.4)])]
G["grave"] = [poly([(12.9,6.37),(16.6,6.37),(20.9,10.6),(18.9,11.3)])]
G["asciicircum"] = [poly([(10.9,16.0),(16.0,6.37),(19.0,6.37),(24.1,16.0),(21.2,16.0),(17.5,9.2),(13.8,16.0)])]
G["underscore"] = ds(f"{C}/endash.svg")                            # 첨부 endash 도형 = 밑줄 위치
G["endash"] = [xform(ds(f"{C}/endash.svg")[0], (1, 0, 0, 1, 0, 20.31 - 30.895))]   # 하이픈 높이로 이동
LESS = poly([(26.04,12.97),(26.04,15.65),(12.9,20.6),(26.04,25.55),(26.04,28.26),(8.96,21.86),(8.96,19.34)])
G["less"] = [LESS]; G["greater"] = [xform(LESS, MIRROR)]
G["backslash"] = [xform(ds(f"{C}/slash.svg")[0], MIRROR)]
BRACE = ("M21.54,4.16V5.9C19.2,5.9 18.6,6.6 18.6,8.6V14.9C18.6,17 17.6,18 15.6,18.32C17.6,18.64 18.6,19.6 18.6,21.7V28"
         "C18.6,30 19.2,30.74 21.54,30.74V32.48C17.4,32.48 16,31.3 16,28.4V22.2C16,20.3 15.2,19.3 13.46,19.22V17.42"
         "C15.2,17.34 16,16.3 16,14.4V8.2C16,5.3 17.4,4.16 21.54,4.16Z")
G["braceleft"] = [BRACE]; G["braceright"] = [xform(BRACE, MIRROR)]
G["asterisk"] = [bar(17.5, 10.95, 9.2, 2.5, a) for a in (0, 60, 120)]
zero = ds(f"{C}/0-number.svg")[0]                                  # x 8.99–26.0, y 7.77–28.6
sx, sy = 0.38, 0.37
G["percent"] = [xform(zero, (sx, 0, 0, sy, 8.6 - 8.99*sx, 7.77 - 7.77*sy)),
                xform(zero, (sx, 0, 0, sy, 20.0 - 8.99*sx, 20.9 - 7.77*sy)),
                poly([(22.3,7.77),(24.8,7.77),(12.7,28.25),(10.2,28.25)])]
G["ampersand"] = [ring(14.5, 11.7, 4.7, 5.3, 1.9, 2.75),
                  arc_band(15.4, 22.5, 6.7, 6.1, 3.4, 3.65, 252, -16),
                  poly([(15.4,15.6),(18.4,14.4),(28.0,28.25),(23.4,28.25)]),
                  poly([(20.6,20.1),(21.9,17.3),(27.0,17.3),(27.0,18.95),(23.4,18.95),(22.3,21.4)])]
# 임시 소문자 z: 새 대문자 Z를 x-height(12.67)에 맞게 축소
Zn = ds(f"{C}/Z-upper.svg")[0]
G["z-lower"] = [xform(Zn, (0.86, 0, 0, 0.712, 17.5 - 17.5*0.86, 28.25 - 28.25*0.712))]
for k, v in G.items(): write(f"gen/{k}.svg", v)
print(len(G), "generated:", ", ".join(G))
