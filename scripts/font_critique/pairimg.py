import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
from fontTools.pens.boundsPen import BoundsPen
OUT = lib.ROOT + "out/font-critique/img/"
def capH(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3] / f.upm
def sheet(fname, lines, names, cap=0.5):
    fig, ax = plt.subplots(figsize=(16, len(lines) * len(names) * 0.62), dpi=110)
    y = 0
    for t in lines:
        for n in names:
            f = lib.load(n); size = cap / capH(f)
            ax.text(-0.15, y + cap * 0.35, n, ha="right", va="center", fontsize=9, color="#B9023D" if "FnGuide" in n else "#666")
            f.draw(ax, t, 0, y, size); y -= 0.85
        y -= 0.25
    ax.set_xlim(-2.6, 15); ax.set_ylim(y + 0.6, cap + 0.3); ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(OUT + fname, bbox_inches="tight"); plt.close()
N = ["FnGuide v1.200", "Helvetica Neue Medium", "Rotis Semi Sans Bold"]
sheet("13-pairs-caps.png", ["HLYH HLTH HLVH HAVAH HAWAH HTAH", "HTo Te Ta Ty Yo Va P. F. T. V."], N)
sheet("14-pairs-lower.png", ["nftn nfjn nfin ntyn nrvn nijn hijk", "fifty after soft lift rift rvery"], N)
