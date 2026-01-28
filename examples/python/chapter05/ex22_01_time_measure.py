"""
Chapter 22 - 성능 최적화
예제 22-01: 실행 시간 측정

time.time()과 time.perf_counter()를 사용하여
코드 실행 시간을 측정하는 방법을 알아봅니다.
"""

import time


def slow_sum(n):
    """느린 방식: 반복문으로 합계 계산"""
    total = 0
    for i in range(n):
        total += i
    return total


def fast_sum(n):
    """빠른 방식: 수학 공식으로 합계 계산 (가우스 공식)"""
    return n * (n - 1) // 2


def measure_with_time(func, *args):
    """time.time()을 사용한 시간 측정 (초 단위, 벽시계 시간)"""
    start = time.time()
    result = func(*args)
    end = time.time()
    elapsed = end - start
    return result, elapsed


def measure_with_perf_counter(func, *args):
    """time.perf_counter()를 사용한 시간 측정 (고해상도 타이머)"""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed


if __name__ == "__main__":
    print("=" * 60)
    print("  실행 시간 측정: time.time() vs time.perf_counter()")
    print("=" * 60)

    n = 10_000_000  # 천만

    # --- time.time() 사용 ---
    print("\n[ time.time() 사용 ]")
    print("-" * 40)

    result1, elapsed1 = measure_with_time(slow_sum, n)
    print(f"반복문 합계:  {result1:>20,}")
    print(f"소요 시간:    {elapsed1:.6f}초")

    result2, elapsed2 = measure_with_time(fast_sum, n)
    print(f"공식 합계:    {result2:>20,}")
    print(f"소요 시간:    {elapsed2:.6f}초")

    # --- time.perf_counter() 사용 ---
    print("\n[ time.perf_counter() 사용 (더 정밀) ]")
    print("-" * 40)

    result3, elapsed3 = measure_with_perf_counter(slow_sum, n)
    print(f"반복문 합계:  {result3:>20,}")
    print(f"소요 시간:    {elapsed3:.6f}초")

    result4, elapsed4 = measure_with_perf_counter(fast_sum, n)
    print(f"공식 합계:    {result4:>20,}")
    print(f"소요 시간:    {elapsed4:.6f}초")

    # --- 비교 결과 ---
    print("\n[ 비교 결과 ]")
    print("-" * 40)
    if elapsed3 > 0 and elapsed4 > 0:
        speedup = elapsed3 / elapsed4
        print(f"반복문 방식:  {elapsed3:.6f}초")
        print(f"공식 방식:    {elapsed4:.6f}초")
        print(f"속도 향상:    {speedup:,.0f}배 빠름")
    else:
        print("공식 방식이 측정 불가능할 정도로 빠릅니다!")

    # --- time.time() vs time.perf_counter() 해상도 비교 ---
    print("\n[ 타이머 해상도 비교 ]")
    print("-" * 40)
    print(f"time.time() 해상도:         {time.get_clock_info('time').resolution:.10f}초")
    print(f"time.perf_counter() 해상도: {time.get_clock_info('perf_counter').resolution:.10f}초")
    print()
    print("tip: perf_counter()는 더 높은 해상도를 제공하므로")
    print("     짧은 코드의 성능 측정에 더 적합합니다.")
