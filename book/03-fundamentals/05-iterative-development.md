# Chapter 14: 반복적 개발

바이브 코딩의 진정한 힘은 한 번의 완벽한 요청에서 나오지 않습니다. 작은 것부터 시작해서 조금씩 키워나가는 **반복적 개발(Iterative Development)**에서 나옵니다. AI에게 "완벽한 계산기를 만들어줘"라고 요청하는 대신, "덧셈만 되는 계산기"부터 시작해서 한 기능씩 추가해 나가면 훨씬 더 안정적이고 이해하기 쉬운 프로그램을 만들 수 있습니다.

이번 챕터에서는 MVP(최소 기능 제품)의 개념부터 시작해서, 점진적으로 기능을 확장하고, Git으로 안전망을 구축하며, 문제가 생겼을 때 롤백하는 전체 흐름을 실습합니다. 이 과정은 바이브 코딩뿐 아니라 모든 소프트웨어 개발의 핵심 원칙이기도 합니다.

---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- MVP(최소 기능 제품)의 개념을 이해하고 적용할 수 있다
- 작은 단위로 기능을 나누어 점진적으로 개발할 수 있다
- AI에게 기능 확장을 단계별로 요청할 수 있다
- Git을 활용해 바이브 코딩의 안전망을 구축할 수 있다
- 문제가 생겼을 때 안전하게 롤백하고 재시도할 수 있다

---

## 14.1 MVP 먼저, 작게 시작하기

### MVP란 무엇인가?

MVP는 **Minimum Viable Product**, 즉 **최소 기능 제품**입니다. "동작하는 가장 작은 버전"이라고 생각하면 됩니다. 바이브 코딩에서 MVP는 특별히 중요합니다. AI에게 한꺼번에 많은 기능을 요청하면 코드가 복잡해지고, 어디서 문제가 생겼는지 파악하기 어려워집니다. 반면 MVP부터 시작하면 다음과 같은 장점이 있습니다:

- **빠른 확인**: 핵심 아이디어가 동작하는지 즉시 확인할 수 있습니다
- **명확한 기준점**: "여기까지는 동작한다"는 확신을 가질 수 있습니다
- **쉬운 디버깅**: 문제가 생기면 가장 최근에 추가한 부분만 확인하면 됩니다
- **동기 부여**: 작은 성공이 쌓이면서 개발에 대한 자신감이 생깁니다

### 계산기 MVP: 덧셈만 되는 계산기

가장 단순한 계산기를 만들어 보겠습니다. AI에게 다음과 같이 요청합니다:

```
덧셈만 되는 아주 간단한 계산기를 만들어줘.
두 숫자를 입력받아서 더한 결과만 보여주면 돼.
```

이 요청으로 만들어진 코드를 살펴보겠습니다.

### 예제 14-1: MVP 계산기 (덧셈만)

덧셈 하나만 동작하는 최소한의 계산기입니다. 기능은 부족하지만 "동작하는 소프트웨어"라는 점이 핵심입니다.

```python
# examples/python/chapter03/ex14_01_mvp_calculator.py
"""
예제 14-1: MVP 계산기 (덧셈만)
================================
반복적 개발의 첫 단계 — 가장 단순한 버전부터 시작합니다.
MVP(Minimum Viable Product)는 '최소 기능 제품'으로,
핵심 기능 하나만 동작하는 가장 작은 버전을 말합니다.

이 계산기는 오직 '덧셈'만 할 수 있습니다.
하지만 이것만으로도 "동작하는 소프트웨어"입니다!
"""


def add(a, b):
    """두 숫자를 더합니다."""
    return a + b


def main():
    print("=" * 40)
    print("  MVP 계산기 v0.1 — 덧셈 전용")
    print("=" * 40)

    try:
        num1 = float(input("첫 번째 숫자: "))
        num2 = float(input("두 번째 숫자: "))
        result = add(num1, num2)
        print(f"\n결과: {num1} + {num2} = {result}")
    except ValueError:
        print("오류: 숫자를 입력해주세요.")

    print("\n[MVP 완료] 덧셈 기능이 동작합니다!")
    print("다음 단계: 사칙연산 추가 예정...")


if __name__ == "__main__":
    main()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_01_mvp_calculator.py
```

**결과:**

```
========================================
  MVP 계산기 v0.1 — 덧셈 전용
========================================
첫 번째 숫자: 10
두 번째 숫자: 3
결과: 10.0 + 3.0 = 13.0

[MVP 완료] 덧셈 기능이 동작합니다!
다음 단계: 사칙연산 추가 예정...
```

이 코드는 `add()` 함수 하나, `main()` 함수 하나, 총 20줄도 안 되는 아주 간단한 프로그램입니다. 하지만 다음 사실을 확인할 수 있습니다:

1. 사용자 입력을 받을 수 있다
2. 계산이 정확하게 동작한다
3. 잘못된 입력(숫자가 아닌 값)을 처리할 수 있다

이것이 바로 MVP입니다. 많은 기능이 빠져 있지만, 핵심 로직이 "동작한다"는 것을 확인했습니다.

> **Tip:** 바이브 코딩에서 MVP를 만들 때, AI에게 "가장 간단한 버전"이라고 명시하세요. "간단한 계산기를 만들어줘"보다 "덧셈만 되는 MVP 계산기를 만들어줘"가 더 작고 명확한 결과를 얻을 수 있습니다.

### 왜 작게 시작해야 할까?

큰 프로그램을 한 번에 요청하면 어떤 일이 벌어질까요?

```
❌ "사칙연산, 히스토리, 파일 저장, 실행 취소가 되는 계산기를 만들어줘"
```

이렇게 요청하면 AI가 200줄이 넘는 코드를 한꺼번에 생성합니다. 코드가 동작하면 다행이지만, 문제가 생기면:

- 어디서 오류가 발생했는지 찾기 어렵습니다
- 어떤 부분이 정상이고 어떤 부분이 비정상인지 구분할 수 없습니다
- 코드 전체를 이해하기 부담스럽습니다

반면 작게 시작하면:

```
✅ "덧셈만 되는 계산기를 만들어줘" → 확인 →
✅ "뺄셈, 곱셈, 나눗셈도 추가해줘" → 확인 →
✅ "계산 기록을 저장하는 기능을 추가해줘" → 확인 → ...
```

각 단계에서 "여기까지는 동작한다"는 확신을 가지고 다음 단계로 넘어갈 수 있습니다.

> **Tip:** MVP의 핵심 질문은 이것입니다: "이 프로그램이 제공해야 하는 가장 기본적인 가치는 무엇인가?" 계산기라면 "계산"이고, 메모장이라면 "메모 작성"입니다. 그 하나만 동작하는 버전이 MVP입니다.

