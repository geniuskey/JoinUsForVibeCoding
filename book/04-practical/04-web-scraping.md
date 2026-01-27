## Chapter 18: 웹 스크래핑

인터넷에는 무한한 정보가 있습니다. 뉴스 헤드라인, 상품 가격, 통계 데이터, 이미지 목록... 이런 정보를 웹 브라우저로 하나씩 확인하는 것은 비효율적입니다. 만약 프로그램이 자동으로 웹 페이지에서 원하는 데이터를 추출해준다면 어떨까요?

**웹 스크래핑(Web Scraping)**은 웹 페이지의 HTML을 분석하여 원하는 데이터를 자동으로 추출하는 기술입니다. 이번 장에서는 Python 표준 라이브러리만을 사용하여 웹 스크래핑의 기초부터 실전 활용까지 단계별로 배워보겠습니다.

---

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- `urllib.request`를 사용하여 웹 페이지 HTML을 가져오는 방법 이해
- `html.parser.HTMLParser`를 활용하여 HTML 구조를 파싱하는 원리 이해
- 태그, 클래스, 속성 등 다양한 기준으로 원하는 요소를 찾는 방법 습득
- CSS 선택자의 개념을 이해하고 파서에 적용
- 링크, 테이블, 이미지 등 다양한 유형의 데이터를 추출
- 뉴스 헤드라인, 상품 정보 등 실전 스크래핑 시나리오 경험
- 추출한 데이터를 CSV, JSON 파일로 저장하여 활용

---

### 18.1 웹 스크래핑이란?

웹 스크래핑의 기본 원리는 간단합니다:

1. **HTML 가져오기**: 웹 페이지의 HTML 소스 코드를 다운로드합니다.
2. **HTML 파싱(분석)**: 다운로드한 HTML의 구조를 분석합니다.
3. **데이터 추출**: 원하는 정보만 골라냅니다.
4. **결과 저장**: 추출한 데이터를 파일이나 데이터베이스에 저장합니다.

이 과정에서 Python 표준 라이브러리의 두 가지 모듈을 사용합니다:

| 모듈 | 역할 |
|------|------|
| `urllib.request` | 웹 페이지에 HTTP 요청을 보내고 HTML을 가져옴 |
| `html.parser` | HTML 문자열을 분석하여 태그, 속성, 텍스트를 추출 |

> **Note:** 이 장에서는 외부 라이브러리(BeautifulSoup, requests 등)를 사용하지 않고 **Python에 기본 내장된 표준 라이브러리만** 사용합니다. 표준 라이브러리로 원리를 이해하면, 이후 외부 라이브러리를 배울 때 훨씬 수월합니다.

> **Warning:** 웹 스크래핑은 대상 웹사이트의 **이용약관**과 **robots.txt** 규칙을 반드시 확인해야 합니다. 과도한 요청은 서버에 부담을 줄 수 있으며, 일부 사이트에서는 스크래핑을 금지하고 있습니다. 학습 목적으로 사용하되, 항상 윤리적으로 활용하세요.

---

### 18.2 HTML 가져오기

웹 스크래핑의 첫 단계는 웹 페이지의 HTML을 가져오는 것입니다. Python의 `urllib.request` 모듈을 사용하면 외부 라이브러리 없이도 HTTP 요청을 보낼 수 있습니다.

#### urllib.request의 기본 사용법

`urllib.request.urlopen()` 함수는 URL에 요청을 보내고 응답을 받습니다. `Request` 객체를 사용하면 사용자 에이전트(User-Agent) 같은 HTTP 헤더를 함께 보낼 수 있습니다.

---

**예제 18-01: HTML 가져오기**

```python
# examples/python/chapter04/ex18_01_fetch_html.py
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
html = fetch_html("https://example.com")

print("\n--- 가져온 HTML 내용 (처음 300자) ---")
print(html[:300])
print("...")

print("\n--- HTML 기본 정보 ---")
print(f"전체 길이: {len(html)} 글자")
print(f"줄 수: {len(html.splitlines())} 줄")
print(f"'<' 태그 시작 개수: {html.count('<')}")
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_01_fetch_html.py
```

**결과:**
```
==================================================
예제 18-01: HTML 가져오기
==================================================
네트워크 오류 발생: ...
내장 HTML 문자열을 대신 사용합니다.

--- 가져온 HTML 내용 (처음 300자) ---
<!DOCTYPE html>
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
</html>
...

--- HTML 기본 정보 ---
전체 길이: 244 글자
줄 수: 13 줄
'<' 태그 시작 개수: 10
```

이 예제에서 주목할 점은 **네트워크 오류에 대비하는 패턴**입니다. 실제 URL 요청이 실패하면 내장 HTML 문자열을 대신 사용하도록 설계했습니다. 이런 방식을 **폴백(fallback)** 패턴이라고 합니다.

#### 핵심 개념 정리

| 요소 | 설명 |
|------|------|
| `urllib.request.Request` | HTTP 요청을 구성하는 객체. URL과 헤더를 설정 |
| `User-Agent` 헤더 | 요청을 보내는 프로그램의 정체를 알려주는 헤더 |
| `urlopen()` | 실제로 요청을 보내고 응답을 받는 함수 |
| `response.read()` | 응답 본문을 바이트로 읽기 |
| `.decode("utf-8")` | 바이트를 문자열로 변환 |
| `timeout` | 응답 대기 시간 제한 (초 단위) |

> **Tip:** 네트워크 요청은 항상 실패할 수 있습니다. `try/except`로 예외를 처리하고 폴백 데이터를 준비하는 것은 안정적인 프로그램을 만드는 좋은 습관입니다.

---

### 18.3 HTMLParser로 태그 찾기

HTML을 가져왔으면 이제 그 안에서 원하는 정보를 찾아야 합니다. Python의 `html.parser.HTMLParser`는 HTML 문자열을 순차적으로 읽으면서 태그, 속성, 텍스트를 처리할 수 있는 이벤트 기반 파서입니다.

#### HTMLParser의 동작 원리

`HTMLParser`는 HTML을 읽으면서 특정 이벤트가 발생할 때 메서드를 호출합니다:

| 메서드 | 호출 시점 | 예시 |
|--------|-----------|------|
| `handle_starttag(tag, attrs)` | 시작 태그를 만났을 때 | `<h1 class="title">` |
| `handle_endtag(tag)` | 종료 태그를 만났을 때 | `</h1>` |
| `handle_data(data)` | 태그 사이의 텍스트를 만났을 때 | `바이브 코딩` |

이 메서드들을 오버라이드(재정의)하여 원하는 동작을 구현합니다.

---

**예제 18-02: 태그로 요소 찾기**

HTML에서 `<h1>`, `<h2>`, `<p>` 태그의 텍스트를 수집하는 파서를 만들어봅시다.

