"""
예제 15-11: 이미지 파일 정리기 (시뮬레이션)
파일을 확장자별 폴더로 분류하는 정리 스크립트입니다.
실제로 파일을 이동하지 않고, 정리 계획만 출력합니다.
"""
import os
import tempfile
import shutil
from pathlib import Path
from collections import defaultdict

# --- 샘플 파일 생성 (혼잡한 다운로드 폴더 시뮬레이션) ---
temp_dir = tempfile.mkdtemp()
download_dir = os.path.join(temp_dir, "Downloads")
os.makedirs(download_dir)

messy_files = [
    # 이미지 파일
    ("vacation_001.jpg", 250000),
    ("vacation_002.jpg", 310000),
    ("screenshot_01.png", 180000),
    ("screenshot_02.png", 220000),
    ("logo_design.svg", 45000),
    ("profile_photo.gif", 89000),
    # 문서 파일
    ("resume_2024.pdf", 150000),
    ("report_q1.pdf", 420000),
    ("meeting_notes.docx", 35000),
    ("budget.xlsx", 78000),
    ("presentation.pptx", 520000),
    # 코드 파일
    ("main.py", 3400),
    ("index.html", 5600),
    ("style.css", 2100),
    ("app.js", 4200),
    # 데이터 파일
    ("users.csv", 12000),
    ("config.json", 850),
    ("database.sql", 67000),
    # 미디어 파일
    ("song.mp3", 4500000),
    ("podcast.mp4", 15000000),
    # 압축 파일
    ("backup.zip", 890000),
    ("archive.tar.gz", 1200000),
    # 기타
    ("README.md", 2800),
    ("notes.txt", 1500),
]

for fname, size in messy_files:
    fpath = os.path.join(download_dir, fname)
    with open(fpath, "w") as f:
        f.write("x" * min(size, 100))  # 실제 크기 대신 작은 데이터만

print("=" * 60)
print("파일 정리기 - 시뮬레이션")
print("=" * 60)
print(f"\n대상 폴더: Downloads/")
print(f"총 파일: {len(messy_files)}개\n")

# --- 분류 규칙 정의 ---
category_rules = {
    "이미지": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"],
    "문서": [".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt"],
    "코드": [".py", ".html", ".css", ".js", ".ts", ".java", ".cpp"],
    "데이터": [".csv", ".json", ".xml", ".sql", ".db"],
    "미디어": [".mp3", ".mp4", ".avi", ".wav", ".mkv", ".mov"],
    "압축": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "텍스트": [".txt", ".md", ".log"],
}

def get_category(filename):
    """파일의 확장자를 기반으로 카테고리를 결정합니다."""
    ext = Path(filename).suffix.lower()
    # .tar.gz 같은 이중 확장자 처리
    if filename.endswith(".tar.gz"):
        return "압축"
    for category, extensions in category_rules.items():
        if ext in extensions:
            return category
    return "기타"

# --- 분류 계획 수립 ---
plan = defaultdict(list)
download_path = Path(download_dir)

for f in download_path.iterdir():
    if f.is_file():
        category = get_category(f.name)
        size = messy_files[[name for name, _ in messy_files].index(f.name)][1]
        plan[category].append((f.name, size))

# --- 정리 계획 출력 ---
print("-" * 60)
print("정리 계획")
print("-" * 60)

total_moved = 0
for category in sorted(plan.keys()):
    files = plan[category]
    cat_size = sum(s for _, s in files)
    print(f"\n  [{category}] 폴더 (→ Downloads/{category}/)")
    print(f"  {'.' * 50}")
    for fname, fsize in sorted(files):
        size_str = format_size(fsize) if 'format_size' in dir() else f"{fsize:>10,} bytes"
        print(f"    {fname:<25s} ({fsize:>10,} bytes)")
        total_moved += 1
    print(f"  소계: {len(files)}개 파일, {cat_size:,} bytes")

# --- 실행 시뮬레이션 ---
print()
print("=" * 60)
print("시뮬레이션 실행 결과")
print("=" * 60)

for category in sorted(plan.keys()):
    folder = f"Downloads/{category}/"
    print(f"\n  [생성] {folder}")
    for fname, _ in sorted(plan[category]):
        print(f"    [이동] {fname} → {folder}{fname}")

# --- 요약 ---
print()
print("=" * 60)
print("정리 요약")
print("=" * 60)
print(f"  정리 대상: {total_moved}개 파일")
print(f"  생성 폴더: {len(plan)}개")
for category in sorted(plan.keys()):
    print(f"    - {category}/ ({len(plan[category])}개)")
print()
print("  ※ 이 결과는 시뮬레이션입니다.")
print("    실제 적용하려면 shutil.move()를 사용하세요.")

# 정리
shutil.rmtree(temp_dir)
print()
print("이미지 파일 정리기 시뮬레이션 예제를 성공적으로 완료했습니다!")
