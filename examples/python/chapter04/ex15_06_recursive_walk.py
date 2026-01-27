"""
예제 15-06: 재귀적 파일 탐색
os.walk()와 pathlib의 rglob()으로 하위 디렉토리까지 탐색합니다.
"""
import os
import tempfile
import shutil
from pathlib import Path

# --- 샘플 디렉토리 구조 생성 ---
temp_dir = tempfile.mkdtemp()
project = os.path.join(temp_dir, "web_project")

structure = {
    "web_project": {
        "index.html": "<html>메인 페이지</html>",
        "style.css": "body { margin: 0; }",
        "app.js": "console.log('hello');",
        "src": {
            "main.py": "# 메인 모듈",
            "utils.py": "# 유틸리티",
            "models": {
                "user.py": "# 사용자 모델",
                "product.py": "# 상품 모델",
            },
        },
        "tests": {
            "test_main.py": "# 메인 테스트",
            "test_utils.py": "# 유틸 테스트",
        },
        "docs": {
            "guide.md": "# 가이드",
            "api.md": "# API 문서",
        },
        "data": {
            "users.csv": "이름,나이",
            "config.json": "{}",
        },
    }
}

def create_structure(base, struct):
    for name, content in struct.items():
        path = os.path.join(base, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

os.makedirs(project, exist_ok=True)
create_structure(temp_dir, structure)

# --- 방법 1: os.walk() ---
print("=" * 50)
print("방법 1: os.walk()로 모든 파일 탐색")
print("=" * 50)
file_count = 0
dir_count = 0
for dirpath, dirnames, filenames in os.walk(project):
    # 현재 디렉토리의 상대 경로
    rel_dir = os.path.relpath(dirpath, project)
    level = rel_dir.count(os.sep)
    indent = "  " * level
    dir_name = os.path.basename(dirpath)
    print(f"{indent}[{dir_name}/]")
    dir_count += 1

    # 파일 출력
    for filename in sorted(filenames):
        print(f"{indent}  {filename}")
        file_count += 1

print(f"\n총 디렉토리: {dir_count}개, 총 파일: {file_count}개")

# --- 방법 2: pathlib.rglob() ---
print()
print("=" * 50)
print("방법 2: pathlib.rglob()으로 모든 파일 탐색")
print("=" * 50)
project_path = Path(project)

all_files = sorted(project_path.rglob("*"))
print("모든 항목:")
for item in all_files:
    rel = item.relative_to(project_path)
    if item.is_dir():
        print(f"  [DIR]  {rel}/")
    else:
        print(f"  [FILE] {rel}")

# --- 특정 확장자 파일 찾기 ---
print()
print("=" * 50)
print("Python 파일만 재귀적으로 찾기 (rglob)")
print("=" * 50)
python_files = sorted(project_path.rglob("*.py"))
print(f"Python 파일 ({len(python_files)}개):")
for pf in python_files:
    rel = pf.relative_to(project_path)
    print(f"  {rel}")

# --- 마크다운 파일 찾기 ---
print()
print("=" * 50)
print("마크다운 파일만 재귀적으로 찾기")
print("=" * 50)
md_files = sorted(project_path.rglob("*.md"))
print(f"마크다운 파일 ({len(md_files)}개):")
for mf in md_files:
    rel = mf.relative_to(project_path)
    print(f"  {rel}")

# --- os.walk()로 특정 디렉토리 제외 ---
print()
print("=" * 50)
print("os.walk()에서 특정 디렉토리 제외하기")
print("=" * 50)
exclude_dirs = {"tests", "docs"}
print(f"제외 디렉토리: {exclude_dirs}")
print()
for dirpath, dirnames, filenames in os.walk(project):
    # 제외할 디렉토리를 dirnames에서 제거 (탐색 중단)
    dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

    rel_dir = os.path.relpath(dirpath, project)
    for filename in sorted(filenames):
        rel_path = os.path.join(rel_dir, filename) if rel_dir != "." else filename
        print(f"  {rel_path}")

# 정리
shutil.rmtree(temp_dir)
print()
print("재귀적 파일 탐색 예제를 성공적으로 완료했습니다!")
