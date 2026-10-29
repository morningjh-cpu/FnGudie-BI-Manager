"""작은 화면 크기(px)로 실제 픽셀에 찍어 본 뒤 4배 확대 (힌팅 없는 회색 단계 렌더링에 가까움)"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib, numpy as np
from PIL import Image
OUT = lib.ROOT + "out/font-critique/img/"
from matplotlib.backends.backend_agg import FigureCanvasAgg
def raster(f, text, px):
    W = int(px * 22); Hh = int(px * 1.6)
    fig = plt.figure(figsize=(W / 100, Hh / 100), dpi=100); ax = fig.add_axes([0, 0, 1, 1])
    f.draw(ax, text, 0.1 * px, 0.4 * px, px)
    ax.set_xlim(0, W); ax.set_ylim(0, Hh); ax.axis("off")
    c = FigureCanvasAgg(fig); c.draw(); a = np.asarray(c.buffer_rgba())[:, :, :3].copy(); plt.close(fig)
    return a
rows = []
text = "FnGuide DataGuide 2026 Il1 office affluent"
for n in ["FnGuide v1.200", "Helvetica Neue Medium", "Rotis Semi Sans Bold"]:
    f = lib.load(n)
    for px in (11, 13, 16, 20):
        a = raster(f, text, px)
        img = Image.fromarray(a).resize((a.shape[1] * 3, a.shape[0] * 3), Image.NEAREST)
        rows.append((f"{n}  {px}px", img))
W = max(i.width for _, i in rows); Ht = sum(i.height + 22 for _, i in rows)
sheet = Image.new("RGB", (W + 10, Ht), "white")
from PIL import ImageDraw, ImageFont
d = ImageDraw.Draw(sheet); fnt = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
y = 0
for label, img in rows:
    d.text((6, y + 3), label, fill=(185, 2, 61) if "FnGuide" in label else (90, 90, 90), font=fnt)
    sheet.paste(img, (0, y + 20)); y += img.height + 22
sheet.save(OUT + "15-small-sizes.png")
