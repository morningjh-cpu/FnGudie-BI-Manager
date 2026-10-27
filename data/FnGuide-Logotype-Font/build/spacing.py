import sys, os, glob, numpy as np
sys.path.insert(0, "/home/claude/f1/kern"); sys.path.insert(0, "/home/claude/font")
from weight import raster, RES
XH, CAP, BASE = 12.67, 6.37, 28.24
_cache = {}
def profile(path):
    """행마다 가장 왼쪽/오른쪽 잉크 x (단위: 글리프 좌표). 잉크 없는 행은 NaN"""
    if path in _cache: return _cache[path]
    m = raster(path)
    cols = np.arange(m.shape[1]) / RES + 0.5/RES
    has = m.any(axis=1)
    L = np.where(has, cols[np.argmax(m, axis=1)], np.nan)
    R = np.where(has, cols[m.shape[1]-1-np.argmax(m[:, ::-1], axis=1)], np.nan)
    ys = np.arange(m.shape[0]) / RES + 0.5/RES
    xs = cols[m.any(axis=0)]
    _cache[path] = (ys, L, R, xs.min(), xs.max(), ys[has].min(), ys[has].max())
    return _cache[path]
def zone_of(name, y0, y1):
    if "_" in name: return XH, BASE
    if name.endswith("-lower"): return XH, BASE
    if name.endswith("-upper") or name.endswith("-number"): return CAP, BASE
    return y0, y1                     # 기호: 자기 높이 범위
def inner_white(path, name, depth):
    """구역 안 평균 흰 깊이 (왼쪽, 오른쪽). depth로 깊이 제한"""
    ys, L, R, xmin, xmax, y0, y1 = profile(path)
    z0, z1 = zone_of(name, y0, y1)
    sel = (ys >= z0) & (ys <= z1)
    Lz = np.where(np.isnan(L[sel]), xmin + depth, np.minimum(L[sel], xmin + depth))
    Rz = np.where(np.isnan(R[sel]), xmax - depth, np.maximum(R[sel], xmax - depth))
    return float(np.mean(Lz - xmin)), float(np.mean(xmax - Rz)), xmin, xmax
def sidebearings(path, name, w, depth):
    """평균 흰 폭이 w가 되도록 (lsb, rsb) — 글리프 단위"""
    aL, aR, xmin, xmax = inner_white(path, name, depth)
    return w - aL, w - aR
