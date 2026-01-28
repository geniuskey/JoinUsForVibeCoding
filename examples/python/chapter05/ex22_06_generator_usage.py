"""
Chapter 22 - 성능 최적화
예제 22-06: 제너레이터 활용

제너레이터(generator)를 사용하여 메모리를 효율적으로 사용하는
데이터 처리 방법을 알아봅니다. 제너레이터는 한 번에 하나의 값만
생성하므로 대용량 데이터 처리 시 메모리 사용을 획기적으로 줄입니다.
"""

import sys
import time


# --- 1. 리스트 vs 제너레이터: 기본 비교 ---

def squares_list(n):
    """리스트로 제곱수 생성 - 모든 값을 메모리에 저장"""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


def squares_generator(n):
    """제너레이터로 제곱수 생성 - 한 번에 하나씩 생성"""
    for i in range(n):
        yield i ** 2


# --- 2. 데이터 파이프라인: 리스트 vs 제너레이터 ---

def pipeline_list(data_size):
    """리스트 기반 파이프라인 - 각 단계에서 전체 리스트 생성"""
    # 1단계: 데이터 생성
    data = [i for i in range(data_size)]
    # 2단계: 필터링 (짝수만)
    filtered = [x for x in data if x % 2 == 0]
    # 3단계: 변환 (제곱)
    transformed = [x ** 2 for x in filtered]
    # 4단계: 상위 10개 선택
    result = transformed[:10]
    return result


def pipeline_generator(data_size):
    """제너레이터 기반 파이프라인 - 필요한 만큼만 처리"""
    # 1단계: 데이터 생성 (제너레이터)
    data = (i for i in range(data_size))
    # 2단계: 필터링 (제너레이터)
    filtered = (x for x in data if x % 2 == 0)
    # 3단계: 변환 (제너레이터)
    transformed = (x ** 2 for x in filtered)
    # 4단계: 상위 10개만 소비
    result = []
    for i, val in enumerate(transformed):
        if i >= 10:
            break
        result.append(val)
    return result


# --- 3. 대용량 파일 처리 시뮬레이션 ---

def process_all_at_once(lines):
    """리스트 방식: 전체 데이터를 메모리에 올려서 처리"""
    # 모든 줄을 대문자로 변환한 리스트 생성
    upper_lines = [line.upper() for line in lines]
    # 'ERROR' 포함된 줄만 필터
    error_lines = [line for line in upper_lines if "ERROR" in line]
    return len(error_lines)


def process_with_generator(lines):
    """제너레이터 방식: 한 줄씩 스트리밍 처리"""
    def to_upper(source):
        for line in source:
            yield line.upper()

    def filter_errors(source):
        for line in source:
            if "ERROR" in line:
                yield line

    # 제너레이터 체이닝 - 메모리를 거의 사용하지 않음
    upper_stream = to_upper(lines)
    error_stream = filter_errors(upper_stream)
    count = sum(1 for _ in error_stream)
    return count


def generate_log_lines(n):
    """테스트용 로그 라인 생성"""
    log_types = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    for i in range(n):
        log_type = log_types[i % len(log_types)]
        yield f"[{log_type}] 2024-01-{(i%28)+1:02d} - 메시지 #{i}: 처리 완료"


def measure(func, *args):
    """시간 측정"""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


