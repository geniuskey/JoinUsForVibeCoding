#!/usr/bin/env python3
"""예제 16-11: 설문 결과 분석기

설문조사 응답 데이터를 분석하고 결과를 시각화합니다.
"""

import json
import statistics
from collections import Counter, defaultdict

# 설문조사 응답 데이터 (JSON 형태)
survey_json = '''
{
    "설문제목": "개발자 도구 사용 현황 조사",
    "조사기간": "2024-10-01 ~ 2024-10-31",
    "응답자수": 20,
    "응답": [
        {"이름": "응답자01", "연차": 1, "주언어": "Python", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자02", "연차": 3, "주언어": "JavaScript", "만족도": 5, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자03", "연차": 5, "주언어": "Java", "만족도": 3, "AI도구사용": "아니오", "선호에디터": "IntelliJ"},
        {"이름": "응답자04", "연차": 2, "주언어": "Python", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자05", "연차": 7, "주언어": "Java", "만족도": 3, "AI도구사용": "아니오", "선호에디터": "IntelliJ"},
        {"이름": "응답자06", "연차": 1, "주언어": "Python", "만족도": 5, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자07", "연차": 4, "주언어": "JavaScript", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자08", "연차": 2, "주언어": "TypeScript", "만족도": 5, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자09", "연차": 10, "주언어": "C++", "만족도": 2, "AI도구사용": "아니오", "선호에디터": "Vim"},
        {"이름": "응답자10", "연차": 3, "주언어": "Python", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자11", "연차": 6, "주언어": "Go", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자12", "연차": 1, "주언어": "Python", "만족도": 5, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자13", "연차": 8, "주언어": "Java", "만족도": 3, "AI도구사용": "아니오", "선호에디터": "IntelliJ"},
        {"이름": "응답자14", "연차": 2, "주언어": "JavaScript", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자15", "연차": 4, "주언어": "TypeScript", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자16", "연차": 3, "주언어": "Python", "만족도": 5, "AI도구사용": "예", "선호에디터": "PyCharm"},
        {"이름": "응답자17", "연차": 5, "주언어": "Go", "만족도": 3, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자18", "연차": 1, "주언어": "Python", "만족도": 4, "AI도구사용": "예", "선호에디터": "VS Code"},
        {"이름": "응답자19", "연차": 9, "주언어": "C++", "만족도": 2, "AI도구사용": "아니오", "선호에디터": "Vim"},
        {"이름": "응답자20", "연차": 2, "주언어": "JavaScript", "만족도": 5, "AI도구사용": "예", "선호에디터": "VS Code"}
    ]
}
'''

data = json.loads(survey_json)
responses = data["응답"]

print("╔" + "═" * 50 + "╗")
print("║" + f"  {data['설문제목']}".ljust(50) + "║")
print("║" + f"  조사기간: {data['조사기간']}".ljust(50) + "║")
print("║" + f"  총 응답자: {data['응답자수']}명".ljust(50) + "║")
print("╚" + "═" * 50 + "╝")

# === 1. 주 사용 언어 분포 ===
lang_counter = Counter(r["주언어"] for r in responses)
print(f"\n[1] 주 사용 프로그래밍 언어")
print("-" * 45)
for lang, count in lang_counter.most_common():
    pct = count / len(responses) * 100
    bar = "█" * (count * 2)
    print(f"  {lang:<12} {bar} {count}명 ({pct:.0f}%)")

# === 2. 만족도 분석 ===
satisfactions = [r["만족도"] for r in responses]
print(f"\n[2] 업무 만족도 (1~5점)")
print("-" * 45)
sat_counter = Counter(satisfactions)
for score in range(5, 0, -1):
    count = sat_counter.get(score, 0)
    stars = "★" * score + "☆" * (5 - score)
    bar = "█" * (count * 2)
    print(f"  {stars} ({score}점) {bar} {count}명")

print(f"\n  평균 만족도: {statistics.mean(satisfactions):.1f}점")
print(f"  중앙값    : {statistics.median(satisfactions):.1f}점")

# === 3. AI 도구 사용 현황 ===
ai_users = Counter(r["AI도구사용"] for r in responses)
print(f"\n[3] AI 코딩 도구 사용 여부")
print("-" * 45)
for answer, count in ai_users.most_common():
    pct = count / len(responses) * 100
    bar = "█" * int(pct / 2)
    print(f"  {answer:<6} {bar} {count}명 ({pct:.0f}%)")

# === 4. 연차별 AI 도구 사용률 ===
career_groups = {"주니어(1-3년)": [], "미들(4-6년)": [], "시니어(7년+)": []}
for r in responses:
    year = r["연차"]
    if year <= 3:
        career_groups["주니어(1-3년)"].append(r)
    elif year <= 6:
        career_groups["미들(4-6년)"].append(r)
    else:
        career_groups["시니어(7년+)"].append(r)

print(f"\n[4] 연차별 AI 도구 사용률")
print("-" * 45)
for group, members in career_groups.items():
    total = len(members)
    ai_count = sum(1 for m in members if m["AI도구사용"] == "예")
    pct = ai_count / total * 100 if total > 0 else 0
    filled = int(pct / 100 * 20)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"  {group:<14} {bar} {pct:.0f}% ({ai_count}/{total}명)")

# === 5. 에디터 선호도 ===
editor_counter = Counter(r["선호에디터"] for r in responses)
print(f"\n[5] 선호 에디터")
print("-" * 45)
for editor, count in editor_counter.most_common():
    pct = count / len(responses) * 100
    bar = "█" * count
    print(f"  {editor:<12} {bar} {count}명 ({pct:.0f}%)")

# === 6. 종합 인사이트 ===
most_common_lang = lang_counter.most_common(1)[0]
ai_usage_rate = ai_users["예"] / len(responses) * 100

print(f"\n{'=' * 50}")
print("  종합 인사이트")
print("=" * 50)
print(f"  1. 가장 인기 있는 언어는 {most_common_lang[0]} ({most_common_lang[1]}명)")
print(f"  2. AI 코딩 도구 사용률 {ai_usage_rate:.0f}%")
print(f"  3. 평균 만족도 {statistics.mean(satisfactions):.1f}/5.0")
print(f"  4. 주니어일수록 AI 도구 적극 활용")
print(f"  5. VS Code가 압도적 에디터 점유율")
