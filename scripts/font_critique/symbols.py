"""⑨ 안 B(비례 숫자 유지 + 고정폭은 선택 기능) 시안과 금융 기호 1순위(₩ − ± × ·) 시안 그림.
숫자 1 은 ⑥ 수정 안 A(one_base.py) 를 쓴다. 서체 파일은 고치지 않는다."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from fontTools.pens.boundsPen import BoundsPen
import one_base
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
cm = fn.tt.getBestCmap(); hm = fn.tt["hmtx"]
RED = "#B9023D"

def area(pts):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2
CW = area([p for op, ps in fn.rec(cm[ord("+")]) for p in ps]) < 0   # 이 서체의 바깥 윤곽 방향
def poly(pts):
    if (area(pts) < 0) != CW: pts = pts[::-1]                        # 같은 방향으로 맞춰 겹친 곳이 합쳐지게
    return [("M", [pts[0]])] + [("L", [p]) for p in pts[1:]] + [("Z", [])]
def rect(x0, y0, x1, y1): return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

# ---- 지금 서체에서 가져온 기준값 ----
# + : 폭 647, 가로획 y 212~293(두께 81), 세로획 x 269~377, 가운데 높이 252.5
# = : 가로획 두께 80~81 / . : 지름 158
PLUS_ADV, MID, BAR = 647, 252.5, 81
# − : + 의 가로획을 기준으로 한다. 해외 서체(Pretendard·Inter·Segoe UI·Verdana·Calibri)는 − 길이가 + 너비의 0.97~1.00(가운데 0.98).
#     + 는 세로획이 가운데를 끊어 실제보다 짧아 보이므로, 같은 비율로 − 를 0.98 로 맞춘다 → 547 × 0.98 = 536
MINUS_W = round(547 * 0.98)
MINUS = rect(323.5 - MINUS_W / 2, 212, 323.5 + MINUS_W / 2, 293)
PLUSMINUS = (rect(50, 300, 597, 381) + rect(269, 130, 377, 551)   # ± : + 를 위로 올리고
             + rect(50, 0, 597, 81))                              #     아래에 같은 두께 가로줄
# × : 해외 서체는 × 가 차지하는 네모가 + 의 0.93~1.01(가운데 0.95). 이 서체의 + 는 547×490 이라 그 가운데값(518)의 0.95 = 492 네모에 맞춘다.
#     획 굵기는 + 가로획 81 과 세로획 108 의 가운데인 94 (사선은 가로와 세로 사이이므로)
TIMES_BOX, TIMES_T = 492, 94
def times():
    t = TIMES_T / 2
    c, h = (323.5, MID), TIMES_BOX / 2 / 0.7071 - t     # 네모 반폭 = (h + t) × 0.7071
    out = []
    for a in (45, 135):
        r = math.radians(a); ux, uy = math.cos(r), math.sin(r); vx, vy = -uy, ux
        out += poly([(c[0] + sx * h * ux + sy * t * vx, c[1] + sx * h * uy + sy * t * vy)
                     for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
    return out
TIMES = times()
DOT = [(op, [(x, y + MID - 68) for x, y in ps]) for op, ps in fn.rec(cm[ord(".")])]   # · : 마침표를 가운데 높이로
# ₩ : W 에 가로획 한 줄 (Pretendard 방식: 대문자 높이 가운데, W 양옆으로 조금 나감)
bp = BoundsPen(fn.gs); fn.gs[cm[ord("W")]].draw(bp); wx0, _, wx1, _ = bp.bounds
# 가로획 높이(350)에서 W 사선은 x 202~957. 왼쪽은 사선 밖으로 184 나가고, 오른쪽은 왼쪽의 약 0.8배인 150 나가게 한다
#  (처음엔 W 윤곽 끝 +8 이라 오른쪽이 88 로 너무 짧았음 — 사용자 의견)
WON_R = 957 + 150
# 가로획 굵기는 이 서체 대문자 가로획과 같은 65 (H·E·F 가운데 가로획 65, E·F·Z·T 위아래 가로획 63~66)
WON_T = 65
WON = [(op, [(x + 20, y) for x, y in ps]) for op, ps in fn.rec(cm[ord("W")]) + rect(wx0 - 8, 350 - WON_T / 2, WON_R, 350 + WON_T / 2)]   # 가로획이 옆 글자에 닿지 않게 왼쪽 20 여유
NEW = {"−": (MINUS, PLUS_ADV), "±": (PLUSMINUS, PLUS_ADV), "×": (TIMES, PLUS_ADV),
       "·": (DOT, hm[cm[ord(".")]][0]), "₩": (WON, round(WON_R + 20 + 47))}

ONE, ONE_ADV = one_base.NEW, one_base.NEW_ADV
one = cm[ord("1")]
TAB = 600
digits = [cm[ord(c)] for c in "0123456789"]

def draw(ax, text, x0, y0, size, tab=False, color="#111"):
    """새 기호는 직접 그리고, 나머지는 서체 그대로(커닝 포함) 그린다. tab=True 면 고정폭 숫자 기능을 켠 상태."""
    s = size / fn.upm; V, C = [], []; x = 0
    def put(ops, dx):
        for op, pts in ops:
            V.extend([(x0 + (dx + px) * s, y0 + py * s) for px, py in pts] or [(0, 0)])
            C.extend({"M": [Path.MOVETO], "L": [Path.LINETO], "C": [Path.CURVE4] * 3,
                      "Q": [Path.CURVE3] * 2, "Z": [Path.CLOSEPOLY]}[op])
    runs, cur = [], ""
    for ch in text:
        if ch in NEW: runs += [cur, ch] if cur else [ch]; cur = ""
        else: cur += ch
    if cur: runs.append(cur)
    for r in runs:
        if r in NEW:
            ops, adv = NEW[r]
            if tab and r in "−±": put(ops, x + (TAB - adv) / 2); x += TAB   # 표에서 부호도 숫자와 같은 폭
            else: put(ops, x); x += adv
            continue
        glyphs, _ = fn.shape(r, {"kern": not tab, "liga": True})
        dx = 0
        for g, gx, gy in glyphs:
            ops = ONE if g == one else fn.rec(g)
            adv = ONE_ADV if g == one else hm[g][0]
            if tab and (g in digits or g == cm[ord("+")]):
                put(ops, x + gx + dx + (TAB - adv) / 2); dx += TAB - hm[g][0]
            else:
                put(ops, x + gx + dx); dx += adv - hm[g][0]
        x += glyphs[-1][1] + dx + hm[glyphs[-1][0]][0]
    ax.add_patch(PathPatch(Path(V, C), fc=color, ec="none"))
    return x * s

def width(text, size, tab=False):
    f2, a2 = plt.subplots(); w = draw(a2, text, 0, 0, size, tab); plt.close(f2); return w

def lab(ax, x, y, t, **k):
    ax.text(x, y, t, family="Malgun Gothic", fontsize=k.pop("fs", 12), **k)

def _figures():
    # ---- 그림 29: ⑨ 안 B — 기본(비례) / 선택 기능 켬(고정폭), 새 1 반영, 오른쪽 맞춤 ----
    rows = ["1,111,111", "9,876,543", "10,450.00", "+12.34%", "−0.71%", "±1.05%", "₩1,203,000"]
    fig, ax = plt.subplots(figsize=(13, 7.4), dpi=130)
    for col, (name, tab) in enumerate([("기본: 비례 숫자 (지금 간격 그대로)", False),
                                       ("선택 기능 켬: 고정폭 숫자 (tnum)", True)]):
        x1 = col * 6 + 5.2
        lab(ax, x1, 0.8, name, ha="right", fs=12, color="#444" if not tab else RED)
        for i, t in enumerate(rows):
            draw(ax, t, x1 - width(t, 0.6, tab), -i * 0.7, 0.6, tab)
        ax.plot([x1, x1], [-len(rows) * 0.7 + 0.45, 0.6], color="#ddd", lw=0.8)
    ax.set_xlim(0, 11.6); ax.set_ylim(-len(rows) * 0.7 + 0.3, 1.25); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "29-draft-figures-B.png")

    # ---- 그림 30: 금융 기호 1순위 시안 — 크게 / Pretendard 비교 / 문장 속 ----
    fig, ax = plt.subplots(figsize=(17, 6.6), dpi=130)
    lab(ax, -0.15, 0.25, "FnGuide 시안", ha="right", color=RED, fs=13)
    x = 0
    for ch, nm in [("₩", "원화"), ("+", "더하기(기준)"), ("−", "빼기"), ("±", "플러스마이너스"), ("×", "곱하기"), ("·", "가운뎃점")]:
        lab(ax, x + 0.02, 0.85, nm, color="#888", fs=10)
        draw(ax, "H" + ch + "H", x, 0, 0.9); x += width("H" + ch + "H", 0.9) + 0.35
    pd = lib.F(lib.UF + "Pretendard-SemiBold.ttf")
    bpp = BoundsPen(pd.gs); pd.gs[pd.tt.getBestCmap()[ord("H")]].draw(bpp)
    lab(ax, -0.15, -0.95, "참고: Pretendard", ha="right", color="#444", fs=13)
    pd.draw(ax, "H₩H  H+H  H−H  H±H  H×H  H·H", 0, -1.2, 0.9 * 0.7 / (bpp.bounds[3] / pd.upm))
    lab(ax, -0.15, -2.15, "문장 속", ha="right", color="#444", fs=13)
    draw(ax, "₩1,203,000  −0.71%  ±1.05  3×4  FnGuide·DataGuide", 0, -2.3, 0.62)
    lab(ax, -0.15, -3.0, "붙임표와 빼기 기호", ha="right", color="#444", fs=13)
    draw(ax, "2026-10-29   −0.71   +0.71", 0, -3.15, 0.62)
    ax.set_xlim(-3.2, 16.5); ax.set_ylim(-3.4, 1.05); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "30-draft-symbols.png")
    print("ok")

if __name__ == "__main__":
    _figures()
