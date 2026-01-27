#!/usr/bin/env python3
"""
예제 19-2: 필수/선택 인자
위치 인자(필수)와 선택 인자를 함께 사용하는 CLI 도구입니다.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="파일 정보를 출력하는 CLI 도구입니다."
    )

    # 위치 인자 (필수)
    parser.add_argument(
        "filename",
        help="처리할 파일 이름 (필수)"
    )

    # 선택 인자
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="파일 인코딩 (기본값: utf-8)"
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=10,
        help="출력할 최대 줄 수 (기본값: 10)"
    )

    args = parser.parse_args()

    print(f"[파일 정보]")
    print(f"  파일명  : {args.filename}")
    print(f"  인코딩  : {args.encoding}")
    print(f"  최대 줄 : {args.lines}줄")
    print()

    # 실제 파일 읽기 시도
    try:
        with open(args.filename, "r", encoding=args.encoding) as f:
            for i, line in enumerate(f, 1):
                if i > args.lines:
                    print(f"  ... (이하 생략, 최대 {args.lines}줄)")
                    break
                print(f"  {i:4d} | {line.rstrip()}")
    except FileNotFoundError:
        print(f"  [데모 모드] '{args.filename}' 파일이 없습니다.")
        print(f"  실제 파일 경로를 지정하면 내용을 출력합니다.")


if __name__ == "__main__":
    main()
