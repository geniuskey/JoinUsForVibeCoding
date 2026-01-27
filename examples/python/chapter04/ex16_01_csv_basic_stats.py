#!/usr/bin/env python3
"""예제 16-01: CSV 읽기와 기본 통계

CSV 문자열을 파싱하고 기본 통계(평균, 최솟값, 최댓값)를 계산합니다.
"""

import csv
import io
import statistics

# CSV 데이터를 코드 내에 직접 정의
csv_data = """이름,과목,점수
김민수,수학,85
이영희,수학,92
박철수,수학,78
정미래,수학,95
한지우,수학,88
오세훈,수학,73
최다은,수학,90
강준혁,수학,82
"""

# CSV 파싱
reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

# 점수 목록 추출
scores = [int(row["점수"]) for row in records]

# 기본 통계 계산
print("=" * 40)
print("  수학 성적 기본 통계")
print("=" * 40)
print(f"  학생 수 : {len(scores)}명")
print(f"  평균    : {statistics.mean(scores):.1f}점")
print(f"  중앙값  : {statistics.median(scores):.1f}점")
print(f"  최고점  : {max(scores)}점")
print(f"  최저점  : {min(scores)}점")
print(f"  표준편차: {statistics.stdev(scores):.1f}")
print("=" * 40)

# 전체 데이터 출력
print("\n[전체 성적 목록]")
print(f"{'이름':<8} {'과목':<6} {'점수':>4}")
print("-" * 22)
for row in records:
    print(f"{row['이름']:<8} {row['과목']:<6} {row['점수']:>4}")
