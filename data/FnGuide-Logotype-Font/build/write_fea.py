import sys, json, numpy as np
sys.path.insert(0, "/home/claude/f1/kern")
from autokern import NAMES, kind
from classify import cluster
M = json.load(open("raw_kern.json"))
r5 = lambda v: int(5 * round(v / 5))
LOGO = {("F","n"): -29, ("n","G"): -2, ("u","i"): 4, ("i","d"): 10, ("d","e"): -10, ("G","u"): 0}
ORDER = {g: i for i, g in enumerate(sorted(NAMES, key=lambda g: (["upper","lower","number","symbol"].index(kind(g)), g)))}
RENAME = {"@R_eight": "@R_digits", "@L_eight": "@L_digits", "@R_ampersand": "@R_symbols", "@L_ampersand": "@L_symbols",
          "@R_quotedbl": "@R_quotes", "@L_quotedblleft": "@L_quotes_open", "@L_quotedbl": "@L_quotes_close",
          "@L_comma": "@L_period_comma", "@R_endash": "@R_dashes", "@L_endash": "@L_dashes",
          "@L_C": "@L_round_UC", "@L_B": "@L_stem_UC", "@L_c": "@L_round_lc", "@L_b": "@L_ascender_lc",
          "@L_n": "@L_stem_lc", "@R_H": "@R_stem_UC", "@R_D": "@R_round_UC"}
def name_classes(cl, side):
    out = []
    for kd, grp in cl:
        grp = sorted(grp, key=lambda g: ORDER[g])
        nm = f"@{side}_{grp[0]}" if len(grp) > 1 else grp[0]
        out.append((RENAME.get(nm, nm), grp))
    return out
RC = name_classes(cluster("R"), "R")    # 첫 글자(오른쪽 면) 클래스
LC = name_classes(cluster("L"), "L")    # 두 번째 글자(왼쪽 면) 클래스
cls_pairs, exceptions = [], {}
for rn, rg in RC:
    for ln, lg in LC:
        vals = {(a, b): M.get(f"{a} {b}", 0.0) for a in rg for b in lg}
        cv = r5(np.median(list(vals.values())))
        if abs(cv) < 10: cv = 0
        if cv: cls_pairs.append((rn, ln, cv))
        for (a, b), v in vals.items():
            gv = r5(v); gv = 0 if abs(gv) < 10 else gv
            if abs(gv - cv) >= 10: exceptions[(a, b)] = gv
for p, v in LOGO.items(): exceptions[p] = v            # 로고 쌍은 정확한 값으로 고정
L = ["# FnGuide Logotype — kerning (1000 UPM)",
     "# 자동 생성: autokern.py → compute_kern.py → classify.py → write_fea.py",
     "# 우선순위: 개별 쌍(로고 쌍·예외) > 클래스 쌍", "",
     "languagesystem DFLT dflt;", "languagesystem latn dflt;", ""]
L.append("# ---- 첫 글자 클래스 (오른쪽 면이 비슷한 글자) ----")
for n, g in RC:
    if len(g) > 1: L.append(f"{n} = [{' '.join(g)}];")
L.append(""); L.append("# ---- 두 번째 글자 클래스 (왼쪽 면이 비슷한 글자) ----")
for n, g in LC:
    if len(g) > 1: L.append(f"{n} = [{' '.join(g)}];")
L += ["", "feature kern {", "    # ---- 로고 기준 쌍 (FnGuide 로고타입에서 측정) ----"]
for (a, b), v in LOGO.items(): L.append(f"    pos {a} {b} {v};")
L.append("    # ---- 개별 예외 ----")
for (a, b), v in sorted(exceptions.items(), key=lambda kv: (ORDER[kv[0][0]], ORDER[kv[0][1]])):
    if (a, b) in LOGO: continue
    L.append(f"    pos {a} {b} {v};")
L.append("    # ---- 클래스 쌍 ----")
for rn, ln, v in sorted(cls_pairs, key=lambda t: t[2]):
    L.append(f"    pos {rn} {ln} {v};")
L += ["} kern;", "",
      "# ---- f 합자 (긴 조합 우선) ----",
      "feature liga {",
      "    sub f f i by f_f_i;", "    sub f f l by f_f_l;", "    sub f f by f_f;",
      "    sub f i by f_i;", "    sub f l by f_l;", "    sub f b by f_b;", "    sub f h by f_h;", "    sub f k by f_k;",
      "} liga;", ""]
open("kerning.fea", "w").write("\n".join(L))
json.dump({"right_classes": RC, "left_classes": LC}, open("classes.json", "w"), indent=1)
print(f"classes: first-glyph {sum(len(g)>1 for _,g in RC)} (+{sum(len(g)==1 for _,g in RC)} single), second-glyph {sum(len(g)>1 for _,g in LC)} (+{sum(len(g)==1 for _,g in LC)} single)")
print(f"class pairs: {len(cls_pairs)} | glyph exceptions: {len(exceptions) - len(LOGO)} | logo pairs: {len(LOGO)}")
