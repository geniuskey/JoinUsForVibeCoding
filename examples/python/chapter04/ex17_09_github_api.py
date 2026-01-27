"""
예제 17-9: GitHub API 활용
GitHub 공개 API를 사용하여 리포지토리 정보를 조회합니다.
인증 없이 공개 데이터에 접근합니다.
"""

import urllib.request
import json


def fetch_repo_info(owner, repo):
    """GitHub 리포지토리 정보를 조회합니다."""
    url = f"https://api.github.com/repos/{owner}/{repo}"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "VibeCoding-Book-Example")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data

    except Exception as e:
        print(f"   API 호출 실패: {e}")
        return None


def display_repo_info():
    """리포지토리 정보를 보기 좋게 출력합니다."""
    print("1. GitHub 리포지토리 정보 조회:")

    # Python 공식 리포지토리 조회
    data = fetch_repo_info("python", "cpython")

    if data:
        print(f"   이름: {data.get('full_name', 'N/A')}")
        print(f"   설명: {data.get('description', 'N/A')}")
        print(f"   언어: {data.get('language', 'N/A')}")
        print(f"   별(Stars): {data.get('stargazers_count', 0):,}개")
        print(f"   포크(Forks): {data.get('forks_count', 0):,}개")
        print(f"   열린 이슈: {data.get('open_issues_count', 0):,}개")
        print(f"   라이선스: {data.get('license', {}).get('name', 'N/A') if data.get('license') else 'N/A'}")
    else:
        print(f"   --- 시뮬레이션 데이터 ---")
        print(f"   이름: python/cpython")
        print(f"   설명: The Python programming language")
        print(f"   언어: Python")
        print(f"   별(Stars): 63,000개")
        print(f"   포크(Forks): 30,000개")
        print(f"   열린 이슈: 7,500개")
        print(f"   라이선스: Python Software Foundation License")


def search_repos(query, sort="stars", limit=5):
    """GitHub에서 리포지토리를 검색합니다."""
    print(f"\n2. GitHub 리포지토리 검색 ('{query}'):")

    import urllib.parse
    params = urllib.parse.urlencode({
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": str(limit),
    })
    url = f"https://api.github.com/search/repositories?{params}"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "VibeCoding-Book-Example")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            items = result.get("items", [])
            total = result.get("total_count", 0)

            print(f"   총 검색 결과: {total:,}개 (상위 {limit}개 표시)")
            print()

            for i, repo in enumerate(items, 1):
                print(f"   {i}. {repo['full_name']}")
                print(f"      설명: {(repo.get('description') or 'N/A')[:60]}")
                print(f"      별: {repo['stargazers_count']:,} | 언어: {repo.get('language', 'N/A')}")

    except Exception as e:
        print(f"   API 호출 실패: {e}")
        print(f"   --- 시뮬레이션 데이터 ---")
        simulated = [
            ("tensorflow/tensorflow", "An Open Source Machine Learning Framework", 185000, "C++"),
            ("pytorch/pytorch", "Tensors and Dynamic neural networks", 82000, "Python"),
            ("keras-team/keras", "Deep Learning for humans", 61000, "Python"),
        ]
        print(f"   총 검색 결과: 약 50,000개 (상위 3개 표시)")
        for i, (name, desc, stars, lang) in enumerate(simulated, 1):
            print(f"   {i}. {name}")
            print(f"      설명: {desc}")
            print(f"      별: {stars:,} | 언어: {lang}")


def fetch_user_info(username):
    """GitHub 사용자 정보를 조회합니다."""
    print(f"\n3. GitHub 사용자 정보 조회 ('{username}'):")

    url = f"https://api.github.com/users/{username}"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "VibeCoding-Book-Example")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

            print(f"   이름: {data.get('name', 'N/A')}")
            print(f"   로그인: {data.get('login', 'N/A')}")
            print(f"   소개: {data.get('bio', 'N/A')}")
            print(f"   공개 리포지토리: {data.get('public_repos', 0)}개")
            print(f"   팔로워: {data.get('followers', 0):,}명")
            print(f"   팔로잉: {data.get('following', 0):,}명")

            # Rate Limit 확인
            remaining = response.headers.get("X-RateLimit-Remaining", "N/A")
            limit = response.headers.get("X-RateLimit-Limit", "N/A")
            print(f"\n   [Rate Limit] 남은 요청: {remaining}/{limit}")

    except Exception as e:
        print(f"   API 호출 실패: {e}")
        print(f"   --- 시뮬레이션 데이터 ---")
        print(f"   이름: Guido van Rossum")
        print(f"   로그인: gvanrossum")
        print(f"   소개: Python creator")
        print(f"   공개 리포지토리: 12개")
        print(f"   팔로워: 45,000명")
        print(f"   팔로잉: 0명")


if __name__ == "__main__":
    print("=" * 50)
    print("예제 17-9: GitHub API 활용")
    print("=" * 50)
    display_repo_info()
    search_repos("machine learning")
    fetch_user_info("gvanrossum")
