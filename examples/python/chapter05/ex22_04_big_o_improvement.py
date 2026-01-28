"""
Chapter 22 - 성능 최적화
예제 22-04: O(n²) → O(n) 개선

중복 찾기 알고리즘을 통해 시간 복잡도를 O(n²)에서 O(n)으로
개선하는 방법을 알아봅니다. 알고리즘 개선은 가장 효과적인
성능 최적화 방법입니다.
"""

import time
import random


def find_duplicates_brute_force(data):
    """
    O(n²) 방식: 이중 반복문으로 중복 찾기
    모든 원소 쌍을 비교하므로 데이터가 커지면 매우 느립니다.
    """
    duplicates = []
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates


def find_duplicates_with_set(data):
    """
    O(n) 방식: 집합(set)을 사용한 중복 찾기
    한 번의 순회로 중복을 찾을 수 있습니다.
    """
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


def find_duplicates_with_dict(data):
    """
    O(n) 방식: 딕셔너리(dict)를 사용한 중복 찾기 + 횟수 추적
    각 원소의 등장 횟수까지 파악할 수 있습니다.
    """
    count = {}
    for item in data:
        count[item] = count.get(item, 0) + 1
    return [item for item, cnt in count.items() if cnt > 1]


def generate_test_data(size, duplicate_ratio=0.3):
    """테스트 데이터 생성 (일정 비율의 중복 포함)"""
    unique_count = int(size * (1 - duplicate_ratio))
    base_data = list(range(unique_count))
    # 중복 데이터 추가
    duplicates = random.choices(base_data, k=size - unique_count)
    data = base_data + duplicates
    random.shuffle(data)
    return data


def measure_time(func, data):
    """함수 실행 시간 측정"""
    start = time.perf_counter()
    result = func(data)
    end = time.perf_counter()
    return result, end - start


if __name__ == "__main__":
    print("=" * 65)
    print("  알고리즘 개선: O(n²) → O(n) 중복 찾기")
    print("=" * 65)

    random.seed(42)  # 재현 가능한 결과를 위한 시드 설정

    # --- 정확성 검증 ---
    print("\n[ 정확성 검증 ]")
    print("-" * 50)
    small_data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"입력 데이터: {small_data}")

    result1 = sorted(find_duplicates_brute_force(small_data))
    result2 = sorted(find_duplicates_with_set(small_data))
    result3 = sorted(find_duplicates_with_dict(small_data))

    print(f"O(n²) 결과:  {result1}")
    print(f"O(n) set:    {result2}")
    print(f"O(n) dict:   {result3}")
    print(f"결과 일치:   {'예' if result1 == result2 == result3 else '아니오'}")

    # --- 다양한 크기에서 성능 비교 ---
    print("\n[ 데이터 크기별 성능 비교 ]")
    print("-" * 65)
    print(f"{'크기':>8} | {'O(n²) 이중루프':>14} | {'O(n) set':>12} | {'O(n) dict':>12} | {'속도향상':>8}")
    print("-" * 65)

    # O(n²)는 큰 데이터에서 매우 느리므로 크기를 제한
    test_sizes = [500, 1000, 2000, 5000]

    for size in test_sizes:
        data = generate_test_data(size)

        _, time_brute = measure_time(find_duplicates_brute_force, data)
        _, time_set = measure_time(find_duplicates_with_set, data)
        _, time_dict = measure_time(find_duplicates_with_dict, data)

        speedup_set = time_brute / time_set if time_set > 0 else float("inf")

        print(
            f"{size:>8,} | {time_brute:>12.6f}초 | {time_set:>10.6f}초 | {time_dict:>10.6f}초 | {speedup_set:>6.0f}배"
        )

    # --- O(n) 방식만으로 큰 데이터 테스트 ---
    print("\n[ O(n) 방식: 대용량 데이터 처리 ]")
    print("-" * 50)

    large_sizes = [100_000, 500_000, 1_000_000]
    for size in large_sizes:
        data = generate_test_data(size)

        _, time_set = measure_time(find_duplicates_with_set, data)
        _, time_dict = measure_time(find_duplicates_with_dict, data)

        print(f"  {size:>10,}개 → set: {time_set:.4f}초, dict: {time_dict:.4f}초")

    # --- 핵심 정리 ---
    print("\n[ 핵심 정리 ]")
    print("-" * 50)
    print("  1. O(n²) → O(n) 개선은 데이터가 클수록 효과가 극적입니다.")
    print("  2. set/dict의 탐색은 평균 O(1)이므로 중복 검사에 적합합니다.")
    print("  3. 코드 레벨 최적화보다 알고리즘 개선이 훨씬 효과적입니다.")
    print("  4. n=5000일 때 이미 수백 배 차이가 발생합니다.")
