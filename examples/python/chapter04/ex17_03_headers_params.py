"""
예제 17-3: 헤더와 파라미터
HTTP 요청에 커스텀 헤더와 쿼리 파라미터를 추가하는 방법을 배웁니다.
"""

import urllib.request
import urllib.parse
import json


def request_with_headers_and_params():
    """커스텀 헤더와 쿼리 파라미터를 포함한 요청을 보냅니다."""

    # 1. 쿼리 파라미터 추가
    base_url = "https://httpbin.org/get"
    params = {
        "language": "python",
        "topic": "vibe coding",
        "page": "1",
    }

    # URL에 쿼리 파라미터 추가
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"

    print("1. 쿼리 파라미터 구성")
    print(f"   기본 URL: {base_url}")
    print(f"   쿼리 문자열: {query_string}")
    print(f"   전체 URL: {full_url}")

    # 2. 커스텀 헤더 추가
    headers = {
        "Accept": "application/json",
        "Accept-Language": "ko-KR",
        "X-Custom-Header": "VibeCoding-Client",
        "User-Agent": "VibeCoding-Book/1.0",
    }

    print(f"\n2. 커스텀 헤더:")
    for key, value in headers.items():
        print(f"   {key}: {value}")

    try:
        # Request 객체 생성 및 헤더 추가
        req = urllib.request.Request(full_url, headers=headers)

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

            print(f"\n3. 서버 응답:")
            print(f"   받은 파라미터: {json.dumps(result.get('args', {}), ensure_ascii=False)}")
            print(f"   받은 헤더 중 일부:")
            resp_headers = result.get("headers", {})
            print(f"     Accept-Language: {resp_headers.get('Accept-Language', 'N/A')}")
            print(f"     X-Custom-Header: {resp_headers.get('X-Custom-Header', 'N/A')}")
            print(f"     User-Agent: {resp_headers.get('User-Agent', 'N/A')}")

    except Exception as e:
        print(f"\n네트워크 요청 실패: {e}")
        print("\n--- 시뮬레이션 모드로 전환 ---\n")

        print(f"3. 서버 응답 (시뮬레이션):")
        print(f"   받은 파라미터: {json.dumps(params, ensure_ascii=False)}")
        print(f"   받은 헤더 중 일부:")
        print(f"     Accept-Language: ko-KR")
        print(f"     X-Custom-Header: VibeCoding-Client")
        print(f"     User-Agent: VibeCoding-Book/1.0")


def demonstrate_url_encoding():
    """한글 등 특수문자의 URL 인코딩을 보여줍니다."""
    print("\n4. URL 인코딩 예시:")

    params_korean = {
        "검색어": "바이브 코딩",
        "카테고리": "프로그래밍",
    }

    encoded = urllib.parse.urlencode(params_korean)
    print(f"   원본: {params_korean}")
    print(f"   인코딩 결과: {encoded}")

    # 디코딩
    decoded = urllib.parse.unquote(encoded)
    print(f"   디코딩 결과: {decoded}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-3: 헤더와 파라미터")
    print("=" * 50)
    request_with_headers_and_params()
    demonstrate_url_encoding()
