"""전용서체(FnGuide Logotype)로 브랜드별 로고타입 SVG를 만든다.

- 글자 간격(커닝)과 f 합자는 서체에 들어 있는 규칙을 그대로 적용한다.
- 회사 CI "FnGuide"는 서체로 다시 입력하지 않고 공식 원본 파일을 쓴다 (서체 문서 5장 사용 원칙).
- 리타민은 B2C 독립 체계라 전용서체 대신 기존 로고(피그마)를 그대로 쓴다.
결과: out/brand-site/logos/*.svg, out/brand-site/logos.js
실행: py scripts/build_logotypes.py   (필요: py -m pip install fonttools uharfbuzz)
"""
import json
import re
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "data" / "FnGuide-Logotype-Font"
FONT = FONT_DIR / "fonts" / "FnGuideLogotype-Regular.otf"
CI_SVG = FONT_DIR / "source-svg" / "0_logo" / "FnGuide.svg"
RETAMIN_SVG = ROOT / "data" / "figma-logo-parts" / "retamin.svg"
OUT = ROOT / "out" / "brand-site"

HEIGHT_PX = 40  # 대문자 높이 700 단위가 28px 정도로 보이는 크기 (1000 단위 = 40px)

# 그룹·색상: 서체 문서 4장 표. 회사 CI는 리뉴얼 후 색 FnRed (FnWine #94243A는 리뉴얼 이전 오리지널 CI 색)
GROUPS = [
    {"id": "ci", "name": "회사 CI", "color": "#B9023D", "colorName": "FnRed"},
    {"id": "b2b", "name": "B2B 대표상품군", "color": "#B9023D", "colorName": "FnRed"},
    {"id": "index", "name": "지수", "color": "#45B792", "colorName": "Index"},
    {"id": "fund", "name": "펀드", "color": "#0C3178", "colorName": "Fund"},
    {"id": "contract", "name": "B2B 계약상품군", "color": "#1C1C3A", "colorName": "Contract"},
    {"id": "b2c", "name": "B2C 독립 체계", "color": "#2457C5", "colorName": "API · 리타민"},
]
COLOR = {g["id"]: g["color"] for g in GROUPS}

# (파일명, 글자, 그룹, 색상 덮어쓰기) — 브랜드 목록은 피그마 「FnGuide Brand Color」 페이지 기준
BRANDS = [
    ("fnguide-com", "FnGuide.com", "b2b", None),
    ("dataguide", "DataGuide", "b2b", None),
    ("quantiwise", "QuantiWise", "b2b", None),
    ("wisereport", "WiseReport", "b2b", None),
    ("fnindex", "FnIndex", "index", None),
    ("wiseindex", "WiseIndex", "index", None),
    ("cryptoguide", "CryptoGuide", "index", None),
    ("fundguide", "FundGuide", "fund", None),
    ("pfguide", "PFGuide", "fund", None),
    ("fnaims", "FnAIMS", "fund", None),
    ("companyguide", "CompanyGuide", "contract", None),
    ("companywise", "CompanyWise", "contract", None),
    ("companyglobal", "CompanyGlobal", "contract", None),
    ("etfglobal", "ETF Global", "contract", None),
    ("marketmonitor", "Market Monitor", "contract", None),
    ("fnspace", "FnSpace", "contract", None),
    ("fnapi", "FnAPI", "b2c", "#2457C5"),
]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def svg_doc(path_d, x0, y0, w, h, color):
    """글꼴 단위(1000) 좌표의 도형을 픽셀 크기가 붙은 SVG 한 파일로 감싼다."""
    pw, ph = w * HEIGHT_PX / 1000, h * HEIGHT_PX / 1000
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(pw)}" height="{fmt(ph)}" '
        f'viewBox="{fmt(x0)} {fmt(y0)} {fmt(w)} {fmt(h)}"><path fill="{color}" d="{path_d}"/></svg>\n'
    )


def typeset(text, color, hb_font, glyph_set, upem):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": True})
    names = TTFONT.getGlyphOrder()
    svg_pen = SVGPathPen(glyph_set)
    bounds = BoundsPen(glyph_set)
    x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = names[info.codepoint]
        # y축을 뒤집어 SVG 좌표(아래로 증가)로 바꾼다
        t = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)
        glyph_set[name].draw(TransformPen(svg_pen, t))
        glyph_set[name].draw(TransformPen(bounds, t))
        x += pos.x_advance
    xmin, ymin, xmax, ymax = bounds.bounds
    return svg_doc(svg_pen.getCommands(), xmin, ymin, xmax - xmin, ymax - ymin, color)


def official_ci():
    """공식 FnGuide 로고 원본에서 그림 부분만 잘라 낸다 (모양·색은 그대로)."""
    src = CI_SVG.read_text(encoding="utf-8")
    color = re.search(r"fill:\s*(#[0-9a-fA-F]{6})", src).group(1)
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', src)
    bounds = BoundsPen(None)
    for d in ds:
        parse_path(d, bounds)
    xmin, ymin, xmax, ymax = bounds.bounds
    w, h = xmax - xmin, ymax - ymin
    scale = HEIGHT_PX * 0.7 / h  # 원본 높이를 서체 대문자 높이(700)에 맞춘다
    paths = "".join(f'<path fill="{color}" d="{d}"/>' for d in ds)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(w * scale)}" height="{fmt(h * scale)}" '
        f'viewBox="{fmt(xmin)} {fmt(ymin)} {fmt(w)} {fmt(h)}">{paths}</svg>\n'
    )


def existing_logo(path):
    """기존 로고 파일을 모양·색 그대로 쓴다 (피그마 내보내기 속성만 정리)."""
    src = path.read_text(encoding="utf-8")
    src = re.sub(r'\s(preserveAspectRatio|overflow|style|id)="[^"]*"', "", src)
    return src.strip() + "\n"


TTFONT = TTFont(FONT)


def main():
    blob = hb.Blob.from_file_path(str(FONT))
    hb_font = hb.Font(hb.Face(blob))
    glyph_set = TTFONT.getGlyphSet()
    upem = TTFONT["head"].unitsPerEm

    (OUT / "logos").mkdir(parents=True, exist_ok=True)
    items = []
    entries = [("fnguide", "FnGuide", "ci", official_ci())]
    for file, text, group, color in BRANDS:
        entries.append((file, text, group, typeset(text, color or COLOR[group], hb_font, glyph_set, upem)))
    entries.insert(-1, ("retamin", "Retamin", "b2c", existing_logo(RETAMIN_SVG)))
    for file, text, group, svg in entries:
        (OUT / "logos" / f"{file}.svg").write_text(svg, encoding="utf-8")
        w, h = (float(v) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
        items.append({"id": file, "name": text, "group": group, "w": w, "h": h, "svg": svg.strip()})
    (OUT / "logos.js").write_text(
        "window.BRAND = " + json.dumps({"groups": GROUPS, "logos": items}, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"logotypes: {len(items)}")


if __name__ == "__main__":
    main()
