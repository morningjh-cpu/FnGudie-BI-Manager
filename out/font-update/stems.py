import sys, os, glob, numpy as np
sys.path.insert(0, ".")
from weight import raster, RES
CAP, XH, BASE = 6.37, 12.67, 28.24
def runs(row):
    d = np.diff(np.concatenate([[0], row.astype(int), [0]]))
    s = np.where(d == 1)[0]; e = np.where(d == -1)[0]
    return [(a / RES, b / RES) for a, b in zip(s, e)]
out = {}
for f in sorted(glob.glob("all/*.svg")):
    n = os.path.basename(f)[:-4]
    if "_" in n or not n.endswith(("-upper", "-lower")): continue
    m = raster(f)
    top = CAP if n.endswith("upper") else XH
    ws = []
    # 기둥이 있는 구간: 윗 세리프·아랫 세리프를 피해 몸통 가운데 (높이 35%~80%)
    for y in np.arange(top + 0.35 * (BASE - top), top + 0.8 * (BASE - top), 0.1):
        for a, b in runs(m[int(y * RES)]):
            if 2.8 <= b - a <= 5.2: ws.append(round(b - a, 2))
    if ws:
        v, c = np.unique(np.round(np.array(ws) / 0.05) * 0.05, return_counts=True)
        out[n] = (float(v[np.argmax(c)]), float(np.median(ws)), len(ws))
for kind in ("upper", "lower"):
    items = sorted([(k.split("-")[0], v) for k, v in out.items() if k.endswith(kind)], key=lambda kv: -kv[1][1])
    med = np.median([v[1] for _, v in items])
    print(f"== {kind}  (전체 중앙값 {med:.2f})")
    print("  ".join(f"{k}:{v[1]:.2f}" for k, v in items))
