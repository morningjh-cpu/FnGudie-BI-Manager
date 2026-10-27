"""사이트 로고타입 v1.100 → v1.200 전후 비교 (HTML + PNG). 실행: py out/font-update/logo-compare.py"""
import re, xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
ROOT = Path(__file__).resolve().parents[2]
OLD, NEW = ROOT / "_trash/brand-site-logos-v1.100", ROOT / "out/brand-site/logos"
NAMES = ["fnguide-com", "quantiwise", "wisereport", "fnindex", "wiseindex", "cryptoguide", "fnaims",
         "companyguide", "companywise", "companyglobal", "fnapi", "fnspace", "marketmonitor"]
NS = "{http://www.w3.org/2000/svg}"
def draw(ax, f, y0):
    r = ET.parse(f).getroot()
    for p in r.iter(NS + "path"):
        rp = RecordingPen(); parse_path(p.get("d"), rp); v, c = [], []
        for op, pts in rp.value:
            pts = [(x, y + y0) for x, y in pts]
            if op == "moveTo": v += pts; c.append(MPath.MOVETO)
            elif op == "lineTo": v += pts; c.append(MPath.LINETO)
            elif op == "curveTo": v += pts; c += [MPath.CURVE4] * 3
            elif op == "qCurveTo": v += pts; c += [MPath.CURVE3] * len(pts)
            elif op in ("closePath", "endPath"): v.append((0, 0)); c.append(MPath.CLOSEPOLY)
        fill = p.get("fill") or "#333"
        ax.add_patch(PathPatch(MPath(v, c), fc=fill, ec="none"))
matplotlib.rcParams["font.family"] = "Malgun Gothic"
fig, axs = plt.subplots(len(NAMES), 2, figsize=(10, len(NAMES) * 0.85))
for i, n in enumerate(NAMES):
    for j, (d, lab) in enumerate(((OLD, "v1.100"), (NEW, "v1.200"))):
        ax = axs[i][j]; ax.axis("off"); ax.set_aspect("equal")
        vb = [float(x) for x in ET.parse(d / f"{n}.svg").getroot().get("viewBox").split()]
        draw(ax, d / f"{n}.svg", 0); ax.set_xlim(vb[0], vb[0] + 8200); ax.set_ylim(260, -780)   # 모든 칸 같은 범위 → 같은 배율, 바닥선도 맞음
        if i == 0: ax.set_title(lab, fontsize=11)
fig.tight_layout(); fig.savefig(ROOT / "out/font-update/v1.200/preview/logo-compare.png", dpi=80)
# 모든 로고를 같은 배율로: SVG 파일의 원래 크기(1000 단위 = 40px)에 SCALE 을 곱함. 높이를 맞추면 로고마다 글자 크기가 달라지므로 쓰지 않는다
SCALE = 1.5
def img(f, src):
    r = ET.parse(f).getroot()
    w, h = float(r.get("width")) * SCALE, float(r.get("height")) * SCALE
    return f'<img src="{src}" style="width:{w:.1f}px;height:{h:.1f}px">'
rows = "".join(f'<tr><td>{n}</td><td>{img(OLD / f"{n}.svg", f"../../_trash/brand-site-logos-v1.100/{n}.svg")}</td>'
               f'<td>{img(NEW / f"{n}.svg", f"../brand-site/logos/{n}.svg")}</td></tr>' for n in NAMES)
(ROOT / "out/font-update/logo-compare.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>로고타입 전후 비교</title>
<style>body{{font-family:'Malgun Gothic',sans-serif;margin:24px;background:#fff;color:#222}}td{{padding:12px 18px;border-bottom:1px solid #eee;vertical-align:top}}img{{display:block}}th{{text-align:left;padding:8px 18px}}td:first-child{{color:#888;font-size:13px;padding-top:18px}}</style>
<h2>사이트 로고타입 v1.100 → v1.200</h2><p>바뀐 글자 f m M s S y r I 가 들어간 로고만 · 모든 로고 같은 배율(글자 크기 동일), 윗선 맞춤</p>
<table><tr><th>파일</th><th>v1.100 (기존)</th><th>v1.200 (새것)</th></tr>{rows}</table>""", encoding="utf-8")
print("done")
