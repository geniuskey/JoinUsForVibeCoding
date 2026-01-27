"""
예제 12-9: 실습 — 스파게티 코드 리팩토링
==========================================
뒤엉킨 스파게티 코드를 깔끔한 함수 구조로 리팩토링하는 실습입니다.

프롬프트: "이 코드가 너무 지저분해. 깔끔하게 리팩토링해줘"
→ 전역 변수, 중복, 깊은 중첩을 제거하고 함수 단위로 정리합니다.
"""


# ====================================================================
# 개선 전: 스파게티 코드 — 학생 성적 관리 스크립트
# ====================================================================
def run_spaghetti_version():
    """스파게티 코드 버전 (모든 것이 뒤엉킨 상태)"""
    data = [
        ("김철수", 85, 90, 78),
        ("이영희", 92, 88, 95),
        ("박민수", 76, 65, 88),
        ("정수진", 98, 95, 92),
        ("최동욱", 45, 50, 55),
    ]
    print("===== 성적 처리 결과 =====")
    total_k = 0
    total_e = 0
    total_m = 0
    cnt = 0
    for d in data:
        cnt = cnt + 1
        total_k = total_k + d[1]
        total_e = total_e + d[2]
        total_m = total_m + d[3]
    avg_k = total_k / cnt
    avg_e = total_e / cnt
    avg_m = total_m / cnt
    print(f"과목 평균 — 국어: {avg_k:.1f}, 영어: {avg_e:.1f}, 수학: {avg_m:.1f}")
    # 개인별 처리
    for d in data:
        s = d[1] + d[2] + d[3]
        a = s / 3
        if a >= 90:
            g = "A"
        else:
            if a >= 80:
                g = "B"
            else:
                if a >= 70:
                    g = "C"
                else:
                    if a >= 60:
                        g = "D"
                    else:
                        g = "F"
        if g == "F":
            w = " [경고: 재시험 대상]"
        else:
            w = ""
        print(f"  {d[0]}: 합계={s}, 평균={a:.1f}, 등급={g}{w}")
    # 1등 찾기
    best_name = ""
    best_avg = 0
    for d in data:
        s = d[1] + d[2] + d[3]
        a = s / 3
        if a > best_avg:
            best_avg = a
            best_name = d[0]
    print(f"수석: {best_name} (평균: {best_avg:.1f})")


# ====================================================================
# 개선 후: 리팩토링된 코드 — 깔끔한 함수 구조
# ====================================================================

# 데이터 구조 정의
def create_student(name, korean, english, math):
    """학생 데이터를 딕셔너리로 생성합니다."""
    return {
        "name": name,
        "korean": korean,
        "english": english,
        "math": math,
    }


def calculate_total(student):
    """학생의 총점을 계산합니다."""
    return student["korean"] + student["english"] + student["math"]


def calculate_average(student):
    """학생의 평균을 계산합니다."""
    return calculate_total(student) / 3


def determine_grade(average):
    """평균 점수에 따른 등급을 결정합니다."""
    thresholds = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]
    for threshold, grade in thresholds:
        if average >= threshold:
            return grade
    return "F"


def needs_reexam(grade):
    """재시험 대상 여부를 확인합니다."""
    return grade == "F"


def calculate_subject_averages(students):
    """과목별 평균을 계산합니다."""
    subjects = ["korean", "english", "math"]
    count = len(students)
    return {
        subject: sum(s[subject] for s in students) / count
        for subject in subjects
    }


def find_top_student(students):
    """최고 성적 학생을 찾습니다."""
    return max(students, key=calculate_average)


def print_report(students):
    """성적 보고서를 출력합니다."""
    print("===== 성적 처리 결과 =====")

    # 과목별 평균
    subject_avgs = calculate_subject_averages(students)
    subject_names = {"korean": "국어", "english": "영어", "math": "수학"}
    avg_parts = [f"{subject_names[s]}: {v:.1f}" for s, v in subject_avgs.items()]
    print(f"과목 평균 — {', '.join(avg_parts)}")

    # 개인별 성적
    for student in students:
        total = calculate_total(student)
        average = calculate_average(student)
        grade = determine_grade(average)
        warning = " [경고: 재시험 대상]" if needs_reexam(grade) else ""
        print(f"  {student['name']}: 합계={total}, 평균={average:.1f}, 등급={grade}{warning}")

    # 수석
    top = find_top_student(students)
    top_avg = calculate_average(top)
    print(f"수석: {top['name']} (평균: {top_avg:.1f})")


def run_refactored_version():
    """리팩토링된 버전 실행"""
    students = [
        create_student("김철수", 85, 90, 78),
        create_student("이영희", 92, 88, 95),
        create_student("박민수", 76, 65, 88),
        create_student("정수진", 98, 95, 92),
        create_student("최동욱", 45, 50, 55),
    ]
    print_report(students)


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-9] 스파게티 코드 리팩토링")
    print("=" * 55)

    print("\n[개선 전] 스파게티 코드")
    print("-" * 40)
    run_spaghetti_version()

    print()
    print("[개선 후] 리팩토링된 코드")
    print("-" * 40)
    run_refactored_version()

    print()
    print("[리팩토링 요약]")
    print("-" * 55)
    improvements = [
        ("튜플 → 딕셔너리", "d[1] → student['korean']", "의미 명확"),
        ("중첩 if → 테이블", "if/else 5단계 → 리스트 순회", "확장 용이"),
        ("중복 계산 제거", "합계/평균 2회 → 함수 호출", "유지보수 쉬움"),
        ("함수 분리", "1개 블록 → 7개 함수", "테스트 가능"),
        ("매직 넘버 제거", "3, 90, 80... → 명명된 구조", "의미 명확"),
    ]
    for before, change, benefit in improvements:
        print(f"  {before:<18} {change:<30} → {benefit}")

    print()
    print("Tip: AI에게 '이 코드를 리팩토링해줘'라고 요청할 때,")
    print("     구체적으로 어떤 부분이 불만인지 말해주면 더 좋은 결과를 얻습니다.")
    print("     예: '중첩 if를 줄여줘', '함수로 분리해줘', '변수명을 개선해줘'")
