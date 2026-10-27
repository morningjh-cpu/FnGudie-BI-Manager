import sys, os, glob, json, numpy as np
sys.path.insert(0, ".")
from spacing import profile, RES
A = "all"
DIG = ['zero','one','two','three','four','five','six','seven','eight','nine']
def gname(base):
    if base.endswith(("-upper","-lower")): return base.split("-")[0]
    if base.endswith("-number"): return DIG[int(base[0])]
    return base
def kind(g):
    if "_" in g: return "lower"
    if len(g) == 1 and g.isupper(): return "upper"
    if len(g) == 1 and g.islower(): return "lower"
    if g in DIG: return "number"
    return "symbol"
SP = json.load(open("spacing.json"))
Y0, Y1 = 4.0, 34.8                     # 고정 행 구간 (모든 쌍 공통)
PROF = {}
for f in glob.glob(f"{A}/*.svg"):
    g = gname(os.path.basename(f)[:-4])
    ys, L, R, xmin, xmax, _, _ = profile(f)
    sel = (ys >= Y0) & (ys <= Y1)
    PROF[g] = ((L[sel] - xmin) * 32 + SP[g][0],      # 왼쪽 흰 폭(행별, 폰트 단위, 여백 포함)
               (xmax - R[sel]) * 32 + SP[g][1])      # 오른쪽 흰 폭
NAMES = sorted(PROF)
REF = {"upper": "H", "number": "H", "lower": "n", "symbol": "n"}
def gap_rows(a, b, gmax):
    g = PROF[a][1] + PROF[b][0]
    return np.where(np.isnan(g), gmax, np.minimum(g, gmax))
def raw_min_gap(a, b, kern=0):
    g = PROF[a][1] + PROF[b][0] + kern
    return np.nanmin(g) if not np.all(np.isnan(g)) else np.inf
def interaction(a, b, gmax):
    ra, rb = REF[kind(a)], REF[kind(b)]
    m = lambda x, y: gap_rows(x, y, gmax).mean()
    return m(a, b) - m(a, rb) - m(ra, b) + m(ra, rb)
def kern_value(a, b, gmax, k, min_gap=25):
    v = -k * interaction(a, b, gmax)
    mg = raw_min_gap(a, b, v)               # 커닝 후에도 최소 간격 보장
    if mg < min_gap: v += (min_gap - mg)
    return float(np.clip(v, -160, 80))

# ---- v2: 공유 구간(두 글자 모두 잉크가 있는 행)에서의 실효 간격 ----
def eff_gap(a, b, gmax=300, q=None, blend=0.5):
    g = PROF[a][1] + PROF[b][0]
    g = g[~np.isnan(g)]
    if len(g) < 8: return None                       # 겹치는 높이가 거의 없음
    g = np.minimum(g, gmax)
    lo = np.percentile(g, 10)                       # 가장 가까운 부분(시각적으로 지배적)
    return blend * lo + (1 - blend) * g.mean()
def ref_for(a, b):
    ka, kb = kind(a), kind(b)
    if ka == "symbol" and kb == "symbol": return None
    if ka == "symbol": return (a, REF[kb])            # 기호 쌍은 그 기호 + 기준 글자를 기준으로
    if kb == "symbol": return (REF[ka], b)
    return (REF[ka], REF[kb])
def kern_v2(a, b, k=0.7, gmax=300, blend=0.5, min_gap=25):
    r = ref_for(a, b)
    if r is None or (a, b) == r: return 0.0
    e, er = eff_gap(a, b, gmax, blend=blend), eff_gap(*r, gmax, blend=blend)
    if e is None or er is None: return 0.0
    v = k * (er - e)
    mg = raw_min_gap(a, b, v)
    if mg < min_gap: v += (min_gap - mg)
    return float(np.clip(v, -160, 80))

# ---- v3: 면별 측정 편향 제거 (직선 기둥 글자와의 값 = 편향) ----
STRAIGHT_L = {"upper": ["H","I","N","M","B","D","E","P","R"], "lower": ["n","m","r"]}   # 왼쪽이 직선
STRAIGHT_R = {"upper": ["H","I","N","M"],                      "lower": ["n","m","u","a"]}   # 오른쪽이 직선
STRAIGHT_L["number"] = STRAIGHT_L["upper"]; STRAIGHT_R["number"] = STRAIGHT_R["upper"]
def _biasR(a, P):   # a의 오른쪽 면 편향: 같은 유형의 직선-왼쪽 글자들과의 중앙값
    ka = kind(a); ka = "lower" if ka == "symbol" else ka
    return float(np.median([kern_v2(a, x, **P, min_gap=-999) for x in STRAIGHT_L[ka]]))
def _biasL(b, P):
    kb = kind(b); kb = "lower" if kb == "symbol" else kb
    return float(np.median([kern_v2(x, b, **P, min_gap=-999) for x in STRAIGHT_R[kb]]))
_BR, _BL = {}, {}
def kern_v3(a, b, k=0.6, gmax=300, blend=0.5, min_gap=25):
    P = dict(k=k, gmax=gmax, blend=blend)
    key = (k, gmax, blend)
    if (key, a) not in _BR: _BR[(key, a)] = _biasR(a, P) if kind(a) != "symbol" else 0.0
    if (key, b) not in _BL: _BL[(key, b)] = _biasL(b, P) if kind(b) != "symbol" else 0.0
    v = kern_v2(a, b, **P, min_gap=-999) - _BR[(key, a)] - _BL[(key, b)]
    mg = raw_min_gap(a, b, v)
    if mg < min_gap: v += (min_gap - mg)
    return float(np.clip(v, -160, 80))
