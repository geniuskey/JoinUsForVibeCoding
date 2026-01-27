# Chapter 17: API 연동

현대 소프트웨어는 혼자 동작하지 않습니다. 날씨 정보를 가져오고, 소셜 미디어에 글을 게시하고, 결제를 처리하는 모든 과정에서 프로그램은 다른 서비스와 **대화**합니다. 이 대화의 규칙이 바로 API(Application Programming Interface)입니다. 이번 챕터에서는 Python의 표준 라이브러리인 `urllib.request`를 사용하여 웹 API와 통신하는 방법을 단계별로 배웁니다. 외부 패키지 설치 없이, Python만으로 API의 세계에 입문합니다.

---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- REST API의 기본 개념과 동작 원리를 이해한다
- HTTP 메서드(GET, POST, PUT, DELETE)의 역할과 차이를 구분한다
- `urllib.request`를 사용하여 API에 요청을 보내고 응답을 받는다
- JSON 형식의 응답 데이터를 파싱하고 활용한다
- API 호출 시 발생하는 다양한 에러를 안전하게 처리한다
- Rate Limiting에 대응하는 재시도 전략을 구현한다

---

## 17.1 REST API 기초 개념

### API란 무엇인가?

API는 **프로그램과 프로그램 사이의 약속된 대화 방식**입니다. 식당에 비유하면, 메뉴판이 API이고, 주문서가 요청(Request), 나오는 음식이 응답(Response)입니다. 손님(클라이언트)은 주방(서버) 내부의 조리 과정을 알 필요 없이, 메뉴판에 적힌 규칙대로 주문하면 됩니다.

### REST API의 핵심 원칙

REST(Representational State Transfer)는 웹 API를 설계하는 가장 널리 사용되는 방식입니다. 핵심 원칙은 다음과 같습니다:

| 원칙 | 설명 | 예시 |
|------|------|------|
| **URL로 자원 식별** | 모든 데이터(자원)는 고유한 URL을 가짐 | `/users/1` = 1번 사용자 |
| **HTTP 메서드로 동작 표현** | GET(조회), POST(생성), PUT(수정), DELETE(삭제) | `GET /users` = 사용자 목록 조회 |
| **상태 없음(Stateless)** | 각 요청은 독립적으로 처리됨 | 이전 요청을 기억하지 않음 |
| **JSON으로 데이터 교환** | 구조화된 데이터를 JSON 형식으로 주고받음 | `{"name": "바이브"}` |

### API 통신의 기본 흐름

```
클라이언트 (Python)                    서버 (API)
     |                                    |
     |  1. HTTP 요청 전송 (URL + 메서드)    |
     | ---------------------------------> |
     |                                    |
     |  2. 서버가 요청 처리                 |
     |                                    |
     |  3. HTTP 응답 반환 (상태 코드 + 데이터)|
     | <--------------------------------- |
     |                                    |
```

**상태 코드**는 요청의 결과를 숫자로 알려줍니다:

| 상태 코드 | 의미 | 설명 |
|-----------|------|------|
| 200 | OK | 요청 성공 |
| 201 | Created | 새 자원 생성 성공 |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 접근 권한 없음 |
| 404 | Not Found | 자원을 찾을 수 없음 |
| 429 | Too Many Requests | 요청 횟수 초과 (Rate Limit) |
| 500 | Internal Server Error | 서버 내부 오류 |

> **Note:** REST API에서 URL은 "무엇을", HTTP 메서드는 "어떻게 할 것인지"를 나타냅니다. 같은 URL `/posts/1`이라도 `GET`이면 조회, `PUT`이면 수정, `DELETE`이면 삭제입니다.

---

## 17.2 HTTP 메서드와 urllib.request

Python 표준 라이브러리의 `urllib.request`는 외부 패키지 없이 HTTP 통신을 수행할 수 있는 모듈입니다. 가장 기본이 되는 GET과 POST 요청부터 살펴보겠습니다.

### GET 요청: 데이터 조회하기

GET은 서버에서 데이터를 **가져오는** 메서드입니다. 웹 브라우저에서 URL을 입력하고 Enter를 누르는 것과 같습니다.

**예제 17-1: GET 요청 기초**

`urllib.request.urlopen()`으로 가장 간단한 GET 요청을 보냅니다. httpbin.org는 HTTP 요청을 테스트할 수 있는 무료 서비스입니다.

```python
# examples/python/chapter04/ex17_01_get_request.py
import urllib.request
import json

def get_request_basic():
    """httpbin.org에 GET 요청을 보내고 응답을 받습니다."""
    url = "https://httpbin.org/get"

    try:
        # GET 요청 보내기
        with urllib.request.urlopen(url, timeout=10) as response:
            # 응답 상태 코드 확인
            status_code = response.status
            print(f"상태 코드: {status_code}")

            # 응답 헤더 확인
            content_type = response.headers.get("Content-Type")
            print(f"Content-Type: {content_type}")

            # 응답 본문 읽기
            data = response.read().decode("utf-8")
            result = json.loads(data)

            print(f"\n요청 URL: {result.get('url', 'N/A')}")
            print(f"요청 출처 IP: {result.get('origin', 'N/A')}")
            print(f"User-Agent: {result.get('headers', {}).get('User-Agent', 'N/A')}")

    except Exception as e:
        print(f"네트워크 요청 실패: {e}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_01_get_request.py
```

**결과:**

