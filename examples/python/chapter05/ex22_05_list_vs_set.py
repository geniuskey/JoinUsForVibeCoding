"""
Chapter 22 - 성능 최적화
예제 22-05: 리스트 vs 집합 성능

리스트(list)와 집합(set)의 검색(탐색) 성능을 비교합니다.
리스트는 O(n), 집합은 O(1) 평균 시간 복잡도를 가지므로
대량 데이터 검색 시 집합이 압도적으로 빠릅니다.
"""

import time
import random


def search_in_list(data_list, targets):
    """리스트에서 검색 (O(n) per lookup)"""
    found = 0
    for target in targets:
        if target in data_list:
            found += 1
    return found


def search_in_set(data_set, targets):
    """집합에서 검색 (O(1) average per lookup)"""
    found = 0
    for target in targets:
        if target in data_set:
            found += 1
    return found


def search_in_dict(data_dict, targets):
    """딕셔너리에서 검색 (O(1) average per lookup)"""
    found = 0
    for target in targets:
        if target in data_dict:
            found += 1
    return found


def measure(func, *args):
    """실행 시간 측정"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


if __name__ == "__main__":
    print("=" * 65)
    print("  리스트 vs 집합 vs 딕셔너리: 검색 성능 비교")
    print("=" * 65)

    random.seed(42)

    # --- 테스트 1: 기본 검색 성능 비교 ---
    print("\n[ 테스트 1: 검색(in 연산) 성능 비교 ]")
    print("-" * 65)
    print(f"{'데이터 크기':>10} | {'검색 수':>7} | {'list':>10} | {'set':>10} | {'dict':>10} | {'배율':>6}")
    print("-" * 65)

    data_sizes = [1_000, 5_000, 10_000, 50_000]
    search_count = 1_000

    for size in data_sizes:
        # 데이터 준비
        all_numbers = list(range(size * 2))
        data = random.sample(all_numbers, size)

        data_list = data
        data_set = set(data)
        data_dict = {x: True for x in data}

        # 검색 대상 (절반은 존재, 절반은 미존재)
        existing = random.sample(data, search_count // 2)
        non_existing = random.sample(
            [x for x in range(size * 2, size * 3)], search_count // 2
        )
        targets = existing + non_existing
        random.shuffle(targets)

        # 성능 측정
        found_l, time_list = measure(search_in_list, data_list, targets)
        found_s, time_set = measure(search_in_set, data_set, targets)
        found_d, time_dict = measure(search_in_dict, data_dict, targets)

        ratio = time_list / time_set if time_set > 0 else float("inf")

        print(
            f"{size:>10,} | {search_count:>7,} | "
            f"{time_list:>8.4f}초 | {time_set:>8.4f}초 | {time_dict:>8.4f}초 | "
            f"{ratio:>5.0f}배"
        )

    # --- 테스트 2: 연산별 성능 비교 ---
    print("\n[ 테스트 2: 다양한 연산 성능 비교 (데이터 크기: 100,000) ]")
    print("-" * 55)

    size = 100_000
    data = list(range(size))
    random.shuffle(data)
    data_set = set(data)

    operations = []

    # 2-1. 검색 (존재하는 원소)
    target = data[size // 2]
    _, t_list = measure(lambda: target in data)
    _, t_set = measure(lambda: target in data_set)
    operations.append(("존재하는 원소 검색", t_list, t_set))

    # 2-2. 검색 (존재하지 않는 원소)
    target = size + 999
    _, t_list = measure(lambda: target in data)
    _, t_set = measure(lambda: target in data_set)
    operations.append(("존재하지 않는 원소 검색", t_list, t_set))

    # 2-3. 교집합
    other_data = list(range(size // 2, size + size // 2))
    other_set = set(other_data)

    _, t_list = measure(lambda: [x for x in data if x in set(other_data)])
    _, t_set = measure(lambda: data_set & other_set)
    operations.append(("교집합 연산", t_list, t_set))

    # 2-4. 합집합
    _, t_list = measure(lambda: list(set(data + other_data)))
    _, t_set = measure(lambda: data_set | other_set)
    operations.append(("합집합 연산", t_list, t_set))

    print(f"{'연산':>22} | {'list':>12} | {'set':>12} | {'배율':>8}")
    print("-" * 55)
    for name, t_l, t_s in operations:
        ratio = t_l / t_s if t_s > 0 else float("inf")
        print(f"{name:>22} | {t_l:>10.6f}초 | {t_s:>10.6f}초 | {ratio:>6.0f}배")

    # --- 테스트 3: 메모리 사용량 비교 ---
    print("\n[ 테스트 3: 메모리 사용량 비교 ]")
    print("-" * 45)

    import sys

    for size in [1_000, 10_000, 100_000]:
        data_l = list(range(size))
        data_s = set(range(size))
        data_d = {i: True for i in range(size)}

        mem_list = sys.getsizeof(data_l)
        mem_set = sys.getsizeof(data_s)
        mem_dict = sys.getsizeof(data_d)

        print(f"  {size:>8,}개:")
        print(f"    list: {mem_list:>10,} bytes")
        print(f"    set:  {mem_set:>10,} bytes ({mem_set/mem_list:.1f}x)")
        print(f"    dict: {mem_dict:>10,} bytes ({mem_dict/mem_list:.1f}x)")

    # --- 핵심 정리 ---
    print("\n[ 핵심 정리 ]")
    print("-" * 50)
    print("  1. 검색(in) 연산: set은 O(1), list는 O(n)")
    print("  2. 대량 데이터 검색 시 set이 수백~수천 배 빠름")
    print("  3. set은 메모리를 더 사용하지만 검색 속도로 보상")
    print("  4. 교집합/합집합 등 집합 연산도 set이 훨씬 빠름")
    print("  5. 데이터 중복 제거가 필요하면 set 사용을 고려하세요")
