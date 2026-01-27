"""
예제 13-10: 스택 트레이스 분석 — 중첩 함수 호출에서의 오류
============================================================
여러 함수가 순서대로 호출되는 과정에서 발생하는 오류를
스택 트레이스를 통해 추적하는 방법을 보여줍니다.
"""

# 버그가 있는 코드: 중첩 함수 호출 체인에서 오류 발생
def calculate_average(numbers):
    """평균을 계산하는 함수"""
    total = sum(numbers)
    average = total / len(numbers)    # ← 빈 리스트이면 ZeroDivisionError!
    return average


def get_class_average(students):
    """반 전체 평균을 계산하는 함수"""
    all_scores = []
    for student in students:
        all_scores.extend(student["scores"])
    return calculate_average(all_scores)


def generate_report(class_name, students):
    """성적 보고서를 생성하는 함수"""
    print(f"=== {class_name} 성적 보고서 ===")
    avg = get_class_average(students)
    print(f"반 평균: {avg:.1f}점")
    return avg


# 실행 — 학생 데이터에 점수가 없는 경우
students = [
    {"name": "김철수", "scores": []},   # ← 점수가 비어 있음!
    {"name": "이영희", "scores": []},   # ← 점수가 비어 있음!
]

generate_report("3학년 1반", students)
