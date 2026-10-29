"""사이트 '폰트 업데이트' 화면 예시 그림 — 모든 그림을 같은 배율로 다시 그림 (2026-10-29).
단위는 화면 픽셀(CSS px). SVG 를 원래 크기로 보여 주므로 그림마다 글자 크기가 같다.
  설명 글자 13px(작은 메모 12px, Pretendard) · 글자 모양 보기 72px · 문장 보기 28px
실제 서체 파일(v1.200, v1.3)로 그리고, 결과는 out/font-critique/img/update/ 에 둔다."""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from fontTools.pens.boundsPen import BoundsPen

OUT = lib.ROOT + "out/font-critique/img/update/"
os.makedirs(OUT, exist_ok=True)
INK, INK2, INK3, RED, LINE = "#1C1C3A", "#5B5866", "#8E8A96", "#B9023D", "#D9CFCA"
LABEL, NOTE, BIG, TEXT = 13, 12, 72, 28            # 설명 · 메모 · 글자 모양 · 문장 (px)
GAP = 12                                            # 설명 글자와 서체 사이
FP = {w: FontProperties(fname=lib.UF + f"Pretendard-{w}.ttf") for w in ("Medium", "SemiBold")}
old = lib.F(lib.ROOT + "out/font-update/v1.200/fonts/FnGuideLogotype-Regular.otf")
new = lib.F(lib.ROOT + "out/font-update/v1.3/fonts/FnGuideLogotype-Regular.otf")

