#!/usr/bin/env python3
"""예제 16-07: 데이터 정제 (결측치 처리)

누락된 값, 잘못된 형식의 데이터를 정제합니다.
"""

import csv
import io
import statistics

# 결측치와 오류가 포함된 CSV 데이터
csv_data = """이름,나이,점수,이메일,도시
김민수,25,85,minsu@test.com,서울
이영희,,92,younghee@test.com,부산
박철수,30,,cheolsu@test.com,대구
정미래,28,95,,서울
한지우,22,88,jiwoo@test.com,
오세훈,-5,73,sehun@test.com,광주
최다은,27,105,invalid-email,서울
강준혁,35,82,junhyuk@test.com,부산
송예린,abc,91,yerin@test.com,인천
윤도현,29,,dohyun@test.com,서울
"""

reader = csv.DictReader(io.StringIO(csv_data.strip()))
raw_records = list(reader)

print("[원본 데이터]")
print(f"{'이름':<8} {'나이':>4} {'점수':>4} {'이메일':<22} {'도시':<4}")
print("-" * 52)
for r in raw_records:
    print(f"{r['이름']:<8} {r['나이']:>4} {r['점수']:>4} {r['이메일']:<22} {r['도시']:<4}")

print(f"\n총 {len(raw_records)}건의 레코드\n")

# 데이터 정제 과정
cleaned = []
issues_log = []

for i, row in enumerate(raw_records):
    name = row["이름"]
    issues = []

    # 나이 정제
    age = row["나이"].strip()
    if not age:
        age = None
        issues.append("나이 누락 → None")
    else:
        try:
            age = int(age)
            if age < 0 or age > 120:
                issues.append(f"나이 범위 오류({age}) → None")
                age = None
        except ValueError:
            issues.append(f"나이 형식 오류('{row['나이']}') → None")
            age = None

    # 점수 정제
    score = row["점수"].strip()
    if not score:
        score = None
        issues.append("점수 누락 → None")
    else:
        try:
            score = int(score)
            if score < 0 or score > 100:
                issues.append(f"점수 범위 오류({score}) → 100으로 보정")
                score = min(max(score, 0), 100)
        except ValueError:
            issues.append(f"점수 형식 오류 → None")
            score = None

    # 이메일 정제
    email = row["이메일"].strip()
    if not email:
        email = None
        issues.append("이메일 누락 → None")
    elif "@" not in email or "." not in email:
        issues.append(f"이메일 형식 오류('{email}') → None")
        email = None

    # 도시 정제
    city = row["도시"].strip()
    if not city:
        city = "미지정"
        issues.append("도시 누락 → '미지정'")

    cleaned.append({
        "이름": name,
        "나이": age,
        "점수": score,
        "이메일": email,
        "도시": city
    })

    if issues:
        issues_log.append((name, issues))

# 정제 로그 출력
print("=" * 50)
print("  데이터 정제 로그")
print("=" * 50)
for name, issues in issues_log:
    print(f"\n  {name}:")
    for issue in issues:
        print(f"    ⚠ {issue}")

# 결측치를 평균으로 대체
valid_ages = [r["나이"] for r in cleaned if r["나이"] is not None]
valid_scores = [r["점수"] for r in cleaned if r["점수"] is not None]
mean_age = round(statistics.mean(valid_ages))
mean_score = round(statistics.mean(valid_scores))

print(f"\n[결측치 대체]")
print(f"  나이 평균값: {mean_age} (결측치 대체용)")
print(f"  점수 평균값: {mean_score} (결측치 대체용)")

for r in cleaned:
    if r["나이"] is None:
        r["나이"] = mean_age
        r["나이_대체"] = True
    else:
        r["나이_대체"] = False
    if r["점수"] is None:
        r["점수"] = mean_score
        r["점수_대체"] = True
    else:
        r["점수_대체"] = False

# 정제 결과 출력
print(f"\n[정제 완료 데이터]")
print(f"{'이름':<8} {'나이':>4} {'점수':>4} {'도시':<6} {'비고'}")
print("-" * 46)
for r in cleaned:
    notes = []
    if r["나이_대체"]:
        notes.append("나이 대체")
    if r["점수_대체"]:
        notes.append("점수 대체")
    if r["이메일"] is None:
        notes.append("이메일 없음")
    note_str = ", ".join(notes) if notes else "-"
    print(f"{r['이름']:<8} {r['나이']:>4} {r['점수']:>4} {r['도시']:<6} {note_str}")

# 정제 요약
total = len(cleaned)
age_missing = sum(1 for r in cleaned if r["나이_대체"])
score_missing = sum(1 for r in cleaned if r["점수_대체"])
email_missing = sum(1 for r in cleaned if r["이메일"] is None)

print(f"\n[정제 요약]")
print(f"  전체 레코드  : {total}건")
print(f"  나이 결측/오류: {age_missing}건 (평균값 대체)")
print(f"  점수 결측/오류: {score_missing}건 (평균값 대체)")
print(f"  이메일 문제   : {email_missing}건")
