"""사이트 '폰트 업데이트' 화면용 그림 — 원화(₩) 내용을 뺀 판 (사용자 요청, 2026-10-29).
39-site: 수정 전/후 종합, 29-site: 기본/고정폭 숫자, 30-site: 금융 기호(− ± × ·)"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, lib
import after, symbols
from fontTools.pens.boundsPen import BoundsPen
OUT = lib.ROOT + "out/font-critique/img/"
RED = "#B9023D"
lab = after.lab

# 39-site: 수정 전 / 수정 후
lines = ["CompanyGlobal  ETF Global  DataGuide", "Clock Graph  every wavy oxygen",
         "soft lift fjord Portfolio  Il1 2011", "1,203,000  −0.71%  ±1.05  3×4  A·B"]
size = 0.6
fig, ax = plt.subplots(figsize=(15, len(lines) * 2 * size * 1.25 + 0.8), dpi=130)
y = 0; wmax = 0
for a, nm in [(False, "수정 전"), (True, "수정 후")]:
    lab(ax, -0.2, y + size * 0.25, nm, ha="right", color=RED if a else "#444", fs=13)
    for t in lines:
        wmax = max(wmax, after.draw(ax, t, 0, y, size, a)); y -= size * 1.3
    y -= size * 0.5
ax.set_xlim(-1.6, wmax + 0.2); ax.set_ylim(y + size * 0.9, size * 1.0); ax.set_aspect("equal"); ax.axis("off")
lib.save(OUT + "39-site-before-after.png")

# 29-site: 기본(비례) / 고정폭
rows = ["1,111,111", "9,876,543", "10,450.00", "+12.34%", "−0.71%", "±1.05%"]
fig, ax = plt.subplots(figsize=(13, 6.6), dpi=130)
for col, (name, tab) in enumerate([("기본: 비례 숫자", False), ("고정폭 숫자 기능을 켠 표", True)]):
    x1 = col * 6 + 5.2
    lab(ax, x1, 0.8, name, ha="right", fs=12, color=RED if tab else "#444")
    for i, t in enumerate(rows):
        symbols.draw(ax, t, x1 - symbols.width(t, 0.6, tab), -i * 0.7, 0.6, tab)
    ax.plot([x1, x1], [-len(rows) * 0.7 + 0.45, 0.6], color="#ddd", lw=0.8)
ax.set_xlim(0, 11.6); ax.set_ylim(-len(rows) * 0.7 + 0.3, 1.25); ax.set_aspect("equal"); ax.axis("off")
lib.save(OUT + "29-site-figures.png")

# 30-site: 금융 기호
fig, ax = plt.subplots(figsize=(15, 4.6), dpi=130)
x = 0
for ch, nm in [("+", "더하기(기준)"), ("−", "빼기"), ("±", "플러스마이너스"), ("×", "곱하기"), ("·", "가운뎃점")]:
    lab(ax, x + 0.02, 0.85, nm, color="#888", fs=10)
    symbols.draw(ax, "H" + ch + "H", x, 0, 0.9); x += symbols.width("H" + ch + "H", 0.9) + 0.35
lab(ax, -0.15, -0.95, "문장 속", ha="right", color="#444", fs=13)
symbols.draw(ax, "−0.71%  ±1.05  3×4  FnGuide·DataGuide", 0, -1.1, 0.62)
ax.set_xlim(-1.6, 13.5); ax.set_ylim(-1.3, 1.05); ax.set_aspect("equal"); ax.axis("off")
lib.save(OUT + "30-site-symbols.png")
print("ok")
