"""
예제 18-02: 태그로 요소 찾기
HTMLParser를 사용하여 HTML 문자열에서 특정 태그의 내용을 추출합니다.
<h1>, <p> 등 원하는 태그를 찾아 텍스트를 수집하는 방법을 배웁니다.
"""

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


# 실행
print("=" * 50)
print("예제 18-02: 태그로 요소 찾기")
print("=" * 50)

# h1, h2, p 태그를 찾는 파서 생성
finder = TagFinder(["h1", "h2", "p"])
finder.feed(HTML_CONTENT)

# 결과 출력
for tag, texts in finder.results.items():
    print(f"\n<{tag}> 태그 ({len(texts)}개 발견):")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")

# 전체 요약
print("\n--- 요약 ---")
total = sum(len(v) for v in finder.results.values())
print(f"총 {total}개의 요소를 찾았습니다.")
