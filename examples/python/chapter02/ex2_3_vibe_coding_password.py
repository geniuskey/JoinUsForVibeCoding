"""
예제 2-3: 대화형 바이브 코딩 예시 - 랜덤 비밀번호 생성기

바이브 코딩 대화 예시:
  사용자: "안전한 랜덤 비밀번호를 생성하는 프로그램을 만들어줘.
          길이를 지정할 수 있고, 대문자, 소문자, 숫자, 특수문자를
          포함할지 선택할 수 있으면 좋겠어. 비밀번호 강도도 알려줘."
  AI: 네, 다음과 같은 비밀번호 생성기를 만들어 드리겠습니다.
"""

import random
import string


def generate_password(length=12, use_upper=True, use_lower=True,
                      use_digits=True, use_special=True):
    """
    옵션에 따라 랜덤 비밀번호를 생성합니다.

    Args:
        length: 비밀번호 길이 (기본값: 12)
        use_upper: 대문자 포함 여부
        use_lower: 소문자 포함 여부
        use_digits: 숫자 포함 여부
        use_special: 특수문자 포함 여부

    Returns:
        생성된 비밀번호 문자열
    """
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()-_=+"

    if not characters:
        return "오류: 최소 하나의 문자 유형을 선택해야 합니다."

    # 각 선택된 유형에서 최소 1개씩 포함 보장
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice("!@#$%^&*()-_=+"))

    # 나머지 길이만큼 랜덤 채우기
    remaining = length - len(password)
    for _ in range(remaining):
        password.append(random.choice(characters))

    # 셔플하여 패턴 제거
    random.shuffle(password)

    return "".join(password)


def check_strength(password):
    """비밀번호 강도를 평가합니다."""
    score = 0
    feedback = []

    # 길이 점수
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    # 문자 유형 점수
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("대문자를 추가하세요")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("소문자를 추가하세요")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("숫자를 추가하세요")

    if any(c in "!@#$%^&*()-_=+" for c in password):
        score += 1
    else:
        feedback.append("특수문자를 추가하세요")

    # 강도 판정
    if score >= 6:
        strength = "강함"
    elif score >= 4:
        strength = "보통"
    else:
        strength = "약함"

    return {
        "강도": strength,
        "점수": f"{score}/7",
        "개선사항": feedback if feedback else ["훌륭합니다!"]
    }


# 실행
if __name__ == "__main__":
    # 시드 고정 (예제 재현을 위해)
    random.seed(42)

    print("=" * 50)
    print("  랜덤 비밀번호 생성기 (바이브 코딩으로 제작)")
    print("=" * 50)

    # 다양한 옵션으로 비밀번호 생성
    configs = [
        {"length": 8, "desc": "기본 8자리"},
        {"length": 12, "desc": "권장 12자리"},
        {"length": 16, "use_special": False, "desc": "특수문자 없이 16자리"},
    ]

    for config in configs:
        desc = config.pop("desc")
        pw = generate_password(**config)
        strength = check_strength(pw)

        print(f"\n[{desc}]")
        print(f"  비밀번호: {pw}")
        print(f"  강도: {strength['강도']} ({strength['점수']})")
        print(f"  피드백: {', '.join(strength['개선사항'])}")
