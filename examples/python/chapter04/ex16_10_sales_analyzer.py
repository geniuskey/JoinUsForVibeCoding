#!/usr/bin/env python3
"""예제 16-10: 판매 데이터 분석기

월별 판매 데이터를 종합 분석하고 요약 리포트를 생성합니다.
"""

import csv
import io
import statistics
from collections import defaultdict

# 월별 판매 데이터
csv_data = """월,제품,카테고리,판매수량,단가
1월,노트북,전자,45,1200000
1월,마우스,전자,120,35000
1월,파이썬 책,도서,80,28000
2월,노트북,전자,38,1200000
2월,마우스,전자,95,35000
2월,파이썬 책,도서,65,28000
3월,노트북,전자,52,1200000
3월,마우스,전자,140,35000
3월,파이썬 책,도서,90,28000
4월,노트북,전자,60,1200000
4월,마우스,전자,155,35000
4월,파이썬 책,도서,75,28000
5월,노트북,전자,48,1200000
5월,마우스,전자,130,35000
5월,파이썬 책,도서,110,28000
6월,노트북,전자,55,1200000
6월,마우스,전자,145,35000
6월,파이썬 책,도서,95,28000
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

# 매출액 계산
for r in records:
    r["매출액"] = int(r["판매수량"]) * int(r["단가"])

# ===== 월별 총매출 분석 =====
monthly_revenue = defaultdict(int)
for r in records:
    monthly_revenue[r["월"]] += r["매출액"]

months_order = ["1월", "2월", "3월", "4월", "5월", "6월"]
monthly_values = [monthly_revenue[m] for m in months_order]

print("╔" + "═" * 58 + "╗")
print("║" + "판매 데이터 종합 분석 리포트".center(46) + "║")
print("╚" + "═" * 58 + "╝")

print("\n[1] 월별 총매출")
print(f"{'월':>4} {'매출액':>14} {'그래프'}")
print("-" * 55)
max_monthly = max(monthly_values)
for month in months_order:
    rev = monthly_revenue[month]
    bar_len = int(rev / max_monthly * 30)
    bar = "█" * bar_len
    print(f"{month:>4} {rev:>12,}원 {bar}")

# 전월 대비 증감
print(f"\n[2] 전월 대비 증감")
print(f"{'월':>4} {'매출액':>14} {'증감액':>14} {'증감률':>8}")
print("-" * 48)
for i, month in enumerate(months_order):
    rev = monthly_values[i]
    if i == 0:
        print(f"{month:>4} {rev:>12,}원 {'-':>14} {'-':>8}")
    else:
        diff = rev - monthly_values[i - 1]
        pct = diff / monthly_values[i - 1] * 100
        sign = "+" if diff >= 0 else ""
        print(f"{month:>4} {rev:>12,}원 {sign}{diff:>12,}원 {sign}{pct:>5.1f}%")

# ===== 제품별 분석 =====
product_stats = defaultdict(lambda: {"총수량": 0, "총매출": 0, "월별매출": []})
for r in records:
    product = r["제품"]
    product_stats[product]["총수량"] += int(r["판매수량"])
    product_stats[product]["총매출"] += r["매출액"]
    product_stats[product]["월별매출"].append(r["매출액"])

print(f"\n[3] 제품별 실적")
print(f"{'제품':<12} {'총수량':>8} {'총매출':>14} {'월평균':>14}")
print("-" * 55)
total_revenue = 0
for product, stats in sorted(product_stats.items(), key=lambda x: x[1]["총매출"], reverse=True):
    avg_monthly = statistics.mean(stats["월별매출"])
    total_revenue += stats["총매출"]
    print(f"{product:<12} {stats['총수량']:>8} {stats['총매출']:>12,}원 {avg_monthly:>12,.0f}원")
print("-" * 55)
print(f"{'합계':<12} {'':>8} {total_revenue:>12,}원")

# ===== 베스트/워스트 분석 =====
print(f"\n[4] 하이라이트")
best_month = max(months_order, key=lambda m: monthly_revenue[m])
worst_month = min(months_order, key=lambda m: monthly_revenue[m])
best_product = max(product_stats.items(), key=lambda x: x[1]["총매출"])

print(f"  ★ 최고 매출 월  : {best_month} ({monthly_revenue[best_month]:,}원)")
print(f"  ▽ 최저 매출 월  : {worst_month} ({monthly_revenue[worst_month]:,}원)")
print(f"  ★ 최고 매출 제품: {best_product[0]} ({best_product[1]['총매출']:,}원)")
print(f"  ◎ 총 매출      : {total_revenue:,}원")
print(f"  ◎ 월 평균 매출  : {total_revenue // len(months_order):,}원")

# ===== 카테고리 비중 =====
cat_revenue = defaultdict(int)
for r in records:
    cat_revenue[r["카테고리"]] += r["매출액"]

print(f"\n[5] 카테고리별 매출 비중")
for cat, rev in sorted(cat_revenue.items(), key=lambda x: x[1], reverse=True):
    pct = rev / total_revenue * 100
    filled = int(pct / 100 * 30)
    bar = "█" * filled + "░" * (30 - filled)
    print(f"  {cat:<6} {bar} {pct:.1f}% ({rev:,}원)")
