"""
예제 17-11: 재시도 로직
API 호출 실패 시 지수 백오프(exponential backoff)를 사용한 재시도 전략을 배웁니다.
"""

import urllib.request
import urllib.error
import json
import time
import random


def simple_retry(url, max_retries=3):
    """단순 재시도: 고정 간격으로 재시도합니다."""
    print(f"1. 단순 재시도 (최대 {max_retries}회):")

    for attempt in range(1, max_retries + 1):
        print(f"   시도 {attempt}/{max_retries}...", end=" ")
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "VibeCoding-Book/1.0")

            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                print(f"성공! (상태: {response.status})")
                return data

        except Exception as e:
            print(f"실패 ({e})")
            if attempt < max_retries:
                wait_time = 1  # 고정 1초 대기
                print(f"   {wait_time}초 후 재시도...")
                time.sleep(wait_time)

    print(f"   모든 시도 실패!")
    return None


def retry_with_exponential_backoff(url, max_retries=4, base_delay=0.5):
    """지수 백오프 재시도: 대기 시간이 점점 늘어납니다."""
    print(f"\n2. 지수 백오프 재시도 (최대 {max_retries}회):")

    for attempt in range(1, max_retries + 1):
        print(f"   시도 {attempt}/{max_retries}...", end=" ")
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "VibeCoding-Book/1.0")

            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                print(f"성공! (상태: {response.status})")
                return data

        except urllib.error.HTTPError as e:
            print(f"HTTP 에러 {e.code}")
            # 4xx 에러는 재시도해도 결과가 같으므로 즉시 중단
            if 400 <= e.code < 500 and e.code != 429:
                print(f"   클라이언트 에러 ({e.code}) - 재시도하지 않습니다.")
                return None

        except Exception as e:
            print(f"실패 ({e})")

        if attempt < max_retries:
            # 지수 백오프: 2^attempt * base_delay + 랜덤 지터
            delay = (2 ** attempt) * base_delay
            jitter = random.uniform(0, delay * 0.1)  # 10% 지터
            total_delay = delay + jitter
            print(f"   {total_delay:.2f}초 대기 후 재시도... (지수 백오프)")
            time.sleep(total_delay)

    print(f"   모든 시도 실패!")
    return None


def retry_with_rate_limit(url, max_retries=3):
    """Rate Limit(429) 에러를 올바르게 처리하는 재시도입니다."""
    print(f"\n3. Rate Limit 인식 재시도:")

    for attempt in range(1, max_retries + 1):
        print(f"   시도 {attempt}/{max_retries}...", end=" ")
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "VibeCoding-Book/1.0")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
                print(f"성공!")
                return data

        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Retry-After 헤더 확인
                retry_after = e.headers.get("Retry-After", None)
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 2 ** attempt

                print(f"Rate Limit 초과!")
                print(f"   서버 권장 대기 시간: {wait_time}초")

                if attempt < max_retries:
                    print(f"   {wait_time}초 대기 중...")
                    time.sleep(min(wait_time, 5))  # 예제에서는 최대 5초만
            else:
                print(f"HTTP 에러 {e.code}")

        except Exception as e:
            print(f"실패 ({e})")

        if attempt < max_retries:
            continue

    print(f"   모든 시도 실패!")
    return None


def demonstrate_retry_strategies():
    """다양한 재시도 전략을 비교 시연합니다."""

    # 성공하는 URL로 테스트
    success_url = "https://httpbin.org/get"

    print("--- 성공 케이스 ---")
    result = simple_retry(success_url, max_retries=2)
    if result:
        print(f"   응답 URL: {result.get('url', 'N/A')}")

    # 실패하는 URL로 테스트 (503 서버 에러)
    fail_url = "https://httpbin.org/status/503"

    print("\n--- 실패 케이스 (서버 에러 503) ---")
    result = retry_with_exponential_backoff(fail_url, max_retries=3, base_delay=0.3)

    # Rate Limit 테스트 (429)
    rate_limit_url = "https://httpbin.org/status/429"

    print("\n--- Rate Limit 케이스 (429) ---")
    result = retry_with_rate_limit(rate_limit_url, max_retries=2)


def show_backoff_schedule():
    """지수 백오프 대기 시간 스케줄을 보여줍니다."""
    print(f"\n4. 지수 백오프 대기 시간 스케줄:")
    print(f"   {'시도':>6} | {'대기 시간':>10} | {'누적 시간':>10}")
    print(f"   {'-' * 6}-+-{'-' * 10}-+-{'-' * 10}")

    base_delay = 1.0
    total = 0
    for attempt in range(1, 7):
        delay = (2 ** attempt) * base_delay
        total += delay
        print(f"   {attempt:>6} | {delay:>8.1f}초 | {total:>8.1f}초")

    print(f"\n   [참고] 실제로는 지터(jitter)를 추가하여")
    print(f"   여러 클라이언트가 동시에 재시도하는 것을 방지합니다.")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-11: 재시도 로직")
    print("=" * 50)
    demonstrate_retry_strategies()
    show_backoff_schedule()