---

## 14.2 점진적 기능 확장

MVP가 동작하는 것을 확인했으면, 이제 한 번에 하나씩 기능을 추가해 나갑니다. 이것을 **점진적 기능 확장(Incremental Feature Development)**이라고 합니다.

### v0.1 → v0.2: 사칙연산 추가

MVP 계산기가 잘 동작하는 것을 확인했으니, AI에게 다음 기능을 요청합니다:

```
계산기에 뺄셈, 곱셈, 나눗셈도 추가해줘.
0으로 나누기 오류도 처리해줘.
```

### 예제 14-2: 사칙연산 계산기 (v0.2)

MVP에서 한 단계 발전시켜 사칙연산을 지원하는 버전입니다. 기존의 `add()` 함수를 유지하면서 `subtract()`, `multiply()`, `divide()` 함수를 추가하고, 연산자 선택 메뉴와 0으로 나누기 오류 처리가 새로 들어갔습니다.

```python
# examples/python/chapter03/ex14_02_four_operations.py
"""
예제 14-2: 기능 추가 — 사칙연산 계산기
========================================
MVP(덧셈만)에서 한 단계 발전시켜 사칙연산을 지원합니다.
반복적 개발에서는 한 번에 하나의 기능을 추가합니다.

변경 사항:
  - 뺄셈(subtract), 곱셈(multiply), 나눗셈(divide) 함수 추가
  - 연산자 선택 메뉴 추가
  - 0으로 나누기 오류 처리 추가
"""


def add(a, b):
    """두 숫자를 더합니다."""
    return a + b


def subtract(a, b):
    """두 숫자를 뺍니다."""
    return a - b


def multiply(a, b):
    """두 숫자를 곱합니다."""
    return a * b


def divide(a, b):
    """두 숫자를 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


# 연산자 매핑 딕셔너리
OPERATIONS = {
    "+": ("덧셈", add),
    "-": ("뺄셈", subtract),
    "*": ("곱셈", multiply),
    "/": ("나눗셈", divide),
}


def main():
    print("=" * 40)
    print("  계산기 v0.2 — 사칙연산")
    print("=" * 40)

    try:
        num1 = float(input("첫 번째 숫자: "))
        print("연산자를 선택하세요: +, -, *, /")
        operator = input("연산자: ").strip()
        num2 = float(input("두 번째 숫자: "))

        if operator not in OPERATIONS:
            print(f"오류: '{operator}'는 지원하지 않는 연산자입니다.")
            return

        name, func = OPERATIONS[operator]
        result = func(num1, num2)
        print(f"\n[{name}] {num1} {operator} {num2} = {result}")

    except ValueError as e:
        print(f"오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

    print("\n[v0.2 완료] 사칙연산이 동작합니다!")
    print("다음 단계: 계산 히스토리 추가 예정...")


if __name__ == "__main__":
    main()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_02_four_operations.py
```

**결과:**

```
========================================
  계산기 v0.2 — 사칙연산
========================================
첫 번째 숫자: 10
연산자를 선택하세요: +, -, *, /
연산자: *
두 번째 숫자: 3

[곱셈] 10.0 * 3.0 = 30.0

[v0.2 완료] 사칙연산이 동작합니다!
다음 단계: 계산 히스토리 추가 예정...
```

v0.1에서 v0.2로의 변화를 정리하면:

| 항목 | v0.1 (MVP) | v0.2 (사칙연산) |
|------|-----------|----------------|
| 지원 연산 | 덧셈 | 덧셈, 뺄셈, 곱셈, 나눗셈 |
| 연산자 선택 | 없음 | 메뉴에서 선택 |
| 오류 처리 | 숫자 검증 | 숫자 검증 + 0 나누기 |
| 코드 구조 | 함수 1개 | 함수 4개 + 딕셔너리 |

기존의 `add()` 함수는 그대로 유지하면서 새로운 함수들이 추가되었습니다. 이것이 점진적 개발의 핵심입니다. **기존에 동작하던 코드를 깨뜨리지 않으면서** 새 기능을 더하는 것입니다.

### v0.2 → v0.3: 계산 히스토리 추가

사칙연산이 동작하는 것을 확인했으니, 다음 기능을 추가합니다:

```
계산 기록을 저장하고 볼 수 있게 해줘.
여러 번 반복 계산할 수 있으면 좋겠어.
```

### 예제 14-3: 계산 히스토리 (v0.3)

사칙연산 계산기에 히스토리(계산 기록) 기능을 추가한 버전입니다. 반복 계산이 가능해졌고, `history` 명령어로 이전 기록을 조회할 수 있습니다.

```python
# examples/python/chapter03/ex14_03_history.py
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
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_03_history.py
```

**결과:**

```
========================================
  계산기 v0.3 — 히스토리 기능
========================================
명령어: 숫자 입력 → 계산 | 'history' → 기록 | 'quit' → 종료

계산하려면 Enter, 'history' 또는 'quit':
첫 번째 숫자: 100
연산자 (+, -, *, /): +
두 번째 숫자: 200

  [덧셈] 100.0 + 200.0 = 300.0
  (총 1건 계산 완료)

계산하려면 Enter, 'history' 또는 'quit':
첫 번째 숫자: 50
연산자 (+, -, *, /): *
두 번째 숫자: 4

  [곱셈] 50.0 * 4.0 = 200.0
  (총 2건 계산 완료)

계산하려면 Enter, 'history' 또는 'quit': history

========================================
  계산 히스토리 (2건)
========================================
  1. 100.0 + 200.0 = 300.0
  2. 50.0 * 4.0 = 200.0

계산하려면 Enter, 'history' 또는 'quit': quit

총 2건의 계산을 수행했습니다. 안녕히!
```

v0.3에서 새로 추가된 핵심 요소는:

- **`history` 리스트**: 계산 기록을 메모리에 저장
- **`while True` 루프**: 반복 계산 가능
- **명령어 체계**: `history`, `quit` 명령어 인식

### v0.3 → v0.4: 파일 저장 기능

프로그램을 종료하면 히스토리가 사라지는 문제가 있습니다. 파일로 저장하면 다음에 다시 시작해도 기록이 유지됩니다:

```
계산 기록을 파일로 저장하고, 다시 시작할 때 불러와줘.
JSON 형식으로 저장하고, 타임스탬프도 기록해줘.
```

### 예제 14-4: 파일 저장 기능 (v0.4)

