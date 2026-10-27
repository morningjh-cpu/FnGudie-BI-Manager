"""weight.py 가 쓰는 도우미: SVG 의 path 들을 그리는 데 필요한 두 함수 (원래 파일이 저장소에 없어 다시 작성)"""
import xml.etree.ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from matplotlib.path import Path
NS = "{http://www.w3.org/2000/svg}"
def ds(f):
    return [p.get("d") for p in ET.parse(f).getroot().iter(NS + "path")]
def mpl_path(d):
    rp = RecordingPen(); parse_path(d, rp)
    v, c = [], []
    for op, pts in rp.value:
        if op == "moveTo": v += pts; c.append(Path.MOVETO)
        elif op == "lineTo": v += pts; c.append(Path.LINETO)
        elif op == "curveTo": v += pts; c += [Path.CURVE4] * 3
        elif op == "qCurveTo": v += pts; c += [Path.CURVE3] * len(pts)
        elif op in ("closePath", "endPath"): v.append((0, 0)); c.append(Path.CLOSEPOLY)
    return Path(v, c)
