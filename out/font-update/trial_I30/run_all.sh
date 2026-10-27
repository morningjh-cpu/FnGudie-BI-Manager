#!/bin/sh
# 여백 → 글자 쌍 간격(커닝) → 서체 파일. PYTHONUTF8=1 필요(윈도우 한글 출력)
set -e
export PYTHONUTF8=1
py make_spacing.py
py compute_kern.py > /dev/null
py tune_kern.py > /dev/null
cp raw_kern.json raw_kern_v1000.json
py caps_kern.py | head -1
py write_fea.py
mkdir -p out
py build_font.py
