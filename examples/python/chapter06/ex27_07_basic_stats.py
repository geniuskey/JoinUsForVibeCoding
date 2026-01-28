"""
예제 27-07: 기본 통계 계산

표준 라이브러리의 statistics 모듈을 활용하여
평균, 중앙값, 표준편차, 최빈값 등 기본 통계를 계산합니다.
"""

import random
import math
import statistics
from collections import Counter


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
    ]
    regions = ["서울", "경기", "부산", "대구", "인천"]

    for i in range(200):
        name, category, base_price = random.choice(products)
        qty = random.randint(1, 10)
        price = base_price + random.randint(-5000, 5000)

        data.append({
            "상품명": name,
            "카테고리": category,
            "수량": qty,
            "단가": price,
            "총액": price * qty,
            "지역": random.choice(regions),
        })

    return data


def calculate_basic_stats(values, label="데이터"):
    """기본 통계량을 계산하고 출력합니다."""

    if not values:
        print(f"  {label}: 데이터 없음")
        return {}

    n = len(values)
    total = sum(values)
    mean = statistics.mean(values)
    median = statistics.median(values)

    # 표준편차 (데이터가 2개 이상일 때)
    stdev = statistics.stdev(values) if n >= 2 else 0

    # 분산
    variance = statistics.variance(values) if n >= 2 else 0

    # 최솟값, 최댓값
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val

    result = {
        "개수": n,
        "합계": total,
        "평균": mean,
        "중앙값": median,
        "표준편차": stdev,
        "분산": variance,
        "최솟값": min_val,
        "최댓값": max_val,
        "범위": range_val,
    }

    return result


def calculate_percentiles(values):
    """백분위수를 계산합니다."""

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    percentiles = {}
    for p in [10, 25, 50, 75, 90, 95, 99]:
        idx = int(n * p / 100)
        idx = min(idx, n - 1)
        percentiles[f"P{p}"] = sorted_vals[idx]

    return percentiles


def calculate_mode(values):
    """최빈값(가장 자주 나타나는 값)을 계산합니다."""

    counter = Counter(values)
    most_common = counter.most_common(5)
    return most_common


def calculate_skewness(values):
    """왜도(비대칭도)를 계산합니다. 정규분포 대칭 여부를 판단합니다."""

    n = len(values)
    if n < 3:
        return 0

    mean = statistics.mean(values)
    stdev = statistics.stdev(values)

    if stdev == 0:
        return 0

    skew = sum((x - mean) ** 3 for x in values) / ((n - 1) * stdev ** 3)
    return skew


def calculate_correlation(x_values, y_values):
    """두 변수 간의 상관계수를 계산합니다 (피어슨 상관계수)."""

    n = len(x_values)
    if n != len(y_values) or n < 2:
        return 0

    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    # 공분산
    covariance = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values)) / (n - 1)

    # 표준편차
    std_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values) / (n - 1))
    std_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values) / (n - 1))

    if std_x == 0 or std_y == 0:
        return 0

    return covariance / (std_x * std_y)


def print_stats_report(stats, label):
    """통계 결과를 보기 좋게 출력합니다."""

    print(f"\n  {label}")
    print(f"  {'-' * 40}")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key:>8s}: {value:>15,.2f}")
        else:
            print(f"  {key:>8s}: {value:>15,}")


def print_distribution(values, bins=10, label="분포"):
    """값의 분포를 간단한 히스토그램으로 출력합니다."""

    if not values:
        return

    min_val = min(values)
    max_val = max(values)
    bin_width = (max_val - min_val) / bins if max_val > min_val else 1

    # 빈 카운트
    bin_counts = [0] * bins
    for v in values:
        idx = int((v - min_val) / bin_width)
        idx = min(idx, bins - 1)
        bin_counts[idx] += 1

    max_count = max(bin_counts) if bin_counts else 1

    print(f"\n  {label} (구간: {bins}개)")
    print(f"  {'구간':>16s} | {'빈도':>5s} | 분포")
    print(f"  {'-' * 16}-+{'-' * 6}-+{'-' * 30}")

    for i in range(bins):
        lower = min_val + i * bin_width
        upper = lower + bin_width
        count = bin_counts[i]
        bar_len = int(count / max_count * 25) if max_count > 0 else 0
        bar = "#" * bar_len

        print(f"  {lower:>7,.0f}~{upper:>7,.0f} | {count:>5d} | {bar}")


