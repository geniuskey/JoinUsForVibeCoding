#!/usr/bin/env python3
"""예제 16-08: 그룹별 집계

카테고리별로 데이터를 그룹화하고 합계, 평균, 개수를 계산합니다.
"""

import csv
import io
from collections import defaultdict

# 온라인 쇼핑몰 주문 데이터
csv_data = """주문ID,상품명,카테고리,수량,단가,지역
O001,노트북,전자기기,1,1200000,서울
O002,마우스,전자기기,2,35000,부산
O003,파이썬 입문서,도서,3,28000,서울
O004,모니터,전자기기,1,450000,대전
O005,알고리즘 책,도서,1,32000,서울
O006,키보드,전자기기,1,89000,부산
O007,텀블러,생활용품,4,18000,대구
O008,데이터과학 입문,도서,2,35000,대전
O009,USB 허브,전자기기,3,15000,서울
O010,노트 세트,생활용품,5,8000,부산
O011,웹개발 책,도서,1,30000,대구
O012,에코백,생활용품,2,12000,서울
O013,헤드셋,전자기기,1,65000,대전
O014,연필 세트,생활용품,3,5000,부산
O015,AI 입문서,도서,2,33000,서울
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

# 매출액 계산
for r in records:
    r["매출액"] = int(r["수량"]) * int(r["단가"])

# === 카테고리별 집계 ===
cat_stats = defaultdict(lambda: {"주문수": 0, "총수량": 0, "총매출": 0, "상품목록": []})

for r in records:
    cat = r["카테고리"]
    cat_stats[cat]["주문수"] += 1
    cat_stats[cat]["총수량"] += int(r["수량"])
    cat_stats[cat]["총매출"] += r["매출액"]
    cat_stats[cat]["상품목록"].append(r["상품명"])

print("=" * 55)
print("  카테고리별 집계")
print("=" * 55)
print(f"{'카테고리':<10} {'주문수':>6} {'총수량':>6} {'총매출':>14}")
print("-" * 55)
for cat, stats in sorted(cat_stats.items(), key=lambda x: x[1]["총매출"], reverse=True):
    print(f"{cat:<10} {stats['주문수']:>6} {stats['총수량']:>6} {stats['총매출']:>12,}원")
print("-" * 55)
total_revenue = sum(s["총매출"] for s in cat_stats.values())
total_orders = sum(s["주문수"] for s in cat_stats.values())
print(f"{'합계':<10} {total_orders:>6} {'':>6} {total_revenue:>12,}원")

# === 지역별 집계 ===
region_stats = defaultdict(lambda: {"주문수": 0, "총매출": 0})

for r in records:
    region = r["지역"]
    region_stats[region]["주문수"] += 1
    region_stats[region]["총매출"] += r["매출액"]

print(f"\n{'=' * 40}")
print("  지역별 집계")
print("=" * 40)
print(f"{'지역':<6} {'주문수':>6} {'총매출':>14} {'비율':>8}")
print("-" * 40)
for region, stats in sorted(region_stats.items(), key=lambda x: x[1]["총매출"], reverse=True):
    ratio = stats["총매출"] / total_revenue * 100
    print(f"{region:<6} {stats['주문수']:>6} {stats['총매출']:>12,}원 {ratio:>6.1f}%")

# === 카테고리 × 지역 교차 집계 ===
cross_stats = defaultdict(lambda: defaultdict(int))
for r in records:
    cross_stats[r["카테고리"]][r["지역"]] += r["매출액"]

regions = sorted(region_stats.keys())
print(f"\n{'=' * 60}")
print("  카테고리 × 지역 교차 집계 (매출액)")
print("=" * 60)
header = f"{'카테고리':<10}"
for region in regions:
    header += f" {region:>10}"
header += f" {'합계':>12}"
print(header)
print("-" * 60)
for cat in sorted(cat_stats.keys()):
    line = f"{cat:<10}"
    row_total = 0
    for region in regions:
        val = cross_stats[cat][region]
        row_total += val
        line += f" {val:>9,}" if val > 0 else f" {'-':>10}"
    line += f" {row_total:>11,}"
    print(line)
