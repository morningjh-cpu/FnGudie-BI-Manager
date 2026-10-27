"""폰트의 advance + GPOS 쌍 커닝으로 문자열을 직접 배치 (matplotlib는 커닝을 적용하지 않으므로)"""
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from matplotlib.path import Path
def load(path):
    f = TTFont(path); gs = f.getGlyphSet(); cmap = f.getBestCmap(); hm = f["hmtx"].metrics
    kern = {}
    if "GPOS" in f:
        for lk in f["GPOS"].table.LookupList.Lookup:
            for st in lk.SubTable:
                if st.Format == 1:
                    for i, first in enumerate(st.Coverage.glyphs):
                        for pvr in st.PairSet[i].PairValueRecord:
                            kern.setdefault((first, pvr.SecondGlyph), getattr(pvr.Value1, "XAdvance", 0) or 0)
                elif st.Format == 2:
                    c1 = st.ClassDef1.classDefs; c2 = st.ClassDef2.classDefs
                    seconds = {}
                    for g in f.getGlyphOrder(): seconds.setdefault(c2.get(g, 0), []).append(g)
                    for first in st.Coverage.glyphs:
                        rec = st.Class1Record[c1.get(first, 0)]
                        for ci, r2 in enumerate(rec.Class2Record):
                            v = getattr(r2.Value1, "XAdvance", 0) or 0 if r2.Value1 else 0
                            if v:
                                for sg in seconds.get(ci, []): kern.setdefault((first, sg), v)
    ligs = {}
    if "GSUB" in f:
        for lk in f["GSUB"].table.LookupList.Lookup:
            for st in lk.SubTable:
                if hasattr(st, "ligatures"):
                    for first, seq in st.ligatures.items():
                        for lg in seq: ligs[tuple([first] + lg.Component)] = lg.LigGlyph
    return dict(gs=gs, cmap=cmap, hm=hm, kern=kern, ligs=ligs)
def shape(F, text, liga=True):
    gl = [F["cmap"].get(ord(ch), ".notdef") for ch in text]
    if not liga or not F.get("ligs"): return gl
    out, i, L = [], 0, sorted(F["ligs"], key=len, reverse=True)
    while i < len(gl):
        for seq in L:
            if tuple(gl[i:i+len(seq)]) == seq: out.append(F["ligs"][seq]); i += len(seq); break
        else: out.append(gl[i]); i += 1
    return out
def glyph_path(F, g, dx, dy=0, s=1.0):
    rp = RecordingPen(); F["gs"][g].draw(rp)
    v, c = [], []
    for op, pts in rp.value:
        P = [(dx + x*s, dy - y*s) for x, y in pts]
        if op == "moveTo": v += P; c += [Path.MOVETO]
        elif op == "lineTo": v += P; c += [Path.LINETO]
        elif op == "curveTo": v += P; c += [Path.CURVE4]*3
        elif op == "qCurveTo":
            # TrueType 2차 곡선: 연속 off-curve 사이 암시적 on-curve
            prev = None
            pts2 = P
            for j in range(len(pts2)-1):
                p1 = pts2[j]
                p2 = pts2[j+1] if j == len(pts2)-2 else ((pts2[j][0]+pts2[j+1][0])/2, (pts2[j][1]+pts2[j+1][1])/2)
                v += [p1, p2]; c += [Path.CURVE3]*2
        elif op in ("closePath", "endPath"): v.append((0,0)); c.append(Path.CLOSEPOLY)
    return Path(v, c) if v else None
def set_text(F, text, x=0, y=0, size=1.0, kerning=True, liga=True):
    paths, prev = [], None
    for g in shape(F, text, liga):
        if prev and kerning: x += F["kern"].get((prev, g), 0) * size
        p = glyph_path(F, g, x, y, size)
        if p is not None: paths.append(p)
        x += F["hm"][g][0] * size; prev = g
    return paths, x
