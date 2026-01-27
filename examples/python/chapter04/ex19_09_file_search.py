#!/usr/bin/env python3
"""
예제 19-9: 파일 검색 도구
디렉토리에서 파일 이름이나 확장자로 파일을 검색하는 CLI 도구입니다.
표준 라이브러리(argparse, os)만 사용합니다.
"""

import argparse
import os
import time


def format_size(size_bytes):
    """바이트를 읽기 좋은 크기 문자열로 변환합니다."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f}GB"


def search_files(directory, name=None, ext=None, min_size=None, max_size=None, recursive=True):
    """조건에 맞는 파일을 검색합니다."""
    results = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if matches(filepath, filename, name, ext, min_size, max_size):
                    results.append(filepath)
    else:
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    if matches(filepath, filename, name, ext, min_size, max_size):
                        results.append(filepath)
        except PermissionError:
            print(f"경고: '{directory}' 접근 권한이 없습니다.")

    return results


def matches(filepath, filename, name, ext, min_size, max_size):
    """파일이 검색 조건에 맞는지 확인합니다."""
    # 이름 필터
    if name and name.lower() not in filename.lower():
        return False

    # 확장자 필터
    if ext:
        target_ext = ext if ext.startswith(".") else f".{ext}"
        if not filename.lower().endswith(target_ext.lower()):
            return False

    # 크기 필터
    try:
        size = os.path.getsize(filepath)
        if min_size is not None and size < min_size:
            return False
        if max_size is not None and size > max_size:
            return False
    except OSError:
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="파일 검색 CLI 도구 — 이름, 확장자, 크기로 파일을 검색합니다.",
        epilog="사용 예: python ex19_09_file_search.py . --ext .py --name test"
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="검색할 디렉토리 (기본값: 현재 디렉토리)"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        help="파일 이름에 포함된 문자열"
    )
    parser.add_argument(
        "--ext", "-e",
        type=str,
        help="파일 확장자 (예: .py, .txt, .md)"
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=None,
        help="최소 파일 크기 (바이트)"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="최대 파일 크기 (바이트)"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="하위 디렉토리를 탐색하지 않음"
    )
    parser.add_argument(
        "--sort",
        choices=["name", "size", "modified"],
        default="name",
        help="정렬 기준 (기본값: name)"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"오류: '{args.directory}'는 유효한 디렉토리가 아닙니다.")
        return

    print(f"검색 디렉토리: {os.path.abspath(args.directory)}")
    conditions = []
    if args.name:
        conditions.append(f"이름 포함: '{args.name}'")
    if args.ext:
        conditions.append(f"확장자: {args.ext}")
    if args.min_size:
        conditions.append(f"최소 크기: {format_size(args.min_size)}")
    if args.max_size:
        conditions.append(f"최대 크기: {format_size(args.max_size)}")
    if conditions:
        print(f"검색 조건: {', '.join(conditions)}")
    print("-" * 60)

    results = search_files(
        args.directory,
        name=args.name,
        ext=args.ext,
        min_size=args.min_size,
        max_size=args.max_size,
        recursive=not args.no_recursive
    )

    # 정렬
    if args.sort == "name":
        results.sort(key=lambda f: os.path.basename(f).lower())
    elif args.sort == "size":
        results.sort(key=lambda f: os.path.getsize(f))
    elif args.sort == "modified":
        results.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    if not results:
        print("검색 결과가 없습니다.")
        return

    total_size = 0
    for filepath in results:
        try:
            size = os.path.getsize(filepath)
            mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(filepath)))
            total_size += size
            rel_path = os.path.relpath(filepath, args.directory)
            print(f"  {format_size(size):>8s}  {mtime}  {rel_path}")
        except OSError:
            print(f"  {'???':>8s}  {'???':16s}  {filepath}")

    print("-" * 60)
    print(f"검색 결과: {len(results)}개 파일 (총 {format_size(total_size)})")


if __name__ == "__main__":
    main()
