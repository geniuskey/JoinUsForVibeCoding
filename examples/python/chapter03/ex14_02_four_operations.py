"""
예제 14-2: 기능 추가 — 사칙연산 계산기
========================================
MVP(덧셈만)에서 한 단계 발전시켜 사칙연산을 지원합니다.
반복적 개발에서는 한 번에 하나의 기능을 추가합니다.

변경 사항:
  - 뺄셈(subtract), 곱셈(multiply), 나눗셈(divide) 함수 추가
  - 연산자 선택 메뉴 추가
  - 0으로 나누기 오류 처리 추가
"""


def add(a, b):
    """두 숫자를 더합니다."""
    return a + b


def subtract(a, b):
    """두 숫자를 뺍니다."""
    return a - b


def multiply(a, b):
    """두 숫자를 곱합니다."""
    return a * b


def divide(a, b):
    """두 숫자를 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


# 연산자 매핑 딕셔너리
OPERATIONS = {
    "+": ("덧셈", add),
    "-": ("뺄셈", subtract),
    "*": ("곱셈", multiply),
    "/": ("나눗셈", divide),
}


def main():
    print("=" * 40)
    print("  계산기 v0.2 — 사칙연산")
    print("=" * 40)

    try:
        num1 = float(input("첫 번째 숫자: "))
        print("연산자를 선택하세요: +, -, *, /")
        operator = input("연산자: ").strip()
        num2 = float(input("두 번째 숫자: "))

        if operator not in OPERATIONS:
            print(f"오류: '{operator}'는 지원하지 않는 연산자입니다.")
            return

        name, func = OPERATIONS[operator]
        result = func(num1, num2)
        print(f"\n[{name}] {num1} {operator} {num2} = {result}")

    except ValueError as e:
        print(f"오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

    print("\n[v0.2 완료] 사칙연산이 동작합니다!")
    print("다음 단계: 계산 히스토리 추가 예정...")


if __name__ == "__main__":
    main()
