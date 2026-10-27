"""최종 강도 조정: 실효 간격을 기준 쌍의 목표 배율로 (글자 1.3 / 문장부호·따옴표 1.4)"""
import sys, json, numpy as np
sys.path.insert(0, ".")
from autokern import PROF, raw_min_gap, kind
from compute_kern import WL
M = json.load(open("raw_kern.json"))
QUOTES = {"quoteright","quotedblright","quotesingle","quotedbl","quoteleft","quotedblleft"}
REFS = {"upper": "H", "lower": "n", "number": "H"}
T_LET, T_SYM = 1.30, 1.40
CAP_LET, CAP_SYM = -180, -200
MIN_GAP = 40
def eff(a, b, k):
    g = PROF[a][1] + PROF[b][0] + k; g = g[~np.isnan(g)]
    return 0.5 * np.percentile(g, 10) + 0.5 * g.mean() if len(g) >= 8 else None
def ref(a, b):
    ra = a if kind(a) == "symbol" else REFS[kind(a)]
    rb = b if kind(b) == "symbol" else REFS[kind(b)]
    if b in QUOTES and kind(a) == "lower": ra = "l"
    if a in QUOTES and kind(b) == "lower": rb = "l"
    return ra, rb
def tune(a, b, cur):
    sym = (a, b) in WL
    t, cap = (T_SYM, CAP_SYM) if sym else (T_LET, CAP_LET)
    ra, rb = ref(a, b)
    e, er = eff(a, b, cur), eff(ra, rb, M.get(f"{ra} {rb}", 0.0))
    if e is None or er is None: return cur
    new = cur - (e - t * er)
    new = min(max(new, cap), 0 if sym else cur + 20)       # 약하게 하는 쪽은 +20까지만
    mg = raw_min_gap(a, b, new)
    if mg < MIN_GAP: new += (MIN_GAP - mg)
    return float(min(new, 0)) if sym else float(new)
if __name__ == "__main__":
    review = [k for k, v in M.items()
              if (tuple(k.split()) in WL) or (all(kind(g) in ("upper", "lower") for g in k.split()) and v <= -30)]
    changed = {}
    for k in review:
        a, b = k.split(); new = round(tune(a, b, M[k]), 1)
        if abs(new - M[k]) >= 1: changed[k] = (M[k], new); M[k] = new
    json.dump(M, open("raw_kern.json", "w"))
    print(f"reviewed {len(review)} pairs, changed {len(changed)}")
    show = ["T o","T a","T e","T n","T y","Y o","Y a","V a","V o","W a","P a","F a","A V","V A","L T","A T","A Y",
            "T period","F period","P period","V period","Y period","r period","y period","T comma","F comma",
            "A quoteright","L quoteright","quoteleft A","T hyphen","f T","F n"]
    for k in show:
        if k in changed: print(f"  {k:14s} {changed[k][0]:7.1f} -> {changed[k][1]:7.1f}")
        elif k in M: print(f"  {k:14s} {M[k]:7.1f}   (unchanged)")
