"""
예제 27-02: 샘플 판매 데이터 CSV 생성

random 모듈을 사용하여 대시보드에서 사용할 현실적인 판매 데이터를 생성합니다.
생성되는 데이터: 날짜, 상품명, 카테고리, 수량, 단가, 지역, 고객등급
"""

import csv
import os
import random
import datetime


def generate_sales_data(num_records=200, seed=42):
    """현실적인 판매 데이터를 생성합니다."""

    # 재현 가능한 결과를 위해 시드 설정
    random.seed(seed)

    # 상품 정보 (상품명, 카테고리, 가격 범위)
    products = [
        ("무선 키보드", "전자기기", 25000, 65000),
        ("블루투스 마우스", "전자기기", 15000, 45000),
        ("USB 허브", "전자기기", 12000, 35000),
        ("모니터 거치대", "사무용품", 20000, 55000),
        ("노트북 파우치", "액세서리", 15000, 40000),
        ("웹캠", "전자기기", 30000, 80000),
        ("마우스패드", "액세서리", 5000, 25000),
        ("헤드셋", "전자기기", 25000, 120000),
        ("USB 메모리", "전자기기", 8000, 30000),
        ("책상 정리함", "사무용품", 10000, 35000),
        ("노트북 스탠드", "사무용품", 18000, 50000),
        ("충전 케이블", "액세서리", 5000, 15000),
        ("보조 배터리", "전자기기", 15000, 45000),
        ("데스크 매트", "사무용품", 12000, 40000),
        ("스마트 펜", "사무용품", 20000, 60000),
    ]

    # 지역 목록
    regions = ["서울", "경기", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]

    # 고객 등급
    customer_grades = ["일반", "실버", "골드", "VIP"]
    grade_weights = [40, 30, 20, 10]  # 가중치 (일반이 가장 많음)

    # 날짜 범위 (최근 6개월)
    end_date = datetime.date(2025, 6, 30)
    start_date = datetime.date(2025, 1, 1)
    date_range = (end_date - start_date).days

    # 데이터 생성
    records = []
    for i in range(num_records):
        # 랜덤 날짜 생성
        random_days = random.randint(0, date_range)
        sale_date = start_date + datetime.timedelta(days=random_days)

        # 랜덤 상품 선택
        product_name, category, min_price, max_price = random.choice(products)

        # 가격 결정 (100원 단위)
        unit_price = round(random.randint(min_price, max_price) / 100) * 100

        # 수량 (1~20, 대부분 1~5)
        quantity = random.choices(
            range(1, 21),
            weights=[30, 25, 15, 10, 8] + [1] * 15,
            k=1
        )[0]

        # 지역
        region = random.choice(regions)

        # 고객 등급 (가중치 적용)
        grade = random.choices(customer_grades, weights=grade_weights, k=1)[0]

        # 할인율 (등급별 차등)
        discount_rates = {"일반": 0, "실버": 0.05, "골드": 0.10, "VIP": 0.15}
        discount = discount_rates[grade]

        # 총액 계산
        total = int(unit_price * quantity * (1 - discount))

        records.append({
            "주문번호": f"ORD-{i+1:04d}",
            "날짜": sale_date.strftime("%Y-%m-%d"),
            "상품명": product_name,
            "카테고리": category,
            "수량": quantity,
            "단가": unit_price,
            "할인율": f"{discount:.0%}",
            "총액": total,
            "지역": region,
            "고객등급": grade,
        })

    # 날짜순 정렬
    records.sort(key=lambda x: x["날짜"])

    return records


def add_dirty_data(records, dirty_ratio=0.05):
    """데이터 정제 예제를 위해 의도적으로 불량 데이터를 추가합니다."""

    dirty_records = list(records)  # 복사
    num_dirty = max(1, int(len(records) * dirty_ratio))

    random.seed(99)

    for _ in range(num_dirty):
        idx = random.randint(0, len(dirty_records) - 1)
        record = dict(dirty_records[idx])  # 복사

        # 불량 데이터 유형 랜덤 선택
        dirty_type = random.choice(["missing", "negative", "outlier", "invalid_date"])

        if dirty_type == "missing":
            # 결측치: 빈 값
            field = random.choice(["수량", "단가", "지역"])
            record[field] = ""
        elif dirty_type == "negative":
            # 음수 값
            record["수량"] = -random.randint(1, 5)
        elif dirty_type == "outlier":
            # 이상치: 비정상적으로 큰 값
            record["단가"] = random.randint(900000, 9999999)
        elif dirty_type == "invalid_date":
            # 잘못된 날짜
            record["날짜"] = "2025-13-45"

        dirty_records[idx] = record

    return dirty_records


def save_to_csv(records, filepath):
    """레코드 목록을 CSV 파일로 저장합니다."""

    if not records:
        print("저장할 데이터가 없습니다.")
        return

    fieldnames = records[0].keys()

    # 디렉토리 생성
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"파일 저장 완료: {filepath}")
    print(f"  - 레코드 수: {len(records)}개")
    file_size = os.path.getsize(filepath)
    print(f"  - 파일 크기: {file_size:,} 바이트")


if __name__ == "__main__":
    print("=" * 60)
    print("  판매 샘플 데이터 생성기")
    print("=" * 60)
    print()

    # 1. 정상 데이터 생성
    print("[1단계] 정상 판매 데이터 생성 중...")
    clean_data = generate_sales_data(num_records=200)
    clean_path = "/tmp/dashboard-data/sales_clean.csv"
    save_to_csv(clean_data, clean_path)
    print()

    # 2. 불량 데이터 포함 버전 생성 (정제 연습용)
    print("[2단계] 불량 데이터 포함 버전 생성 중...")
    dirty_data = add_dirty_data(clean_data, dirty_ratio=0.05)
    dirty_path = "/tmp/dashboard-data/sales_raw.csv"
    save_to_csv(dirty_data, dirty_path)
    print()

    # 3. 데이터 미리보기
    print("-" * 60)
    print("데이터 미리보기 (처음 5건):")
    print("-" * 60)

    # 헤더 출력
    headers = list(clean_data[0].keys())
    # 주요 컬럼만 표시
    display_cols = ["주문번호", "날짜", "상품명", "수량", "단가", "총액", "지역"]

    header_line = " | ".join(f"{h:>8s}" for h in display_cols)
    print(header_line)
    print("-" * len(header_line))

    for record in clean_data[:5]:
        values = []
        for col in display_cols:
            val = record[col]
            if isinstance(val, int):
                values.append(f"{val:>8,}")
            else:
                values.append(f"{str(val):>8s}")
        print(" | ".join(values))

    print()

    # 4. 데이터 요약
    print("-" * 60)
    print("데이터 요약:")
    print("-" * 60)

    total_sales = sum(r["총액"] for r in clean_data)
    total_qty = sum(r["수량"] for r in clean_data)
    categories = set(r["카테고리"] for r in clean_data)
    regions = set(r["지역"] for r in clean_data)
    dates = [r["날짜"] for r in clean_data]

    print(f"  총 주문 건수: {len(clean_data):,}건")
    print(f"  총 판매액: {total_sales:,}원")
    print(f"  총 판매 수량: {total_qty:,}개")
    print(f"  평균 주문액: {total_sales // len(clean_data):,}원")
    print(f"  카테고리 수: {len(categories)}개 ({', '.join(sorted(categories))})")
    print(f"  지역 수: {len(regions)}개")
    print(f"  기간: {min(dates)} ~ {max(dates)}")
