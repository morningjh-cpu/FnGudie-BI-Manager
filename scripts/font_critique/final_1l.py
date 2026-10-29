"""폰트 업데이트 화면용: v1.3 의 숫자 1 받침·소문자 l 꼬리를 실제 서체 파일로 그린 그림 (반영된 최종안만).
40: 1 — v1.200 / v1.3 / 참고한 F 왼쪽 위 세리프 / 해외 서체의 1 받침 너비
41: l — v1.200 / v1.3(깃발 88·꼬리 94 표시) / 참고한 t 아래 꼬리"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from fontTools.pens.boundsPen import BoundsPen
OUT = lib.ROOT + "out/font-critique/img/"
RED = "#B9023D"
old = lib.F(lib.ROOT + "out/font-update/v1.200/fonts/FnGuideLogotype-Regular.otf")
new = lib.F(lib.ROOT + "out/font-update/v1.3/fonts/FnGuideLogotype-Regular.otf")

def capH(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm
def lab(ax, x, y, t, **k):
    ax.text(x, y, t, family="Malgun Gothic", fontsize=k.pop("fs", 12), **k)

# ---- 그림 40: 숫자 1 ----
fig, ax = plt.subplots(figsize=(16, 3.6), dpi=130)
x = 0
for name, f, c in [("v1.200", old, "#444"), ("v1.3", new, RED)]:
    lab(ax, x, 0.86, name, color=c, fs=13); x += f.draw(ax, "1", x, 0, 1.0) + 0.35
lab(ax, x, 0.86, "참고: F 왼쪽 위 세리프", color="#444", fs=13)
w = new.draw(ax, "F", x, 0, 1.0)
ax.add_patch(plt.Rectangle((x + 0.01, 0.55), 0.26, 0.17, fc="none", ec=RED, lw=1.5, ls="--"))
x += w + 0.6
ax.plot([x - 0.3, x - 0.3], [-0.02, 0.9], color="#ddd", lw=1)
lab(ax, x, 0.86, "해외 서체의 1 받침 (같은 대문자 높이)", color="#444", fs=13)
W = "C:/Windows/Fonts/"
for nm, p in [("Verdana", W + "verdanab.ttf"), ("Tahoma", W + "tahomabd.ttf"), ("Calibri", W + "calibrib.ttf"), ("Cambria", W + "cambriab.ttf")]:
    f = lib.F(p); lab(ax, x, -0.1, nm, color="#888", fs=10)
    x += f.draw(ax, "1", x, 0, 0.7 / capH(f)) + 0.25
ax.set_xlim(-0.1, x); ax.set_ylim(-0.16, 0.95); ax.set_aspect("equal"); ax.axis("off")
lib.save(OUT + "40-final-1.png")

# ---- 그림 41: 소문자 l ----
fig, ax = plt.subplots(figsize=(12, 3.8), dpi=130)
x = 0
lab(ax, x, 0.86, "v1.200", color="#444", fs=13); x += old.draw(ax, "l", x, 0, 1.0) + 0.45
lab(ax, x, 0.93, "v1.3", color=RED, fs=13)
gx = x; x += new.draw(ax, "l", x, 0, 1.0) + 0.45
for xx in (-6, 82, 202, 296):                       # 깃발 끝 · 기둥 왼쪽 · 기둥 오른쪽 · 꼬리 끝
    ax.plot([gx + xx / 1000] * 2, [-0.05, 0.75], color=RED, lw=0.8, ls=":")
lab(ax, gx + 0.0, 0.77, "깃발 88", color=RED, fs=10); lab(ax, gx + 0.2, -0.09, "꼬리 94", color=RED, fs=10)
lab(ax, x, 0.86, "참고: t 아래 꼬리", color="#444", fs=13)
w = new.draw(ax, "t", x, 0, 1.0)
ax.add_patch(plt.Rectangle((x + 0.05, -0.03), 0.3, 0.17, fc="none", ec=RED, lw=1.5, ls="--"))
x += w + 0.6
lab(ax, x, 0.86, "문장 속", color="#444", fs=13)
for i, (nm, f, c) in enumerate([("v1.200", old, "#444"), ("v1.3", new, RED)]):
    lab(ax, x, 0.5 - i * 0.32 + 0.08, nm, color=c, fs=10)
    f.draw(ax, "Il1 little", x + 0.45, 0.5 - i * 0.32, 0.3)
ax.set_xlim(-0.1, x + 2.2); ax.set_ylim(-0.14, 1.02); ax.set_aspect("equal"); ax.axis("off")
lib.save(OUT + "41-final-l.png")
print("ok")
