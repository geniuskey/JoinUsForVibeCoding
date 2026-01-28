"""
Chapter 22 - 성능 최적화
예제 22-07: 캐싱 적용

functools.lru_cache를 사용하여 반복 계산을 캐싱하는 방법을 알아봅니다.
캐싱은 동일한 입력에 대해 이미 계산한 결과를 재사용하므로
반복적인 함수 호출의 성능을 획기적으로 개선합니다.
"""

import functools
import time


# --- 1. 피보나치: 캐싱 없음 vs 캐싱 있음 ---

def fibonacci_naive(n):
    """캐싱 없는 피보나치 (지수적 시간 복잡도: O(2^n))"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fibonacci_cached(n):
    """lru_cache 적용 피보나치 (선형 시간 복잡도: O(n))"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


# --- 2. 수동 캐싱 (딕셔너리 사용) ---

def fibonacci_manual_cache(n, cache=None):
    """딕셔너리를 이용한 수동 캐싱 (메모이제이션)"""
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    result = fibonacci_manual_cache(n - 1, cache) + fibonacci_manual_cache(n - 2, cache)
    cache[n] = result
    return result


# --- 3. 실용적 예: 비용이 큰 계산의 캐싱 ---

call_count = {"without_cache": 0, "with_cache": 0}


def expensive_calculation(x, y):
    """비용이 큰 계산 시뮬레이션 (캐싱 없음)"""
    call_count["without_cache"] += 1
    # 의도적으로 느린 계산
    result = 0
    for i in range(100_000):
        result += (x * y + i) % 97
    return result


@functools.lru_cache(maxsize=128)
def expensive_calculation_cached(x, y):
    """비용이 큰 계산 시뮬레이션 (캐싱 적용)"""
    call_count["with_cache"] += 1
    result = 0
    for i in range(100_000):
        result += (x * y + i) % 97
    return result


# --- 4. maxsize 설정에 따른 캐시 효율 ---

@functools.lru_cache(maxsize=4)
def small_cache_func(n):
    """작은 캐시 (최근 4개만 저장)"""
    return n ** 2 + n


def measure(func, *args):
    """시간 측정"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


if __name__ == "__main__":
    print("=" * 60)
    print("  functools.lru_cache를 활용한 캐싱 최적화")
    print("=" * 60)

    # --- 테스트 1: 피보나치 성능 비교 ---
    print("\n[ 테스트 1: 피보나치 수열 - 캐싱 효과 ]")
    print("-" * 55)

    # 캐싱 없는 버전 (작은 숫자만 테스트)
    print("\n  캐싱 없는 피보나치 (O(2^n)):")
    for n in [20, 25, 30, 35]:
        result, elapsed = measure(fibonacci_naive, n)
        print(f"    F({n:>2}) = {result:>12,}  소요: {elapsed:.4f}초")

    # 캐시 초기화
    fibonacci_cached.cache_clear()

    # 캐싱 있는 버전 (큰 숫자도 가능)
    print("\n  lru_cache 피보나치 (O(n)):")
    for n in [20, 25, 30, 35, 100, 200, 500]:
        result, elapsed = measure(fibonacci_cached, n)
        print(f"    F({n:>3}) = {result:>40,}  소요: {elapsed:.6f}초"
              if n <= 35 else
              f"    F({n:>3}) = {str(result)[:30]}...({len(str(result))}자리)  소요: {elapsed:.6f}초")

    # 캐시 통계 출력
    cache_info = fibonacci_cached.cache_info()
    print(f"\n  캐시 통계:")
    print(f"    적중(hits):    {cache_info.hits:,}회")
    print(f"    미스(misses):  {cache_info.misses:,}회")
    print(f"    현재 크기:     {cache_info.currsize:,}개")
    print(f"    최대 크기:     {'무제한' if cache_info.maxsize is None else cache_info.maxsize}")
    print(f"    적중률:        {cache_info.hits / (cache_info.hits + cache_info.misses) * 100:.1f}%")

    # --- 테스트 2: 반복 호출이 많은 계산 ---
    print("\n[ 테스트 2: 반복 호출이 많은 비용 큰 계산 ]")
    print("-" * 55)

    # 테스트 데이터: 동일한 인자로 여러 번 호출
    test_args = [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4),
                 (1, 2), (7, 8), (3, 4), (1, 2), (5, 6)]

    # 캐싱 없음
    call_count["without_cache"] = 0
    start = time.perf_counter()
    for x, y in test_args:
        expensive_calculation(x, y)
    time_no_cache = time.perf_counter() - start

    # 캐싱 있음
    call_count["with_cache"] = 0
    expensive_calculation_cached.cache_clear()
    start = time.perf_counter()
    for x, y in test_args:
        expensive_calculation_cached(x, y)
    time_cached = time.perf_counter() - start

    print(f"  총 호출 횟수:    {len(test_args)}회")
    print(f"  고유한 인자 수:  {len(set(test_args))}개")
    print()
    print(f"  캐싱 없음:")
    print(f"    실제 계산 횟수: {call_count['without_cache']}회")
    print(f"    소요 시간:      {time_no_cache:.4f}초")
    print()
    print(f"  캐싱 적용:")
    print(f"    실제 계산 횟수: {call_count['with_cache']}회")
    print(f"    소요 시간:      {time_cached:.4f}초")
    if time_cached > 0:
        print(f"    속도 향상:      {time_no_cache / time_cached:.1f}배")

    cache_info = expensive_calculation_cached.cache_info()
    print(f"    캐시 적중률:    {cache_info.hits / (cache_info.hits + cache_info.misses) * 100:.1f}%")

    # --- 테스트 3: maxsize 설정 ---
    print("\n[ 테스트 3: maxsize 설정에 따른 캐시 동작 ]")
    print("-" * 55)

    small_cache_func.cache_clear()

    # 순서대로 호출
    values = [1, 2, 3, 4, 5, 1, 2, 3]
    print(f"  maxsize=4인 캐시, 호출 순서: {values}")
    print()

    for v in values:
        result = small_cache_func(v)
        info = small_cache_func.cache_info()
        status = "적중" if info.hits > sum(1 for x in values[:values.index(v)] if x == v) else "미스"
        print(f"    f({v}) = {result:>3}  캐시: hits={info.hits}, misses={info.misses}, size={info.currsize}")

    print()
    print(f"  최종 캐시 상태: {small_cache_func.cache_info()}")
    print()
    print("  tip: maxsize가 작으면 오래된 항목이 제거(LRU)되어")
    print("       이전에 캐싱된 값도 다시 계산해야 할 수 있습니다.")

    # --- 핵심 정리 ---
    print("\n[ 핵심 정리 ]")
    print("-" * 55)
    print("  1. @lru_cache는 동일 입력의 반복 호출을 매우 빠르게 만듦")
    print("  2. 피보나치: O(2^n) → O(n)으로 개선 가능")
    print("  3. maxsize=None: 무제한 캐시 (메모리 주의)")
    print("  4. maxsize=N: 최근 N개만 유지 (LRU 정책)")
    print("  5. cache_info()로 캐시 효율을 모니터링 가능")
    print("  6. cache_clear()로 캐시를 수동 초기화 가능")
    print("  7. 인자가 해시 가능(hashable)해야 캐싱 가능")
