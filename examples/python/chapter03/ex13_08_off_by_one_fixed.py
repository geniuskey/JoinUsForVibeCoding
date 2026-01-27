"""
예제 13-8: Off-by-one 오류 — range() 범위 실수 (수정 완료)
============================================================
수정: range(1, 10) → range(1, 11)로 변경하여 10 포함
"""

# 수정된 코드: range(1, 11)로 10까지 포함
print("1부터 10까지의 합 계산")
print("=" * 35)

total = 0
numbers = []

for i in range(1, 11):           # ← 수정! range(1, 11)은 1~10까지 포함
    total += i
    numbers.append(i)

print(f"더한 숫자: {numbers}")
print(f"계산 결과: {total}")
print(f"기대 결과: 55")
print(f"결과 일치: {total == 55}")  # True!

# range() 동작 원리 정리
print("\n=== range() 동작 원리 ===")
print(f"range(5)     → {list(range(5))}")       # 0~4
print(f"range(1, 5)  → {list(range(1, 5))}")    # 1~4
print(f"range(1, 6)  → {list(range(1, 6))}")    # 1~5
print(f"range(1, 11) → {list(range(1, 11))}")   # 1~10
print("\n핵심: range(a, b)는 a 이상 b '미만'!")
