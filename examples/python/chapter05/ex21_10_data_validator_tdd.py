"""
예제 21-10: 실습 - TDD로 데이터 검증기 만들기
- 이메일, 전화번호, 날짜 검증 함수를 TDD 방식으로 개발합니다
- 실무에서 자주 사용하는 입력 검증 패턴을 배웁니다
"""

import unittest
import re
from datetime import datetime


# ============================================================
# 데이터 검증 함수들 (TDD로 개발)
# ============================================================

def validate_email(email):
    """이메일 주소가 유효한지 검증합니다.

    검증 규칙:
    - @가 정확히 하나 포함
    - @ 앞에 최소 1글자
    - @ 뒤에 도메인이 있어야 함 (점 포함)
    - 공백 불허

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(email, str):
        return False, "이메일은 문자열이어야 합니다"

    if not email or email.strip() != email:
        return False, "이메일에 공백이 포함되어서는 안 됩니다"

    if " " in email:
        return False, "이메일에 공백이 포함되어서는 안 됩니다"

    # @ 기호 확인
    at_count = email.count("@")
    if at_count == 0:
        return False, "이메일에 @가 포함되어야 합니다"
    if at_count > 1:
        return False, "이메일에 @가 하나만 있어야 합니다"

    local, domain = email.split("@")

    if not local:
        return False, "@ 앞에 사용자명이 필요합니다"

    if not domain:
        return False, "@ 뒤에 도메인이 필요합니다"

    if "." not in domain:
        return False, "도메인에 점(.)이 포함되어야 합니다"

    # 도메인의 마지막 부분(TLD) 확인
    parts = domain.split(".")
    if any(not part for part in parts):
        return False, "도메인 형식이 올바르지 않습니다"

    return True, "유효한 이메일입니다"


def validate_phone(phone):
    """한국 전화번호가 유효한지 검증합니다.

    허용 형식:
    - 010-1234-5678
    - 01012345678
    - 010 1234 5678

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(phone, str):
        return False, "전화번호는 문자열이어야 합니다"

    # 숫자만 추출
    digits = re.sub(r"[\s\-]", "", phone)

    # 숫자 외의 문자가 있으면 실패
    if not digits.isdigit():
        return False, "전화번호에는 숫자, 하이픈(-), 공백만 허용됩니다"

    # 길이 확인 (한국 휴대폰: 11자리, 일반 전화: 10~11자리)
    if len(digits) < 10 or len(digits) > 11:
        return False, "전화번호는 10~11자리여야 합니다"

    # 시작 번호 확인
    valid_prefixes = ("010", "011", "016", "017", "018", "019",
                      "02", "031", "032", "033", "041", "042",
                      "043", "044", "051", "052", "053", "054",
                      "055", "061", "062", "063", "064")

    if not any(digits.startswith(prefix) for prefix in valid_prefixes):
        return False, "유효하지 않은 지역번호입니다"

    return True, "유효한 전화번호입니다"


