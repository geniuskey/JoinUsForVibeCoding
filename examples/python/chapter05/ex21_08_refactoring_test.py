"""
예제 21-08: 리팩토링 후 테스트 확인
- 기존 코드를 리팩토링한 후 테스트가 여전히 통과하는지 확인합니다
- 테스트가 있으면 안심하고 코드를 개선할 수 있음을 보여줍니다

시나리오: 학생 성적 관리 시스템을 리팩토링합니다
"""

import unittest


# ============================================================
# 리팩토링 전 (Before): 모든 로직이 하나의 함수에 몰려 있음
# ============================================================
def calculate_student_result_before(scores):
    """리팩토링 전: 한 함수에 모든 로직이 몰려 있는 코드

    점수 리스트를 받아서 평균, 학점, 통과 여부를 반환합니다.
    """
    if not scores:
        return {"average": 0, "grade": "F", "passed": False}

    total = 0
    for s in scores:
        total = total + s
    avg = total / len(scores)

    # 학점 계산
    if avg >= 90:
        grade = "A"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    elif avg >= 60:
        grade = "D"
    else:
        grade = "F"

    # 통과 여부
    passed = avg >= 60

    return {"average": round(avg, 1), "grade": grade, "passed": passed}


# ============================================================
# 리팩토링 후 (After): 역할별로 함수를 분리
# ============================================================
def calculate_average(scores):
    """점수 리스트의 평균을 계산합니다."""
    if not scores:
        return 0
    return round(sum(scores) / len(scores), 1)


def determine_grade(average):
    """평균 점수에 따른 학점을 결정합니다."""
    grade_thresholds = [
        (90, "A"),
        (80, "B"),
        (70, "C"),
        (60, "D"),
    ]
    for threshold, grade in grade_thresholds:
        if average >= threshold:
            return grade
    return "F"


def is_passed(average, passing_score=60):
    """통과 여부를 판단합니다."""
    return average >= passing_score


def calculate_student_result_after(scores):
    """리팩토링 후: 각 역할을 분리하여 깔끔해진 코드"""
    avg = calculate_average(scores)
    grade = determine_grade(avg)
    passed = is_passed(avg)
    return {"average": avg, "grade": grade, "passed": passed}


# ============================================================
# 테스트: 리팩토링 전후 결과가 동일한지 확인
# ============================================================
class TestStudentResultConsistency(unittest.TestCase):
    """리팩토링 전후 결과 일관성 테스트"""

    def test_same_result_high_scores(self):
        """높은 점수: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [95, 88, 92, 100]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)

    def test_same_result_low_scores(self):
        """낮은 점수: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [40, 55, 30, 45]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)

    def test_same_result_mixed_scores(self):
        """혼합 점수: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [70, 85, 60, 90]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)

    def test_same_result_empty(self):
        """빈 리스트: 리팩토링 전후 결과가 동일해야 합니다"""
        before = calculate_student_result_before([])
        after = calculate_student_result_after([])
        self.assertEqual(before, after)

    def test_same_result_single_score(self):
        """점수 하나: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [75]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)


# ============================================================
# 테스트: 분리된 각 함수가 정확하게 동작하는지 확인
# ============================================================
class TestRefactoredFunctions(unittest.TestCase):
    """리팩토링 후 분리된 함수들의 개별 테스트"""

    # --- calculate_average 테스트 ---
    def test_average_normal(self):
        """일반적인 평균 계산"""
        self.assertEqual(calculate_average([80, 90, 100]), 90.0)

    def test_average_empty(self):
        """빈 리스트의 평균"""
        self.assertEqual(calculate_average([]), 0)

    def test_average_single(self):
        """원소 하나의 평균"""
        self.assertEqual(calculate_average([75]), 75.0)

    def test_average_decimal(self):
        """소수점이 나오는 경우"""
        self.assertEqual(calculate_average([70, 80, 85]), 78.3)

    # --- determine_grade 테스트 ---
    def test_grade_a(self):
        self.assertEqual(determine_grade(95), "A")
        self.assertEqual(determine_grade(90), "A")

    def test_grade_b(self):
        self.assertEqual(determine_grade(85), "B")
        self.assertEqual(determine_grade(80), "B")

    def test_grade_c(self):
        self.assertEqual(determine_grade(75), "C")

    def test_grade_d(self):
        self.assertEqual(determine_grade(65), "D")

    def test_grade_f(self):
        self.assertEqual(determine_grade(50), "F")
        self.assertEqual(determine_grade(0), "F")

    # --- is_passed 테스트 ---
    def test_passed(self):
        self.assertTrue(is_passed(60))
        self.assertTrue(is_passed(100))

    def test_failed(self):
        self.assertFalse(is_passed(59))
        self.assertFalse(is_passed(0))

    def test_custom_passing_score(self):
        """커스텀 합격 점수 사용"""
        self.assertTrue(is_passed(70, passing_score=70))
        self.assertFalse(is_passed(69, passing_score=70))


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-08: 리팩토링 후 테스트 확인")
    print("=" * 60)
    print()
    print("리팩토링 전:")
    print("  - calculate_student_result_before()")
    print("  - 한 함수에 모든 로직(평균, 학점, 통과 여부)이 몰려 있음")
    print()
    print("리팩토링 후:")
    print("  - calculate_average()  : 평균 계산만 담당")
    print("  - determine_grade()    : 학점 결정만 담당")
    print("  - is_passed()          : 통과 여부만 담당")
    print("  - calculate_student_result_after() : 위 함수들을 조합")
    print()
    print("테스트의 역할:")
    print("  - 리팩토링 전후 결과가 동일한지 보장합니다")
    print("  - 분리된 각 함수가 정확하게 동작하는지 확인합니다")
    print("  - 테스트가 있으니 안심하고 코드를 개선할 수 있습니다!")
    print()

    # 리팩토링 전후 비교 데모
    print("-" * 60)
    print("리팩토링 전후 결과 비교 데모:")
    print("-" * 60)
    test_scores = [85, 92, 78, 95, 88]
    before = calculate_student_result_before(test_scores)
    after = calculate_student_result_after(test_scores)
    print(f"  점수: {test_scores}")
    print(f"  리팩토링 전: {before}")
    print(f"  리팩토링 후: {after}")
    print(f"  결과 동일: {before == after}")
    print()

    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
