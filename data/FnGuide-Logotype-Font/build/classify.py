import sys, json, numpy as np
sys.path.insert(0, "/home/claude/f1/kern")
from autokern import NAMES, kind
M = json.load(open("raw_kern.json"))
TOL = 12
def vec(g, side):
    """side='L': g가 두 번째 글자일 때(왼쪽 면) 모든 첫 글자에 대한 값 / 'R': 첫 글자일 때"""
    return np.array([M.get(f"{x} {g}" if side == "L" else f"{g} {x}", 0.0) for x in NAMES])
def cluster(side):
    out = []
    for kd in ("upper", "lower", "number", "symbol"):
        gs = [g for g in NAMES if kind(g) == kd]
        V = {g: vec(g, side) for g in gs}
        gs.sort(key=lambda g: -np.abs(V[g]).sum())
        groups = []
        for g in gs:
            for grp in groups:
                if all(np.max(np.abs(V[g] - V[h])) <= TOL for h in grp):
                    grp.append(g); break
            else:
                groups.append([g])
        out += [(kd, grp) for grp in groups]
    return out
if __name__ == "__main__":
    for side, lab in (("R", "RIGHT side (as 1st glyph)"), ("L", "LEFT side (as 2nd glyph)")):
        cl = cluster(side)
        multi = [c for c in cl if len(c[1]) > 1]
        print(f"\n{lab}: {len(cl)} classes ({len(multi)} with 2+ members)")
        for kd, grp in cl:
            if len(grp) > 1: print(f"  {kd:7s} {' '.join(grp)}")
        print("  singletons:", " ".join(g for _, grp in cl if len(grp) == 1 for g in grp))
