"""
예제 13-4: IndexError — 리스트 인덱스 범위 초과 (수정 완료)
============================================================
수정: len()으로 리스트 길이를 확인하고, 안전한 접근 방법 사용
"""

# 수정된 코드: 안전한 인덱스 접근
fruits = ["사과", "바나나", "딸기", "포도", "수박"]

# 방법 1: len()으로 길이 확인
print(f"과일 목록 (총 {len(fruits)}개):")
for i in range(len(fruits)):     # ← len(fruits) = 5, range(5) = 0~4
    print(f"  {i + 1}번: {fruits[i]}")

# 방법 2: enumerate 사용 (더 파이썬다운 방법!)
print("\nenumerate로 출력:")
for idx, fruit in enumerate(fruits, start=1):
    print(f"  {idx}번: {fruit}")

# 방법 3: 인덱스 접근 전 범위 확인
target_index = 5
if target_index < len(fruits):
    print(f"\n{target_index}번 인덱스: {fruits[target_index]}")
else:
    print(f"\n{target_index}번 인덱스는 범위를 벗어났습니다! (유효 범위: 0~{len(fruits) - 1})")
