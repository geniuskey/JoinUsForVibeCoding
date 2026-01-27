"""
예제 14-4: 기능 추가 — 파일 저장
==================================
계산 히스토리를 파일로 저장하고 불러오는 기능을 추가합니다.
프로그램을 종료해도 이전 기록이 유지됩니다.

변경 사항:
  - JSON 파일로 히스토리 저장 (save_history)
  - 프로그램 시작 시 히스토리 불러오기 (load_history)
  - 'save' 명령어 추가
  - 종료 시 자동 저장
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "calc_history.json"


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


def load_history(filepath):
    """파일에서 히스토리를 불러옵니다."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"  저장된 기록 {len(data)}건을 불러왔습니다.")
            return data
    return []


def save_history(history, filepath):
    """히스토리를 파일로 저장합니다."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"  {len(history)}건의 기록을 '{filepath}'에 저장했습니다.")


def show_history(history):
    """계산 히스토리를 출력합니다."""
    if not history:
        print("  (아직 계산 기록이 없습니다)")
        return

    print(f"\n{'='*40}")
    print(f"  계산 히스토리 ({len(history)}건)")
    print(f"{'='*40}")
    for i, record in enumerate(history, 1):
        expr = record["expression"]
        time = record["timestamp"]
        print(f"  {i}. [{time}] {expr}")
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

        expression = f"{num1} {operator} {num2} = {result}"
        record = {
            "expression": expression,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        history.append(record)

        print(f"\n  [{name}] {expression}")
        print(f"  (총 {len(history)}건 계산 완료)")

    except ValueError as e:
        print(f"  오류: {e}")


def main():
    print("=" * 40)
    print("  계산기 v0.4 — 파일 저장 기능")
    print("=" * 40)
    print("명령어: Enter→계산 | history | save | quit\n")

    # 저장된 히스토리 불러오기
    history = load_history(HISTORY_FILE)

    while True:
        command = input("\n명령: ").strip().lower()

        if command == "quit":
            save_history(history, HISTORY_FILE)
            print(f"총 {len(history)}건의 계산 기록을 저장하고 종료합니다. 안녕히!")
            break
        elif command == "history":
            show_history(history)
        elif command == "save":
            save_history(history, HISTORY_FILE)
        else:
            calculate_once(history)

    # 저장된 파일 확인
    if os.path.exists(HISTORY_FILE):
        size = os.path.getsize(HISTORY_FILE)
        print(f"\n[파일 확인] {HISTORY_FILE} ({size} bytes)")


if __name__ == "__main__":
    main()
