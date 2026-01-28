"""
예제 21-04: 예외 테스트
- assertRaises를 사용하여 예외 발생을 검증합니다
- 올바른 예외가 올바른 상황에서 발생하는지 확인합니다
"""

import unittest


# ============================================================
# 테스트할 함수들
# ============================================================
def divide(a, b):
    """나눗셈을 수행합니다. 0으로 나누면 예외를 발생시킵니다."""
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return a / b


def get_element(lst, index):
    """리스트에서 인덱스로 요소를 가져옵니다."""
    if not isinstance(index, int):
        raise TypeError("인덱스는 정수여야 합니다")
    if index < 0 or index >= len(lst):
        raise IndexError(f"인덱스 {index}가 범위를 벗어났습니다 (0~{len(lst)-1})")
    return lst[index]


def parse_age(value):
    """문자열을 나이(정수)로 변환합니다."""
    if not isinstance(value, str):
        raise TypeError("문자열을 입력해야 합니다")
    try:
        age = int(value)
    except ValueError:
        raise ValueError(f"'{value}'는 유효한 숫자가 아닙니다")
    if age < 0:
        raise ValueError("나이는 0 이상이어야 합니다")
    if age > 150:
        raise ValueError("나이는 150 이하여야 합니다")
    return age


# ============================================================
# 테스트 클래스 1: 기본 예외 테스트
# ============================================================
class TestDivide(unittest.TestCase):
    """나눗셈 함수의 예외 테스트"""

    def test_normal_division(self):
        """정상적인 나눗셈"""
        self.assertEqual(divide(10, 2), 5.0)
        self.assertAlmostEqual(divide(1, 3), 0.3333, places=3)

    def test_divide_by_zero(self):
        """0으로 나누면 ZeroDivisionError가 발생해야 합니다"""
        # 방법 1: assertRaises를 컨텍스트 매니저로 사용
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_divide_by_zero_message(self):
        """예외 메시지도 확인합니다"""
        # 방법 2: 컨텍스트 매니저로 예외 객체에 접근
        with self.assertRaises(ZeroDivisionError) as context:
            divide(10, 0)

        # 예외 메시지 확인
        self.assertIn("0으로 나눌 수 없습니다", str(context.exception))


# ============================================================
# 테스트 클래스 2: 다양한 예외 타입 테스트
# ============================================================
class TestGetElement(unittest.TestCase):
    """리스트 요소 접근 예외 테스트"""

    def test_valid_index(self):
        """유효한 인덱스 접근"""
        self.assertEqual(get_element([10, 20, 30], 0), 10)
        self.assertEqual(get_element([10, 20, 30], 2), 30)

    def test_index_out_of_range(self):
        """범위를 벗어난 인덱스 → IndexError"""
        with self.assertRaises(IndexError):
            get_element([10, 20, 30], 5)

    def test_negative_index(self):
        """음수 인덱스 → IndexError"""
        with self.assertRaises(IndexError):
            get_element([10, 20, 30], -1)

    def test_invalid_index_type(self):
        """정수가 아닌 인덱스 → TypeError"""
        with self.assertRaises(TypeError):
            get_element([10, 20, 30], "abc")

    def test_index_error_message(self):
        """IndexError 메시지에 인덱스 정보가 포함되는지 확인"""
        with self.assertRaises(IndexError) as context:
            get_element([10, 20, 30], 10)
        self.assertIn("10", str(context.exception))


# ============================================================
# 테스트 클래스 3: 여러 예외 시나리오
# ============================================================
class TestParseAge(unittest.TestCase):
    """나이 파싱 함수의 예외 테스트"""

    def test_valid_age(self):
        """유효한 나이 문자열"""
        self.assertEqual(parse_age("25"), 25)
        self.assertEqual(parse_age("0"), 0)
        self.assertEqual(parse_age("150"), 150)

    def test_non_string_input(self):
        """문자열이 아닌 입력 → TypeError"""
        with self.assertRaises(TypeError):
            parse_age(25)  # 정수를 직접 전달

    def test_non_numeric_string(self):
        """숫자가 아닌 문자열 → ValueError"""
        with self.assertRaises(ValueError) as context:
            parse_age("스물다섯")
        self.assertIn("유효한 숫자가 아닙니다", str(context.exception))

    def test_negative_age(self):
        """음수 나이 → ValueError"""
        with self.assertRaises(ValueError) as context:
            parse_age("-5")
        self.assertIn("0 이상", str(context.exception))

    def test_too_old(self):
        """너무 큰 나이 → ValueError"""
        with self.assertRaises(ValueError) as context:
            parse_age("200")
        self.assertIn("150 이하", str(context.exception))

    def test_assertRaisesRegex(self):
        """assertRaisesRegex로 예외 메시지를 정규식으로 검증"""
        # 예외 메시지가 정규식 패턴과 일치하는지 확인
        self.assertRaisesRegex(
            ValueError,
            r"유효한 숫자",
            parse_age,
            "abc"
        )


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-04: 예외 테스트 (assertRaises)")
    print("=" * 60)
    print()
    print("예외 테스트가 중요한 이유:")
    print("  - 잘못된 입력에 대해 적절한 에러를 반환하는지 확인")
    print("  - 에러 메시지가 사용자에게 유용한 정보를 제공하는지 확인")
    print("  - 예상치 못한 동작을 사전에 방지")
    print()
    print("사용된 메서드:")
    print("  - assertRaises(예외타입)     : 예외 발생 확인")
    print("  - assertRaisesRegex(예외, 패턴) : 예외 + 메시지 패턴 확인")
    print("  - context.exception          : 발생한 예외 객체 접근")
    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
