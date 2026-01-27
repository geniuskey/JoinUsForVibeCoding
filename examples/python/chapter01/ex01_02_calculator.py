# examples/python/chapter01/ex01_02_calculator.py
# 바이브 코딩으로 만든 간단한 계산기
# AI에게 "두 숫자를 입력받아 사칙연산을 해주는 계산기를 만들어줘"라고 요청

def calculate(a, b, operator):
    """두 숫자와 연산자를 받아 계산 결과를 반환합니다."""
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            return "오류: 0으로 나눌 수 없습니다"
        return a / b
    else:
        return "오류: 지원하지 않는 연산자입니다"

# 계산 예시
print("=== 간단한 계산기 ===")
print(f"10 + 3 = {calculate(10, 3, '+')}")
print(f"10 - 3 = {calculate(10, 3, '-')}")
print(f"10 * 3 = {calculate(10, 3, '*')}")
print(f"10 / 3 = {calculate(10, 3, '/'):.2f}")
print(f"10 / 0 = {calculate(10, 0, '/')}")
