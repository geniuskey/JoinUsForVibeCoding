#!/usr/bin/env python3
"""예제 16-06: 데이터 변환 CSV → JSON

CSV 형식의 데이터를 JSON으로 변환합니다.
"""

import csv
import io
import json

# 원본 CSV 데이터
csv_data = """직원ID,이름,부서,직급,연봉
E001,김민수,개발팀,선임,5200
E002,이영희,디자인팀,책임,5800
E003,박철수,개발팀,주임,4200
E004,정미래,마케팅팀,선임,4800
E005,한지우,개발팀,책임,6100
E006,오세훈,디자인팀,주임,3900
E007,최다은,마케팅팀,책임,5500
E008,강준혁,개발팀,주임,4000
"""

print("[원본 CSV 데이터]")
print(csv_data.strip())
print()

# CSV → 딕셔너리 리스트로 파싱
reader = csv.DictReader(io.StringIO(csv_data.strip()))
records = list(reader)

# 숫자 필드 변환
for record in records:
    record["연봉"] = int(record["연봉"])

# 방법 1: 단순 리스트 형태 JSON
simple_json = json.dumps(records, ensure_ascii=False, indent=2)
print("[변환 결과 1: 리스트 형태 JSON]")
print(simple_json[:300] + "..." if len(simple_json) > 300 else simple_json)
print()

# 방법 2: 부서별 그룹화 JSON
grouped = {}
for record in records:
    dept = record["부서"]
    if dept not in grouped:
        grouped[dept] = {
            "부서명": dept,
            "직원수": 0,
            "직원목록": []
        }
    grouped[dept]["직원수"] += 1
    grouped[dept]["직원목록"].append({
        "직원ID": record["직원ID"],
        "이름": record["이름"],
        "직급": record["직급"],
        "연봉": record["연봉"]
    })

# 부서별 평균 연봉 추가
for dept_info in grouped.values():
    salaries = [e["연봉"] for e in dept_info["직원목록"]]
    dept_info["평균연봉"] = round(sum(salaries) / len(salaries))

result = {
    "회사정보": {
        "총직원수": len(records),
        "부서수": len(grouped),
        "평균연봉": round(sum(r["연봉"] for r in records) / len(records))
    },
    "부서별데이터": list(grouped.values())
}

grouped_json = json.dumps(result, ensure_ascii=False, indent=2)
print("[변환 결과 2: 부서별 그룹화 JSON]")
print(grouped_json)
print()

# 변환 결과 요약
print("[변환 요약]")
print(f"  CSV 레코드 수 : {len(records)}건")
print(f"  JSON 부서 수  : {len(grouped)}개")
for dept_name, dept_data in grouped.items():
    print(f"    {dept_name}: {dept_data['직원수']}명 (평균 연봉 {dept_data['평균연봉']:,}만원)")
