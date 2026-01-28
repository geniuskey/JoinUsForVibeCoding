"""
예제 27-03: CSV 데이터 로드

csv 모듈을 사용하여 CSV 파일에서 데이터를 읽어들이고
기본적인 데이터 확인 작업을 수행합니다.
"""

import csv
import os
import random
import datetime


def generate_sample_csv(filepath):
    """데모용 샘플 CSV 파일을 생성합니다."""

    random.seed(42)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

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

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["주문번호", "날짜", "상품명", "카테고리", "수량", "단가", "총액", "지역"])

        for i in range(100):
            name, category, base_price = random.choice(products)
            qty = random.randint(1, 10)
            price = base_price + random.randint(-5000, 5000)
            date = datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 180))
            writer.writerow([
                f"ORD-{i+1:04d}",
                date.strftime("%Y-%m-%d"),
                name, category, qty, price, price * qty,
                random.choice(regions),
            ])

    return filepath


def load_csv(filepath):
    """CSV 파일을 로드하여 딕셔너리 리스트로 반환합니다."""

    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다 - {filepath}")
        return []

    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    return records


def inspect_data(records, name="데이터"):
    """데이터의 기본 정보를 출력합니다."""

    if not records:
        print("데이터가 비어 있습니다.")
        return

    print(f"\n{'=' * 60}")
    print(f"  {name} 기본 정보")
    print(f"{'=' * 60}")

    # 레코드 수
    print(f"\n총 레코드 수: {len(records):,}개")

    # 컬럼 정보
    columns = list(records[0].keys())
    print(f"컬럼 수: {len(columns)}개")
    print(f"컬럼 목록: {', '.join(columns)}")

    # 각 컬럼별 정보
    print(f"\n{'컬럼명':>12s} | {'타입':>8s} | {'비어있음':>8s} | {'고유값':>8s} | 샘플값")
    print("-" * 75)

    for col in columns:
        values = [r[col] for r in records]
        non_empty = [v for v in values if v.strip() != ""]
        unique_count = len(set(values))

        # 숫자인지 판별
        numeric = True
        for v in non_empty[:10]:
            try:
                float(v.replace(",", ""))
            except ValueError:
                numeric = False
                break

        dtype = "숫자" if numeric else "문자열"
        empty_count = len(values) - len(non_empty)
        sample = non_empty[0] if non_empty else "(없음)"

        if len(sample) > 15:
            sample = sample[:12] + "..."

        print(f"{col:>12s} | {dtype:>8s} | {empty_count:>8d} | {unique_count:>8d} | {sample}")

    return columns


def show_head(records, n=5):
    """처음 n개 레코드를 표시합니다."""

    if not records:
        return

    print(f"\n처음 {n}개 레코드:")
    print("-" * 80)

    columns = list(records[0].keys())

    # 각 컬럼의 최대 너비 계산
    col_widths = {}
    for col in columns:
        max_width = len(col)
        for r in records[:n]:
            max_width = max(max_width, len(str(r[col])))
        col_widths[col] = min(max_width, 14)  # 최대 14자

    # 헤더 출력
    header = " | ".join(f"{col:>{col_widths[col]}s}" for col in columns)
    print(header)
    print("-" * len(header))

    # 데이터 출력
    for record in records[:n]:
        row = " | ".join(
            f"{str(record[col])[:col_widths[col]]:>{col_widths[col]}s}"
            for col in columns
        )
        print(row)


def show_tail(records, n=5):
    """마지막 n개 레코드를 표시합니다."""

    if not records:
        return

    print(f"\n마지막 {n}개 레코드:")
    print("-" * 80)

    columns = list(records[0].keys())

    col_widths = {}
    for col in columns:
        max_width = len(col)
        for r in records[-n:]:
            max_width = max(max_width, len(str(r[col])))
        col_widths[col] = min(max_width, 14)

    header = " | ".join(f"{col:>{col_widths[col]}s}" for col in columns)
    print(header)
    print("-" * len(header))

    for record in records[-n:]:
        row = " | ".join(
            f"{str(record[col])[:col_widths[col]]:>{col_widths[col]}s}"
            for col in columns
        )
        print(row)


def get_numeric_summary(records, column):
    """숫자 컬럼의 기본 통계를 출력합니다."""

    values = []
    for r in records:
        try:
            val = float(r[column].replace(",", ""))
            values.append(val)
        except (ValueError, AttributeError):
            continue

    if not values:
        print(f"'{column}' 컬럼에 유효한 숫자 데이터가 없습니다.")
        return

    values.sort()
    total = sum(values)
    mean = total / len(values)
    minimum = values[0]
    maximum = values[-1]
    median = values[len(values) // 2]

    print(f"\n'{column}' 컬럼 통계:")
    print(f"  유효 데이터: {len(values):,}개")
    print(f"  합계: {total:,.0f}")
    print(f"  평균: {mean:,.0f}")
    print(f"  최솟값: {minimum:,.0f}")
    print(f"  최댓값: {maximum:,.0f}")
    print(f"  중앙값: {median:,.0f}")


if __name__ == "__main__":
    print("=" * 60)
    print("  CSV 데이터 로더")
    print("=" * 60)

    # 샘플 데이터 생성
    csv_path = "/tmp/dashboard-data/sales_demo.csv"
    print(f"\n샘플 CSV 파일 생성 중: {csv_path}")
    generate_sample_csv(csv_path)
    print(f"파일 크기: {os.path.getsize(csv_path):,} 바이트")

    # CSV 로드
    print("\nCSV 파일 로드 중...")
    data = load_csv(csv_path)
    print(f"로드 완료: {len(data)}개 레코드")

    # 데이터 정보 확인
    inspect_data(data, "판매 데이터")

    # 데이터 미리보기
    show_head(data, 5)
    show_tail(data, 3)

    # 숫자 컬럼 통계
    for col in ["수량", "단가", "총액"]:
        get_numeric_summary(data, col)