```
==================================================
예제 17-1: GET 요청 기초
==================================================
상태 코드: 200
Content-Type: application/json

요청 URL: https://httpbin.org/get
요청 출처 IP: 123.45.67.89
User-Agent: Python-urllib/3.11
```

핵심 패턴을 분석해 보겠습니다:

1. `urllib.request.urlopen(url)` -- URL에 GET 요청을 보냅니다
2. `response.status` -- HTTP 상태 코드를 확인합니다 (200이면 성공)
3. `response.read().decode("utf-8")` -- 응답 본문을 문자열로 읽습니다
4. `json.loads(data)` -- JSON 문자열을 Python 딕셔너리로 변환합니다

> **Tip:** `with` 문을 사용하면 응답을 다 읽은 뒤 자동으로 연결이 닫힙니다. 리소스 누수를 방지하는 좋은 습관입니다.

### POST 요청: 데이터 전송하기

POST는 서버에 새로운 데이터를 **전송하는** 메서드입니다. 회원가입, 게시글 작성, 주문 생성 등에 사용됩니다.

**예제 17-2: POST 요청 기초**

JSON 데이터를 서버에 전송하는 POST 요청을 만듭니다. GET과 달리 `Request` 객체를 생성하고 `data`와 `method`를 지정합니다.

```python
# examples/python/chapter04/ex17_02_post_request.py
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
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_02_post_request.py
```

**결과:**

```
==================================================
예제 17-2: POST 요청 기초
==================================================
상태 코드: 200

전송한 데이터:
  name: 바이브 코더
  skill: AI 프로그래밍
  level: 입문자

서버가 확인한 Content-Type: application/json
```

POST 요청의 핵심 과정은 다음과 같습니다:

1. 전송할 데이터를 Python 딕셔너리로 준비합니다
2. `json.dumps()`로 JSON 문자열로 변환합니다
3. `.encode("utf-8")`로 바이트 데이터로 인코딩합니다
4. `Request` 객체에 `data`와 `method="POST"`를 지정합니다
5. `Content-Type: application/json` 헤더를 추가합니다

> **Warning:** POST 요청에서 `Content-Type` 헤더를 빠뜨리면 서버가 전송된 데이터를 올바르게 해석하지 못할 수 있습니다. JSON 데이터를 보낼 때는 반드시 `application/json`을 지정하세요.

### 헤더와 쿼리 파라미터

실제 API를 사용할 때는 커스텀 헤더와 쿼리 파라미터를 함께 보내는 경우가 많습니다. 인증 토큰, 응답 형식 지정, 검색 조건 등이 이에 해당합니다.

**예제 17-3: 헤더와 파라미터**

`urllib.parse.urlencode()`로 쿼리 파라미터를 안전하게 구성하고, `Request` 객체에 커스텀 헤더를 추가합니다.

```python
# examples/python/chapter04/ex17_03_headers_params.py
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

    # 2. 커스텀 헤더 추가
    headers = {
        "Accept": "application/json",
        "Accept-Language": "ko-KR",
        "X-Custom-Header": "VibeCoding-Client",
        "User-Agent": "VibeCoding-Book/1.0",
    }

    req = urllib.request.Request(full_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(f"받은 파라미터: {json.dumps(result.get('args', {}), ensure_ascii=False)}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_03_headers_params.py
```

**결과:**

```
==================================================
예제 17-3: 헤더와 파라미터
==================================================
1. 쿼리 파라미터 구성
   기본 URL: https://httpbin.org/get
   쿼리 문자열: language=python&topic=vibe+coding&page=1
   전체 URL: https://httpbin.org/get?language=python&topic=vibe+coding&page=1

2. 커스텀 헤더:
   Accept: application/json
   Accept-Language: ko-KR
   X-Custom-Header: VibeCoding-Client
   User-Agent: VibeCoding-Book/1.0

3. 서버 응답:
   받은 파라미터: {"language": "python", "topic": "vibe coding", "page": "1"}
   받은 헤더 중 일부:
     Accept-Language: ko-KR
     X-Custom-Header: VibeCoding-Client
     User-Agent: VibeCoding-Book/1.0

4. URL 인코딩 예시:
   원본: {'검색어': '바이브 코딩', '카테고리': '프로그래밍'}
   인코딩 결과: %EA%B2%80%EC%83%89%EC%96%B4=%EB%B0%94...
   디코딩 결과: 검색어=바이브 코딩&카테고리=프로그래밍
```

> **Note:** `urllib.parse.urlencode()`는 한글, 공백 등 특수문자를 URL에서 안전하게 사용할 수 있도록 자동 인코딩합니다. 직접 URL을 조립하면 인코딩 문제가 발생할 수 있으니, 반드시 이 함수를 사용하세요.

### HTTP 메서드 비교 정리

`urllib.request.Request`의 `method` 파라미터로 모든 HTTP 메서드를 지정할 수 있습니다:

| 메서드 | 용도 | urllib 사용법 | 데이터 본문 |
|--------|------|---------------|-------------|
| **GET** | 조회 | `urlopen(url)` 또는 `Request(url, method="GET")` | 없음 |
| **POST** | 생성 | `Request(url, data=body, method="POST")` | 있음 |
| **PUT** | 수정 | `Request(url, data=body, method="PUT")` | 있음 |
| **DELETE** | 삭제 | `Request(url, method="DELETE")` | 보통 없음 |

