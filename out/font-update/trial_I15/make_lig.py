"""f 합자 (v0.700 f 기준). 다음 글자 기둥과 이어지는 가로획, 또는 f 터미널이 i 점을 대신하는 형태"""
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
TPL = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 35 35">\n  <defs><style>.st0 {{ fill: #b9023d; }}</style></defs>\n{p}\n</svg>\n'
def write(name, ds): open(f"all/{name}.svg", "w").write(TPL.format(p="\n".join(f'  <path class="st0" d="{d}"/>' for d in ds)))
def mv(d, dx):
    pen = SVGPathPen(None); parse_path(d, TransformPen(pen, (1, 0, 0, 1, dx, 0))); return pen.getCommands()
F_FULL = ("M13,28.25H16.75V14.9H20.6V13H16.75V11.2C16.75,8.6 17.6,7.6 19.4,7.6C20.4,7.6 21,8.4 21.15,9.75H24.95"
          "C24.85,7.5 23,6.1 19.6,6.1C15.1,6.1 13,8.05 13,12V13H10.4V14.9H13Z")
def f_bar(SL, SR, bot=8.6):
    """f 몸통 + 윗 가로획(두께 1.5, f 곡선 위 두께와 같음)이 다음 기둥 SL~SR 위까지 이어짐. bot까지 기둥 윗부분을 채움"""
    return (f"M13,28.25H16.75V14.9H20.6V13H16.75V11.2C16.75,8.6 17.6,7.6 19.4,7.6H{SL:.2f}V{bot}H{SR:.2f}V6.75"
            f"C{SR:.2f},6.35 {SR-0.4:.2f},6.1 {SR-0.9:.2f},6.1H19.6C15.1,6.1 13,8.05 13,12V13H10.4V14.9H13Z")
SL = 22.4                                         # f 가로획 끝(20.6) + 1.8
JOIN = 7.0                                        # 다음 기둥은 가로획 안쪽에서 시작 (깃발 세리프 없음)
STEMS = {   # 기둥 왼쪽 x(원래 위치), 기둥 폭, 깃발을 뗀 경로
 "l": (0, 3.75, lambda s: f"M{s:.2f},{JOIN}H{s+3.75:.2f}V28.23H{s:.2f}Z"),
 "b": (11.68, 3.72, lambda s: mv("M19.86,12.58C18.33,12.58 16.73,13.38 15.4,14.91V7H11.68V28.24H13.9L15.36,26.62C16.08,27.62 17.35,28.6 19.71,28.6"
        "C25,28.6 26.01,24.11 26.01,20.35C26.01,15.41 23.83,12.58 19.86,12.58ZM21.99,20.35C21.99,24.4 20.83,26.45 18.75,26.45"
        "C16.04,26.45 15.37,23.81 15.37,21.6V20.29C15.37,18.62 15.78,14.74 18.71,14.74C21.64,14.74 21.99,17.95 21.99,20.35Z", s - 11.68)),
 "h": (12.03, 3.75, lambda s: mv("M21.43,12.64C20.35,12.64 17.73,13 15.78,16.24V7H12.03V28.25H15.78V20.83C15.78,17.85 17.66,15.23 19.81,15.23"
        "C21.83,15.23 22.14,16.73 22.14,18.54V28.25H25.87V17C25.87,13.07 22.77,12.64 21.43,12.64Z", s - 12.03)),
 "k": (11.48, 3.75, lambda s: mv("M25.15,12.99H21.8L15.23,19.1V7H11.48V28.25H15.23V20.58L21.42,28.25H26.5L18.59,19L25.14,12.99Z", s - 11.48)),
}
# 점 없는 i (깃발 유지) — 기둥이 f 터미널(21.15~24.95) 바로 아래 오도록
DOTLESS_I = "M13.04,14.82H13.23C15.54,14.88 15.8,15.97 15.8,16.78V28.25H19.55V12.64L13.04,13.77V14.82Z"
I_DX = (21.15 + 24.95) / 2 - (15.8 + 19.55) / 2   # 터미널 중심 = 기둥 중심
def lig_bar(second, shift):
    _, w, mk = STEMS[second]
    return [mv(f_bar(SL, SL + w), shift), mv(mk(SL), shift)]
I_L = 21.18                                        # i 기둥 왼쪽 (f 터미널 중심 아래)
def fi_body(dx=0.0, crossbar_from=20.6):
    return [mv(f"M{crossbar_from},13H{I_L+0.5:.2f}V14.9H{crossbar_from}Z", dx),          # 가로획 연장
            mv(f"M{I_L:.2f},12.67H{I_L+3.75:.2f}V28.25H{I_L:.2f}Z", dx)]                  # 점·깃발 없는 i 기둥
write("f_i", [F_FULL] + fi_body())
write("f_l", lig_bar("l", 0.0))
write("f_b", lig_bar("b", -3.5))
write("f_h", lig_bar("h", -3.5))
write("f_k", lig_bar("k", -4.0))
DX2 = SL - 13                                      # 두 번째 f 위치
def f_bar_ff(SL, SR):
    return (f"M13,28.25H16.75V14.9H20.6V13H16.75V11.2C16.75,8.6 17.6,7.6 19.4,7.6H{SL:.2f}V12.5H{SR:.2f}V7.6"
            f"H{SL+6.6:.2f}V6.1H19.6C15.1,6.1 13,8.05 13,12V13H10.4V14.9H13Z")
write("f_f", [mv(f_bar_ff(SL, SL + 3.75), -3.0), mv(F_FULL, DX2 - 3.0)])
write("f_f_i", [mv(f_bar_ff(SL, SL + 3.75), -8.0), mv(F_FULL, DX2 - 8.0)] + fi_body(DX2 - 8.0))
write("f_f_l", [mv(f_bar_ff(SL, SL + 3.75), -8.0), mv(f_bar(SL, SL + 3.75), DX2 - 8.0), mv(STEMS["l"][2](SL), DX2 - 8.0)])
print("ligatures written")
