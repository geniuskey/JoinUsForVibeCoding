"""
예제 21-02: unittest 실행
- TestRunner를 사용하여 테스트를 실행하고 결과를 분석합니다
- 프로그래밍 방식으로 테스트를 실행하는 방법을 배웁니다
"""

import unittest
import io
import sys


# ============================================================
# 테스트할 함수들
# ============================================================
def celsius_to_fahrenheit(celsius):
    """섭씨를 화씨로 변환합니다."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """화씨를 섭씨로 변환합니다."""
    return (fahrenheit - 32) * 5 / 9


# ============================================================
# 테스트 클래스
# ============================================================
class TestTemperatureConversion(unittest.TestCase):
    """온도 변환 함수 테스트"""

    def test_freezing_point(self):
        """물의 어는점 변환 테스트"""
        self.assertEqual(celsius_to_fahrenheit(0), 32)

    def test_boiling_point(self):
        """물의 끓는점 변환 테스트"""
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_body_temperature(self):
        """체온 변환 테스트"""
        self.assertAlmostEqual(celsius_to_fahrenheit(36.5), 97.7)

    def test_reverse_freezing(self):
        """화씨 → 섭씨 어는점 변환"""
        self.assertEqual(fahrenheit_to_celsius(32), 0)

    def test_reverse_boiling(self):
        """화씨 → 섭씨 끓는점 변환"""
        self.assertEqual(fahrenheit_to_celsius(212), 100)

    def test_round_trip(self):
        """왕복 변환 테스트 (섭씨 → 화씨 → 섭씨)"""
        original = 25
        converted = celsius_to_fahrenheit(original)
        back = fahrenheit_to_celsius(converted)
        self.assertAlmostEqual(back, original)


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-02: unittest 실행 - TestRunner 활용")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # 방법 1: TestLoader로 테스트 수집
    # --------------------------------------------------------
    print("[방법 1] TestLoader로 테스트 수집하기")
    print("-" * 40)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTemperatureConversion)

    # 테스트 수 확인
    print(f"  수집된 테스트 수: {suite.countTestCases()}개")
    print()

    # --------------------------------------------------------
    # 방법 2: TextTestRunner로 실행하기
    # --------------------------------------------------------
    print("[방법 2] TextTestRunner로 실행하기")
    print("-" * 40)

    # 버퍼를 사용하여 결과를 캡처합니다
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()

    # --------------------------------------------------------
    # 결과 분석
    # --------------------------------------------------------
    print("[결과 분석]")
    print("-" * 40)
    print(f"  실행한 테스트 수: {result.testsRun}")
    print(f"  성공: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  실패: {len(result.failures)}")
    print(f"  에러: {len(result.errors)}")
    print(f"  전체 통과 여부: {'통과' if result.wasSuccessful() else '실패'}")
    print()

    # --------------------------------------------------------
    # 방법 3: TestSuite에 개별 테스트 추가
    # --------------------------------------------------------
    print("[방법 3] 개별 테스트만 골라서 실행하기")
    print("-" * 40)

    custom_suite = unittest.TestSuite()
    # 특정 테스트만 골라서 추가
    custom_suite.addTest(TestTemperatureConversion("test_freezing_point"))
    custom_suite.addTest(TestTemperatureConversion("test_boiling_point"))

    print(f"  선택된 테스트 수: {custom_suite.countTestCases()}개")
    runner2 = unittest.TextTestRunner(verbosity=2)
    result2 = runner2.run(custom_suite)

    print()
    print("=" * 60)
    print("핵심 정리:")
    print("  - TestLoader: 테스트 클래스에서 테스트를 자동 수집합니다")
    print("  - TestSuite: 여러 테스트를 하나의 그룹으로 묶습니다")
    print("  - TextTestRunner: 테스트를 실행하고 결과를 출력합니다")
    print("  - result 객체로 성공/실패 수를 분석할 수 있습니다")
    print("=" * 60)
