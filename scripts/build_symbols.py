"""피그마에서 내보낸 서비스 심볼 아이콘(data/Symbol)을 사이트용으로 정리한다.

피그마 내보내기에는 캔버스·섹션·프레임 바탕이 함께 들어 있으므로
아이콘 그룹(KEEP 의 id)과 <defs>(그러데이션)만 남겨 out/brand-site/symbols.js 로 쓴다.
사이트는 내 컴퓨터 파일로 열기 때문에 SVG 를 따로 불러오지 않고 js 안에 글자로 담는다.

실행: py scripts/build_symbols.py
"""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "Symbol"
OUT = ROOT / "out" / "brand-site" / "symbols.js"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# 서비스 id: (원본 파일, 남길 그룹 id, 설명) — 피그마 "FnGuide Brand Symbol" 페이지
KEEP = {
    "retamin": ("retamin/retamin-icon-navy.svg", "img/retamin-app-icon", "Report 의 R — 네모·세모·원"),
    "dataguide": ("dataguide/figma/dataguide-icon-256.svg", "Icon-set", "D·G 와 ∞ — 무한한 데이터 흐름"),
    "cryptoguide": ("cryptoguide/cryptoguide-icon-512.svg", "CryptoGuide", "Crypto·Guide 이니셜의 큐브"),
}


def clean(path, keep_id):
    root = ET.parse(SRC / path).getroot()
    w, h = root.get("width"), root.get("height")
    group = next(e for e in root.iter() if e.get("id") == keep_id)
    defs = [e for e in root if e.tag == f"{{{NS}}}defs"]
    out = ET.Element(f"{{{NS}}}svg", {"width": w, "height": h, "viewBox": f"0 0 {w} {h}", "fill": "none"})
    out.append(group)
    out.extend(defs)
    for e in out.iter():  # 피그마 레이어 이름(id)은 필요 없음 — 그러데이션 id 만 남김
        if e.get("id") and not e.tag.endswith("linearGradient") and not e.tag.endswith("clipPath") and not e.tag.endswith("mask"):
            del e.attrib["id"]
    svg = ET.tostring(out, encoding="unicode")
    return re.sub(r">\s+<", "><", svg)


def main():
    data = {}
    for sid, (path, keep_id, desc) in KEEP.items():
        svg = clean(path, keep_id)
        # 서비스마다 그러데이션 id 가 같으므로(paint0_linear_4_5306) 한 화면에 함께 그려도 섞이지 않게 바꾼다
        svg = svg.replace("paint", f"{sid}-paint")
        data[sid] = {"svg": svg, "desc": desc, "size": int(re.search(r'width="(\d+)', svg).group(1))}
    OUT.write_text("window.SYMBOLS = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print("symbols:", ", ".join(data))


if __name__ == "__main__":
    main()
