"""
예제 13-8: Off-by-one 오류 — range() 범위 실수
================================================
흔한 오류: 1부터 10까지의 합을 구하려는데
range(1, 10)을 사용하여 10이 포함되지 않는 경우
"""

# 버그가 있는 코드: range(1, 10)은 1~9까지만 포함!
print("1부터 10까지의 합 계산")
print("=" * 35)

total = 0
numbers = []

for i in range(1, 10):           # ← 버그! range(1, 10)은 1~9까지만 포함
    total += i
    numbers.append(i)

print(f"더한 숫자: {numbers}")
print(f"계산 결과: {total}")
print(f"기대 결과: 55")          # 1+2+...+10 = 55
print(f"결과 일치: {total == 55}")  # False!
