"""
예제 17-2: POST 요청 기초
urllib.request를 사용하여 POST 요청으로 데이터를 전송하는 방법을 배웁니다.
"""

import urllib.request
import json


def post_request_basic():
    """httpbin.org에 POST 요청으로 JSON 데이터를 전송합니다."""
    url = "https://httpbin.org/post"

    # 전송할 데이터
    payload = {
        "name": "바이브 코더",
        "skill": "AI 프로그래밍",
        "level": "입문자",
    }

    # JSON 문자열로 변환 후 바이트로 인코딩
    data = json.dumps(payload).encode("utf-8")

    try:
        # POST 요청 생성
        req = urllib.request.Request(
            url,
            data=data,
            method="POST",
        )
        req.add_header("Content-Type", "application/json")

        # 요청 전송 및 응답 받기
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.status
            result = json.loads(response.read().decode("utf-8"))

            print(f"상태 코드: {status_code}")
            print(f"\n전송한 데이터:")
            sent_data = json.loads(result.get("data", "{}"))
            for key, value in sent_data.items():
                print(f"  {key}: {value}")

            print(f"\n서버가 확인한 Content-Type: {result.get('headers', {}).get('Content-Type', 'N/A')}")

    except Exception as e:
        print(f"네트워크 요청 실패: {e}")
        print("\n--- 시뮬레이션 모드로 전환 ---\n")

        # 시뮬레이션 응답
        print(f"상태 코드: 200")
        print(f"\n전송한 데이터:")
        for key, value in payload.items():
            print(f"  {key}: {value}")
        print(f"\n서버가 확인한 Content-Type: application/json")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-2: POST 요청 기초")
    print("=" * 50)
    post_request_basic()
