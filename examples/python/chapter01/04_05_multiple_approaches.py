# examples/python/chapter01/04_05_multiple_approaches.py
# AI에게 같은 문제를 여러 방법으로 풀어달라고 요청한 결과

from functools import reduce

numbers = [34, 67, 23, 89, 12, 45, 78, 56, 90, 11]
print(f"숫자 리스트: {numbers}")
print()

# === 방법 1: for 루프 사용 ===
print("--- 방법 1: for 루프 ---")

def find_max_loop(numbers):
    """반복문으로 최댓값 찾기"""
    max_value = numbers[0]
    for num in numbers[1:]:
        if num > max_value:
            max_value = num
    return max_value

result1 = find_max_loop(numbers)
print(f"최댓값: {result1}")
print("장점: 로직을 명확히 이해할 수 있음")
print()

# === 방법 2: 내장 함수 사용 ===
print("--- 방법 2: 내장 함수 max() ---")

result2 = max(numbers)
print(f"최댓값: {result2}")
print("장점: 간결하고 가독성이 높음")
print()

# === 방법 3: reduce 사용 ===
print("--- 방법 3: functools.reduce() ---")

result3 = reduce(lambda a, b: a if a > b else b, numbers)
print(f"최댓값: {result3}")
print("장점: 함수형 프로그래밍 스타일")
print()

# === 결과 비교 ===
print("=== 결과 비교 ===")
print(f"방법 1 (for 루프): {result1}")
print(f"방법 2 (내장 함수): {result2}")
print(f"방법 3 (reduce):    {result3}")
print(f"모든 결과가 동일: {result1 == result2 == result3}")
