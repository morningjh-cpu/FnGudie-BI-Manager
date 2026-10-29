import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib, sys
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
def strip(name, items, size=1.0, gap=0.25, guides=True):
    fig, ax = plt.subplots(figsize=(16, 2.2 * len(items) / 1.0 * 0.6), dpi=110)
    for r, t in enumerate(items):
        y = -r * 1.35 * size
        w = fn.draw(ax, t, 0, y, size)
        if guides:
            for yy, c in ((0, "#e66"), (0.498, "#59d"), (0.7, "#4a4")):
                ax.plot([-0.05, 15], [y + yy*size]*2, color=c, lw=0.6, alpha=.6)
    ax.set_xlim(-0.1, 15); ax.set_ylim(-(len(items)-1)*1.35*size - 0.35*size, 0.95*size)
    ax.set_aspect("equal"); ax.axis("off")
    plt.savefig(OUT + name, bbox_inches="tight"); plt.close()
strip("03-zoom-confusable.png", ["Il1| Ill1 IlI", "O0 oO0 B8 S5 Z2"], 1.0)
strip("04-zoom-spacing.png", ["fifty ft fj fy", "hijk ijk nijn", "rn m  cl d  vv w"], 1.0)
strip("05-zoom-round.png", ["HOHOH nonon", "HxH ExE oxo"], 1.0)
