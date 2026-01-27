#!/usr/bin/env python3
"""
예제 19-5: 타입 지정과 검증
argparse의 type, choices, 범위 검증 기능을 사용합니다.
"""

import argparse


def positive_int(value):
    """양의 정수만 허용하는 커스텀 타입 함수"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}'는 정수가 아닙니다.")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"'{value}'는 양의 정수가 아닙니다. (1 이상 필요)")
    return ivalue


def main():
    parser = argparse.ArgumentParser(
        description="성적 계산기 — 타입 검증 예제"
    )

    parser.add_argument(
        "name",
        type=str,
        help="학생 이름"
    )
    parser.add_argument(
        "--score",
        type=int,
        required=True,
        help="점수 (0~100 사이의 정수)"
    )
    parser.add_argument(
        "--subject",
        type=str,
        choices=["math", "english", "science", "korean"],
        default="math",
        help="과목 선택 (math, english, science, korean)"
    )
    parser.add_argument(
        "--repeat",
        type=positive_int,
        default=1,
        help="출력 반복 횟수 (양의 정수, 기본값: 1)"
    )

    args = parser.parse_args()

    # 점수 범위 검증
    if not 0 <= args.score <= 100:
        parser.error(f"점수는 0~100 사이여야 합니다. (입력값: {args.score})")

    # 등급 계산
    if args.score >= 90:
        grade = "A"
    elif args.score >= 80:
        grade = "B"
    elif args.score >= 70:
        grade = "C"
    elif args.score >= 60:
        grade = "D"
    else:
        grade = "F"

    subject_names = {
        "math": "수학",
        "english": "영어",
        "science": "과학",
        "korean": "국어"
    }
    subject_kr = subject_names[args.subject]

    for i in range(args.repeat):
        if args.repeat > 1:
            print(f"--- 출력 {i + 1}/{args.repeat} ---")
        print(f"학생: {args.name}")
        print(f"과목: {subject_kr}")
        print(f"점수: {args.score}점")
        print(f"등급: {grade}")
        if i < args.repeat - 1:
            print()


if __name__ == "__main__":
    main()
