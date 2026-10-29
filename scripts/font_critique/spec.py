import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
cm = fn.tt.getBestCmap()
chars = "".join(chr(c) for c in sorted(cm) if c > 32)
# 1. 글자표
cols = 16; rows = (len(chars) + cols - 1) // cols
fig, ax = plt.subplots(figsize=(16, rows * 1.25), dpi=110)
for i, ch in enumerate(chars):
    r, c = divmod(i, cols); x = c * 1.0; y = -r * 1.25
    ax.add_patch(plt.Rectangle((x, y - 0.3), 0.98, 1.2, fc="#fafafa", ec="#ddd", lw=0.5))
    for yy, col in ((0, "#e88"), (0.498, "#8ae"), (0.7, "#8c8")):
        ax.plot([x, x + 0.98], [y + yy * 0.8, y + yy * 0.8], color=col, lw=0.4)
    w = fn.path(ch, size=0.8)[1]
    fn.draw(ax, ch, x + (0.98 - w) / 2, y, 0.8)
ax.set_xlim(-0.1, cols); ax.set_ylim(-(rows - 1) * 1.25 - 0.4, 1.0); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(OUT + "01-glyph-set.png", bbox_inches="tight"); plt.close()

# 2. 문장 견본
lines = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789 !?&@#%()[]{}.,:;",
         "Hamburgefonstiv Handgloves", "The quick brown fox jumps over the lazy dog",
         "FnGuide DataGuide CompanyGuide FnSpectrum", "office affluent fifty flight", "Wave AVATAR Type LTV Fly 2026"]
fig, ax = plt.subplots(figsize=(16, len(lines) * 1.0), dpi=110)
for i, t in enumerate(lines):
    fn.draw(ax, t, 0, -i * 1.0, 0.62)
ax.set_xlim(-0.1, 17); ax.set_ylim(-len(lines) + 0.6, 0.7); ax.set_aspect("equal"); ax.axis("off")
plt.savefig(OUT + "02-text-specimen.png", bbox_inches="tight"); plt.close()
print(chars)
