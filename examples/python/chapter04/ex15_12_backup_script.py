"""
예제 15-12: 백업 스크립트
파일에 타임스탬프를 붙여 백업하는 스크립트입니다.
"""
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# --- 샘플 프로젝트 디렉토리 생성 ---
temp_dir = tempfile.mkdtemp()
project_dir = os.path.join(temp_dir, "my_project")
backup_dir = os.path.join(temp_dir, "backups")
os.makedirs(project_dir)
os.makedirs(backup_dir)

# 프로젝트 파일 생성
project_files = {
    "main.py": '''def main():
    print("바이브 코딩 프로젝트")

if __name__ == "__main__":
    main()
''',
    "config.json": '{"app_name": "vibe_app", "version": "1.0.0"}',
    "README.md": "# 바이브 코딩 프로젝트\n\n이 프로젝트는 예제입니다.\n",
    "utils.py": 'def helper():\n    return "도우미 함수"\n',
    "data.csv": "이름,점수\n김민수,95\n이서연,88\n",
}

for fname, content in project_files.items():
    fpath = os.path.join(project_dir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("=" * 60)
print("파일 백업 스크립트")
print("=" * 60)
print(f"\n프로젝트 디렉토리: my_project/")
print(f"백업 디렉토리: backups/")
print(f"프로젝트 파일: {len(project_files)}개\n")

# --- 방법 1: 개별 파일 백업 (타임스탬프 접미사) ---
print("-" * 60)
print("방법 1: 개별 파일에 타임스탬프 붙여 백업")
print("-" * 60)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

project_path = Path(project_dir)
backup_path = Path(backup_dir)
individual_backup = backup_path / "individual"
individual_backup.mkdir(exist_ok=True)

backed_up = []
for f in sorted(project_path.iterdir()):
    if f.is_file():
        # 파일이름_타임스탬프.확장자 형식
        new_name = f"{f.stem}_{timestamp}{f.suffix}"
        dest = individual_backup / new_name
        shutil.copy2(f, dest)
        backed_up.append((f.name, new_name))
        print(f"  {f.name:>15s}  →  {new_name}")

print(f"\n  총 {len(backed_up)}개 파일 백업 완료")

# --- 방법 2: 디렉토리 통째로 백업 ---
print()
print("-" * 60)
print("방법 2: 디렉토리 통째로 백업 (폴더 복사)")
print("-" * 60)
folder_backup_name = f"my_project_backup_{timestamp}"
folder_backup_dest = backup_path / folder_backup_name
shutil.copytree(project_dir, folder_backup_dest)

# 백업된 내용 확인
backup_files = list(Path(folder_backup_dest).iterdir())
print(f"  백업 폴더: {folder_backup_name}/")
print(f"  백업된 파일: {len(backup_files)}개")
for bf in sorted(backup_files):
    size = bf.stat().st_size
    print(f"    {bf.name} ({size} bytes)")

# --- 방법 3: 증분 백업 시뮬레이션 ---
print()
print("-" * 60)
print("방법 3: 변경된 파일만 백업 (증분 백업)")
print("-" * 60)

# 일부 파일 '수정' 시뮬레이션
modified_file = os.path.join(project_dir, "main.py")
with open(modified_file, "a", encoding="utf-8") as f:
    f.write('\nprint("새로운 기능 추가!")\n')

# 백업본과 비교하여 변경된 파일만 백업
incremental_dir = backup_path / f"incremental_{timestamp}"
incremental_dir.mkdir(exist_ok=True)

changed_count = 0
unchanged_count = 0

for f in sorted(project_path.iterdir()):
    if f.is_file():
        backup_copy = folder_backup_dest / f.name
        if backup_copy.exists():
            # 크기 비교 (간단한 변경 감지)
            if f.stat().st_size != backup_copy.stat().st_size:
                shutil.copy2(f, incremental_dir / f.name)
                print(f"  [변경됨] {f.name} → 백업")
                changed_count += 1
            else:
                print(f"  [동일함] {f.name} → 건너뜀")
                unchanged_count += 1
        else:
            shutil.copy2(f, incremental_dir / f.name)
            print(f"  [새파일] {f.name} → 백업")
            changed_count += 1

print(f"\n  변경/신규: {changed_count}개, 건너뜀: {unchanged_count}개")

# --- 백업 현황 요약 ---
print()
print("=" * 60)
print("백업 현황 요약")
print("=" * 60)

total_backup_size = 0
for item in backup_path.rglob("*"):
    if item.is_file():
        total_backup_size += item.stat().st_size

backup_folders = [d for d in backup_path.iterdir() if d.is_dir()]
print(f"  백업 위치: backups/")
print(f"  백업 폴더 수: {len(backup_folders)}개")
for bf in sorted(backup_folders):
    file_count = sum(1 for f in bf.rglob("*") if f.is_file())
    folder_size = sum(f.stat().st_size for f in bf.rglob("*") if f.is_file())
    print(f"    {bf.name}/ ({file_count}개 파일, {folder_size:,} bytes)")
print(f"  전체 백업 크기: {total_backup_size:,} bytes")
print(f"  백업 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 정리
shutil.rmtree(temp_dir)
print()
print("백업 스크립트 예제를 성공적으로 완료했습니다!")
