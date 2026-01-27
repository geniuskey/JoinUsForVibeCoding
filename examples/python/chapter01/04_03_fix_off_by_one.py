# examples/python/chapter01/04_03_fix_off_by_one.py
# AI가 생성한 코드에서 Off-by-one 오류를 발견하고 수정하는 예제

print("=== AI가 처음 생성한 코드 (버그 있음) ===")

def find_average_buggy(numbers):
    """리스트의 평균을 구하는 함수 (버그 있는 버전)"""
    total = 0
    # 버그: range(1, len(numbers))는 첫 번째 요소를 건너뜀!
    for i in range(1, len(numbers)):
        total += numbers[i]
    average = total / len(numbers)
    return average

numbers = [10, 20, 30, 40, 50]
buggy_result = find_average_buggy(numbers)
print(f"숫자: {numbers}")
print(f"버그 있는 결과: {buggy_result}")
print(f"기대하는 결과: {sum(numbers) / len(numbers)}")
print(f"결과가 올바른가? {buggy_result == sum(numbers) / len(numbers)}")

print()
print("=== 수정 요청 후 AI가 고친 코드 ===")

def find_average_fixed(numbers):
    """리스트의 평균을 구하는 함수 (수정된 버전)"""
    if not numbers:
        return 0  # 빈 리스트 처리도 추가
    total = 0
    # 수정: range(0, len(numbers))로 첫 번째 요소부터 포함
    for i in range(0, len(numbers)):
        total += numbers[i]
    average = total / len(numbers)
    return average

fixed_result = find_average_fixed(numbers)
print(f"숫자: {numbers}")
print(f"수정된 결과: {fixed_result}")
print(f"기대하는 결과: {sum(numbers) / len(numbers)}")
print(f"결과가 올바른가? {fixed_result == sum(numbers) / len(numbers)}")
