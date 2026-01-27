"""
예제 17-7: API 키 인증
API 키를 사용한 인증 패턴을 보여줍니다.
실제 API 키 대신 시뮬레이션을 사용합니다.
"""

import urllib.request
import urllib.parse
import json
import os


def api_key_in_header():
    """헤더에 API 키를 포함하는 인증 방식입니다."""
    print("1. 헤더 방식 API 키 인증:")

    # 환경변수에서 API 키 읽기 (보안 모범 사례)
    api_key = os.environ.get("MY_API_KEY", "demo-key-12345")

    url = "https://httpbin.org/headers"

    req = urllib.request.Request(url)
    # API 키를 헤더에 추가 (일반적인 패턴들)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("X-API-Key", api_key)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            headers = result.get("headers", {})
            print(f"   Authorization: {headers.get('Authorization', 'N/A')}")
            print(f"   X-Api-Key: {headers.get('X-Api-Key', 'N/A')}")

    except Exception as e:
        print(f"   네트워크 실패 ({e}), 시뮬레이션:")
        print(f"   Authorization: Bearer {api_key}")
        print(f"   X-API-Key: {api_key}")


def api_key_in_query_param():
    """쿼리 파라미터에 API 키를 포함하는 인증 방식입니다."""
    print(f"\n2. 쿼리 파라미터 방식 API 키 인증:")

    api_key = os.environ.get("WEATHER_API_KEY", "demo-weather-key")

    base_url = "https://httpbin.org/get"
    params = {
        "apikey": api_key,
        "city": "Seoul",
        "units": "metric",
    }

    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"

    print(f"   요청 URL: {base_url}?apikey=***&city=Seoul&units=metric")
    print(f"   (실제 키는 로그에 숨김 처리)")

    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            args = result.get("args", {})
            # API 키는 마스킹 처리
            masked_key = args.get("apikey", "N/A")
            print(f"   서버가 받은 apikey: {masked_key[:4]}***")
            print(f"   서버가 받은 city: {args.get('city', 'N/A')}")

    except Exception as e:
        print(f"   네트워크 실패 ({e}), 시뮬레이션:")
        print(f"   서버가 받은 apikey: demo***")
        print(f"   서버가 받은 city: Seoul")


def secure_api_key_management():
    """API 키를 안전하게 관리하는 방법을 보여줍니다."""
    print(f"\n3. API 키 안전 관리 모범 사례:")
    print(f"   [방법 1] 환경변수 사용:")
    print(f"   $ export MY_API_KEY='your-actual-key-here'")
    print(f"   api_key = os.environ.get('MY_API_KEY')")

    print(f"\n   [방법 2] .env 파일 사용:")
    print(f"   # .env 파일 (반드시 .gitignore에 추가!)")
    print(f"   MY_API_KEY=your-actual-key-here")

    print(f"\n   [주의사항]")
    print(f"   - API 키를 소스 코드에 직접 작성하지 마세요")
    print(f"   - .env 파일은 반드시 .gitignore에 추가하세요")
    print(f"   - 키가 노출되면 즉시 재발급하세요")
    print(f"   - 프로덕션에서는 환경변수 또는 비밀 관리 시스템을 사용하세요")


def simulate_authenticated_api():
    """인증이 필요한 API 호출 패턴을 시뮬레이션합니다."""
    print(f"\n4. 인증 API 호출 시뮬레이션:")

    # 실제 API 호출 패턴 (시뮬레이션)
    api_key = os.environ.get("MY_API_KEY", "demo-key-12345")

    # 인증된 요청 시뮬레이션
    if api_key == "demo-key-12345":
        print(f"   [시뮬레이션] 데모 키 사용 중")
        simulated_response = {
            "status": "success",
            "user": {
                "name": "바이브 코더",
                "plan": "free",
                "api_calls_remaining": 95,
            },
        }
        print(f"   응답 상태: {simulated_response['status']}")
        user = simulated_response["user"]
        print(f"   사용자: {user['name']}")
        print(f"   플랜: {user['plan']}")
        print(f"   남은 호출 횟수: {user['api_calls_remaining']}")
    else:
        print(f"   실제 API 키가 설정되어 있습니다. 실제 API 호출을 진행합니다.")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-7: API 키 인증")
    print("=" * 50)
    api_key_in_header()
    api_key_in_query_param()
    secure_api_key_management()
    simulate_authenticated_api()
