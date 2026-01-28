"""
예제 27-06: 데이터 변환 (형식 변환, 집계, 피벗)

원본 데이터를 분석에 적합한 형태로 변환합니다.
형식 변환, 파생 변수 생성, 집계, 피벗 테이블 등의 변환 작업을 수행합니다.
"""

import csv
import os
import random
import datetime
from collections import defaultdict


def generate_sample_data():
    """샘플 판매 데이터를 생성합니다."""

    random.seed(42)
    records = []

    products = [
        ("무선 키보드", "전자기기", 35000),
        ("블루투스 마우스", "전자기기", 25000),
        ("모니터 거치대", "사무용품", 32000),
        ("노트북 파우치", "액세서리", 22000),
        ("USB 허브", "전자기기", 18000),
        ("헤드셋", "전자기기", 55000),
        ("마우스패드", "액세서리", 12000),
        ("책상 정리함", "사무용품", 28000),
    ]
    regions = ["서울", "경기", "부산", "대구", "인천"]
    grades = ["일반", "실버", "골드", "VIP"]

    for i in range(150):
        name, category, base_price = random.choice(products)
        qty = random.randint(1, 8)
        price = base_price + random.randint(-3000, 5000)
        date = datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 180))
        grade = random.choices(grades, weights=[40, 30, 20, 10], k=1)[0]
        discount = {"일반": 0, "실버": 0.05, "골드": 0.10, "VIP": 0.15}[grade]

        records.append({
            "주문번호": f"ORD-{i+1:04d}",
            "날짜": date.strftime("%Y-%m-%d"),
            "상품명": name,
            "카테고리": category,
            "수량": qty,
            "단가": price,
            "할인율": discount,
            "총액": int(price * qty * (1 - discount)),
            "지역": random.choice(regions),
            "고객등급": grade,
        })

    return records


def add_derived_columns(records):
    """파생 변수(새로운 컬럼)를 추가합니다."""

    print("[변환] 파생 변수 생성 중...")

    for record in records:
        # 1. 날짜 파생 변수
        date = datetime.datetime.strptime(record["날짜"], "%Y-%m-%d")
        record["연도"] = date.year
        record["월"] = date.month
        record["요일"] = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        record["분기"] = f"Q{(date.month - 1) // 3 + 1}"

        # 2. 금액 구간 분류
        total = record["총액"]
        if total < 50000:
            record["금액구간"] = "소액"
        elif total < 200000:
            record["금액구간"] = "중액"
        else:
            record["금액구간"] = "고액"

        # 3. 할인 금액 계산
        record["할인금액"] = int(record["단가"] * record["수량"] * record["할인율"])

        # 4. 건당 단가 (총액 / 수량)
        record["건당단가"] = record["총액"] // record["수량"] if record["수량"] > 0 else 0

    added_cols = ["연도", "월", "요일", "분기", "금액구간", "할인금액", "건당단가"]
    print(f"  추가된 컬럼: {', '.join(added_cols)}")
    return records


def aggregate(records, group_by, agg_field, agg_func="sum"):
    """데이터를 그룹별로 집계합니다."""

    groups = defaultdict(list)
    for record in records:
        key = record[group_by]
        try:
            groups[key].append(float(record[agg_field]))
        except (ValueError, TypeError):
            pass

    result = {}
    for key, values in groups.items():
        if agg_func == "sum":
            result[key] = sum(values)
        elif agg_func == "mean":
            result[key] = sum(values) / len(values) if values else 0
        elif agg_func == "count":
            result[key] = len(values)
        elif agg_func == "max":
            result[key] = max(values)
        elif agg_func == "min":
            result[key] = min(values)

    return result


def create_pivot_table(records, row_field, col_field, value_field, agg_func="sum"):
    """피벗 테이블을 생성합니다."""

    # 피벗 데이터 수집
    pivot = defaultdict(lambda: defaultdict(list))
    col_values = set()

    for record in records:
        row_key = record[row_field]
        col_key = record[col_field]
        col_values.add(col_key)
        try:
            pivot[row_key][col_key].append(float(record[value_field]))
        except (ValueError, TypeError):
            pass

    # 집계 적용
    result = {}
    col_values = sorted(col_values)

    for row_key in sorted(pivot.keys()):
        result[row_key] = {}
        for col_key in col_values:
            values = pivot[row_key].get(col_key, [])
            if not values:
                result[row_key][col_key] = 0
            elif agg_func == "sum":
                result[row_key][col_key] = sum(values)
            elif agg_func == "mean":
                result[row_key][col_key] = sum(values) / len(values)
            elif agg_func == "count":
                result[row_key][col_key] = len(values)

    return result, col_values


