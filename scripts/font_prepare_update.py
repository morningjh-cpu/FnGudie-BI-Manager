"""전용서체 업데이트용: source-svg/7_update 의 일러스트레이터 원본에서 보이는 글자 도형만 꺼내
기존 글자와 같은 규격(35칸 캔버스, 글자 바닥선 28.24)으로 맞춘 SVG 를 만든다.
사용: py scripts/font_prepare_update.py <7_update 폴더> <내보낼 폴더>"""
import sys, os, glob
import xml.etree.ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
NS = "{http://www.w3.org/2000/svg}"
BASE_OLD, BASE_NEW = 28.24, 28.98              # 기존 글자 바닥선 / 새 파일의 바닥선
DY = BASE_OLD - BASE_NEW                       # 위로 0.74
TPL = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 35 35">\n  <defs><style>.st0 {{ fill: #b9023d; }}</style></defs>\n{p}\n</svg>\n'
def num(v): return ("%.3f" % v).rstrip("0").rstrip(".")
def visible_paths(root):
    out = []
    def walk(e, hidden):
        hidden = hidden or e.get("class", "") in ("st2", "st3", "st4")
        if e.tag == NS + "path" and not hidden: out.append(e.get("d"))
        for c in e: walk(c, hidden)
    walk(root, False)
    return out
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, "*.svg"))):
    ds = visible_paths(ET.parse(f).getroot())
    if len(ds) != 1: raise SystemExit(f"{os.path.basename(f)}: 보이는 도형이 {len(ds)}개 (1개여야 함)")
    pen = SVGPathPen(None, ntos=num); parse_path(ds[0], TransformPen(pen, (1, 0, 0, 1, 0, DY)))
    d = pen.getCommands()
    bp = BoundsPen(None); parse_path(d, bp); b = bp.bounds
    if b[0] < 0 or b[2] > 35 or b[1] < 0 or b[3] > 35: raise SystemExit(f"{os.path.basename(f)}: 캔버스를 벗어남 {b}")
    open(os.path.join(dst, os.path.basename(f)), "w", encoding="utf-8").write(TPL.format(p=f'  <path class="st0" d="{d}"/>'))
    print(os.path.basename(f), [round(v, 2) for v in b])
