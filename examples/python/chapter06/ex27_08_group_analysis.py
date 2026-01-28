"""
예제 27-08: 그룹별 분석 (카테고리별 집계 및 분석)

데이터를 다양한 기준으로 그룹화하고 그룹별 통계를 계산합니다.
카테고리별, 지역별, 기간별 분석을 통해 비즈니스 인사이트를 도출합니다.
"""

import random
import datetime
import statistics
from collections import defaultdict


def generate_sample_data():
    """분석용 샘플 판매 데이터를 생성합니다."""

    random.seed(42)
    data = []

    products = [
        ("무선 키보드", "전자기기", 35000),
        ("블루투스 마우스", "전자기기", 25000),
        ("모니터 거치대", "사무용품", 32000),
        ("노트북 파우치", "액세서리", 22000),
        ("USB 허브", "전자기기", 18000),
        ("헤드셋", "전자기기", 55000),
        ("마우스패드", "액세서리", 12000),
        ("책상 정리함", "사무용품", 28000),
        ("노트북 스탠드", "사무용품", 42000),
        ("충전 케이블", "액세서리", 8000),
    ]
    regions = ["서울", "경기", "부산", "대구", "인천"]
    grades = ["일반", "실버", "골드", "VIP"]

    for i in range(300):
        name, category, base_price = random.choice(products)
        qty = random.randint(1, 10)
        price = base_price + random.randint(-3000, 5000)
        date = datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 180))
        grade = random.choices(grades, weights=[40, 30, 20, 10], k=1)[0]

        data.append({
            "상품명": name,
            "카테고리": category,
            "수량": qty,
            "단가": price,
            "총액": price * qty,
            "지역": random.choice(regions),
            "고객등급": grade,
            "날짜": date.strftime("%Y-%m-%d"),
            "월": date.month,
        })

    return data


def group_by(data, key_field):
    """데이터를 특정 필드 기준으로 그룹화합니다."""

    groups = defaultdict(list)
    for record in data:
        groups[record[key_field]].append(record)
    return dict(groups)


def group_stats(data, group_field, value_field):
    """그룹별 통계를 계산합니다."""

    groups = group_by(data, group_field)
    results = {}

    for group_name, records in groups.items():
        values = [r[value_field] for r in records]
        results[group_name] = {
            "건수": len(values),
            "합계": sum(values),
            "평균": statistics.mean(values),
            "중앙값": statistics.median(values),
            "최솟값": min(values),
            "최댓값": max(values),
            "표준편차": statistics.stdev(values) if len(values) >= 2 else 0,
        }

    return results


def top_n_by_group(data, group_field, value_field, n=3, ascending=False):
    """그룹별 상위/하위 N개 항목을 추출합니다."""

    groups = group_by(data, group_field)
    results = {}

    for group_name, records in groups.items():
        sorted_records = sorted(
            records,
            key=lambda x: x[value_field],
            reverse=not ascending
        )
        results[group_name] = sorted_records[:n]

    return results


def cross_tabulation(data, row_field, col_field, value_field="총액", agg="sum"):
    """교차 분석(크로스 탭)을 수행합니다."""

    cross = defaultdict(lambda: defaultdict(list))
    col_values = set()

    for record in data:
        row_key = record[row_field]
        col_key = record[col_field]
        col_values.add(col_key)
        cross[row_key][col_key].append(record[value_field])

    # 집계
    result = {}
    for row_key in cross:
        result[row_key] = {}
        for col_key in sorted(col_values):
            vals = cross[row_key].get(col_key, [])
            if not vals:
                result[row_key][col_key] = 0
            elif agg == "sum":
                result[row_key][col_key] = sum(vals)
            elif agg == "count":
                result[row_key][col_key] = len(vals)
            elif agg == "mean":
                result[row_key][col_key] = sum(vals) / len(vals)

    return result, sorted(col_values)


def growth_analysis(data, period_field="월", value_field="총액"):
    """기간별 성장률을 분석합니다."""

    # 기간별 합계
    period_totals = defaultdict(float)
    for record in data:
        period_totals[record[period_field]] += record[value_field]

    sorted_periods = sorted(period_totals.keys())

    results = []
    prev_value = None
    for period in sorted_periods:
        current = period_totals[period]
        growth = None
        if prev_value is not None and prev_value != 0:
            growth = (current - prev_value) / prev_value * 100

        results.append({
            "기간": period,
            "매출": current,
            "성장률": growth,
        })
        prev_value = current

    return results


