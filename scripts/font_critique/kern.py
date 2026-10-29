import lib, numpy as np
from fontTools.pens.boundsPen import BoundsPen
names = ["FnGuide v1.200", "Rotis Semi Sans Bold", "Candara Bold", "Helvetica Neue Medium", "Avenir Next Demi", "DIN Medium"]
pairs = ["AV","AW","AT","AY","VA","TA","YA","LT","LV","LY","LW","PA","FA","To","Te","Ta","Vo","Va","Yo","Ty","T.","P.","F.","V.","Y.","r.","y.","ft","fj","ij","ty","rv"]
def capH(f):
    bp = BoundsPen(f.gs); f.gs[f.tt.getBestCmap()[ord("H")]].draw(bp); return bp.bounds[3]
print("짝".ljust(5) + "".join(n[:11].rjust(12) for n in names))
for p in pairs:
    row = p.ljust(5)
    for n in names:
        f = lib.load(n); k = 1000 / capH(f)
        g, adv = f.shape(p); g0 = f.shape(p[0])[1]
        kern = (g[1][1] - g0) * k if len(g) == 2 else float("nan")
        row += (f"{kern:.0f}" if len(g)==2 else "합자").rjust(12)
    print(row)
