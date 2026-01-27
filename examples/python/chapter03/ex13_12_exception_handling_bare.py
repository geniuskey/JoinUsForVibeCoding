"""
예제 13-12: 실습 — 예외 처리 추가 (기본 버전)
===============================================
아래 코드는 정상적인 입력에서는 동작하지만,
예상치 못한 입력이나 상황에서 오류가 발생합니다.
AI에게 도움을 요청하여 예외 처리를 추가해 보세요!

프로그램 목적: 간단한 계산기
"""

# === 예외 처리 없는 기본 계산기 ===

def divide(a, b):
    """나눗셈"""
    return a / b


def calculate():
    """사용자 입력을 받아 계산 수행"""
    print("=== 간단한 계산기 ===")
    print("두 숫자와 연산자를 입력하세요.\n")

    num1 = float(input("첫 번째 숫자: "))
    num2 = float(input("두 번째 숫자: "))
    operator = input("연산자 (+, -, *, /): ")

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = divide(num1, num2)

    print(f"\n결과: {num1} {operator} {num2} = {result}")


# 실행
calculate()
