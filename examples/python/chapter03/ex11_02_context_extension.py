# examples/python/chapter03/ex11_02_context_extension.py
# 예제 11-2: 컨텍스트 유지하며 기능 확장
#
# AI와의 대화에서 컨텍스트를 유지하며 기능을 확장하는 과정을 보여줍니다.
# 기본 단위 변환기 → "여기에 히스토리 기능 추가해줘" → 확장된 버전

import sys
from datetime import datetime


# ============================================================
# [1차 대화] "단위 변환기 만들어줘"
# ============================================================

def basic_converter():
    """1차 대화: 기본 단위 변환기"""
    print("=" * 45)
    print("  [1차] 기본 단위 변환기")
    print("=" * 45)

    converters = {
        "1": ("km → mile", lambda x: x * 0.621371),
        "2": ("mile → km", lambda x: x / 0.621371),
        "3": ("kg → lb", lambda x: x * 2.20462),
        "4": ("lb → kg", lambda x: x / 2.20462),
        "5": ("°C → °F", lambda x: x * 9 / 5 + 32),
        "6": ("°F → °C", lambda x: (x - 32) * 5 / 9),
    }

    print("\n변환 종류를 선택하세요:")
    for key, (name, _) in converters.items():
        print(f"  {key}. {name}")

    choice = input("\n선택: ").strip()
    if choice not in converters:
        print("잘못된 선택입니다.")
        return

    name, func = converters[choice]
    try:
        value = float(input(f"변환할 값 ({name}): "))
    except ValueError:
        print("올바른 숫자를 입력해주세요.")
        return

    result = func(value)
    print(f"\n결과: {value} → {result:.2f}")


# ============================================================
# [2차 대화] "여기에 히스토리 기능 추가해줘"
# AI가 1차 코드의 컨텍스트를 기억하고 확장
# ============================================================

def converter_with_history():
    """2차 대화: 히스토리 기능이 추가된 단위 변환기"""
    print("=" * 45)
    print("  [2차] 히스토리 기능 추가된 단위 변환기")
    print("  → '여기에 히스토리 기능 추가해줘'")
    print("=" * 45)

    converters = {
        "1": ("km → mile", "km", "mile", lambda x: x * 0.621371),
        "2": ("mile → km", "mile", "km", lambda x: x / 0.621371),
        "3": ("kg → lb", "kg", "lb", lambda x: x * 2.20462),
        "4": ("lb → kg", "lb", "kg", lambda x: x / 2.20462),
        "5": ("°C → °F", "°C", "°F", lambda x: x * 9 / 5 + 32),
        "6": ("°F → °C", "°F", "°C", lambda x: (x - 32) * 5 / 9),
    }

    # 히스토리 저장 (2차 대화에서 추가된 부분)
    history = []

    while True:
        print("\n변환 종류를 선택하세요:")
        for key, (name, *_) in converters.items():
            print(f"  {key}. {name}")
        print(f"  h. 변환 히스토리 보기 ({len(history)}건)")
        print(f"  q. 종료")

        choice = input("\n선택: ").strip().lower()

        if choice == "q":
            if history:
                print(f"\n총 {len(history)}건의 변환을 수행했습니다.")
            print("변환기를 종료합니다.")
            break

        if choice == "h":
            if not history:
                print("\n  아직 변환 기록이 없습니다.")
            else:
                print("\n  ┌─── 변환 히스토리 ───────────────────┐")
                for i, record in enumerate(history, 1):
                    print(f"  │ {i}. {record['time']} | "
                          f"{record['input']}{record['from']} → "
                          f"{record['output']}{record['to']}")
                print(f"  └─── 총 {len(history)}건 "
                      f"{'─' * 25}┘")
            continue

        if choice not in converters:
            print("  잘못된 선택입니다.")
            continue

        name, unit_from, unit_to, func = converters[choice]
        try:
            value = float(input(f"  변환할 값 ({name}): "))
        except ValueError:
            print("  올바른 숫자를 입력해주세요.")
            continue

        result = func(value)

        # 히스토리에 기록 (2차 대화에서 추가된 부분)
        history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "input": f"{value:.1f}",
            "output": f"{result:.2f}",
            "from": unit_from,
            "to": unit_to,
        })

        print(f"  ✓ {value:.1f}{unit_from} → {result:.2f}{unit_to}")


# ============================================================
# 컨텍스트 유지의 효과 설명
# ============================================================

def show_context_benefit():
    """컨텍스트 유지의 이점을 설명합니다"""
    print("\n" + "=" * 50)
    print("  컨텍스트 유지의 효과")
    print("=" * 50)
    print()
    print("  [1차 대화] '단위 변환기 만들어줘'")
    print("  → 기본 변환 기능만 있는 프로그램 생성")
    print()
    print("  [2차 대화] '여기에 히스토리 기능 추가해줘'")
    print("  → AI가 기존 코드 구조를 기억하고 확장!")
    print()
    print("  핵심 포인트:")
    print("  • AI는 같은 세션에서 이전 코드를 기억합니다")
    print("  • '여기에', '이 코드에'라는 참조가 가능합니다")
    print("  • 기존 구조를 깨뜨리지 않고 기능을 추가합니다")
    print("  • 변수명, 함수명 등의 일관성이 유지됩니다")
    print()
    print("  만약 새 세션에서 히스토리 기능을 요청하면?")
    print("  → 완전히 새로운 코드를 작성하게 됩니다")
    print("  → 기존 변환기의 구조와 다를 수 있습니다")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--basic":
        basic_converter()
    elif len(sys.argv) > 1 and sys.argv[1] == "--context":
        show_context_benefit()
    else:
        show_context_benefit()
        print("히스토리 기능이 추가된 변환기를 실행합니다:\n")
        converter_with_history()
