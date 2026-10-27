"""대문자–대문자 리듬 조정: 공통 조임(T) + 새 H–H 기준으로 사선·돌출 쌍 재최적화 (강화만)"""
import sys, json, numpy as np
sys.path.insert(0, ".")
from autokern import raw_min_gap, kind
from tune_kern import eff
T = -55                    # API 로고 P→I 에서 측정한 대문자 공통 조임 (-56)
TARGET, CAP = 1.30, -180
MIN_GAP = 30               # 대문자끼리 최소 윤곽 간격
M = json.load(open("raw_kern_v1000.json"))
UC = [k for k in M if all(kind(g) == "upper" for g in k.split())]
before = {k: M[k] for k in UC}
for k in UC: M[k] = M[k] + T
ref = eff("H", "H", M["H H"])
stronger = 0
for k in UC:
    a, b = k.split(); e = eff(a, b, M[k])
    if e is not None and e > TARGET * ref:
        M[k] = max(M[k] - (e - TARGET * ref), CAP); stronger += 1
    mg = raw_min_gap(a, b, M[k])
    if mg < MIN_GAP: M[k] += MIN_GAP - mg
json.dump(M, open("raw_kern.json", "w"))
print(f"UC–UC pairs {len(UC)} | common {T} | re-optimized {stronger} | new H–H eff ref {ref:.0f} (was {eff('H','H',before['H H']):.0f})")
for k in ["H H","A P","P I","A V","V A","L T","A T","A Y","T A","P A","K O","F A","L V","R V","W A","Y A","O V","T T","E T","S T"]:
    if k in before: print(f"  {k:5s} {before[k]:7.1f} -> {M[k]:7.1f}   min gap {raw_min_gap(*k.split(), M[k]):5.0f}")
