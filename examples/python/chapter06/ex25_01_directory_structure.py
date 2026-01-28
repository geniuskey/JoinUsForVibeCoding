"""
예제 25-01: 디렉토리 구조 생성
- os.makedirs를 사용하여 CLI 할일 관리 앱의 프로젝트 구조를 만듭니다.
- 프로젝트에 필요한 폴더와 기본 파일을 자동으로 생성합니다.
"""

import os
import shutil
from pathlib import Path


def create_project_structure(base_dir: str) -> list[str]:
    """CLI 할일 관리 앱의 프로젝트 디렉토리 구조를 생성합니다."""

    # 프로젝트 디렉토리 구조 정의
    directories = [
        "",                    # 프로젝트 루트
        "src",                 # 소스 코드
        "src/commands",        # CLI 명령어 모듈
        "src/models",          # 데이터 모델
        "src/utils",           # 유틸리티 함수
        "data",                # 데이터 저장소
        "tests",               # 테스트 코드
    ]

    # 기본 파일 정의 (파일 경로: 파일 내용)
    files = {
        "README.md": "# CLI 할일 관리 앱\n\n바이브 코딩으로 만드는 할일 관리 도구입니다.\n",
        "src/__init__.py": '"""CLI 할일 관리 앱 패키지"""\n',
        "src/commands/__init__.py": '"""명령어 모듈"""\n',
        "src/models/__init__.py": '"""데이터 모델 모듈"""\n',
        "src/utils/__init__.py": '"""유틸리티 모듈"""\n',
        "src/main.py": '"""앱 진입점"""\n\ndef main():\n    print("할일 관리 앱 시작!")\n\nif __name__ == "__main__":\n    main()\n',
        "src/commands/add.py": '"""할일 추가 명령어"""\n',
        "src/commands/list_todos.py": '"""할일 목록 명령어"""\n',
        "src/commands/complete.py": '"""할일 완료 명령어"""\n',
        "src/commands/delete.py": '"""할일 삭제 명령어"""\n',
        "src/models/todo.py": '"""할일 데이터 모델"""\n',
        "src/utils/storage.py": '"""데이터 저장/불러오기 유틸리티"""\n',
        "src/utils/display.py": '"""화면 출력 유틸리티"""\n',
        "data/.gitkeep": "",
        "tests/__init__.py": '"""테스트 패키지"""\n',
        "tests/test_todo.py": '"""할일 모델 테스트"""\n',
    }

    created_items = []

    # 디렉토리 생성
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        # exist_ok=True: 이미 존재해도 에러 없이 넘어감
        os.makedirs(dir_path, exist_ok=True)
        created_items.append(f"[폴더] {dir_path}/")

    # 파일 생성
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        created_items.append(f"[파일] {full_path}")

    return created_items


def display_tree(directory: str, prefix: str = "", is_last: bool = True) -> None:
    """디렉토리 트리를 시각적으로 출력합니다."""
    path = Path(directory)
    connector = "└── " if is_last else "├── "

    # 루트 디렉토리는 이름만 출력
    if prefix == "":
        print(f"{path.name}/")
    else:
        print(f"{prefix}{connector}{path.name}/" if path.is_dir() else f"{prefix}{connector}{path.name}")

    if path.is_dir():
        # 자식 항목을 정렬 (폴더 먼저, 그 다음 파일)
        children = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            extension = "    " if is_last else "│   "
            new_prefix = prefix + extension if prefix else "    " if is_last else "│   "

            if child.is_dir():
                display_tree(str(child), new_prefix if prefix else "", is_last_child)
            else:
                child_connector = "└── " if is_last_child else "├── "
                child_prefix = new_prefix if prefix else ""
                print(f"{child_prefix}{child_connector}{child.name}")


if __name__ == "__main__":
    # /tmp 아래에 프로젝트 구조 생성 (실제 프로젝트 디렉토리를 더럽히지 않음)
    project_dir = "/tmp/todo-cli-app"

    # 기존 디렉토리가 있으면 삭제 (데모용)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)

    print("=" * 50)
    print("CLI 할일 관리 앱 - 프로젝트 구조 생성")
    print("=" * 50)
    print()

    # 프로젝트 구조 생성
    created = create_project_structure(project_dir)

    print(f"프로젝트 위치: {project_dir}")
    print(f"총 {len(created)}개 항목 생성 완료!")
    print()

    # 생성된 항목 목록 출력
    print("--- 생성된 항목 ---")
    for item in created:
        print(f"  {item}")
    print()

    # 트리 구조 출력
    print("--- 프로젝트 트리 ---")
    display_tree(project_dir)

    # 정리
    shutil.rmtree(project_dir)
    print()
    print("데모용 디렉토리를 정리했습니다.")
