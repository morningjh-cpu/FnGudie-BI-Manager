import os, glob
from fontTools.fontBuilder import FontBuilder
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.agl import toUnicode
DIGITS = ['zero','one','two','three','four','five','six','seven','eight','nine']
def identify(base):
    if '_' in base: return base, None, 'lower'
    """파일명 → (글리프 이름, 유니코드, 분류). A-upper / a-lower / 0-number / 글리프 이름(period 등)"""
    if base.endswith(('-upper', '-lower')):
        ch, case = base.split('-'); return ch, ord(ch), case
    if base.endswith('-number'):
        n = int(base.split('-')[0]); return DIGITS[n], 0x30 + n, 'number'
    u = toUnicode(base)
    if len(u) != 1: raise SystemExit(f'알 수 없는 글리프 이름: {base}')
    return base, ord(u), 'symbol'

import xml.etree.ElementTree as ET

FAMILY, STYLE = "FnGuide Logotype", "Regular"
PS = "FnGuideLogotype-Regular"
VERSION = "1.100"
UPM, SCALE, BASE = 1000, 32.0, 28.24          # 35px viewBox → cap height ≈ 700 units
ROUND = {"0","3","6","8","9","G","Q","O","C","S","o","c","e","d","p","s","a","b","q","g"}  # 둥근 글자는 사이드베어링을 좁게
SB = {"upper": 60, "lower": 45, "number": 50, "symbol": 50}
OVERRIDE = {"f": (35, -60), "j": (-55, 45)}  # (spacing.json 이 없을 때만 쓰는 예전 규칙)
import json
SPACING = json.load(open("spacing.json")) if os.path.exists("spacing.json") else None
KERN_FEA = "kerning.fea"

def contours(svgfile):
    """SVG path → (y 반전·스케일 적용된) 윤곽선 리스트"""
    root = ET.parse(svgfile).getroot()
    rec = RecordingPen()
    tp = TransformPen(rec, (SCALE, 0, 0, -SCALE, 0, BASE*SCALE))
    cs = []
    for gi, p in enumerate(root.iter("{http://www.w3.org/2000/svg}path")):
        rec.value = []
        parse_path(p.get("d"), tp)
        cur = []
        for op, pts in rec.value:
            if op == "moveTo": cur = [(op, pts)]
            elif op in ("closePath", "endPath"):
                cs.append((gi, cur)); cur = []
            else: cur.append((op, pts))
        if cur: cs.append((gi, cur))
    return cs

def poly(c): return [pt for op, pts in c for pt in pts]
def area(c):
    p = poly(c); return sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2
