import sys, numpy as np
sys.path.insert(0, "/home/claude/font")
from render import ds
import matplotlib; matplotlib.use("Agg")
from matplotlib.path import Path
from render import mpl_path
from scipy import ndimage
from skimage.morphology import skeletonize
RES = 40  # px per unit
def raster(f):
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch
    N = 35 * RES
    fig = plt.figure(figsize=(N/100, N/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    for d in ds(f): ax.add_patch(PathPatch(mpl_path(d), fc="black", ec="none", antialiased=False))
    ax.set_xlim(0, 35); ax.set_ylim(35, 0)
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())[:, :, 0]
    plt.close(fig)
    return img < 128

def stroke_stats(f):
    m = raster(f)
    dt = ndimage.distance_transform_edt(m) / RES
    sk = skeletonize(m)
    w = 2 * dt[sk]
    w = w[w > 0.6]   # 끝단 잡음 제거
    return dict(med=np.median(w), p25=np.percentile(w, 25), p75=np.percentile(w, 75), p90=np.percentile(w, 90),
                ink=m.sum()/RES**2)
if __name__ == "__main__":
    for n in sys.argv[1:]:
        s = stroke_stats(f"all/{n}.svg")
        print(f"{n:14s} median {s['med']:.2f}  p25 {s['p25']:.2f}  p75 {s['p75']:.2f}  p90 {s['p90']:.2f}  ink {s['ink']:.0f}")
