"""
예제 21-06: AI에게 테스트 먼저 요청하기
- 테스트 코드를 먼저 작성하고, 구현은 나중에 하는 TDD 접근법
- "AI야, 이 기능의 테스트를 먼저 작성해줘" 패턴을 시연합니다

시나리오: 사용자가 AI에게 "비밀번호 검증 함수"의 테스트를 먼저 요청합니다
"""

import unittest


# ============================================================
# 1단계: 테스트를 먼저 작성합니다
#
# AI에게 이렇게 요청할 수 있습니다:
# "비밀번호가 유효한지 검증하는 함수를 만들 건데,
#  테스트 코드를 먼저 작성해줘.
#  조건은: 8자 이상, 대문자 포함, 소문자 포함, 숫자 포함"
# ============================================================

# 아직 구현되지 않은 함수를 미리 import한다고 가정합니다
# (아래에서 구현할 예정)


class TestPasswordValidator(unittest.TestCase):
    """비밀번호 검증 함수의 테스트 (구현보다 먼저 작성!)"""

    def test_valid_password(self):
        """유효한 비밀번호는 True를 반환해야 합니다"""
        self.assertTrue(validate_password("MyPass123"))
        self.assertTrue(validate_password("HelloWorld99"))
        self.assertTrue(validate_password("Abcdefg1"))

    def test_too_short(self):
        """8자 미만이면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("Ab1"))
        self.assertFalse(validate_password("Pass1"))
        self.assertFalse(validate_password("Abcdef7"))  # 7자

    def test_no_uppercase(self):
        """대문자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("mypass123"))

    def test_no_lowercase(self):
        """소문자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("MYPASS123"))

    def test_no_digit(self):
        """숫자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("MyPassword"))

    def test_empty_password(self):
        """빈 문자열이면 False를 반환해야 합니다"""
        self.assertFalse(validate_password(""))

    def test_password_feedback(self):
        """검증 실패 시 피드백 메시지를 반환해야 합니다"""
        is_valid, messages = validate_password_with_feedback("abc")
        self.assertFalse(is_valid)
        # 메시지 목록에 "8자 이상"이 포함된 항목이 있는지 확인
        self.assertTrue(any("8자 이상" in m for m in messages))

    def test_valid_password_feedback(self):
        """유효한 비밀번호의 피드백은 빈 리스트여야 합니다"""
        is_valid, messages = validate_password_with_feedback("MyPass123")
        self.assertTrue(is_valid)
        self.assertEqual(len(messages), 0)


# ============================================================
# 2단계: 테스트를 통과시키는 구현을 작성합니다
#
# AI에게: "위 테스트를 모두 통과하도록 구현해줘"
# ============================================================

def validate_password(password):
    """비밀번호가 유효한지 검증합니다.

    조건:
    - 8자 이상
    - 대문자 최소 1개 포함
    - 소문자 최소 1개 포함
    - 숫자 최소 1개 포함

    Returns:
        bool: 유효하면 True, 아니면 False
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


def validate_password_with_feedback(password):
    """비밀번호를 검증하고 피드백 메시지를 반환합니다.

    Returns:
        tuple: (is_valid: bool, messages: list[str])
    """
    messages = []

    if len(password) < 8:
        messages.append("8자 이상이어야 합니다")
    if not any(c.isupper() for c in password):
        messages.append("대문자를 포함해야 합니다")
    if not any(c.islower() for c in password):
        messages.append("소문자를 포함해야 합니다")
    if not any(c.isdigit() for c in password):
        messages.append("숫자를 포함해야 합니다")

    is_valid = len(messages) == 0
    return is_valid, messages


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-06: AI에게 테스트 먼저 요청하기")
    print("=" * 60)
    print()
    print("TDD(Test-Driven Development) 접근법:")
    print()
    print("  1단계: 테스트를 먼저 작성합니다")
    print("    → 'AI야, 비밀번호 검증 함수의 테스트를 먼저 작성해줘'")
    print()
    print("  2단계: 테스트를 실행하면 당연히 실패합니다 (Red)")
    print("    → 함수가 아직 없으니까!")
    print()
    print("  3단계: 테스트를 통과시키는 구현을 작성합니다 (Green)")
    print("    → 'AI야, 이 테스트를 모두 통과하도록 구현해줘'")
    print()
    print("  4단계: 코드를 개선합니다 (Refactor)")
    print("    → 테스트가 보호해주니 안심하고 리팩토링!")
    print()
    print("비밀번호 검증 규칙:")
    print("  - 8자 이상")
    print("  - 대문자 1개 이상 포함")
    print("  - 소문자 1개 이상 포함")
    print("  - 숫자 1개 이상 포함")
    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
