"""
예제 21-07: Red-Green-Refactor 사이클 데모
- 테스트 실패(Red) → 구현(Green) → 리팩토링(Refactor)의 TDD 사이클을 보여줍니다
- 각 단계를 순서대로 시연합니다

시나리오: 간단한 계산기(Calculator) 클래스를 TDD로 만들어봅니다
"""

import unittest
import io
import sys


# ============================================================
# TDD 사이클을 직접 시연하는 데모 코드
# ============================================================

def run_tests_silently(test_class):
    """테스트를 실행하고 결과를 반환합니다 (출력 억제)."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)
    result = runner.run(suite)
    return result


# ============================================================
# 1단계 [Red]: 테스트를 먼저 작성 (아직 구현 없음)
# ============================================================
# 이 단계에서는 Calculator 클래스가 아직 없다고 가정합니다.
# 아래처럼 빈 클래스만 있는 상태에서 시작합니다.

class CalculatorV1:
    """버전 1: 빈 클래스 (아직 구현 없음)"""
    pass


class TestCalculatorRed(unittest.TestCase):
    """Red 단계: 실패하는 테스트"""

    def test_add(self):
        calc = CalculatorV1()
        # CalculatorV1에는 add 메서드가 없으므로 실패!
        result = calc.add(2, 3)
        self.assertEqual(result, 5)


# ============================================================
# 2단계 [Green]: 테스트를 통과하는 최소한의 구현
# ============================================================

class CalculatorV2:
    """버전 2: 최소한의 구현 (테스트를 통과시키기 위한)"""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b


class TestCalculatorGreen(unittest.TestCase):
    """Green 단계: 통과하는 테스트"""

    def setUp(self):
        self.calc = CalculatorV2()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)


# ============================================================
# 3단계 [Refactor]: 코드 개선 (기능은 동일, 구조 개선)
# ============================================================

class CalculatorV3:
    """버전 3: 리팩토링된 버전
    - 연산 이력(history)을 기록합니다
    - 코드 구조를 개선했습니다
    """

    def __init__(self):
        self.history = []

    def _record(self, expression, result):
        """연산 이력을 기록합니다."""
        self.history.append(f"{expression} = {result}")

    def add(self, a, b):
        """덧셈"""
        result = a + b
        self._record(f"{a} + {b}", result)
        return result

    def subtract(self, a, b):
        """뺄셈"""
        result = a - b
        self._record(f"{a} - {b}", result)
        return result

    def multiply(self, a, b):
        """곱셈"""
        result = a * b
        self._record(f"{a} * {b}", result)
        return result

    def divide(self, a, b):
        """나눗셈"""
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        result = a / b
        self._record(f"{a} / {b}", result)
        return result

    def get_history(self):
        """연산 이력을 반환합니다."""
        return self.history.copy()

    def clear_history(self):
        """연산 이력을 초기화합니다."""
        self.history.clear()


class TestCalculatorRefactored(unittest.TestCase):
    """Refactor 단계: 기존 테스트 + 새 기능 테스트"""

    def setUp(self):
        self.calc = CalculatorV3()

    # 기존 테스트는 여전히 통과해야 합니다!
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    # 새로 추가된 기능에 대한 테스트
    def test_history_recorded(self):
        """연산 이력이 기록되는지 확인"""
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], "1 + 2 = 3")
        self.assertEqual(history[1], "3 * 4 = 12")

    def test_clear_history(self):
        """이력 초기화 테스트"""
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)


# ============================================================
# 메인: 각 단계를 순서대로 보여줍니다
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-07: Red-Green-Refactor 사이클 데모")
    print("=" * 60)
    print()

    # ---- 1단계: Red (테스트 실패) ----
    print("[1단계] Red - 테스트 실패")
    print("-" * 40)
    print("아직 구현이 없는 상태에서 테스트를 실행합니다...")

    result_red = run_tests_silently(TestCalculatorRed)
    failures = len(result_red.failures) + len(result_red.errors)
    print(f"  실행: {result_red.testsRun}개 | "
          f"실패/에러: {failures}개")
    print(f"  결과: 실패! (예상대로)")
    print(f"  이유: CalculatorV1에 add() 메서드가 없습니다")
    print()

    # ---- 2단계: Green (최소 구현) ----
    print("[2단계] Green - 테스트를 통과시키는 구현")
    print("-" * 40)
    print("최소한의 구현을 추가하고 테스트를 다시 실행합니다...")

    result_green = run_tests_silently(TestCalculatorGreen)
    passed = result_green.testsRun - len(result_green.failures) - len(result_green.errors)
    print(f"  실행: {result_green.testsRun}개 | "
          f"통과: {passed}개")
    print(f"  결과: {'통과!' if result_green.wasSuccessful() else '실패!'}")
    print(f"  모든 기본 연산(+, -, *, /)이 동작합니다")
    print()

    # ---- 3단계: Refactor (코드 개선) ----
    print("[3단계] Refactor - 코드 구조 개선")
    print("-" * 40)
    print("연산 이력 기능을 추가하고 기존 테스트가 여전히 통과하는지 확인...")

    result_refactor = run_tests_silently(TestCalculatorRefactored)
    passed = result_refactor.testsRun - len(result_refactor.failures) - len(result_refactor.errors)
    print(f"  실행: {result_refactor.testsRun}개 | "
          f"통과: {passed}개")
    print(f"  결과: {'통과!' if result_refactor.wasSuccessful() else '실패!'}")
    print(f"  기존 테스트 + 새 기능 테스트 모두 통과!")
    print()

    # ---- 사이클 요약 ----
    print("=" * 60)
    print("Red-Green-Refactor 사이클 요약:")
    print("=" * 60)
    print()
    print("  Red     : 실패하는 테스트를 먼저 작성한다")
    print("          → '무엇을 만들 것인가'를 명확히 한다")
    print()
    print("  Green   : 테스트를 통과하는 최소한의 코드를 작성한다")
    print("          → '일단 동작하게 만든다'")
    print()
    print("  Refactor: 테스트가 보호해주니 안심하고 코드를 개선한다")
    print("          → '더 좋은 코드로 바꾼다'")
    print()
    print("  이 사이클을 계속 반복하면서 소프트웨어를 성장시킵니다!")
    print()

    # 최종 테스트 실행 (상세 출력)
    print("-" * 60)
    print("최종 버전(V3) 상세 테스트 결과:")
    print("-" * 60)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCalculatorRefactored)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
