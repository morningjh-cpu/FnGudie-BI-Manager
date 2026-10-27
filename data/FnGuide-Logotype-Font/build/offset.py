import sys, numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.basePen import BasePen
sys.path.insert(0, "/home/claude/font")
from render import ds
from weight import raster, RES

class Flatten(BasePen):
    """곡선을 촘촘한 점열로 펼침 (곡선 길이에 비례해 분할)"""
    def __init__(self, step=0.08):
        super().__init__(None); self.cs, self.cur, self.step = [], [], step
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        L = sum(np.hypot(b[0]-a[0], b[1]-a[1]) for a, b in ((p0,p1),(p1,p2),(p2,p3)))
        n = max(2, int(L / self.step))
        for i in range(1, n+1):
            t = i/n; u = 1-t
            self.cur.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                             u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        self._curveToOne((p0[0]+2/3*(p1[0]-p0[0]), p0[1]+2/3*(p1[1]-p0[1])),
                         (p2[0]+2/3*(p1[0]-p2[0]), p2[1]+2/3*(p1[1]-p2[1])), p2)
    def _closePath(self):
        c = self.cur
        if len(c) > 1 and np.hypot(c[0][0]-c[-1][0], c[0][1]-c[-1][1]) < 1e-6: c = c[:-1]
        self.cs.append(np.array(c)); self.cur = []
    _endPath = _closePath

def dedupe(c, eps=1e-4):
    keep = [c[0]]
    for p in c[1:]:
        if np.hypot(*(p - keep[-1])) > eps: keep.append(p)
    return np.array(keep)

def offset_contour(c, delta, mask):
    """각 변을 법선 방향으로 delta만큼 평행 이동 후 이웃 변과 교차(마이터) → 획 두께를 2·delta만큼 줄임"""
    c = dedupe(c); n = len(c)
    d = np.roll(c, -1, axis=0) - c
    L = np.hypot(d[:, 0], d[:, 1]); d = d / L[:, None]
    nrm = np.c_[-d[:, 1], d[:, 0]]          # 왼쪽 법선
    # 채움(잉크)이 어느 쪽인지 마스크로 판정: 가장 긴 변의 중점에서 양쪽을 찍어 봄
    i = int(np.argmax(L)); mid = c[i] + d[i] * L[i] / 2
    def ink(p):
        x, y = int(p[0]*RES), int(p[1]*RES)
        return 0 <= x < mask.shape[1] and 0 <= y < mask.shape[0] and mask[y, x]
    side = 1 if ink(mid + nrm[i]*0.05) else -1   # +1: 잉크가 왼쪽
    shift = nrm * side * delta                   # 잉크 쪽(안쪽)으로 이동
    out = []
    for k in range(n):
        a0, da = c[k-1] + shift[k-1], d[k-1]
        b0, db = c[k] + shift[k], d[k]
        cross = da[0]*db[1] - da[1]*db[0]
        if abs(cross) < 1e-3:                    # 거의 평행: 단순 이동
            out.append(c[k] + shift[k]); continue
        t = ((b0[0]-a0[0])*db[1] - (b0[1]-a0[1])*db[0]) / cross
        p = a0 + da * t
        if np.hypot(*(p - c[k])) > 4 * delta:    # 너무 뾰족한 모서리는 마이터 제한
            p = c[k] + (shift[k-1] + shift[k]) / 2
        out.append(p)
    return np.array(out)

def rdp(pts, eps):
    """Ramer–Douglas–Peucker (닫힌 윤곽은 두 극점으로 나눠 처리)"""
    def _r(p):
        if len(p) < 3: return p
        a, b = p[0], p[-1]; ab = b - a; L = np.hypot(*ab)
        dist = np.abs(np.cross(ab, p - a)) / L if L > 0 else np.hypot(*(p - a).T)
        i = int(np.argmax(dist))
        if dist[i] > eps: return np.vstack([_r(p[:i+1])[:-1], _r(p[i:])])
        return np.array([a, b])
    j = int(np.argmax(np.hypot(*(pts - pts[0]).T)))
    A = _r(np.vstack([pts[:j+1]])); B = _r(np.vstack([pts[j:], pts[:1]]))
    return np.vstack([A[:-1], B[:-1]])

def thin_glyph(svg_in, delta, eps=0.006):
    mask = raster(svg_in)
    out = []
    for d in ds(svg_in):
        fp = Flatten(); parse_path(d, fp)
        parts = []
        for c in fp.cs:
            o = rdp(offset_contour(c, delta, mask), eps)
            parts.append("M" + "L".join(f"{x:.3f},{y:.3f}" for x, y in o) + "Z")
        out.append("".join(parts))
    return out

def _seg_x(p1, p2, p3, p4):
    d1, d2 = p2 - p1, p4 - p3
    den = d1[0]*d2[1] - d1[1]*d2[0]
    if abs(den) < 1e-12: return None
    t = ((p3[0]-p1[0])*d2[1] - (p3[1]-p1[1])*d2[0]) / den
    u = ((p3[0]-p1[0])*d1[1] - (p3[1]-p1[1])*d1[0]) / den
    if 1e-9 < t < 1-1e-9 and 1e-9 < u < 1-1e-9: return p1 + d1 * t
    return None

def remove_loops(c, window=60):
    """오프셋으로 생긴 작은 자기교차 고리를 잘라냄 (가까운 인덱스 범위의 교차만 검사)"""
    changed = True
    while changed:
        changed = False
        n = len(c)
        for i in range(n):
            a, b = c[i], c[(i+1) % n]
            for k in range(2, min(window, n-1)):
                j = (i + k) % n
                p = _seg_x(a, b, c[j], c[(j+1) % n])
                if p is not None:
                    if i + k < n:   # i+1..j 구간(고리)을 교차점 하나로 대체
                        c = np.vstack([c[:i+1], [p], c[j+1:]])
                    else:           # 시작점을 넘어가는 고리
                        c = np.vstack([[p], c[(j+1):i+1]])
                    changed = True; break
            if changed: break
    return c

def thin_glyph(svg_in, delta, eps=0.006):
    mask = raster(svg_in)
    out = []
    for d in ds(svg_in):
        fp = Flatten(); parse_path(d, fp)
        parts = []
        for c in fp.cs:
            o = remove_loops(offset_contour(c, delta, mask))
            o = rdp(o, eps)
            parts.append("M" + "L".join(f"{x:.3f},{y:.3f}" for x, y in o) + "Z")
        out.append("".join(parts))
    return out
