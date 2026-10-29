import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
fig, axs = plt.subplots(2, 1, figsize=(16, 6.4), dpi=120)
for ax, t, lines in ((axs[0], "HCHGHOHSH", [(0, "기준선 0"), (0.700, "대문자 700"), (0.711, "O 711")]),
                     (axs[1], "nonvnwnxnzn", [(0, "기준선 0"), (0.500, "n 500"), (0.485, "v·w·x 485")])):
    w = fn.draw(ax, t, 0, 0, 1.0)
    for y, lab in lines:
        ax.plot([-0.05, w + 0.05], [y, y], color="#B9023D" if lab[0] in "Ovn" else "#59d", lw=0.8)
        pass
    top = max(l[0] for l in lines)
    ax.set_xlim(-0.1, w + 1.3); ax.set_ylim(top - 0.08, top + 0.03) if False else ax.set_ylim(-0.05, top + 0.05)
    ax.set_aspect("equal"); ax.axis("off")
plt.savefig(OUT + "06-alignment.png", bbox_inches="tight"); plt.close()
# 윗부분 확대 (세로 6배 강조 없이, 위쪽 띠만 잘라 크게)
from PIL import Image
crops=[]
for t, y0, y1, ys in (("OHCHGHS", 0.60, 0.73, ((0.700, "#2a7de1"), (0.711, "#B9023D"), (0.688, "#e08a00"))),
                      ("nonvnxs", 0.40, 0.515, ((0.500, "#2a7de1"), (0.485, "#e08a00")))):
    fig = plt.figure(figsize=(16, 16 * (y1 - y0) / 4.6), dpi=200); ax = fig.add_axes([0, 0, 1, 1])
    w = fn.draw(ax, t, 0, 0, 1.0)
    for y, c in ys: ax.plot([-0.05, w], [y, y], color=c, lw=1.2)
    ax.set_xlim(-0.05, -0.05 + 4.6); ax.set_ylim(y0, y1); ax.axis("off")
    p = OUT + f"_c{len(crops)}.png"; fig.savefig(p); plt.close(fig); crops.append(Image.open(p))
W = max(c.width for c in crops); img = Image.new("RGB", (W, sum(c.height + 30 for c in crops)), "white"); y = 0
for c in crops: img.paste(c, (0, y)); y += c.height + 30
img.save(OUT + "07-alignment-zoom.png")
import os
for k in range(len(crops)): os.remove(OUT + f"_c{k}.png")
