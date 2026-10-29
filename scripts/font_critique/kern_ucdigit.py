"""대문자–숫자 커닝 계산 (v1.31).
v1.3 에는 대문자↔숫자 쌍의 커닝이 하나도 없다. 이 서체의 기존 대문자끼리 커닝에서 '얼마나 조이는지(K)'를 배워
같은 방식으로 대문자→숫자, 숫자→대문자 520쌍의 값을 계산하고, 해외 서체 값과 비교해 다듬는다.
  실효 간격 = 두 글자 모두 잉크가 있는 높이에서의 가로 간격 (가장 가까운 10% 와 평균의 반반, 300 이상은 300)
  상호작용 = eff(a,H) + eff(H,b) − eff(H,H) − eff(a,b)    (H 와 붙을 때보다 더 벌어져 보이는 만큼)
결과: out/font-update/work/kern_uc_digit.json  {"A one": -40, ...}"""
import json, numpy as np, lib
from fontTools.pens.boundsPen import BoundsPen

NEW = lib.ROOT + "out/font-update/v1.3/fonts/FnGuideLogotype-Regular.otf"
OUT = lib.ROOT + "out/font-update/work/kern_uc_digit.json"
UC = [chr(c) for c in range(65, 91)]
DG = "0123456789"
ROWS = np.arange(-20, 721, 5)                # 바닥선~대문자 높이 + 넘침 (숫자 높이도 이 안)
GMAX, MIN_GAP = 300, 30                       # 대문자끼리 최소 간격과 같은 30

class Prof:
    def __init__(s, path):
        s.f = lib.F(path); s.cm = s.f.tt.getBestCmap(); s.hm = s.f.tt["hmtx"]; s.P = {}
        s.upm = s.f.upm
    def name(s, ch): return s.cm[ord(ch)]
    def adv(s, ch): return s.hm[s.name(ch)][0]
    def prof(s, ch):
        """행마다 (왼쪽 잉크 x, 오른쪽 잉크 x), 잉크 없으면 nan — 서체 단위"""
        if ch in s.P: return s.P[ch]
        p, _ = s.f.path(ch, 0, 0, s.upm, {"kern": False, "liga": False})
        L = np.full(len(ROWS), np.nan); R = np.full(len(ROWS), np.nan)
        for poly in p.to_polygons(closed_only=False):
            a, b = poly, np.roll(poly, -1, axis=0)
            for i, y in enumerate(ROWS * s.upm / 1000):
                m = (a[:, 1] > y) != (b[:, 1] > y)
                if not m.any(): continue
                xs = a[m, 0] + (y - a[m, 1]) * (b[m, 0] - a[m, 0]) / (b[m, 1] - a[m, 1])
                L[i] = np.nanmin([L[i], xs.min()]); R[i] = np.nanmax([R[i], xs.max()])
        s.P[ch] = (L, R); return s.P[ch]
    def kern(s, a, b):
        g, w = s.f.shape(a + b, {"kern": True, "liga": False})
        return g[1][1] - s.adv(a)
    def rows(s, a, b, k=0):
        La, Ra = s.prof(a); Lb, Rb = s.prof(b)
        return (s.adv(a) - Ra) + Lb + k
    def eff(s, a, b, k=None):
        k = s.kern(a, b) if k is None else k
        g = s.rows(a, b, k); g = g[~np.isnan(g)]
        if len(g) < 8: return None
        g = np.minimum(g, GMAX)
        return 0.5 * np.percentile(g, 10) + 0.5 * g.mean()
    def min_gap(s, a, b, k):
        g = s.rows(a, b, k); return np.nanmin(g)
    def inter(s, a, b):
        return s.eff(a, "H") + s.eff("H", b) - s.eff("H", "H") - s.eff(a, b, 0)

fn = Prof(NEW)

