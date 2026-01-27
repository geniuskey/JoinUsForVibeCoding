#!/usr/bin/env python3
"""예제 16-03: CSV 정렬

다양한 기준으로 데이터를 정렬합니다.
"""

import csv
import io

# 제품 판매 데이터
csv_data = """제품명,카테고리,가격,판매량
무선 마우스,전자기기,25000,150
기계식 키보드,전자기기,89000,85
USB 허브,전자기기,15000,200
노트 세트,문구류,8000,320
볼펜 10개입,문구류,5000,450
텀블러,생활용품,18000,175
에코백,생활용품,12000,280
마우스패드,전자기기,9000,190
형광펜 세트,문구류,6500,310
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

def print_table(title, data, columns):
    """표 형식으로 데이터 출력"""
    print(f"\n[{title}]")
    header = f"{'순위':>4}"
    for col, width, align in columns:
        if align == "left":
            header += f"  {col:<{width}}"
        else:
            header += f"  {col:>{width}}"
    print(header)
    print("-" * (len(header) + 2))
    for i, row in enumerate(data, 1):
        line = f"{i:>4}"
        for col, width, align in columns:
            val = row[col]
            if align == "left":
                line += f"  {val:<{width}}"
            else:
                line += f"  {val:>{width}}"
        print(line)

# 정렬 1: 가격 내림차순
by_price = sorted(records, key=lambda x: int(x["가격"]), reverse=True)
print_table(
    "가격 높은 순",
    by_price,
    [("제품명", 14, "left"), ("가격", 8, "right"), ("카테고리", 8, "left")]
)

# 정렬 2: 판매량 내림차순
by_sales = sorted(records, key=lambda x: int(x["판매량"]), reverse=True)
print_table(
    "판매량 많은 순",
    by_sales,
    [("제품명", 14, "left"), ("판매량", 6, "right"), ("카테고리", 8, "left")]
)

# 정렬 3: 카테고리별 → 가격순 (다중 정렬)
by_category_price = sorted(
    records,
    key=lambda x: (x["카테고리"], int(x["가격"]))
)
print_table(
    "카테고리별 → 가격 오름차순",
    by_category_price,
    [("카테고리", 8, "left"), ("제품명", 14, "left"), ("가격", 8, "right")]
)

# 매출액(가격 × 판매량) 기준 정렬
for r in records:
    r["매출액"] = int(r["가격"]) * int(r["판매량"])

by_revenue = sorted(records, key=lambda x: x["매출액"], reverse=True)
print(f"\n[매출액 기준 상위 5개]")
print(f"{'순위':>4}  {'제품명':<14}  {'매출액':>12}")
print("-" * 36)
for i, row in enumerate(by_revenue[:5], 1):
    revenue_str = f"{row['매출액']:,}원"
    print(f"{i:>4}  {row['제품명']:<14}  {revenue_str:>12}")
