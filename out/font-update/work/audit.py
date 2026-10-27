import sys, os, glob, numpy as np
sys.path.insert(0, "/home/claude/d1"); sys.path.insert(0, ".")
from weight import raster, RES
A = os.environ.get("GLYPHS", "all")
ORIG = set(f[:-4] for f in os.listdir("/home/claude/build/src"))
PROV = set(f[:-4] for f in os.listdir("/home/claude/v3/clean")) | {"ampersand","percent","quoteright","quotedblright","a-lower"}
def src(n):
    if n in PROV: return "user"
    if n in ORIG: return "logo"
    return "draft"
_M = {}
def mask(n):
    if n not in _M: _M[n] = raster(f"{A}/{n}.svg")
    return _M[n]
def runs_row(n, y):
    r = mask(n)[int(y * RES)]
    d = np.diff(np.r_[0, r.astype(int), 0]); s = np.where(d == 1)[0]; e = np.where(d == -1)[0]
    return [(a / RES, b / RES) for a, b in zip(s, e)]
def runs_col(n, x):
    c = mask(n)[:, int(x * RES)]
    d = np.diff(np.r_[0, c.astype(int), 0]); s = np.where(d == 1)[0]; e = np.where(d == -1)[0]
    return [(a / RES, b / RES) for a, b in zip(s, e)]
def extent(n):
    m = mask(n); ys = np.where(m.any(axis=1))[0]; xs = np.where(m.any(axis=0))[0]
    return xs[0]/RES, ys[0]/RES, (xs[-1]+1)/RES, (ys[-1]+1)/RES
def top_at(n, x):   # 특정 x에서의 가장 위 잉크
    r = runs_col(n, x); return r[0][0] if r else None
