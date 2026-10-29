import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from fontTools.pens.boundsPen import BoundsPen
OUT = lib.ROOT + "out/font-critique/img/"
names = ["FnGuide v1.200", "Rotis Semi Sans Bold", "Candara Bold", "Helvetica Neue Medium", "Avenir Next Demi", "Futura Medium", "DIN Medium"]
fonts = {n: lib.load(n) for n in names}
def capH(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm
def sheet(fname, text, cap=0.55, rowh=1.0, width=14):
    fig, ax = plt.subplots(figsize=(16, len(names) * 1.05), dpi=110)
    for i, n in enumerate(names):
        f = fonts[n]; size = cap / capH(f); y = -i * rowh
        ax.text(-0.15, y + cap * 0.3, n.replace(" v1.200", "\nv1.200"), ha="right", va="center", fontsize=10, color="#B9023D" if "FnGuide" in n else "#555")
        for yy in (0, cap):
            ax.plot([0, width], [y + yy] * 2, color="#ccc", lw=0.5)
        f.draw(ax, text, 0, y, size, color="#111")
    ax.set_xlim(-2.4, width); ax.set_ylim(-(len(names) - 1) * rowh - 0.3, cap + 0.35); ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(OUT + fname, bbox_inches="tight"); plt.close()
sheet("10-compare-handgloves.png", "Handgloves HOHOH nonon")
sheet("11-compare-brand.png", "FnGuide DataGuide 2026")
# 같은 크기 o·n·O·H 겹쳐 보기: 굵기 대비
fig, axs = plt.subplots(1, len(names), figsize=(16, 3.2), dpi=110)
for ax, n in zip(axs, names):
    f = fonts[n]; size = 1 / capH(f)
    w = f.draw(ax, "Ho", 0, 0, size)
    ax.set_title(n, fontsize=9, color="#B9023D" if "FnGuide" in n else "#333")
    ax.set_xlim(-0.05, 2.5); ax.set_ylim(-0.1, 1.1); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(OUT + "12-compare-contrast.png", bbox_inches="tight"); plt.close()
