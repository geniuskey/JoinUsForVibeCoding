# examples/python/chapter03/ex11_01_single_vs_iterative.py
# 예제 11-1: 단일 요청 vs 대화형 개발 비교
#
# 같은 "계산기" 프로그램을 두 가지 방식으로 개발한 결과를 비교합니다.
# - 방식 A: 단일 요청 ("계산기 만들어줘") → 기본적인 결과
# - 방식 B: 대화형 단계별 개발 → 풍부한 기능의 결과

import sys

# ============================================================
# 방식 A: 단일 요청으로 만든 기본 계산기
# AI에게 "간단한 계산기 만들어줘"라고 한 번만 요청한 결과
# ============================================================

def basic_calculator():
    """단일 요청으로 생성된 기본 계산기"""
    print("=" * 50)
    print("  [방식 A] 단일 요청 계산기")
    print("  → '계산기 만들어줘' 한 번의 요청 결과")
    print("=" * 50)

    num1 = float(input("첫 번째 숫자: "))
    operator = input("연산자 (+, -, *, /): ")
    num2 = float(input("두 번째 숫자: "))

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2 if num2 != 0 else "오류: 0으로 나눌 수 없습니다"
    else:
        result = "오류: 잘못된 연산자"

    print(f"결과: {result}")


# ============================================================
# 방식 B: 대화형 개발로 만든 향상된 계산기
# 여러 번의 대화를 통해 점진적으로 개선한 결과
# ============================================================

def enhanced_calculator():
    """대화형 개발로 만든 향상된 계산기"""
    print("=" * 50)
    print("  [방식 B] 대화형 개발 계산기")
    print("  → 5번의 대화를 통해 점진적으로 개선한 결과")
    print("=" * 50)

    # 1차 대화: 기본 계산기 만들어줘
    # 2차 대화: 반복 계산이 되게 해줘
    # 3차 대화: 입력 검증을 추가해줘
    # 4차 대화: 계산 히스토리를 보여줘
    # 5차 대화: 결과를 보기 좋게 포맷팅해줘

    history = []
    operators = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b if b != 0 else None,
    }

    print("\n사용법: 숫자 연산자 숫자 (예: 10 + 5)")
    print("명령어: 'history' = 기록 보기, 'quit' = 종료\n")

    while True:
        user_input = input("계산> ").strip()

        if user_input.lower() == "quit":
            print("\n계산기를 종료합니다.")
            break

        if user_input.lower() == "history":
            if not history:
                print("  아직 계산 기록이 없습니다.")
            else:
                print("\n  ┌─── 계산 기록 ───┐")
                for i, record in enumerate(history, 1):
                    print(f"  │ {i}. {record}")
                print(f"  └── 총 {len(history)}건 ──┘\n")
            continue

        # 입력 파싱 및 검증 (3차 대화에서 추가)
        parts = user_input.split()
        if len(parts) != 3:
            print("  ⚠ 형식: 숫자 연산자 숫자 (예: 10 + 5)")
            continue

        try:
            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])
        except ValueError:
            print("  ⚠ 올바른 숫자를 입력해주세요.")
            continue

        if op not in operators:
            print(f"  ⚠ 지원하지 않는 연산자: {op}")
            print(f"  사용 가능: {', '.join(operators.keys())}")
            continue

        result = operators[op](num1, num2)
        if result is None:
            print("  ⚠ 오류: 0으로 나눌 수 없습니다.")
            continue

        # 결과 포맷팅 (5차 대화에서 추가)
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = f"{result:.4f}".rstrip("0").rstrip(".")

        expression = f"{parts[0]} {op} {parts[2]} = {result_str}"
        history.append(expression)
        print(f"  ✓ {expression}")


# ============================================================
# 비교 실행
# ============================================================

def compare_approaches():
    """두 방식의 차이점을 보여줍니다"""
    print("\n" + "=" * 50)
    print("  📊 두 방식 비교")
    print("=" * 50)
    print()
    print("  ┌────────────────┬──────────────┬──────────────┐")
    print("  │      항목      │   방식 A     │   방식 B     │")
    print("  │                │ (단일 요청)  │ (대화형)     │")
    print("  ├────────────────┼──────────────┼──────────────┤")
    print("  │ AI 대화 횟수   │    1회       │    5회       │")
    print("  │ 반복 계산      │    ✗         │    ✓         │")
    print("  │ 입력 검증      │    최소      │    완전      │")
    print("  │ 계산 기록      │    ✗         │    ✓         │")
    print("  │ 결과 포맷팅    │    기본      │    정돈됨    │")
    print("  │ 사용자 경험    │    단순      │    풍부      │")
    print("  └────────────────┴──────────────┴──────────────┘")
    print()
    print("  → 대화형 개발은 더 많은 대화가 필요하지만,")
    print("    결과물의 품질이 크게 향상됩니다.")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        compare_approaches()
    elif len(sys.argv) > 1 and sys.argv[1] == "--basic":
        basic_calculator()
    elif len(sys.argv) > 1 and sys.argv[1] == "--enhanced":
        enhanced_calculator()
    else:
        # 기본: 비교 표를 보여주고 대화형 계산기 실행
        compare_approaches()
        print("대화형 개발 계산기를 실행합니다:\n")
        enhanced_calculator()