계산 히스토리를 JSON 파일로 저장하고 불러오는 기능이 추가된 버전입니다. 프로그램을 종료해도 이전 기록이 유지됩니다. `save` 명령어를 통해 수동 저장이 가능하고, 종료 시에도 자동으로 저장됩니다.

```python
# examples/python/chapter03/ex14_04_file_save.py
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


if __name__ == "__main__":
    main()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_04_file_save.py
```

**결과:**

```
========================================
  계산기 v0.4 — 파일 저장 기능
========================================
명령어: Enter→계산 | history | save | quit

명령:
첫 번째 숫자: 15
연산자 (+, -, *, /): +
두 번째 숫자: 25

  [덧셈] 15.0 + 25.0 = 40.0
  (총 1건 계산 완료)

명령: save
  1건의 기록을 'calc_history.json'에 저장했습니다.

명령: quit
  1건의 기록을 'calc_history.json'에 저장했습니다.
총 1건의 계산 기록을 저장하고 종료합니다. 안녕히!
```

### 버전별 진화 과정 요약

네 단계를 거쳐 계산기가 어떻게 발전했는지 정리해 보겠습니다:

```
v0.1 (MVP)         → 덧셈만 가능한 최소 계산기
  ↓ +뺄셈,곱셈,나눗셈
v0.2 (사칙연산)    → 네 가지 연산 지원, 연산자 선택
  ↓ +히스토리,반복계산
v0.3 (히스토리)    → 계산 기록 저장, 반복 계산 루프
  ↓ +파일저장,불러오기
v0.4 (파일 저장)   → JSON 파일 영구 저장, 타임스탬프
```

각 단계에서 AI에게 보낸 요청은 한두 문장이었지만, 결과적으로 상당히 완성도 있는 프로그램이 만들어졌습니다. 이것이 점진적 개발의 힘입니다.

> **Tip:** 기능을 추가할 때 AI에게 "기존 코드는 그대로 두고, 여기에 ~~기능을 추가해줘"라고 요청하면 기존 코드가 깨지는 것을 방지할 수 있습니다. 특히 "기존 함수를 수정하지 말고"라는 조건은 매우 효과적입니다.

---

## 14.3 Git과 바이브 코딩

### Git은 바이브 코딩의 안전망

바이브 코딩에서 Git은 단순한 버전 관리 도구가 아닙니다. AI가 생성한 코드가 마음에 들면 커밋하고, 문제가 생기면 이전 상태로 되돌릴 수 있는 **안전망**입니다. 안전망이 있으면 과감하게 새로운 시도를 할 수 있습니다. 실패해도 안전하게 되돌아갈 수 있으니까요.

Git의 기본 워크플로우를 순서대로 살펴보겠습니다.

### 예제 14-5: Git 초기화와 첫 커밋

Git 저장소를 초기화하고 첫 커밋을 만드는 전체 워크플로우를 보여주는 교육용 스크립트입니다. 실제 Git 명령어를 실행하지 않고, 각 단계에서 어떤 명령어를 사용하는지 설명합니다.

```python
# examples/python/chapter03/ex14_05_git_init.py
"""
예제 14-5: git init과 첫 커밋 시뮬레이션
==========================================
Git의 기본 흐름을 보여주는 교육용 스크립트입니다.
실제 git 명령어를 실행하지 않고, 각 단계에서
어떤 명령어를 사용하는지 설명합니다.

바이브 코딩에서 Git은 "안전망" 역할을 합니다.
AI가 생성한 코드가 마음에 들면 커밋하고,
문제가 생기면 이전 상태로 되돌릴 수 있습니다.
"""


def show_git_workflow():
    """Git 초기화부터 첫 커밋까지의 워크플로우를 보여줍니다."""

    steps = [
        {
            "title": "1단계: 프로젝트 폴더 생성",
            "commands": [
                "mkdir my-calculator",
                "cd my-calculator",
            ],
            "explanation": "새 프로젝트를 위한 빈 폴더를 만듭니다.",
        },
        {
            "title": "2단계: Git 저장소 초기화",
            "commands": [
                "git init",
            ],
            "explanation": (
                "현재 폴더를 Git 저장소로 만듭니다.\n"
                "    → .git 폴더가 생성되어 버전 관리가 시작됩니다."
            ),
        },
        {
            "title": "3단계: .gitignore 파일 생성",
            "commands": [
                'echo "__pycache__/" > .gitignore',
                'echo "*.pyc" >> .gitignore',
                'echo ".env" >> .gitignore',
            ],
            "explanation": (
                "추적하지 않을 파일 패턴을 지정합니다.\n"
                "    → 캐시 파일, 환경 변수 파일 등을 제외합니다."
            ),
        },
        {
            "title": "4단계: MVP 코드 작성",
            "commands": [
                "# AI에게 요청: 'MVP 계산기를 만들어줘. 덧셈만 되면 돼.'",
                "# → calculator.py 파일이 생성됨",
            ],
            "explanation": (
                "바이브 코딩으로 첫 번째 코드를 생성합니다.\n"
                "    → 가장 단순한 버전(MVP)부터 시작합니다."
            ),
        },
        {
            "title": "5단계: 변경 사항 확인",
            "commands": [
                "git status",
            ],
            "explanation": (
                "어떤 파일이 변경되었는지 확인합니다.\n"
                "    → 새 파일: .gitignore, calculator.py"
            ),
        },
        {
            "title": "6단계: 스테이징 (변경 사항 준비)",
            "commands": [
                "git add .",
            ],
            "explanation": (
                "모든 변경 사항을 커밋 준비 상태로 만듭니다.\n"
                "    → 또는 git add calculator.py 처럼 개별 파일 지정 가능"
            ),
        },
        {
            "title": "7단계: 첫 커밋!",
            "commands": [
                'git commit -m "feat: MVP 계산기 - 덧셈 기능 구현"',
            ],
            "explanation": (
                "현재 상태를 저장합니다. 이제 언제든 이 시점으로\n"
                "    되돌아올 수 있습니다!"
            ),
        },
        {
            "title": "8단계: 커밋 확인",
            "commands": [
                "git log --oneline",
            ],
            "explanation": (
                "커밋 이력을 확인합니다.\n"
                '    → abc1234 feat: MVP 계산기 - 덧셈 기능 구현'
            ),
        },
    ]

    print("=" * 55)
    print("  Git 초기화 & 첫 커밋 워크플로우")
    print("  (바이브 코딩의 안전망 만들기)")
    print("=" * 55)

    for step in steps:
        print(f"\n--- {step['title']} ---")
        print(f"  설명: {step['explanation']}")
        print(f"  명령어:")
        for cmd in step["commands"]:
            print(f"    $ {cmd}")

    print("\n" + "=" * 55)
    print("  첫 커밋 완료! 이제 안전하게 코드를 발전시킬 수 있습니다.")
    print("=" * 55)


if __name__ == "__main__":
    show_git_workflow()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_05_git_init.py
```

