import sys; sys.path.insert(0, ".")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.backends.backend_pdf import PdfPages
from layout import load, set_text
NEW = load("out/FnGuideLogotype-Regular.otf"); OLD = load("/home/claude/k1/out/FnGuideLogotype-Regular.otf")
RED, GREY, LIGHT = "#b9023d", "#777", "#9aa0a6"
W = 26000           # 페이지 폭 (폰트 단위)
def draw(ax, F, text, x, y, size, kern, color):
    paths, w = set_text(F, text, x=x, y=y, size=size, kerning=kern)
    for p in paths: ax.add_patch(PathPatch(p, fc=color, ec="none"))
    return w
def page(pdf, title, rows, size=1.0, a=("kerning off", OLD, False, LIGHT), b=("kerning on", NEW, True, RED)):
    fig, ax = plt.subplots(figsize=(11.69, 8.27)); fig.subplots_adjust(0.04, 0.03, 0.98, 0.97); ax.axis("off")
    LH = 1150 * size; y = 0
    ax.text(0, -500, title, fontsize=15, fontweight="bold")
    y += 900
    for cap, txt in rows:
        ax.text(0, y, cap, fontsize=8, color=GREY); y += LH
        for lab, F, kern, col in (a, b):
            draw(ax, F, txt, 2600, y, size, kern, col)
            ax.text(0, y - 250*size, lab, fontsize=7, color=col); y += LH
        y += 350
    ax.set_xlim(-100, W); ax.set_ylim(max(y, 18000), -1100); ax.set_aspect("equal")
    pdf.savefig(fig); plt.close(fig)
with PdfPages("/mnt/user-data/outputs/kerning-proof-v0.600.pdf") as pdf:
    page(pdf, "FnGuide Logotype v0.600 — kerning proof  (882 rules · 1000 UPM · no collisions)",
         [("sample", "Taiwan, Vietnam & Yonsei \u2013 \u201cAVA\u201d LT"), ("", "Today\u2019s Top Value: Wave, Yield, Pay."),
          ("logo words — must match the logo", "FnGuide DataGuide WiseReport")],
         size=1.15, a=("v0.500", OLD, True, LIGHT), b=("v0.600", NEW, True, RED))
    page(pdf, "Uppercase pairs", [("diagonals", "HAVAH HAWAH HAYAH HATAH"), ("", "HLTLH HLVLH HLYLH HPAPH HFAFH"),
         ("", "HVOVH HYOYH HTOTH HKOKH HXOXH"), ("round", "HOOH HCOCH HDODH HQOQH"), ("words", "KOSPI KOSDAQ ANALYST WAVY")])
    page(pdf, "Uppercase \u2192 lowercase", [("T", "nTanTenTonTrnTunTyn"), ("V W", "nVanVenVonWanWenWon"), ("Y", "nYanYenYon"),
         ("F P", "nFanFenFonPanPenPon"), ("words", "Taiwan Today Vietnam Yonsei")])
    page(pdf, "Lowercase pairs", [("diagonals", "nvonvenwonwenyonyenxon"), ("round", "noonnoennecnnoen"),
         ("collision fixes", "fl fb fh  gj qj jj  fi ff"), ("words", "lowly avoid every eye yawn waxy")])
    page(pdf, "Punctuation & digits", [("period / comma", "T. V. W. Y. F. P. r. v. y."), ("", "T, V, W, Y, F, P, r, v, y,"),
         ("quotes", "\u201cA\u201d \u2018A\u2019 L\u2019 \u201cT\u201d \u2018V\u2019 \u201cW\u201d \u2018Y\u2019"), ("dashes", "T\u2013V A\u2013Y -T- -V-"),
         ("digits — no kerning by design", "0.4 1.7 2026.10.26 $1,250.00 +3.5%")])
print("ok")