```python
# examples/python/chapter04/ex18_02_find_tags.py
from html.parser import HTMLParser

# 파싱할 HTML 문자열
HTML_CONTENT = """<!DOCTYPE html>
<html>
<head><title>바이브 코딩 소개</title></head>
<body>
    <h1>바이브 코딩이란?</h1>
    <p>AI와 대화하며 코드를 작성하는 새로운 방식입니다.</p>
    <h2>왜 바이브 코딩인가?</h2>
    <p>프로그래밍의 진입 장벽을 크게 낮춰줍니다.</p>
    <h1>시작하기</h1>
    <p>터미널을 열고 AI 어시스턴트와 대화를 시작하세요.</p>
    <h2>필요한 도구</h2>
    <p>Python, CLI, 그리고 AI 어시스턴트만 있으면 됩니다.</p>
</body>
</html>"""


class TagFinder(HTMLParser):
    """특정 태그의 텍스트 내용을 수집하는 파서"""

    def __init__(self, target_tags):
        super().__init__()
        self.target_tags = target_tags    # 찾을 태그 목록
        self.current_tag = None           # 현재 처리 중인 태그
        self.results = {}                 # 태그별 결과 저장

        # 각 태그별 빈 리스트 초기화
        for tag in target_tags:
            self.results[tag] = []

    def handle_starttag(self, tag, attrs):
        """시작 태그를 만났을 때 호출됩니다."""
        if tag in self.target_tags:
            self.current_tag = tag

    def handle_endtag(self, tag):
        """종료 태그를 만났을 때 호출됩니다."""
        if tag == self.current_tag:
            self.current_tag = None

    def handle_data(self, data):
        """태그 안의 텍스트 데이터를 처리합니다."""
        if self.current_tag and data.strip():
            self.results[self.current_tag].append(data.strip())


# h1, h2, p 태그를 찾는 파서 생성
finder = TagFinder(["h1", "h2", "p"])
finder.feed(HTML_CONTENT)

# 결과 출력
for tag, texts in finder.results.items():
    print(f"\n<{tag}> 태그 ({len(texts)}개 발견):")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_02_find_tags.py
```

**결과:**
```
==================================================
예제 18-02: 태그로 요소 찾기
==================================================

<h1> 태그 (2개 발견):
  1. 바이브 코딩이란?
  2. 시작하기

<h2> 태그 (2개 발견):
  1. 왜 바이브 코딩인가?
  2. 필요한 도구

<p> 태그 (4개 발견):
  1. AI와 대화하며 코드를 작성하는 새로운 방식입니다.
  2. 프로그래밍의 진입 장벽을 크게 낮춰줍니다.
  3. 터미널을 열고 AI 어시스턴트와 대화를 시작하세요.
  4. Python, CLI, 그리고 AI 어시스턴트만 있으면 됩니다.

--- 요약 ---
총 8개의 요소를 찾았습니다.
```

#### 파서의 동작 흐름

`TagFinder` 클래스가 HTML을 처리하는 과정을 단계별로 살펴봅시다:

```
HTML: <h1>바이브 코딩이란?</h1>

1. handle_starttag("h1", [])  →  current_tag = "h1"  (찾을 태그!)
2. handle_data("바이브 코딩이란?")  →  results["h1"]에 추가
3. handle_endtag("h1")  →  current_tag = None  (태그 종료)
```

이처럼 파서는 HTML을 위에서 아래로 순차적으로 읽으면서, 시작 태그 - 텍스트 - 종료 태그의 패턴을 추적합니다.

> **Tip:** `handle_data`에서 `data.strip()`으로 공백을 제거하는 것은 중요합니다. HTML에는 들여쓰기나 줄바꿈 등의 불필요한 공백이 많기 때문입니다.

---

### 18.4 클래스(class)로 요소 찾기

실제 웹 페이지에서는 같은 태그가 수십, 수백 개 사용됩니다. 예를 들어 `<p>` 태그는 모든 단락에 사용되기 때문에, 태그 이름만으로는 원하는 요소를 정확히 찾기 어렵습니다.

이럴 때 HTML의 **class 속성**을 활용합니다. class는 요소에 부여된 이름표 같은 것으로, 같은 스타일이나 역할을 하는 요소들에 공통으로 지정됩니다.

```html
<!-- 같은 <p> 태그지만 class가 다릅니다 -->
<p class="intro">소개 문단입니다.</p>
<p class="highlight">강조 문단입니다.</p>
<p>일반 문단입니다.</p>
```

---

**예제 18-03: 클래스로 요소 찾기**

```python
# examples/python/chapter04/ex18_03_find_by_class.py
from html.parser import HTMLParser

HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <div class="header">
        <h1 class="title main-title">바이브 코딩 가이드</h1>
    </div>
    <div class="content">
        <p class="intro">이 가이드는 바이브 코딩을 처음 시작하는 분을 위해 작성되었습니다.</p>
        <p class="highlight">AI 어시스턴트와 함께라면 누구나 프로그래밍을 할 수 있습니다!</p>
        <p>일반 단락입니다. 클래스가 없습니다.</p>
        <p class="highlight">자연어만으로 복잡한 프로그램을 만들 수 있습니다.</p>
        <p class="intro">기초부터 심화까지 단계별로 안내합니다.</p>
    </div>
    <div class="footer">
        <p class="copyright">&copy; 2025 바이브 코딩</p>
    </div>
</body>
</html>"""


class ClassFinder(HTMLParser):
    """특정 class를 가진 요소의 텍스트를 수집하는 파서"""

    def __init__(self, target_class):
        super().__init__()
        self.target_class = target_class
        self.is_matching = False
        self.results = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        """시작 태그에서 class 속성을 확인합니다."""
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")

        # class 속성에 target_class가 포함되어 있는지 확인
        # class="title main-title"처럼 여러 클래스가 있을 수 있음
        class_list = class_value.split()
        if self.target_class in class_list:
            self.is_matching = True
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == self.current_tag and self.is_matching:
            self.is_matching = False
            self.current_tag = None

    def handle_data(self, data):
        if self.is_matching and data.strip():
            self.results.append(data.strip())


# 다양한 클래스로 검색
search_classes = ["highlight", "intro", "title", "copyright"]

for class_name in search_classes:
    finder = ClassFinder(class_name)
    finder.feed(HTML_CONTENT)

    print(f'\nclass="{class_name}" 요소 ({len(finder.results)}개):')
    if finder.results:
        for i, text in enumerate(finder.results, 1):
            print(f"  {i}. {text}")
    else:
        print("  (발견되지 않음)")
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_03_find_by_class.py
```

**결과:**
```
==================================================
예제 18-03: 클래스로 요소 찾기
==================================================

class="highlight" 요소 (2개):
  1. AI 어시스턴트와 함께라면 누구나 프로그래밍을 할 수 있습니다!
  2. 자연어만으로 복잡한 프로그램을 만들 수 있습니다.

class="intro" 요소 (2개):
  1. 이 가이드는 바이브 코딩을 처음 시작하는 분을 위해 작성되었습니다.
  2. 기초부터 심화까지 단계별로 안내합니다.

class="title" 요소 (1개):
  1. 바이브 코딩 가이드

class="copyright" 요소 (1개):
  1. © 2025 바이브 코딩

--- HTML에 사용된 모든 클래스 ---
  - content
  - copyright
  - footer
  - header
  - highlight
  - intro
  - main-title
  - title
```

#### 여러 클래스를 가진 요소

HTML 요소는 여러 클래스를 동시에 가질 수 있습니다:

```html
<h1 class="title main-title">바이브 코딩 가이드</h1>
```

이 요소의 `class` 속성값은 `"title main-title"`이라는 하나의 문자열입니다. 따라서 `.split()`으로 분리한 후 원하는 클래스가 포함되어 있는지 확인해야 합니다:

```python
class_list = "title main-title".split()  # ["title", "main-title"]
"title" in class_list  # True
```

> **Note:** 단순히 `"title" in "title main-title"` 같은 문자열 포함 검사를 하면 `"main-title"`에도 `"title"`이 매칭되는 문제가 생깁니다. 반드시 `split()` 후 리스트에서 검사하세요.

---

### 18.5 CSS 선택자 패턴 이해하기