**결과:**

```
=======================================================
  Git 초기화 & 첫 커밋 워크플로우
  (바이브 코딩의 안전망 만들기)
=======================================================

--- 1단계: 프로젝트 폴더 생성 ---
  설명: 새 프로젝트를 위한 빈 폴더를 만듭니다.
  명령어:
    $ mkdir my-calculator
    $ cd my-calculator

--- 2단계: Git 저장소 초기화 ---
  설명: 현재 폴더를 Git 저장소로 만듭니다.
    → .git 폴더가 생성되어 버전 관리가 시작됩니다.
  명령어:
    $ git init

--- 3단계: .gitignore 파일 생성 ---
  설명: 추적하지 않을 파일 패턴을 지정합니다.
    → 캐시 파일, 환경 변수 파일 등을 제외합니다.
  명령어:
    $ echo "__pycache__/" > .gitignore
    $ echo "*.pyc" >> .gitignore
    $ echo ".env" >> .gitignore

--- 4단계: MVP 코드 작성 ---
  설명: 바이브 코딩으로 첫 번째 코드를 생성합니다.
    → 가장 단순한 버전(MVP)부터 시작합니다.
  명령어:
    $ # AI에게 요청: 'MVP 계산기를 만들어줘. 덧셈만 되면 돼.'
    $ # → calculator.py 파일이 생성됨

--- 5단계: 변경 사항 확인 ---
  설명: 어떤 파일이 변경되었는지 확인합니다.
    → 새 파일: .gitignore, calculator.py
  명령어:
    $ git status

--- 6단계: 스테이징 (변경 사항 준비) ---
  설명: 모든 변경 사항을 커밋 준비 상태로 만듭니다.
    → 또는 git add calculator.py 처럼 개별 파일 지정 가능
  명령어:
    $ git add .

--- 7단계: 첫 커밋! ---
  설명: 현재 상태를 저장합니다. 이제 언제든 이 시점으로
    되돌아올 수 있습니다!
  명령어:
    $ git commit -m "feat: MVP 계산기 - 덧셈 기능 구현"

--- 8단계: 커밋 확인 ---
  설명: 커밋 이력을 확인합니다.
    → abc1234 feat: MVP 계산기 - 덧셈 기능 구현
  명령어:
    $ git log --oneline

=======================================================
  첫 커밋 완료! 이제 안전하게 코드를 발전시킬 수 있습니다.
=======================================================
```

이 워크플로우에서 핵심은 **4단계(MVP 코드 작성)와 7단계(커밋)** 사이의 관계입니다. AI가 코드를 생성하고, 그 코드가 잘 동작하는 것을 확인한 후에 커밋합니다. 이렇게 하면 언제든 이 "동작하는 시점"으로 되돌아올 수 있습니다.

> **Tip:** 바이브 코딩에서 Git을 사용할 때 가장 중요한 원칙은 "동작하는 상태에서만 커밋하라"입니다. 코드가 오류 없이 실행되는 것을 확인한 후에 커밋하세요. 그래야 되돌아갈 때 항상 동작하는 코드로 복원됩니다.

### 한 기능 = 한 커밋 원칙

바이브 코딩에서 가장 효과적인 커밋 전략은 **"한 기능 = 한 커밋"** 원칙입니다. AI에게 새 기능을 요청하고, 동작을 확인하고, 커밋하는 사이클을 반복합니다.

### 예제 14-6: 기능별 커밋 만들기

각 기능을 추가할 때마다 커밋하는 워크플로우를 시뮬레이션합니다. 커밋 히스토리를 통해 프로젝트의 발전 과정을 한눈에 볼 수 있습니다.

```python
# examples/python/chapter03/ex14_06_feature_commits.py
"""
예제 14-6: 기능별 커밋 만들기
================================
각 기능을 추가할 때마다 커밋하는 워크플로우를 보여줍니다.
바이브 코딩에서 "한 기능 = 한 커밋" 원칙은 매우 중요합니다.

AI에게 새 기능을 요청할 때마다 커밋하면,
문제가 생겼을 때 정확히 어느 시점으로 돌아갈지 알 수 있습니다.
"""


def show_commit_history():
    """기능별 커밋 히스토리를 시뮬레이션합니다."""

    commits = [
        {
            "hash": "a1b2c3d",
            "message": "feat: MVP 계산기 - 덧셈 기능 구현",
            "description": "v0.1 — add() 함수, 기본 입출력",
            "files_changed": ["calculator.py"],
            "prompt": "덧셈만 되는 간단한 계산기를 만들어줘",
        },
        {
            "hash": "e4f5g6h",
            "message": "feat: 사칙연산 추가 (뺄셈, 곱셈, 나눗셈)",
            "description": "v0.2 — subtract(), multiply(), divide() 추가",
            "files_changed": ["calculator.py"],
            "prompt": "계산기에 뺄셈, 곱셈, 나눗셈도 추가해줘",
        },
        # ... (이하 생략)
    ]

    # --- 커밋 히스토리 표시 ---
    print("=" * 60)
    print("  기능별 커밋 히스토리")
    print("  (git log --oneline 스타일)")
    print("=" * 60)

    for commit in commits:
        print(f"  {commit['hash']} {commit['message']}")

    # ... (이하 생략)


if __name__ == "__main__":
    show_commit_history()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_06_feature_commits.py
```

**결과:**

