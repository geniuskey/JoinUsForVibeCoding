"""
예제 17-12: API 클라이언트 클래스
객체지향 프로그래밍으로 재사용 가능한 API 클라이언트를 만드는 방법을 배웁니다.
"""

import urllib.request
import urllib.error
import urllib.parse
import json
import time
import random


class APIClient:
    """범용 REST API 클라이언트 클래스."""

    def __init__(self, base_url, headers=None, timeout=10, max_retries=3):
        """
        API 클라이언트를 초기화합니다.

        Args:
            base_url: API의 기본 URL (예: "https://api.example.com")
            headers: 모든 요청에 포함할 기본 헤더
            timeout: 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = {
            "Accept": "application/json",
            "User-Agent": "VibeCoding-APIClient/1.0",
        }
        if headers:
            self.default_headers.update(headers)

        # 요청 통계
        self._stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "retries": 0,
        }

    def _build_url(self, endpoint, params=None):
        """전체 URL을 구성합니다."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        return url

    def _make_request(self, method, endpoint, data=None, params=None, headers=None):
        """HTTP 요청을 생성하고 전송합니다."""
        url = self._build_url(endpoint, params)

        # 헤더 병합
        req_headers = dict(self.default_headers)
        if headers:
            req_headers.update(headers)

        # 요청 본문 처리
        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            req_headers["Content-Type"] = "application/json"

        # 재시도 로직 포함
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            self._stats["total_requests"] += 1

            try:
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers=req_headers,
                    method=method,
                )

                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    response_body = response.read().decode("utf-8")
                    self._stats["successful"] += 1

                    result = {
                        "status": response.status,
                        "headers": dict(response.headers),
                        "data": json.loads(response_body) if response_body else None,
                    }
                    return result

            except urllib.error.HTTPError as e:
                last_error = e
                # 4xx 에러는 재시도하지 않음 (429 제외)
                if 400 <= e.code < 500 and e.code != 429:
                    self._stats["failed"] += 1
                    return {
                        "status": e.code,
                        "headers": dict(e.headers) if e.headers else {},
                        "data": None,
                        "error": f"HTTP {e.code}: {e.reason}",
                    }

            except Exception as e:
                last_error = e

            # 재시도 대기
            if attempt < self.max_retries:
                self._stats["retries"] += 1
                delay = (2 ** attempt) * 0.5 + random.uniform(0, 0.5)
                time.sleep(delay)

        self._stats["failed"] += 1
        return {
            "status": None,
            "headers": {},
            "data": None,
            "error": f"모든 재시도 실패: {last_error}",
        }

    def get(self, endpoint, params=None, headers=None):
        """GET 요청을 보냅니다."""
        return self._make_request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, data=None, params=None, headers=None):
        """POST 요청을 보냅니다."""
        return self._make_request("POST", endpoint, data=data, params=params, headers=headers)

    def put(self, endpoint, data=None, params=None, headers=None):
        """PUT 요청을 보냅니다."""
        return self._make_request("PUT", endpoint, data=data, params=params, headers=headers)

    def delete(self, endpoint, params=None, headers=None):
        """DELETE 요청을 보냅니다."""
        return self._make_request("DELETE", endpoint, params=params, headers=headers)

    def get_stats(self):
        """요청 통계를 반환합니다."""
        return dict(self._stats)


class GitHubClient(APIClient):
    """GitHub API 전용 클라이언트."""

    def __init__(self, token=None):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"

        super().__init__(
            base_url="https://api.github.com",
            headers=headers,
            timeout=10,
            max_retries=3,
        )

    def get_repo(self, owner, repo):
        """리포지토리 정보를 조회합니다."""
        result = self.get(f"/repos/{owner}/{repo}")
        if result.get("data"):
            data = result["data"]
            return {
                "name": data.get("full_name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "language": data.get("language"),
            }
        return None

    def search_repos(self, query, limit=5):
        """리포지토리를 검색합니다."""
        result = self.get("/search/repositories", params={
            "q": query,
            "sort": "stars",
            "per_page": str(limit),
        })
        if result.get("data"):
            return [
                {
                    "name": r["full_name"],
                    "stars": r["stargazers_count"],
                    "description": (r.get("description") or "")[:60],
                }
                for r in result["data"].get("items", [])
            ]
        return []


class JSONPlaceholderClient(APIClient):
    """JSONPlaceholder API 전용 클라이언트."""

    def __init__(self):
        super().__init__(
            base_url="https://jsonplaceholder.typicode.com",
            timeout=10,
            max_retries=2,
        )

    def get_posts(self, user_id=None):
        """게시글 목록을 조회합니다."""
        params = {"userId": str(user_id)} if user_id else None
        result = self.get("/posts", params=params)
        return result.get("data", [])

    def create_post(self, title, body, user_id=1):
        """새 게시글을 생성합니다."""
        result = self.post("/posts", data={
            "title": title,
            "body": body,
            "userId": user_id,
        })
        return result

    def get_user(self, user_id):
        """사용자 정보를 조회합니다."""
        result = self.get(f"/users/{user_id}")
        return result.get("data")


def demonstrate_api_client():
    """API 클라이언트 클래스 사용을 시연합니다."""

    # 1. 기본 APIClient 사용
    print("1. 기본 APIClient 사용:")
    client = APIClient("https://httpbin.org")

    result = client.get("/get", params={"test": "hello"})
    if result.get("data"):
        print(f"   GET 성공! 파라미터: {result['data'].get('args', {})}")
    else:
        print(f"   GET 실패: {result.get('error', '알 수 없는 에러')}")

    result = client.post("/post", data={"message": "안녕하세요!"})
    if result.get("data"):
        print(f"   POST 성공! 상태: {result['status']}")
    else:
        print(f"   POST 실패: {result.get('error', '알 수 없는 에러')}")

    # 2. JSONPlaceholder 클라이언트
    print(f"\n2. JSONPlaceholder 클라이언트:")
    jp_client = JSONPlaceholderClient()

    posts = jp_client.get_posts(user_id=1)
    if posts:
        print(f"   게시글 {len(posts)}개 조회됨")
        for post in posts[:3]:
            print(f"   - {post['title'][:40]}...")
    else:
        print(f"   게시글 조회 실패 (시뮬레이션 데이터 없음)")

    # 새 게시글 생성
    result = jp_client.create_post(
        title="바이브 코딩으로 만든 첫 게시글",
        body="AI와 함께 API 클라이언트를 만들었습니다!",
    )
    if result.get("data"):
        print(f"   새 게시글 생성! ID: {result['data'].get('id', 'N/A')}")

    # 3. GitHub 클라이언트
    print(f"\n3. GitHub 클라이언트:")
    gh_client = GitHubClient()

    repo = gh_client.get_repo("python", "cpython")
    if repo:
        print(f"   리포지토리: {repo['name']}")
        print(f"   설명: {repo['description']}")
        print(f"   별: {repo['stars']:,}개")
        print(f"   언어: {repo['language']}")
    else:
        print(f"   리포지토리 조회 실패")
        print(f"   (시뮬레이션) python/cpython - The Python programming language")

    # 4. 요청 통계
    print(f"\n4. 요청 통계:")
    for name, c in [("httpbin", client), ("JSONPlaceholder", jp_client), ("GitHub", gh_client)]:
        stats = c.get_stats()
        print(f"   [{name}] 총: {stats['total_requests']}, "
              f"성공: {stats['successful']}, "
              f"실패: {stats['failed']}, "
              f"재시도: {stats['retries']}")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-12: API 클라이언트 클래스")
    print("=" * 50)
    demonstrate_api_client()
