"""
예제 17-1: GET 요청 기초
urllib.request를 사용하여 GET 요청을 보내는 기본 방법을 배웁니다.
"""

import urllib.request
import json


def get_request_basic():
    """httpbin.org에 GET 요청을 보내고 응답을 받습니다."""
    url = "https://httpbin.org/get"

    try:
        # GET 요청 보내기
        with urllib.request.urlopen(url, timeout=10) as response:
            # 응답 상태 코드 확인
            status_code = response.status
            print(f"상태 코드: {status_code}")

            # 응답 헤더 확인
            content_type = response.headers.get("Content-Type")
            print(f"Content-Type: {content_type}")

            # 응답 본문 읽기
            data = response.read().decode("utf-8")
            result = json.loads(data)

            print(f"\n요청 URL: {result.get('url', 'N/A')}")
            print(f"요청 출처 IP: {result.get('origin', 'N/A')}")
            print(f"User-Agent: {result.get('headers', {}).get('User-Agent', 'N/A')}")

    except Exception as e:
        print(f"네트워크 요청 실패: {e}")
        print("\n--- 시뮬레이션 모드로 전환 ---\n")

        # 시뮬레이션 데이터
        simulated = {
            "url": "https://httpbin.org/get",
            "origin": "123.45.67.89",
            "headers": {
                "User-Agent": "Python-urllib/3.11",
                "Host": "httpbin.org",
            },
        }
        print(f"상태 코드: 200")
        print(f"Content-Type: application/json")
        print(f"\n요청 URL: {simulated['url']}")
        print(f"요청 출처 IP: {simulated['origin']}")
        print(f"User-Agent: {simulated['headers']['User-Agent']}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-1: GET 요청 기초")
    print("=" * 50)
    get_request_basic()
