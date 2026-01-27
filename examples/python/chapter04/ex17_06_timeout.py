"""
예제 17-6: 타임아웃 설정
API 요청에 타임아웃을 설정하여 무한 대기를 방지하는 방법을 배웁니다.
"""

import urllib.request
import urllib.error
import json
import time


def demonstrate_timeout():
    """타임아웃 설정과 그 효과를 보여줍니다."""

    # 1. 짧은 타임아웃으로 빠른 실패 확인
    print("1. 짧은 타임아웃 (0.001초) - 실패 예상:")
    url = "https://httpbin.org/delay/3"  # 3초 지연 응답

    start = time.time()
    try:
        with urllib.request.urlopen(url, timeout=0.001) as response:
            print(f"   응답 받음: {response.status}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"   타임아웃 발생! ({elapsed:.3f}초 후)")
        print(f"   에러: {type(e).__name__}")

    # 2. 적절한 타임아웃 설정
    print(f"\n2. 적절한 타임아웃 (10초):")
    url = "https://httpbin.org/get"

    start = time.time()
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            elapsed = time.time() - start
            print(f"   응답 받음! 상태: {response.status} ({elapsed:.3f}초 소요)")
    except urllib.error.URLError as e:
        elapsed = time.time() - start
        print(f"   에러 발생: {e.reason} ({elapsed:.3f}초 후)")
    except Exception as e:
        elapsed = time.time() - start
        print(f"   에러 발생: {e} ({elapsed:.3f}초 후)")


def timeout_with_fallback():
    """타임아웃 발생 시 대체 데이터를 제공하는 패턴입니다."""
    print(f"\n3. 타임아웃 시 대체 데이터 패턴:")

    def fetch_user_info(user_id, timeout_sec=5):
        """사용자 정보를 가져옵니다. 실패 시 캐시된 기본 정보를 반환합니다."""

        # 캐시된 기본 데이터 (오프라인에서도 사용 가능)
        default_data = {
            "id": user_id,
            "name": "알 수 없음",
            "email": "정보 없음",
            "source": "캐시(기본값)",
        }

        url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

        try:
            with urllib.request.urlopen(url, timeout=timeout_sec) as response:
                data = json.loads(response.read().decode("utf-8"))
                data["source"] = "API 서버"
                return data

        except Exception as e:
            print(f"   API 호출 실패 ({e}), 기본 데이터 사용")
            return default_data

    # 정상 호출
    user = fetch_user_info(1)
    print(f"   이름: {user.get('name', 'N/A')}")
    print(f"   이메일: {user.get('email', 'N/A')}")
    print(f"   데이터 출처: {user.get('source', 'N/A')}")


def measure_response_times():
    """여러 API의 응답 시간을 측정합니다."""
    print(f"\n4. 응답 시간 측정:")

    endpoints = [
        ("https://httpbin.org/get", "httpbin GET"),
        ("https://jsonplaceholder.typicode.com/posts/1", "JSONPlaceholder 게시글"),
        ("https://jsonplaceholder.typicode.com/users/1", "JSONPlaceholder 사용자"),
    ]

    for url, name in endpoints:
        start = time.time()
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                response.read()  # 본문까지 모두 읽기
                elapsed = time.time() - start
                print(f"   {name}: {elapsed:.3f}초 (상태: {response.status})")
        except Exception as e:
            elapsed = time.time() - start
            print(f"   {name}: 실패 ({elapsed:.3f}초 후) - {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-6: 타임아웃 설정")
    print("=" * 50)
    demonstrate_timeout()
    timeout_with_fallback()
    measure_response_times()
