#!/usr/bin/env python3
"""
예제 19-3: 플래그 옵션
--verbose, --quiet 등 불리언 플래그를 사용하는 CLI 도구입니다.
"""

import argparse
import os


def get_directory_info(path, verbose=False, quiet=False):
    """디렉토리 정보를 수집합니다."""
    items = os.listdir(path)
    files = [f for f in items if os.path.isfile(os.path.join(path, f))]
    dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]

    if quiet:
        # 조용한 모드: 숫자만 출력
        print(f"{len(files)}개 파일, {len(dirs)}개 디렉토리")
        return

    print(f"디렉토리: {os.path.abspath(path)}")
    print(f"파일: {len(files)}개 | 디렉토리: {len(dirs)}개")

    if verbose:
        # 상세 모드: 모든 항목을 출력
        print()
        if dirs:
            print("[디렉토리 목록]")
            for d in sorted(dirs):
                full_path = os.path.join(path, d)
                sub_count = len(os.listdir(full_path))
                print(f"  📁 {d}/ ({sub_count}개 항목)")
        if files:
            print("[파일 목록]")
            for f in sorted(files):
                full_path = os.path.join(path, f)
                size = os.path.getsize(full_path)
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f}KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f}MB"
                print(f"  -- {f} ({size_str})")


def main():
    parser = argparse.ArgumentParser(
        description="디렉토리 정보를 출력하는 도구입니다."
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="조회할 디렉토리 경로 (기본값: 현재 디렉토리)"
    )

    # 상호 배타적 그룹: --verbose와 --quiet는 동시 사용 불가
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="상세 모드: 모든 파일과 디렉토리를 출력"
    )
    group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="조용한 모드: 개수만 출력"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"오류: '{args.path}'는 유효한 디렉토리가 아닙니다.")
        return

    get_directory_info(args.path, verbose=args.verbose, quiet=args.quiet)


if __name__ == "__main__":
    main()
