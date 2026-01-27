# examples/python/chapter03/ex11_05_positive_feedback.py
# 예제 11-5: 긍정적 피드백 예시
#
# AI에게 긍정적 피드백을 주면서 기능을 확장하는 과정을 보여줍니다.
# "잘 됐어! 이제 여기에 색상 출력 추가해줘"

import sys


# ============================================================
# [1차 대화] 기본 프로그래스 바 만들어줘
# ============================================================

def basic_progress_bar():
    """1차 대화: 기본 프로그래스 바"""
    print("=" * 50)
    print("  [1차] 기본 프로그래스 바")
    print("=" * 50)
    print()

    tasks = ["데이터 로딩", "분석 처리", "결과 생성", "보고서 작성", "완료 처리"]

    for i, task in enumerate(tasks, 1):
        progress = i / len(tasks)
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        percent = progress * 100
        print(f"  [{bar}] {percent:5.1f}% - {task}")

    print()


# ============================================================
# [2차 대화] "잘 됐어! 이제 여기에 색상 출력 추가해줘"
# 긍정적 피드백 → AI가 자신감을 가지고 기능 추가
# ============================================================

# ANSI 색상 코드
class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def colored_progress_bar():
    """2차 대화: 색상이 추가된 프로그래스 바"""
    print("=" * 50)
    print("  [2차] 색상 프로그래스 바")
    print('  → "잘 됐어! 이제 여기에 색상 출력 추가해줘"')
    print("=" * 50)
    print()

    tasks = [
        ("데이터 로딩", Color.BLUE),
        ("분석 처리", Color.CYAN),
        ("결과 생성", Color.YELLOW),
        ("보고서 작성", Color.MAGENTA),
        ("완료 처리", Color.GREEN),
    ]

    for i, (task, color) in enumerate(tasks, 1):
        progress = i / len(tasks)
        bar_length = 30
        filled = int(bar_length * progress)

        # 진행률에 따른 색상 설정
        if progress < 0.3:
            bar_color = Color.RED
        elif progress < 0.7:
            bar_color = Color.YELLOW
        else:
            bar_color = Color.GREEN

        bar = f"{bar_color}{'█' * filled}{Color.RESET}{'░' * (bar_length - filled)}"
        percent = progress * 100

        status = "✓" if progress == 1.0 else "→"
        print(f"  {status} [{bar}] {color}{percent:5.1f}%{Color.RESET} - "
              f"{Color.BOLD}{task}{Color.RESET}")

    print()


# ============================================================
# [3차 대화] "멋져! 완료 시간도 표시해줘"
# 계속 긍정적 피드백 → AI가 더 나은 결과 생성
# ============================================================

def full_progress_display():
    """3차 대화: 시간 표시가 추가된 최종 버전"""
    import time

    print("=" * 50)
    print("  [3차] 시간 표시 + 색상 프로그래스 바")
    print('  → "멋져! 완료 시간도 표시해줘"')
    print("=" * 50)
    print()

    tasks = [
        ("데이터 로딩", 0.3),
        ("분석 처리", 0.5),
        ("결과 생성", 0.4),
        ("보고서 작성", 0.6),
        ("완료 처리", 0.2),
    ]

    total_time = 0.0

    for i, (task, duration) in enumerate(tasks, 1):
        progress = i / len(tasks)
        bar_length = 30
        filled = int(bar_length * progress)

        if progress < 0.3:
            bar_color = Color.RED
        elif progress < 0.7:
            bar_color = Color.YELLOW
        else:
            bar_color = Color.GREEN

        bar = f"{bar_color}{'█' * filled}{Color.RESET}{'░' * (bar_length - filled)}"
        percent = progress * 100

        total_time += duration
        time_str = f"{duration:.1f}s"

        status = f"{Color.GREEN}✓{Color.RESET}" if True else "→"
        print(f"  {status} [{bar}] {percent:5.1f}% - {Color.BOLD}{task}{Color.RESET}"
              f"  ({time_str})")

    print(f"\n  {Color.GREEN}{Color.BOLD}모든 작업 완료!{Color.RESET}"
          f" 총 소요 시간: {total_time:.1f}초")
    print()


# ============================================================
# 긍정적 피드백의 효과 설명
# ============================================================

def show_feedback_effect():
    """긍정적 피드백의 효과를 설명합니다"""
    print("\n" + "=" * 55)
    print("  긍정적 피드백이 대화에 미치는 영향")
    print("=" * 55)
    print()
    print('  1차: "프로그래스 바 만들어줘"')
    print("       → 기본적인 텍스트 프로그래스 바 생성")
    print()
    print('  2차: "잘 됐어! 이제 여기에 색상 출력 추가해줘"')
    print('        ^^^^^^^^')
    print("        긍정적 피드백으로 시작!")
    print("       → AI가 기존 코드를 유지하면서 색상 기능 추가")
    print()
    print('  3차: "멋져! 완료 시간도 표시해줘"')
    print('        ^^^^^^')
    print("        다시 긍정적 피드백!")
    print("       → AI가 더 적극적으로 기능 개선")
    print()
    print("  효과:")
    print("  • 잘 된 부분을 인정하면 AI가 그 방향을 유지합니다")
    print("  • '잘 됐어 + 추가 요청' 패턴이 매우 효과적입니다")
    print("  • AI가 기존 코드를 변경하지 않고 확장합니다")
    print("  • 대화의 흐름이 자연스럽게 이어집니다")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--basic":
        basic_progress_bar()
    elif len(sys.argv) > 1 and sys.argv[1] == "--colored":
        colored_progress_bar()
    elif len(sys.argv) > 1 and sys.argv[1] == "--full":
        full_progress_display()
    elif len(sys.argv) > 1 and sys.argv[1] == "--effect":
        show_feedback_effect()
    else:
        show_feedback_effect()
        basic_progress_bar()
        colored_progress_bar()
        full_progress_display()
