"""로고 보정 스페이싱 (v0.500과 같은 규칙): 평균 흰 폭 대문자·숫자 2.70, 소문자 1.80, 깊이 2.0 (글리프 단위)"""
import sys, os, glob, json
sys.path.insert(0, ".")
from spacing import sidebearings
A = "all"
DEPTH, W = 2.0, {"upper": 2.70, "number": 2.70, "lower": 1.80, "symbol": 1.80}
DIG = ['zero','one','two','three','four','five','six','seven','eight','nine']
sp = {}
for f in sorted(glob.glob(f"{A}/*.svg")):
    base = os.path.basename(f)[:-4]
    kind = base.split("-")[1] if base.endswith(("-upper","-lower","-number")) else ("lower" if "_" in base else "symbol")
    g = base if "_" in base else base.split("-")[0] if kind in ("upper","lower") else DIG[int(base[0])] if kind == "number" else base
    l, r = sidebearings(f, base, W[kind], DEPTH); sp[g] = [round(l*32), round(r*32)]
FIXED = {"plus":(50,50), "less":(45,45), "greater":(45,45), "asciicircum":(40,40), "numbersign":(35,35), "percent":(30,30),
         "dollar":(40,40), "at":(30,30), "slash":(15,15), "backslash":(15,15), "question":(30,30), "grave":(30,30), "ampersand":(25,15)}
for g, v in FIXED.items(): sp[g] = list(v)
for g, side in (("bracketleft",1),("parenleft",1),("braceleft",1),("bracketright",0),("parenright",0),("braceright",0)):
    sp[g][side] = max(sp[g][side], 30)
sp["braceleft"][0] = max(sp["braceleft"][0], 15); sp["braceright"][1] = max(sp["braceright"][1], 15)
json.dump(sp, open("spacing.json", "w"), indent=1)
old = json.load(open("spacing_old.json"))
print("changed sidebearings:", {g: (old[g], sp[g]) for g in sp if old.get(g) != sp[g]})
