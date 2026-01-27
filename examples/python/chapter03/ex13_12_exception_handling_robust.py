"""
예제 13-12: 실습 — 예외 처리 추가 (견고한 버전)
=================================================
try/except를 사용하여 다양한 오류 상황을 처리하는
견고한(robust) 계산기 프로그램

처리하는 예외:
  1. ValueError — 숫자가 아닌 입력
  2. ZeroDivisionError — 0으로 나누기
  3. 잘못된 연산자 입력
  4. KeyboardInterrupt — Ctrl+C 종료
"""

# === 예외 처리가 추가된 견고한 계산기 ===

def divide(a, b):
    """나눗셈 (0으로 나누기 방지)"""
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다!")
    return a / b


def get_number(prompt):
    """숫자 입력을 안전하게 받는 함수"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("  ⚠️ 올바른 숫자를 입력해 주세요. (예: 10, 3.14)")


def get_operator():
    """연산자 입력을 안전하게 받는 함수"""
    valid_operators = ["+", "-", "*", "/"]
    while True:
        op = input("연산자 (+, -, *, /): ").strip()
        if op in valid_operators:
            return op
        print(f"  ⚠️ 올바른 연산자를 입력해 주세요: {', '.join(valid_operators)}")


def calculate():
    """사용자 입력을 받아 계산 수행 (견고한 버전)"""
    print("=== 간단한 계산기 (견고한 버전) ===")
    print("두 숫자와 연산자를 입력하세요.")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    try:
        num1 = get_number("첫 번째 숫자: ")
        num2 = get_number("두 번째 숫자: ")
        operator = get_operator()

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            try:
                result = divide(num1, num2)
            except ZeroDivisionError as e:
                print(f"\n오류: {e}")
                return

        # 결과가 정수인 경우 깔끔하게 출력
        if result == int(result):
            result = int(result)

        print(f"\n결과: {num1} {operator} {num2} = {result}")

    except KeyboardInterrupt:
        print("\n\n계산기를 종료합니다. 안녕히 가세요!")


# 데모 실행 (입력 없이 결과 확인)
if __name__ == "__main__":
    print("=== 계산기 데모 (자동 테스트) ===\n")

    # 정상 케이스
    test_cases = [
        (10, 3, "+", "덧셈"),
        (10, 3, "-", "뺄셈"),
        (10, 3, "*", "곱셈"),
        (10, 3, "/", "나눗셈"),
    ]

    for num1, num2, op, desc in test_cases:
        if op == "+":
            result = num1 + num2
        elif op == "-":
            result = num1 - num2
        elif op == "*":
            result = num1 * num2
        elif op == "/":
            result = divide(num1, num2)
        print(f"  {desc}: {num1} {op} {num2} = {result}")

    # 0으로 나누기 테스트
    print("\n  0으로 나누기 테스트:")
    try:
        result = divide(10, 0)
    except ZeroDivisionError as e:
        print(f"    예외 처리 성공: {e}")

    print("\n모든 테스트 통과!")
