"""
예제 15-09: 중복 파일 찾기
파일 크기와 해시값을 비교하여 중복 파일을 찾습니다.
"""
import os
import tempfile
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

# --- 샘플 파일 생성 (일부는 중복 내용) ---
temp_dir = tempfile.mkdtemp()
test_dir = os.path.join(temp_dir, "documents")
os.makedirs(test_dir)

# 서로 다른 이름이지만 같은 내용을 가진 파일들
file_contents = {
    "report_final.txt": "이것은 최종 보고서입니다. 바이브 코딩 프로젝트 결과물.",
    "report_copy.txt": "이것은 최종 보고서입니다. 바이브 코딩 프로젝트 결과물.",
    "report_backup.txt": "이것은 최종 보고서입니다. 바이브 코딩 프로젝트 결과물.",
    "memo.txt": "회의 메모: 다음 주 월요일 오전 10시",
    "meeting_notes.txt": "회의 메모: 다음 주 월요일 오전 10시",
    "todo_list.txt": "할 일 목록: 파이썬 공부, 운동, 독서",
    "tasks.txt": "할 일 목록: 파이썬 공부, 운동, 독서",
    "unique_doc.txt": "이 문서는 유일한 내용입니다.",
    "another_unique.txt": "이것도 유일한 내용을 가지고 있습니다.",
    "data_analysis.txt": "데이터 분석 결과 보고서. 매출이 전년 대비 15% 증가.",
}

for fname, content in file_contents.items():
    fpath = os.path.join(test_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("=" * 60)
print("중복 파일 찾기")
print("=" * 60)
print(f"\n검사 대상: {len(file_contents)}개 파일\n")

# --- 1단계: 파일 크기별 그룹화 ---
print("-" * 60)
print("1단계: 파일 크기별 그룹화")
print("-" * 60)

size_groups = defaultdict(list)
test_path = Path(test_dir)

for f in test_path.iterdir():
    if f.is_file():
        size = f.stat().st_size
        size_groups[size].append(f)

# 같은 크기의 파일이 2개 이상인 그룹만 필터
potential_dupes = {size: files for size, files in size_groups.items() if len(files) >= 2}
print(f"  같은 크기의 파일 그룹: {len(potential_dupes)}개")
for size, files in potential_dupes.items():
    names = [f.name for f in files]
    print(f"  크기 {size:>4}bytes: {names}")

# --- 2단계: 해시값으로 정확한 중복 확인 ---
print()
print("-" * 60)
print("2단계: 해시값(SHA-256)으로 정확한 중복 확인")
print("-" * 60)

def get_file_hash(filepath, algorithm="sha256"):
    """파일의 해시값을 계산합니다."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

hash_groups = defaultdict(list)

for size, files in potential_dupes.items():
    for f in files:
        file_hash = get_file_hash(f)
        hash_groups[file_hash].append(f)

# 실제 중복 파일 (해시가 같은 2개 이상)
duplicates = {h: files for h, files in hash_groups.items() if len(files) >= 2}

# --- 결과 출력 ---
print()
print("=" * 60)
print("중복 파일 검사 결과")
print("=" * 60)

if duplicates:
    total_wasted = 0
    group_num = 0
    for file_hash, files in duplicates.items():
        group_num += 1
        file_size = files[0].stat().st_size
        wasted = file_size * (len(files) - 1)
        total_wasted += wasted

        print(f"\n  중복 그룹 {group_num}:")
        print(f"  해시: {file_hash[:16]}...")
        print(f"  크기: {file_size} bytes")
        for i, f in enumerate(files):
            marker = "(원본)" if i == 0 else "(중복)"
            print(f"    {marker} {f.name}")

    print(f"\n  {'=' * 40}")
    print(f"  중복 그룹 수: {len(duplicates)}")
    total_dupes = sum(len(files) - 1 for files in duplicates.values())
    print(f"  중복 파일 수: {total_dupes}개")
    print(f"  낭비 공간: {total_wasted:,} bytes")
else:
    print("  중복 파일이 없습니다.")

# 정리
shutil.rmtree(temp_dir)
print()
print("중복 파일 찾기 예제를 성공적으로 완료했습니다!")
