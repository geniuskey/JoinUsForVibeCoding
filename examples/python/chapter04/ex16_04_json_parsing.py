#!/usr/bin/env python3
"""예제 16-04: JSON 파싱

JSON 문자열을 파싱하고 필요한 필드를 추출합니다.
"""

import json

# JSON 데이터를 코드 내에 직접 정의
json_string = '''
{
    "서점": "바이브 북스",
    "위치": "서울 강남구",
    "개업일": "2024-03-15",
    "도서목록": [
        {
            "제목": "파이썬 입문",
            "저자": "김개발",
            "가격": 28000,
            "재고": 45,
            "장르": "프로그래밍"
        },
        {
            "제목": "AI 시대의 코딩",
            "저자": "이미래",
            "가격": 32000,
            "재고": 30,
            "장르": "프로그래밍"
        },
        {
            "제목": "데이터 과학 기초",
            "저자": "박분석",
            "가격": 35000,
            "재고": 20,
            "장르": "데이터"
        },
        {
            "제목": "웹 개발 실전",
            "저자": "최풀스택",
            "가격": 30000,
            "재고": 38,
            "장르": "웹개발"
        }
    ]
}
'''

# JSON 파싱
data = json.loads(json_string)

# 기본 정보 출력
print("=" * 40)
print(f"  서점명 : {data['서점']}")
print(f"  위치   : {data['위치']}")
print(f"  개업일 : {data['개업일']}")
print("=" * 40)

# 도서 목록 출력
books = data["도서목록"]
print(f"\n보유 도서: 총 {len(books)}권\n")
print(f"{'번호':>4}  {'제목':<16} {'저자':<8} {'가격':>8} {'재고':>4}")
print("-" * 48)
for i, book in enumerate(books, 1):
    price_str = f"{book['가격']:,}원"
    print(f"{i:>4}  {book['제목']:<16} {book['저자']:<8} {price_str:>8} {book['재고']:>4}")

# 통계 정보
prices = [b["가격"] for b in books]
stocks = [b["재고"] for b in books]
total_value = sum(b["가격"] * b["재고"] for b in books)

print(f"\n[도서 통계]")
print(f"  평균 가격    : {sum(prices) / len(prices):,.0f}원")
print(f"  최고가 도서  : {max(books, key=lambda b: b['가격'])['제목']}")
print(f"  총 재고 수량 : {sum(stocks)}권")
print(f"  총 재고 가치 : {total_value:,}원")

# JSON으로 다시 변환 (예쁘게 출력)
print(f"\n[가장 비싼 도서 JSON]")
most_expensive = max(books, key=lambda b: b["가격"])
print(json.dumps(most_expensive, ensure_ascii=False, indent=2))
