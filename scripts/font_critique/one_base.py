"""⑥ 안 A 수정 시안: 숫자 1 — 윗부분은 지금 깃발 그대로, 아래 받침은 F 왼쪽 위 세리프를
위아래로 뒤집어 기둥 양쪽에 좌우 대칭으로 붙임. 서체 파일은 고치지 않는다."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from matplotlib.path import Path
from matplotlib.patches import PathPatch
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
cm = fn.tt.getBestCmap(); hm = fn.tt["hmtx"]
RED = "#B9023D"
one = cm[ord("1")]

# F 왼쪽 위 세리프 윤곽 (기둥 왼쪽 면 x=132, 윗면 y=700 기준으로 잰 값: 바깥으로 dx, 아래로 dy)
F_SERIF = [(106, 0), (106, 36), "C", (83, 39), (29, 47), (14, 62), "C", (-1, 76), (0, 112), (0, 138)]

# 받침 너비 기준: 1 에 받침이 있는 해외 서체 7종(Verdana·Tahoma·Calibri·Cambria·Times·Palatino·Book Antiqua, 굵은 꼴)
#   받침/기둥 2.45~2.90(가운데 2.72), 받침/0 너비 0.71~0.88(0.81), 받침/대문자 높이 0.53~0.67(0.62)
#   FnGuide 에 맞춘 값: 기둥 139 → 378, 0 너비 544 → 441, 대문자 700 × (1 높이 655/700) → 406. 세 값의 가운데쯤인 420 을 쓴다.
BASE_W = 420

def one_with_base(base_w=BASE_W):
    L, R = 155, 294            # 지금 1 의 기둥 왼쪽·오른쪽 면
    k = (base_w - (R - L)) / 2 / 106            # F 세리프(기둥 밖 106)를 가로로만 늘리는 비율
    sh = max(0, 27 - (L - 106 * k))             # 왼쪽 끝이 깃발 끝(27)보다 나가면 글자를 오른쪽으로 민다
    left = lambda dx_, dy_: (L - dx_ * k, dy_)      # 뒤집어서 왼쪽 아래에
    right = lambda dx_, dy_: (R + dx_ * k, dy_)     # 좌우로 한 번 더 뒤집어서 오른쪽 아래에
    ops = [("M", [(236, 655)]), ("L", [(27, 580)]), ("L", [(27, 538)]), ("L", [(44, 541)]),
           ("C", [(63, 545), (82, 549), (101, 549)]), ("C", [(140, 549), (155, 534), (155, 497)])]
    # 왼쪽: 기둥(L,138) → 곡선 → 끝(L-106, 36) → 바닥
    ops += [("L", [left(0, 138)]),
            ("C", [left(0, 112), left(-1, 76), left(14, 62)]),
            ("C", [left(29, 47), left(83, 39), left(106, 36)]),
            ("L", [left(106, 0)])]
    # 오른쪽: 바닥 → 끝(R+106, 36) → 곡선 → 기둥(R,138)
    ops += [("L", [right(106, 0)]), ("L", [right(106, 36)]),
            ("C", [right(83, 39), right(29, 47), right(14, 62)]),
            ("C", [right(-1, 76), right(0, 112), right(0, 138)]),
            ("L", [(R, 655)]), ("Z", [])]
    ops = [(op, [(x + sh, y) for x, y in pts]) for op, pts in ops]
    adv = R + 106 * k + sh + 27    # 오른쪽 여백을 왼쪽(깃발 끝 27)과 같게
    return ops, round(adv)

def draw(ax, text, x0, y0, size, over=None, adv=None, shift=None, color="#111"):
    over, adv, shift = over or {}, adv or {}, shift or {}
    glyphs, _ = fn.shape(text)
    s = size / fn.upm; V, C = [], []; dx = 0
    for g, gx, gy in glyphs:
        for op, pts in over.get(g) or fn.rec(g):
            P = [(x0 + (gx + dx + shift.get(g, 0) + px) * s, y0 + (gy + py) * s) for px, py in pts]
            V += P if P else [(0, 0)]
            C += {"M": [Path.MOVETO], "L": [Path.LINETO], "C": [Path.CURVE4] * 3,
                  "Q": [Path.CURVE3] * 2, "Z": [Path.CLOSEPOLY]}[op]
        if g in adv: dx += adv[g] - hm[g][0]
    ax.add_patch(PathPatch(Path(V, C), fc=color, ec="none"))
    return (glyphs[-1][1] + dx + hm[glyphs[-1][0]][0]) * s

def lab(ax, x, y, t, **k):
    ax.text(x, y, t, family="Malgun Gothic", fontsize=k.pop("fs", 12), **k)

NEW, NEW_ADV = one_with_base()
if __name__ == "__main__": print("새 1 폭", NEW_ADV)

def _figures():
    # 그림 26: 크게 — 지금 / 이전 안 A / 수정 안 A, 그리고 참고 F·E·L
    fig, ax = plt.subplots(figsize=(15, 4.2), dpi=130)
    x = 0
    for name, over, adv in [("지금", {}, {}), ("수정 안 A", {one: NEW}, {one: NEW_ADV})]:
        lab(ax, x + 0.05, 0.86, name, color=RED if "수정" in name else "#444", fs=14)
        x += draw(ax, "1", x, 0, 1.0, over=over, adv=adv) + 0.35
    lab(ax, x + 0.05, 0.86, "참고: F 왼쪽 위 세리프", color="#444", fs=14)
    w = draw(ax, "F", x, 0, 1.0)
    ax.add_patch(plt.Rectangle((x + 0.01, 0.55), 0.26, 0.17, fc="none", ec=RED, lw=1.5, ls="--"))
    ax.set_xlim(-0.1, x + w + 0.1); ax.set_ylim(-0.08, 0.95); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "26-draft-1-base.png")

    # 그림 27: 글자·숫자 속에서 (비례 숫자 / 고정폭 숫자)
    digits = [cm[c] for c in map(ord, "0123456789")]
    TAB = 600
    tab_adv = {g: TAB for g in digits}
    tab_shift = {g: (TAB - hm[g][0]) / 2 for g in digits}
    tab_shift[one] = (TAB - NEW_ADV) / 2
    fig, ax = plt.subplots(figsize=(15, 6.4), dpi=130)
    rows = [("지금", "Il1  Illinois 2011  1,111,111", {}, {}, {}),
            ("수정 안 A", "Il1  Illinois 2011  1,111,111", {one: NEW}, {one: NEW_ADV}, {}),
            ("수정 안 A + 고정폭", "Il1  Illinois 2011  1,111,111", {one: NEW}, {**tab_adv, one: TAB}, tab_shift)]
    y = 0
    for name, t, over, adv, sh in rows:
        lab(ax, -0.15, y + 0.2, name, ha="right", color=RED if "수정" in name else "#444", fs=13)
        draw(ax, t, 0, y, 0.72, over=over, adv=adv, shift=sh)
        y -= 1.05
    ax.set_xlim(-2.9, 14.2); ax.set_ylim(y + 0.75, 0.75); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "27-draft-1-base-text.png")

    # 그림 28: 해외 서체의 받침 너비와 비교 (대문자 높이를 같게 맞춤)
    from fontTools.pens.boundsPen import BoundsPen
    def capH(f):
        bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm
    W = "C:/Windows/Fonts/"
    refs = [("Verdana", W + "verdanab.ttf"), ("Tahoma", W + "tahomabd.ttf"), ("Calibri", W + "calibrib.ttf"),
            ("Cambria", W + "cambriab.ttf"), ("Times", W + "timesbd.ttf"), ("Palatino", W + "palab.ttf")]
    OLD, OLD_ADV = one_with_base(139 + 2 * 106)
    fig, ax = plt.subplots(figsize=(18, 3.4), dpi=130)
    x = 0
    for name, path in refs:
        f = lib.F(path); size = 0.7 / capH(f)
        lab(ax, x + 0.02, 0.86, name, color="#444", fs=12)
        f.draw(ax, "1H", x, 0, size); x += 1.75
    for name, over, adv, c in [("FnGuide 직전 시안 (351)", {one: OLD}, {one: OLD_ADV}, "#888"),
                               ("FnGuide 조정 (420)", {one: NEW}, {one: NEW_ADV}, RED)]:
        lab(ax, x + 0.02, 0.86, name, color=c, fs=12)
        draw(ax, "1H", x, 0, 1.0, over=over, adv=adv, color="#111"); x += 2.3
    ax.set_xlim(-0.1, x); ax.set_ylim(-0.08, 0.95); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "28-ref-1-base-width.png")

if __name__ == "__main__":
    _figures()
