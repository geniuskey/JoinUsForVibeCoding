"""
예제 15-05: 디렉토리 내 파일 목록 조회
os.listdir()과 pathlib.Path.iterdir()로 파일 목록을 확인합니다.
"""
import os
import tempfile
from pathlib import Path

# --- 샘플 디렉토리 구조 생성 ---
temp_dir = tempfile.mkdtemp()
sample_dir = os.path.join(temp_dir, "my_project")
os.makedirs(sample_dir)

# 샘플 파일 생성
sample_files = [
    "main.py",
    "utils.py",
    "config.json",
    "README.md",
    "requirements.txt",
    "data.csv",
    ".gitignore",
    "test_main.py",
]

for fname in sample_files:
    filepath = os.path.join(sample_dir, fname)
    with open(filepath, "w") as f:
        f.write(f"# {fname} 샘플 파일\n")

# 샘플 하위 디렉토리 생성
sub_dirs = ["src", "tests", "docs"]
for d in sub_dirs:
    os.makedirs(os.path.join(sample_dir, d))

# --- 방법 1: os.listdir() ---
print("=" * 50)
print("방법 1: os.listdir()")
print("=" * 50)
items = os.listdir(sample_dir)
print(f"항목 수: {len(items)}")
for item in sorted(items):
    full_path = os.path.join(sample_dir, item)
    item_type = "디렉토리" if os.path.isdir(full_path) else "파일"
    print(f"  [{item_type:>4s}] {item}")

# --- 방법 2: os.scandir() ---
print()
print("=" * 50)
print("방법 2: os.scandir() (더 효율적)")
print("=" * 50)
with os.scandir(sample_dir) as entries:
    for entry in sorted(entries, key=lambda e: e.name):
        entry_type = "디렉토리" if entry.is_dir() else "파일"
        if entry.is_file():
            size = entry.stat().st_size
            print(f"  [{entry_type:>4s}] {entry.name} ({size} bytes)")
        else:
            print(f"  [{entry_type:>4s}] {entry.name}/")

# --- 방법 3: pathlib.Path.iterdir() ---
print()
print("=" * 50)
print("방법 3: pathlib.Path.iterdir() (현대적 방법)")
print("=" * 50)
project_path = Path(sample_dir)

files = []
dirs = []
for item in project_path.iterdir():
    if item.is_file():
        files.append(item)
    elif item.is_dir():
        dirs.append(item)

print(f"디렉토리: {len(dirs)}개")
for d in sorted(dirs):
    print(f"  📁 {d.name}/")

print(f"\n파일: {len(files)}개")
for f in sorted(files):
    print(f"  📄 {f.name} (확장자: {f.suffix or '없음'})")

# --- 파일만 필터링 ---
print()
print("=" * 50)
print("파이썬 파일만 필터링")
print("=" * 50)
python_files = list(project_path.glob("*.py"))
print(f"Python 파일 ({len(python_files)}개):")
for pf in sorted(python_files):
    print(f"  {pf.name}")

# 정리
import shutil
shutil.rmtree(temp_dir)
print()
print("디렉토리 탐색 예제를 성공적으로 완료했습니다!")
