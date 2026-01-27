"""
예제 13-4: IndexError — 리스트 인덱스 범위 초과
=================================================
흔한 오류: 리스트 길이를 넘는 인덱스 접근
"""

# 버그가 있는 코드: 인덱스 범위 초과
fruits = ["사과", "바나나", "딸기", "포도", "수박"]

print("과일 목록:")
print(f"  1번: {fruits[0]}")
print(f"  2번: {fruits[1]}")
print(f"  3번: {fruits[2]}")
print(f"  4번: {fruits[3]}")
print(f"  5번: {fruits[4]}")
print(f"  6번: {fruits[5]}")    # ← 오류! 인덱스는 0~4까지만 유효

# 반복문에서도 같은 실수 발생 가능
print("\n반복문으로 출력:")
for i in range(6):               # ← 오류! range(5) 또는 range(len(fruits)) 사용해야 함
    print(f"  {fruits[i]}")