# ---- 1. 기준 ----
# 이 서체는 대문자끼리 −55 를 공통으로 조였고(로고 리듬), 숫자끼리는 조이지 않았다.
# 그래서 대문자 옆 숫자가 대문자끼리보다 약 50 넓다 (H0 162 vs HO 110, 실효 간격).
# 대문자–숫자는 그 사이(반)로: 공통 −25.
COMMON = -25
# 모양 때문에 생기는 차이(T4, 7A 처럼 빈 공간이 큰 쌍)는 원래 커닝 엔진과 같은 비율 0.6, 60 넘는 부분은 반만.
K = 0.6
def compress(v, knee=60): return v if abs(v) <= knee else np.sign(v) * (knee + 0.5 * (abs(v) - knee))
def inter0(a, b):
    """커닝 없이 잰 상호작용 (+면 H 기준 예상보다 더 벌어져 보임)"""
    return fn.eff(a, b, 0) - (fn.eff(a, "H", 0) + fn.eff("H", b, 0) - fn.eff("H", "H", 0))
# ---- 2. 해외 서체: 같은 쌍의 커닝을 대문자 높이 700 기준으로 환산 ----
W = "C:/Windows/Fonts/"
REF = {"Helvetica Neue": lib.UF + "HelveticaNeue-Medium.otf", "Avenir Next": lib.UF + "AvenirNextLTPro-Demi.otf",
       "Inter": lib.UF + "Inter_18pt-Medium.ttf", "DIN": W + "DIN Medium.otf", "Futura": W + "Futura Medium.otf",
       "Rotis Semi Sans": lib.UF + "RotisSemiSansStd-Bold.otf", "Candara": W + "Candarab.ttf",
       "Segoe UI": W + "seguisb.ttf", "Calibri": W + "calibrib.ttf", "Cambria": W + "cambriab.ttf",
       "Georgia": W + "georgiab.ttf", "Verdana": W + "verdanab.ttf"}
refs = {}
for nm, p in REF.items():
    try:
        r = Prof(p); bp = BoundsPen(r.f.gs); r.f.gs[r.name("H")].draw(bp); r.scale = 700 / bp.bounds[3]; refs[nm] = r
    except Exception as e: print("건너뜀", nm, e)
def ref_vals(a, b):
    return [refs[n].kern(a, b) * refs[n].scale for n in refs]

# ---- 3. 520쌍 계산 ----
res = {}
for a, b in [(u, d) for u in UC for d in DG] + [(d, u) for d in DG for u in UC]:
    shape = float(compress(-K * inter0(a, b)))
    v = COMMON + shape
    rv = np.array(ref_vals(a, b))
    v = float(np.clip(v, -120, 30))
    mg = fn.min_gap(a, b, v)
    if mg < MIN_GAP: v += MIN_GAP - mg
    v = int(5 * round(v / 5))
    res[f"{a} {b}"] = dict(v=v, shape=round(shape), inter=round(rv.min()) if len(rv) else 0,
                          ref_n=int((np.abs(rv) >= 10).sum()), gap=round(float(fn.min_gap(a, b, v))))
json.dump(res, open(OUT.replace(".json", "-detail.json"), "w"), indent=0)
G = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
final = {" ".join(G.get(c, c) for c in k.split()): d["v"] for k, d in res.items() if abs(d["v"]) >= 10}
json.dump(final, open(OUT, "w"), indent=0)
print("쌍", len(final), "/ 520")
vals = np.array([d["v"] for d in res.values()]); print("분포", np.percentile(vals, [0, 10, 50, 90, 100]))
for k, d in sorted(res.items(), key=lambda t: t[1]["v"])[:45]:
    print(f"  {k}  {d['v']:5d}  (모양 {d['shape']:5d}, Inter {d['inter']:5d}, 최소간격 {d['gap']})")
for k, d in sorted(res.items(), key=lambda t: -t[1]["v"])[:10]:
    print(f"  {k}  {d['v']:5d}  (모양 {d['shape']:5d}, Inter {d['inter']:5d}, 최소간격 {d['gap']})")
inter_pairs = [(k, d) for k, d in res.items() if d["inter"] <= -10]
print("Inter 가 조이는 쌍", len(inter_pairs)); [print("  ", k, d["v"], d["inter"]) for k, d in inter_pairs]
