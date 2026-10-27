import sys, re, glob, os, xml.etree.ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
NS = "{http://www.w3.org/2000/svg}"
def styles(root):
    css = "".join(e.text or "" for e in root.iter(NS+"style"))
    out = {}
    for name, body in re.findall(r"\.(st\d+)\s*\{([^}]*)\}", css):
        out[name] = body
    return out
def to_d(e):
    t = e.tag[len(NS):]
    g = lambda k: float(e.get(k, 0))
    if t == "path": return e.get("d")
    if t == "rect":
        x,y,w,h = g("x"),g("y"),g("width"),g("height"); return f"M{x},{y}h{w}v{h}h{-w}Z"
    if t in ("polygon","polyline"):
        pts = e.get("points").split(); nums = re.findall(r"-?[\d.]+", e.get("points"))
        p = list(zip(nums[0::2], nums[1::2])); return "M" + "L".join(f"{a},{b}" for a,b in p) + "Z"
    if t == "circle":
        cx,cy,r = g("cx"),g("cy"),g("r"); return f"M{cx-r},{cy}a{r},{r} 0 1,0 {2*r},0a{r},{r} 0 1,0 {-2*r},0Z"
    if t == "ellipse":
        cx,cy,rx,ry = g("cx"),g("cy"),g("rx"),g("ry"); return f"M{cx-rx},{cy}a{rx},{ry} 0 1,0 {2*rx},0a{rx},{ry} 0 1,0 {-2*rx},0Z"
    return None
def visible_shapes(f):
    root = ET.parse(f).getroot(); st = styles(root)
    hidden = {k for k,v in st.items() if "display: none" in v or "display:none" in v}
    out = []
    def walk(e, hid, tr):
        cls = set((e.get("class") or "").split())
        h = hid or bool(cls & hidden) or e.get("display") == "none"
        tr = tr or bool(e.get("transform"))
        d = to_d(e)
        if d is not None:
            fill = ";".join(st.get(c,"") for c in cls)
            m = re.search(r"fill:\s*([^;]+)", fill)
            bp = BoundsPen(None); parse_path(d, bp)
            out.append(dict(tag=e.tag[len(NS):], hidden=h, fill=m.group(1).strip() if m else None, bounds=bp.bounds, d=d, tr=tr))
        for c in e: walk(c, h, tr)
    walk(root, False, False)
    return out
if __name__ == "__main__":
    for f in sorted(glob.glob("up/*.svg")):
        sh = visible_shapes(f)
        vis = [s for s in sh if not s["hidden"]]
        print(os.path.basename(f), "total", len(sh), "visible", len(vis))
        for s in vis:
            b = s["bounds"]; print("   ", s["tag"], s["fill"], "tr" if s["tr"] else "", tuple(round(v,2) for v in b) if b else None)
