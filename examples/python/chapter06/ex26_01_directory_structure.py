"""
예제 26-01: 블로그 프로젝트 디렉토리 구조 생성

마크다운 블로그 생성기의 기본 디렉토리 구조를 자동으로 만듭니다.
바이브 코딩에서는 프로젝트 골격을 AI에게 설명하고
자동으로 생성하는 것부터 시작합니다.
"""

import os
from pathlib import Path


def create_blog_structure(base_dir: str) -> dict:
    """블로그 프로젝트의 디렉토리 구조를 생성합니다.

    Args:
        base_dir: 블로그 프로젝트 루트 경로

    Returns:
        생성된 디렉토리 및 파일 목록
    """
    base = Path(base_dir)

    # 블로그 프로젝트 디렉토리 구조 정의
    directories = [
        "content/posts",       # 마크다운 글 저장소
        "content/drafts",      # 초안 저장소
        "templates",           # HTML 템플릿
        "static/css",          # CSS 스타일시트
        "static/images",       # 이미지 파일
        "static/js",           # JavaScript 파일
        "output/posts",        # 생성된 HTML 글
        "output/tags",         # 태그 페이지
        "output/static",       # 정적 파일 복사본
    ]

    # 기본 파일 정의 (파일명: 초기 내용)
    default_files = {
        "config.ini": (
            "[blog]\n"
            "title = 나의 바이브 코딩 블로그\n"
            "author = 바이브 코더\n"
            "description = AI와 함께하는 코딩 이야기\n"
            "url = https://myblog.example.com\n"
            "language = ko\n"
            "\n"
            "[build]\n"
            "output_dir = output\n"
            "content_dir = content/posts\n"
            "template_dir = templates\n"
        ),
        "content/posts/hello-world.md": (
            "---\n"
            "title: 첫 번째 글\n"
            "date: 2025-01-15\n"
            "tags: 시작, 블로그\n"
            "---\n"
            "\n"
            "# 안녕하세요!\n"
            "\n"
            "이것은 마크다운 블로그의 첫 번째 글입니다.\n"
        ),
        "templates/.gitkeep": "",
        "static/css/.gitkeep": "",
    }

    created = {"directories": [], "files": []}

    # 디렉토리 생성
    for dir_path in directories:
        full_path = base / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        created["directories"].append(str(full_path))

    # 기본 파일 생성
    for file_path, content in default_files.items():
        full_path = base / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        created["files"].append(str(full_path))

    return created


def display_tree(base_dir: str, prefix: str = "", max_depth: int = 4, current_depth: int = 0):
    """디렉토리 트리를 시각적으로 출력합니다.

    Args:
        base_dir: 출력할 디렉토리 경로
        prefix: 들여쓰기 접두사
        max_depth: 최대 깊이
        current_depth: 현재 깊이
    """
    if current_depth >= max_depth:
        return

    base = Path(base_dir)

    # 파일과 디렉토리를 분리하여 정렬
    entries = sorted(base.iterdir(), key=lambda e: (not e.is_dir(), e.name))

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "

        # 디렉토리는 / 접미사 추가
        name = f"{entry.name}/" if entry.is_dir() else entry.name
        print(f"{prefix}{connector}{name}")

        # 하위 디렉토리 재귀 탐색
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            display_tree(str(entry), prefix + extension, max_depth, current_depth + 1)


if __name__ == "__main__":
    # /tmp 아래에 블로그 프로젝트 구조 생성
    blog_dir = "/tmp/my-vibe-blog"

    print("=" * 50)
    print("  마크다운 블로그 프로젝트 구조 생성기")
    print("=" * 50)
    print()

    # 기존 디렉토리가 있으면 정리
    import shutil
    if os.path.exists(blog_dir):
        shutil.rmtree(blog_dir)

    # 구조 생성
    result = create_blog_structure(blog_dir)

    print(f"📁 프로젝트 위치: {blog_dir}")
    print()

    # 생성된 디렉토리 목록
    print(f"[생성된 디렉토리] ({len(result['directories'])}개)")
    for d in result["directories"]:
        rel = os.path.relpath(d, blog_dir)
        print(f"  + {rel}/")

    print()

    # 생성된 파일 목록
    print(f"[생성된 파일] ({len(result['files'])}개)")
    for f in result["files"]:
        rel = os.path.relpath(f, blog_dir)
        size = os.path.getsize(f)
        print(f"  + {rel} ({size} bytes)")

    print()

    # 트리 구조 출력
    print("[디렉토리 트리]")
    print(f"{os.path.basename(blog_dir)}/")
    display_tree(blog_dir)

    print()
    print("블로그 프로젝트 구조가 성공적으로 생성되었습니다!")
