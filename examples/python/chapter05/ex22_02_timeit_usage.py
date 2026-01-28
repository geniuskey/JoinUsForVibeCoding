"""
Chapter 22 - 성능 최적화
예제 22-02: timeit 사용

timeit 모듈을 사용하여 코드 성능을 정확하게 측정하는 방법을 알아봅니다.
timeit은 여러 번 반복 실행하여 평균 시간을 계산하므로
일회성 측정보다 더 신뢰할 수 있는 결과를 제공합니다.
"""

import timeit


def method_concat_plus():
    """문자열 연결: + 연산자 사용"""
    result = ""
    for i in range(1000):
        result += str(i)
    return result


def method_concat_join():
    """문자열 연결: join() 사용"""
    return "".join(str(i) for i in range(1000))


def method_concat_fstring():
    """문자열 연결: f-string 사용"""
    parts = []
    for i in range(1000):
        parts.append(f"{i}")
    return "".join(parts)


def method_list_append():
    """리스트 생성: append() 사용"""
    result = []
    for i in range(10000):
        result.append(i * 2)
    return result


def method_list_comprehension():
    """리스트 생성: 리스트 컴프리헨션 사용"""
    return [i * 2 for i in range(10000)]


def method_list_map():
    """리스트 생성: map() 사용"""
    return list(map(lambda i: i * 2, range(10000)))


if __name__ == "__main__":
    print("=" * 60)
    print("  timeit 모듈을 활용한 정밀 성능 측정")
    print("=" * 60)

    repeat_count = 5       # 전체 테스트 반복 횟수
    number_per_test = 1000  # 각 테스트당 실행 횟수

    # --- 테스트 1: 문자열 연결 방법 비교 ---
    print("\n[ 테스트 1: 문자열 연결 방법 비교 ]")
    print(f"  (각 방법을 {number_per_test}번씩, {repeat_count}회 반복 측정)")
    print("-" * 50)

    str_methods = [
        ("+ 연산자", "method_concat_plus"),
        ("join()", "method_concat_join"),
        ("f-string + join", "method_concat_fstring"),
    ]

    str_results = []
    for name, func_name in str_methods:
        times = timeit.repeat(
            stmt=f"{func_name}()",
            setup=f"from __main__ import {func_name}",
            repeat=repeat_count,
            number=number_per_test,
        )
        avg_time = sum(times) / len(times)
        min_time = min(times)
        str_results.append((name, avg_time, min_time))
        print(f"  {name:<16} 평균: {avg_time:.4f}초  최소: {min_time:.4f}초")

    # 가장 빠른 방법 표시
    fastest = min(str_results, key=lambda x: x[2])
    print(f"\n  >>> 가장 빠른 방법: {fastest[0]}")

    # --- 테스트 2: 리스트 생성 방법 비교 ---
    print(f"\n[ 테스트 2: 리스트 생성 방법 비교 ]")
    print(f"  (각 방법을 {number_per_test}번씩, {repeat_count}회 반복 측정)")
    print("-" * 50)

    list_methods = [
        ("append()", "method_list_append"),
        ("리스트 컴프리헨션", "method_list_comprehension"),
        ("map()", "method_list_map"),
    ]

    list_results = []
    for name, func_name in list_methods:
        times = timeit.repeat(
            stmt=f"{func_name}()",
            setup=f"from __main__ import {func_name}",
            repeat=repeat_count,
            number=number_per_test,
        )
        avg_time = sum(times) / len(times)
        min_time = min(times)
        list_results.append((name, avg_time, min_time))
        print(f"  {name:<16} 평균: {avg_time:.4f}초  최소: {min_time:.4f}초")

    fastest = min(list_results, key=lambda x: x[2])
    print(f"\n  >>> 가장 빠른 방법: {fastest[0]}")

    # --- 테스트 3: timeit 간편 사용법 ---
    print("\n[ 테스트 3: timeit.timeit() 간편 사용법 ]")
    print("-" * 50)

    # 간단한 표현식 직접 측정
    expressions = [
        ("리스트 정렬 (sorted)", "sorted(range(1000, 0, -1))"),
        ("리스트 뒤집기 (reversed)", "list(reversed(range(1000)))"),
        ("range to list", "list(range(1000))"),
    ]

    for name, expr in expressions:
        elapsed = timeit.timeit(stmt=expr, number=10000)
        per_call = elapsed / 10000
        print(f"  {name:<28} 총: {elapsed:.4f}초  (1회: {per_call * 1000:.4f}ms)")

    # --- 결론 ---
    print("\n[ 정리 ]")
    print("-" * 50)
    print("  1. timeit.timeit()   : 총 실행 시간 반환 (간편 측정)")
    print("  2. timeit.repeat()   : 여러 번 반복 측정 (신뢰도 향상)")
    print("  3. min(times) 사용   : 최소값이 가장 신뢰할 수 있는 결과")
    print("  4. 리스트 컴프리헨션 > append() (일반적으로)")
    print("  5. join() > + 연산자 (문자열 연결 시)")
