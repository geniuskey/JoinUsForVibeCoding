"""
예제 13-3: TypeError — 문자열과 정수 결합 오류
================================================
흔한 오류: print()에서 문자열과 숫자를 + 연산자로 연결
"""

# 버그가 있는 코드: 문자열 + 정수 결합 시도
product_name = "노트북"
price = 1500000
quantity = 3

# TypeError: 문자열과 정수는 + 연산자로 직접 결합 불가
total = price * quantity
print("상품: " + product_name)
print("수량: " + quantity + "개")           # ← 오류 발생!
print("총 금액: " + total + "원")           # ← 오류 발생!
