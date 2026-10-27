"""f 합자 v2 — 새 f(source-svg/7_update)에 맞춰 make_lig.py 의 구성 방식을 그대로 다시 계산.
기존 구성: 다음 글자 기둥과 이어지는 가로획(윗 곡선 두께와 같음), 또는 f 터미널이 i 점을 대신함, 다음 글자의 깃발 세리프 제거.
기존 f 수치(왼쪽) → 새 f 수치(오른쪽): 기둥 13–16.75 → 13.18–17.18 / 가로획 13–14.9, 끝 20.6 → 12.91–14.64, 끝 21.9
윗 곡선 바깥 6.1·안쪽 7.6 → 5.39·6.92 / 터미널 21.15–24.95 → 21.2–25.67"""
import re, xml.etree.ElementTree as ET
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
TPL = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 35 35">\n  <defs><style>.st0 {{ fill: #b9023d; }}</style></defs>\n{p}\n</svg>\n'
def mv(d, dx):
    pen = SVGPathPen(None); parse_path(d, TransformPen(pen, (1, 0, 0, 1, dx, 0))); return pen.getCommands()
def xmax(ds):
    bp = BoundsPen(None)
    for d in ds: parse_path(d, bp)
    return bp.bounds[2]
LIMIT = 34.6                                       # 캔버스(35) 안에 들어오도록 왼쪽으로 밀어주는 한계
def write(name, ds, shift=0.0):
    ds = [mv(d, shift) for d in ds]
    over = xmax(ds) - LIMIT
    if over > 0: ds = [mv(d, -over) for d in ds]
    open(f"all/{name}.svg", "w").write(TPL.format(p="\n".join(f'  <path class="st0" d="{d}"/>' for d in ds)))
F_D = re.search(r' d="([^"]+)"', open("all/f-lower.svg").read()).group(1)    # 새 f
STEM_L, STEM_R, BASE = 13.18, 17.18, 28.24
XBAR_T, XBAR_B, XBAR_END = 12.91, 14.64, 21.9
TOP_O, TOP_I, PEAK_X = 5.39, 6.92, 19.16           # 윗 곡선 바깥/안쪽 높이, 안쪽 곡선 꼭대기 x
TERM_L, TERM_R = 21.2, 25.67
STEM_W = STEM_R - STEM_L
def f_head(): return f"M{STEM_L},{BASE}H{STEM_R}V{XBAR_B}H{XBAR_END}V{XBAR_T}H{STEM_R}V10.26L17.19,10.25C17.19,8.52 17.43,{TOP_I} {PEAK_X},{TOP_I}"
def f_tail(): return f"H18.91C15.32,5.39 13.18,7.48 13.18,10.99V{XBAR_T}H10.31V{XBAR_B}H13.18Z"
def f_bar(SL, SR, bot=TOP_I + 1.0):
    """f 몸통 + 윗 가로획이 다음 기둥 SL~SR 위까지 이어짐. bot까지 기둥 윗부분을 채움"""
    return (f_head() + f"H{SL:.2f}V{bot:.2f}H{SR:.2f}V{TOP_O + 0.65:.2f}"
            f"C{SR:.2f},{TOP_O + 0.25:.2f} {SR - 0.4:.2f},{TOP_O:.2f} {SR - 0.9:.2f},{TOP_O:.2f}" + f_tail())
SL = XBAR_END + 1.8                                # 가로획 끝 + 1.8
JOIN = TOP_O + 0.9                                 # 다음 기둥은 가로획 안쪽에서 시작 (깃발 세리프 없음)
STEMS = {
 "l": (3.75, lambda s: f"M{s:.2f},{JOIN:.2f}H{s+3.75:.2f}V28.23H{s:.2f}Z"),
 "b": (3.72, lambda s: mv("M19.86,12.58C18.33,12.58 16.73,13.38 15.4,14.91V7H11.68V28.24H13.9L15.36,26.62C16.08,27.62 17.35,28.6 19.71,28.6"
        "C25,28.6 26.01,24.11 26.01,20.35C26.01,15.41 23.83,12.58 19.86,12.58ZM21.99,20.35C21.99,24.4 20.83,26.45 18.75,26.45"
        "C16.04,26.45 15.37,23.81 15.37,21.6V20.29C15.37,18.62 15.78,14.74 18.71,14.74C21.64,14.74 21.99,17.95 21.99,20.35Z", s - 11.68)),
 "h": (3.75, lambda s: mv("M21.43,12.64C20.35,12.64 17.73,13 15.78,16.24V7H12.03V28.25H15.78V20.83C15.78,17.85 17.66,15.23 19.81,15.23"
        "C21.83,15.23 22.14,16.73 22.14,18.54V28.25H25.87V17C25.87,13.07 22.77,12.64 21.43,12.64Z", s - 12.03)),
 "k": (3.75, lambda s: mv("M25.15,12.99H21.8L15.23,19.1V7H11.48V28.25H15.23V20.58L21.42,28.25H26.5L18.59,19L25.14,12.99Z", s - 11.48)),
}
def lig_bar(second):
    w, mk = STEMS[second]
    return [f_bar(SL, SL + w), mk(SL)]
TERM_C = (TERM_L + TERM_R) / 2                     # 터미널 중심 = i 기둥 중심
I_L = TERM_C - 3.75 / 2
def fi_body(crossbar_from=XBAR_END):
    return [f"M{crossbar_from},{XBAR_T}H{I_L+0.5:.2f}V{XBAR_B}H{crossbar_from}Z",
            f"M{I_L:.2f},12.67H{I_L+3.75:.2f}V{BASE}H{I_L:.2f}Z"]                     # 점·깃발 없는 i 기둥
write("f_i", [F_D] + fi_body())
write("f_l", lig_bar("l"))
write("f_b", lig_bar("b"), -3.5)
write("f_h", lig_bar("h"), -3.5)
write("f_k", lig_bar("k"), -4.0)
DX2 = SL - STEM_L                                  # 두 번째 f 위치 (기둥이 SL 에서 시작)
FF_EXT = (PEAK_X + DX2 + 0.2) - SL                 # 첫 f 윗 가로획이 두 번째 f 곡선 꼭대기까지
def f_bar_ff(SL, SR):
    return (f_head() + f"H{SL:.2f}V{XBAR_T - 0.5:.2f}H{SR:.2f}V{TOP_I}"
            f"H{SL+FF_EXT:.2f}V{TOP_O}" + f_tail())
write("f_f", [f_bar_ff(SL, SL + STEM_W), mv(F_D, DX2)], -3.0)
write("f_f_i", [f_bar_ff(SL, SL + STEM_W)] + [mv(F_D, DX2)] + [mv(d, DX2) for d in fi_body()], -8.0)
write("f_f_l", [f_bar_ff(SL, SL + STEM_W), mv(f_bar(SL, SL + 3.75), DX2), mv(STEMS["l"][1](SL), DX2)], -8.0)
print("ligatures written")