def print_pivot_table(pivot, col_values, row_label, format_func=None):
    """피벗 테이블을 출력합니다."""

    if format_func is None:
        format_func = lambda x: f"{x:>10,.0f}"

    # 헤더
    header = f"{'':>{len(row_label) + 2}s}"
    for col in col_values:
        header += f" | {col:>10s}"
    header += f" | {'합계':>10s}"

    print(header)
    print("-" * len(header))

    # 데이터 행
    for row_key, cols in sorted(pivot.items()):
        row_total = sum(cols.values())
        line = f"{str(row_key):>{len(row_label) + 2}s}"
        for col in col_values:
            line += f" | {format_func(cols.get(col, 0))}"
        line += f" | {format_func(row_total)}"
        print(line)

    # 합계 행
    print("-" * len(header))
    totals_line = f"{'합계':>{len(row_label) + 2}s}"
    grand_total = 0
    for col in col_values:
        col_total = sum(pivot[row][col] for row in pivot)
        totals_line += f" | {format_func(col_total)}"
        grand_total += col_total
    totals_line += f" | {format_func(grand_total)}"
    print(totals_line)


def convert_format(records, output_format="list_of_dicts"):
    """데이터 형식을 변환합니다."""

    if output_format == "column_dict":
        # 컬럼 기반 딕셔너리 (각 컬럼이 리스트)
        if not records:
            return {}
        result = {key: [] for key in records[0].keys()}
        for record in records:
            for key, value in record.items():
                result[key].append(value)
        return result

    elif output_format == "nested":
        # 카테고리별 중첩 구조
        result = defaultdict(list)
        for record in records:
            result[record.get("카테고리", "미분류")].append(record)
        return dict(result)

    return records


if __name__ == "__main__":
    print("=" * 60)
    print("  데이터 변환 도구")
    print("=" * 60)
    print()

    # 샘플 데이터 생성
    data = generate_sample_data()
    print(f"원본 데이터: {len(data)}개 레코드, {len(data[0])}개 컬럼")
    print()

    # 1. 파생 변수 추가
    print("-" * 60)
    data = add_derived_columns(data)
    print(f"변환 후: {len(data[0])}개 컬럼")
    print(f"컬럼 목록: {', '.join(data[0].keys())}")
    print()

    # 2. 집계 - 카테고리별 총 매출
    print("-" * 60)
    print("[집계] 카테고리별 총 매출:")
    cat_sales = aggregate(data, "카테고리", "총액", "sum")
    for cat, total in sorted(cat_sales.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {total:>12,.0f}원")
    print()

    # 3. 집계 - 월별 주문 건수
    print("[집계] 월별 주문 건수:")
    monthly_count = aggregate(data, "월", "총액", "count")
    for month, count in sorted(monthly_count.items()):
        print(f"  {int(month):>2d}월: {int(count):>4d}건")
    print()

    # 4. 집계 - 요일별 평균 매출
    print("[집계] 요일별 평균 매출:")
    day_avg = aggregate(data, "요일", "총액", "mean")
    day_order = ["월", "화", "수", "목", "금", "토", "일"]
    for day in day_order:
        if day in day_avg:
            print(f"  {day}요일: {day_avg[day]:>10,.0f}원")
    print()

    # 5. 피벗 테이블 - 카테고리 x 분기 매출
    print("-" * 60)
    print("[피벗] 카테고리 x 분기 매출:")
    pivot, cols = create_pivot_table(data, "카테고리", "분기", "총액", "sum")
    print_pivot_table(pivot, cols, "카테고리")
    print()

    # 6. 피벗 테이블 - 지역 x 카테고리 주문건수
    print("[피벗] 지역 x 카테고리 주문 건수:")
    pivot2, cols2 = create_pivot_table(data, "지역", "카테고리", "총액", "count")
    print_pivot_table(pivot2, cols2, "지역", format_func=lambda x: f"{x:>10.0f}")
    print()

    # 7. 형식 변환
    print("-" * 60)
    print("[형식 변환]")

    # 컬럼 기반 변환
    col_dict = convert_format(data[:5], "column_dict")
    print(f"\n컬럼 기반 형식 (키 목록): {list(col_dict.keys())[:5]}...")

    # 중첩 구조 변환
    nested = convert_format(data, "nested")
    print(f"\n카테고리별 중첩 구조:")
    for cat, items in nested.items():
        print(f"  {cat}: {len(items)}건")

    # 8. 금액 구간별 분포
    print(f"\n[파생 변수 활용] 금액 구간별 분포:")
    amount_dist = aggregate(data, "금액구간", "총액", "count")
    for seg in ["소액", "중액", "고액"]:
        count = int(amount_dist.get(seg, 0))
        pct = count / len(data) * 100
        print(f"  {seg}: {count:>4d}건 ({pct:>5.1f}%)")