```
============================================================
  기능별 커밋 히스토리
  (git log --oneline 스타일)
============================================================
  a1b2c3d feat: MVP 계산기 - 덧셈 기능 구현
  e4f5g6h feat: 사칙연산 추가 (뺄셈, 곱셈, 나눗셈)
  i7j8k9l feat: 계산 히스토리 기능 추가
  m0n1o2p feat: 히스토리 파일 저장/불러오기
  q3r4s5t fix: 0으로 나누기 오류 처리 개선
  u6v7w8x docs: README.md 추가

============================================================
  상세 커밋 히스토리
============================================================

  [1] a1b2c3d — feat: MVP 계산기 - 덧셈 기능 구현
      설명: v0.1 — add() 함수, 기본 입출력
      변경 파일: calculator.py
      AI 프롬프트: "덧셈만 되는 간단한 계산기를 만들어줘"

  [2] e4f5g6h — feat: 사칙연산 추가 (뺄셈, 곱셈, 나눗셈)
      설명: v0.2 — subtract(), multiply(), divide() 추가
      변경 파일: calculator.py
      AI 프롬프트: "계산기에 뺄셈, 곱셈, 나눗셈도 추가해줘"

  [3] i7j8k9l — feat: 계산 히스토리 기능 추가
      설명: v0.3 — history 리스트, 반복 계산 루프
      변경 파일: calculator.py
      AI 프롬프트: "계산 기록을 저장하고 볼 수 있게 해줘"

  [4] m0n1o2p — feat: 히스토리 파일 저장/불러오기
      설명: v0.4 — JSON 파일 저장, 타임스탬프 추가
      변경 파일: calculator.py
      AI 프롬프트: "계산 기록을 파일로 저장하고, 다시 시작할 때 불러와줘"

  [5] q3r4s5t — fix: 0으로 나누기 오류 처리 개선
      설명: 버그 수정 — ZeroDivisionError 예외 처리
      변경 파일: calculator.py
      AI 프롬프트: "0으로 나눌 때 에러 대신 친절한 메시지가 나오게 해줘"

  [6] u6v7w8x — docs: README.md 추가
      설명: 문서 — 프로젝트 설명, 사용법, 설치 방법
      변경 파일: README.md
      AI 프롬프트: "이 프로젝트의 README를 작성해줘"

============================================================
  커밋 메시지 규칙 (Conventional Commits)
============================================================
  feat:        새 기능 추가      예) feat: 사칙연산 추가
  fix:         버그 수정          예) fix: 0으로 나누기 오류 처리
  docs:        문서 변경          예) docs: README 추가
  refactor:    리팩토링          예) refactor: 함수 분리
  test:        테스트 추가       예) test: 사칙연산 단위 테스트
  style:       코드 스타일       예) style: PEP8 포맷 적용

  핵심 원칙:
  - 한 커밋 = 하나의 논리적 변경
  - 동작하는 상태에서만 커밋
  - 메시지는 '무엇을 했는지' 명확하게
```

상세 히스토리에서 주목할 점은 **각 커밋에 대응하는 AI 프롬프트**가 있다는 것입니다. 바이브 코딩에서의 커밋은 곧 "AI에게 보낸 요청의 결과물"입니다. 이 관계를 기억하면 프로젝트 관리가 훨씬 수월해집니다.

### 커밋 메시지 작성 규칙

위 예제에서 소개한 **Conventional Commits** 규칙을 정리하면:

| 접두어 | 의미 | 사용 시점 |
|--------|------|-----------|
| `feat:` | 새 기능 추가 | AI에게 새 기능을 요청하고 성공했을 때 |
| `fix:` | 버그 수정 | AI에게 버그 수정을 요청하고 해결했을 때 |
| `docs:` | 문서 변경 | README나 주석을 추가/수정했을 때 |
| `refactor:` | 리팩토링 | AI에게 코드 구조 개선을 요청했을 때 |
| `test:` | 테스트 추가 | AI에게 테스트 코드를 요청했을 때 |
| `style:` | 코드 스타일 | AI에게 포맷팅이나 스타일 정리를 요청했을 때 |

> **Tip:** Claude Code와 같은 AI 도구는 Git 명령어도 대신 실행해 줄 수 있습니다. "현재 변경사항을 커밋해줘. 메시지는 적절하게 작성해줘"라고 요청하면 AI가 변경 내용을 분석하고 적절한 커밋 메시지를 만들어 줍니다.

---

## 14.4 롤백과 재시도

### 실패는 성공의 과정

바이브 코딩에서 AI가 항상 완벽한 코드를 생성하는 것은 아닙니다. 때로는 새 기능을 추가하면서 기존에 잘 동작하던 기능이 망가지기도 합니다. 이런 상황이 발생했을 때 당황하지 않고 대처하는 방법을 배워야 합니다. Git이 있다면 이런 상황은 전혀 두렵지 않습니다.

### 실습: 메모장 앱 점진적 개발

롤백을 배우기 전에, 먼저 점진적 개발의 실전 예제를 하나 더 살펴보겠습니다. 계산기와는 다른 프로그램인 **메모장 앱**을 4단계에 걸쳐 만들어 봅니다.

### 예제 14-7: 메모장 앱 점진적 개발

4단계에 걸쳐 메모장 앱을 점진적으로 개발한 최종 버전입니다. 각 단계(Stage)는 독립적으로 동작하는 완성된 버전이며, 주석으로 각 단계에서 AI에게 보낸 프롬프트가 표시되어 있습니다.

