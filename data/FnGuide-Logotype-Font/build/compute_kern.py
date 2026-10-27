import sys, json, numpy as np
sys.path.insert(0, "/home/claude/f1/kern")
from autokern import kern_v3, raw_min_gap, eff_gap, NAMES, kind
P = dict(k=0.65, gmax=500, blend=0.5)
MIN_GAP = 25
QUOTES_L = ["quoteleft", "quotedblleft"]
QUOTES_R = ["quoteright", "quotedblright", "quotesingle", "quotedbl"]
WL = {}
for a in ["T","V","W","Y","F","P","r","v","w","y"]:
    for b in ["period", "comma"]: WL[(a, b)] = -80
for q in QUOTES_L + QUOTES_R:
    for L in ["A","T","V","W","Y"]: WL[(q, L)] = -70; WL[(L, q)] = -70
    WL[("L", q)] = -70
for d in ["hyphen", "endash"]:
    for L in ["T","V","W","Y","A"]: WL[(d, L)] = -60; WL[(L, d)] = -60
K_SYM = 0.45
def compress(v, knee=60):
    return v if abs(v) <= knee else np.sign(v) * (knee + 0.5 * (abs(v) - knee))
def collision_only(a, b):
    mg = raw_min_gap(a, b); return max(0.0, MIN_GAP - mg) if mg < MIN_GAP else 0.0
def sym_ref(a, b):
    sym, other, sym_left = (a, b, True) if kind(a) == "symbol" else (b, a, False)
    ref = "H" if kind(other) == "upper" else ("l" if sym in QUOTES_L + QUOTES_R else "n")
    return (sym, ref) if sym_left else (ref, sym)
def value(a, b):
    ka, kb = kind(a), kind(b)
    if "number" in (ka, kb): return collision_only(a, b)            # 숫자: 충돌 방지만
    if "symbol" in (ka, kb):
        if (a, b) not in WL: return collision_only(a, b)
        e, er = eff_gap(a, b, P["gmax"], blend=P["blend"]), eff_gap(*sym_ref(a, b), P["gmax"], blend=P["blend"])
        v = 0.0 if (e is None or er is None) else float(np.clip(K_SYM * (er - e), WL[(a, b)], 0))
        mg = raw_min_gap(a, b, v)
        return v + (MIN_GAP - mg if mg < MIN_GAP else 0)
    v = compress(kern_v3(a, b, **P, min_gap=-999))
    mg = raw_min_gap(a, b, v)
    return float(v + (MIN_GAP - mg if mg < MIN_GAP else 0))
if __name__ == "__main__":
    M = {}
    for a in NAMES:
        for b in NAMES:
            if kind(a) == "symbol" and kind(b) == "symbol": continue
            M[f"{a} {b}"] = round(value(a, b), 1)
    json.dump(M, open("raw_kern.json", "w"))
    v = np.array(list(M.values()))
    print(f"{len(M)} pairs | |kern|>=10: {(abs(v)>=10).sum()}  >=50: {(abs(v)>=50).sum()}")
    ll = {k: x for k, x in M.items() if all(len(t) == 1 for t in k.split())}
    print("letters most negative:", [(k, round(x)) for k, x in sorted(ll.items(), key=lambda kv: kv[1])[:24]])
    print("letters most positive:", [(k, round(x)) for k, x in sorted(ll.items(), key=lambda kv: -kv[1])[:14]])
    sy = {k: x for k, x in M.items() if not all(len(t) == 1 for t in k.split()) and abs(x) >= 10}
    print("symbol/digit pairs:", len(sy), [(k, round(x)) for k, x in sorted(sy.items(), key=lambda kv: kv[1])][:30])
    print("  positive:", [(k, round(x)) for k, x in sorted(sy.items(), key=lambda kv: -kv[1])][:12])
    chk = ["F n","A V","V A","T o","L T","A T","Y o","P A","h o","n o","o o","H O","W a","r period","T period","A quoteright","quoteleft A","T hyphen"]
    print("check:", [(c, round(M[c])) for c in chk])