웹 스크래핑에서 **CSS 선택자**는 원하는 HTML 요소를 정확히 지정하는 표준 방법입니다. CSS 선택자의 개념을 이해하면 웹 페이지의 구조를 빠르게 파악하고, 원하는 데이터를 효율적으로 찾을 수 있습니다.

---

**예제 18-04: CSS 선택자 개념과 구현**

```python
# examples/python/chapter04/ex18_04_css_selectors.py
from html.parser import HTMLParser

HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <div id="main-content">
        <h1>바이브 코딩 튜토리얼</h1>
        <p class="description">AI와 함께 코딩하는 방법을 배워봅시다.</p>
        <ul>
            <li class="item active">1장: 소개</li>
            <li class="item">2장: 환경 설정</li>
            <li class="item active">3장: 첫 번째 프로젝트</li>
            <li class="item">4장: 실전 활용</li>
        </ul>
        <a href="https://example.com" class="link">더 알아보기</a>
    </div>
    <div id="sidebar">
        <p class="description">사이드바 설명</p>
        <a href="https://example.com/about" class="link">소개 페이지</a>
    </div>
</body>
</html>"""


class SelectorParser(HTMLParser):
    """CSS 선택자 개념을 구현한 간단한 파서"""

    def __init__(self):
        super().__init__()
        self.elements = []
        self._current = None
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._current = {
            "tag": tag,
            "id": attrs_dict.get("id", ""),
            "class": attrs_dict.get("class", ""),
            "attrs": attrs_dict,
            "text": "",
            "depth": self._depth,
        }
        self._depth += 1

    def handle_endtag(self, tag):
        self._depth -= 1
        if self._current and self._current["tag"] == tag:
            if self._current["text"].strip():
                self.elements.append(self._current)
            self._current = None

    def handle_data(self, data):
        if self._current and data.strip():
            self._current["text"] += data.strip()

    def select_by_tag(self, tag_name):
        """태그 선택자: p, h1 등"""
        return [e for e in self.elements if e["tag"] == tag_name]

    def select_by_class(self, class_name):
        """.클래스 선택자: .description 등"""
        return [e for e in self.elements
                if class_name in e["class"].split()]

    def select_by_id(self, id_name):
        """#아이디 선택자: #main-content 등"""
        return [e for e in self.elements if e["id"] == id_name]

    def select_by_tag_and_class(self, tag_name, class_name):
        """태그.클래스 선택자: li.active 등"""
        return [e for e in self.elements
                if e["tag"] == tag_name and class_name in e["class"].split()]

    def select_by_attribute(self, attr_name, attr_value=None):
        """[속성] 또는 [속성=값] 선택자"""
        if attr_value is None:
            return [e for e in self.elements if attr_name in e["attrs"]]
        return [e for e in self.elements
                if e["attrs"].get(attr_name) == attr_value]
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_04_css_selectors.py
```

**결과:**
```
==================================================
예제 18-04: CSS 선택자 개념
==================================================

CSS 선택자는 HTML 요소를 '선택'하는 패턴입니다.
웹 스크래핑에서 원하는 데이터를 정확히 찾기 위해 사용합니다.

주요 선택자 종류:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  선택자          │ 의미                  │ 예시
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  태그            │ 태그 이름으로 선택     │ p, h1, div
  .클래스         │ class 속성으로 선택    │ .description
  #아이디         │ id 속성으로 선택       │ #main-content
  태그.클래스     │ 태그 + 클래스 조합     │ li.active
  부모 > 자식     │ 직계 자식 요소 선택    │ ul > li
  [속성]          │ 속성 존재 여부로 선택  │ [href]
  [속성=값]       │ 속성값으로 선택        │ [class=item]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

--- 선택자 실습 ---

선택자: p  →  2개 발견
  "AI와 함께 코딩하는 방법을 배워봅시다."
  "사이드바 설명"

선택자: .active  →  2개 발견
  "1장: 소개"
  "3장: 첫 번째 프로젝트"

선택자: #main-content  →  0개 발견

선택자: li.active  →  2개 발견
  "1장: 소개"
  "3장: 첫 번째 프로젝트"

선택자: [href]  →  2개 발견
  "더 알아보기" → https://example.com
  "소개 페이지" → https://example.com/about
```

#### CSS 선택자 요약표

이 표를 기억해두면 웹 스크래핑할 때 원하는 요소를 빠르게 찾을 수 있습니다:

| CSS 선택자 | Python 구현 방식 | 용도 |
|------------|------------------|------|
| `p` | `tag == "p"` | 특정 태그의 모든 요소 |
| `.intro` | `"intro" in class_list` | 특정 클래스를 가진 요소 |
| `#header` | `id == "header"` | 특정 ID를 가진 유일한 요소 |
| `li.active` | `tag == "li" and "active" in class_list` | 태그 + 클래스 조합 |
| `[href]` | `"href" in attrs` | 특정 속성이 있는 요소 |

> **Tip:** 웹 브라우저의 개발자 도구(F12)에서 요소를 마우스 오른쪽 클릭하고 "검사"를 선택하면, 해당 요소의 태그, 클래스, ID를 바로 확인할 수 있습니다. 이를 통해 스크래핑에 필요한 선택자를 쉽게 파악할 수 있습니다.

---

### 18.6 링크 추출하기

웹 페이지에서 가장 많이 추출하는 데이터 중 하나가 바로 **링크(URL)**입니다. `<a>` 태그의 `href` 속성에 담긴 URL과 링크 텍스트를 함께 수집하면, 사이트의 구조를 파악하거나 관련 페이지를 탐색하는 데 활용할 수 있습니다.

---

**예제 18-05: 링크 추출하기**

```python
# examples/python/chapter04/ex18_05_extract_links.py
from html.parser import HTMLParser

HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <nav>
        <a href="/">홈</a>
        <a href="/about">소개</a>
        <a href="/tutorials">튜토리얼</a>
        <a href="/contact">문의</a>
    </nav>

    <main>
        <h1>유용한 바이브 코딩 자료</h1>

        <h2>공식 문서</h2>
        <ul>
            <li><a href="https://docs.python.org/ko/3/">Python 공식 문서</a></li>
            <li><a href="https://developer.mozilla.org/ko/">MDN 웹 문서</a></li>
        </ul>

        <h2>추천 도구</h2>
        <ul>
            <li><a href="https://code.visualstudio.com/">VS Code 다운로드</a></li>
            <li><a href="https://github.com/" target="_blank">GitHub</a></li>
        </ul>

        <h2>커뮤니티</h2>
        <p>
            <a href="https://discord.gg/example">디스코드 채널</a>에 참여하거나
            <a href="mailto:hello@example.com">이메일</a>로 연락주세요.
        </p>
    </main>

    <footer>
        <a href="/privacy">개인정보처리방침</a> |
        <a href="/terms">이용약관</a>
    </footer>
</body>
</html>"""


class LinkExtractor(HTMLParser):
    """HTML에서 모든 링크(<a> 태그)를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.links = []
        self.current_href = None
        self.current_attrs = {}
        self.current_text = ""
        self.in_a_tag = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_a_tag = True
            self.current_attrs = dict(attrs)
            self.current_href = self.current_attrs.get("href", "")
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "a" and self.in_a_tag:
            self.links.append({
                "text": self.current_text.strip(),
                "href": self.current_href,
                "attrs": self.current_attrs,
            })
            self.in_a_tag = False

    def handle_data(self, data):
        if self.in_a_tag:
            self.current_text += data


# 실행
extractor = LinkExtractor()
extractor.feed(HTML_CONTENT)

# 모든 링크 출력
print(f"\n총 {len(extractor.links)}개의 링크를 발견했습니다:\n")
for i, link in enumerate(extractor.links, 1):
    print(f"  {i:2d}. [{link['text']}] -> {link['href']}")

# 링크 유형별 분류
internal_links = []
external_links = []
mail_links = []

for link in extractor.links:
    href = link["href"]
    if href.startswith("mailto:"):
        mail_links.append(link)
    elif href.startswith("http://") or href.startswith("https://"):
        external_links.append(link)
    else:
        internal_links.append(link)
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_05_extract_links.py
```

