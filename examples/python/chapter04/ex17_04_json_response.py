"""
예제 17-4: JSON 응답 처리
API에서 받은 JSON 응답을 파싱하고 활용하는 방법을 배웁니다.
"""

import urllib.request
import json


def fetch_and_parse_json():
    """JSON 응답을 받아 다양한 방법으로 처리합니다."""

    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw_data = response.read().decode("utf-8")
            post = json.loads(raw_data)

    except Exception as e:
        print(f"네트워크 요청 실패: {e}")
        print("--- 시뮬레이션 모드로 전환 ---\n")

        # 시뮬레이션 데이터
        post = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        }

    # 1. 기본 데이터 접근
    print("1. 기본 데이터 접근:")
    print(f"   게시글 ID: {post['id']}")
    print(f"   작성자 ID: {post['userId']}")
    print(f"   제목: {post['title']}")
    print(f"   본문: {post['body'][:50]}...")

    # 2. get()으로 안전하게 접근 (키가 없을 때 기본값)
    print(f"\n2. 안전한 데이터 접근 (get 메서드):")
    print(f"   제목: {post.get('title', '제목 없음')}")
    print(f"   댓글 수: {post.get('comments_count', '정보 없음')}")
    print(f"   카테고리: {post.get('category', '미분류')}")

    # 3. JSON 문자열로 변환 (보기 좋게 출력)
    print(f"\n3. 보기 좋게 JSON 출력 (pretty print):")
    pretty = json.dumps(post, indent=2, ensure_ascii=False)
    print(pretty)


def process_json_list():
    """JSON 배열(리스트) 응답을 처리합니다."""

    url = "https://jsonplaceholder.typicode.com/posts?userId=1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            posts = json.loads(response.read().decode("utf-8"))

    except Exception as e:
        print(f"\n네트워크 요청 실패: {e}")
        print("--- 시뮬레이션 모드로 전환 ---\n")

        # 시뮬레이션 데이터
        posts = [
            {"userId": 1, "id": 1, "title": "첫 번째 글", "body": "내용 1"},
            {"userId": 1, "id": 2, "title": "두 번째 글", "body": "내용 2"},
            {"userId": 1, "id": 3, "title": "세 번째 글", "body": "내용 3"},
            {"userId": 1, "id": 4, "title": "네 번째 글", "body": "내용 4"},
            {"userId": 1, "id": 5, "title": "다섯 번째 글", "body": "내용 5"},
        ]

    print(f"\n4. JSON 배열 처리:")
    print(f"   총 게시글 수: {len(posts)}")

    print(f"\n   처음 5개 게시글 제목:")
    for i, post in enumerate(posts[:5], 1):
        title = post["title"][:40]
        print(f"   {i}. [ID: {post['id']}] {title}")

    # 5. 리스트 컴프리헨션으로 특정 필드만 추출
    titles = [p["title"] for p in posts[:3]]
    print(f"\n5. 제목만 추출 (리스트 컴프리헨션):")
    for title in titles:
        print(f"   - {title[:50]}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-4: JSON 응답 처리")
    print("=" * 50)
    fetch_and_parse_json()
    process_json_list()
