import glob, os
from svgscan import visible_shapes
TPL = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 35 35">
  <defs><style>.st0 {{ fill: #b9023d; }}</style></defs>
{p}
</svg>
'''
def write(path, ds):
    open(path, "w").write(TPL.format(p="\n".join(f'  <path class="st0" d="{d}"/>' for d in ds)))
for f in sorted(glob.glob("up/*.svg")):
    name = os.path.basename(f)[:-4]
    if name == "z-lower": continue
    keep, seen = [], set()
    for s in visible_shapes(f):
        b = s["bounds"]
        if s["hidden"] or b is None or b[0] > 35 or b[2] < 0: continue
        if s["d"] in seen: continue
        seen.add(s["d"]); keep.append(s["d"])
    write(f"clean/{name}.svg", keep)
    print(f"{name:14s} {len(keep)} shape(s)")
