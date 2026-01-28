"""
예제 27-05: 데이터 정제 (결측치/이상치 처리)

실무에서 자주 발생하는 데이터 품질 문제를 탐지하고 처리하는 방법을 보여줍니다.
결측치(빈 값), 이상치(비정상적으로 크거나 작은 값), 잘못된 형식의 데이터를 다룹니다.
"""

import csv
import os
import random
import datetime
import copy


def generate_dirty_data():
    """정제가 필요한 불량 데이터가 포함된 샘플 데이터를 생성합니다."""

    random.seed(42)
    records = []

    products = [
        ("무선 키보드", "전자기기", 35000),
        ("블루투스 마우스", "전자기기", 25000),
        ("모니터 거치대", "사무용품", 32000),
        ("노트북 파우치", "액세서리", 22000),
        ("USB 허브", "전자기기", 18000),
    ]
    regions = ["서울", "경기", "부산", "대구", "인천"]

    for i in range(50):
        name, category, base_price = random.choice(products)
        qty = random.randint(1, 10)
        price = base_price + random.randint(-3000, 3000)
        date = datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 180))

        records.append({
            "주문번호": f"ORD-{i+1:04d}",
            "날짜": date.strftime("%Y-%m-%d"),
            "상품명": name,
            "카테고리": category,
            "수량": str(qty),
            "단가": str(price),
            "총액": str(price * qty),
            "지역": random.choice(regions),
        })

    # 의도적으로 불량 데이터 삽입
    # 1. 결측치 (빈 값)
    records[3]["수량"] = ""
    records[7]["단가"] = ""
    records[12]["지역"] = ""
    records[15]["상품명"] = ""
    records[20]["수량"] = ""
    records[25]["단가"] = ""

    # 2. 음수 값 (논리적 오류)
    records[5]["수량"] = "-3"
    records[18]["단가"] = "-15000"

    # 3. 이상치 (비정상적으로 큰 값)
    records[10]["단가"] = "9999999"
    records[30]["수량"] = "500"

    # 4. 잘못된 날짜 형식
    records[8]["날짜"] = "2025-13-45"
    records[22]["날짜"] = "날짜오류"

    # 5. 타입 오류 (숫자 필드에 문자)
    records[35]["수량"] = "다섯개"
    records[40]["단가"] = "삼만원"

    # 6. 중복 데이터
    records.append(dict(records[0]))  # 완전 중복
    records.append(dict(records[1]))  # 완전 중복

    return records