if __name__ == "__main__":
    print("=" * 60)
    print("  제너레이터를 활용한 메모리 효율적 데이터 처리")
    print("=" * 60)

    # --- 테스트 1: 메모리 사용량 비교 ---
    print("\n[ 테스트 1: 메모리 사용량 비교 ]")
    print("-" * 50)

    n = 1_000_000

    # 리스트
    sq_list = squares_list(n)
    mem_list = sys.getsizeof(sq_list)

    # 제너레이터
    sq_gen = squares_generator(n)
    mem_gen = sys.getsizeof(sq_gen)

    print(f"  {n:,}개의 제곱수:")
    print(f"    리스트 메모리:     {mem_list:>12,} bytes ({mem_list / 1024 / 1024:.1f} MB)")
    print(f"    제너레이터 메모리: {mem_gen:>12,} bytes")
    print(f"    메모리 절약:       {mem_list / mem_gen:,.0f}배 적은 메모리 사용")

    # 제너레이터 소비 (합계 계산)
    total_gen = sum(squares_generator(n))
    total_list = sum(sq_list)
    print(f"\n    리스트 합계:     {total_list:>20,}")
    print(f"    제너레이터 합계: {total_gen:>20,}")
    print(f"    결과 일치:       {'예' if total_list == total_gen else '아니오'}")

    # 리스트 메모리 해제
    del sq_list

    # --- 테스트 2: 파이프라인 성능 비교 ---
    print("\n[ 테스트 2: 데이터 파이프라인 성능 비교 ]")
    print("-" * 50)

    sizes = [100_000, 1_000_000, 5_000_000]

    for size in sizes:
        result_list, time_list = measure(pipeline_list, size)
        result_gen, time_gen = measure(pipeline_generator, size)

        print(f"\n  데이터 크기: {size:>10,}개 (상위 10개만 필요)")
        print(f"    리스트 방식:     {time_list:.4f}초  결과: {result_list[:5]}...")
        print(f"    제너레이터 방식: {time_gen:.4f}초  결과: {result_gen[:5]}...")
        if time_gen > 0:
            print(f"    속도 향상:       {time_list / time_gen:.1f}배")

    # --- 테스트 3: 로그 처리 시뮬레이션 ---
    print("\n[ 테스트 3: 로그 처리 시뮬레이션 ]")
    print("-" * 50)

    log_size = 500_000

    # 리스트 방식
    log_lines_list = list(generate_log_lines(log_size))
    mem_log_list = sys.getsizeof(log_lines_list)
    count_list, time_list = measure(process_all_at_once, log_lines_list)

    # 제너레이터 방식
    log_gen = generate_log_lines(log_size)
    mem_log_gen = sys.getsizeof(log_gen)
    count_gen, time_gen = measure(process_with_generator, generate_log_lines(log_size))

    print(f"  로그 라인 수: {log_size:,}")
    print(f"  ERROR 라인 수: {count_list:,}")
    print(f"\n  리스트 방식:")
    print(f"    소요 시간: {time_list:.4f}초")
    print(f"    데이터 메모리: {mem_log_list:,} bytes")
    print(f"\n  제너레이터 방식:")
    print(f"    소요 시간: {time_gen:.4f}초")
    print(f"    데이터 메모리: {mem_log_gen:,} bytes")

    del log_lines_list

    # --- 테스트 4: 유용한 제너레이터 패턴 ---
    print("\n[ 보너스: 유용한 제너레이터 표현식 ]")
    print("-" * 50)

    numbers = range(1, 101)

    # 제너레이터 표현식 예시
    print(f"  1~100 짝수 합:  {sum(x for x in numbers if x % 2 == 0)}")
    print(f"  1~100 제곱 합:  {sum(x**2 for x in numbers)}")
    print(f"  1~100 최대값:   {max(x * 3 + 1 for x in numbers)}")
    print(f"  조건 만족 여부: {any(x > 99 for x in numbers)}")
    print(f"  모두 양수?:     {all(x > 0 for x in numbers)}")

    # --- 핵심 정리 ---
    print("\n[ 핵심 정리 ]")
    print("-" * 50)
    print("  1. 제너레이터는 값을 한 번에 하나씩 생성 (lazy evaluation)")
    print("  2. 대용량 데이터 처리 시 메모리를 획기적으로 절약")
    print("  3. 일부만 필요한 경우 불필요한 계산을 하지 않음")
    print("  4. 제너레이터 체이닝으로 효율적인 파이프라인 구성 가능")
    print("  5. sum(), max(), any() 등과 함께 사용하면 매우 효율적")
