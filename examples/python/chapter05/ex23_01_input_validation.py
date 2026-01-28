"""
예제 23-01: 입력 검증 기초
- 사용자 입력 검증: 길이, 타입, 범위 체크
- 바이브 코딩에서 AI가 생성한 코드의 입력 검증 확인하기

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
"""

import re
from typing import Optional


# ============================================================
# ❌ 취약한 코드: 입력 검증 없이 사용자 입력을 그대로 사용
# ============================================================

def vulnerable_create_user(username: str, age: str, email: str) -> dict:
    """
    ❌ 취약: 입력값을 검증하지 않고 그대로 사용
    - 빈 문자열, 너무 긴 문자열도 허용
    - 나이에 문자열이 들어와도 오류 없이 저장
    - 이메일 형식을 확인하지 않음
    """
    return {
        "username": username,
        "age": age,
        "email": email,
        "status": "created"
    }


# ============================================================
# ✅ 안전한 코드: 체계적인 입력 검증
# ============================================================

class ValidationError(Exception):
    """입력 검증 실패 시 발생하는 예외"""
    pass


def validate_username(username: str) -> str:
    """
    ✅ 사용자 이름 검증
    - 타입 확인: 문자열인지
    - 길이 확인: 3~20자
    - 문자 확인: 영문, 숫자, 밑줄만 허용
    """
    if not isinstance(username, str):
        raise ValidationError("사용자 이름은 문자열이어야 합니다")

    username = username.strip()

    if len(username) < 3:
        raise ValidationError(f"사용자 이름이 너무 짧습니다 (최소 3자, 현재 {len(username)}자)")

    if len(username) > 20:
        raise ValidationError(f"사용자 이름이 너무 깁니다 (최대 20자, 현재 {len(username)}자)")

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError("사용자 이름은 영문, 숫자, 밑줄(_)만 사용할 수 있습니다")

    return username


def validate_age(age_input: str) -> int:
    """
    ✅ 나이 검증
    - 타입 변환: 문자열 -> 정수
    - 범위 확인: 1~150
    """
    try:
        age = int(age_input)
    except (ValueError, TypeError):
        raise ValidationError(f"나이는 숫자여야 합니다: '{age_input}'")

    if age < 1 or age > 150:
        raise ValidationError(f"나이는 1~150 사이여야 합니다: {age}")

    return age


def validate_email(email: str) -> str:
    """
    ✅ 이메일 검증
    - 기본 형식 확인: @ 포함, 도메인 존재
    - 길이 제한: 최대 254자 (RFC 5321)
    """
    if not isinstance(email, str):
        raise ValidationError("이메일은 문자열이어야 합니다")

    email = email.strip().lower()

    if len(email) > 254:
        raise ValidationError("이메일이 너무 깁니다 (최대 254자)")

    # 기본적인 이메일 형식 검증
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError(f"올바른 이메일 형식이 아닙니다: '{email}'")

    return email


def safe_create_user(username: str, age: str, email: str) -> dict:
    """
    ✅ 안전: 모든 입력값을 검증한 후 사용
    """
    validated_username = validate_username(username)
    validated_age = validate_age(age)
    validated_email = validate_email(email)

    return {
        "username": validated_username,
        "age": validated_age,
        "email": validated_email,
        "status": "created"
    }


# ============================================================
# ✅ 범용 입력 검증 도구
# ============================================================

def sanitize_string(text: str, max_length: int = 255,
                    allow_html: bool = False) -> str:
    """
    ✅ 문자열 정제(Sanitization)
    - 앞뒤 공백 제거
    - 길이 제한
    - HTML 태그 제거 (선택)
    """
    if not isinstance(text, str):
        raise ValidationError("문자열이 아닙니다")

    text = text.strip()

    if len(text) > max_length:
        text = text[:max_length]

    if not allow_html:
        # 간단한 HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)

    return text