**결과:**
```
==================================================
예제 18-05: 링크 추출하기
==================================================

총 12개의 링크를 발견했습니다:

   1. [홈] → /
   2. [소개] → /about
   3. [튜토리얼] → /tutorials
   4. [문의] → /contact
   5. [Python 공식 문서] → https://docs.python.org/ko/3/
   6. [MDN 웹 문서] → https://developer.mozilla.org/ko/
   7. [VS Code 다운로드] → https://code.visualstudio.com/
   8. [GitHub] → https://github.com/
   9. [디스코드 채널] → https://discord.gg/example
  10. [이메일] → mailto:hello@example.com
  11. [개인정보처리방침] → /privacy
  12. [이용약관] → /terms

--- 링크 유형별 분류 ---

내부 링크 (6개):
  - [홈] → /
  - [소개] → /about
  - [튜토리얼] → /tutorials
  - [문의] → /contact
  - [개인정보처리방침] → /privacy
  - [이용약관] → /terms

외부 링크 (5개):
  - [Python 공식 문서] → https://docs.python.org/ko/3/
  - [MDN 웹 문서] → https://developer.mozilla.org/ko/
  - [VS Code 다운로드] → https://code.visualstudio.com/
  - [GitHub] → https://github.com/
  - [디스코드 채널] → https://discord.gg/example

메일 링크 (1개):
  - [이메일] → mailto:hello@example.com
```

#### 링크 유형 분류

추출한 링크를 유형별로 분류하면 더 유용하게 활용할 수 있습니다:

| 유형 | 판별 방법 | 예시 |
|------|-----------|------|
| 내부 링크 | `/`로 시작하는 상대 경로 | `/about`, `/tutorials` |
| 외부 링크 | `http://` 또는 `https://`로 시작 | `https://github.com/` |
| 메일 링크 | `mailto:`로 시작 | `mailto:hello@example.com` |

> **Tip:** 내부 링크(상대 경로)를 절대 URL로 변환하려면 `urllib.parse.urljoin()`을 사용하면 됩니다. 이 기능은 예제 18-07에서 자세히 다룹니다.

---

### 18.7 테이블 데이터 추출

HTML `<table>`은 행과 열로 구조화된 데이터를 담고 있어, 스크래핑에서 매우 유용한 대상입니다. 통계, 순위, 가격표 등 다양한 데이터가 테이블 형태로 제공됩니다.

#### HTML 테이블 구조

```html
<table>
    <thead>        <!-- 헤더 영역 -->
        <tr>       <!-- 행(row) -->
            <th>이름</th>    <!-- 헤더 셀 -->
            <th>점수</th>
        </tr>
    </thead>
    <tbody>        <!-- 데이터 영역 -->
        <tr>
            <td>홍길동</td>  <!-- 데이터 셀 -->
            <td>95</td>
        </tr>
    </tbody>
</table>
```

---

**예제 18-06: 테이블 데이터 추출**

```python
# examples/python/chapter04/ex18_06_table_data.py
from html.parser import HTMLParser

HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <h1>프로그래밍 언어 인기 순위 (2025)</h1>
    <table>
        <thead>
            <tr>
                <th>순위</th>
                <th>언어</th>
                <th>점유율</th>
                <th>주요 용도</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>Python</td>
                <td>28.1%</td>
                <td>AI/ML, 데이터 분석, 웹</td>
            </tr>
            <!-- ... 더 많은 행 ... -->
        </tbody>
    </table>
</body>
</html>"""


class TableParser(HTMLParser):
    """HTML 테이블을 파싱하여 딕셔너리 리스트로 변환하는 파서"""

    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_thead = False
        self.in_tbody = False
        self.in_tr = False
        self.in_cell = False
        self.current_cell = ""
        self.current_row = []
        self.headers = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif tag == "thead":
            self.in_thead = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
        elif tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "tr":
            self.in_tr = False
            if self.in_thead:
                self.headers = self.current_row
            elif self.in_tbody:
                self.rows.append(self.current_row)
        elif tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

    def to_dict_list(self):
        """헤더와 데이터 행을 딕셔너리 리스트로 변환합니다."""
        result = []
        for row in self.rows:
            row_dict = {}
            for i, header in enumerate(self.headers):
                if i < len(row):
                    row_dict[header] = row[i]
            result.append(row_dict)
        return result
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_06_table_data.py
```

**결과:**
```
==================================================
예제 18-06: 테이블 데이터 추출
==================================================

헤더: ['순위', '언어', '점유율', '주요 용도']
데이터 행 수: 5

--- 추출된 데이터 (딕셔너리 리스트) ---

  {'순위': '1', '언어': 'Python', '점유율': '28.1%', '주요 용도': 'AI/ML, 데이터 분석, 웹'}
  {'순위': '2', '언어': 'JavaScript', '점유율': '20.5%', '주요 용도': '웹 프론트엔드, 서버'}
  {'순위': '3', '언어': 'Java', '점유율': '12.3%', '주요 용도': '엔터프라이즈, 안드로이드'}
  {'순위': '4', '언어': 'TypeScript', '점유율': '9.7%', '주요 용도': '웹 프론트엔드, 서버'}
  {'순위': '5', '언어': 'Rust', '점유율': '5.2%', '주요 용도': '시스템 프로그래밍'}

--- 정리된 표 ---

  순위 | 언어           |    점유율 | 주요 용도
-------------------------------------------------------
   1 | Python       |  28.1% | AI/ML, 데이터 분석, 웹
   2 | JavaScript   |  20.5% | 웹 프론트엔드, 서버
   3 | Java         |  12.3% | 엔터프라이즈, 안드로이드
   4 | TypeScript   |   9.7% | 웹 프론트엔드, 서버
   5 | Rust         |   5.2% | 시스템 프로그래밍

--- 점유율 10% 이상 언어 ---
  Python: 28.1%
  JavaScript: 20.5%
  Java: 12.3%
```

#### 테이블 파서의 핵심: 상태 추적

테이블 파서는 여러 개의 상태 플래그를 사용합니다. 이는 테이블이 중첩된 구조(`table > thead > tr > th`)를 가지기 때문입니다:

```
<table>       →  in_table = True
  <thead>     →  in_thead = True
    <tr>      →  in_tr = True
      <th>    →  in_cell = True, current_cell 수집 시작
      </th>   →  in_cell = False, current_row에 추가
    </tr>     →  in_tr = False, headers에 저장
  </thead>    →  in_thead = False
  <tbody>     →  in_tbody = True
    <tr>      →  in_tr = True
      <td>    →  in_cell = True
      </td>   →  current_row에 추가
    </tr>     →  rows에 추가
  </tbody>
</table>
```

`to_dict_list()` 메서드는 헤더와 데이터 행을 결합하여 `{"순위": "1", "언어": "Python", ...}` 형태의 딕셔너리 리스트로 변환합니다. 이렇게 변환하면 `item["언어"]`처럼 이름으로 데이터에 접근할 수 있어 훨씬 편리합니다.