```python
# PUT 요청 예시 (데이터 수정)
req = urllib.request.Request(
    "https://httpbin.org/put",
    data=json.dumps({"title": "수정된 제목"}).encode("utf-8"),
    method="PUT",
)
req.add_header("Content-Type", "application/json")

# DELETE 요청 예시 (데이터 삭제)
req = urllib.request.Request(
    "https://httpbin.org/delete",
    method="DELETE",
)
```

---

## 17.3 응답 처리: JSON 다루기

대부분의 REST API는 JSON(JavaScript Object Notation) 형식으로 데이터를 반환합니다. Python의 `json` 모듈을 사용하면 JSON을 딕셔너리와 리스트로 자유롭게 변환할 수 있습니다.

### JSON 응답 파싱과 활용

**예제 17-4: JSON 응답 처리**

JSONPlaceholder(무료 테스트 API)에서 게시글 데이터를 가져와 다양한 방법으로 처리합니다.

```python
# examples/python/chapter04/ex17_04_json_response.py
import urllib.request
import json

def fetch_and_parse_json():
    """JSON 응답을 받아 다양한 방법으로 처리합니다."""
    url = "https://jsonplaceholder.typicode.com/posts/1"

    with urllib.request.urlopen(url, timeout=10) as response:
        raw_data = response.read().decode("utf-8")
        post = json.loads(raw_data)

    # 1. 기본 데이터 접근
    print(f"게시글 ID: {post['id']}")
    print(f"작성자 ID: {post['userId']}")
    print(f"제목: {post['title']}")

    # 2. get()으로 안전하게 접근 (키가 없을 때 기본값)
    print(f"댓글 수: {post.get('comments_count', '정보 없음')}")

    # 3. JSON 문자열로 변환 (보기 좋게 출력)
    pretty = json.dumps(post, indent=2, ensure_ascii=False)
    print(pretty)
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_04_json_response.py
```

**결과:**

```
==================================================
예제 17-4: JSON 응답 처리
==================================================
1. 기본 데이터 접근:
   게시글 ID: 1
   작성자 ID: 1
   제목: sunt aut facere repellat provident occaecati...
   본문: quia et suscipit
suscipit recusandae consequun...

2. 안전한 데이터 접근 (get 메서드):
   제목: sunt aut facere repellat provident occaecati...
   댓글 수: 정보 없음
   카테고리: 미분류

3. 보기 좋게 JSON 출력 (pretty print):
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat...",
  "body": "quia et suscipit..."
}

4. JSON 배열 처리:
   총 게시글 수: 10
   처음 5개 게시글 제목:
   1. [ID: 1] sunt aut facere repellat provident
   2. [ID: 2] qui est esse
   3. [ID: 3] ea molestias quasi exercitationem rep
   4. [ID: 4] eum et est occaecati
   5. [ID: 5] nesciunt quas odio
```

JSON 처리에서 기억해야 할 세 가지 핵심 기법:

1. **`json.loads()`** -- JSON 문자열을 Python 객체(딕셔너리/리스트)로 변환
2. **`.get(key, default)`** -- 키가 없어도 에러 없이 기본값 반환
3. **`json.dumps(obj, indent=2)`** -- Python 객체를 보기 좋은 JSON 문자열로 변환

> **Tip:** API 응답의 구조를 처음 파악할 때는 `json.dumps(data, indent=2, ensure_ascii=False)`로 예쁘게 출력해 보세요. 중첩된 구조가 한눈에 들어옵니다. `ensure_ascii=False`를 추가하면 한글이 깨지지 않고 그대로 출력됩니다.

---

## 17.4 API 키 인증과 공공 API 활용

많은 API는 누가 요청을 보내는지 확인하기 위해 **API 키 인증**을 요구합니다. API 키는 서비스에 가입하면 발급받는 고유한 문자열로, 요청에 포함하여 자신을 증명합니다.

### API 키 인증 패턴

**예제 17-7: API 키 인증**

API 키를 요청에 포함하는 두 가지 대표적인 방식을 보여줍니다.

```python
# examples/python/chapter04/ex17_07_api_key_auth.py
import urllib.request
import urllib.parse
import os

def api_key_in_header():
    """헤더에 API 키를 포함하는 인증 방식입니다."""
    # 환경변수에서 API 키 읽기 (보안 모범 사례)
    api_key = os.environ.get("MY_API_KEY", "demo-key-12345")

    url = "https://httpbin.org/headers"
    req = urllib.request.Request(url)
    # API 키를 헤더에 추가 (일반적인 패턴들)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("X-API-Key", api_key)

def api_key_in_query_param():
    """쿼리 파라미터에 API 키를 포함하는 인증 방식입니다."""
    api_key = os.environ.get("WEATHER_API_KEY", "demo-weather-key")

    base_url = "https://httpbin.org/get"
    params = {
        "apikey": api_key,
        "city": "Seoul",
        "units": "metric",
    }
    query_string = urllib.parse.urlencode(params)
    full_url = f"{base_url}?{query_string}"
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_07_api_key_auth.py
```

**결과:**