def inside(pt, c):
    p, x, y, r = poly(c), pt[0], pt[1], False
    for i in range(len(p)):
        (x1,y1),(x2,y2) = p[i], p[i-1]
        if (y1>y) != (y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: r = not r
    return r

def draw(cs, pen, dx, ps_style):
    """바깥 윤곽/안쪽 구멍 방향을 정규화해서 그림 (CFF: 반시계 외곽, TT: 시계 외곽)"""
    tp = TransformPen(pen, (1,0,0,1,dx,0))
    for i, (g, c) in enumerate(cs):
        depth = sum(inside(c[0][1][0], o) for j, (h, o) in enumerate(cs) if j != i and h == g)
        want_ccw = (depth % 2 == 0) == ps_style
        target = ReverseContourPen(tp) if (area(c) > 0) != want_ccw else tp
        target.moveTo(c[0][1][0])
        for op, pts in c[1:]:
            getattr(target, op)(*pts)
        target.closePath()

glyphs, uni, kind = {}, {}, {}
for f in sorted(glob.glob("/home/claude/f1/all/*.svg")):
    base = os.path.basename(f)[:-4]
    name, code, case = identify(base)
    cs = contours(f)
    bp = BoundsPen(None)
    for _, c in cs:
        bp.moveTo(c[0][1][0]); [getattr(bp, op)(*pts) for op, pts in c[1:]]; bp.closePath()
    xmin, ymin, xmax, ymax = bp.bounds
    key = base.split("-")[0] if case in ("upper", "lower", "number") else name
    sb = SB[case] - (12 if key in ROUND else 0)
    lsb, rsb = OVERRIDE.get(key, (sb, sb))
    if SPACING is not None:
        lsb, rsb = SPACING[name]
    glyphs[name] = dict(cs=cs, dx=lsb - xmin, adv=round(xmax - xmin + lsb + rsb))
    uni[name], kind[name] = code, case

rank = {"upper": 0, "lower": 1, "number": 2, "symbol": 3}
order = [".notdef", "space"] + sorted(glyphs, key=lambda g: (rank[kind[g]], uni[g] if uni[g] is not None else 0x10000, g))
cmap = {uni[g]: g for g in glyphs if uni[g] is not None}; cmap[0x20] = "space"
adv = {".notdef": 500, "space": 250, **{c: g["adv"] for c, g in glyphs.items()}}

def notdef(pen):
    pen.moveTo((50,0)); pen.lineTo((50,700)); pen.lineTo((450,700)); pen.lineTo((450,0)); pen.closePath()
    pen.moveTo((100,50)); pen.lineTo((400,50)); pen.lineTo((400,650)); pen.lineTo((100,650)); pen.closePath()

def build(kind):
    fb = FontBuilder(UPM, isTTF=(kind == "ttf"))
    fb.setupGlyphOrder(order); fb.setupCharacterMap(cmap)
    if kind == "otf":
        cs = {}
        for g in order:
            pen = T2CharStringPen(adv[g], None)
            if g == ".notdef": notdef(pen)
            elif g != "space": draw(glyphs[g]["cs"], pen, glyphs[g]["dx"], True)
            cs[g] = pen.getCharString()
        fb.setupCFF(PS, {"FullName": f"{FAMILY} {STYLE}"}, cs, {})
    else:
        gl = {}
        for g in order:
            pen = TTGlyphPen(None)
            if g == ".notdef":
                notdef(ReverseContourPen(pen))
            elif g != "space":
                draw(glyphs[g]["cs"], Cu2QuPen(pen, 1.0, reverse_direction=False), glyphs[g]["dx"], False)
            gl[g] = pen.glyph()
        fb.setupGlyf(gl)
    metrics = {}
    for g in order:
        lsb = 0
        if g in glyphs:
            xs = [pt[0] + glyphs[g]["dx"] for _, c in glyphs[g]["cs"] for op, pts in c for pt in pts]
            lsb = round(min(xs))
        elif g == ".notdef": lsb = 50
        metrics[g] = (adv[g], lsb)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-250)
    fb.setupNameTable({"familyName": FAMILY, "styleName": STYLE, "uniqueFontIdentifier": f"{PS};{VERSION}",
                       "fullName": f"{FAMILY} {STYLE}", "psName": PS, "version": f"Version {VERSION}",
                       "copyright": "Copyright (c) 2026 FnGuide. All rights reserved.",
                       "description": "Logotype font based on the FnGuide logo (A-Z, a-z, 0-9, ASCII punctuation; includes draft glyphs; internal use)."})
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-250, sTypoLineGap=0, usWinAscent=850, usWinDescent=260,
                sxHeight=498, sCapHeight=700, fsType=0x0008, achVendID="FNGD")
    fb.setupPost()
    if os.path.exists(KERN_FEA):
        from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
        addOpenTypeFeaturesFromString(fb.font, open(KERN_FEA).read())
    fb.font.save(f"out/{PS}.{kind}")
    return fb.font

os.makedirs("out", exist_ok=True)
build("otf"); f = build("ttf")
f.flavor = "woff"; f.save(f"out/{PS}.woff")
print(len(glyphs), "glyphs +", "space, .notdef")
