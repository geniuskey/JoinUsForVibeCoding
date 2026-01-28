"""
Chapter 22 - 성능 최적화
예제 22-03: 프로파일링 결과 분석

cProfile 모듈을 사용하여 프로그램의 성능 병목 지점을 찾는 방법을 알아봅니다.
프로파일링은 어떤 함수가 가장 많은 시간을 소비하는지 분석하여
최적화 대상을 정확히 파악할 수 있게 해줍니다.
"""

import cProfile
import io
import pstats
import time


# --- 분석 대상 코드 ---

def read_data(size):
    """데이터 읽기 시뮬레이션"""
    data = []
    for i in range(size):
        data.append({"id": i, "value": i * 2.5, "name": f"item_{i}"})
    return data


def filter_data(data, threshold):
    """조건에 맞는 데이터 필터링"""
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(item)
    return result


def sort_data(data):
    """데이터 정렬"""
    return sorted(data, key=lambda x: x["value"], reverse=True)


def format_output(data):
    """결과 포맷팅 (의도적으로 느리게 구현)"""
    lines = []
    for item in data:
        # 비효율적인 문자열 연결
        line = ""
        line = line + "ID: " + str(item["id"])
        line = line + " | "
        line = line + "값: " + str(item["value"])
        line = line + " | "
        line = line + "이름: " + item["name"]
        lines.append(line)
    return "\n".join(lines)


def calculate_statistics(data):
    """통계 계산 (의도적으로 비효율적)"""
    # 매번 전체를 순회하는 비효율적 방식
    total = sum(item["value"] for item in data)
    count = len(data)
    average = total / count if count > 0 else 0

    # 최대/최소를 별도 순회로 찾음
    max_val = max(item["value"] for item in data)
    min_val = min(item["value"] for item in data)

    # 분산 계산 (추가 순회)
    variance = sum((item["value"] - average) ** 2 for item in data) / count

    return {
        "total": total,
        "count": count,
        "average": average,
        "max": max_val,
        "min": min_val,
        "variance": variance,
    }


def process_pipeline(size=50000):
    """전체 데이터 처리 파이프라인"""
    # 1. 데이터 읽기
    data = read_data(size)

    # 2. 필터링
    filtered = filter_data(data, threshold=50000)

    # 3. 정렬
    sorted_data = sort_data(filtered)

    # 4. 통계 계산
    stats = calculate_statistics(sorted_data)

    # 5. 포맷팅 (상위 100개만)
    output = format_output(sorted_data[:100])

    return stats, output


def run_profiling():
    """cProfile로 프로파일링 실행"""
    # 프로파일러 생성
    profiler = cProfile.Profile()

    # 프로파일링 시작
    profiler.enable()
    stats_result, output = process_pipeline(50000)
    profiler.disable()

    return profiler, stats_result


def print_profile_results(profiler):
    """프로파일링 결과를 보기 좋게 출력"""
    # pstats로 결과 분석
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)

    # 누적 시간 기준 정렬
    stats.sort_stats("cumulative")

    print("\n[ 누적 시간 기준 상위 15개 함수 ]")
    print("-" * 70)
    stats.print_stats(15)
    print(stream.getvalue())

    # 자체 시간(tottime) 기준 정렬
    stream2 = io.StringIO()
    stats2 = pstats.Stats(profiler, stream=stream2)
    stats2.sort_stats("tottime")

    print("\n[ 자체 실행 시간 기준 상위 10개 함수 ]")
    print("-" * 70)
    stats2.print_stats(10)
    print(stream2.getvalue())


if __name__ == "__main__":
    print("=" * 70)
    print("  cProfile 프로파일링 분석")
    print("=" * 70)

    # --- 1단계: 프로파일링 실행 ---
    print("\n[1단계] 프로파일링 실행 중...")
    profiler, stats_result = run_profiling()

    # --- 2단계: 결과 출력 ---
    print("[2단계] 프로파일링 결과 분석")
    print_profile_results(profiler)

    # --- 3단계: 통계 결과 확인 ---
    print("\n[ 데이터 처리 통계 결과 ]")
    print("-" * 40)
    for key, value in stats_result.items():
        if isinstance(value, float):
            print(f"  {key:<12}: {value:>15,.2f}")
        else:
            print(f"  {key:<12}: {value:>15,}")

    # --- 프로파일링 결과 해석 가이드 ---
    print("\n[ 프로파일링 결과 읽는 방법 ]")
    print("-" * 50)
    print("  ncalls    : 함수 호출 횟수")
    print("  tottime   : 함수 자체 실행 시간 (하위 함수 제외)")
    print("  percall   : 호출당 평균 시간 (tottime / ncalls)")
    print("  cumtime   : 누적 시간 (하위 함수 포함)")
    print("  percall   : 호출당 누적 평균 시간")
    print("  filename  : 파일명:줄번호(함수명)")
    print()
    print("  tip: tottime이 가장 큰 함수가 최적화 1순위입니다!")
    print("  tip: cumtime은 해당 함수와 그 안에서 호출하는")
    print("       모든 함수의 시간을 포함합니다.")
