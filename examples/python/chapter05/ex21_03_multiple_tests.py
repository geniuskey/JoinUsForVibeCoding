"""
예제 21-03: 여러 테스트 케이스
- 다양한 assert 메서드를 활용한 테스트 작성
- unittest가 제공하는 풍부한 검증 도구를 배웁니다
"""

import unittest


# ============================================================
# 테스트할 함수들
# ============================================================
def get_grade(score):
    """점수에 따른 학점을 반환합니다."""
    if not isinstance(score, (int, float)):
        raise TypeError("점수는 숫자여야 합니다")
    if score < 0 or score > 100:
        raise ValueError("점수는 0~100 사이여야 합니다")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def is_even(n):
    """짝수인지 확인합니다."""
    return n % 2 == 0


def get_unique_items(items):
    """리스트에서 중복을 제거하고 정렬된 리스트를 반환합니다."""
    return sorted(set(items))


def find_max(numbers):
    """리스트에서 최대값을 찾습니다. 빈 리스트면 None을 반환합니다."""
    if not numbers:
        return None
    return max(numbers)


# ============================================================
# 테스트 클래스 1: assertEqual과 assertNotEqual
# ============================================================
class TestGrade(unittest.TestCase):
    """학점 계산 함수 테스트 - assertEqual / assertNotEqual 사용"""

    def test_grade_a(self):
        """90점 이상은 A학점"""
        self.assertEqual(get_grade(95), "A")
        self.assertEqual(get_grade(90), "A")
        self.assertEqual(get_grade(100), "A")

    def test_grade_b(self):
        """80~89점은 B학점"""
        self.assertEqual(get_grade(85), "B")
        self.assertNotEqual(get_grade(85), "A")  # B는 A가 아닙니다

    def test_grade_f(self):
        """60점 미만은 F학점"""
        self.assertEqual(get_grade(50), "F")
        self.assertEqual(get_grade(0), "F")


# ============================================================
# 테스트 클래스 2: assertTrue와 assertFalse
# ============================================================
class TestEvenOdd(unittest.TestCase):
    """짝수/홀수 판별 테스트 - assertTrue / assertFalse 사용"""

    def test_even_numbers(self):
        """짝수 확인"""
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(100))

    def test_odd_numbers(self):
        """홀수 확인"""
        self.assertFalse(is_even(1))
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(99))


# ============================================================
# 테스트 클래스 3: assertIn, assertNotIn, assertIsNone, assertIsNotNone
# ============================================================
class TestCollectionOperations(unittest.TestCase):
    """컬렉션 관련 테스트 - assertIn / assertIsNone 등 사용"""

    def test_unique_items(self):
        """중복 제거 테스트"""
        result = get_unique_items([3, 1, 2, 1, 3])
        self.assertEqual(result, [1, 2, 3])

    def test_item_in_result(self):
        """결과에 특정 항목이 포함되는지 확인"""
        result = get_unique_items(["사과", "바나나", "사과", "체리"])
        self.assertIn("바나나", result)       # "바나나"가 포함되어야 함
        self.assertNotIn("포도", result)       # "포도"는 포함되지 않아야 함

    def test_find_max_with_values(self):
        """최대값 찾기 - 값이 있는 경우"""
        result = find_max([3, 7, 1, 9, 4])
        self.assertIsNotNone(result)           # None이 아니어야 함
        self.assertEqual(result, 9)

    def test_find_max_empty(self):
        """최대값 찾기 - 빈 리스트인 경우"""
        result = find_max([])
        self.assertIsNone(result)              # None이어야 함


# ============================================================
# 테스트 클래스 4: assertGreater, assertLess, assertAlmostEqual
# ============================================================
class TestNumericComparisons(unittest.TestCase):
    """수치 비교 테스트 - assertGreater / assertAlmostEqual 등 사용"""

    def test_greater_less(self):
        """크기 비교 테스트"""
        self.assertGreater(10, 5)              # 10 > 5
        self.assertLess(3, 7)                  # 3 < 7
        self.assertGreaterEqual(5, 5)          # 5 >= 5
        self.assertLessEqual(4, 4)             # 4 <= 4

    def test_almost_equal(self):
        """부동소수점 비교 테스트 (근사값 비교)"""
        # 부동소수점 연산은 정확하지 않을 수 있으므로 assertAlmostEqual 사용
        result = 0.1 + 0.2
        # self.assertEqual(result, 0.3)  # 이건 실패할 수 있음!
        self.assertAlmostEqual(result, 0.3, places=7)  # 소수 7자리까지 비교

    def test_is_instance(self):
        """타입 확인 테스트"""
        self.assertIsInstance(get_grade(95), str)   # 결과가 문자열인지 확인
        self.assertIsInstance(42, int)               # 정수 타입 확인
        self.assertNotIsInstance("hello", int)       # 문자열은 int가 아님


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-03: 다양한 assert 메서드 활용")
    print("=" * 60)
    print()
    print("사용된 assert 메서드 목록:")
    print("  - assertEqual(a, b)       : a == b 인지 확인")
    print("  - assertNotEqual(a, b)    : a != b 인지 확인")
    print("  - assertTrue(x)           : x가 True인지 확인")
    print("  - assertFalse(x)          : x가 False인지 확인")
    print("  - assertIn(a, b)          : a가 b에 포함되는지 확인")
    print("  - assertNotIn(a, b)       : a가 b에 없는지 확인")
    print("  - assertIsNone(x)         : x가 None인지 확인")
    print("  - assertIsNotNone(x)      : x가 None이 아닌지 확인")
    print("  - assertGreater(a, b)     : a > b 인지 확인")
    print("  - assertLess(a, b)        : a < b 인지 확인")
    print("  - assertAlmostEqual(a, b) : 부동소수점 근사 비교")
    print("  - assertIsInstance(a, T)  : a가 타입 T인지 확인")
    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
