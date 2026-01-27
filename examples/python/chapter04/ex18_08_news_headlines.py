"""
예제 18-08: 뉴스 헤드라인 수집기
뉴스 웹사이트의 HTML 구조를 분석하여 헤드라인(제목)과
기사 정보를 추출하는 스크래퍼를 만듭니다.
"""

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

        <article class="news-item">
            <h2 class="headline">오픈소스 AI 모델, 코드 생성 정확도 95% 달성</h2>
            <p class="summary">커뮤니티에서 개발한 오픈소스 AI 모델이 상용 모델에
            버금가는 코드 생성 능력을 보여주고 있다.</p>
            <span class="category">기술</span>
            <span class="author">박오픈 기자</span>
            <time class="published">2025-07-14 15:00</time>
        </article>

        <article class="news-item">
            <h2 class="headline">기업 80%, 향후 2년 내 AI 코딩 도구 도입 예정</h2>
            <p class="summary">글로벌 설문 조사 결과, 대부분의 기업이
            AI 코딩 도구 도입을 계획하고 있는 것으로 확인되었다.</p>
            <span class="category">비즈니스</span>
            <span class="author">최비즈 기자</span>
            <time class="published">2025-07-14 11:00</time>
        </article>

        <article class="news-item">
            <h2 class="headline">자연어 프로그래밍 교육과정, 대학에 신설</h2>
            <p class="summary">주요 대학들이 AI를 활용한 자연어 프로그래밍
            교육과정을 새롭게 개설하기 시작했다.</p>
            <span class="category">교육</span>
            <span class="author">정교육 기자</span>
            <time class="published">2025-07-13 14:00</time>
        </article>
    </section>
</body>
</html>"""


class NewsParser(HTMLParser):
    """뉴스 HTML에서 기사 정보를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.articles = []            # 수집된 기사 목록
        self.in_article = False       # <article> 안인지
        self.is_featured = False      # 주요 기사인지
        self.current_article = {}     # 현재 기사 정보
        self.current_tag = None       # 현재 태그
        self.current_class = ""       # 현재 클래스

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
            # summary는 여러 줄에 걸쳐 있을 수 있음
            existing = self.current_article.get("summary", "")
            self.current_article["summary"] = (existing + " " + text).strip()
        elif self.current_class == "category":
            self.current_article["category"] = text
        elif self.current_class == "author":
            self.current_article["author"] = text
        elif self.current_class == "published":
            self.current_article["published"] = text


# 실행
print("=" * 60)
print("예제 18-08: 뉴스 헤드라인 수집기")
print("=" * 60)

parser = NewsParser()
parser.feed(NEWS_HTML)

print(f"\n총 {len(parser.articles)}개의 기사를 수집했습니다.\n")

# 헤드라인만 출력
print("--- 헤드라인 목록 ---\n")
for i, article in enumerate(parser.articles, 1):
    featured = " ★" if article.get("featured") else ""
    print(f"  {i}. {article.get('headline', '(제목 없음)')}{featured}")

# 상세 정보 출력
print("\n--- 기사 상세 ---\n")
for i, article in enumerate(parser.articles, 1):
    print(f"[{i}] {article.get('headline', '(제목 없음)')}")
    print(f"    카테고리: {article.get('category', '-')}")
    print(f"    기자: {article.get('author', '-')}")
    print(f"    발행일: {article.get('published', '-')}")
    print(f"    요약: {article.get('summary', '-')}")
    if article.get("featured"):
        print("    ★ 주요 기사")
    print()

# 카테고리별 분류
print("--- 카테고리별 분류 ---\n")
categories = {}
for article in parser.articles:
    cat = article.get("category", "기타")
    categories.setdefault(cat, []).append(article.get("headline", ""))

for cat, headlines in sorted(categories.items()):
    print(f"{cat} ({len(headlines)}건):")
    for h in headlines:
        print(f"  - {h}")
