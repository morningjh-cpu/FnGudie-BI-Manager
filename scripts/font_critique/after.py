"""수정 전 / 수정 후 비교 그림 (개선안 보고서 다시 쓰기용).
수정 후 = 크리틱 "수정 필요" ①~④ + ⑥ 숫자 1 받침·l 꼬리(마지막 수정본) + ⑨ 금융 기호 1순위.
⑤(파일 설정)는 그림이 아니라 보고서의 수치 표로 보여 준다. 서체 파일은 고치지 않는다."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
import uharfbuzz as hb
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import one_base, tail_l, symbols
from symbols import poly, rect
OUT = lib.ROOT + "out/font-critique/img/"
fn = lib.load("FnGuide v1.200")
cm = fn.tt.getBestCmap(); hm = fn.tt["hmtx"]
RED, GRAY = "#B9023D", "#9AA0A6"
G = lambda ch: cm[ord(ch)]

# ---- 높이 고치기: 윗부분만 부드럽게 올림(맨 위 근처는 통째로 올라가 획 굵기가 그대로 유지됨) ----
def ss(t):
    t = min(1, max(0, t)); return t * t * (3 - 2 * t)
def lift(ops, base, top, d):
    """base 아래는 그대로, top 은 d 만큼, 그 사이는 부드럽게"""
    return [(op, [(x, y + d * ss((y - base) / (top - base))) for x, y in pts]) for op, pts in ops]

OV = {}
# ① C·G 윗부분 688 → O 와 같은 711
for ch in "CG": OV[G(ch)] = lift(fn.rec(G(ch)), 350, 688, 23)
# ② v·w·x 485(x 484)·y 491 → 소문자 높이 500
for ch, top in [("v", 485), ("w", 485), ("x", 484), ("y", 491)]: OV[G(ch)] = lift(fn.rec(G(ch)), 0, top, 500 - top)
# ③ o·c·e 위쪽 498 → 512 (아래쪽 넘침 −12 와 같은 만큼 위로 넘침)
for ch in "oce": OV[G(ch)] = lift(fn.rec(G(ch)), 250, 498, 14)
# ⑥ 숫자 1 받침, l 꼬리 (마지막 수정본)
OV[G("1")], ADV1 = one_base.NEW, one_base.NEW_ADV
OV[G("l")], ADVL = tail_l.L_NEW, tail_l.L_ADV
ADV = {G("1"): ADV1, G("l"): ADVL}

# ---- ④ 이어 쓰기 글자: 기존 f_i 방식(f 가로획이 다음 글자 기둥까지 이어짐) ----
f_ops = fn.rec(G("f"))
# ft: t 를 395 만큼 옮겨 t 의 깃발이 f 머리 끝(493)과 25 띄어지게 하고, t 가로획 높이를 f 가로획(435~491)에 맞춰 잇는다
T_OX = 395
t_ops = [(op, [(x + T_OX, {427: 435, 488: 491}.get(y, y)) for x, y in pts]) for op, pts in fn.rec(G("t"))]
F_T = f_ops + rect(360, 435, T_OX + 10, 491) + t_ops
F_T_ADV = T_OX + hm[G("t")][0]
# fj: j 의 점과 왼쪽 깃발을 빼고(f_i 의 i 처럼) 기둥을 f 가로획 끝(361~481)에 맞춘다
J_OX = 130
j_ops = [("M", [(231, 498)]), ("L", [(231, -69)]), ("C", [(231, -117), (215, -140), (176, -140)]),
         ("C", [(141, -140), (125, -120), (125, -72)]), ("L", [(125, -66)]), ("L", [(-6, -66)]),
         ("C", [(-3, -133), (42, -207), (167, -207)]), ("C", [(298, -207), (351, -140), (351, -18)]),
         ("L", [(351, 498)]), ("Z", [])]
F_J = f_ops + [(op, [(x + J_OX, y) for x, y in pts]) for op, pts in j_ops]
F_J_ADV = J_OX + hm[G("j")][0]
LIG = {(G("f"), G("t")): (F_T, F_T_ADV), (G("f"), G("j")): (F_J, F_J_ADV)}
NOKERN = {(G("t"), G("y")), (G("r"), G("v"))}     # ④ 간격을 벌리던 + 보정을 0 으로

def layout(text, after):
    """→ [(윤곽, x)], 전체 폭 (서체 단위)"""
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(fn.hbf, buf, {"kern": True, "liga": True})
    it = [(fn.order[i.codepoint], text[i.cluster], p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
    out, x, k = [], 0, 0
    while k < len(it):
        g, ch, adv = it[k]
        if not after:
            out.append((fn.rec(g), x)); x += adv; k += 1; continue
        if k + 1 < len(it) and (g, it[k + 1][0]) in LIG:
            ops, a = LIG[(g, it[k + 1][0])]; out.append((ops, x)); x += a; k += 2; continue
        if ch in symbols.NEW:
            ops, a = symbols.NEW[ch]; out.append((ops, x)); x += a; k += 1; continue
        a = adv + ADV.get(g, hm[g][0]) - hm[g][0]
        if k + 1 < len(it) and (g, it[k + 1][0]) in NOKERN: a = ADV.get(g, hm[g][0])
        out.append((OV.get(g) or fn.rec(g), x)); x += a; k += 1
    return out, x

def draw(ax, text, x0, y0, size, after, color="#111"):
    s = size / fn.upm; V, C = [], []
    items, w = layout(text, after)
    for ops, gx in items:
        for op, pts in ops:
            V.extend([(x0 + (gx + px) * s, y0 + py * s) for px, py in pts] or [(0, 0)])
            C.extend({"M": [Path.MOVETO], "L": [Path.LINETO], "C": [Path.CURVE4] * 3,
                      "Q": [Path.CURVE3] * 2, "Z": [Path.CLOSEPOLY]}[op])
    ax.add_patch(PathPatch(Path(V, C), fc=color, ec="none"))
    return w * s

def lab(ax, x, y, t, **k):
    ax.text(x, y, t, family="Malgun Gothic", fontsize=k.pop("fs", 12), **k)

def pair_fig(name, text, size, lines=(), width=None, extra=None, mark=False):
    """수정 전 / 수정 후 두 줄. lines = [(높이, 이름)] 기준선"""
    w = max(draw(plt.subplots()[1], text, 0, 0, size, a) for a in (False, True)); plt.close("all")
    fig, ax = plt.subplots(figsize=(width or 14, 2 * size * 1.55 + 0.6), dpi=130)
    for r, (after, nm) in enumerate([(False, "수정 전"), (True, "수정 후")]):
        y0 = -r * size * 1.35
        lab(ax, -0.2, y0 + size * 0.25, nm, ha="right", color=RED if after else "#444", fs=13)
        prev = None
        for h, ln in sorted(lines):
            ax.plot([-0.05, w + 0.05], [y0 + h / 1000 * size] * 2, color=RED if after else GRAY, lw=0.7, ls=":")
            dx = 0.75 if prev is not None and h - prev < 40 else 0      # 가까운 선은 이름을 옆으로 비켜 씀
            lab(ax, w + 0.1 + dx, y0 + h / 1000 * size - 0.03, ln, color=RED if after else GRAY, fs=9)
            prev = h
        if after and mark:      # 수정 후를 빨갛게 깔고 수정 전을 검게 덮어, 늘어난 곳만 빨갛게 보이게
            draw(ax, text, 0, y0, size, True, color=RED); draw(ax, text, 0, y0, size, False)
        else:
            draw(ax, text, 0, y0, size, after)
    if extra: extra(ax)
    ax.set_xlim(-1.6, w + 1.9); ax.set_ylim(-size * 1.35 - 0.35, size * 1.05); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + name)

if __name__ == "__main__":
    pair_fig("33-fix-1-CG.png", "OCG HCG", 1.3, [(0, "0"), (700, "H 700"), (711, "O 711")], mark=True)
    pair_fig("34-fix-2-vwxy.png", "nvwxyz", 1.3, [(0, "0"), (500, "n 500")], mark=True)
    pair_fig("35-fix-3-oce.png", "nocen", 1.3, [(-12, "-12"), (0, "0"), (500, "n 500"), (512, "512")], mark=True)
    pair_fig("36-fix-4-ft-fj.png", "soft lift fjord Portfolio  pretty curvy", 0.62, [], width=16)
    pair_fig("37-fix-6-zoom.png", "Il1", 1.5, [], width=8)

    # 그림 38: ⑥ 문장 속, 그림 39: 종합 (여러 줄)
    def multi(name, lines_, size, width):
        fig, ax = plt.subplots(figsize=(width, len(lines_) * 2 * size * 1.25 + 0.8), dpi=130)
        y = 0; wmax = 0
        for after, nm in [(False, "수정 전"), (True, "수정 후")]:
            lab(ax, -0.2, y + size * 0.25, nm, ha="right", color=RED if after else "#444", fs=13)
            for t in lines_:
                wmax = max(wmax, draw(ax, t, 0, y, size, after)); y -= size * 1.3
            y -= size * 0.5
        ax.set_xlim(-1.6, wmax + 0.2); ax.set_ylim(y + size * 0.9, size * 1.0); ax.set_aspect("equal"); ax.axis("off")
        lib.save(OUT + name)
    multi("38-fix-6-text.png", ["Il1  Illinois 2011  1,111,111", "CompanyGlobal  ETF Global  little"], 0.62, 15)
    multi("39-before-after.png", ["CompanyGlobal  ETF Global  DataGuide",
                                  "Clock Graph  every wavy oxygen",
                                  "soft lift fjord Portfolio  Il1 2011",
                                  "₩1,203,000  −0.71%  ±1.05  3×4  A·B"], 0.6, 15)
    print("ok")