```
==================================================
예제 17-7: API 키 인증
==================================================
1. 헤더 방식 API 키 인증:
   Authorization: Bearer demo-key-12345
   X-API-Key: demo-key-12345

2. 쿼리 파라미터 방식 API 키 인증:
   요청 URL: https://httpbin.org/get?apikey=***&city=Seoul&units=metric
   (실제 키는 로그에 숨김 처리)
   서버가 받은 apikey: demo***
   서버가 받은 city: Seoul

3. API 키 안전 관리 모범 사례:
   [방법 1] 환경변수 사용:
   $ export MY_API_KEY='your-actual-key-here'
   api_key = os.environ.get('MY_API_KEY')

   [방법 2] .env 파일 사용:
   # .env 파일 (반드시 .gitignore에 추가!)
   MY_API_KEY=your-actual-key-here
```

> **Warning:** API 키를 소스 코드에 직접 작성하지 마세요! 코드가 GitHub 등에 공개되면 키가 유출됩니다. 반드시 환경변수(`os.environ.get()`)나 `.env` 파일을 사용하고, `.env` 파일은 `.gitignore`에 추가하세요.

### 공공 API 활용하기

인터넷에는 무료로 사용할 수 있는 다양한 공공 API가 있습니다. 인증 없이 바로 사용할 수 있는 것도 많아, API 학습에 안성맞춤입니다.

**예제 17-8: 공공 API 활용**

날씨 정보, 국가 정보, 활동 추천 등 다양한 공공 API를 활용하는 방법을 보여줍니다.

```python
# examples/python/chapter04/ex17_08_public_api.py
import urllib.request
import json

def fetch_country_info():
    """국가 정보 API를 사용합니다 (restcountries.com)."""
    url = "https://restcountries.com/v3.1/name/korea?fullText=false"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")

    with urllib.request.urlopen(req, timeout=10) as response:
        countries = json.loads(response.read().decode("utf-8"))

        for country in countries:
            name = country.get("name", {}).get("common", "N/A")
            official = country.get("name", {}).get("official", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            population = country.get("population", 0)
            region = country.get("region", "N/A")

            print(f"국가명: {name}")
            print(f"공식명: {official}")
            print(f"수도: {capital}")
            print(f"인구: {population:,}명")
            print(f"지역: {region}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_08_public_api.py
```

**결과:**

```
==================================================
예제 17-8: 공공 API 활용
==================================================
1. 날씨 API 활용 (시뮬레이션):
   도시: Seoul (KR)
   기온: 15.2°C
   체감 온도: 13.8°C
   날씨: 구름 조금
   습도: 62%
   풍속: 3.5 m/s

2. 국가 정보 API:
   국가명: South Korea
   공식명: Republic of Korea
   수도: Seoul
   인구: 51,780,579명
   지역: Asia

3. 무작위 활동 제안 API:
   활동: Learn a new programming language
   유형: education
   참여 인원: 1명

4. 유용한 무료 공공 API 목록:
   - JSONPlaceholder: 테스트용 가짜 REST API
     URL: https://jsonplaceholder.typicode.com
   - httpbin.org: HTTP 요청/응답 테스트
     URL: https://httpbin.org
   - REST Countries: 국가 정보
     URL: https://restcountries.com
   - Open Meteo: 날씨 데이터 (키 불필요)
     URL: https://open-meteo.com
   - GitHub API: GitHub 공개 데이터
     URL: https://api.github.com
   - 공공데이터포털: 한국 공공데이터 (키 필요)
     URL: https://data.go.kr
```

### GitHub API 활용

GitHub API는 인증 없이도 공개 리포지토리 정보를 조회할 수 있는 훌륭한 학습 대상입니다.

**예제 17-9: GitHub API 활용**

GitHub 리포지토리 정보 조회, 검색, 사용자 정보 조회를 수행합니다.

```python
# examples/python/chapter04/ex17_09_github_api.py
import urllib.request
import json

def fetch_repo_info(owner, repo):
    """GitHub 리포지토리 정보를 조회합니다."""
    url = f"https://api.github.com/repos/{owner}/{repo}"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "VibeCoding-Book-Example")

    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_09_github_api.py
```

**결과:**

```
==================================================
예제 17-9: GitHub API 활용
==================================================
1. GitHub 리포지토리 정보 조회:
   이름: python/cpython
   설명: The Python programming language
   언어: Python
   별(Stars): 63,000개
   포크(Forks): 30,000개
   열린 이슈: 7,500개
   라이선스: Python Software Foundation License

2. GitHub 리포지토리 검색 ('machine learning'):
   총 검색 결과: 약 50,000개 (상위 5개 표시)

   1. tensorflow/tensorflow
      설명: An Open Source Machine Learning Framework for Ever
      별: 185,000 | 언어: C++
   2. pytorch/pytorch
      설명: Tensors and Dynamic neural networks in Python wit
      별: 82,000 | 언어: Python

3. GitHub 사용자 정보 조회 ('gvanrossum'):
   이름: Guido van Rossum
   로그인: gvanrossum
   소개: Python creator
   공개 리포지토리: 12개
   팔로워: 45,000명

   [Rate Limit] 남은 요청: 58/60
```

> **Note:** GitHub API는 인증 없이 시간당 60회까지 요청할 수 있습니다. 인증 토큰을 사용하면 시간당 5,000회로 늘어납니다. 응답 헤더의 `X-RateLimit-Remaining`으로 남은 횟수를 확인할 수 있습니다.

---

## 17.5 여러 API 조합하기

실제 애플리케이션에서는 하나의 API만 사용하는 경우가 드뭅니다. 여러 API에서 데이터를 가져와 조합하면 훨씬 유용한 정보를 만들 수 있습니다.

**예제 17-10: 여러 API 조합**

