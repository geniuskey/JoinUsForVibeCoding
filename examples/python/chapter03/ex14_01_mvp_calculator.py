"""
예제 14-1: MVP 계산기 (덧셈만)
================================
반복적 개발의 첫 단계 — 가장 단순한 버전부터 시작합니다.
MVP(Minimum Viable Product)는 '최소 기능 제품'으로,
핵심 기능 하나만 동작하는 가장 작은 버전을 말합니다.

이 계산기는 오직 '덧셈'만 할 수 있습니다.
하지만 이것만으로도 "동작하는 소프트웨어"입니다!
"""


def add(a, b):
    """두 숫자를 더합니다."""
    return a + b


def main():
    print("=" * 40)
    print("  MVP 계산기 v0.1 — 덧셈 전용")
    print("=" * 40)

    try:
        num1 = float(input("첫 번째 숫자: "))
        num2 = float(input("두 번째 숫자: "))
        result = add(num1, num2)
        print(f"\n결과: {num1} + {num2} = {result}")
    except ValueError:
        print("오류: 숫자를 입력해주세요.")

    print("\n[MVP 완료] 덧셈 기능이 동작합니다!")
    print("다음 단계: 사칙연산 추가 예정...")


if __name__ == "__main__":
    main()
