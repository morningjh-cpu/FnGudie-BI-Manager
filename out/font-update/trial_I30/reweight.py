"""윤곽 오프셋으로 획 두께 조정 후 원래 외곽 크기로 복원 (delta>0: 가늘게, <0: 굵게)"""
import sys
sys.path.insert(0, "/home/claude/d1"); sys.path.insert(0, ".")
from offset import thin_glyph
from render import ds
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fix_shapes import write
def bounds(dl):
    bp = BoundsPen(None)
    for d in dl: parse_path(d, bp)
    return bp.bounds
def reweight(name, delta):
    src = f"all/{name}.svg"; o = bounds(ds(src))
    new = thin_glyph(src, delta); n = bounds(new)
    sx = (o[2]-o[0]) / (n[2]-n[0]); sy = (o[3]-o[1]) / (n[3]-n[1])
    m = (sx, 0, 0, sy, o[0] - n[0]*sx, o[1] - n[1]*sy)
    out = []
    for d in new:
        pen = SVGPathPen(None); parse_path(d, TransformPen(pen, m)); out.append(pen.getCommands())
    write(name, out)
if __name__ == "__main__":
    for name, delta in (("S-upper", 0.25), ("X-upper", 0.33), ("w-lower", -0.24), ("z-lower", -0.30)):
        reweight(name, delta); print("reweighted", name, delta)
