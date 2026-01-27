"""
예제 15-08: 파일 일괄 이름변경 (시뮬레이션)
파일 이름을 패턴에 따라 일괄 변경하는 방법을 시뮬레이션합니다.
실제 파일 이름을 변경하지 않고, 변경될 결과만 출력합니다.
"""
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# --- 샘플 파일 생성 ---
temp_dir = tempfile.mkdtemp()
photo_dir = os.path.join(temp_dir, "photos")
os.makedirs(photo_dir)

sample_photos = [
    "IMG_20240315_001.jpg",
    "IMG_20240315_002.jpg",
    "IMG_20240316_001.jpg",
    "IMG_20240316_002.jpg",
    "IMG_20240316_003.jpg",
    "DSC_1001.png",
    "DSC_1002.png",
    "Screenshot 2024-03-15.png",
    "photo (1).jpg",
    "photo (2).jpg",
]

for fname in sample_photos:
    fpath = os.path.join(photo_dir, fname)
    with open(fpath, "w") as f:
        f.write("fake image data")

# --- 패턴 1: 접두사 추가 ---
print("=" * 50)
print("패턴 1: 접두사 추가 (시뮬레이션)")
print("=" * 50)
prefix = "여행_"
photo_path = Path(photo_dir)
for f in sorted(photo_path.iterdir()):
    new_name = prefix + f.name
    print(f"  {f.name:>35s}  -->  {new_name}")

# --- 패턴 2: 공백을 밑줄로 교체 ---
print()
print("=" * 50)
print("패턴 2: 공백 및 특수문자를 밑줄로 교체 (시뮬레이션)")
print("=" * 50)
import re
for f in sorted(photo_path.iterdir()):
    new_name = re.sub(r'[\s()\[\]]+', '_', f.stem)
    new_name = re.sub(r'_+', '_', new_name)  # 중복 밑줄 제거
    new_name = new_name.strip('_') + f.suffix
    if new_name != f.name:
        print(f"  {f.name:>35s}  -->  {new_name}")
    else:
        print(f"  {f.name:>35s}  -->  (변경 없음)")

# --- 패턴 3: 순번으로 일괄 변경 ---
print()
print("=" * 50)
print("패턴 3: 순번으로 일괄 변경 (시뮬레이션)")
print("=" * 50)
base_name = "travel_photo"
files_sorted = sorted(photo_path.iterdir())
for i, f in enumerate(files_sorted, start=1):
    new_name = f"{base_name}_{i:03d}{f.suffix}"
    print(f"  {f.name:>35s}  -->  {new_name}")

# --- 패턴 4: 확장자 통일 (대문자 → 소문자) ---
print()
print("=" * 50)
print("패턴 4: 확장자를 소문자로 통일 (시뮬레이션)")
print("=" * 50)
# 대문자 확장자 파일 추가 시뮬레이션
mixed_case = ["Photo.JPG", "Image.PNG", "Doc.TXT", "script.py", "data.CSV"]
for fname in mixed_case:
    stem = Path(fname).stem
    ext = Path(fname).suffix.lower()
    new_name = stem + ext
    changed = " (변경)" if new_name != fname else ""
    print(f"  {fname:>15s}  -->  {new_name}{changed}")

# --- 실제 적용 함수 예시 ---
print()
print("=" * 50)
print("실제 적용시 사용할 함수 예시 (코드만 출력)")
print("=" * 50)
code = '''
def batch_rename(directory, pattern_func, dry_run=True):
    """파일 일괄 이름변경 함수

    Args:
        directory: 대상 디렉토리 경로
        pattern_func: (Path) -> str 새 이름 반환 함수
        dry_run: True면 시뮬레이션, False면 실제 변경
    """
    target = Path(directory)
    changes = []

    for f in sorted(target.iterdir()):
        if f.is_file():
            new_name = pattern_func(f)
            if new_name != f.name:
                changes.append((f, f.parent / new_name))

    for old, new in changes:
        if dry_run:
            print(f"  [시뮬레이션] {old.name} --> {new.name}")
        else:
            old.rename(new)
            print(f"  [완료] {old.name} --> {new.name}")

    print(f"총 {len(changes)}개 파일 변경{"(시뮬레이션)" if dry_run else ""}")
'''
print(code)

# 정리
shutil.rmtree(temp_dir)
print("파일 일괄 이름변경 시뮬레이션 예제를 성공적으로 완료했습니다!")