```python
# examples/python/chapter03/ex14_07_memo_app.py
"""
예제 14-7: 실습 — 메모장 앱 점진적 개발
==========================================
4단계에 걸쳐 메모장 앱을 점진적으로 개발합니다.
각 단계는 독립적으로 동작하는 '완성된' 버전입니다.

Stage 1: 메모 생성 (create)
Stage 2: 메모 목록 (list)
Stage 3: 메모 검색 (search)
Stage 4: 메모 삭제 (delete)
"""

import json
import os
from datetime import datetime

MEMO_FILE = "memos.json"


# ── Stage 1: 메모 생성 ──────────────────────────
# 첫 번째 바이브 코딩 요청:
# "간단한 메모를 생성하는 프로그램을 만들어줘.
#  제목과 내용을 입력받아 저장해줘."

def create_memo(memos):
    """새 메모를 생성합니다. [Stage 1에서 추가]"""
    title = input("  제목: ").strip()
    if not title:
        print("  오류: 제목을 입력해주세요.")
        return

    content = input("  내용: ").strip()

    memo = {
        "id": len(memos) + 1,
        "title": title,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    memos.append(memo)
    save_memos(memos)
    print(f"  메모 '{title}' 생성 완료! (ID: {memo['id']})")


# ── Stage 2: 메모 목록 ──────────────────────────
# 두 번째 바이브 코딩 요청:
# "저장된 메모를 목록으로 보여주는 기능을 추가해줘.
#  번호, 제목, 생성 날짜가 보이면 좋겠어."

def list_memos(memos):
    """모든 메모를 목록으로 표시합니다. [Stage 2에서 추가]"""
    if not memos:
        print("  저장된 메모가 없습니다.")
        return

    print(f"\n  {'ID':<4} {'제목':<20} {'생성일':<16}")
    print(f"  {'-'*4} {'-'*20} {'-'*16}")
    for memo in memos:
        print(f"  {memo['id']:<4} {memo['title']:<20} {memo['created_at']:<16}")
    print(f"\n  총 {len(memos)}개의 메모")


# ── Stage 3: 메모 검색 ──────────────────────────
# 세 번째 바이브 코딩 요청:
# "메모를 키워드로 검색하는 기능을 추가해줘.
#  제목과 내용에서 모두 검색되면 좋겠어."

def search_memos(memos):
    """키워드로 메모를 검색합니다. [Stage 3에서 추가]"""
    keyword = input("  검색어: ").strip()
    if not keyword:
        print("  오류: 검색어를 입력해주세요.")
        return

    results = [
        m for m in memos
        if keyword.lower() in m["title"].lower()
        or keyword.lower() in m["content"].lower()
    ]

    if not results:
        print(f"  '{keyword}'에 대한 검색 결과가 없습니다.")
        return

    print(f"\n  '{keyword}' 검색 결과 ({len(results)}건):")
    print(f"  {'-'*40}")
    for memo in results:
        print(f"  [{memo['id']}] {memo['title']}")
        print(f"       {memo['content'][:50]}...")
        print()


# ── Stage 4: 메모 삭제 ──────────────────────────
# 네 번째 바이브 코딩 요청:
# "메모를 ID로 삭제하는 기능을 추가해줘.
#  삭제 전에 확인 질문을 해줘."

def delete_memo(memos):
    """메모를 삭제합니다. [Stage 4에서 추가]"""
    try:
        memo_id = int(input("  삭제할 메모 ID: "))
    except ValueError:
        print("  오류: 숫자를 입력해주세요.")
        return

    target = None
    for memo in memos:
        if memo["id"] == memo_id:
            target = memo
            break

    if target is None:
        print(f"  오류: ID {memo_id}번 메모를 찾을 수 없습니다.")
        return

    print(f"  제목: {target['title']}")
    print(f"  내용: {target['content']}")
    confirm = input("  정말 삭제하시겠습니까? (y/n): ").strip().lower()

    if confirm == "y":
        memos.remove(target)
        save_memos(memos)
        print(f"  메모 '{target['title']}' 삭제 완료!")
    else:
        print("  삭제를 취소했습니다.")


# ── 파일 저장/불러오기 유틸리티 ──────────────────

def load_memos():
    """파일에서 메모를 불러옵니다."""
    if os.path.exists(MEMO_FILE):
        with open(MEMO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memos(memos):
    """메모를 파일로 저장합니다."""
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)


# ── 메인 프로그램 ──────────────────────────────

def main():
    print("=" * 45)
    print("  메모장 v1.0 — 점진적 개발 완성본")
    print("=" * 45)
    print("  명령어: create | list | search | delete | quit")
    print()

    memos = load_memos()
    if memos:
        print(f"  ({len(memos)}개의 저장된 메모를 불러왔습니다)\n")

    commands = {
        "create": ("메모 생성", create_memo),
        "list": ("메모 목록", list_memos),
        "search": ("메모 검색", search_memos),
        "delete": ("메모 삭제", delete_memo),
    }

    while True:
        command = input("[메모장] > ").strip().lower()

        if command == "quit":
            print(f"\n  메모장을 종료합니다. (총 {len(memos)}개 메모)")
            break
        elif command in commands:
            name, func = commands[command]
            print(f"\n  --- {name} ---")
            func(memos)
            print()
        elif command == "":
            continue
        else:
            print(f"  알 수 없는 명령어: '{command}'")
            print("  사용 가능: create | list | search | delete | quit\n")


if __name__ == "__main__":
    main()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_07_memo_app.py
```

**결과:**

```
=============================================
  메모장 v1.0 — 점진적 개발 완성본
=============================================
  명령어: create | list | search | delete | quit

[메모장] > create

  --- 메모 생성 ---
  제목: 바이브 코딩 공부
  내용: Chapter 14 반복적 개발 학습 중
  메모 '바이브 코딩 공부' 생성 완료! (ID: 1)

[메모장] > create

  --- 메모 생성 ---
  제목: 장보기 목록
  내용: 우유, 빵, 계란, 사과
  메모 '장보기 목록' 생성 완료! (ID: 2)

[메모장] > list

  --- 메모 목록 ---

  ID   제목                   생성일
  ---- -------------------- ----------------
  1    바이브 코딩 공부       2026-01-27 14:30
  2    장보기 목록            2026-01-27 14:31

  총 2개의 메모

[메모장] > search

  --- 메모 검색 ---
  검색어: 코딩

  '코딩' 검색 결과 (1건):
  ----------------------------------------
  [1] 바이브 코딩 공부
       Chapter 14 반복적 개발 학습 중...

[메모장] > quit

  메모장을 종료합니다. (총 2개 메모)
```

이 메모장 앱의 진화 과정을 보면, 계산기와 동일한 패턴을 따릅니다:

```
Stage 1: create만 가능 → "메모를 만들 수 있다" (MVP)
Stage 2: + list 추가   → "저장된 메모를 볼 수 있다"
Stage 3: + search 추가 → "원하는 메모를 찾을 수 있다"
Stage 4: + delete 추가 → "필요 없는 메모를 지울 수 있다"
```

각 Stage마다 AI에게 보낸 프롬프트가 주석에 기록되어 있습니다. 실제 바이브 코딩에서도 이처럼 단계별로 요청하는 것이 효과적입니다.

> **Tip:** 점진적 개발의 순서를 정할 때는 "사용자가 가장 기본적으로 필요로 하는 기능"부터 시작하세요. 메모장이라면 "메모 작성"이 없으면 아무것도 할 수 없으니 가장 먼저 만들고, "목록 보기"가 그 다음, "검색"과 "삭제"는 그 이후입니다.

### 실패 시 롤백하기

이제 바이브 코딩에서 가장 중요한 생존 기술을 배울 차례입니다. AI에게 새 기능을 요청했는데, 기존에 잘 동작하던 기능이 망가지는 상황입니다. 이런 일은 실제로 자주 발생합니다.

### 예제 14-8: 실패 시 롤백하기

새 기능을 추가했는데 기존 기능이 망가지는 상황을 시뮬레이션합니다. v0.4 계산기에 "제곱근, 거듭제곱" 기능을 추가했더니 기존 덧셈 함수가 거듭제곱으로 바뀌어 버리는 버그가 발생합니다.

