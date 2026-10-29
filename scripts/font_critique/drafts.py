"""개선 권장 ⑥(1·I·l 구분)·⑨(고정폭 숫자·금융 기호) 시안 그림.
서체 파일은 고치지 않고, 그림 위에서만 글자 윤곽을 바꿔 보여 준다."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
cm = fn.tt.getBestCmap()
RED = "#B9023D"

# ---- 시안 글자 윤곽 (서체 단위, 1000 = 한 칸) ----
def poly(*pts):
    return [("M", [pts[0]])] + [("L", [p]) for p in pts[1:]] + [("Z", [])]
# 안 A: 숫자 1 — 아래 받침을 달고 깃발을 조금 길게 (Verdana·IBM Plex 계열). 폭 376 → 450
ONE_A = poly((60, 0), (390, 0), (390, 64), (294, 64), (294, 655), (236, 655), (24, 560), (24, 506), (155, 543), (155, 64), (60, 64))
ONE_ADV = 450
# 안 B: 소문자 l — 아래 끝을 오른쪽으로 꺾은 꼬리 (Inter 대체 글자·Fira Sans·Ubuntu 계열)
L_B = [("M", [(-6, 627)]), ("L", [(0, 627)]), ("C", [(74, 625), (82, 590), (82, 564)]),
       ("L", [(82, 170)]), ("C", [(82, 40), (130, -11), (215, -11)]),
       ("C", [(240, -11), (262, -7), (284, -1)]), ("L", [(284, 92)]),
       ("C", [(268, 88), (250, 86), (236, 86)]), ("C", [(212, 86), (202, 104), (202, 150)]),
       ("L", [(202, 697)]), ("L", [(-6, 661)]), ("Z", [])]

def gname(ch): return cm[ord(ch)]

def draw(ax, text, x0, y0, size, color="#111", over=None, adv=None, shift=None, kern=True):
    """over: {글자이름: 윤곽}, adv: {글자이름: 새 폭}, shift: {글자이름: 오른쪽 이동}"""
    over, adv, shift = over or {}, adv or {}, shift or {}
    glyphs, _ = fn.shape(text, None if kern else {"kern": False, "liga": True})
    s = size / fn.upm; V, C = [], []; dx = 0
    hm = fn.tt["hmtx"]
    for g, gx, gy in glyphs:
        ops = over.get(g) or fn.rec(g)
        sh = shift.get(g, 0)
        for op, pts in ops:
            P = [(x0 + (gx + dx + sh + px) * s, y0 + (gy + py) * s) for px, py in pts]
            V += P if P else [(0, 0)]
            C += {"M": [Path.MOVETO], "L": [Path.LINETO], "C": [Path.CURVE4] * 3,
                  "Q": [Path.CURVE3] * 2, "Z": [Path.CLOSEPOLY]}[op]
        if g in adv: dx += adv[g] - hm[g][0]
    ax.add_patch(PathPatch(Path(V, C), fc=color, ec="none"))
    return (glyphs[-1][1] + dx + hm[glyphs[-1][0]][0]) * s

def label(ax, x, y, t, **k):
    ax.text(x, y, t, fontsize=k.pop("fs", 11), family="Malgun Gothic", **k)

def finish(name, ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(OUT + name, bbox_inches="tight"); plt.close()

# ---- 그림 20: 참고 서체의 1·I·l ----
def capH(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm
refs = [("FnGuide v1.200 (지금)", lib.FONTS["FnGuide v1.200"], None),
        ("Helvetica Neue — 1 깃발이 길다", lib.FONTS["Helvetica Neue Medium"], None),
        ("DIN — l 아래 꼬리", lib.FONTS["DIN Medium"], None),
        ("Rotis Semi Sans — 1 깃발이 길다", lib.FONTS["Rotis Semi Sans Bold"], None),
        ("Verdana — I에 위아래 받침, 1에 받침", "C:/Windows/Fonts/verdana.ttf", None),
        ("Inter 기본", lib.UF + "Inter_18pt-Medium.ttf", None),
        ("Inter 구분 글자(l 꼬리 cv05 · I 받침 cv08)", lib.UF + "Inter_18pt-Medium.ttf", {"cv05": True, "cv08": True}),]
fig, ax = plt.subplots(figsize=(14, len(refs) * 0.95), dpi=120)
y = 0
for name, path, feat in refs:
    f = lib.F(path); size = 0.55 / capH(f)
    feats = {"kern": True, "liga": True, **(feat or {})}
    f.draw(ax, "Il1  Ill1  1Il", 3.6, y, size, color=RED if "FnGuide" in name else "#111", features=feats)
    label(ax, 3.4, y + 0.2, name, ha="right", color=RED if "FnGuide" in name else "#444")
    y -= 0.85
finish("20-ref-Il1.png", ax, (-0.2, 10.5), (y + 0.6, 0.75))

# ---- 그림 21: ⑥ 시안 A·B ----
one, ell = gname("1"), gname("l")
rows = [("지금", {}, {}),
        ("안 A · 1 받침", {one: ONE_A}, {one: ONE_ADV}),
        ("안 B · l 꼬리", {ell: L_B}, {ell: 300}),
        ("A + B 함께", {one: ONE_A, ell: L_B}, {ell: 300, one: ONE_ADV})]
fig, ax = plt.subplots(figsize=(15, 7.2), dpi=120)
y = 0
for name, over, adv in rows:
    label(ax, -0.15, y + 0.2, name, ha="right", fs=13, color=RED if name != "지금" else "#444")
    draw(ax, "Il1 Ill1 1Il", 0, y, 0.75, over=over, adv=adv)
    draw(ax, "Illinois 2011 Fill", 6.3, y, 0.75, over=over, adv=adv)
    y -= 1.1
finish("21-draft-Il1.png", ax, (-2.6, 14), (y + 0.75, 0.75))

# ---- 그림 22: 참고 서체의 숫자 방식 ----
nums = ["1,111,111", "9,876,543", "+12.34%", "-0.71%"]
fig, ax = plt.subplots(figsize=(15, 6.6), dpi=120)
col = 0
for name, path, feat in [("Helvetica Neue\n(기본이 고정폭)", lib.FONTS["Helvetica Neue Medium"], None),
                         ("Inter 기본\n(비례 숫자)", lib.UF + "Inter_18pt-Medium.ttf", None),
                         ("Inter + 고정폭 기능\n(tnum 켬)", lib.UF + "Inter_18pt-Medium.ttf", {"tnum": True}),
                         ("FnGuide v1.200\n(지금: 비례만)", lib.FONTS["FnGuide v1.200"], None)]:
    f = lib.F(path); size = 0.42 / capH(f); x1 = col * 3.6 + 3.1
    label(ax, x1, 0.75, name, ha="right", fs=11, color=RED if "FnGuide" in name else "#444")
    for i, t in enumerate(nums):
        w = f.path(t, size=size, features={"kern": True, **(feat or {})})[1]
        f.draw(ax, t, x1 - w, -i * 0.7, size, features={"kern": True, **(feat or {})})
    ax.plot([x1, x1], [-len(nums) * 0.7 + 0.4, 0.55], color="#ddd", lw=0.8)
    col += 1
finish("22-ref-figures.png", ax, (0, 14.6), (-len(nums) * 0.7 + 0.3, 1.2))

# ---- 그림 23: ⑨ 시안 A·B (고정폭 숫자, 오른쪽 맞춤 표) ----
TAB = 600  # 고정폭 숫자 한 칸 (지금 숫자 폭 평균 약 584)
digits = [gname(c) for c in "0123456789"]
hm = fn.tt["hmtx"]
tab_adv = {g: TAB for g in digits}
tab_shift = {g: (TAB - hm[g][0]) / 2 for g in digits}
fig, ax = plt.subplots(figsize=(15, 6.6), dpi=120)
for col, (name, kw) in enumerate([("지금 (비례 숫자)", {}),
                                  ("고정폭 숫자 (안 A 기본값 / 안 B 선택 기능)", dict(adv=tab_adv, shift=tab_shift)),
                                  ("고정폭 + 1 받침(⑥ 안 A)", dict(adv=tab_adv, shift={**tab_shift, one: (TAB - ONE_ADV) / 2}, over={one: ONE_A}))]):
    x1 = col * 4.6 + 4.1
    label(ax, x1, 0.75, name, ha="right", fs=11, color="#444" if col == 0 else RED)
    for i, t in enumerate(["1,111,111", "9,876,543", "10,450.00", "1,203"]):
        # 폭을 먼저 재고 오른쪽 맞춤
        fig2, ax2 = plt.subplots(); w = draw(ax2, t, 0, 0, 0.6, **kw); plt.close(fig2)
        draw(ax, t, x1 - w, -i * 0.7, 0.6, **kw)
    ax.plot([x1, x1], [-3 * 0.7 - 0.1, 0.55], color="#ddd", lw=0.8)
finish("23-draft-figures.png", ax, (0, 14), (-3 * 0.7 - 0.3, 1.2))
print("done")

# ---- 그림 24: ⑥ 시안 크게 ----
fig, axs = plt.subplots(1, 3, figsize=(15, 3.6), dpi=120)
for ax, (name, over, adv) in zip(axs, [("지금", {}, {}), ("안 A · 1 받침", {one: ONE_A}, {one: ONE_ADV}), ("안 B · l 꼬리", {ell: L_B}, {ell: 300})]):
    w = draw(ax, "Il1", 0, 0, 1.0, over=over, adv=adv, kern=False)
    ax.set_title(name, family="Malgun Gothic", fontsize=13, color="#444" if name == "지금" else RED)
    ax.set_xlim(-0.1, 1.5); ax.set_ylim(-0.08, 0.78); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(OUT + "24-draft-Il1-zoom.png", bbox_inches="tight"); plt.close()

# ---- 그림 25: 금융 기호 참고 + ₩ 시안 ----
SYM = "₩ − ± × · — … ° ‰ ▲▼"
fig, ax = plt.subplots(figsize=(15, 4.4), dpi=120)
y = 0
for name, path in [("Pretendard", lib.UF + "Pretendard-SemiBold.ttf"), ("Inter", lib.UF + "Inter_18pt-Medium.ttf"), ("Segoe UI", "C:/Windows/Fonts/seguisb.ttf")]:
    f = lib.F(path); size = 0.5 / capH(f)
    label(ax, 2.2, y + 0.15, name, ha="right", color="#444")
    f.draw(ax, "100" + SYM, 2.4, y, size)
    y -= 0.85
# FnGuide ₩ 시안: W 위에 가로획 두 개 (한국 원화 표기에서 흔한 두 줄형)
label(ax, 2.2, y + 0.15, "FnGuide ₩ 시안", ha="right", color=RED)
s = 0.5 / 0.7
w100 = draw(ax, "100", 2.4, y, s)
wx = 2.4 + w100 + 0.02
wW = draw(ax, "W", wx, y, s)
for by in (0.30, 0.43):
    ax.add_patch(plt.Rectangle((wx - 0.02, y + by * s), wW + 0.04, 0.045 * s, fc="#111", ec="none"))
label(ax, wx + wW + 0.25, y + 0.15, "← W 윤곽에 가로획 두 줄 (모양은 디자이너가 다듬어야 함)", color="#888", fs=10)
finish("25-ref-symbols.png", ax, (-0.2, 12.5), (y - 0.25, 0.75))
print("done2")
