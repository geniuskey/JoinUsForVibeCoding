"""
예제 2-2: Copilot 스타일 자동완성 예시

GitHub Copilot이 등장하면서 주석(코멘트)을 작성하면
AI가 코드를 자동완성하는 방식이 대중화되었습니다.

아래 코드는 개발자가 주석을 작성하고,
Copilot이 그에 맞는 코드를 자동 생성하는 과정을 시뮬레이션합니다.
"""

# === 개발자가 작성한 주석 → Copilot이 자동완성한 코드 ===

# 1. 리스트에서 짝수만 필터링하는 함수
def filter_even_numbers(numbers):
    """주어진 리스트에서 짝수만 반환합니다."""
    return [n for n in numbers if n % 2 == 0]


# 2. 문자열을 뒤집는 함수
def reverse_string(text):
    """주어진 문자열을 뒤집어 반환합니다."""
    return text[::-1]


# 3. 두 리스트를 딕셔너리로 합치는 함수
def merge_to_dict(keys, values):
    """두 리스트를 키-값 쌍의 딕셔너리로 합칩니다."""
    return dict(zip(keys, values))


# 4. 온도를 섭씨에서 화씨로 변환하는 함수
def celsius_to_fahrenheit(celsius):
    """섭씨 온도를 화씨로 변환합니다."""
    return celsius * 9 / 5 + 32


# 5. 리스트의 중복을 제거하고 정렬하는 함수
def unique_sorted(items):
    """리스트의 중복을 제거하고 정렬된 결과를 반환합니다."""
    return sorted(set(items))


# 실행 및 결과 확인
if __name__ == "__main__":
    print("=== Copilot 스타일 자동완성 예시 ===")
    print()

    # 1. 짝수 필터링
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"1. 짝수 필터링")
    print(f"   입력: {numbers}")
    print(f"   결과: {filter_even_numbers(numbers)}")
    print()

    # 2. 문자열 뒤집기
    text = "바이브 코딩"
    print(f"2. 문자열 뒤집기")
    print(f"   입력: {text}")
    print(f"   결과: {reverse_string(text)}")
    print()

    # 3. 리스트 → 딕셔너리
    keys = ["이름", "나이", "직업"]
    values = ["김개발", 28, "개발자"]
    print(f"3. 리스트를 딕셔너리로")
    print(f"   키: {keys}")
    print(f"   값: {values}")
    print(f"   결과: {merge_to_dict(keys, values)}")
    print()

    # 4. 온도 변환
    temp = 25
    print(f"4. 온도 변환")
    print(f"   섭씨: {temp}°C")
    print(f"   화씨: {celsius_to_fahrenheit(temp)}°F")
    print()

    # 5. 중복 제거 및 정렬
    items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"5. 중복 제거 및 정렬")
    print(f"   입력: {items}")
    print(f"   결과: {unique_sorted(items)}")
