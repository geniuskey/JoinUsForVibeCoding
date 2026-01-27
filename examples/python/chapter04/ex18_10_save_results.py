"""
예제 18-10: 스크래핑 결과 저장
추출한 데이터를 CSV 파일과 JSON 파일로 저장하는 방법을 배웁니다.
수집한 데이터를 영구적으로 보관하고 다른 프로그램에서 활용할 수 있게 합니다.
"""

import csv
import json
import os
from html.parser import HTMLParser

# 스크래핑할 HTML 데이터 (도서 목록)
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
        <div class="book">
            <h3 class="book-title">AI와 함께하는 코딩</h3>
            <span class="book-author">이에이 저</span>
            <span class="book-price">32,000원</span>
            <span class="book-publisher">미래출판</span>
            <span class="book-year">2025</span>
        </div>
        <div class="book">
            <h3 class="book-title">바이브 코딩 완전 정복</h3>
            <span class="book-author">박바이브 저</span>
            <span class="book-price">28,000원</span>
            <span class="book-publisher">코딩출판사</span>
            <span class="book-year">2024</span>
        </div>
        <div class="book">
            <h3 class="book-title">웹 개발의 정석</h3>
            <span class="book-author">최웹 저</span>
            <span class="book-price">35,000원</span>
            <span class="book-publisher">테크북스</span>
            <span class="book-year">2024</span>
        </div>
        <div class="book">
            <h3 class="book-title">데이터 과학 첫걸음</h3>
            <span class="book-author">정데이터 저</span>
            <span class="book-price">30,000원</span>
            <span class="book-publisher">미래출판</span>
            <span class="book-year">2025</span>
        </div>
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

    # 첫 번째 항목의 키를 헤더로 사용
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


def load_and_display_csv(filename):
    """저장된 CSV 파일을 읽어서 표시합니다."""
    print(f"\n--- CSV 파일 내용: {filename} ---\n")

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"  {row}")


def load_and_display_json(filename):
    """저장된 JSON 파일을 읽어서 표시합니다."""
    print(f"\n--- JSON 파일 내용: {filename} ---\n")

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(json.dumps(data, ensure_ascii=False, indent=2))


# 실행
print("=" * 60)
print("예제 18-10: 스크래핑 결과 저장")
print("=" * 60)

# 1단계: HTML 파싱
print("\n[1단계] HTML에서 데이터 추출 중...\n")
parser = BookParser()
parser.feed(BOOKSTORE_HTML)

print(f"  {len(parser.books)}개의 도서 정보를 추출했습니다:")
for book in parser.books:
    print(f"  - {book['title']} ({book['author']})")

# 2단계: 저장 디렉토리 준비
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "outputs")
os.makedirs(output_dir, exist_ok=True)

csv_file = os.path.join(output_dir, "books.csv")
json_file = os.path.join(output_dir, "books.json")

# 3단계: CSV로 저장
print("\n[2단계] CSV 파일로 저장...\n")
save_to_csv(parser.books, csv_file)

# 4단계: JSON으로 저장
print("\n[3단계] JSON 파일로 저장...\n")
save_to_json(parser.books, json_file)

# 5단계: 저장된 파일 확인
print("\n[4단계] 저장된 파일 확인...\n")

# CSV 파일 내용 확인
load_and_display_csv(csv_file)

# JSON 파일 내용 확인
load_and_display_json(json_file)

# 파일 크기 정보
print("\n--- 파일 크기 ---")
csv_size = os.path.getsize(csv_file)
json_size = os.path.getsize(json_file)
print(f"  CSV:  {csv_size:,} 바이트 ({csv_file})")
print(f"  JSON: {json_size:,} 바이트 ({json_file})")

print("\n저장이 완료되었습니다!")
print("CSV 파일은 Excel이나 Google Sheets에서 열 수 있습니다.")
print("JSON 파일은 다른 Python 프로그램에서 바로 불러올 수 있습니다.")
