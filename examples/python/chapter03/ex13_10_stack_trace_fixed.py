"""
예제 13-10: 스택 트레이스 분석 — 중첩 함수 호출에서의 오류 (수정 완료)
======================================================================
수정: 빈 리스트 체크 추가 + 예외 처리로 안전하게 보호
"""

# 수정된 코드: 빈 리스트 체크 및 예외 처리 추가
def calculate_average(numbers):
    """평균을 계산하는 함수 (안전한 버전)"""
    if not numbers:                  # ← 빈 리스트 체크 추가!
        print("  경고: 점수 데이터가 없습니다.")
        return 0.0
    total = sum(numbers)
    average = total / len(numbers)
    return average


def get_class_average(students):
    """반 전체 평균을 계산하는 함수 (안전한 버전)"""
    all_scores = []
    for student in students:
        scores = student.get("scores", [])    # ← .get()으로 안전 접근
        all_scores.extend(scores)
    return calculate_average(all_scores)


def generate_report(class_name, students):
    """성적 보고서를 생성하는 함수 (안전한 버전)"""
    print(f"=== {class_name} 성적 보고서 ===")
    try:
        avg = get_class_average(students)
        if avg > 0:
            print(f"반 평균: {avg:.1f}점")
        else:
            print("반 평균: 데이터 없음")
    except Exception as e:
        print(f"보고서 생성 중 오류 발생: {e}")
    print()


# 테스트 1: 빈 점수 데이터
students_empty = [
    {"name": "김철수", "scores": []},
    {"name": "이영희", "scores": []},
]
generate_report("3학년 1반 (빈 데이터)", students_empty)

# 테스트 2: 정상 데이터
students_normal = [
    {"name": "김철수", "scores": [85, 90, 78]},
    {"name": "이영희", "scores": [92, 88, 95]},
    {"name": "박민수", "scores": [76, 82, 89]},
]
generate_report("3학년 2반 (정상 데이터)", students_normal)