사용자 정보, 게시글, 댓글, 날씨 데이터를 조합하여 하나의 대시보드를 구성합니다.

```python
# examples/python/chapter04/ex17_10_combine_apis.py
import urllib.request
import json
import time

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

def build_user_dashboard(user_id):
    """여러 API를 조합하여 사용자 대시보드를 구성합니다."""
    print("사용자 대시보드 구성 중...\n")
    start_time = time.time()

    # 1단계: 사용자 정보 가져오기
    print("[1/4] 사용자 정보 조회...")
    user = fetch_json(f"https://jsonplaceholder.typicode.com/users/{user_id}")

    # 2단계: 사용자 게시글 가져오기
    print("[2/4] 게시글 목록 조회...")
    posts = fetch_json(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")

    # 3단계: 각 게시글의 댓글 수 가져오기
    print("[3/4] 댓글 정보 조회...")
    # ... 댓글 데이터 수집 ...

    # 4단계: 날씨 정보 (시뮬레이션)
    print("[4/4] 날씨 정보 조회...")

    elapsed = time.time() - start_time
    # --- 대시보드 출력 ---
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_10_combine_apis.py
```

**결과:**

```
==================================================
예제 17-10: 여러 API 조합
==================================================
사용자 대시보드 구성 중...

[1/4] 사용자 정보 조회...
[2/4] 게시글 목록 조회...
[3/4] 댓글 정보 조회...
[4/4] 날씨 정보 조회...

==================================================
  사용자 대시보드 - 김바이브
==================================================

  [프로필]
  이름: 김바이브
  이메일: vibe@example.com
  도시: Seoul

  [현재 날씨 - Seoul]
  기온: 15.2°C
  날씨: 맑음
  습도: 55%

  [최근 게시글] (총 3개)
  1. 바이브 코딩 시작하기... (댓글 2개)
  2. Python으로 API 다루기... (댓글 1개)
  3. 프롬프트 엔지니어링 팁... (댓글 0개)

  [통계]
  총 게시글: 3개
  표시된 게시글 댓글 합계: 3개
  데이터 로딩 시간: 1.25초
==================================================
```

여러 API를 조합할 때의 핵심 전략:

1. **공통 헬퍼 함수** 만들기 -- `fetch_json()`처럼 반복되는 HTTP 요청 로직을 함수로 추출합니다
2. **단계별 진행 표시** -- 사용자에게 현재 진행 상황을 알려줍니다
3. **실패 대비** -- 한 API가 실패해도 나머지 데이터로 부분적인 결과를 제공합니다
4. **시간 측정** -- 전체 소요 시간을 측정하여 성능을 파악합니다

---

## 17.6 에러 처리와 타임아웃

API 호출은 네트워크를 거쳐야 하므로 언제든 실패할 수 있습니다. 서버가 다운되었거나, 인터넷 연결이 끊겼거나, 요청이 잘못되었을 수 있습니다. 안정적인 프로그램을 만들려면 이런 상황을 **예상하고 대비**해야 합니다.

### HTTP 에러 코드별 처리

**예제 17-5: 에러 처리**

`urllib.error` 모듈의 `HTTPError`와 `URLError`를 사용하여 다양한 에러 상황을 구분하고 적절히 대응합니다.

```python
# examples/python/chapter04/ex17_05_error_handling.py
import urllib.request
import urllib.error
import json

def handle_http_errors():
    """HTTP 에러 코드별 처리를 보여줍니다."""
    test_urls = [
        ("https://httpbin.org/status/200", "정상 응답"),
        ("https://httpbin.org/status/404", "존재하지 않는 리소스"),
        ("https://httpbin.org/status/500", "서버 내부 에러"),
        ("https://httpbin.org/status/403", "접근 권한 없음"),
    ]

    for url, description in test_urls:
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                print(f"  성공! 상태 코드: {response.status}")

        except urllib.error.HTTPError as e:
            print(f"  HTTP 에러 발생!")
            print(f"  상태 코드: {e.code}")
            print(f"  에러 메시지: {e.reason}")

            if e.code == 404:
                print(f"  안내: 요청한 리소스를 찾을 수 없습니다.")
            elif e.code == 403:
                print(f"  안내: 접근 권한이 없습니다. 인증을 확인하세요.")
            elif e.code == 500:
                print(f"  안내: 서버에 문제가 발생했습니다. 잠시 후 다시 시도하세요.")

        except urllib.error.URLError as e:
            print(f"  네트워크 에러: {e.reason}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_05_error_handling.py
```

**결과:**

```
==================================================
예제 17-5: 에러 처리
==================================================

테스트: 정상 응답 (200)
  성공! 상태 코드: 200

테스트: 존재하지 않는 리소스 (404)
  HTTP 에러 발생!
  상태 코드: 404
  에러 메시지: NOT FOUND
  안내: 요청한 리소스를 찾을 수 없습니다.

테스트: 서버 내부 에러 (500)
  HTTP 에러 발생!
  상태 코드: 500
  에러 메시지: INTERNAL SERVER ERROR
  안내: 서버에 문제가 발생했습니다. 잠시 후 다시 시도하세요.

테스트: 접근 권한 없음 (403)
  HTTP 에러 발생!
  상태 코드: 403
  에러 메시지: FORBIDDEN
  안내: 접근 권한이 없습니다. 인증을 확인하세요.
```

에러 처리에서 가장 중요한 점은 **에러의 종류에 따라 다르게 대응하는 것**입니다:

