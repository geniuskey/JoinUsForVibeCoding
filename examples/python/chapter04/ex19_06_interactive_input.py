#!/usr/bin/env python3
"""
예제 19-6: 대화형 입력
input()과 검증 루프를 사용하여 사용자와 대화하는 CLI 도구입니다.
"""

import sys


def get_validated_input(prompt, validator, error_msg, max_attempts=3):
    """검증 루프를 사용하여 올바른 입력을 받습니다."""
    for attempt in range(1, max_attempts + 1):
        try:
            value = input(prompt)
            if validator(value):
                return value
            else:
                print(f"  오류: {error_msg}")
        except (EOFError, KeyboardInterrupt):
            print("\n입력이 취소되었습니다.")
            sys.exit(0)

        remaining = max_attempts - attempt
        if remaining > 0:
            print(f"  (남은 시도: {remaining}회)")
        else:
            print(f"  최대 시도 횟수를 초과했습니다.")
            return None

    return None


def main():
    print("=" * 40)
    print("  간단한 프로필 등록 프로그램")
    print("=" * 40)
    print()

    # 이름 입력 (빈 문자열 불가)
    name = get_validated_input(
        "이름을 입력하세요: ",
        lambda v: len(v.strip()) > 0,
        "이름은 비어 있을 수 없습니다."
    )
    if name is None:
        return

    # 나이 입력 (1~150 사이 정수)
    age_str = get_validated_input(
        "나이를 입력하세요 (1~150): ",
        lambda v: v.isdigit() and 1 <= int(v) <= 150,
        "1에서 150 사이의 숫자를 입력해주세요."
    )
    if age_str is None:
        return
    age = int(age_str)

    # 이메일 입력 (@ 포함 여부 확인)
    email = get_validated_input(
        "이메일을 입력하세요: ",
        lambda v: "@" in v and "." in v.split("@")[-1],
        "올바른 이메일 형식이 아닙니다. (예: user@example.com)"
    )
    if email is None:
        return

    # 관심 분야 선택
    print()
    print("관심 분야를 선택하세요:")
    interests = ["웹 개발", "데이터 분석", "AI/ML", "게임 개발", "모바일 앱"]
    for i, interest in enumerate(interests, 1):
        print(f"  {i}. {interest}")

    choice_str = get_validated_input(
        f"번호를 입력하세요 (1~{len(interests)}): ",
        lambda v: v.isdigit() and 1 <= int(v) <= len(interests),
        f"1에서 {len(interests)} 사이의 번호를 입력해주세요."
    )
    if choice_str is None:
        return
    interest = interests[int(choice_str) - 1]

    # 결과 출력
    print()
    print("=" * 40)
    print("  등록된 프로필 정보")
    print("=" * 40)
    print(f"  이름    : {name.strip()}")
    print(f"  나이    : {age}세")
    print(f"  이메일  : {email}")
    print(f"  관심분야: {interest}")
    print("=" * 40)
    print("프로필 등록이 완료되었습니다!")


if __name__ == "__main__":
    main()
