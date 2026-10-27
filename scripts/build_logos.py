"""[더 이상 쓰지 않음 — 서체 제작 전의 옛 로고. 지금은 build_logotypes.py 사용]
피그마에서 받은 로고 조각(data/figma-logo-parts)을 로고 하나당 SVG 한 파일로 합친다.

결과: out/brand-site/logos/*.svg, out/brand-site/logos.js (웹페이지가 읽는 목록)
실행: py scripts/build_logos.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "data" / "figma-logo-parts"
OUT = ROOT / "out" / "brand-site"

# 그룹: 피그마 「FnGuide Brand Color」 페이지 / 색상: 서체 문서 4장 표
GROUPS = [
    {"id": "ci", "name": "회사 CI", "color": "#94243A", "colorName": "FnWine"},
    {"id": "b2b", "name": "B2B 대표상품군", "color": "#B9023D", "colorName": "FnRed"},
    {"id": "index", "name": "지수", "color": "#45B792", "colorName": "Index"},
    {"id": "fund", "name": "펀드", "color": "#0C3178", "colorName": "Fund"},
    {"id": "contract", "name": "B2B 계약상품군", "color": "#1C1C3A", "colorName": "Contract"},
    {"id": "b2c", "name": "B2C 독립 체계", "color": "#2457C5", "colorName": "API · 리타민"},
]

# (파일명, 표시 이름, 그룹, 폭, 높이, [(조각, x, y), ...])  — 위치는 피그마 노드 값
LOGOS = [
    ("fnguide", "FnGuide", "ci", 421, 80, [("newlogo", 0, 0)]),
    ("fnguide-com", "FnGuide.com", "b2b", 183.745, 22.428,
     [("fn", 0, 0.466), ("guide", 37.961, 0), ("com", 119.985, 6.789)]),
    ("dataguide", "DataGuide", "b2b", 152.85, 23.529, [("dataguide", 0, 0)]),
    ("quantiwise", "QuantiWise", "b2b", 163, 26, [("quanti", 0, 0), ("wise1", 93.432, 0.174)]),
    ("wisereport", "WiseReport", "b2b", 165, 28, [("wise", 0, 0), ("report", 70.983, 0)]),
    ("fnindex", "FnIndex", "index", 115, 24.186, [("fn1", 0, 0.919), ("index", 36.375, 0)]),
    ("wiseindex", "WiseIndex", "index", 148.311, 24.174, [("wise2", 0, 0.679), ("index1", 69.721, 0)]),
    ("cryptoguide", "CryptoGuide", "index", 193.25, 30.28, [("crypto", 0, 0)]),
    ("fundguide", "FundGuide", "fund", 156, 22.227, [("group1", 0, 0), ("group", 76.35, 0.11)]),
    ("pfguide", "PFGuide", "fund", 119, 22.278, [("pf", 0, 0), ("guide1", 39.127, 0.111)]),
    ("fnaims", "FnAIMS", "fund", 110, 23.481, [("aims_fn", 0, 0.37), ("aims", 36.6, 0)]),
    ("companyguide", "CompanyGuide", "contract", 226, 30, [("group3", 0, 0), ("group2", 141.205, 0.309)]),
    ("companywise", "CompanyWise", "contract", 205.357, 29, [("companywise_full", 0, 0)]),
    ("companyglobal", "CompanyGlobal", "contract", 215, 29, [("company1", 0, 0), ("global", 135.063, 0.481)]),
    ("etfglobal", "ETF Global", "contract", 141, 22, [("etf", 0, 0), ("global1", 61.222, 0)]),
    ("marketmonitor", "Market Monitor", "contract", 215.44, 23, [("marketmonitor", 0, 0)]),
    ("fnspace", "FnSpace", "contract", 115.3, 30, [("fnspace_fn", 0, 0.37), ("space", 37.57, 0)]),
    ("retamin", "Retamin", "b2c", 134, 29, [("retamin", 0, 0)]),
    ("fnapi", "FnAPI", "b2c", 87, 23.053, [("fnapi_a", 0, 0.11), ("fnapi_b", 38.84, 0)]),
]


def part_inner(name):
    """조각 SVG의 viewBox와 안쪽 도형만 꺼낸다 (id는 겹치지 않게 지움)."""
    src = (PARTS / f"{name}.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    w = re.search(r'width="([^"]+)"', src).group(1)
    h = re.search(r'height="([^"]+)"', src).group(1)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
    inner = re.sub(r'\s(id|data-figma-[\w-]+)="[^"]*"', "", inner)
    return vb, w, h, inner.strip()


def compose(w, h, parts):
    body = []
    for name, x, y in parts:
        vb, pw, ph, inner = part_inner(name)
        body.append(
            f'<svg x="{x}" y="{y}" width="{pw}" height="{ph}" viewBox="{vb}" overflow="visible">{inner}</svg>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
        + "".join(body)
        + "</svg>\n"
    )


def main():
    (OUT / "logos").mkdir(parents=True, exist_ok=True)
    items = []
    for file, label, group, w, h, parts in LOGOS:
        svg = compose(w, h, parts)
        (OUT / "logos" / f"{file}.svg").write_text(svg, encoding="utf-8")
        items.append({"id": file, "name": label, "group": group, "w": w, "h": h, "svg": svg.strip()})
    data = {"groups": GROUPS, "logos": items}
    (OUT / "logos.js").write_text(
        "window.BRAND = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8"
    )
    print(f"로고 {len(items)}개 생성 → {OUT / 'logos'}")


if __name__ == "__main__":
    main()
