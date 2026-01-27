"""
예제 18-04: CSS 선택자 개념
CSS 선택자의 종류와 의미를 이해하고,
HTMLParser를 사용하여 선택자 개념을 직접 구현해봅니다.
"""

from html.parser import HTMLParser

# 다양한 속성을 가진 HTML
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

# CSS 선택자 개념 설명
print("=" * 50)
print("예제 18-04: CSS 선택자 개념")
print("=" * 50)

print("""
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
""")


class SelectorParser(HTMLParser):
    """CSS 선택자 개념을 구현한 간단한 파서"""

    def __init__(self):
        super().__init__()
        self.elements = []       # 모든 요소 정보 저장
        self._current = None     # 현재 처리 중인 요소
        self._depth = 0          # 태그 깊이 추적

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


# 파싱 실행
parser = SelectorParser()
parser.feed(HTML_CONTENT)

# 다양한 선택자 테스트
print("--- 선택자 실습 ---\n")

# 1. 태그 선택자
results = parser.select_by_tag("p")
print(f'선택자: p  →  {len(results)}개 발견')
for r in results:
    print(f'  "{r["text"]}"')

# 2. 클래스 선택자
print()
results = parser.select_by_class("active")
print(f'선택자: .active  →  {len(results)}개 발견')
for r in results:
    print(f'  "{r["text"]}"')

# 3. 아이디 선택자
print()
results = parser.select_by_id("main-content")
print(f'선택자: #main-content  →  {len(results)}개 발견')
for r in results:
    print(f'  "{r["text"]}"')

# 4. 태그 + 클래스 조합
print()
results = parser.select_by_tag_and_class("li", "active")
print(f'선택자: li.active  →  {len(results)}개 발견')
for r in results:
    print(f'  "{r["text"]}"')

# 5. 속성 선택자
print()
results = parser.select_by_attribute("href")
print(f'선택자: [href]  →  {len(results)}개 발견')
for r in results:
    print(f'  "{r["text"]}" → {r["attrs"]["href"]}')