class DataCleaner:
    """데이터 정제 도구: 다양한 데이터 품질 문제를 탐지하고 처리합니다."""

    def __init__(self, records):
        self.original = records
        self.cleaned = copy.deepcopy(records)
        self.issues = []  # 발견된 문제 목록
        self.stats = {
            "총_레코드": len(records),
            "결측치": 0,
            "이상치": 0,
            "형식오류": 0,
            "중복": 0,
            "음수값": 0,
            "수정됨": 0,
            "제거됨": 0,
        }

    def detect_missing_values(self, required_fields=None):
        """결측치(빈 값)를 탐지합니다."""

        print("\n[검사] 결측치 탐지 중...")

        if required_fields is None:
            required_fields = list(self.cleaned[0].keys())

        count = 0
        for i, record in enumerate(self.cleaned):
            for field in required_fields:
                if field in record and (record[field] is None or str(record[field]).strip() == ""):
                    self.issues.append({
                        "행": i,
                        "필드": field,
                        "유형": "결측치",
                        "값": record[field],
                    })
                    count += 1

        self.stats["결측치"] = count
        print(f"  발견: {count}건")
        return count

    def detect_invalid_numbers(self, numeric_fields):
        """숫자 필드에서 잘못된 값을 탐지합니다."""

        print("\n[검사] 숫자 필드 유효성 검사 중...")

        format_errors = 0
        negative_errors = 0

        for i, record in enumerate(self.cleaned):
            for field in numeric_fields:
                value = str(record.get(field, "")).strip()
                if value == "":
                    continue  # 결측치는 별도 처리

                try:
                    num = float(value)
                    if num < 0:
                        self.issues.append({
                            "행": i,
                            "필드": field,
                            "유형": "음수값",
                            "값": value,
                        })
                        negative_errors += 1
                except ValueError:
                    self.issues.append({
                        "행": i,
                        "필드": field,
                        "유형": "형식오류",
                        "값": value,
                    })
                    format_errors += 1

        self.stats["형식오류"] += format_errors
        self.stats["음수값"] = negative_errors
        print(f"  형식 오류: {format_errors}건")
        print(f"  음수 값: {negative_errors}건")
        return format_errors + negative_errors

    def detect_outliers(self, field, method="iqr"):
        """이상치를 탐지합니다 (IQR 방법)."""

        print(f"\n[검사] '{field}' 이상치 탐지 중 (IQR 방법)...")

        # 유효한 숫자 값만 추출
        values = []
        for record in self.cleaned:
            try:
                val = float(str(record.get(field, "")).strip())
                if val >= 0:
                    values.append(val)
            except ValueError:
                continue

        if len(values) < 4:
            print("  데이터가 부족하여 이상치 탐지를 건너뜁니다.")
            return 0

        # IQR 계산
        values.sort()
        n = len(values)
        q1 = values[n // 4]
        q3 = values[3 * n // 4]
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        print(f"  Q1: {q1:,.0f}, Q3: {q3:,.0f}, IQR: {iqr:,.0f}")
        print(f"  정상 범위: {max(0, lower_bound):,.0f} ~ {upper_bound:,.0f}")

        count = 0
        for i, record in enumerate(self.cleaned):
            try:
                val = float(str(record.get(field, "")).strip())
                if val < lower_bound or val > upper_bound:
                    self.issues.append({
                        "행": i,
                        "필드": field,
                        "유형": "이상치",
                        "값": str(val),
                    })
                    count += 1
            except ValueError:
                continue

        self.stats["이상치"] += count
        print(f"  발견: {count}건")
        return count

    def detect_invalid_dates(self, date_field="날짜", date_format="%Y-%m-%d"):
        """잘못된 날짜를 탐지합니다."""

        print(f"\n[검사] '{date_field}' 날짜 유효성 검사 중...")

        count = 0
        for i, record in enumerate(self.cleaned):
            value = str(record.get(date_field, "")).strip()
            if value == "":
                continue

            try:
                datetime.datetime.strptime(value, date_format)
            except ValueError:
                self.issues.append({
                    "행": i,
                    "필드": date_field,
                    "유형": "날짜오류",
                    "값": value,
                })
                count += 1

        self.stats["형식오류"] += count
        print(f"  발견: {count}건")
        return count

    def detect_duplicates(self, key_field="주문번호"):
        """중복 레코드를 탐지합니다."""

        print(f"\n[검사] 중복 레코드 탐지 중 (키: {key_field})...")

        seen = {}
        count = 0
        for i, record in enumerate(self.cleaned):
            key = record.get(key_field, "")
            if key in seen:
                self.issues.append({
                    "행": i,
                    "필드": key_field,
                    "유형": "중복",
                    "값": key,
                    "원본행": seen[key],
                })
                count += 1
            else:
                seen[key] = i

        self.stats["중복"] = count
        print(f"  발견: {count}건")
        return count

    def fix_missing_values(self, field, strategy="median", default_value=None):
        """결측치를 처리합니다."""

        if strategy == "remove":
            # 결측치가 있는 행 제거
            self.cleaned = [
                r for r in self.cleaned
                if str(r.get(field, "")).strip() != ""
            ]
        elif strategy == "default":
            # 기본값으로 대체
            for record in self.cleaned:
                if str(record.get(field, "")).strip() == "":
                    record[field] = str(default_value)
                    self.stats["수정됨"] += 1
        elif strategy == "median":
            # 중앙값으로 대체 (숫자 필드)
            values = []
            for r in self.cleaned:
                try:
                    values.append(float(str(r[field]).strip()))
                except (ValueError, KeyError):
                    pass
            if values:
                values.sort()
                median_val = values[len(values) // 2]
                for record in self.cleaned:
                    if str(record.get(field, "")).strip() == "":
                        record[field] = str(int(median_val))
                        self.stats["수정됨"] += 1

    def fix_invalid_numbers(self, field):
        """숫자 필드의 잘못된 값을 제거합니다."""

        to_remove = []
        for i, record in enumerate(self.cleaned):
            value = str(record.get(field, "")).strip()
            if value == "":
                continue
            try:
                num = float(value)
                if num < 0:
                    to_remove.append(i)
            except ValueError:
                to_remove.append(i)

        # 역순으로 제거 (인덱스 유지를 위해)
        for i in reversed(to_remove):
            self.cleaned.pop(i)
            self.stats["제거됨"] += 1

    def fix_outliers(self, field, upper_bound):
        """이상치를 제거합니다."""

        to_remove = []
        for i, record in enumerate(self.cleaned):
            try:
                val = float(str(record.get(field, "")).strip())
                if val > upper_bound:
                    to_remove.append(i)
            except ValueError:
                pass

        for i in reversed(to_remove):
            self.cleaned.pop(i)
            self.stats["제거됨"] += 1

    def fix_duplicates(self, key_field="주문번호"):
        """중복 레코드를 제거합니다 (첫 번째만 유지)."""

        seen = set()
        unique = []
        for record in self.cleaned:
            key = record.get(key_field, "")
            if key not in seen:
                seen.add(key)
                unique.append(record)
            else:
                self.stats["제거됨"] += 1
        self.cleaned = unique

    def report(self):
        """정제 결과 보고서를 출력합니다."""

        print("\n" + "=" * 60)
        print("  데이터 정제 결과 보고서")
        print("=" * 60)

        print(f"\n원본 데이터: {self.stats['총_레코드']}개 레코드")
        print(f"정제 후 데이터: {len(self.cleaned)}개 레코드")
        print()

        print("발견된 문제:")
        print(f"  결측치: {self.stats['결측치']}건")
        print(f"  형식 오류: {self.stats['형식오류']}건")
        print(f"  음수 값: {self.stats['음수값']}건")
        print(f"  이상치: {self.stats['이상치']}건")
        print(f"  중복: {self.stats['중복']}건")
        total_issues = sum(v for k, v in self.stats.items()
                          if k not in ("총_레코드", "수정됨", "제거됨"))
        print(f"  --------")
        print(f"  합계: {total_issues}건")
        print()

        print("처리 결과:")
        print(f"  수정된 값: {self.stats['수정됨']}건")
        print(f"  제거된 행: {self.stats['제거됨']}건")
        print(f"  데이터 손실률: {self.stats['제거됨'] / self.stats['총_레코드'] * 100:.1f}%")

        # 상세 이슈 목록 (최대 10건)
        if self.issues:
            print(f"\n상세 이슈 목록 (처음 10건):")
            print(f"  {'행':>4s} | {'필드':>10s} | {'유형':>8s} | 값")
            print(f"  {'-'*4}-+-{'-'*10}-+-{'-'*8}-+------")
            for issue in self.issues[:10]:
                val = str(issue['값'])[:20]
                print(f"  {issue['행']:>4d} | {issue['필드']:>10s} | "
                      f"{issue['유형']:>8s} | {val}")
            if len(self.issues) > 10:
                print(f"  ... 외 {len(self.issues) - 10}건")


if __name__ == "__main__":
    print("=" * 60)
    print("  데이터 정제 도구")
    print("=" * 60)

    # 불량 데이터 생성
    print("\n불량 데이터가 포함된 샘플 생성 중...")
    dirty_data = generate_dirty_data()
    print(f"생성된 레코드: {len(dirty_data)}개")

    # 정제기 초기화
    cleaner = DataCleaner(dirty_data)

    # 1단계: 문제 탐지
    print("\n" + "=" * 60)
    print("  1단계: 데이터 품질 검사")
    print("=" * 60)

    cleaner.detect_missing_values(["수량", "단가", "지역", "상품명"])
    cleaner.detect_invalid_numbers(["수량", "단가", "총액"])
    cleaner.detect_outliers("단가")
    cleaner.detect_outliers("수량")
    cleaner.detect_invalid_dates("날짜")
    cleaner.detect_duplicates("주문번호")

    # 2단계: 문제 수정
    print("\n" + "=" * 60)
    print("  2단계: 데이터 정제")
    print("=" * 60)

    print("\n결측치 처리...")
    cleaner.fix_missing_values("수량", strategy="median")
    cleaner.fix_missing_values("단가", strategy="median")
    cleaner.fix_missing_values("지역", strategy="default", default_value="미분류")
    cleaner.fix_missing_values("상품명", strategy="default", default_value="미확인상품")

    print("숫자 오류 처리...")
    cleaner.fix_invalid_numbers("수량")
    cleaner.fix_invalid_numbers("단가")

    print("이상치 처리...")
    cleaner.fix_outliers("단가", upper_bound=100000)
    cleaner.fix_outliers("수량", upper_bound=50)

    print("중복 제거...")
    cleaner.fix_duplicates("주문번호")

    # 3단계: 결과 보고
    cleaner.report()

    # 정제된 데이터 저장
    output_path = "/tmp/dashboard-data/sales_cleaned.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if cleaner.cleaned:
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cleaner.cleaned[0].keys())
            writer.writeheader()
            writer.writerows(cleaner.cleaned)
        print(f"\n정제된 데이터 저장 완료: {output_path}")
        print(f"최종 레코드 수: {len(cleaner.cleaned)}개")
