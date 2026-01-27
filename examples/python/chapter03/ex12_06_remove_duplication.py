"""
예제 12-6: 중복 코드 제거 요청
================================
반복되는 코드 패턴을 공통 함수로 추출하도록 AI에게 요청하는 예제입니다.

프롬프트: "중복되는 코드가 많아. 공통 함수로 묶어줘"
→ 반복 로직을 한 곳에 모아 유지보수성을 높입니다.
"""


# --- 개선 전: 중복 코드가 가득한 데이터 처리 ---
def process_students_before():
    """학생 데이터 처리 — 중복 코드가 많은 버전"""
    students = [
        {"name": "김철수", "korean": 85, "english": 90, "math": 78},
        {"name": "이영희", "korean": 92, "english": 88, "math": 95},
        {"name": "박민수", "korean": 76, "english": 82, "math": 88},
    ]

    # 국어 평균 계산 (중복 패턴 1)
    korean_total = 0
    for student in students:
        korean_total += student["korean"]
    korean_avg = korean_total / len(students)

    # 영어 평균 계산 (중복 패턴 2 — 같은 구조 반복)
    english_total = 0
    for student in students:
        english_total += student["english"]
    english_avg = english_total / len(students)

    # 수학 평균 계산 (중복 패턴 3 — 같은 구조 반복)
    math_total = 0
    for student in students:
        math_total += student["math"]
    math_avg = math_total / len(students)

    # 국어 최고 점수 (중복 패턴 4)
    korean_best = ""
    korean_max = 0
    for student in students:
        if student["korean"] > korean_max:
            korean_max = student["korean"]
            korean_best = student["name"]

    # 영어 최고 점수 (중복 패턴 5 — 같은 구조 반복)
    english_best = ""
    english_max = 0
    for student in students:
        if student["english"] > english_max:
            english_max = student["english"]
            english_best = student["name"]

    # 수학 최고 점수 (중복 패턴 6 — 같은 구조 반복)
    math_best = ""
    math_max = 0
    for student in students:
        if student["math"] > math_max:
            math_max = student["math"]
            math_best = student["name"]

    print("  과목별 평균:")
    print(f"    국어: {korean_avg:.1f}  영어: {english_avg:.1f}  수학: {math_avg:.1f}")
    print("  과목별 최고 점수:")
    print(f"    국어: {korean_best}({korean_max})  영어: {english_best}({english_max})  수학: {math_best}({math_max})")


# --- "중복 코드를 공통 함수로 묶어줘" 요청 후 개선된 코드 ---
def calculate_subject_average(students, subject):
    """특정 과목의 평균 점수를 계산합니다."""
    total = sum(student[subject] for student in students)
    return total / len(students)


def find_top_student(students, subject):
    """특정 과목의 최고 점수 학생을 찾습니다."""
    top = max(students, key=lambda s: s[subject])
    return top["name"], top[subject]


def process_students_after():
    """학생 데이터 처리 — 중복 제거 버전"""
    students = [
        {"name": "김철수", "korean": 85, "english": 90, "math": 78},
        {"name": "이영희", "korean": 92, "english": 88, "math": 95},
        {"name": "박민수", "korean": 76, "english": 82, "math": 88},
    ]
    subjects = ["korean", "english", "math"]
    subject_names = {"korean": "국어", "english": "영어", "math": "수학"}

    # 평균 계산 — 공통 함수 활용
    print("  과목별 평균:")
    avgs = []
    for subj in subjects:
        avg = calculate_subject_average(students, subj)
        avgs.append(f"{subject_names[subj]}: {avg:.1f}")
    print(f"    {'  '.join(avgs)}")

    # 최고 점수 — 공통 함수 활용
    print("  과목별 최고 점수:")
    tops = []
    for subj in subjects:
        name, score = find_top_student(students, subj)
        tops.append(f"{subject_names[subj]}: {name}({score})")
    print(f"    {'  '.join(tops)}")


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-6] 중복 코드 제거 요청")
    print("=" * 55)

    print("\n[개선 전] 중복 코드 (약 40줄)")
    print("-" * 40)
    process_students_before()

    print()
    print("[개선 후] 공통 함수 활용 (약 15줄 + 함수 2개)")
    print("-" * 40)
    process_students_after()

    print()
    print("[코드량 비교]")
    print(f"  개선 전: 약 40줄 (동일 패턴 6회 반복)")
    print(f"  개선 후: 약 20줄 (공통 함수 2개 + 루프)")
    print(f"  절감율: 약 50%")
    print()
    print("Tip: 비슷한 코드가 3번 이상 반복되면 함수로 추출하세요.")
    print("     AI에게 '중복 코드를 묶어줘'라고 요청하면 됩니다.")
