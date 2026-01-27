"""
예제 18-05: 링크 추출하기
HTML에서 모든 <a href="..."> 태그를 찾아 링크를 추출합니다.
링크 텍스트와 URL을 함께 수집하는 방법을 배웁니다.
"""

from html.parser import HTMLParser

# 다양한 링크가 포함된 HTML
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
        self.links = []           # 추출된 링크 목록
        self.current_href = None  # 현재 링크의 href
        self.current_attrs = {}   # 현재 링크의 모든 속성
        self.current_text = ""    # 현재 링크의 텍스트
        self.in_a_tag = False     # <a> 태그 안인지 여부

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
print("=" * 50)
print("예제 18-05: 링크 추출하기")
print("=" * 50)

extractor = LinkExtractor()
extractor.feed(HTML_CONTENT)

# 모든 링크 출력
print(f"\n총 {len(extractor.links)}개의 링크를 발견했습니다:\n")
for i, link in enumerate(extractor.links, 1):
    print(f"  {i:2d}. [{link['text']}] → {link['href']}")

# 링크 유형별 분류
print("\n--- 링크 유형별 분류 ---\n")

internal_links = []   # 내부 링크 (상대 경로)
external_links = []   # 외부 링크 (http/https)
mail_links = []       # 메일 링크 (mailto:)

for link in extractor.links:
    href = link["href"]
    if href.startswith("mailto:"):
        mail_links.append(link)
    elif href.startswith("http://") or href.startswith("https://"):
        external_links.append(link)
    else:
        internal_links.append(link)

print(f"내부 링크 ({len(internal_links)}개):")
for link in internal_links:
    print(f"  - [{link['text']}] → {link['href']}")

print(f"\n외부 링크 ({len(external_links)}개):")
for link in external_links:
    print(f"  - [{link['text']}] → {link['href']}")

print(f"\n메일 링크 ({len(mail_links)}개):")
for link in mail_links:
    print(f"  - [{link['text']}] → {link['href']}")
