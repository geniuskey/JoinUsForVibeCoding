"""
예제 20-01: 표준 프로젝트 구조 생성 및 출력
os.makedirs를 사용하여 파이썬 프로젝트의 표준 디렉토리 구조를 만들고,
tree 형태로 시각화합니다.
"""

import os
import tempfile
import shutil


def create_project_structure(base_path, project_name):
    """표준 파이썬 프로젝트 디렉토리 구조를 생성합니다."""
    # 프로젝트 구조 정의: (경로, 파일인지 여부, 파일 내용)
    structure = [
        # 최상위 파일들
        ("README.md", True, f"# {project_name}\n\n프로젝트 설명을 여기에 작성합니다.\n"),
        ("setup.py", True, f'from setuptools import setup\n\nsetup(name="{project_name}")\n'),
        ("pyproject.toml", True, '[build-system]\nrequires = ["setuptools"]\n'),
        ("requirements.txt", True, "# 프로젝트 의존성\n"),
        (".gitignore", True, "__pycache__/\n*.pyc\n.env\nvenv/\n"),

        # 소스 코드 패키지
        (f"src/{project_name}/__init__.py", True, f'"""패키지: {project_name}"""\n\n__version__ = "0.1.0"\n'),
        (f"src/{project_name}/main.py", True, '"""메인 모듈"""\n\ndef main():\n    print("Hello!")\n'),
        (f"src/{project_name}/utils.py", True, '"""유틸리티 함수 모음"""\n'),
        (f"src/{project_name}/config.py", True, '"""설정 관리"""\n'),

        # 테스트
        ("tests/__init__.py", True, ""),
        ("tests/test_main.py", True, '"""메인 모듈 테스트"""\n'),
        ("tests/test_utils.py", True, '"""유틸리티 테스트"""\n'),

        # 문서
        ("docs/index.md", True, "# 문서 홈\n"),
        ("docs/installation.md", True, "# 설치 방법\n"),

        # 기타 디렉토리
        ("data/", False, None),
        ("scripts/", False, None),
    ]

    project_root = os.path.join(base_path, project_name)

    for path, is_file, content in structure:
        full_path = os.path.join(project_root, path)

        if is_file:
            # 파일이면 부모 디렉토리 먼저 생성
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            # 디렉토리만 생성
            os.makedirs(full_path, exist_ok=True)

    return project_root


def print_tree(directory, prefix="", is_last=True, is_root=True):
    """디렉토리 구조를 tree 형태로 출력합니다."""
    basename = os.path.basename(directory)

    if is_root:
        print(f"{basename}/")
    else:
        connector = "└── " if is_last else "├── "
        if os.path.isdir(directory):
            print(f"{prefix}{connector}{basename}/")
        else:
            print(f"{prefix}{connector}{basename}")

    if os.path.isdir(directory):
        # 디렉토리 내부 항목 정렬 (디렉토리 먼저, 그 다음 파일)
        entries = sorted(os.listdir(directory))
        dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
        sorted_entries = dirs + files

        for i, entry in enumerate(sorted_entries):
            entry_path = os.path.join(directory, entry)
            is_last_entry = (i == len(sorted_entries) - 1)

            if is_root:
                new_prefix = ""
            else:
                new_prefix = prefix + ("    " if is_last else "│   ")

            print_tree(entry_path, new_prefix, is_last_entry, is_root=False)


def count_structure(directory):
    """디렉토리와 파일 수를 셉니다."""
    dir_count = 0
    file_count = 0
    for root, dirs, files in os.walk(directory):
        dir_count += len(dirs)
        file_count += len(files)
    return dir_count, file_count


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-01: 표준 프로젝트 구조 생성 및 출력")
    print("=" * 60)
    print()

    # 임시 디렉토리에 프로젝트 생성
    temp_dir = tempfile.mkdtemp()
    project_name = "my_awesome_app"

    try:
        print(f"프로젝트 '{project_name}' 구조를 생성합니다...")
        print()

        # 프로젝트 구조 생성
        project_root = create_project_structure(temp_dir, project_name)

        # tree 형태로 출력
        print("-" * 60)
        print("프로젝트 디렉토리 구조:")
        print("-" * 60)
        print_tree(project_root)
        print()

        # 통계 출력
        dir_count, file_count = count_structure(project_root)
        print("-" * 60)
        print(f"구조 요약: {dir_count}개 디렉토리, {file_count}개 파일")
        print("-" * 60)
        print()

        # 각 디렉토리의 역할 설명
        print("각 디렉토리의 역할:")
        roles = {
            f"src/{project_name}/": "핵심 소스 코드가 위치하는 패키지 디렉토리",
            "tests/": "테스트 코드 모음",
            "docs/": "프로젝트 문서",
            "data/": "데이터 파일 저장소",
            "scripts/": "유틸리티 스크립트 모음",
        }
        for dir_name, role in roles.items():
            print(f"  {dir_name:<25s} → {role}")

        print()
        print("프로젝트 구조가 성공적으로 생성되었습니다!")

    finally:
        # 임시 디렉토리 정리
        shutil.rmtree(temp_dir)
        print(f"(임시 디렉토리 정리 완료)")