---

### 18.8 이미지 URL 추출

웹 페이지에서 이미지를 수집하려면 `<img>` 태그의 `src` 속성을 추출합니다. 이미지 스크래핑은 갤러리 데이터 수집, 상품 이미지 분석 등에 활용됩니다.

이때 중요한 것은 **상대 경로와 절대 경로의 구분**입니다:

- **절대 경로**: `https://cdn.example.com/photos/image.png` (완전한 URL)
- **상대 경로**: `/images/logo.png` (기준 URL과 합쳐야 완전한 URL이 됨)

`urllib.parse.urljoin()`을 사용하면 상대 경로를 절대 URL로 쉽게 변환할 수 있습니다.

---

**예제 18-07: 이미지 URL 수집**

```python
# examples/python/chapter04/ex18_07_image_urls.py
from html.parser import HTMLParser
from urllib.parse import urljoin

HTML_CONTENT = """<!DOCTYPE html>
<html>
<body>
    <header>
        <img src="/images/logo.png" alt="사이트 로고" width="200">
    </header>
    <main>
        <h1>바이브 코딩 갤러리</h1>
        <section class="gallery">
            <figure>
                <img src="/images/vibe-coding-intro.jpg" alt="바이브 코딩 소개 이미지">
            </figure>
            <figure>
                <img src="https://cdn.example.com/photos/ai-assistant.png"
                     alt="AI 어시스턴트 화면">
            </figure>
            <!-- ... 더 많은 이미지 ... -->
        </section>
    </main>
</body>
</html>"""

BASE_URL = "https://www.vibecoding-example.com"


class ImageExtractor(HTMLParser):
    """HTML에서 모든 이미지 정보를 추출하는 파서"""

    def __init__(self, base_url=""):
        super().__init__()
        self.base_url = base_url
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attrs_dict = dict(attrs)
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "(대체 텍스트 없음)")
            width = attrs_dict.get("width", "")
            height = attrs_dict.get("height", "")

            # 상대 경로를 절대 경로로 변환
            if self.base_url and not src.startswith(("http://", "https://")):
                full_url = urljoin(self.base_url, src)
            else:
                full_url = src

            self.images.append({
                "src": src,
                "full_url": full_url,
                "alt": alt,
                "width": width,
                "height": height,
            })


extractor = ImageExtractor(base_url=BASE_URL)
extractor.feed(HTML_CONTENT)

print(f"\n총 {len(extractor.images)}개의 이미지를 발견했습니다:\n")
for i, img in enumerate(extractor.images, 1):
    print(f"이미지 {i}:")
    print(f"  원본 경로: {img['src']}")
    print(f"  절대 URL:  {img['full_url']}")
    print(f"  대체 텍스트: {img['alt']}")
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_07_image_urls.py
```

**결과:**
```
==================================================
예제 18-07: 이미지 URL 수집
==================================================

총 6개의 이미지를 발견했습니다:

이미지 1:
  원본 경로: /images/logo.png
  절대 URL:  https://www.vibecoding-example.com/images/logo.png
  대체 텍스트: 사이트 로고
  크기: 200x

이미지 2:
  원본 경로: /images/vibe-coding-intro.jpg
  절대 URL:  https://www.vibecoding-example.com/images/vibe-coding-intro.jpg
  대체 텍스트: 바이브 코딩 소개 이미지

이미지 3:
  원본 경로: https://cdn.example.com/photos/ai-assistant.png
  절대 URL:  https://cdn.example.com/photos/ai-assistant.png
  대체 텍스트: AI 어시스턴트 화면

--- 확장자별 분류 ---

.gif (1개):
  - 코드 실행 결과
.jpg (1개):
  - 바이브 코딩 소개 이미지
.png (3개):
  - 사이트 로고
  - AI 어시스턴트 화면
  - 터미널 스크린샷
.webp (1개):
  - 프로젝트 완성

--- 호스팅 위치별 분류 ---

내부 이미지 (4개):
  - 사이트 로고: https://www.vibecoding-example.com/images/logo.png
  - 바이브 코딩 소개 이미지: https://www.vibecoding-example.com/images/vibe-coding-intro.jpg
  - 터미널 스크린샷: https://www.vibecoding-example.com/images/terminal-screenshot.png
  - 프로젝트 완성: https://www.vibecoding-example.com/images/project-complete.webp

외부 이미지 (2개):
  - AI 어시스턴트 화면: https://cdn.example.com/photos/ai-assistant.png
  - 코드 실행 결과: https://cdn.example.com/photos/code-result.gif
```

#### urljoin의 동작 원리

`urllib.parse.urljoin()`은 기준 URL과 상대 경로를 합쳐 절대 URL을 만듭니다:

```python
from urllib.parse import urljoin

base = "https://www.example.com"

urljoin(base, "/images/logo.png")
# → "https://www.example.com/images/logo.png"

urljoin(base, "https://cdn.example.com/photo.jpg")
# → "https://cdn.example.com/photo.jpg"  (이미 절대 URL이면 그대로)
```

이 기능은 이미지뿐만 아니라 상대 경로로 된 모든 링크를 절대 URL로 변환할 때 사용할 수 있습니다.

> **Tip:** 이미지를 확장자별로 분류하면 PNG, JPG, GIF, WebP 등 파일 형식을 파악할 수 있습니다. 이는 이미지 다운로드나 필터링 시 유용합니다.

---

### 18.9 실전: 뉴스 헤드라인 수집기

지금까지 배운 기법을 종합하여 실전 스크래핑 프로젝트를 만들어봅시다. 첫 번째 실전 프로젝트는 **뉴스 헤드라인 수집기**입니다.

뉴스 사이트의 HTML 구조를 분석하여 기사의 제목, 요약, 카테고리, 기자명, 발행일 등을 추출합니다.

---

**예제 18-08: 뉴스 헤드라인 수집기**

```python
# examples/python/chapter04/ex18_08_news_headlines.py
from html.parser import HTMLParser

# 뉴스 사이트를 모사한 HTML
NEWS_HTML = """<!DOCTYPE html>
<html>
<body>
    <header>
        <h1>바이브 코딩 뉴스</h1>
        <p class="date">2025년 7월 15일</p>
    </header>

    <section class="news-list">
        <article class="news-item featured">
            <h2 class="headline">AI 코딩 어시스턴트, 개발 생산성 300% 향상시켜</h2>
            <p class="summary">최근 연구에 따르면 AI 코딩 도구를 사용하는 개발자의
            생산성이 평균 3배 이상 증가한 것으로 나타났다.</p>
            <span class="category">기술</span>
            <span class="author">김바이브 기자</span>
            <time class="published">2025-07-15 09:00</time>
        </article>

        <article class="news-item">
            <h2 class="headline">프로그래밍 입문자 수, 전년 대비 150% 증가</h2>
            <p class="summary">바이브 코딩의 등장으로 프로그래밍에 도전하는
            비전공자가 급증하고 있다.</p>
            <span class="category">교육</span>
            <span class="author">이코딩 기자</span>
            <time class="published">2025-07-15 10:30</time>
        </article>
        <!-- ... 더 많은 기사 ... -->
    </section>
</body>
</html>"""


class NewsParser(HTMLParser):
    """뉴스 HTML에서 기사 정보를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.articles = []
        self.in_article = False
        self.is_featured = False
        self.current_article = {}
        self.current_tag = None
        self.current_class = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")

        if tag == "article" and "news-item" in class_value:
            self.in_article = True
            self.is_featured = "featured" in class_value
            self.current_article = {"featured": self.is_featured}

        if self.in_article:
            self.current_tag = tag
            self.current_class = class_value

    def handle_endtag(self, tag):
        if tag == "article" and self.in_article:
            self.articles.append(self.current_article)
            self.in_article = False
            self.current_article = {}

        if self.in_article:
            self.current_tag = None
            self.current_class = ""

    def handle_data(self, data):
        if not self.in_article or not data.strip():
            return

        text = data.strip()
        if self.current_class == "headline":
            self.current_article["headline"] = text
        elif self.current_class == "summary":
            existing = self.current_article.get("summary", "")
            self.current_article["summary"] = (existing + " " + text).strip()
        elif self.current_class == "category":
            self.current_article["category"] = text
        elif self.current_class == "author":
            self.current_article["author"] = text
        elif self.current_class == "published":
            self.current_article["published"] = text
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_08_news_headlines.py
```