def validate_in_range(value: str, min_val: float, max_val: float,
                      field_name: str = "값") -> float:
    """
    ✅ 숫자 범위 검증
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name}은(는) 숫자여야 합니다: '{value}'")

    if num < min_val or num > max_val:
        raise ValidationError(
            f"{field_name}은(는) {min_val}~{max_val} 범위여야 합니다: {num}"
        )

    return num


def validate_choice(value: str, allowed: list, field_name: str = "값") -> str:
    """
    ✅ 허용된 값 목록에서만 선택
    """
    if value not in allowed:
        raise ValidationError(
            f"{field_name}은(는) {allowed} 중 하나여야 합니다: '{value}'"
        )
    return value


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-01: 입력 검증 기초")
    print("=" * 60)

    # --- ❌ 취약한 코드 시연 ---
    print("\n--- ❌ 취약한 코드: 검증 없는 사용자 생성 ---")

    # 문제 1: 빈 문자열
    result = vulnerable_create_user("", "", "")
    print(f"빈 입력 허용됨: {result}")

    # 문제 2: 너무 긴 입력
    result = vulnerable_create_user("A" * 10000, "abc", "not-email")
    print(f"비정상 입력 허용됨: username 길이={len(result['username'])}, "
          f"age='{result['age']}', email='{result['email']}'")

    # --- ✅ 안전한 코드 시연 ---
    print("\n--- ✅ 안전한 코드: 검증된 사용자 생성 ---")

    # 정상 입력
    try:
        result = safe_create_user("john_doe", "25", "john@example.com")
        print(f"정상 생성: {result}")
    except ValidationError as e:
        print(f"검증 실패: {e}")

    # 비정상 입력 테스트
    test_cases = [
        ("", "25", "john@example.com", "빈 사용자 이름"),
        ("ab", "25", "john@example.com", "너무 짧은 이름"),
        ("john_doe", "abc", "john@example.com", "나이에 문자열"),
        ("john_doe", "200", "john@example.com", "범위 초과 나이"),
        ("john_doe", "25", "not-email", "잘못된 이메일"),
        ("john<script>", "25", "john@example.com", "특수문자 이름"),
    ]

    print("\n--- 다양한 비정상 입력 테스트 ---")
    for username, age, email, description in test_cases:
        try:
            safe_create_user(username, age, email)
            print(f"  [{description}] 통과 (예상치 못한 결과)")
        except ValidationError as e:
            print(f"  [{description}] 차단됨 -> {e}")

    # 문자열 정제 시연
    print("\n--- ✅ 문자열 정제(Sanitization) ---")
    dirty_input = "  <script>alert('XSS')</script>안녕하세요  "
    clean = sanitize_string(dirty_input, max_length=50)
    print(f"  원본: '{dirty_input}'")
    print(f"  정제: '{clean}'")

    # 범위 검증 시연
    print("\n--- ✅ 숫자 범위 검증 ---")
    try:
        price = validate_in_range("15000", 0, 100000, "가격")
        print(f"  가격 검증 통과: {price}")
    except ValidationError as e:
        print(f"  가격 검증 실패: {e}")

    try:
        price = validate_in_range("-500", 0, 100000, "가격")
    except ValidationError as e:
        print(f"  음수 가격 차단: {e}")

    # 선택지 검증 시연
    print("\n--- ✅ 허용된 값 목록 검증 ---")
    try:
        role = validate_choice("admin", ["user", "admin", "guest"], "역할")
        print(f"  역할 검증 통과: {role}")
    except ValidationError as e:
        print(f"  역할 검증 실패: {e}")

    try:
        role = validate_choice("superuser", ["user", "admin", "guest"], "역할")
    except ValidationError as e:
        print(f"  잘못된 역할 차단: {e}")

    print("\n" + "=" * 60)
    print("핵심 원칙: 모든 외부 입력은 신뢰하지 않고 반드시 검증하세요!")
    print("바이브 코딩 팁: AI에게 '입력 검증 코드를 추가해줘'라고 요청하세요.")
    print("=" * 60)
