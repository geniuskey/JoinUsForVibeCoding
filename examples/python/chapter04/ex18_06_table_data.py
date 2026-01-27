"""
예제 18-06: 테이블 데이터 추출
HTML <table>에서 데이터를 추출하여 딕셔너리 리스트로 변환합니다.
표 형태의 데이터를 구조화된 Python 데이터로 바꾸는 방법을 배웁니다.
"""

from html.parser import HTMLParser

# 테이블이 포함된 HTML
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
            <tr>
                <td>2</td>
                <td>JavaScript</td>
                <td>20.5%</td>
                <td>웹 프론트엔드, 서버</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Java</td>
                <td>12.3%</td>
                <td>엔터프라이즈, 안드로이드</td>
            </tr>
            <tr>
                <td>4</td>
                <td>TypeScript</td>
                <td>9.7%</td>
                <td>웹 프론트엔드, 서버</td>
            </tr>
            <tr>
                <td>5</td>
                <td>Rust</td>
                <td>5.2%</td>
                <td>시스템 프로그래밍</td>
            </tr>
        </tbody>
    </table>
</body>
</html>"""


class TableParser(HTMLParser):
    """HTML 테이블을 파싱하여 딕셔너리 리스트로 변환하는 파서"""

    def __init__(self):
        super().__init__()
        self.in_table = False     # <table> 안인지
        self.in_thead = False     # <thead> 안인지
        self.in_tbody = False     # <tbody> 안인지
        self.in_tr = False        # <tr> 안인지
        self.in_cell = False      # <td> 또는 <th> 안인지
        self.current_cell = ""    # 현재 셀의 텍스트
        self.current_row = []     # 현재 행의 셀 목록
        self.headers = []         # 헤더 행
        self.rows = []            # 데이터 행들

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


# 실행
print("=" * 50)
print("예제 18-06: 테이블 데이터 추출")
print("=" * 50)

parser = TableParser()
parser.feed(HTML_CONTENT)

# 원시 데이터 출력
print(f"\n헤더: {parser.headers}")
print(f"데이터 행 수: {len(parser.rows)}")

# 딕셔너리 리스트로 변환
data = parser.to_dict_list()

print("\n--- 추출된 데이터 (딕셔너리 리스트) ---\n")
for item in data:
    print(f"  {item}")

# 표 형태로 보기 좋게 출력
print("\n--- 정리된 표 ---\n")
print(f"{'순위':>4} | {'언어':<12} | {'점유율':>6} | {'주요 용도'}")
print("-" * 55)
for item in data:
    print(f"{item['순위']:>4} | {item['언어']:<12} | {item['점유율']:>6} | {item['주요 용도']}")

# 특정 조건으로 필터링
print("\n--- 점유율 10% 이상 언어 ---")
for item in data:
    rate = float(item["점유율"].replace("%", ""))
    if rate >= 10.0:
        print(f"  {item['언어']}: {item['점유율']}")