def pareto_analysis(data, group_field, value_field="총액"):
    """파레토 분석 (80/20 법칙)을 수행합니다."""

    # 그룹별 합계
    group_totals = defaultdict(float)
    for record in data:
        group_totals[record[group_field]] += record[value_field]

    # 내림차순 정렬
    sorted_groups = sorted(group_totals.items(), key=lambda x: -x[1])
    grand_total = sum(v for _, v in sorted_groups)

    results = []
    cumulative = 0
    for name, total in sorted_groups:
        cumulative += total
        cum_pct = cumulative / grand_total * 100
        pct = total / grand_total * 100
        results.append({
            "항목": name,
            "매출": total,
            "비율": pct,
            "누적비율": cum_pct,
        })

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("  그룹별 데이터 분석")
    print("=" * 60)

    data = generate_sample_data()
    print(f"\n데이터: {len(data)}개 판매 레코드")

    # 1. 카테고리별 통계
    print("\n" + "=" * 60)
    print("  1. 카테고리별 매출 통계")
    print("=" * 60)

    cat_stats = group_stats(data, "카테고리", "총액")
    print(f"\n{'카테고리':>8s} | {'건수':>5s} | {'합계':>12s} | {'평균':>10s} | {'표준편차':>10s}")
    print("-" * 65)

    for cat in sorted(cat_stats.keys()):
        s = cat_stats[cat]
        print(f"{cat:>8s} | {s['건수']:>5d} | {s['합계']:>12,.0f} | "
              f"{s['평균']:>10,.0f} | {s['표준편차']:>10,.0f}")

    # 2. 지역별 통계
    print("\n" + "=" * 60)
    print("  2. 지역별 매출 분석")
    print("=" * 60)

    region_stats = group_stats(data, "지역", "총액")
    total_sales = sum(s["합계"] for s in region_stats.values())

    print(f"\n{'지역':>6s} | {'건수':>5s} | {'합계':>12s} | {'비율':>6s} | {'평균':>10s}")
    print("-" * 55)

    for region in sorted(region_stats.keys(), key=lambda x: -region_stats[x]["합계"]):
        s = region_stats[region]
        pct = s["합계"] / total_sales * 100
        print(f"{region:>6s} | {s['건수']:>5d} | {s['합계']:>12,.0f} | "
              f"{pct:>5.1f}% | {s['평균']:>10,.0f}")

    # 3. 고객등급별 분석
    print("\n" + "=" * 60)
    print("  3. 고객 등급별 분석")
    print("=" * 60)

    grade_stats = group_stats(data, "고객등급", "총액")
    grade_order = ["일반", "실버", "골드", "VIP"]

    print(f"\n{'등급':>6s} | {'고객수':>6s} | {'총매출':>12s} | {'객단가':>10s} | {'최고거래':>10s}")
    print("-" * 60)

    for grade in grade_order:
        if grade in grade_stats:
            s = grade_stats[grade]
            print(f"{grade:>6s} | {s['건수']:>6d} | {s['합계']:>12,.0f} | "
                  f"{s['평균']:>10,.0f} | {s['최댓값']:>10,.0f}")

    # 4. 교차 분석 (지역 x 카테고리)
    print("\n" + "=" * 60)
    print("  4. 교차 분석 (지역 x 카테고리 매출)")
    print("=" * 60)

    cross, cols = cross_tabulation(data, "지역", "카테고리", "총액", "sum")

    # 헤더
    header = f"\n{'지역':>6s}"
    for col in cols:
        header += f" | {col:>10s}"
    print(header)
    print("-" * (8 + 13 * len(cols)))

    for region in sorted(cross.keys()):
        line = f"{region:>6s}"
        for col in cols:
            line += f" | {cross[region].get(col, 0):>10,.0f}"
        print(line)

    # 5. 월별 성장률 분석
    print("\n" + "=" * 60)
    print("  5. 월별 매출 성장률")
    print("=" * 60)

    growth = growth_analysis(data, "월", "총액")

    print(f"\n{'월':>4s} | {'매출':>12s} | {'성장률':>8s} | 추세")
    print("-" * 50)

    for g in growth:
        growth_str = f"{g['성장률']:>+7.1f}%" if g['성장률'] is not None else "    -  "
        trend = ""
        if g['성장률'] is not None:
            if g['성장률'] > 10:
                trend = "++ 크게 상승"
            elif g['성장률'] > 0:
                trend = "+  소폭 상승"
            elif g['성장률'] > -10:
                trend = "-  소폭 하락"
            else:
                trend = "-- 크게 하락"
        print(f"{g['기간']:>4d} | {g['매출']:>12,.0f} | {growth_str} | {trend}")

    # 6. 파레토 분석
    print("\n" + "=" * 60)
    print("  6. 파레토 분석 (상품별 매출)")
    print("=" * 60)

    pareto = pareto_analysis(data, "상품명", "총액")

    print(f"\n{'순위':>4s} | {'상품명':>14s} | {'매출':>12s} | {'비율':>6s} | {'누적':>6s} | 그래프")
    print("-" * 75)

    for i, p in enumerate(pareto, 1):
        bar = "#" * int(p["비율"] / 2)
        marker = " <-- 80%" if p["누적비율"] >= 80 and (i == 1 or pareto[i-2]["누적비율"] < 80) else ""
        print(f"{i:>4d} | {p['항목']:>14s} | {p['매출']:>12,.0f} | "
              f"{p['비율']:>5.1f}% | {p['누적비율']:>5.1f}% | {bar}{marker}")

    # 7. 카테고리별 Top 3 상품
    print("\n" + "=" * 60)
    print("  7. 카테고리별 최고 매출 거래 Top 3")
    print("=" * 60)

    top_items = top_n_by_group(data, "카테고리", "총액", n=3)
    for cat in sorted(top_items.keys()):
        print(f"\n  [{cat}]")
        for i, record in enumerate(top_items[cat], 1):
            print(f"    {i}. {record['상품명']} - {record['총액']:,}원 "
                  f"({record['수량']}개 x {record['단가']:,}원, {record['지역']})")