**결과:**
```
============================================================
예제 18-08: 뉴스 헤드라인 수집기
============================================================

총 5개의 기사를 수집했습니다.

--- 헤드라인 목록 ---

  1. AI 코딩 어시스턴트, 개발 생산성 300% 향상시켜 ★
  2. 프로그래밍 입문자 수, 전년 대비 150% 증가
  3. 오픈소스 AI 모델, 코드 생성 정확도 95% 달성
  4. 기업 80%, 향후 2년 내 AI 코딩 도구 도입 예정
  5. 자연어 프로그래밍 교육과정, 대학에 신설

--- 기사 상세 ---

[1] AI 코딩 어시스턴트, 개발 생산성 300% 향상시켜
    카테고리: 기술
    기자: 김바이브 기자
    발행일: 2025-07-15 09:00
    요약: 최근 연구에 따르면 AI 코딩 도구를 사용하는 개발자의
            생산성이 평균 3배 이상 증가한 것으로 나타났다.
    ★ 주요 기사

[2] 프로그래밍 입문자 수, 전년 대비 150% 증가
    카테고리: 교육
    기자: 이코딩 기자
    발행일: 2025-07-15 10:30
    요약: 바이브 코딩의 등장으로 프로그래밍에 도전하는
            비전공자가 급증하고 있다.

--- 카테고리별 분류 ---

교육 (2건):
  - 프로그래밍 입문자 수, 전년 대비 150% 증가
  - 자연어 프로그래밍 교육과정, 대학에 신설
기술 (2건):
  - AI 코딩 어시스턴트, 개발 생산성 300% 향상시켜
  - 오픈소스 AI 모델, 코드 생성 정확도 95% 달성
비즈니스 (1건):
  - 기업 80%, 향후 2년 내 AI 코딩 도구 도입 예정
```

#### 뉴스 파서의 설계 포인트

이 파서는 이전 예제들과 비교하여 몇 가지 새로운 패턴을 사용합니다:

1. **`<article>` 태그 범위 추적**: `in_article` 플래그로 기사 영역 안에서만 데이터를 수집합니다.
2. **`featured` 클래스 감지**: `class="news-item featured"`에서 `featured` 포함 여부로 주요 기사를 판별합니다.
3. **여러 줄 텍스트 처리**: `summary`는 HTML에서 여러 줄에 걸쳐 있을 수 있으므로, 기존 텍스트에 이어 붙입니다.
4. **카테고리별 분류**: 수집 후 딕셔너리의 `setdefault()`를 사용하여 카테고리별로 그룹화합니다.

> **Note:** 실제 뉴스 사이트의 HTML 구조는 이보다 훨씬 복잡합니다. 하지만 핵심 원리는 동일합니다: 개발자 도구로 HTML 구조를 분석하고, 패턴에 맞는 파서를 작성하는 것입니다.

---

### 18.10 실전: 상품 정보 수집기

두 번째 실전 프로젝트는 **쇼핑몰 상품 정보 수집기**입니다. 상품명, 가격, 평점, 리뷰 수, 재고 상태를 추출하고, 가격순/평점순 정렬, 필터링, 통계 분석까지 수행합니다.

---

**예제 18-09: 상품 정보 수집기**

```python
# examples/python/chapter04/ex18_09_product_info.py
from html.parser import HTMLParser

SHOP_HTML = """<!DOCTYPE html>
<html>
<body>
    <h1>바이브 코딩 추천 장비</h1>
    <div class="product-list">
        <div class="product-card">
            <img src="/img/keyboard.jpg" alt="기계식 키보드">
            <h3 class="product-name">프로그래머 기계식 키보드</h3>
            <p class="product-price">89,000원</p>
            <p class="product-rating">★★★★★ (4.8/5.0, 리뷰 324개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>
        <!-- ... 더 많은 상품 ... -->
    </div>
</body>
</html>"""


class ProductParser(HTMLParser):
    """쇼핑몰 HTML에서 상품 정보를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.products = []
        self.in_product = False
        self.current_product = {}
        self.current_class = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")

        if tag == "div" and "product-card" in class_value:
            self.in_product = True
            self.current_product = {}

        if self.in_product:
            self.current_class = class_value
            if tag == "img":
                self.current_product["image"] = attrs_dict.get("src", "")

    def handle_endtag(self, tag):
        if tag == "div" and self.in_product and self.current_product:
            if "name" in self.current_product:
                self.products.append(self.current_product)
                self.in_product = False
                self.current_product = {}

    def handle_data(self, data):
        if not self.in_product or not data.strip():
            return

        text = data.strip()
        if "product-name" in self.current_class:
            self.current_product["name"] = text
        elif "product-price" in self.current_class:
            self.current_product["price_text"] = text
            # 숫자만 추출하여 정수로 변환
            price_num = text.replace(",", "").replace("원", "").strip()
            try:
                self.current_product["price"] = int(price_num)
            except ValueError:
                self.current_product["price"] = 0
        elif "product-rating" in self.current_class:
            self.current_product["rating_text"] = text
            # 평점과 리뷰 수 추출
            if "/" in text:
                try:
                    rating_part = text.split("(")[1].split("/")[0]
                    self.current_product["rating"] = float(rating_part)
                except (IndexError, ValueError):
                    self.current_product["rating"] = 0.0
        elif "product-status" in self.current_class:
            self.current_product["status"] = text
            self.current_product["in_stock"] = "in-stock" in self.current_class
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_09_product_info.py
```

**결과:**
```
============================================================
예제 18-09: 상품 정보 수집기
============================================================

총 6개의 상품을 수집했습니다.

--- 상품 목록 ---

  1. 프로그래머 기계식 키보드
     가격: 89,000원
     평점: 4.8 / 5.0 (리뷰 324개)
     상태: ✓ 구매가능

  2. 32인치 4K 코딩 모니터
     가격: 450,000원
     평점: 4.5 / 5.0 (리뷰 189개)
     상태: ✓ 구매가능

  3. 인체공학 버티컬 마우스
     가격: 55,000원
     평점: 4.3 / 5.0 (리뷰 567개)
     상태: ✓ 구매가능

  4. 노이즈캔슬링 코딩 헤드셋
     가격: 199,000원
     평점: 4.9 / 5.0 (리뷰 892개)
     상태: ✗ 품절

  5. 전동 높이조절 스탠딩 데스크
     가격: 320,000원
     평점: 4.6 / 5.0 (리뷰 156개)
     상태: ✓ 구매가능

  6. 프리미엄 인체공학 의자
     가격: 680,000원
     평점: 4.7 / 5.0 (리뷰 445개)
     상태: ✓ 구매가능

--- 가격순 정렬 (낮은 순) ---

       55,000원  인체공학 버티컬 마우스
       89,000원  프로그래머 기계식 키보드
      199,000원  노이즈캔슬링 코딩 헤드셋
      320,000원  전동 높이조절 스탠딩 데스크
      450,000원  32인치 4K 코딩 모니터
      680,000원  프리미엄 인체공학 의자

--- 평점순 정렬 (높은 순) ---

  4.9/5.0  노이즈캔슬링 코딩 헤드셋
  4.8/5.0  프로그래머 기계식 키보드
  4.7/5.0  프리미엄 인체공학 의자
  4.6/5.0  전동 높이조절 스탠딩 데스크
  4.5/5.0  32인치 4K 코딩 모니터
  4.3/5.0  인체공학 버티컬 마우스

--- 구매 가능한 상품 ---

  5개 상품 구매 가능:
  - 프로그래머 기계식 키보드 (89,000원)
  - 32인치 4K 코딩 모니터 (450,000원)
  - 인체공학 버티컬 마우스 (55,000원)
  - 전동 높이조절 스탠딩 데스크 (320,000원)
  - 프리미엄 인체공학 의자 (680,000원)

--- 가격 통계 ---
  최저가: 55,000원
  최고가: 680,000원
  평균가: 298,833원
```

