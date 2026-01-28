"""
예제 21-01: 첫 번째 테스트 작성
- unittest를 사용한 간단한 함수 테스트
- 바이브 코딩에서 테스트의 기본 구조를 이해합니다
"""

import unittest


# ============================================================
# 테스트할 함수: 두 수를 더하는 간단한 함수
# ============================================================
def add(a, b):
    """두 수를 더해서 반환합니다."""
    return a + b


def multiply(a, b):
    """두 수를 곱해서 반환합니다."""
    return a * b


# ============================================================
# 테스트 클래스: unittest.TestCase를 상속받아 테스트를 작성합니다
# ============================================================
class TestBasicMath(unittest.TestCase):
    """기본 수학 함수에 대한 테스트"""

    def test_add_positive_numbers(self):
        """양수 두 개를 더하는 테스트"""
        result = add(3, 5)
        self.assertEqual(result, 8)  # 3 + 5 = 8이어야 합니다

    def test_add_negative_numbers(self):
        """음수를 포함하는 덧셈 테스트"""
        result = add(-1, -2)
        self.assertEqual(result, -3)  # -1 + (-2) = -3이어야 합니다

    def test_add_zero(self):
        """0을 더하는 테스트"""
        result = add(10, 0)
        self.assertEqual(result, 10)  # 10 + 0 = 10이어야 합니다

    def test_multiply_basic(self):
        """기본 곱셈 테스트"""
        result = multiply(4, 3)
        self.assertEqual(result, 12)  # 4 × 3 = 12이어야 합니다

    def test_multiply_by_zero(self):
        """0을 곱하는 테스트"""
        result = multiply(5, 0)
        self.assertEqual(result, 0)  # 5 × 0 = 0이어야 합니다


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-01: 첫 번째 테스트 작성")
    print("=" * 60)
    print()
    print("📋 테스트 설명:")
    print("  - add() 함수: 두 수를 더합니다")
    print("  - multiply() 함수: 두 수를 곱합니다")
    print("  - unittest.TestCase를 상속받아 테스트를 작성합니다")
    print("  - assertEqual()로 기대값과 실제값을 비교합니다")
    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    # unittest 실행 (verbosity=2로 상세 출력)
    unittest.main(verbosity=2)
