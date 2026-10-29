"""⑥ 안 B 수정 시안: 소문자 l 아래 꼬리 — 끝이 얇아지게.
지금 서체의 t 아래 꼬리(끝으로 갈수록 얇아지는 곡선)를 그대로 가져와 l 기둥에 맞춰 붙인다. 서체 파일은 고치지 않는다."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
import one_base
from one_base import draw, lab, fn, cm, hm, RED, OUT
import drafts_lb

ell, one = cm[ord("l")], cm[ord("1")]
# t 꼬리: 기둥 87~204, 바닥 -11, 끝 x 335 에서 높이 55(-2~53) 로 얇아짐. l 기둥은 82~202 라 왼쪽 -5, 안쪽 -2 만큼 옮긴다
a, b = -5, -2
L_T = [("M", [(-6, 627)]), ("L", [(0, 627)]), ("C", [(74, 625), (82, 590), (82, 564)]),
       ("L", [(87 + a, 127)]),
       ("C", [(87 + a, -1), (159 + a, -11), (257 + a, -11)]),          # 바깥 곡선(바닥)
       ("C", [(283 + a, -11), (310 + a, -6), (332 + a, -3)]),
       ("L", [(335 + a, -2)]), ("L", [(335 + a, 53)]), ("L", [(330 + a, 52)]),   # 얇은 끝
       ("C", [(319 + b, 49), (305 + b, 48), (291 + b, 48)]),            # 안쪽 곡선
       ("C", [(210 + b, 48), (204 + b, 76), (204 + b, 144)]),
       ("L", [(202, 697)]), ("L", [(-6, 661)]), ("Z", [])]
# 꼬리 길이: 처음 안 B(끝 284)와 직전 안(끝 307) 사이에서 글자 전체 균형으로 정한다(사용자 요청).
#   위 깃발은 기둥 왼쪽 밖으로 88(82 → -6) 나간다. 아래 꼬리도 기둥 오른쪽 밖으로 같은 만큼 나가면 위아래가 대각선으로 맞는다.
#   다만 꼬리는 끝이 얇아 실제보다 짧아 보이므로 6 을 더 준다(눈 보정) → 202 + 88 + 6 = 296
# 바깥 곡선은 기둥 왼쪽(82), 안쪽 곡선은 기둥 오른쪽(202)을 기준으로 가로만 줄여 기둥은 그대로 둔다.
TAIL_END = 296
def shrink(ops, end=TAIL_END):
    k_out = (end - 82) / (330 - 82)
    k_in = (end - 5 - 202) / (325 - 202)        # 안쪽 끝(325)은 바깥 끝보다 5 안쪽
    out = []
    for i, (op, pts) in enumerate(ops):
        inner = 9 <= i <= 10                    # 안쪽 곡선 두 개
        piv, k = (202, k_in) if inner else (82, k_out)
        out.append((op, [((piv + (x - piv) * k) if (y < 140 and x > 82) else x, y) for x, y in pts]))
    return out
L_NEW = shrink(L_T)
L_ADV = TAIL_END + 32         # 끝 뒤 여백 32 (t 는 23, 꼬리 다음 글자와 닿지 않게 조금 더)
if __name__ == "__main__": print("새 l 폭", L_ADV)

def _figures():
    # 그림 31: 크게 — 지금 l / 처음 안 B / 수정 안 B / 참고 t
    fig, ax = plt.subplots(figsize=(17, 4.4), dpi=130)
    x = 0
    for name, over, adv, c in [("지금", {}, {}, "#444"), ("처음 안 B", {ell: drafts_lb.L_B}, {ell: 300}, "#888"),
                               ("직전 안 B (끝 307)", {ell: shrink(L_T, 307)}, {ell: 307 + 32}, "#888"),
                               ("수정 안 B (끝 296)", {ell: L_NEW}, {ell: L_ADV}, RED)]:
        lab(ax, x + 0.02, 0.86, name, color=c, fs=14)
        x += draw(ax, "l", x + 0.05, 0, 1.0, over=over, adv=adv) + 0.45
    # 수정 안 B 에 깃발·꼬리 길이 표시 (방금 그린 글자 기준)
    gx = x - 0.45 - L_ADV / 1000 + 0.05
    for xx in (-6, 82, 202, 296):
        ax.plot([gx + xx / 1000] * 2, [-0.05, 0.75], color=RED, lw=0.8, ls=":")
    lab(ax, gx - 0.01, 0.76, "88", color=RED, fs=10); lab(ax, gx + 0.215, -0.075, "94", color=RED, fs=10)
    lab(ax, x + 0.02, 0.86, "참고: t 아래 꼬리", color="#444", fs=14)
    w = draw(ax, "t", x + 0.05, 0, 1.0)
    ax.add_patch(plt.Rectangle((x + 0.1, -0.03), 0.3, 0.17, fc="none", ec=RED, lw=1.5, ls="--"))
    ax.set_xlim(-0.1, x + w + 0.3); ax.set_ylim(-0.08, 0.95); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "31-draft-l-tail.png")

    # 그림 32: 문장 속 — 지금 / 수정 안 B / 수정 안 A + B (1 받침 + l 꼬리)
    T1, T2 = "Il1  Illinois 2011  1,111,111", "little  tall  CompanyGlobal  ETF Global"
    rows = [("지금", {}, {}), ("수정 안 B", {ell: L_NEW}, {ell: L_ADV}),
            ("수정 안 A + B", {ell: L_NEW, one: one_base.NEW}, {ell: L_ADV, one: one_base.NEW_ADV})]
    fig, ax = plt.subplots(figsize=(15, 8.6), dpi=130)
    y = 0
    for name, over, adv in rows:
        lab(ax, -0.15, y + 0.2, name, ha="right", color="#444" if name == "지금" else RED, fs=13)
        draw(ax, T1, 0, y, 0.68, over=over, adv=adv)
        draw(ax, T2, 0, y - 0.8, 0.68, over=over, adv=adv)
        y -= 1.85
    ax.set_xlim(-2.6, 14.5); ax.set_ylim(y + 0.75, 0.75); ax.set_aspect("equal"); ax.axis("off")
    lib.save(OUT + "32-draft-l-tail-text.png")

if __name__ == "__main__":
    _figures()