#### 데이터 정제(Cleaning) 기법

상품 파서에서 주목할 점은 **데이터 정제** 과정입니다:

**가격 문자열을 숫자로 변환:**
```python
text = "89,000원"
price_num = text.replace(",", "").replace("원", "").strip()
# "89000"
price = int(price_num)
# 89000
```

**평점 숫자 추출:**
```python
text = "★★★★★ (4.8/5.0, 리뷰 324개)"
rating_part = text.split("(")[1].split("/")[0]
# "4.8"
rating = float(rating_part)
# 4.8
```

**재고 상태 판별:**
```python
# class="product-status in-stock" → 재고 있음
# class="product-status out-of-stock" → 품절
in_stock = "in-stock" in class_value  # True 또는 False
```

이처럼 웹에서 추출한 텍스트 데이터를 프로그램에서 활용하려면 문자열 조작을 통해 적절한 데이터 타입으로 변환해야 합니다.

> **Tip:** `sorted()` 함수와 `lambda`를 사용하면 딕셔너리 리스트를 원하는 기준으로 쉽게 정렬할 수 있습니다: `sorted(products, key=lambda x: x["price"])`

---

### 18.11 스크래핑 결과 저장하기

데이터를 수집했으면 이를 파일로 저장해야 나중에 다시 활용할 수 있습니다. 가장 많이 사용되는 두 가지 형식은 **CSV**와 **JSON**입니다.

| 형식 | 장점 | 적합한 상황 |
|------|------|------------|
| CSV | Excel에서 바로 열 수 있음, 간결함 | 표 형태의 단순한 데이터 |
| JSON | 중첩 구조 지원, 프로그래밍 친화적 | 복잡한 구조의 데이터 |

---

**예제 18-10: 스크래핑 결과 저장**

```python
# examples/python/chapter04/ex18_10_save_results.py
import csv
import json
import os
from html.parser import HTMLParser

BOOKSTORE_HTML = """<!DOCTYPE html>
<html>
<body>
    <h1>바이브 코딩 추천 도서</h1>
    <div class="book-list">
        <div class="book">
            <h3 class="book-title">파이썬 프로그래밍 입문</h3>
            <span class="book-author">김파이 저</span>
            <span class="book-price">25,000원</span>
            <span class="book-publisher">코딩출판사</span>
            <span class="book-year">2025</span>
        </div>
        <!-- ... 더 많은 도서 ... -->
    </div>
</body>
</html>"""


class BookParser(HTMLParser):
    """도서 정보를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.books = []
        self.in_book = False
        self.current_book = {}
        self.current_class = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")
        if tag == "div" and class_value == "book":
            self.in_book = True
            self.current_book = {}
        if self.in_book:
            self.current_class = class_value

    def handle_endtag(self, tag):
        if tag == "div" and self.in_book and "title" in self.current_book:
            self.books.append(self.current_book)
            self.in_book = False
            self.current_book = {}

    def handle_data(self, data):
        if not self.in_book or not data.strip():
            return
        text = data.strip()
        if "book-title" in self.current_class:
            self.current_book["title"] = text
        elif "book-author" in self.current_class:
            self.current_book["author"] = text
        elif "book-price" in self.current_class:
            self.current_book["price"] = text
        elif "book-publisher" in self.current_class:
            self.current_book["publisher"] = text
        elif "book-year" in self.current_class:
            self.current_book["year"] = text


def save_to_csv(data, filename):
    """데이터를 CSV 파일로 저장합니다."""
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    headers = list(data[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV 파일 저장 완료: {filename}")
    print(f"  - {len(data)}개 항목, {len(headers)}개 열")


def save_to_json(data, filename):
    """데이터를 JSON 파일로 저장합니다."""
    output = {
        "total_count": len(data),
        "data": data,
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"JSON 파일 저장 완료: {filename}")
    print(f"  - {len(data)}개 항목")
```

**실행:**
```bash
$ python examples/python/chapter04/ex18_10_save_results.py
```

**결과:**
```
============================================================
예제 18-10: 스크래핑 결과 저장
============================================================

[1단계] HTML에서 데이터 추출 중...

  5개의 도서 정보를 추출했습니다:
  - 파이썬 프로그래밍 입문 (김파이 저)
  - AI와 함께하는 코딩 (이에이 저)
  - 바이브 코딩 완전 정복 (박바이브 저)
  - 웹 개발의 정석 (최웹 저)
  - 데이터 과학 첫걸음 (정데이터 저)

[2단계] CSV 파일로 저장...

CSV 파일 저장 완료: .../outputs/books.csv
  - 5개 항목, 5개 열

[3단계] JSON 파일로 저장...

JSON 파일 저장 완료: .../outputs/books.json
  - 5개 항목

[4단계] 저장된 파일 확인...

--- CSV 파일 내용 ---

  {'title': '파이썬 프로그래밍 입문', 'author': '김파이 저', 'price': '25,000원', ...}
  {'title': 'AI와 함께하는 코딩', 'author': '이에이 저', 'price': '32,000원', ...}
  ...

--- JSON 파일 내용 ---

{
  "total_count": 5,
  "data": [
    {
      "title": "파이썬 프로그래밍 입문",
      "author": "김파이 저",
      "price": "25,000원",
      "publisher": "코딩출판사",
      "year": "2025"
    },
    ...
  ]
}

--- 파일 크기 ---
  CSV:  407 바이트
  JSON: 925 바이트

저장이 완료되었습니다!
CSV 파일은 Excel이나 Google Sheets에서 열 수 있습니다.
JSON 파일은 다른 Python 프로그램에서 바로 불러올 수 있습니다.
```

#### CSV 저장 핵심 코드

```python
import csv

# 딕셔너리 리스트를 CSV로 저장
headers = list(data[0].keys())  # 첫 항목의 키를 헤더로 사용

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()   # 헤더 행 작성
    writer.writerows(data) # 데이터 행들 작성
```

#### JSON 저장 핵심 코드

```python
import json

output = {"total_count": len(data), "data": data}

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False: 한국어가 유니코드 이스케이프 되지 않도록
    # indent=2: 읽기 좋게 들여쓰기
```

> **Note:** `ensure_ascii=False`를 지정하지 않으면 한국어가 `\uD30C\uC774\uC36C`처럼 유니코드 이스케이프 형태로 저장됩니다. 한국어를 그대로 저장하려면 반드시 이 옵션을 사용하세요.

