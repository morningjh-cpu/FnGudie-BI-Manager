"""모든 글자 쌍의 실제 흰 간격(커닝 적용 뒤)을 재서 튀는 쌍을 찾는다"""
import numpy as np, lib, json, sys
from PIL import Image, ImageDraw
name = sys.argv[1] if len(sys.argv) > 1 else "FnGuide v1.200"
f = lib.load(name); u = f.upm; cm = f.tt.getBestCmap()
Y0, Y1, STEP = -300, 1000, 5
rows = np.arange(Y0, Y1, STEP)
prof = {}
def profile(ch):
    p, _ = f.path(ch, size=u)
    img = Image.new("1", (3000, Y1 - Y0)); d = ImageDraw.Draw(img)
    for poly in p.to_polygons(closed_only=False):
        d.polygon([(x + 500, Y1 - y) for x, y in poly], fill=1)
    a = np.array(img)
    L = np.full(len(rows), np.nan); R = np.full(len(rows), np.nan)
    for i, y in enumerate(rows):
        r = a[Y1 - y - 1]; xs = np.nonzero(r)[0]
        if len(xs): L[i] = xs[0] - 500; R[i] = xs[-1] + 1 - 500
    return L, R
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,"
for c in chars: prof[c] = profile(c)
def gap(a, b):
    g, adv = f.shape(a + b)
    if len(g) != 2: return None
    x2 = g[1][1]
    d = x2 + prof[b][0] - prof[a][1]
    d = d[~np.isnan(d)]
    return (float(d.min()), float(np.mean(np.sort(d)[:max(3, len(d)//4)]))) if len(d) else None
out = {}
for a in chars:
    for b in chars:
        r = gap(a, b)
        if r: out[a + b] = r
json.dump(out, open(f"pairs-{name.split()[0]}.json", "w"))
ref = {k: out[k][0] for k in ("nn", "HH")}
print(name, "기준 nn", round(ref["nn"]), "HH", round(ref["HH"]), "oo", round(out["oo"][0]), "no", round(out["no"][0]), "OO", round(out["OO"][0]), "HO", round(out["HO"][0]))
def cls(c): return "U" if c.isupper() else "l" if c.islower() else "d" if c.isdigit() else "p"
lc = [(k, v[0]) for k, v in out.items() if k.isalpha() and k.islower()]
uc = [(k, v[0]) for k, v in out.items() if k.isalpha() and k.isupper()]
for label, arr, base in (("소문자", lc, ref["nn"]), ("대문자", uc, ref["HH"])):
    arr.sort(key=lambda t: t[1])
    print(label, "가장 좁음:", [(k, round(v)) for k, v in arr[:15]])
    print(label, "가장 넓음:", [(k, round(v)) for k, v in arr[-15:]])
mixed = sorted([(k, v[0]) for k, v in out.items() if k[0].isupper() and k[1].islower()], key=lambda t: t[1])
print("대+소 좁음:", [(k, round(v)) for k, v in mixed[:12]])
print("대+소 넓음:", [(k, round(v)) for k, v in mixed[-12:]])
