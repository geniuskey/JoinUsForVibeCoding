"""
예제 15-07: 확장자별 파일 분류
디렉토리 내 파일들을 확장자별로 그룹화하고 통계를 출력합니다.
"""
import os
import tempfile
import shutil
from pathlib import Path
from collections import defaultdict

# --- 샘플 파일 생성 ---
temp_dir = tempfile.mkdtemp()
project_dir = os.path.join(temp_dir, "mixed_files")
os.makedirs(project_dir)

sample_files = [
    ("report.py", 1200),
    ("main.py", 3400),
    ("utils.py", 980),
    ("test_main.py", 2100),
    ("index.html", 5600),
    ("about.html", 3200),
    ("style.css", 1500),
    ("theme.css", 890),
    ("app.js", 2700),
    ("helpers.js", 1100),
    ("data.json", 450),
    ("config.json", 320),
    ("README.md", 2800),
    ("CHANGELOG.md", 1900),
    ("notes.txt", 600),
    ("todo.txt", 250),
    ("logo.png", 15000),
    ("banner.png", 28000),
    ("icon.svg", 4500),
    ("photo.jpg", 52000),
]

for fname, size in sample_files:
    fpath = os.path.join(project_dir, fname)
    with open(fpath, "w") as f:
        f.write("x" * size)  # 지정된 크기만큼 작성

# --- 확장자별 파일 분류 ---
print("=" * 50)
print("확장자별 파일 분류 결과")
print("=" * 50)

ext_groups = defaultdict(list)
project_path = Path(project_dir)

for file_path in project_path.iterdir():
    if file_path.is_file():
        ext = file_path.suffix.lower() if file_path.suffix else "(확장자 없음)"
        size = file_path.stat().st_size
        ext_groups[ext].append((file_path.name, size))

# 파일 수 기준 내림차순 정렬
sorted_groups = sorted(ext_groups.items(), key=lambda x: len(x[1]), reverse=True)

total_files = 0
total_size = 0

for ext, files in sorted_groups:
    group_size = sum(size for _, size in files)
    total_files += len(files)
    total_size += group_size

    print(f"\n  {ext} 파일 ({len(files)}개, {group_size:,} bytes)")
    print(f"  {'-' * 40}")
    for fname, fsize in sorted(files):
        print(f"    {fname:<20s}  {fsize:>8,} bytes")

# --- 통계 요약 ---
print()
print("=" * 50)
print("통계 요약")
print("=" * 50)
print(f"  총 파일 수: {total_files}개")
print(f"  총 크기: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
print(f"  확장자 종류: {len(ext_groups)}가지")
print()

# 카테고리별 분류
categories = {
    "코드": [".py", ".js"],
    "웹": [".html", ".css"],
    "데이터": [".json", ".csv", ".txt"],
    "문서": [".md"],
    "이미지": [".png", ".jpg", ".svg"],
}

print("카테고리별 분류:")
for category, extensions in categories.items():
    cat_files = []
    for ext in extensions:
        if ext in ext_groups:
            cat_files.extend(ext_groups[ext])
    if cat_files:
        cat_size = sum(s for _, s in cat_files)
        pct = (len(cat_files) / total_files) * 100
        print(f"  {category:>6s}: {len(cat_files):>2}개 ({pct:5.1f}%) | {cat_size:>8,} bytes")

# 정리
shutil.rmtree(temp_dir)
print()
print("확장자별 파일 분류 예제를 성공적으로 완료했습니다!")