| 에러 유형 | 클래스 | 대응 방법 |
|-----------|--------|-----------|
| HTTP 에러 (4xx, 5xx) | `urllib.error.HTTPError` | 상태 코드별 분기 처리 |
| 네트워크 에러 | `urllib.error.URLError` | 연결 상태 확인 안내 |
| JSON 파싱 에러 | `json.JSONDecodeError` | 응답 형식 확인 |
| 기타 에러 | `Exception` | 일반적인 에러 메시지 |

예제 17-5에 포함된 `safe_api_call()` 함수는 이 모든 에러를 하나의 일관된 형식으로 처리하는 **재사용 가능한 패턴**입니다:

```python
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
```

> **Tip:** API 호출 결과를 `{"success": True/False, "data": ..., "error": ...}` 형태의 딕셔너리로 통일하면, 호출하는 쪽에서 항상 같은 방식으로 결과를 처리할 수 있어 코드가 깔끔해집니다.

### 타임아웃 설정

API 서버가 응답하지 않으면 프로그램이 무한히 대기할 수 있습니다. `timeout` 파라미터로 최대 대기 시간을 설정하면 이 문제를 방지할 수 있습니다.

**예제 17-6: 타임아웃 설정**

적절한 타임아웃 값을 설정하고, 타임아웃 발생 시 대체 데이터를 제공하는 패턴을 배웁니다.

```python
# examples/python/chapter04/ex17_06_timeout.py
import urllib.request
import time

def demonstrate_timeout():
    """타임아웃 설정과 그 효과를 보여줍니다."""

    # 짧은 타임아웃 (0.001초) - 실패 예상
    url = "https://httpbin.org/delay/3"  # 3초 지연 응답
    start = time.time()
    try:
        with urllib.request.urlopen(url, timeout=0.001) as response:
            print(f"응답 받음: {response.status}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"타임아웃 발생! ({elapsed:.3f}초 후)")

def timeout_with_fallback():
    """타임아웃 발생 시 대체 데이터를 제공하는 패턴입니다."""
    def fetch_user_info(user_id, timeout_sec=5):
        # 캐시된 기본 데이터 (오프라인에서도 사용 가능)
        default_data = {
            "id": user_id,
            "name": "알 수 없음",
            "source": "캐시(기본값)",
        }

        try:
            url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
            with urllib.request.urlopen(url, timeout=timeout_sec) as response:
                data = json.loads(response.read().decode("utf-8"))
                data["source"] = "API 서버"
                return data
        except Exception:
            return default_data
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_06_timeout.py
```

**결과:**

```
==================================================
예제 17-6: 타임아웃 설정
==================================================
1. 짧은 타임아웃 (0.001초) - 실패 예상:
   타임아웃 발생! (0.001초 후)
   에러: timeout

2. 적절한 타임아웃 (10초):
   응답 받음! 상태: 200 (0.342초 소요)

3. 타임아웃 시 대체 데이터 패턴:
   이름: Leanne Graham
   이메일: Sincere@april.biz
   데이터 출처: API 서버

4. 응답 시간 측정:
   httpbin GET: 0.285초 (상태: 200)
   JSONPlaceholder 게시글: 0.198초 (상태: 200)
   JSONPlaceholder 사용자: 0.215초 (상태: 200)
```

> **Warning:** 타임아웃을 너무 짧게 설정하면 정상 응답도 놓칠 수 있고, 너무 길게 설정하면 사용자가 오래 기다려야 합니다. 일반적으로 **5~10초**가 적절하며, API의 특성에 따라 조정하세요.

---

## 17.7 재시도 전략과 Rate Limiting 대응

네트워크는 불안정합니다. 일시적인 서버 오류나 네트워크 지연으로 요청이 실패할 수 있습니다. 또한, 대부분의 API는 과도한 요청을 방지하기 위해 **Rate Limiting**(요청 횟수 제한)을 적용합니다. 이 두 가지 상황에 올바르게 대응하는 것이 안정적인 API 클라이언트의 핵심입니다.

### 재시도 전략

**예제 17-11: 재시도 로직**

단순 재시도, 지수 백오프(exponential backoff), Rate Limit 인식 재시도의 세 가지 전략을 비교합니다.

```python
# examples/python/chapter04/ex17_11_retry_logic.py
import urllib.request
import urllib.error
import time
import random

def simple_retry(url, max_retries=3):
    """단순 재시도: 고정 간격으로 재시도합니다."""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                print(f"성공! (상태: {response.status})")
                return data
        except Exception as e:
            print(f"실패 ({e})")
            if attempt < max_retries:
                time.sleep(1)  # 고정 1초 대기
    return None

def retry_with_exponential_backoff(url, max_retries=4, base_delay=0.5):
    """지수 백오프 재시도: 대기 시간이 점점 늘어납니다."""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            # 4xx 에러는 재시도해도 결과가 같으므로 즉시 중단
            if 400 <= e.code < 500 and e.code != 429:
                return None

        except Exception as e:
            pass

        if attempt < max_retries:
            # 지수 백오프: 2^attempt * base_delay + 랜덤 지터
            delay = (2 ** attempt) * base_delay
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
    return None
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_11_retry_logic.py
```

**결과:**

