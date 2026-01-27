"""
예제 10-6: 출력 형식 지정하기
==============================
같은 데이터라도 출력 형식을 명시하면
AI가 원하는 형태로 정확히 코드를 생성합니다.

프롬프트: "학생 성적 데이터를 다음 3가지 형식으로 출력하는 함수를 각각 만들어줘:
         1) JSON 형식
         2) 표(table) 형식
         3) 마크다운 리스트 형식"
"""

import json


# 샘플 데이터
STUDENTS = [
    {"name": "김바이브", "math": 95, "english": 88, "science": 92},
    {"name": "이코딩",  "math": 82, "english": 95, "science": 78},
    {"name": "박프롬",  "math": 90, "english": 72, "science": 85},
    {"name": "최에이",  "math": 78, "english": 90, "science": 95},
]


def output_as_json(students):
    """JSON 형식으로 출력합니다."""
    result = []
    for s in students:
        avg = round((s["math"] + s["english"] + s["science"]) / 3, 1)
        result.append({
            "이름": s["name"],
            "수학": s["math"],
            "영어": s["english"],
            "과학": s["science"],
            "평균": avg,
        })
    return json.dumps(result, ensure_ascii=False, indent=2)


def output_as_table(students):
    """표(table) 형식으로 출력합니다."""
    header = f"{'이름':<10} {'수학':>6} {'영어':>6} {'과학':>6} {'평균':>6}"
    separator = "-" * len(header)
    lines = [header, separator]

    for s in students:
        avg = round((s["math"] + s["english"] + s["science"]) / 3, 1)
        lines.append(
            f"{s['name']:<10} {s['math']:>6} {s['english']:>6} "
            f"{s['science']:>6} {avg:>6}"
        )

    lines.append(separator)
    return "\n".join(lines)


def output_as_markdown_list(students):
    """마크다운 리스트 형식으로 출력합니다."""
    lines = ["# 학생 성적표\n"]

    for s in students:
        avg = round((s["math"] + s["english"] + s["science"]) / 3, 1)
        lines.append(f"- **{s['name']}**")
        lines.append(f"  - 수학: {s['math']}점")
        lines.append(f"  - 영어: {s['english']}점")
        lines.append(f"  - 과학: {s['science']}점")
        lines.append(f"  - 평균: **{avg}점**")
        lines.append("")

    return "\n".join(lines)


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[형식 1] JSON 출력")
    print("=" * 55)
    print(output_as_json(STUDENTS))

    print()
    print("=" * 55)
    print("[형식 2] 표(Table) 출력")
    print("=" * 55)
    print(output_as_table(STUDENTS))

    print()
    print("=" * 55)
    print("[형식 3] 마크다운 리스트 출력")
    print("=" * 55)
    print(output_as_markdown_list(STUDENTS))
