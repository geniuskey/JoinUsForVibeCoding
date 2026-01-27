#!/usr/bin/env python3
"""
예제 19-1: 기본 argparse 사용
가장 간단한 argparse CLI 도구 — --name 인자를 받아 인사합니다.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="간단한 인사 프로그램입니다."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="세계",
        help="인사할 이름 (기본값: 세계)"
    )

    args = parser.parse_args()
    print(f"안녕하세요, {args.name}님! 바이브 코딩의 세계에 오신 것을 환영합니다!")


if __name__ == "__main__":
    main()
