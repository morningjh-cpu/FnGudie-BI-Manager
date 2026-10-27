"""바뀐 글자(f m M s S y, f 합자)와 상관없는 글자 쌍의 간격은 기존 서체(v1.100) 값으로 고정한다.
kerning.fea 의 '클래스 쌍' 앞에 개별 쌍으로 끼워 넣는다 (개별 쌍이 클래스보다 우선)."""
import sys, re
sys.path.insert(0, ".")
from layout import load
OLD, NEW = sys.argv[1], sys.argv[2]
CH = {"f","m","M","s","S","y","f_b","f_f","f_f_i","f_f_l","f_h","f_i","f_k","f_l"}
o, n = load(OLD), load(NEW)
names = [g for g in o["hm"] if g in n["hm"] and g not in (".notdef", "space")]
pins = [(a, b, o["kern"].get((a, b), 0)) for a in names for b in names
        if a not in CH and b not in CH and abs(o["kern"].get((a, b), 0) - n["kern"].get((a, b), 0)) > 0.5]
fea = open("kerning.fea", encoding="utf-8").read()
marker = "    # ---- 클래스 쌍 ----"
add = "    # ---- 서체 업데이트(v1.200)로 클래스가 다시 묶이며 달라진 쌍을 v1.100 값으로 고정 ----\n" + "".join(f"    pos {a} {b} {int(v)};\n" for a, b, v in pins)
assert marker in fea
open("kerning.fea", "w", encoding="utf-8").write(fea.replace(marker, add + marker))
print("pinned", len(pins))
