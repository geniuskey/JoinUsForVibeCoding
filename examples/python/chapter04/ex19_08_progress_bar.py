#!/usr/bin/env python3
"""
예제 19-8: 진행률 바
\r과 sys.stdout을 사용하여 터미널에 진행률 바를 표시합니다.
외부 라이브러리 없이 표준 라이브러리만 사용합니다.
"""

import sys
import time


def progress_bar(current, total, bar_length=40, prefix="진행"):
    """텍스트 기반 진행률 바를 출력합니다."""
    fraction = current / total
    filled = int(bar_length * fraction)
    bar = "█" * filled + "░" * (bar_length - filled)
    percent = fraction * 100
    sys.stdout.write(f"\r{prefix}: [{bar}] {percent:5.1f}% ({current}/{total})")
    sys.stdout.flush()


def spinner(duration=3, message="처리 중"):
    """회전 스피너 애니메이션을 표시합니다."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start = time.time()
    i = 0
    while time.time() - start < duration:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{frame} {message}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r✓ {message} 완료!   \n")
    sys.stdout.flush()


def countdown(seconds):
    """카운트다운을 표시합니다."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r카운트다운: {remaining}초 남음... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r카운트다운: 완료!          \n")
    sys.stdout.flush()


def multi_task_progress():
    """여러 작업의 진행률을 순차적으로 표시합니다."""
    tasks = [
        ("파일 검색", 30),
        ("데이터 분석", 50),
        ("결과 저장", 20),
    ]

    for task_name, steps in tasks:
        for i in range(steps + 1):
            progress_bar(i, steps, bar_length=30, prefix=f"{task_name:8s}")
            time.sleep(0.02)
        print("  ✓")


def main():
    print("=" * 60)
    print("  진행률 표시 데모")
    print("=" * 60)
    print()

    # 1. 기본 진행률 바
    print("[1] 기본 진행률 바")
    total = 50
    for i in range(total + 1):
        progress_bar(i, total)
        time.sleep(0.03)
    print("  완료!")
    print()

    # 2. 스피너
    print("[2] 스피너 애니메이션")
    spinner(duration=2, message="데이터 로딩")
    print()

    # 3. 카운트다운
    print("[3] 카운트다운")
    countdown(3)
    print()

    # 4. 다중 작업 진행률
    print("[4] 다중 작업 진행률")
    multi_task_progress()
    print()

    print("모든 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