```python
# examples/python/chapter03/ex14_08_rollback.py
"""
예제 14-8: 실습 — 실패 시 롤백하기
=====================================
새 기능을 추가했는데 기존 기능이 망가지는 상황을 시뮬레이션합니다.

시나리오:
  1. v0.4 계산기가 잘 동작하고 있음 (안정 버전)
  2. "고급 수학 함수(제곱근, 거듭제곱)"를 추가 요청
  3. AI가 생성한 코드에 버그 발생! (기존 사칙연산이 망가짐)
  4. git checkout으로 안정 버전으로 롤백
  5. 다시 요청하여 올바른 코드 획득
"""


# ── 안정 버전 (v0.4) ── 잘 동작하는 코드 ──────────

def calculator_v04():
    """v0.4 안정 버전: 사칙연산이 정상 동작합니다."""
    print("[v0.4 안정 버전] 사칙연산 테스트")

    tests = [
        ("10 + 3", 10 + 3, 13),
        ("10 - 3", 10 - 3, 7),
        ("10 * 3", 10 * 3, 30),
        ("10 / 3", round(10 / 3, 2), 3.33),
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if round(result, 2) == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} [{status}]")

    return all_passed


# ── 버그 버전 (v0.5-buggy) ──────────────────────

def add_buggy(a, b):
    """버그! AI가 제곱근 기능 추가하면서 실수로 add를 변경."""
    return a ** b  # 덧셈이 거듭제곱이 되어버림!


def calculator_v05_buggy():
    """v0.5 버그 버전: 고급 함수 추가 후 기존 기능이 망가짐!"""
    print("[v0.5 버그 버전] 고급 수학 함수 추가 후 테스트")

    tests = [
        ("10 + 3", add_buggy(10, 3), 13),      # 10**3 = 1000 (버그!)
        ("sqrt(16)", 16 ** 0.5, 4.0),            # 새 기능 정상
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} (기대값: {expected}) [{status}]")

    return all_passed


# ── 수정 버전 (v0.5-fixed) ──────────────────────

def calculator_v05_fixed():
    """v0.5 수정 버전: 기존 기능 유지 + 새 기능 추가"""
    print("[v0.5 수정 버전] 기존 기능 + 고급 수학 함수")

    tests = [
        ("10 + 3", 10 + 3, 13),
        ("10 - 3", 10 - 3, 7),
        ("10 * 3", 10 * 3, 30),
        ("10 / 2", 10 / 2, 5.0),
        ("sqrt(16)", 16 ** 0.5, 4.0),
        ("2 ** 10", 2 ** 10, 1024),
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} [{status}]")

    return all_passed


if __name__ == "__main__":
    main()
```

**실행:**

```bash
$ python examples/python/chapter03/ex14_08_rollback.py
```

**결과:**

```
============================================================
  롤백 시나리오 시뮬레이션
  (새 기능 추가 → 버그 발생 → 롤백 → 재시도)
============================================================

────────────────────────────────────────────────────────────
단계 1: 현재 안정 버전 확인
────────────────────────────────────────────────────────────
[v0.4 안정 버전] 사칙연산 테스트
  10 + 3 = 13 [PASS]
  10 - 3 = 7 [PASS]
  10 * 3 = 30 [PASS]
  10 / 3 = 3.33 [PASS]
  결과: 모든 테스트 통과!

────────────────────────────────────────────────────────────
단계 2: AI에게 고급 수학 함수 추가 요청
  프롬프트: '제곱근과 거듭제곱 기능을 추가해줘'
────────────────────────────────────────────────────────────
[v0.5 버그 버전] 고급 수학 함수 추가 후 테스트
  10 + 3 = 1000 (기대값: 13) [FAIL]
  10 - 3 = 7 (기대값: 7) [PASS]
  sqrt(16) = 4.0 (기대값: 4.0) [PASS]
  결과: 버그 발견! 기존 기능이 망가졌습니다!

────────────────────────────────────────────────────────────
단계 3: Git으로 안정 버전으로 롤백
────────────────────────────────────────────────────────────
  실행할 Git 명령어:
  $ git diff                     # 무엇이 변경되었는지 확인
  $ git stash                    # 현재 변경사항 임시 저장
  $ git checkout HEAD -- .       # 마지막 커밋 상태로 복원
  (또는)
  $ git checkout HEAD -- calculator.py  # 특정 파일만 복원
  → 안정 버전(v0.4)으로 되돌아감!

────────────────────────────────────────────────────────────
단계 4: AI에게 더 구체적으로 다시 요청
  프롬프트: '기존 add, subtract, multiply, divide 함수를 절대
  수정하지 말고, sqrt와 power 함수만 새로 추가해줘.'
────────────────────────────────────────────────────────────
[v0.5 수정 버전] 기존 기능 + 고급 수학 함수
  10 + 3 = 13 [PASS]
  10 - 3 = 7 [PASS]
  10 * 3 = 30 [PASS]
  10 / 2 = 5.0 [PASS]
  sqrt(16) = 4.0 [PASS]
  2 ** 10 = 1024 [PASS]
  결과: 모든 테스트 통과!

============================================================
  롤백 시나리오 요약
============================================================
  1. 새 기능 추가 시 기존 기능이 망가질 수 있다
  2. Git이 있으면 안전하게 이전 상태로 돌아갈 수 있다
  3. 롤백 후 더 구체적인 프롬프트로 재시도한다
  4. '기존 코드를 수정하지 말고'라는 조건을 명시한다

  핵심: 자주 커밋하고, 문제가 생기면 롤백하라!
```

이 시뮬레이션에서 보여주는 핵심은 4단계 사이클입니다:

```
1. 안정 버전 확인  →  "지금까지는 잘 동작한다"
2. 새 기능 요청    →  AI가 코드를 생성하지만 버그 발생
3. 롤백            →  Git으로 안정 버전으로 되돌아감
4. 재시도          →  더 구체적인 프롬프트로 다시 요청
```

### 롤백을 위한 핵심 Git 명령어

실제로 롤백이 필요한 상황에서 사용할 수 있는 Git 명령어를 정리합니다:

```bash
# 1. 변경 사항 확인
$ git diff                           # 무엇이 변경되었는지 확인

# 2. 특정 파일만 되돌리기
$ git checkout HEAD -- calculator.py # 마지막 커밋 상태로 복원

# 3. 모든 변경 사항 되돌리기
$ git checkout HEAD -- .             # 모든 파일을 마지막 커밋으로

# 4. 변경 사항 임시 저장 (나중에 다시 쓸 수 있음)
$ git stash                          # 변경 사항 임시 보관
$ git stash pop                      # 임시 보관한 내용 복원

# 5. 이전 커밋으로 되돌아가기
$ git log --oneline                  # 커밋 히스토리 확인
$ git checkout abc1234               # 특정 커밋으로 이동
```

> **Tip:** 롤백 후 재시도할 때는 **프롬프트를 더 구체적으로** 작성하세요. 특히 "기존 함수를 절대 수정하지 말고, 새 함수만 추가해줘"처럼 AI가 기존 코드를 건드리지 않도록 명확한 조건을 붙이는 것이 효과적입니다.