```
==================================================
예제 17-11: 재시도 로직
==================================================
--- 성공 케이스 ---
1. 단순 재시도 (최대 2회):
   시도 1/2... 성공! (상태: 200)
   응답 URL: https://httpbin.org/get

--- 실패 케이스 (서버 에러 503) ---

2. 지수 백오프 재시도 (최대 3회):
   시도 1/3... HTTP 에러 503
   0.63초 대기 후 재시도... (지수 백오프)
   시도 2/3... HTTP 에러 503
   1.22초 대기 후 재시도... (지수 백오프)
   시도 3/3... HTTP 에러 503
   모든 시도 실패!

--- Rate Limit 케이스 (429) ---

3. Rate Limit 인식 재시도:
   시도 1/2... Rate Limit 초과!
   서버 권장 대기 시간: 2초
   2초 대기 중...
   시도 2/2... Rate Limit 초과!
   모든 시도 실패!

4. 지수 백오프 대기 시간 스케줄:
     시도 |   대기 시간 |   누적 시간
   ------+-----------+-----------
        1 |      2.0초 |      2.0초
        2 |      4.0초 |      6.0초
        3 |      8.0초 |     14.0초
        4 |     16.0초 |     30.0초
        5 |     32.0초 |     62.0초
        6 |     64.0초 |    126.0초

   [참고] 실제로는 지터(jitter)를 추가하여
   여러 클라이언트가 동시에 재시도하는 것을 방지합니다.
```

세 가지 재시도 전략을 비교해 보겠습니다:

| 전략 | 대기 시간 | 장점 | 단점 |
|------|-----------|------|------|
| **단순 재시도** | 고정 (1초) | 구현이 간단 | 서버 부하를 줄이지 못함 |
| **지수 백오프** | 2초, 4초, 8초... | 서버 회복 시간 확보 | 오래 기다릴 수 있음 |
| **지수 백오프 + 지터** | 2초+랜덤, 4초+랜덤... | 동시 재시도 방지 | 약간 복잡 |

핵심 규칙:
- **4xx 에러(429 제외)** -- 클라이언트 잘못이므로 재시도해도 결과가 같습니다. 즉시 중단합니다.
- **5xx 에러** -- 서버 문제이므로 시간을 두고 재시도하면 성공할 수 있습니다.
- **429 에러** -- Rate Limit 초과입니다. `Retry-After` 헤더의 대기 시간을 따릅니다.

### Rate Limiting 대응

Rate Limiting이란 API 서버가 클라이언트의 요청 횟수를 제한하는 것입니다. 과도한 요청으로 서버가 다운되는 것을 방지하기 위한 보호 장치입니다.

예제 17-11의 `retry_with_rate_limit()` 함수는 Rate Limit 상황을 감지하고 적절히 대응합니다:

```python
def retry_with_rate_limit(url, max_retries=3):
    """Rate Limit(429) 에러를 올바르게 처리하는 재시도입니다."""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Retry-After 헤더 확인
                retry_after = e.headers.get("Retry-After", None)
                wait_time = int(retry_after) if retry_after else 2 ** attempt
                print(f"Rate Limit 초과! {wait_time}초 대기...")
                time.sleep(wait_time)
            else:
                print(f"HTTP 에러 {e.code}")
    return None
```

Rate Limiting 대응의 핵심 포인트:

1. **응답 헤더 확인** -- `X-RateLimit-Remaining`으로 남은 호출 횟수를 미리 파악합니다
2. **429 에러 감지** -- HTTP 429 상태 코드는 "요청이 너무 많다"는 뜻입니다
3. **Retry-After 준수** -- 서버가 알려주는 대기 시간을 존중합니다
4. **요청 간격 조절** -- 한꺼번에 많은 요청을 보내지 않고 적절한 간격을 둡니다

> **Note:** Rate Limit은 API마다 다릅니다. GitHub API는 인증 없이 시간당 60회, 인증 시 5,000회입니다. API 문서에서 제한 사항을 반드시 확인하세요.

---

## 17.8 재사용 가능한 API 클라이언트 만들기

지금까지 배운 모든 기법(요청 전송, JSON 처리, 에러 처리, 재시도)을 하나의 **클래스**로 통합하면, 어떤 API에든 재사용할 수 있는 범용 클라이언트를 만들 수 있습니다.

**예제 17-12: API 클라이언트 클래스**

객체지향 프로그래밍으로 헤더 관리, 재시도 로직, 요청 통계까지 포함한 완전한 API 클라이언트를 구현합니다.

```python
# examples/python/chapter04/ex17_12_api_client_class.py
import urllib.request
import urllib.error
import urllib.parse
import json
import time
import random

class APIClient:
    """범용 REST API 클라이언트 클래스."""

    def __init__(self, base_url, headers=None, timeout=10, max_retries=3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = {
            "Accept": "application/json",
            "User-Agent": "VibeCoding-APIClient/1.0",
        }
        if headers:
            self.default_headers.update(headers)

        self._stats = {"total_requests": 0, "successful": 0, "failed": 0, "retries": 0}

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
```

이 `APIClient` 클래스를 상속하면 특정 API에 특화된 클라이언트를 쉽게 만들 수 있습니다:

