#!/usr/bin/env python3
"""예제 16-02: CSV 필터링

조건에 맞는 행만 추출하여 결과를 표시합니다.
"""

import csv
import io

# 학생 성적 CSV 데이터
csv_data = """이름,과목,점수,학년
김민수,수학,85,2
이영희,영어,92,3
박철수,수학,78,1
정미래,영어,95,2
한지우,과학,88,3
오세훈,수학,73,1
최다은,영어,90,2
강준혁,과학,82,3
송예린,수학,96,3
윤도현,과학,67,1
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

print(f"전체 학생 수: {len(records)}명\n")

# 필터 1: 점수 85점 이상
high_scores = [r for r in records if int(r["점수"]) >= 85]
print("[필터 1] 85점 이상 학생")
print(f"{'이름':<8} {'과목':<6} {'점수':>4} {'학년':>4}")
print("-" * 26)
for r in high_scores:
    print(f"{r['이름']:<8} {r['과목']:<6} {r['점수']:>4} {r['학년']:>4}")
print(f"→ {len(high_scores)}명 해당\n")

# 필터 2: 수학 과목만
math_students = [r for r in records if r["과목"] == "수학"]
print("[필터 2] 수학 과목 학생")
print(f"{'이름':<8} {'점수':>4} {'학년':>4}")
print("-" * 20)
for r in math_students:
    print(f"{r['이름']:<8} {r['점수']:>4} {r['학년']:>4}")
print(f"→ {len(math_students)}명 해당\n")

# 필터 3: 3학년이면서 점수 80점 이상
senior_high = [r for r in records if r["학년"] == "3" and int(r["점수"]) >= 80]
print("[필터 3] 3학년 & 80점 이상")
print(f"{'이름':<8} {'과목':<6} {'점수':>4}")
print("-" * 22)
for r in senior_high:
    print(f"{r['이름']:<8} {r['과목']:<6} {r['점수']:>4}")
print(f"→ {len(senior_high)}명 해당")
