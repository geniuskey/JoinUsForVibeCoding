#!/bin/bash
# 파일 정리 스크립트 - 확장자별로 폴더에 분류합니다

echo "=== 파일 정리 스크립트 ==="
echo ""

# 작업 디렉토리 생성
WORK_DIR="/tmp/organize_demo"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# 샘플 파일 생성
echo "1단계: 샘플 파일 생성 중..."
touch report.txt notes.txt memo.txt
touch photo1.jpg photo2.jpg screenshot.png
touch app.py utils.py test.py
touch style.css index.html script.js
echo "  → 12개 파일 생성 완료"
echo ""

# 현재 파일 목록 확인
echo "2단계: 현재 파일 목록"
ls -1
echo ""

# 확장자별 폴더 생성
echo "3단계: 확장자별 폴더 생성 중..."
mkdir -p documents images python web
echo "  → 4개 폴더 생성 완료"
echo ""

# 파일 분류
echo "4단계: 파일 분류 중..."
mv *.txt documents/
echo "  → .txt 파일 → documents/"
mv *.jpg *.png images/
echo "  → .jpg, .png 파일 → images/"
mv *.py python/
echo "  → .py 파일 → python/"
mv *.css *.html *.js web/
echo "  → .css, .html, .js 파일 → web/"
echo ""

# 결과 확인
echo "5단계: 정리 결과"
echo "---"
for dir in documents images python web; do
    count=$(ls "$dir" | wc -l)
    echo "📂 $dir/ ($count개 파일)"
    ls "$dir" | while read file; do
        echo "   - $file"
    done
done
echo "---"
echo ""
echo "=== 파일 정리 완료! ==="
