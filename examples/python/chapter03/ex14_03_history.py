"""
예제 14-3: 기능 추가 — 계산 히스토리
======================================
사칙연산 계산기에 히스토리(계산 기록) 기능을 추가합니다.
반복 계산이 가능하며, 이전 계산 기록을 볼 수 있습니다.

변경 사항:
  - history 리스트로 계산 기록 저장
  - 반복 계산 루프 추가
  - 'history' 명령어로 기록 조회
  - 'quit' 명령어로 종료
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


OPERATIONS = {
    "+": ("덧셈", add),
    "-": ("뺄셈", subtract),
    "*": ("곱셈", multiply),
    "/": ("나눗셈", divide),
}


def show_history(history):
    """계산 히스토리를 출력합니다."""
    if not history:
        print("  (아직 계산 기록이 없습니다)")
        return

    print(f"\n{'='*40}")
    print(f"  계산 히스토리 ({len(history)}건)")
    print(f"{'='*40}")
    for i, record in enumerate(history, 1):
        print(f"  {i}. {record}")
    print()


def calculate_once(history):
    """한 번의 계산을 수행하고 히스토리에 추가합니다."""
    try:
        num1 = float(input("첫 번째 숫자: "))
        operator = input("연산자 (+, -, *, /): ").strip()
        num2 = float(input("두 번째 숫자: "))

        if operator not in OPERATIONS:
            print(f"  오류: '{operator}'는 지원하지 않는 연산자입니다.")
            return

        name, func = OPERATIONS[operator]
        result = func(num1, num2)

        # 히스토리에 기록
        record = f"{num1} {operator} {num2} = {result}"
        history.append(record)

        print(f"\n  [{name}] {record}")
        print(f"  (총 {len(history)}건 계산 완료)")

    except ValueError as e:
        print(f"  오류: {e}")


def main():
    print("=" * 40)
    print("  계산기 v0.3 — 히스토리 기능")
    print("=" * 40)
    print("명령어: 숫자 입력 → 계산 | 'history' → 기록 | 'quit' → 종료\n")

    history = []  # 계산 기록 저장용 리스트

    while True:
        command = input("계산하려면 Enter, 'history' 또는 'quit': ").strip().lower()

        if command == "quit":
            print(f"\n총 {len(history)}건의 계산을 수행했습니다. 안녕히!")
            break
        elif command == "history":
            show_history(history)
        else:
            calculate_once(history)
            print()


if __name__ == "__main__":
    main()
