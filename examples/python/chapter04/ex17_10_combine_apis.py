"""
예제 17-10: 여러 API 조합
여러 API의 데이터를 조합하여 유용한 정보를 만드는 방법을 배웁니다.
네트워크 의존을 줄이기 위해 시뮬레이션 기반으로 동작합니다.
"""

import urllib.request
import json
import time


# --- 시뮬레이션 데이터 ---
SIMULATED_USER = {
    "id": 1,
    "name": "김바이브",
    "email": "vibe@example.com",
    "address": {
        "city": "Seoul",
        "geo": {"lat": "37.5665", "lng": "126.9780"},
    },
}

SIMULATED_POSTS = [
    {"userId": 1, "id": 1, "title": "바이브 코딩 시작하기", "body": "AI와 함께 코딩하는 새로운 방법"},
    {"userId": 1, "id": 2, "title": "Python으로 API 다루기", "body": "urllib로 HTTP 요청 보내기"},
    {"userId": 1, "id": 3, "title": "프롬프트 엔지니어링 팁", "body": "AI에게 효과적으로 요청하기"},
]

SIMULATED_COMMENTS = {
    1: [
        {"postId": 1, "name": "좋은 글이네요!", "email": "reader1@example.com"},
        {"postId": 1, "name": "도움이 많이 되었습니다", "email": "reader2@example.com"},
    ],
    2: [
        {"postId": 2, "name": "urllib 예제 감사합니다", "email": "reader3@example.com"},
    ],
    3: [],
}

SIMULATED_WEATHER = {
    "Seoul": {"temp": 15.2, "description": "맑음", "humidity": 55},
}


def fetch_json(url, timeout_sec=10):
    """URL에서 JSON 데이터를 가져옵니다."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "VibeCoding-Book/1.0")
        req.add_header("Accept", "application/json")

        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def get_user_profile(user_id):
    """사용자 프로필 정보를 가져옵니다."""
    data = fetch_json(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    return data if data else SIMULATED_USER


def get_user_posts(user_id):
    """사용자의 게시글 목록을 가져옵니다."""
    data = fetch_json(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    return data if data else SIMULATED_POSTS


def get_post_comments(post_id):
    """게시글의 댓글을 가져옵니다."""
    data = fetch_json(f"https://jsonplaceholder.typicode.com/comments?postId={post_id}")
    return data if data else SIMULATED_COMMENTS.get(post_id, [])


def get_weather(city):
    """도시의 날씨 정보를 가져옵니다 (시뮬레이션)."""
    # 실제로는 날씨 API를 호출하지만, 여기서는 시뮬레이션
    return SIMULATED_WEATHER.get(city, {"temp": 20.0, "description": "정보 없음", "humidity": 50})


def build_user_dashboard(user_id):
    """여러 API를 조합하여 사용자 대시보드를 구성합니다."""
    print("사용자 대시보드 구성 중...\n")
    start_time = time.time()

    # 1단계: 사용자 정보 가져오기
    print("[1/4] 사용자 정보 조회...")
    user = get_user_profile(user_id)
    user_name = user.get("name", "알 수 없음")
    user_city = user.get("address", {}).get("city", "Seoul")

    # 2단계: 사용자 게시글 가져오기
    print("[2/4] 게시글 목록 조회...")
    posts = get_user_posts(user_id)

    # 3단계: 각 게시글의 댓글 수 가져오기
    print("[3/4] 댓글 정보 조회...")
    post_details = []
    for post in posts[:3]:  # 처음 3개만
        comments = get_post_comments(post["id"])
        post_details.append({
            "title": post["title"],
            "comment_count": len(comments),
        })

    # 4단계: 사용자 위치의 날씨 정보
    print("[4/4] 날씨 정보 조회...")
    weather = get_weather(user_city)

    elapsed = time.time() - start_time

    # --- 대시보드 출력 ---
    print(f"\n{'=' * 50}")
    print(f"  사용자 대시보드 - {user_name}")
    print(f"{'=' * 50}")

    # 프로필 섹션
    print(f"\n  [프로필]")
    print(f"  이름: {user_name}")
    print(f"  이메일: {user.get('email', 'N/A')}")
    print(f"  도시: {user_city}")

    # 날씨 섹션
    print(f"\n  [현재 날씨 - {user_city}]")
    print(f"  기온: {weather['temp']}°C")
    print(f"  날씨: {weather['description']}")
    print(f"  습도: {weather['humidity']}%")

    # 게시글 섹션
    print(f"\n  [최근 게시글] (총 {len(posts)}개)")
    for i, detail in enumerate(post_details, 1):
        title = detail["title"][:35]
        print(f"  {i}. {title}... (댓글 {detail['comment_count']}개)")

    # 통계
    total_comments = sum(d["comment_count"] for d in post_details)
    print(f"\n  [통계]")
    print(f"  총 게시글: {len(posts)}개")
    print(f"  표시된 게시글 댓글 합계: {total_comments}개")
    print(f"  데이터 로딩 시간: {elapsed:.2f}초")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-10: 여러 API 조합")
    print("=" * 50)
    build_user_dashboard(1)
