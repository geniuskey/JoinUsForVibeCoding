"""
예제 2-1: 2020년 스타일 AI 코딩 vs 현재 바이브 코딩

이 예제는 AI 코딩 방식의 발전을 보여줍니다.
- 과거: 단순 자동완성 (함수 이름만 보고 본문 생성)
- 현재: 대화형 바이브 코딩 (자연어 요청으로 전체 프로그램 생성)
"""

# ============================================
# [과거] 2020년 스타일: 단순 자동완성
# 개발자가 함수 시그니처를 작성하면
# AI가 본문을 자동완성하는 방식
# ============================================

def calculate_average(numbers):
    """숫자 리스트의 평균을 계산합니다."""
    # 2020년 AI: 함수 이름과 파라미터를 보고 단순 자동완성
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


# ============================================
# [현재] 2024-2026년 스타일: 바이브 코딩
# 자연어로 "학생 성적 분석 프로그램 만들어줘"라고 요청하면
# AI가 전체 프로그램을 대화를 통해 생성
# ============================================

def analyze_student_scores(students: dict) -> dict:
    """
    학생 성적을 종합 분석합니다.

    바이브 코딩 요청 예시:
    "학생 이름과 점수를 받아서 평균, 최고점, 최저점,
     등급까지 분석해주는 프로그램을 만들어줘"
    """
    if not students:
        return {"오류": "학생 데이터가 없습니다."}

    scores = list(students.values())
    avg = sum(scores) / len(scores)

    # 등급 계산
    def get_grade(score):
        if score >= 90: return "A"
        elif score >= 80: return "B"
        elif score >= 70: return "C"
        elif score >= 60: return "D"
        else: return "F"

    # 종합 분석 결과
    result = {
        "총 학생 수": len(students),
        "평균 점수": round(avg, 1),
        "최고 점수": max(scores),
        "최저 점수": min(scores),
        "최고 점수 학생": max(students, key=students.get),
        "최저 점수 학생": min(students, key=students.get),
        "학생별 등급": {name: get_grade(score) for name, score in students.items()}
    }
    return result


# 실행
if __name__ == "__main__":
    print("=" * 50)
    print("[과거] 2020년 스타일: 단순 자동완성 결과")
    print("=" * 50)
    numbers = [85, 92, 78, 95, 88]
    avg = calculate_average(numbers)
    print(f"숫자: {numbers}")
    print(f"평균: {avg}")

    print()
    print("=" * 50)
    print("[현재] 바이브 코딩 스타일: 종합 분석 결과")
    print("=" * 50)
    students = {
        "김민수": 95,
        "이서연": 87,
        "박지훈": 72,
        "최은영": 91,
        "정다운": 68
    }

    analysis = analyze_student_scores(students)
    for key, value in analysis.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for name, grade in value.items():
                print(f"  {name}: {grade}")
        else:
            print(f"{key}: {value}")
