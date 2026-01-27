"""
예제 17-5: 에러 처리
API 요청에서 발생할 수 있는 다양한 에러를 처리하는 방법을 배웁니다.
"""

import urllib.request
import urllib.error
import json


def handle_http_errors():
    """HTTP 에러 코드별 처리를 보여줍니다."""

    # 다양한 HTTP 에러 상황 테스트
    test_urls = [
        ("https://httpbin.org/status/200", "정상 응답"),
        ("https://httpbin.org/status/404", "존재하지 않는 리소스"),
        ("https://httpbin.org/status/500", "서버 내부 에러"),
        ("https://httpbin.org/status/403", "접근 권한 없음"),
    ]

    for url, description in test_urls:
        print(f"\n테스트: {description} ({url.split('/')[-1]})")
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                print(f"  성공! 상태 코드: {response.status}")

        except urllib.error.HTTPError as e:
            # HTTP 에러 (4xx, 5xx)
            print(f"  HTTP 에러 발생!")
            print(f"  상태 코드: {e.code}")
            print(f"  에러 메시지: {e.reason}")

            # 에러 코드별 안내 메시지
            if e.code == 404:
                print(f"  안내: 요청한 리소스를 찾을 수 없습니다.")
            elif e.code == 403:
                print(f"  안내: 접근 권한이 없습니다. 인증을 확인하세요.")
            elif e.code == 500:
                print(f"  안내: 서버에 문제가 발생했습니다. 잠시 후 다시 시도하세요.")

        except urllib.error.URLError as e:
            # 네트워크 에러 (DNS 실패, 연결 거부 등)
            print(f"  네트워크 에러: {e.reason}")

        except Exception as e:
            print(f"  예기치 않은 에러: {e}")


def handle_network_error():
    """네트워크 연결 에러 처리를 보여줍니다."""
    print("\n\n--- 네트워크 에러 처리 ---")

    # 존재하지 않는 도메인으로 요청
    fake_url = "https://this-domain-does-not-exist-12345.com/api"

    try:
        with urllib.request.urlopen(fake_url, timeout=5) as response:
            print(f"응답: {response.read()}")

    except urllib.error.URLError as e:
        print(f"URL 에러 발생!")
        print(f"  에러 유형: {type(e.reason).__name__}")
        print(f"  에러 내용: {e.reason}")
        print(f"  해결 방법: 인터넷 연결 상태와 URL을 확인하세요.")


def safe_api_call(url):
    """안전하게 API를 호출하는 함수 (재사용 가능한 패턴)."""
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"success": True, "data": data, "status": response.status}

    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}", "status": e.code}

    except urllib.error.URLError as e:
        return {"success": False, "error": f"네트워크 에러: {e.reason}", "status": None}

    except json.JSONDecodeError:
        return {"success": False, "error": "JSON 파싱 실패", "status": None}

    except Exception as e:
        return {"success": False, "error": f"알 수 없는 에러: {e}", "status": None}


def demonstrate_safe_api_call():
    """안전한 API 호출 패턴을 시연합니다."""
    print("\n\n--- 안전한 API 호출 패턴 ---")

    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/99999",
    ]

    for url in urls:
        print(f"\n요청: {url}")
        result = safe_api_call(url)

        if result["success"]:
            print(f"  성공 (상태: {result['status']})")
            title = result["data"].get("title", "N/A")
            print(f"  제목: {title[:50]}")
        else:
            print(f"  실패: {result['error']}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-5: 에러 처리")
    print("=" * 50)
    handle_http_errors()
    handle_network_error()
    demonstrate_safe_api_call()