### 롤백과 재시도의 황금 규칙

바이브 코딩에서 롤백과 재시도를 효과적으로 활용하기 위한 규칙을 정리합니다:

**규칙 1: 자주 커밋하라**

새 기능이 동작할 때마다 커밋합니다. 커밋 간격이 짧을수록 롤백 시 잃어버리는 코드가 적습니다.

```bash
# 좋은 패턴: 기능마다 커밋
$ git commit -m "feat: 덧셈 기능"
# (다음 기능 개발)
$ git commit -m "feat: 뺄셈 기능"

# 나쁜 패턴: 오랜 시간 커밋 없이 작업
# (모든 기능을 한꺼번에 개발한 후 커밋)
$ git commit -m "feat: 모든 기능 추가"
```

**규칙 2: 테스트 후 커밋하라**

코드가 오류 없이 동작하는 것을 확인한 후에만 커밋합니다. 그래야 롤백했을 때 항상 동작하는 코드로 복원됩니다.

**규칙 3: 롤백 후에는 프롬프트를 개선하라**

같은 프롬프트로 다시 요청하면 같은 문제가 반복될 수 있습니다. 롤백 후에는 반드시 프롬프트를 더 구체적으로 수정합니다.

```
# 첫 번째 시도 (실패)
"제곱근과 거듭제곱 기능을 추가해줘"

# 두 번째 시도 (성공)
"기존 add, subtract, multiply, divide 함수를 절대 수정하지 말고,
sqrt와 power 함수만 새로 추가해줘.
기존 테스트가 모두 통과하는지 확인해줘."
```

**규칙 4: 실패 원인을 분석하라**

AI가 왜 기존 코드를 망가뜨렸는지 이해하면, 다음에 같은 실수를 방지할 수 있습니다. 위 예제에서는 AI가 `add()` 함수를 거듭제곱으로 변경한 것이 문제였습니다. "기존 함수를 수정하지 말라"는 조건을 추가하면 이런 문제를 예방할 수 있습니다.

> **Tip:** 바이브 코딩의 반복 사이클을 한 문장으로 요약하면 이렇습니다: **"요청 → 확인 → 커밋 → 요청 → 확인 → 커밋"**. 이 리듬을 유지하면서 문제가 생기면 롤백하고 다시 시작합니다. 이것이 바이브 코딩의 핵심 흐름입니다.

---

## Part 3 마무리

Part 3 "바이브 코딩 기초"를 모두 완료했습니다. Chapter 10부터 Chapter 14까지 다섯 개 챕터에 걸쳐 바이브 코딩의 핵심 기술을 배웠습니다. 지금까지 배운 내용을 정리해 보겠습니다.

### Chapter 10: 프롬프트 엔지니어링 기초

AI에게 효과적으로 요청하는 방법을 배웠습니다. 모호한 요청보다 구체적인 요청이 더 좋은 결과를 만들고, 역할 지정, 맥락 제공, 출력 형식 지정, Few-shot 예시, Chain of Thought 등의 기법을 활용하면 AI의 응답 품질을 크게 높일 수 있습니다.

**핵심 키워드:** 구체적 요청, 역할-맥락-요청-형식, Few-shot, Chain of Thought

### Chapter 11: AI와의 대화 기술

단일 요청이 아닌 대화를 통해 코드를 발전시키는 기술을 배웠습니다. 컨텍스트를 유지하며 단계별로 요청하고, 긍정적 피드백과 수정 피드백을 적절히 활용하는 방법을 익혔습니다.

**핵심 키워드:** 대화형 개발, 컨텍스트 유지, 단계별 요청, 피드백

### Chapter 12: 코드 리뷰와 수정

AI가 생성한 코드를 검토하고 개선하는 방법을 배웠습니다. "이 코드 설명해줘"로 시작해서, 변수명 개선, 함수 분리, 중복 제거, PEP8 스타일 적용 등의 리팩토링 기법을 AI에게 요청하는 방법을 익혔습니다.

**핵심 키워드:** 코드 리뷰, 리팩토링, 가독성 개선, 코드 스타일

### Chapter 13: AI와 함께 디버깅하기

오류 메시지를 읽고, AI에게 디버깅을 요청하는 방법을 배웠습니다. SyntaxError부터 논리 오류까지 다양한 종류의 버그를 AI와 함께 해결하는 경험을 했고, 스택 트레이스 분석과 예방적 디버깅 전략도 배웠습니다.

**핵심 키워드:** 오류 해석, 스택 트레이스, 논리 오류, 예외 처리

### Chapter 14: 반복적 개발 (이번 챕터)

MVP부터 시작해서 점진적으로 기능을 확장하고, Git으로 안전망을 구축하며, 문제가 생겼을 때 롤백하는 전체 흐름을 배웠습니다. "요청 → 확인 → 커밋"의 반복 사이클이 바이브 코딩의 핵심 리듬입니다.

**핵심 키워드:** MVP, 점진적 개발, Git 안전망, 롤백과 재시도

### Part 3에서 배운 것을 한 그림으로

```
[프롬프트 작성] ──→ [AI에게 요청] ──→ [코드 생성]
      ↑                                    │
      │                                    ↓
 [프롬프트 개선]                      [코드 리뷰]
      ↑                                    │
      │                                    ↓
   [롤백]  ←── [문제 발견] ←── [실행 & 테스트]
                                           │
                                           ↓ (성공)
                                    [Git 커밋] ──→ [다음 기능]
```

이 다섯 가지 기술은 서로 밀접하게 연결되어 있습니다. 좋은 프롬프트로 AI에게 요청하고(Ch.10), 대화를 통해 발전시키며(Ch.11), 코드를 검토하고(Ch.12), 문제가 있으면 디버깅하고(Ch.13), 이 전체 과정을 반복적으로 수행합니다(Ch.14).

---

## 다음 장 예고

Part 4 "실전 바이브 코딩"에서는 이제까지 배운 기초를 바탕으로 실제 프로젝트를 만들어 봅니다. Chapter 15에서는 **파일 처리 자동화**를 다룹니다. 텍스트 파일 읽기/쓰기, CSV 및 JSON 파일 처리, 디렉토리 탐색과 파일 정리 등 실무에서 자주 사용하는 파일 처리 기술을 AI와 함께 구현합니다. Part 3에서 배운 프롬프트 작성법, 대화 기술, 코드 리뷰, 디버깅, 반복적 개발을 모두 활용하게 될 것입니다.