def cap(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm

class Canvas:
    def __init__(s): s.items = []; s.box = [1e9, 1e9, -1e9, -1e9]
    def _grow(s, x0, y0, x1, y1):
        b = s.box; s.box = [min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1)]
    def _path(s, p, color, clip=None):
        s.items.append(("p", p, color, clip))
        if clip: s._grow(clip[0], clip[1], clip[0] + clip[2], clip[1] + clip[3])
        else: e = p.get_extents(); s._grow(e.x0, e.y0, e.x1, e.y1)
    def label(s, x, y, t, size=LABEL, color=INK2, ha="left", w="Medium"):
        """y = 글자 바닥선. 폭을 돌려준다"""
        tp = TextPath((0, 0), t, size=size, prop=FP[w]); e = tp.get_extents()
        dx = {"left": 0, "right": -e.x1, "center": -e.x1 / 2}[ha]
        s._path(tp.transformed(matplotlib.transforms.Affine2D().translate(x + dx, y)), color); return e.x1
    def font(s, f, t, x, y, size, color=INK, feat=None, clip=None):
        p, w = f.path(t, x, y, size, {"kern": True, "liga": True, **(feat or {})})
        if p is not None: s._path(p, color, clip)
        return w
    def line(s, x0, y0, x1, y1, color=LINE, ls=(0, (1, 2)), lw=1):
        s.items.append(("l", (x0, x1), (y0, y1), color, ls, lw)); s._grow(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
    def rect(s, x, y, w, h, color=RED):
        s.items.append(("r", x, y, w, h, color)); s._grow(x, y, x + w, y + h)
    def save(s, name, pad=2):
        x0, y0, x1, y1 = s.box; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
        W, H = x1 - x0, y1 - y0
        fig = plt.figure(figsize=(W / 96, H / 96)); ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.axis("off")
        for it in s.items:
            if it[0] == "p":
                pp = PathPatch(it[1], fc=it[2], ec="none", lw=0); ax.add_patch(pp)
                if it[3]: pp.set_clip_path(Rectangle(it[3][:2], *it[3][2:], transform=ax.transData))
            elif it[0] == "l":
                ax.plot(it[1], it[2], color=it[3], ls=it[4], lw=it[5] * 0.75, solid_capstyle="butt")
            else:
                ax.add_patch(Rectangle(it[1:3], it[3], it[4], fc="none", ec=it[5], lw=0.9, ls=(0, (3, 2))))
        fig.savefig(OUT + name, transparent=True)
        if os.environ.get("PREV"): fig.savefig(os.environ["PREV"] + name[:-4] + ".png", dpi=192, facecolor="white")
        plt.close(fig)
        print(name, round(W), "x", round(H))

def pair(c, f_text, y_top, size, guides=(), right=None, highlight=True):
    """수정 전 / 수정 후 두 줄. 수정 후는 늘어난 부분을 빨갛게. 다음 줄 위치를 돌려준다"""
    y = y_top
    for nm, f, col in [("수정 전", old, INK2), ("수정 후", new, RED)]:
        y -= LABEL; c.label(0, y, nm, color=col); y -= GAP + size * 0.76
        if f is new and highlight: c.font(new, f_text, 0, y, size, RED)
        w = c.font(old if f is new and highlight else f, f_text, 0, y, size)
        for g, txt in guides:
            gy = y + g / 1000 * size
            c.line(-4, gy, w + 6, gy, color=RED if f is new else LINE)
            if txt: c.label(w + 10, gy - 4, txt, size=NOTE, color=RED if f is new else INK3)
        y -= size * 0.24 + 28
    return y

# ---- 수정 전후 종합 (문장 28px) ----
c = Canvas()
lines = ["CompanyGlobal  ETF Global  DataGuide", "Clock Graph  every wavy oxygen",
         "soft lift fjord Portfolio  Il1 2011", "1,203,000  −0.71%  ±1.05  3×4  A·B"]
y = 0
for nm, f, col in [("수정 전", old, INK2), ("수정 후", new, RED)]:
    y -= LABEL; c.label(0, y, nm, color=col); y -= GAP + TEXT * 0.76
    for t in lines: c.font(f, t, 0, y, TEXT); y -= TEXT * 1.5
    y -= 18
c.save("overview.svg")

# ---- 높이 맞춤 3종 (72px, 세 칸에 나란히 들어가도록 폭 300px 안쪽) ----
c = Canvas(); pair(c, "OCG", 0, BIG, [(0, ""), (711, "O 711")]); c.save("height-CG.svg")
c = Canvas(); pair(c, "nvwxy", 0, BIG, [(0, ""), (500, "n 500")]); c.save("height-vwxy.svg")
# o·c·e 넘침은 12 단위(72px 에서 1px 미만)라 위쪽만 3배로 확대해 보여 준다
c = Canvas(); Z = BIG * 2; y = 0
for nm, f, col in [("수정 전", old, INK2), ("수정 후", new, RED)]:
    y -= LABEL; w = c.label(0, y, nm, color=col); c.label(w + 8, y, "위쪽 2배 확대", size=NOTE, color=INK3)
    y -= GAP; top = y; base = top - 0.545 * Z            # 서체 단위 225~545 만 보이게
    clip = (0, top - 0.32 * Z, 236, 0.32 * Z)
    if f is new: c.font(new, "oce", 0, base, Z, RED, clip=clip)
    c.font(old, "oce", 0, base, Z, clip=clip)
    gy = base + 0.5 * Z; c.line(-4, gy, 236, gy, color=LINE); c.label(242, gy - 11, "500", size=NOTE, color=INK3)
    if f is new:
        gy = base + 0.512 * Z; c.line(-4, gy, 236, gy, color=RED); c.label(242, gy + 2, "512", size=NOTE, color=RED)
    y = top - 0.32 * Z - 28
c.save("height-oce.svg")

# ---- ft · fj 합자 (72px) ----
c = Canvas(); pair(c, "soft lift fjord", 0, BIG, highlight=False); c.save("lig-ft-fj.svg")

# ---- 숫자 1 (72px) ----
c = Canvas(); x = 0; base = -LABEL - GAP - BIG * 0.72
for nm, f, col in [("v1.200", old, INK2), ("v1.3", new, RED)]:
    c.label(x, -LABEL, nm, color=col); x += max(c.font(f, "1", x, base, BIG), 60) + 28
c.label(x, -LABEL, "참고: F 왼쪽 위 세리프", color=INK2)
w = c.font(new, "F", x, base, BIG)
c.rect(x - 2, base + 0.54 * BIG, 0.29 * BIG, 0.2 * BIG)
x += max(w, 150) + 36
c.line(x - 18, base - 22, x - 18, -2, color=LINE, ls="-")
c.label(x, -LABEL, "해외 서체의 1 받침 (같은 대문자 높이)", color=INK2)
W = "C:/Windows/Fonts/"
for nm, p in [("Verdana", W + "verdanab.ttf"), ("Tahoma", W + "tahomabd.ttf"),
              ("Calibri", W + "calibrib.ttf"), ("Cambria", W + "cambriab.ttf")]:
    f = lib.F(p); w = c.font(f, "1", x, base, BIG * cap(new) / cap(f))
    c.label(x, base - 22, nm, size=NOTE, color=INK3); x += max(w, 52) + 24
c.save("final-1.svg")

# ---- 소문자 l (72px, 문장 28px) ----
c = Canvas(); x = 0; base = -LABEL - GAP - BIG * 0.76
c.label(x, -LABEL, "v1.200", color=INK2); x += c.font(old, "l", x, base, BIG) + 40
c.label(x, -LABEL, "v1.3", color=RED); gx = x; x += c.font(new, "l", x, base, BIG) + 40
s = BIG / 1000
for xx in (-6, 82, 202, 296):                        # 깃발 끝 · 기둥 왼쪽 · 기둥 오른쪽 · 꼬리 끝
    c.line(gx + xx * s, base - 6, gx + xx * s, base + 0.76 * BIG, color=RED, lw=0.8)
c.label(gx - 6 * s, base - 20, "깃발 88", size=NOTE, color=RED)
c.label(gx + 200 * s, base - 34, "꼬리 94", size=NOTE, color=RED)
x += 20
c.label(x, -LABEL, "참고: t 아래 꼬리", color=INK2)
w = c.font(new, "t", x, base, BIG); c.rect(x + 0.06 * BIG, base - 0.03 * BIG, 0.3 * BIG, 0.17 * BIG)
x += max(w, 110) + 36
c.line(x - 18, base - 34, x - 18, -2, color=LINE, ls="-")
c.label(x, -LABEL, "문장 속", color=INK2)
y = -LABEL - GAP - TEXT * 0.76
for nm, f, col in [("v1.200", old, INK2), ("v1.3", new, RED)]:
    c.label(x, y + 2, nm, color=col); c.font(f, "Il1 little", x + 56, y, TEXT); y -= TEXT * 1.5
c.save("final-l.svg")

# ---- 기본 숫자 / 고정폭 숫자 (28px) ----
rows = ["1,111,111", "9,876,543", "10,450.00", "+12.34%", "−0.71%", "±1.05%"]
c = Canvas(); x = 0
for nm, tab, col in [("기본: 비례 숫자", False, INK2), ("고정폭 숫자 기능을 켠 표", True, RED)]:
    ft = {"tnum": True} if tab else None
    wmax = max(new.path(t, 0, 0, TEXT, {"kern": True, "tnum": tab})[1] for t in rows)
    right = x + max(wmax, 170)
    c.label(right, -LABEL, nm, color=col, ha="right"); y = -LABEL - GAP - TEXT * 0.76
    for t in rows:
        w = new.path(t, 0, 0, TEXT, {"kern": True, "tnum": tab})[1]; c.font(new, t, right - w, y, TEXT, feat=ft); y -= TEXT * 1.5
    c.line(right + 8, y + TEXT * 1.1, right + 8, -LABEL - GAP + 4, color=LINE, ls="-")
    x = right + 80
c.save("tabular.svg")

# ---- 금융 기호 (72px, 문장 28px) ----
c = Canvas(); x = 0; base = -LABEL - GAP - BIG * 0.76
for ch, nm in [("+", "더하기(기준)"), ("−", "빼기"), ("±", "플러스마이너스"), ("×", "곱하기"), ("·", "가운뎃점")]:
    c.label(x, -LABEL, nm, color=INK2); x += c.font(new, "H" + ch + "H", x, base, BIG) + 32
y = base - BIG * 0.24 - 28 - LABEL
c.label(0, y, "문장 속", color=INK2); y -= GAP + TEXT * 0.76
c.font(new, "−0.71%  ±1.05  3×4  FnGuide·DataGuide", 0, y, TEXT)
c.save("symbols.svg")

# ---- v1.31 대문자–숫자 간격 (72px) ----
v13 = lib.F(lib.ROOT + "out/font-update/v1.3/fonts/FnGuideLogotype-Regular.otf")
v131 = lib.F(lib.ROOT + "out/font-update/v1.31/fonts/FnGuideLogotype-Regular.otf")
c = Canvas(); y = 0
for nm, f, col in [("수정 전 (v1.3)", v13, INK2), ("수정 후 (v1.31)", v131, RED)]:
    y -= LABEL; c.label(0, y, nm, color=col); y -= GAP + BIG * 0.72
    c.font(f, "FY2025  T4  7A  V4  L1", 0, y, BIG); y -= BIG * 0.24 + 28
c.save("kern-uc-digit.svg")