def validate_date(date_str, fmt="%Y-%m-%d"):
    """날짜 문자열이 유효한지 검증합니다.

    기본 형식: YYYY-MM-DD

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not isinstance(date_str, str):
        return False, "날짜는 문자열이어야 합니다"

    if not date_str.strip():
        return False, "날짜가 비어있습니다"

    try:
        parsed = datetime.strptime(date_str, fmt)
    except ValueError:
        return False, f"날짜 형식이 올바르지 않습니다 (올바른 형식: {fmt})"

    # 연도 범위 확인
    if parsed.year < 1900:
        return False, "연도는 1900년 이후여야 합니다"
    if parsed.year > 2100:
        return False, "연도는 2100년 이전이어야 합니다"

    return True, "유효한 날짜입니다"


# ============================================================
# 종합 데이터 검증기 클래스
# ============================================================
class DataValidator:
    """여러 필드를 한 번에 검증하는 종합 검증기"""

    def __init__(self):
        self.errors = []

    def validate(self, data):
        """데이터 딕셔너리를 검증합니다.

        Args:
            data: {"email": "...", "phone": "...", "birth_date": "..."}

        Returns:
            tuple: (is_valid: bool, errors: list[str])
        """
        self.errors = []

        # 이메일 검증
        if "email" in data:
            valid, msg = validate_email(data["email"])
            if not valid:
                self.errors.append(f"이메일: {msg}")

        # 전화번호 검증
        if "phone" in data:
            valid, msg = validate_phone(data["phone"])
            if not valid:
                self.errors.append(f"전화번호: {msg}")

        # 날짜 검증
        if "birth_date" in data:
            valid, msg = validate_date(data["birth_date"])
            if not valid:
                self.errors.append(f"생년월일: {msg}")

        return len(self.errors) == 0, self.errors


# ============================================================
# 테스트 클래스들
# ============================================================

class TestValidateEmail(unittest.TestCase):
    """이메일 검증 테스트"""

    def test_valid_emails(self):
        """유효한 이메일 주소들"""
        valid_emails = [
            "user@example.com",
            "test@domain.co.kr",
            "hello.world@email.org",
            "user123@test.net",
        ]
        for email in valid_emails:
            is_valid, msg = validate_email(email)
            self.assertTrue(is_valid, f"'{email}'은 유효해야 합니다: {msg}")

    def test_missing_at(self):
        """@ 없는 이메일"""
        is_valid, msg = validate_email("userexample.com")
        self.assertFalse(is_valid)
        self.assertIn("@", msg)

    def test_multiple_at(self):
        """@ 여러 개"""
        is_valid, msg = validate_email("user@@example.com")
        self.assertFalse(is_valid)

    def test_no_domain(self):
        """도메인 없음"""
        is_valid, msg = validate_email("user@")
        self.assertFalse(is_valid)

    def test_no_username(self):
        """사용자명 없음"""
        is_valid, msg = validate_email("@example.com")
        self.assertFalse(is_valid)

    def test_no_dot_in_domain(self):
        """도메인에 점 없음"""
        is_valid, msg = validate_email("user@example")
        self.assertFalse(is_valid)
        self.assertIn("점", msg)

    def test_with_spaces(self):
        """공백 포함"""
        is_valid, msg = validate_email("user @example.com")
        self.assertFalse(is_valid)

    def test_empty_string(self):
        """빈 문자열"""
        is_valid, msg = validate_email("")
        self.assertFalse(is_valid)

    def test_non_string(self):
        """문자열이 아닌 입력"""
        is_valid, msg = validate_email(123)
        self.assertFalse(is_valid)


class TestValidatePhone(unittest.TestCase):
    """전화번호 검증 테스트"""

    def test_valid_mobile_with_dash(self):
        """유효한 휴대폰 번호 (하이픈 포함)"""
        is_valid, msg = validate_phone("010-1234-5678")
        self.assertTrue(is_valid, msg)

    def test_valid_mobile_no_dash(self):
        """유효한 휴대폰 번호 (하이픈 없음)"""
        is_valid, msg = validate_phone("01012345678")
        self.assertTrue(is_valid, msg)

    def test_valid_mobile_with_space(self):
        """유효한 휴대폰 번호 (공백)"""
        is_valid, msg = validate_phone("010 1234 5678")
        self.assertTrue(is_valid, msg)

    def test_valid_landline(self):
        """유효한 일반 전화번호"""
        is_valid, msg = validate_phone("02-1234-5678")
        self.assertTrue(is_valid, msg)

    def test_valid_area_code(self):
        """유효한 지역번호"""
        is_valid, msg = validate_phone("031-123-4567")
        self.assertTrue(is_valid, msg)

    def test_too_short(self):
        """너무 짧은 번호"""
        is_valid, msg = validate_phone("010-123")
        self.assertFalse(is_valid)

    def test_too_long(self):
        """너무 긴 번호"""
        is_valid, msg = validate_phone("010-1234-56789")
        self.assertFalse(is_valid)

    def test_invalid_chars(self):
        """잘못된 문자 포함"""
        is_valid, msg = validate_phone("010-abcd-5678")
        self.assertFalse(is_valid)

    def test_non_string(self):
        """문자열이 아닌 입력"""
        is_valid, msg = validate_phone(1012345678)
        self.assertFalse(is_valid)


class TestValidateDate(unittest.TestCase):
    """날짜 검증 테스트"""

    def test_valid_date(self):
        """유효한 날짜"""
        is_valid, msg = validate_date("2024-01-15")
        self.assertTrue(is_valid, msg)

    def test_valid_leap_year(self):
        """윤년 2월 29일"""
        is_valid, msg = validate_date("2024-02-29")
        self.assertTrue(is_valid, msg)

    def test_invalid_leap_year(self):
        """윤년이 아닌 해의 2월 29일"""
        is_valid, msg = validate_date("2023-02-29")
        self.assertFalse(is_valid)

    def test_invalid_format(self):
        """잘못된 형식"""
        is_valid, msg = validate_date("15/01/2024")
        self.assertFalse(is_valid)
        self.assertIn("형식", msg)

    def test_invalid_month(self):
        """13월은 없습니다"""
        is_valid, msg = validate_date("2024-13-01")
        self.assertFalse(is_valid)

    def test_invalid_day(self):
        """32일은 없습니다"""
        is_valid, msg = validate_date("2024-01-32")
        self.assertFalse(is_valid)

    def test_too_old(self):
        """1900년 이전"""
        is_valid, msg = validate_date("1899-12-31")
        self.assertFalse(is_valid)
        self.assertIn("1900", msg)

    def test_too_future(self):
        """2100년 이후"""
        is_valid, msg = validate_date("2101-01-01")
        self.assertFalse(is_valid)
        self.assertIn("2100", msg)

    def test_custom_format(self):
        """커스텀 형식"""
        is_valid, msg = validate_date("15/01/2024", fmt="%d/%m/%Y")
        self.assertTrue(is_valid, msg)

    def test_empty(self):
        """빈 문자열"""
        is_valid, msg = validate_date("")
        self.assertFalse(is_valid)


class TestDataValidator(unittest.TestCase):
    """종합 데이터 검증기 테스트"""

    def setUp(self):
        self.validator = DataValidator()

    def test_all_valid(self):
        """모든 필드가 유효한 경우"""
        data = {
            "email": "user@example.com",
            "phone": "010-1234-5678",
            "birth_date": "1990-05-15"
        }
        is_valid, errors = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_all_invalid(self):
        """모든 필드가 잘못된 경우"""
        data = {
            "email": "invalid-email",
            "phone": "abc",
            "birth_date": "not-a-date"
        }
        is_valid, errors = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 3)

    def test_partial_invalid(self):
        """일부 필드만 잘못된 경우"""
        data = {
            "email": "user@example.com",
            "phone": "invalid",
            "birth_date": "1990-05-15"
        }
        is_valid, errors = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 1)
        self.assertIn("전화번호", errors[0])

    def test_partial_data(self):
        """일부 필드만 있는 경우"""
        data = {"email": "user@example.com"}
        is_valid, errors = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_empty_data(self):
        """빈 데이터"""
        data = {}
        is_valid, errors = self.validator.validate(data)
        self.assertTrue(is_valid)

    def test_error_messages_are_descriptive(self):
        """에러 메시지가 어떤 필드인지 알려주는지 확인"""
        data = {
            "email": "bad",
            "phone": "bad",
        }
        is_valid, errors = self.validator.validate(data)
        self.assertFalse(is_valid)
        # 각 에러가 필드명을 포함하는지 확인
        has_email_error = any("이메일" in e for e in errors)
        has_phone_error = any("전화번호" in e for e in errors)
        self.assertTrue(has_email_error)
        self.assertTrue(has_phone_error)


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-10: TDD로 데이터 검증기 만들기")
    print("=" * 60)
    print()
    print("구현한 검증 함수:")
    print("  1. validate_email()  : 이메일 주소 검증")
    print("  2. validate_phone()  : 한국 전화번호 검증")
    print("  3. validate_date()   : 날짜 문자열 검증")
    print("  4. DataValidator     : 종합 데이터 검증기")
    print()

    # 사용 예시
    print("-" * 60)
    print("사용 예시:")
    print("-" * 60)

    # 이메일 검증
    test_emails = ["user@example.com", "invalid-email", "user@@test.com"]
    print("\n  [이메일 검증]")
    for email in test_emails:
        is_valid, msg = validate_email(email)
        status = "유효" if is_valid else "무효"
        print(f'    "{email}" → {status} ({msg})')

    # 전화번호 검증
    test_phones = ["010-1234-5678", "01012345678", "123-456"]
    print("\n  [전화번호 검증]")
    for phone in test_phones:
        is_valid, msg = validate_phone(phone)
        status = "유효" if is_valid else "무효"
        print(f'    "{phone}" → {status} ({msg})')

    # 날짜 검증
    test_dates = ["2024-01-15", "2024-02-29", "2024-13-01"]
    print("\n  [날짜 검증]")
    for date in test_dates:
        is_valid, msg = validate_date(date)
        status = "유효" if is_valid else "무효"
        print(f'    "{date}" → {status} ({msg})')

    # 종합 검증
    print("\n  [종합 검증]")
    validator = DataValidator()
    data = {
        "email": "user@example.com",
        "phone": "010-9876-5432",
        "birth_date": "1995-03-20"
    }
    is_valid, errors = validator.validate(data)
    print(f"    데이터: {data}")
    print(f"    결과: {'유효' if is_valid else '무효'}")
    if errors:
        for err in errors:
            print(f"    오류: {err}")

    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