```python
class GitHubClient(APIClient):
    """GitHub API 전용 클라이언트."""

    def __init__(self, token=None):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        super().__init__(base_url="https://api.github.com", headers=headers)

    def get_repo(self, owner, repo):
        """리포지토리 정보를 조회합니다."""
        result = self.get(f"/repos/{owner}/{repo}")
        if result.get("data"):
            data = result["data"]
            return {
                "name": data.get("full_name"),
                "stars": data.get("stargazers_count"),
                "language": data.get("language"),
            }
        return None

class JSONPlaceholderClient(APIClient):
    """JSONPlaceholder API 전용 클라이언트."""

    def __init__(self):
        super().__init__(base_url="https://jsonplaceholder.typicode.com")

    def get_posts(self, user_id=None):
        params = {"userId": str(user_id)} if user_id else None
        result = self.get("/posts", params=params)
        return result.get("data", [])

    def create_post(self, title, body, user_id=1):
        return self.post("/posts", data={"title": title, "body": body, "userId": user_id})
```

**실행:**

```bash
$ python examples/python/chapter04/ex17_12_api_client_class.py
```

**결과:**

```
==================================================
예제 17-12: API 클라이언트 클래스
==================================================
1. 기본 APIClient 사용:
   GET 성공! 파라미터: {'test': 'hello'}
   POST 성공! 상태: 200

2. JSONPlaceholder 클라이언트:
   게시글 10개 조회됨
   - sunt aut facere repellat provident occ...
   - qui est esse...
   - ea molestias quasi exercitationem repe...
   새 게시글 생성! ID: 101

3. GitHub 클라이언트:
   리포지토리: python/cpython
   설명: The Python programming language
   별: 63,000개
   언어: Python

4. 요청 통계:
   [httpbin] 총: 2, 성공: 2, 실패: 0, 재시도: 0
   [JSONPlaceholder] 총: 2, 성공: 2, 실패: 0, 재시도: 0
   [GitHub] 총: 1, 성공: 1, 실패: 0, 재시도: 0
```

API 클라이언트 클래스의 설계 원칙:

1. **기본 설정 중앙화** -- base URL, 헤더, 타임아웃을 생성자에서 한 번만 설정합니다
2. **메서드별 편의 함수** -- `get()`, `post()`, `put()`, `delete()`로 직관적으로 사용합니다
3. **자동 재시도** -- 내부적으로 지수 백오프 재시도가 동작합니다
4. **통계 추적** -- 요청 횟수, 성공, 실패, 재시도 횟수를 자동으로 기록합니다
5. **상속으로 확장** -- 특정 API에 맞는 전용 클라이언트를 쉽게 만들 수 있습니다

> **Tip:** 이 클라이언트 클래스 패턴을 자신의 프로젝트에 가져다 쓰세요. `base_url`만 바꾸면 어떤 REST API와도 바로 통신할 수 있습니다. 실무에서 더 많은 기능이 필요하다면 `requests` 라이브러리를 살펴보는 것도 좋습니다.

---

## 정리

이번 챕터에서 배운 핵심 내용을 정리합니다.

### 핵심 개념

| 개념 | 설명 |
|------|------|
| REST API | URL로 자원을 식별하고, HTTP 메서드로 동작을 표현하는 API 설계 방식 |
| HTTP 메서드 | GET(조회), POST(생성), PUT(수정), DELETE(삭제) |
| 상태 코드 | 200(성공), 404(없음), 429(제한 초과), 500(서버 오류) 등 |
| JSON | API에서 데이터를 주고받는 표준 형식 |
| Rate Limiting | API 요청 횟수를 제한하는 서버 측 보호 장치 |

### 핵심 코드 패턴

```python
# 1. GET 요청
with urllib.request.urlopen(url, timeout=10) as response:
    data = json.loads(response.read().decode("utf-8"))

# 2. POST 요청
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
req.add_header("Content-Type", "application/json")

# 3. 안전한 에러 처리
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print(f"HTTP 에러: {e.code}")
except urllib.error.URLError as e:
    print(f"네트워크 에러: {e.reason}")

# 4. 지수 백오프 재시도
delay = (2 ** attempt) * base_delay + random.uniform(0, jitter)
time.sleep(delay)
```

### 예제 파일 목록

| 예제 | 파일 | 주제 |
|------|------|------|
| 17-1 | `ex17_01_get_request.py` | GET 요청 기초 |
| 17-2 | `ex17_02_post_request.py` | POST 요청 기초 |
| 17-3 | `ex17_03_headers_params.py` | 헤더와 쿼리 파라미터 |
| 17-4 | `ex17_04_json_response.py` | JSON 응답 처리 |
| 17-5 | `ex17_05_error_handling.py` | HTTP 에러 처리 |
| 17-6 | `ex17_06_timeout.py` | 타임아웃 설정 |
| 17-7 | `ex17_07_api_key_auth.py` | API 키 인증 |
| 17-8 | `ex17_08_public_api.py` | 공공 API 활용 |
| 17-9 | `ex17_09_github_api.py` | GitHub API 활용 |
| 17-10 | `ex17_10_combine_apis.py` | 여러 API 조합 |
| 17-11 | `ex17_11_retry_logic.py` | 재시도 로직 |
| 17-12 | `ex17_12_api_client_class.py` | API 클라이언트 클래스 |

---

## 다음 장 예고

**Chapter 18: 웹 스크래핑**에서는 API가 제공되지 않는 웹사이트에서 데이터를 추출하는 방법을 배웁니다. HTML 구조를 분석하고, BeautifulSoup 라이브러리를 사용하여 원하는 정보를 체계적으로 수집하는 기술을 익힙니다. API 연동과 웹 스크래핑을 함께 활용하면, 인터넷의 거의 모든 데이터에 접근할 수 있게 됩니다.
