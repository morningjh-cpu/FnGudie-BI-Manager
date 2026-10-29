import numpy as np, lib, json, sys
from fontTools.pens.boundsPen import BoundsPen
def runs(mask, coords):
    """True 구간 [(시작,끝)]"""
    out=[]; on=None
    for v,c in zip(mask,coords):
        if v and on is None: on=c
        if not v and on is not None: out.append((on,c)); on=None
    if on is not None: out.append((on,coords[-1]))
    return out
def gpath(f, ch):
    p,_ = f.path(ch, size=f.upm); return p
from matplotlib.path import Path
def inside(f,ch,pts):
    """짝홀 규칙: 점을 감싸는 윤곽 수가 홀수면 안쪽"""
    n=np.zeros(len(pts),int)
    for poly in gpath(f,ch).to_polygons(closed_only=False):
        n+=Path(poly).contains_points(pts)
    return n%2==1
def hscan(f,ch,y,x0=-200,x1=2500):
    xs=np.arange(x0,x1,0.5); return runs(inside(f,ch,np.c_[xs,np.full_like(xs,y)]),xs)
def vscan(f,ch,x,y0=-400,y1=1200):
    ys=np.arange(y0,y1,0.5); return runs(inside(f,ch,np.c_[np.full_like(ys,x),ys]),ys)
def bbox(f,ch):
    g=f.tt.getBestCmap()[ord(ch)]; bp=BoundsPen(f.gs); f.gs[g].draw(bp); return bp.bounds
def adv(f,ch): return f.tt["hmtx"][f.tt.getBestCmap()[ord(ch)]][0]
res={}
for name in [n for n in lib.FONTS if n!='FnGuide (logo)' and n!='Inter Medium']:
    f=lib.load(name); u=f.upm
    H=bbox(f,"H"); cap=H[3]; x=bbox(f,"x"); xh=x[3]
    O=bbox(f,"O"); o=bbox(f,"o"); l=bbox(f,"l"); p=bbox(f,"p")
    Hs=hscan(f,"H",cap*0.3); stemH=Hs[0][1]-Hs[0][0]
    cx=(H[0]+H[2])/2; bar=[r for r in vscan(f,"H",cx) if r[0]>0][0]; barH=bar[1]-bar[0]
    ns=hscan(f,"n",xh*0.3); stem_n=ns[0][1]-ns[0][0]
    Os=hscan(f,"O",cap*0.5); Oside=Os[0][1]-Os[0][0]
    ocx=(O[0]+O[2])/2; Ov=vscan(f,"O",ocx); Otop=Ov[-1][1]-Ov[-1][0]; Obot=Ov[0][1]-Ov[0][0]
    os_=hscan(f,"o",xh*0.5); oside=os_[0][1]-os_[0][0]
    ov=vscan(f,"o",(o[0]+o[2])/2); otop=ov[-1][1]-ov[-1][0]
    def msb(ch, y):  # 글자 중간 높이에서 잰 왼쪽·오른쪽 여백
        rr=hscan(f,ch,y); return rr[0][0], adv(f,ch)-rr[-1][1]
    lsb=lambda ch: msb(ch, (cap if ch.isupper() else xh)*0.5)[0]; rsb=lambda ch: msb(ch,(cap if ch.isupper() else xh)*0.5)[1]
    k=1000/cap  # 대문자 높이 1000 기준으로 맞춤
    r=dict(xh_cap=xh/cap, asc_cap=l[3]/cap, desc_cap=-p[1]/cap,
        O_over_top=(O[3]-cap)*k, O_over_bot=-O[1]*k, o_over_top=(o[3]-xh)*k, o_over_bot=-o[1]*k,
        stemH=stemH*k, barH=barH*k, stem_n=stem_n*k, n_vs_H=stem_n/stemH, O_side=Oside*k, O_top=Otop*k,
        contrast_O=Otop/Oside, O_bot=Obot*k, counter_n=(ns[1][0]-ns[0][1])*k, counter_H=(Hs[1][0]-Hs[0][1])*k, contrast_H=barH/stemH, o_side=oside*k, o_top=otop*k,
        wH=adv(f,"H")*k, wO=adv(f,"O")*k, wn=adv(f,"n")*k, wo=adv(f,"o")*k,
        O_H=adv(f,"O")/adv(f,"H"), o_n=adv(f,"o")/adv(f,"n"),
        sbH=(lsb("H")*k, rsb("H")*k), sbO=(lsb("O")*k, rsb("O")*k), sbn=(lsb("n")*k, rsb("n")*k), sbo=(lsb("o")*k,rsb("o")*k),
        sbn_stem=lsb("n")/stem_n, sbH_stem=lsb("H")/stemH)
    res[name]={kk:(tuple(round(float(v),1) for v in vv) if isinstance(vv,tuple) else round(vv,3)) for kk,vv in r.items()}
json.dump(res,open("metrics.json","w"),indent=1)
keys=list(next(iter(res.values())).keys())
names=list(res)
print("항목".ljust(14)+"".join(n[:12].rjust(13) for n in names))
for kk in keys: print(kk.ljust(14)+"".join(str(res[n][kk]).rjust(13) for n in names))
