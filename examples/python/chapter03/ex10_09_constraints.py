"""
예제 10-9: 제약조건 명시하기
==============================
"외부 라이브러리 없이", "100줄 이내로", "Python 3.10 이상" 등
제약조건을 명시하면 AI가 조건에 맞는 코드를 생성합니다.

프롬프트:
  "외부 라이브러리 없이 표준 라이브러리만 사용해서
   간단한 HTTP 서버의 상태를 확인하는 헬스체크 함수를 작성해줘.
   제약조건:
   - 표준 라이브러리만 사용 (requests 등 외부 패키지 금지)
   - 타임아웃 3초
   - 결과는 딕셔너리로 반환
   - 상태코드, 응답시간, 서버 상태를 포함"
"""

# 표준 라이브러리만 사용!
import urllib.request
import urllib.error
import time
import ssl


def health_check(url, timeout=3):
    """
    HTTP 서버 헬스체크 — 표준 라이브러리만 사용.

    제약조건:
    - 외부 라이브러리 없음 (urllib만 사용)
    - 타임아웃 3초
    - 딕셔너리 반환

    Args:
        url: 확인할 URL
        timeout: 타임아웃(초), 기본값 3
    Returns:
        dict: 상태코드, 응답시간, 서버 상태 정보
    """
    result = {
        "url": url,
        "status_code": None,
        "response_time_ms": None,
        "status": "unknown",
        "message": "",
    }

    # SSL 인증서 검증 비활성화 (데모용)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    start = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "HealthCheck/1.0")

        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            elapsed = (time.time() - start) * 1000
            result["status_code"] = resp.status
            result["response_time_ms"] = round(elapsed, 2)

            if resp.status == 200:
                result["status"] = "healthy"
                result["message"] = "서버가 정상적으로 응답하고 있습니다."
            else:
                result["status"] = "degraded"
                result["message"] = f"서버가 응답했지만 상태 코드가 {resp.status}입니다."

    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        result["status_code"] = e.code
        result["response_time_ms"] = round(elapsed, 2)
        result["status"] = "error"
        result["message"] = f"HTTP 오류: {e.code} {e.reason}"

    except urllib.error.URLError as e:
        elapsed = (time.time() - start) * 1000
        result["response_time_ms"] = round(elapsed, 2)
        result["status"] = "unreachable"
        result["message"] = f"서버에 연결할 수 없습니다: {e.reason}"

    except Exception as e:
        elapsed = (time.time() - start) * 1000
        result["response_time_ms"] = round(elapsed, 2)
        result["status"] = "error"
        result["message"] = f"예기치 않은 오류: {str(e)}"

    return result


def print_health_report(result):
    """헬스체크 결과를 보기 좋게 출력합니다."""
    status_icons = {
        "healthy": "[OK]",
        "degraded": "[WARN]",
        "error": "[ERR]",
        "unreachable": "[DOWN]",
        "unknown": "[???]",
    }
    icon = status_icons.get(result["status"], "[???]")
    print(f"  {icon} {result['url']}")
    print(f"      상태     : {result['status']}")
    if result["status_code"]:
        print(f"      상태코드 : {result['status_code']}")
    if result["response_time_ms"]:
        print(f"      응답시간 : {result['response_time_ms']}ms")
    print(f"      메시지   : {result['message']}")


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 60)
    print("제약조건: 외부 라이브러리 없이 헬스체크")
    print("(표준 라이브러리 urllib만 사용)")
    print("=" * 60)
    print()

    # 테스트할 URL 목록
    urls = [
        "https://httpbin.org/status/200",     # 정상
        "https://httpbin.org/status/500",     # 서버 오류
        "https://invalid.nowhere.test",       # 접근 불가
    ]

    for url in urls:
        result = health_check(url, timeout=3)
        print_health_report(result)
        print()

    # 제약조건 확인 출력
    print("-" * 60)
    print("[제약조건 충족 확인]")
    print("  - 외부 라이브러리 사용: 없음 (urllib, time, ssl만 사용)")
    print("  - 타임아웃 설정: 3초")
    print("  - 반환 형식: 딕셔너리")
    print("  - 포함 정보: 상태코드, 응답시간, 서버 상태, 메시지")
