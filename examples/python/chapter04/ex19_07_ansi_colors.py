#!/usr/bin/env python3
"""
예제 19-7: ANSI 색상 출력
외부 라이브러리 없이 ANSI 이스케이프 코드를 사용하여 터미널에 색상을 출력합니다.
"""

import sys


# ANSI 이스케이프 코드 상수
class Color:
    """ANSI 색상 코드 모음"""
    # 리셋
    RESET = "\033[0m"

    # 기본 전경색
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 밝은 전경색
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    # 스타일
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"

    # 배경색
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colorize(text, *styles):
    """텍스트에 ANSI 스타일을 적용합니다."""
    style_str = "".join(styles)
    return f"{style_str}{text}{Color.RESET}"


def print_color_demo():
    """색상 데모를 출력합니다."""
    print(colorize("=== ANSI 색상 출력 데모 ===", Color.BOLD, Color.BRIGHT_CYAN))
    print()

    # 기본 색상
    print(colorize("[1] 기본 색상", Color.BOLD))
    colors = [
        ("빨강", Color.RED),
        ("초록", Color.GREEN),
        ("노랑", Color.YELLOW),
        ("파랑", Color.BLUE),
        ("마젠타", Color.MAGENTA),
        ("시안", Color.CYAN),
    ]
    for name, color in colors:
        print(f"  {colorize(name, color)}", end="")
    print()
    print()

    # 밝은 색상
    print(colorize("[2] 밝은 색상", Color.BOLD))
    bright_colors = [
        ("밝은 빨강", Color.BRIGHT_RED),
        ("밝은 초록", Color.BRIGHT_GREEN),
        ("밝은 노랑", Color.BRIGHT_YELLOW),
        ("밝은 파랑", Color.BRIGHT_BLUE),
        ("밝은 마젠타", Color.BRIGHT_MAGENTA),
        ("밝은 시안", Color.BRIGHT_CYAN),
    ]
    for name, color in bright_colors:
        print(f"  {colorize(name, color)}", end="")
    print()
    print()

    # 스타일
    print(colorize("[3] 텍스트 스타일", Color.BOLD))
    print(f"  {colorize('굵은 텍스트', Color.BOLD)}")
    print(f"  {colorize('흐린 텍스트', Color.DIM)}")
    print(f"  {colorize('밑줄 텍스트', Color.UNDERLINE)}")
    print(f"  {colorize('반전 텍스트', Color.REVERSE)}")
    print()

    # 조합
    print(colorize("[4] 스타일 조합", Color.BOLD))
    print(f"  {colorize('굵은 빨강', Color.BOLD, Color.RED)}")
    print(f"  {colorize('밑줄 파랑', Color.UNDERLINE, Color.BLUE)}")
    print(f"  {colorize('굵은 밑줄 초록', Color.BOLD, Color.UNDERLINE, Color.GREEN)}")
    print()

    # 실용적 예제: 상태 메시지
    print(colorize("[5] 실용 예제: 로그 메시지", Color.BOLD))
    print(f"  {colorize('[성공]', Color.BRIGHT_GREEN, Color.BOLD)} 파일이 저장되었습니다.")
    print(f"  {colorize('[경고]', Color.BRIGHT_YELLOW, Color.BOLD)} 디스크 공간이 부족합니다.")
    print(f"  {colorize('[오류]', Color.BRIGHT_RED, Color.BOLD)} 파일을 찾을 수 없습니다.")
    print(f"  {colorize('[정보]', Color.BRIGHT_CYAN, Color.BOLD)} 시스템이 시작되었습니다.")


if __name__ == "__main__":
    # 파이프 출력이면 색상 비활성화
    if not sys.stdout.isatty():
        # 파이프 환경에서도 데모가 보이도록 그대로 출력
        pass

    print_color_demo()
