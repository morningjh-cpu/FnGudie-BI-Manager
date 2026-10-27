import sys, os, glob, json, numpy as np
sys.path.insert(0, "/home/claude/k2")
from spacing import profile
from fontTools.ttLib import TTFont
from layout import load
A = "/home/claude/v6/all"
DIG = ['zero','one','two','three','four','five','six','seven','eight','nine']
def gname(base):
    if base.endswith(("-upper","-lower")): return base.split("-")[0]
    if base.endswith("-number"): return DIG[int(base[0])]
    return base
def scan(fontpath, sp=None):
    F = load(fontpath)
    sp = sp or json.load(open("spacing.json"))
    P = {}
    for f in glob.glob(f"{A}/*.svg"):
        g = gname(os.path.basename(f)[:-4])
        ys, L, R, xmin, xmax, _, _ = profile(f)
        P[g] = ((L - xmin) * 32, (xmax - R) * 32)   # 행별 안쪽 흰 깊이 (폰트 단위)
    names = sorted(P)
    out = []
    for a in names:
        ra = P[a][1] + sp[a][1]
        for b in names:
            lb_ = P[b][0] + sp[b][0]
            gap = ra + lb_ + F["kern"].get((a, b), 0)
            ok = ~np.isnan(gap)
            if ok.any(): out.append((float(np.nanmin(gap)), a, b))
    return sorted(out)