if __name__ == "__main__":
    print("=" * 60)
    print("  기본 통계 분석")
    print("=" * 60)

    # 샘플 데이터 생성
    data = generate_sample_data()
    print(f"\n데이터: {len(data)}개 판매 레코드")

    # 분석 대상 컬럼 추출
    amounts = [d["총액"] for d in data]
    quantities = [d["수량"] for d in data]
    prices = [d["단가"] for d in data]

    # 1. 기본 통계량
    print("\n" + "=" * 60)
    print("  1. 기본 통계량")
    print("=" * 60)

    for label, values in [("총액", amounts), ("수량", quantities), ("단가", prices)]:
        stats = calculate_basic_stats(values, label)
        print_stats_report(stats, f"'{label}' 통계")

    # 2. 백분위수
    print("\n" + "=" * 60)
    print("  2. 총액 백분위수")
    print("=" * 60)

    percentiles = calculate_percentiles(amounts)
    print()
    for p_name, p_val in percentiles.items():
        bar_len = int(p_val / max(amounts) * 30)
        bar = "=" * bar_len
        print(f"  {p_name:>4s}: {p_val:>10,.0f}원 |{bar}")

    # 3. 최빈값
    print("\n" + "=" * 60)
    print("  3. 최빈값 (가장 많이 팔린)")
    print("=" * 60)

    product_counts = [d["상품명"] for d in data]
    modes = calculate_mode(product_counts)
    print("\n  상품별 판매 빈도 (상위 5개):")
    for item, count in modes:
        pct = count / len(data) * 100
        print(f"  {item:>12s}: {count:>4d}건 ({pct:>5.1f}%)")

    region_counts = [d["지역"] for d in data]
    modes_region = calculate_mode(region_counts)
    print("\n  지역별 판매 빈도:")
    for item, count in modes_region:
        pct = count / len(data) * 100
        print(f"  {item:>6s}: {count:>4d}건 ({pct:>5.1f}%)")

    # 4. 왜도
    print("\n" + "=" * 60)
    print("  4. 분포 특성")
    print("=" * 60)

    skew = calculate_skewness(amounts)
    print(f"\n  총액 왜도: {skew:.3f}")
    if skew > 0.5:
        print("  -> 오른쪽으로 치우친 분포 (고액 주문이 적음)")
    elif skew < -0.5:
        print("  -> 왼쪽으로 치우친 분포 (소액 주문이 적음)")
    else:
        print("  -> 비교적 대칭적 분포")

    # 5. 상관관계
    print("\n" + "=" * 60)
    print("  5. 상관관계 분석")
    print("=" * 60)

    corr_qty_amount = calculate_correlation(quantities, amounts)
    corr_price_amount = calculate_correlation(prices, amounts)
    corr_qty_price = calculate_correlation(quantities, prices)

    print(f"\n  수량 vs 총액:  r = {corr_qty_amount:>7.4f}", end="")
    if abs(corr_qty_amount) > 0.7:
        print(" (강한 상관)")
    elif abs(corr_qty_amount) > 0.3:
        print(" (중간 상관)")
    else:
        print(" (약한 상관)")

    print(f"  단가 vs 총액:  r = {corr_price_amount:>7.4f}", end="")
    if abs(corr_price_amount) > 0.7:
        print(" (강한 상관)")
    elif abs(corr_price_amount) > 0.3:
        print(" (중간 상관)")
    else:
        print(" (약한 상관)")

    print(f"  수량 vs 단가:  r = {corr_qty_price:>7.4f}", end="")
    if abs(corr_qty_price) > 0.7:
        print(" (강한 상관)")
    elif abs(corr_qty_price) > 0.3:
        print(" (중간 상관)")
    else:
        print(" (약한 상관)")

    # 6. 분포 히스토그램
    print("\n" + "=" * 60)
    print("  6. 분포 히스토그램")
    print("=" * 60)

    print_distribution(amounts, bins=8, label="총액 분포")
    print_distribution(prices, bins=6, label="단가 분포")
