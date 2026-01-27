"""
예제 18-03: 클래스로 요소 찾기
HTML 요소의 class 속성을 기준으로 원하는 요소를 찾는 방법을 배웁니다.
웹 페이지에서 특정 스타일이 적용된 요소만 골라내는 데 유용합니다.
"""

from html.parser import HTMLParser

# class 속성이 포함된 HTML
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
        <p class="copyright">© 2025 바이브 코딩</p>
    </div>
</body>
</html>"""


class ClassFinder(HTMLParser):
    """특정 class를 가진 요소의 텍스트를 수집하는 파서"""

    def __init__(self, target_class):
        super().__init__()
        self.target_class = target_class  # 찾을 class 이름
        self.is_matching = False          # 현재 태그가 매칭되는지
        self.results = []                 # 결과 목록
        self.current_tag = None           # 현재 태그 이름

    def handle_starttag(self, tag, attrs):
        """시작 태그에서 class 속성을 확인합니다."""
        # attrs는 (속성이름, 값) 튜플의 리스트
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")

        # class 속성에 target_class가 포함되어 있는지 확인
        # class="title main-title"처럼 여러 클래스가 있을 수 있음
        class_list = class_value.split()
        if self.target_class in class_list:
            self.is_matching = True
            self.current_tag = tag

    def handle_endtag(self, tag):
        """종료 태그를 만나면 매칭 상태를 해제합니다."""
        if tag == self.current_tag and self.is_matching:
            self.is_matching = False
            self.current_tag = None

    def handle_data(self, data):
        """매칭된 태그의 텍스트를 수집합니다."""
        if self.is_matching and data.strip():
            self.results.append(data.strip())


# 실행
print("=" * 50)
print("예제 18-03: 클래스로 요소 찾기")
print("=" * 50)

# 다양한 클래스로 검색
search_classes = ["highlight", "intro", "title", "copyright"]

for class_name in search_classes:
    finder = ClassFinder(class_name)
    finder.feed(HTML_CONTENT)

    print(f"\nclass=\"{class_name}\" 요소 ({len(finder.results)}개):")
    if finder.results:
        for i, text in enumerate(finder.results, 1):
            print(f"  {i}. {text}")
    else:
        print("  (발견되지 않음)")

# 모든 클래스 목록 추출
print("\n--- HTML에 사용된 모든 클래스 ---")


class AllClassCollector(HTMLParser):
    """HTML에서 사용된 모든 class 이름을 수집합니다."""

    def __init__(self):
        super().__init__()
        self.classes = set()

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")
        for cls in class_value.split():
            if cls:
                self.classes.add(cls)


collector = AllClassCollector()
collector.feed(HTML_CONTENT)
for cls in sorted(collector.classes):
    print(f"  - {cls}")