> **Tip:** CSV 파일의 `newline=""`은 Windows에서 빈 줄이 추가되는 문제를 방지합니다. 플랫폼에 관계없이 항상 지정하는 것이 좋습니다.

---

### 18.12 웹 스크래핑 종합 워크플로우

지금까지 배운 내용을 종합하면, 웹 스크래핑의 전체 워크플로우는 다음과 같습니다:

```
┌─────────────────┐
│  1. 대상 분석    │  웹 브라우저 개발자 도구로 HTML 구조 파악
└────────┬────────┘
         ▼
┌─────────────────┐
│  2. HTML 가져오기 │  urllib.request로 페이지 다운로드
└────────┬────────┘
         ▼
┌─────────────────┐
│  3. 파서 작성    │  HTMLParser 서브클래스 구현
└────────┬────────┘
         ▼
┌─────────────────┐
│  4. 데이터 추출  │  태그, 클래스, 속성으로 원하는 데이터 수집
└────────┬────────┘
         ▼
┌─────────────────┐
│  5. 데이터 정제  │  문자열 → 숫자 변환, 공백 제거 등
└────────┬────────┘
         ▼
┌─────────────────┐
│  6. 결과 저장    │  CSV, JSON 등 파일로 저장
└─────────────────┘
```

#### 표준 라이브러리 vs 외부 라이브러리 비교

| 기능 | 표준 라이브러리 | 외부 라이브러리 |
|------|----------------|----------------|
| HTTP 요청 | `urllib.request` | `requests` |
| HTML 파싱 | `html.parser.HTMLParser` | `BeautifulSoup` |
| CSS 선택자 | 직접 구현 필요 | `.select()` 메서드 제공 |
| 학습 가치 | 원리 이해에 탁월 | 실무 생산성에 탁월 |
| 코드 분량 | 상대적으로 많음 | 상대적으로 적음 |
| 설치 | 불필요 (기본 내장) | `pip install` 필요 |

> **Tip:** 이 장에서 표준 라이브러리로 HTML 파싱의 원리를 배웠으므로, 이후 BeautifulSoup이나 requests 같은 외부 라이브러리를 사용할 때 내부 동작을 훨씬 잘 이해할 수 있을 것입니다. 원리를 알고 쓰는 것과 모르고 쓰는 것은 큰 차이입니다.

---

### 18.13 주의사항과 모범 사례

웹 스크래핑을 할 때 반드시 지켜야 할 사항들입니다:

#### 법적/윤리적 주의사항

> **Warning:** 웹 스크래핑은 법적 문제를 야기할 수 있습니다. 다음 사항을 반드시 확인하세요.

1. **robots.txt 확인**: 대부분의 웹사이트는 `https://사이트주소/robots.txt`에 스크래핑 허용 범위를 명시합니다.
2. **이용약관 확인**: 사이트의 이용약관에서 자동 수집을 금지하는지 확인합니다.
3. **적절한 요청 간격**: 서버에 부담을 주지 않도록 요청 사이에 적절한 대기 시간을 둡니다.
4. **개인정보 보호**: 개인정보가 포함된 데이터를 수집하지 않습니다.
5. **상업적 사용 주의**: 수집한 데이터의 상업적 사용은 별도의 허가가 필요할 수 있습니다.

#### 기술적 모범 사례

```python
import time

# 요청 간격 두기 (예: 1초)
time.sleep(1)

# User-Agent 명시하기
headers = {"User-Agent": "학습용 스크래퍼 (연락처: your@email.com)"}

# 에러 처리 항상 포함
try:
    html = fetch_html(url)
except Exception as e:
    print(f"오류: {e}")

# 타임아웃 설정
urllib.request.urlopen(request, timeout=10)
```

---

### 요약

이번 장에서 배운 내용을 정리합니다:

| 주제 | 핵심 내용 | 예제 |
|------|-----------|------|
| HTML 가져오기 | `urllib.request`로 웹 페이지 다운로드 | 예제 18-01 |
| 태그 찾기 | `HTMLParser`로 특정 태그의 텍스트 추출 | 예제 18-02 |
| 클래스 찾기 | `class` 속성으로 요소를 정확히 선택 | 예제 18-03 |
| CSS 선택자 | 태그, 클래스, ID, 속성 기반 선택 패턴 | 예제 18-04 |
| 링크 추출 | `<a>` 태그에서 URL과 텍스트 수집 | 예제 18-05 |
| 테이블 추출 | `<table>` 구조를 딕셔너리 리스트로 변환 | 예제 18-06 |
| 이미지 추출 | `<img>` 태그에서 URL 수집, 상대/절대 경로 변환 | 예제 18-07 |
| 뉴스 수집 | 복합적인 기사 정보 추출 및 분류 | 예제 18-08 |
| 상품 수집 | 가격/평점 데이터 정제 및 분석 | 예제 18-09 |
| 결과 저장 | CSV, JSON 형식으로 파일 저장 | 예제 18-10 |

#### 핵심 패턴 정리

모든 스크래핑 파서의 기본 구조:

```python
from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []        # 결과 저장
        self.in_target = False   # 상태 추적

    def handle_starttag(self, tag, attrs):
        # 시작 태그 처리: 상태 변경, 속성 확인

    def handle_endtag(self, tag):
        # 종료 태그 처리: 결과 저장, 상태 초기화

    def handle_data(self, data):
        # 텍스트 처리: 상태에 따라 데이터 수집

parser = MyParser()
parser.feed(html_string)
# parser.results에서 결과 사용
```

---

### 연습 문제

**연습 1: 기본 파서 만들기**

다음 HTML에서 모든 `<li>` 태그의 텍스트를 추출하는 파서를 작성하세요.

```html
<ul>
    <li>Python 배우기</li>
    <li>HTML 이해하기</li>
    <li>웹 스크래핑 실습하기</li>
</ul>
```

**연습 2: 속성 추출기**

HTML에서 모든 `<a>` 태그의 `href`와 `target` 속성을 함께 추출하는 파서를 작성하세요. `target` 속성이 없는 경우 `"_self"`를 기본값으로 사용하세요.

**연습 3: 폼 데이터 추출기**

다음과 같은 HTML 폼에서 `<input>` 태그의 `name`, `type`, `value` 속성을 추출하는 파서를 작성하세요.

```html
<form>
    <input type="text" name="username" value="">
    <input type="email" name="email" value="">
    <input type="password" name="password" value="">
    <input type="submit" value="가입하기">
</form>
```

**연습 4: 복합 스크래퍼**

뉴스 헤드라인 수집기(예제 18-08)를 확장하여, 수집한 기사를 발행일 기준으로 정렬하고, 특정 키워드(예: "AI")가 포함된 기사만 필터링하는 기능을 추가해보세요.

**연습 5: 완전한 스크래핑 파이프라인**

다음 단계를 모두 포함하는 스크래핑 프로그램을 작성하세요:
1. HTML 문자열에서 데이터 추출 (원하는 주제 자유 선택)
2. 추출한 데이터를 정제 (문자열을 숫자로 변환 등)
3. 데이터를 CSV와 JSON 두 가지 형식으로 저장
4. 저장된 파일을 다시 읽어서 간단한 통계를 출력

> **Tip:** AI 어시스턴트에게 "도서 목록이 있는 HTML을 만들어줘"라고 요청하면 연습용 HTML 데이터를 쉽게 생성할 수 있습니다. 바이브 코딩으로 연습 문제도 풀어보세요!
