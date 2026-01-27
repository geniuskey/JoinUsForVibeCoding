"""
예제 18-01: HTML 가져오기
urllib.request를 사용하여 웹 페이지를 가져오는 방법을 배웁니다.
네트워크 오류에 대비하여 내장 HTML 문자열로 대체하는 패턴도 함께 익힙니다.
"""

import urllib.request
import urllib.error

# 내장 HTML (네트워크 접속이 안 될 경우 사용)
SAMPLE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>바이브 코딩 블로그</title>
</head>
<body>
    <h1>바이브 코딩에 오신 것을 환영합니다!</h1>
    <p>AI와 함께하는 새로운 프로그래밍 패러다임을 소개합니다.</p>
    <p>자연어로 코드를 작성하는 시대가 열렸습니다.</p>
</body>
</html>"""


def fetch_html(url):
    """URL에서 HTML을 가져옵니다. 실패 시 내장 HTML을 반환합니다."""
    try:
        # urllib.request로 웹 페이지 요청
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (학습용 스크래퍼)"}
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            # 응답 정보 출력
            print(f"상태 코드: {response.status}")
            print(f"콘텐츠 타입: {response.headers['Content-Type']}")
            html = response.read().decode("utf-8")
            print(f"가져온 HTML 크기: {len(html)} 바이트")
            return html
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"네트워크 오류 발생: {e}")
        print("내장 HTML 문자열을 대신 사용합니다.\n")
        return SAMPLE_HTML


# 실행
print("=" * 50)
print("예제 18-01: HTML 가져오기")
print("=" * 50)

# 실제 URL 요청 시도 (실패 시 내장 HTML 사용)
html = fetch_html("https://example.com")

print("\n--- 가져온 HTML 내용 (처음 300자) ---")
print(html[:300])
print("...")

print("\n--- HTML 기본 정보 ---")
print(f"전체 길이: {len(html)} 글자")
print(f"줄 수: {len(html.splitlines())} 줄")
print(f"'<' 태그 시작 개수: {html.count('<')}")
