"""서체 윤곽에서 곧은 세로 선 두 개(왼쪽 면·오른쪽 면)를 짝지어 기둥 두께를 잰다 (1000 단위 → 35칸 좌표로 환산)"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
path = sys.argv[1]
f = TTFont(path); gs = f.getGlyphSet()
def edges(g):
    rp = DecomposingRecordingPen(gs); gs[g].draw(rp)
    out = []; cur = None; start = None
    for op, pts in rp.value:
        if op == "moveTo": cur = start = pts[0]
        elif op == "lineTo":
            p = pts[0]
            if abs(p[0] - cur[0]) <= 3 and abs(p[1] - cur[1]) >= 150: out.append((cur[0], cur[1], p[1]))   # (x, y시작, y끝)
            cur = p
        elif op == "curveTo": cur = pts[-1]
        elif op in ("closePath", "endPath"):
            if cur and start and abs(start[0] - cur[0]) <= 3 and abs(start[1] - cur[1]) >= 150: out.append((cur[0], cur[1], start[1]))
            cur = None
    return out
res = {}
for g in "BDEFHIJKLMNPRTUY" + "bdfhijklmnpqrtu":
    es = edges(g); ws = []
    downs = [e for e in es if e[2] < e[1]]; ups = [e for e in es if e[2] > e[1]]   # 아래로 가는 선 = 왼쪽 면, 위로 가는 선 = 오른쪽 면 (CFF 반시계 외곽)
    for a in downs:
        for b in ups:
            lo = max(min(a[1], a[2]), min(b[1], b[2])); hi = min(max(a[1], a[2]), max(b[1], b[2]))
            w = b[0] - a[0]
            if hi - lo >= 150 and 90 <= w <= 170: ws.append((w, hi - lo))
    if ws: ws.sort(key=lambda t: -t[1]); res[g] = ws[0][0] / 32
for kind, chars in (("대문자", "BDEFHIJKLMNPRTUY"), ("소문자", "bdfhijklmnpqrtu")):
    items = sorted([(c, res[c]) for c in chars if c in res], key=lambda kv: -kv[1])
    import statistics
    med = statistics.median(v for _, v in items)
    print(kind, f"중앙값 {med:.2f}")
    print("  " + "  ".join(f"{c}:{v:.2f}({(v/med-1)*100:+.0f}%)" for c, v in items))
    print("  못 잰 글자:", [c for c in chars if c not in res])
