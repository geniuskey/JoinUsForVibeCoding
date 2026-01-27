#!/usr/bin/env python3
"""예제 16-05: 중첩 JSON 처리

깊이 중첩된 JSON 구조를 탐색하고 필요한 데이터를 추출합니다.
"""

import json

# 중첩된 JSON 데이터 (회사 조직도)
json_string = '''
{
    "회사명": "테크스타트",
    "설립년도": 2020,
    "부서": {
        "개발팀": {
            "팀장": "김개발",
            "인원수": 8,
            "프로젝트": [
                {"이름": "프론트엔드 개선", "상태": "진행중", "예산": 5000},
                {"이름": "API 리팩토링", "상태": "완료", "예산": 3000},
                {"이름": "모바일 앱", "상태": "계획중", "예산": 8000}
            ],
            "기술스택": ["Python", "JavaScript", "React", "Docker"]
        },
        "디자인팀": {
            "팀장": "이디자인",
            "인원수": 5,
            "프로젝트": [
                {"이름": "UI 리뉴얼", "상태": "진행중", "예산": 4000},
                {"이름": "브랜딩", "상태": "완료", "예산": 2000}
            ],
            "기술스택": ["Figma", "Photoshop", "Illustrator"]
        },
        "마케팅팀": {
            "팀장": "박마케팅",
            "인원수": 4,
            "프로젝트": [
                {"이름": "SNS 캠페인", "상태": "진행중", "예산": 6000},
                {"이름": "콘텐츠 마케팅", "상태": "진행중", "예산": 3500}
            ],
            "기술스택": ["Google Analytics", "HubSpot"]
        }
    }
}
'''

data = json.loads(json_string)

print("=" * 50)
print(f"  {data['회사명']} (설립: {data['설립년도']}년)")
print("=" * 50)

# 부서별 정보 탐색
departments = data["부서"]
total_employees = 0
total_budget = 0
all_projects = []

for dept_name, dept_info in departments.items():
    total_employees += dept_info["인원수"]
    print(f"\n[{dept_name}]")
    print(f"  팀장  : {dept_info['팀장']}")
    print(f"  인원  : {dept_info['인원수']}명")
    print(f"  기술  : {', '.join(dept_info['기술스택'])}")

    # 프로젝트 정보 추출
    print(f"  프로젝트:")
    for proj in dept_info["프로젝트"]:
        status_icon = {"진행중": "●", "완료": "✓", "계획중": "○"}
        icon = status_icon.get(proj["상태"], "?")
        print(f"    {icon} {proj['이름']} ({proj['상태']}) - {proj['예산']:,}만원")
        total_budget += proj["예산"]
        all_projects.append({**proj, "부서": dept_name})

# 전체 요약
print("\n" + "=" * 50)
print("  전체 요약")
print("=" * 50)
print(f"  총 부서 수     : {len(departments)}개")
print(f"  총 직원 수     : {total_employees}명")
print(f"  총 프로젝트 수 : {len(all_projects)}개")
print(f"  총 예산        : {total_budget:,}만원")

# 상태별 프로젝트 분류
print(f"\n[상태별 프로젝트 현황]")
for status in ["진행중", "완료", "계획중"]:
    projects = [p for p in all_projects if p["상태"] == status]
    if projects:
        budget_sum = sum(p["예산"] for p in projects)
        print(f"  {status}: {len(projects)}건 (예산 {budget_sum:,}만원)")
        for p in projects:
            print(f"    - {p['이름']} ({p['부서']})")
