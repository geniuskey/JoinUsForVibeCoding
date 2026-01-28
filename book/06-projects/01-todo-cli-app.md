# Chapter 25: 프로젝트 1 - CLI 할일 관리 앱

지금까지 배운 모든 것을 활용하여 첫 번째 실전 프로젝트를 완성합니다. 터미널에서 동작하는 **CLI 할일 관리 앱**을 처음부터 끝까지 바이브 코딩으로 만들어봅니다. AI에게 단계별로 요청하며 기능을 하나씩 추가하고, 각 단계에서 코드를 실행해 결과를 확인하는 **반복적인 개발 과정(Iterative Development)**을 체험합니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- **프로젝트 요구사항**을 정의하고 기능 목록을 작성할 수 있다
- AI에게 **단계별 프롬프트**를 보내 점진적으로 기능을 구현할 수 있다
- **프로젝트 디렉토리 구조**를 설계하고 생성할 수 있다
- Python `argparse`로 **CLI 인터페이스**를 구성할 수 있다
- `dataclass`와 `Enum`으로 **데이터 모델**을 설계할 수 있다
- **CRUD**(생성, 읽기, 수정, 삭제) 기능을 구현할 수 있다
- **JSON 파일**로 데이터를 영구 저장하고 불러올 수 있다
- **검색과 필터** 기능으로 데이터를 효과적으로 조회할 수 있다
- 개별 모듈을 **하나의 완성된 앱**으로 통합할 수 있다

---

## 25.1 프로젝트 개요와 목표

### 무엇을 만드는가?

터미널에서 동작하는 **할일(Todo) 관리 앱**을 만듭니다. 다음과 같이 사용할 수 있는 도구입니다:

```bash
# 할일 추가
$ todo add "보고서 작성" --priority high --due 2025-12-31

# 할일 목록 확인
$ todo list

# 할일 완료 처리
$ todo complete 1

# 할일 검색
$ todo search "보고서"
```

GUI(그래픽 인터페이스) 없이 터미널 명령어만으로 모든 기능을 사용합니다. 이런 형태의 도구를 **CLI(Command Line Interface) 앱**이라고 부릅니다.

### 왜 CLI 앱인가?

CLI 앱은 첫 번째 프로젝트로 최적의 선택입니다:

| 장점 | 설명 |
|------|------|
| **단순한 구조** | 웹 서버나 데이터베이스 없이 파이썬만으로 완성 가능 |
| **빠른 피드백** | 코드를 작성하고 바로 터미널에서 실행하여 결과 확인 |
| **핵심 개념 학습** | 파일 I/O, 데이터 구조, 에러 처리 등 기본기를 모두 활용 |
| **실용적** | 실제로 일상에서 사용할 수 있는 도구 |
| **확장 가능** | 나중에 웹 UI나 데이터베이스를 추가하여 발전시킬 수 있음 |

### 바이브 코딩 접근법

이 프로젝트에서는 **"한 번에 전부"가 아니라 "조금씩 반복"**하는 접근법을 사용합니다:

```
Step 1: 프로젝트 뼈대 만들기
    ↓ 실행 & 확인
Step 2: 데이터 모델 + 추가/목록 기능
    ↓ 실행 & 확인
Step 3: 완료/삭제 기능
    ↓ 실행 & 확인
Step 4: 파일 저장/불러오기
    ↓ 실행 & 확인
Step 5: 검색/필터 기능
    ↓ 실행 & 확인
완성: 전체 통합
```

각 단계마다 AI에게 구체적인 프롬프트를 보내고, 실행 결과를 확인한 뒤, 다음 단계로 넘어갑니다. 실제 바이브 코딩 개발 과정을 그대로 재현합니다.

> **Tip:** 복잡한 프로젝트도 작은 단계로 나누면 관리할 수 있습니다. "코끼리를 먹는 방법은? 한 입씩!"이라는 격언을 기억하세요.

---

## 25.2 요구사항 정의

프로젝트를 시작하기 전에, AI에게 전체 그림을 먼저 설명합니다.

### AI에게 보내는 첫 프롬프트

```
CLI로 동작하는 할일(Todo) 관리 앱을 Python으로 만들고 싶어.
다음 기능이 필요해:

1. 할일 추가: 제목, 우선순위(높음/보통/낮음), 마감일, 태그 지정
2. 할일 목록: 미완료 목록 보기, 전체 목록 보기
3. 할일 완료: 특정 할일을 완료 상태로 변경
4. 할일 삭제: 완료된 할일 삭제, 강제 삭제 옵션
5. 데이터 저장: JSON 파일로 저장하고 불러오기
6. 검색: 키워드로 할일 검색
7. 필터: 우선순위, 상태, 태그별 필터링

먼저 프로젝트 디렉토리 구조를 설계해줘.
```

이 프롬프트에서 중요한 점은 **전체 기능 목록을 먼저 나열**한 것입니다. AI가 전체적인 설계를 이해한 상태에서 각 부분을 구현하면 코드의 일관성이 훨씬 좋아집니다.

### 기능 요구사항 정리

AI의 도움을 받아 기능을 정리하면 다음과 같습니다:

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `add` | 할일 추가 | `todo add "우유 사기" -p high` |
| `list` | 목록 표시 | `todo list --all` |
| `complete` | 완료 처리 | `todo complete 1` |
| `delete` | 삭제 | `todo delete 1 --force` |
| `search` | 키워드 검색 | `todo search "보고서"` |
| `filter` | 조건 필터 | `todo filter --priority high` |
| `stats` | 통계 보기 | `todo stats` |

---

## 25.3 기술 스택 선택

### 사용 기술

이 프로젝트에서는 Python **표준 라이브러리만** 사용합니다. 외부 패키지를 설치할 필요가 없습니다:

| 모듈 | 용도 |
|------|------|
| `argparse` | CLI 명령어 파싱 |
| `dataclasses` | 데이터 모델 정의 |
| `enum` | 우선순위 열거형 |
| `json` | 데이터 저장/로드 |
| `datetime` | 날짜/시간 처리 |
| `os`, `pathlib` | 파일/디렉토리 관리 |

> **Note:** 표준 라이브러리만 사용하면 `pip install` 없이 어디서든 바로 실행할 수 있는 장점이 있습니다. 실전에서는 `click`이나 `typer` 같은 라이브러리를 사용하면 CLI를 더 쉽게 만들 수 있습니다.

---

## 25.4 Step 1: 프로젝트 구조 설정

### 프롬프트 1: 디렉토리 구조

```
할일 관리 CLI 앱의 프로젝트 디렉토리 구조를 생성하는
Python 스크립트를 작성해줘.
다음 구조로 만들어줘:
- src/ : 소스 코드 (main.py, commands/, models/, utils/)
- data/ : 데이터 저장
- tests/ : 테스트 코드
모든 Python 패키지에 __init__.py를 포함해줘.
```

AI가 생성한 코드는 프로젝트의 뼈대를 자동으로 만들어 줍니다:

**예제 25-01: 디렉토리 구조 생성**

```python
# examples/python/chapter06/ex25_01_directory_structure.py
import os
import shutil
from pathlib import Path


def create_project_structure(base_dir: str) -> list[str]:
    """CLI 할일 관리 앱의 프로젝트 디렉토리 구조를 생성합니다."""

    # 프로젝트 디렉토리 구조 정의
    directories = [
        "",                    # 프로젝트 루트
        "src",                 # 소스 코드
        "src/commands",        # CLI 명령어 모듈
        "src/models",          # 데이터 모델
        "src/utils",           # 유틸리티 함수
        "data",                # 데이터 저장소
        "tests",               # 테스트 코드
    ]

    # 기본 파일 정의 (파일 경로: 파일 내용)
    files = {
        "README.md": "# CLI 할일 관리 앱\n\n바이브 코딩으로 만드는 할일 관리 도구입니다.\n",
        "src/__init__.py": '"""CLI 할일 관리 앱 패키지"""\n',
        "src/commands/__init__.py": '"""명령어 모듈"""\n',
        "src/models/__init__.py": '"""데이터 모델 모듈"""\n',
        "src/utils/__init__.py": '"""유틸리티 모듈"""\n',
        "src/main.py": '"""앱 진입점"""\n\ndef main():\n    print("할일 관리 앱 시작!")\n\nif __name__ == "__main__":\n    main()\n',
        "src/commands/add.py": '"""할일 추가 명령어"""\n',
        "src/commands/list_todos.py": '"""할일 목록 명령어"""\n',
        "src/commands/complete.py": '"""할일 완료 명령어"""\n',
        "src/commands/delete.py": '"""할일 삭제 명령어"""\n',
        "src/models/todo.py": '"""할일 데이터 모델"""\n',
        "src/utils/storage.py": '"""데이터 저장/불러오기 유틸리티"""\n',
        "src/utils/display.py": '"""화면 출력 유틸리티"""\n',
        "data/.gitkeep": "",
        "tests/__init__.py": '"""테스트 패키지"""\n',
        "tests/test_todo.py": '"""할일 모델 테스트"""\n',
    }

    created_items = []

    # 디렉토리 생성
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        created_items.append(f"[폴더] {dir_path}/")

    # 파일 생성
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        created_items.append(f"[파일] {full_path}")

    return created_items
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_01_directory_structure.py
```

**결과:**
```
==================================================
CLI 할일 관리 앱 - 프로젝트 구조 생성
==================================================

프로젝트 위치: /tmp/todo-cli-app
총 21개 항목 생성 완료!

--- 프로젝트 트리 ---
todo-cli-app/
├── data/
│   └── .gitkeep
├── src/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── add.py
│   │   ├── complete.py
│   │   ├── delete.py
│   │   └── list_todos.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── display.py
│   │   └── storage.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_todo.py
└── README.md
```

### 구조 설계의 핵심 원칙

생성된 디렉토리 구조를 살펴보면 몇 가지 설계 원칙이 보입니다:

| 디렉토리 | 역할 | 설계 원칙 |
|-----------|------|-----------|
| `src/commands/` | 각 CLI 명령어 | **단일 책임** - 명령어당 하나의 파일 |
| `src/models/` | 데이터 구조 | **모델 분리** - 데이터와 로직 분리 |
| `src/utils/` | 공통 기능 | **재사용** - 여러 곳에서 쓰는 코드 |
| `data/` | JSON 저장소 | **데이터 분리** - 코드와 데이터 분리 |
| `tests/` | 테스트 코드 | **품질 보장** - 테스트 가능한 구조 |

> **Tip:** 처음부터 완벽한 구조를 만들 필요는 없습니다. 바이브 코딩에서는 "일단 동작하는 구조를 만들고, 필요할 때 개선"하는 것이 효과적입니다.

### 프롬프트 2: CLI 뼈대 구성

```
Python argparse를 사용해서 CLI 뼈대를 만들어줘.
서브커맨드로 add, list, complete, delete를 지원해야 해.
각 명령어의 옵션도 정의해줘:
- add: title(필수), --priority(선택), --due(선택)
- list: --all 옵션
- complete: id(필수)
- delete: id(필수), --force 옵션
일단 각 명령어는 받은 인자를 출력만 하는 뼈대로 만들어줘.
```

**예제 25-02: 기본 CLI 뼈대**

```python
# examples/python/chapter06/ex25_02_cli_skeleton.py
import argparse


def handle_add(args: argparse.Namespace) -> None:
    """할일 추가 명령어 핸들러 (뼈대)"""
    print(f"[add] 할일 추가: '{args.title}'")
    if args.priority:
        print(f"  우선순위: {args.priority}")
    if args.due:
        print(f"  마감일: {args.due}")


def handle_list(args: argparse.Namespace) -> None:
    """할일 목록 명령어 핸들러 (뼈대)"""
    print("[list] 할일 목록 표시")
    if args.all:
        print("  완료된 항목 포함")
    else:
        print("  미완료 항목만")


def handle_complete(args: argparse.Namespace) -> None:
    """할일 완료 명령어 핸들러 (뼈대)"""
    print(f"[complete] 할일 #{args.id} 완료 처리")


def handle_delete(args: argparse.Namespace) -> None:
    """할일 삭제 명령어 핸들러 (뼈대)"""
    print(f"[delete] 할일 #{args.id} 삭제")
    if args.force:
        print("  강제 삭제 (확인 없음)")


def create_parser() -> argparse.ArgumentParser:
    """CLI 파서를 생성하고 서브커맨드를 등록합니다."""

    # 메인 파서 생성
    parser = argparse.ArgumentParser(
        prog="todo",
        description="CLI 할일 관리 앱 - 터미널에서 할일을 관리하세요!",
        epilog="예시: todo add '우유 사기' --priority high",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # 서브커맨드 그룹 생성
    subparsers = parser.add_subparsers(
        title="명령어", description="사용 가능한 명령어", dest="command",
    )

    # --- add 서브커맨드 ---
    add_parser = subparsers.add_parser("add", help="새로운 할일을 추가합니다")
    add_parser.add_argument("title", help="할일 제목")
    add_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"],
                            default="medium", help="우선순위 (기본값: medium)")
    add_parser.add_argument("-d", "--due", help="마감일 (YYYY-MM-DD 형식)")
    add_parser.set_defaults(func=handle_add)

    # --- list 서브커맨드 ---
    list_parser = subparsers.add_parser("list", help="할일 목록을 표시합니다")
    list_parser.add_argument("-a", "--all", action="store_true",
                             help="완료된 항목도 함께 표시")
    list_parser.set_defaults(func=handle_list)

    # --- complete 서브커맨드 ---
    complete_parser = subparsers.add_parser("complete", help="할일을 완료 처리합니다")
    complete_parser.add_argument("id", type=int, help="완료할 할일 번호")
    complete_parser.set_defaults(func=handle_complete)

    # --- delete 서브커맨드 ---
    delete_parser = subparsers.add_parser("delete", help="할일을 삭제합니다")
    delete_parser.add_argument("id", type=int, help="삭제할 할일 번호")
    delete_parser.add_argument("-f", "--force", action="store_true",
                               help="확인 없이 삭제")
    delete_parser.set_defaults(func=handle_delete)

    return parser
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_02_cli_skeleton.py
```

**결과:**
```
==================================================
CLI 할일 관리 앱 - 기본 CLI 뼈대 데모
==================================================

>>> todo add 우유 사기 --priority high
[add] 할일 추가: '우유 사기'
  우선순위: high

>>> todo add 보고서 작성 -d 2025-12-31
[add] 할일 추가: '보고서 작성'
  마감일: 2025-12-31

>>> todo list
[list] 할일 목록 표시
  미완료 항목만

>>> todo list --all
[list] 할일 목록 표시
  완료된 항목 포함

>>> todo complete 1
[complete] 할일 #1 완료 처리

>>> todo delete 2 --force
[delete] 할일 #2 삭제
  강제 삭제 (확인 없음)
```

### argparse의 핵심 구성요소

이 뼈대 코드에서 `argparse`의 핵심 패턴을 배울 수 있습니다:

```
ArgumentParser (메인 파서)
├── add_subparsers()     # 서브커맨드 그룹
│   ├── add_parser("add")       # add 서브커맨드
│   │   ├── add_argument("title")     # 필수 인자
│   │   └── add_argument("--priority") # 옵션 인자
│   ├── add_parser("list")      # list 서브커맨드
│   ├── add_parser("complete")  # complete 서브커맨드
│   └── add_parser("delete")    # delete 서브커맨드
└── parse_args()         # 인자 파싱 실행
```

> **Note:** `set_defaults(func=handle_add)`는 각 서브커맨드에 핸들러 함수를 연결하는 패턴입니다. 나중에 `args.func(args)`로 호출하면 해당 명령어의 함수가 자동으로 실행됩니다.

---

## 25.5 Step 2: 데이터 모델과 할일 추가/목록

CLI 뼈대가 동작하는 것을 확인했으니, 이제 **실제 데이터를 다루는 코드**를 만들 차례입니다.

### 프롬프트 3: 데이터 모델

```
할일(Todo) 데이터를 표현하는 Python dataclass를 만들어줘.
필요한 필드:
- id: 고유 번호 (int)
- title: 제목 (str)
- priority: 우선순위 (Enum - low/medium/high)
- completed: 완료 여부 (bool)
- created_at: 생성 일시 (ISO 형식 문자열)
- completed_at: 완료 일시 (None 가능)
- due_date: 마감일 (None 가능)
- tags: 태그 목록 (list[str])

메서드도 추가해줘:
- mark_complete(): 완료 처리
- is_overdue(): 마감일 초과 확인
- to_dict() / from_dict(): JSON 변환용
- summary(): 한 줄 요약 문자열
```

**예제 25-03: Todo 데이터 클래스**

```python
# examples/python/chapter06/ex25_03_todo_dataclass.py
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum


class Priority(Enum):
    """할일 우선순위"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def to_korean(self) -> str:
        """우선순위를 한국어로 변환합니다."""
        labels = {
            Priority.LOW: "낮음",
            Priority.MEDIUM: "보통",
            Priority.HIGH: "높음",
        }
        return labels[self]

    def to_symbol(self) -> str:
        """우선순위를 기호로 변환합니다."""
        symbols = {
            Priority.LOW: "!",
            Priority.MEDIUM: "!!",
            Priority.HIGH: "!!!",
        }
        return symbols[self]


@dataclass
class Todo:
    """할일 데이터 클래스"""
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str | None = None
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    def mark_complete(self) -> None:
        """할일을 완료 상태로 변경합니다."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def is_overdue(self) -> bool:
        """마감일이 지났는지 확인합니다."""
        if not self.due_date:
            return False
        due = datetime.fromisoformat(self.due_date)
        return not self.completed and datetime.now() > due

    def to_dict(self) -> dict:
        """딕셔너리로 변환합니다 (JSON 저장용)."""
        data = asdict(self)
        data["priority"] = self.priority.value  # Enum을 문자열로
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """딕셔너리에서 Todo 객체를 생성합니다 (JSON 로드용)."""
        data["priority"] = Priority(data["priority"])
        return cls(**data)

    def summary(self) -> str:
        """할일 요약 문자열을 반환합니다."""
        status = "[완료]" if self.completed else "[미완료]"
        priority_str = self.priority.to_symbol()
        parts = [f"#{self.id}", status, priority_str, self.title]
        if self.due_date:
            overdue = " (기한 초과!)" if self.is_overdue() else ""
            parts.append(f"(마감: {self.due_date}{overdue})")
        if self.tags:
            tag_str = " ".join(f"#{tag}" for tag in self.tags)
            parts.append(f"[{tag_str}]")
        return " ".join(parts)
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_03_todo_dataclass.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - Todo 데이터 클래스 데모
=======================================================

--- 1. 기본 할일 생성 ---
할일 1: #1 [미완료] !! 우유 사기
  우선순위: 보통
  완료 여부: False

--- 2. 상세 할일 생성 ---
할일 2: #2 [미완료] !!! 보고서 작성 (마감: 2025-12-20) [#업무 #급함]
  기한 초과: False

--- 4. 할일 완료 처리 ---
완료 전: #1 [미완료] !! 우유 사기
완료 후: #1 [완료] !! 우유 사기
  완료 시각: 2025-12-19T14:30:00.123456

--- 5. 딕셔너리 변환 ---
딕셔너리: {'id': 2, 'title': '보고서 작성', 'priority': 'high', ...}

--- 6. 딕셔너리에서 복원 ---
복원된 할일: #2 [미완료] !!! 보고서 작성 (마감: 2025-12-20) [#업무 #급함]
  원본과 동일: True
```

### 데이터 모델 설계의 핵심

`Todo` 클래스에서 주목해야 할 설계 결정들이 있습니다:

**1. `@dataclass` 사용 이유:**
```python
# 일반 클래스로 작성하면 __init__, __repr__ 등을 직접 구현해야 함
# dataclass는 이를 자동으로 생성해줌
@dataclass
class Todo:
    id: int
    title: str
    # ... 필드 선언만으로 충분!
```

**2. `Enum`으로 우선순위 관리:**
```python
# 문자열 대신 Enum을 사용하면 오타를 방지할 수 있음
Priority.HIGH    # OK
Priority("high") # OK
Priority("hihg") # ValueError 발생 - 오타 즉시 발견!
```

**3. `to_dict()` / `from_dict()` 패턴:**
```python
# 저장할 때: Todo 객체 -> 딕셔너리 -> JSON
todo_dict = todo.to_dict()
json.dumps(todo_dict)

# 불러올 때: JSON -> 딕셔너리 -> Todo 객체
data = json.loads(json_string)
todo = Todo.from_dict(data)
```

> **Warning:** `dataclass`의 `field(default_factory=...)`를 사용하는 이유에 주의하세요. `tags: list[str] = []`로 작성하면 모든 인스턴스가 같은 리스트를 공유하는 버그가 발생합니다. `field(default_factory=list)`를 사용해야 각 인스턴스마다 독립된 리스트가 생성됩니다.

### 프롬프트 4: add 명령어

```
TodoManager 클래스를 만들어줘.
add 메서드를 구현하고, 다음을 포함해줘:
- 제목이 비어있으면 에러 발생
- 마감일 형식(YYYY-MM-DD) 검증
- 우선순위 문자열을 Enum으로 변환
- 자동 ID 부여
argparse 파서도 함께 만들어줘.
```

**예제 25-04: add 명령어 구현**

```python
# examples/python/chapter06/ex25_04_add_command.py
class TodoManager:
    """할일 관리자 - 할일 추가 기능에 집중"""

    def __init__(self) -> None:
        self.todos: list[Todo] = []
        self._next_id: int = 1

    def add(
        self,
        title: str,
        priority: str = "medium",
        due_date: str | None = None,
        tags: list[str] | None = None,
    ) -> Todo:
        """새로운 할일을 추가합니다."""

        # 제목 유효성 검사
        title = title.strip()
        if not title:
            raise ValueError("할일 제목은 비어 있을 수 없습니다.")

        # 마감일 유효성 검사
        if due_date:
            try:
                parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
                if parsed_date.date() < datetime.now().date():
                    print(f"  주의: 마감일({due_date})이 과거 날짜입니다.")
            except ValueError:
                raise ValueError(
                    f"잘못된 날짜 형식: '{due_date}' (YYYY-MM-DD 형식 필요)"
                )

        # 우선순위 변환
        try:
            priority_enum = Priority(priority)
        except ValueError:
            raise ValueError(
                f"잘못된 우선순위: '{priority}' (low/medium/high 중 선택)"
            )

        # 할일 객체 생성
        todo = Todo(
            id=self._next_id,
            title=title,
            priority=priority_enum,
            due_date=due_date,
            tags=tags or [],
        )

        self.todos.append(todo)
        self._next_id += 1
        return todo
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_04_add_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - add 명령어 데모
=======================================================

--- 기본 추가 ---
>>> todo add 우유 사기
  추가 완료: #1 [미완료] !! 우유 사기

--- 높은 우선순위로 추가 ---
>>> todo add 보고서 작성 --priority high
  추가 완료: #2 [미완료] !!! 보고서 작성

--- 마감일 포함 추가 ---
>>> todo add 프레젠테이션 준비 -p high -d 2025-12-31
  추가 완료: #3 [미완료] !!! 프레젠테이션 준비 (마감: 2025-12-31)

--- 태그 포함 추가 ---
>>> todo add 운동하기 -t 건강 루틴
  추가 완료: #4 [미완료] !! 운동하기 [#건강 #루틴]

--- 현재 할일 목록 ---
  #1 [미완료] !! 우유 사기
  #2 [미완료] !!! 보고서 작성
  #3 [미완료] !!! 프레젠테이션 준비 (마감: 2025-12-31)
  #4 [미완료] !! 운동하기 [#건강 #루틴]

총 4개의 할일이 등록되었습니다.
```

### 프롬프트 5: list 명령어 (시각적 출력)

```
할일 목록을 예쁘게 출력하는 기능을 만들어줘.
ANSI 색상 코드를 사용해서:
- 우선순위별 다른 색상 (높음=빨강, 보통=노랑, 낮음=파랑)
- 완료된 항목은 취소선 + 흐리게
- 마감일 D-day 표시
- 진행률 바 표시
--all 옵션이 있으면 완료 항목도 표시해줘.
```

**예제 25-05: list 명령어 구현**

```python
# examples/python/chapter06/ex25_05_list_command.py

# ANSI 색상 코드
class Color:
    """터미널 ANSI 색상 코드"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    STRIKETHROUGH = "\033[9m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"


def format_todo_line(todo: Todo, use_color: bool = True) -> str:
    """할일 한 줄을 포맷팅합니다."""
    # 체크박스
    if todo.completed:
        checkbox = Color.colorize("[x]", Color.GREEN) if use_color else "[x]"
    else:
        checkbox = "[ ]"

    # 우선순위 라벨 (색상별 구분)
    priority_map = {
        Priority.HIGH: ("높음", Color.RED, Color.BOLD),
        Priority.MEDIUM: ("보통", Color.YELLOW,),
        Priority.LOW: ("낮음", Color.BLUE,),
    }
    label, *colors = priority_map[todo.priority]
    priority_str = Color.colorize(f"[{label}]", *colors) if use_color else f"[{label}]"

    # 마감일 D-day 계산
    due_str = ""
    if todo.due_date and not todo.completed:
        due = datetime.strptime(todo.due_date, "%Y-%m-%d")
        days_left = (due.date() - datetime.now().date()).days
        if days_left < 0:
            due_str = f"(기한 초과 {abs(days_left)}일!)"
        elif days_left == 0:
            due_str = "(오늘 마감!)"
        elif days_left <= 3:
            due_str = f"(D-{days_left})"

    parts = [checkbox, f"#{todo.id:>3}", priority_str, todo.title]
    if due_str:
        parts.append(due_str)
    return " ".join(parts)


def display_todo_list(todos: list[Todo], show_completed: bool = False) -> None:
    """할일 목록을 표시합니다."""
    filtered = todos if show_completed else [t for t in todos if not t.completed]

    # 통계 헤더
    total = len(todos)
    done = sum(1 for t in todos if t.completed)
    print(f"  할일 목록 | 전체: {total} | 완료: {done} | 미완료: {total - done}")
    print(f"  {'─' * 50}")

    # 정렬: 미완료 먼저, 우선순위 높은 것 먼저
    priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
    sorted_todos = sorted(
        filtered,
        key=lambda t: (t.completed, priority_order[t.priority], t.id),
    )

    for todo in sorted_todos:
        print(f"  {format_todo_line(todo)}")
    print(f"  {'─' * 50}")

    # 진행률 바
    if total > 0:
        progress = done / total
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"  진행률: [{bar}] {progress:.0%}")
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_05_list_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - list 명령어 데모
=======================================================

--- 1. 미완료 할일만 표시 (색상 출력) ---
  할일 목록 | 전체: 7 | 완료: 2 | 미완료: 5
  ──────────────────────────────────────────────────
  [ ] #  4 [높음] 이메일 답장 (기한 초과 1일!)
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!)
  [ ] #  2 [높음] 보고서 작성 (D-1)
  [ ] #  3 [보통] 운동하기
  [ ] #  5 [낮음] 책 읽기
  ──────────────────────────────────────────────────
  진행률: [█████░░░░░░░░░░░░░░░] 29%
```

이 출력에서 주목할 점:

1. **우선순위별 정렬**: 높음 -> 보통 -> 낮음 순으로 정렬됩니다
2. **마감일 표시**: "기한 초과", "오늘 마감!", "D-1" 등 상황에 맞는 표시
3. **진행률 바**: 전체 대비 완료 비율을 시각적으로 보여줍니다
4. **ANSI 색상**: 터미널에서 실제로 실행하면 색상이 적용됩니다

> **Tip:** ANSI 색상 코드(`\033[31m` 등)는 대부분의 현대 터미널에서 지원합니다. Windows의 명령 프롬프트(cmd)에서는 동작하지 않을 수 있지만, Windows Terminal이나 PowerShell에서는 잘 동작합니다.

---

## 25.6 Step 3: 완료와 삭제 기능

데이터 모델과 추가/목록 기능이 동작하므로, 이제 **상태를 변경하는 기능**을 구현합니다.

### 프롬프트 6: complete 명령어

```
할일 완료 처리 기능을 구현해줘.
TodoManager에 다음 메서드를 추가해줘:
- complete(todo_id): 단일 할일 완료
- complete_multiple(todo_ids): 여러 할일 동시 완료
- uncomplete(todo_id): 완료 취소
각 메서드는 (성공여부, 메시지) 튜플을 반환해줘.
이미 완료된 할일이나 존재하지 않는 ID에 대한 에러 처리도 포함해줘.
```

**예제 25-06: complete 명령어 구현**

```python
# examples/python/chapter06/ex25_06_complete_command.py
class TodoManager:
    """할일 관리자 - 완료 기능에 집중"""

    def find_by_id(self, todo_id: int) -> Todo | None:
        """ID로 할일을 찾습니다."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def complete(self, todo_id: int) -> tuple[bool, str]:
        """할일을 완료 처리합니다."""
        todo = self.find_by_id(todo_id)

        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        if todo.completed:
            return False, f"알림: #{todo_id} '{todo.title}'은(는) 이미 완료 상태입니다."

        todo.completed = True
        todo.completed_at = datetime.now().isoformat()
        return True, f"완료: #{todo_id} '{todo.title}'을(를) 완료 처리했습니다."

    def complete_multiple(self, todo_ids: list[int]) -> list[tuple[int, bool, str]]:
        """여러 할일을 한 번에 완료 처리합니다."""
        results = []
        for todo_id in todo_ids:
            success, message = self.complete(todo_id)
            results.append((todo_id, success, message))
        return results

    def uncomplete(self, todo_id: int) -> tuple[bool, str]:
        """할일 완료를 취소합니다."""
        todo = self.find_by_id(todo_id)

        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        if not todo.completed:
            return False, f"알림: #{todo_id} '{todo.title}'은(는) 이미 미완료 상태입니다."

        todo.completed = False
        todo.completed_at = None
        return True, f"되돌림: #{todo_id} '{todo.title}'을(를) 미완료로 변경했습니다."
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_06_complete_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - complete 명령어 데모
=======================================================

--- 초기 할일 목록 ---
  #1 [미완료] 우유 사기
  #2 [미완료] 보고서 작성
  #3 [미완료] 운동하기
  #4 [미완료] 이메일 답장
  #5 [미완료] 책 읽기

--- 1. 단일 할일 완료 ---
>>> todo complete 1
  완료: #1 '우유 사기'을(를) 완료 처리했습니다.

--- 2. 이미 완료된 할일 재완료 시도 ---
>>> todo complete 1
  알림: #1 '우유 사기'은(는) 이미 완료 상태입니다.

--- 3. 존재하지 않는 할일 완료 시도 ---
>>> todo complete 99
  오류: #99 할일을 찾을 수 없습니다.

--- 4. 여러 할일 동시 완료 ---
>>> todo complete 2 3 4
  [성공] 완료: #2 '보고서 작성'을(를) 완료 처리했습니다.
  [성공] 완료: #3 '운동하기'을(를) 완료 처리했습니다.
  [성공] 완료: #4 '이메일 답장'을(를) 완료 처리했습니다.

--- 5. 완료 취소 ---
>>> todo uncomplete 3
  되돌림: #3 '운동하기'을(를) 미완료로 변경했습니다.

--- 통계 ---
  전체: 5
  완료: 3
  미완료: 2
  완료율: 60.0%
```

### 에러 처리 패턴

`complete` 메서드의 **반환 값 패턴**에 주목하세요:

```python
def complete(self, todo_id: int) -> tuple[bool, str]:
    # 실패 케이스 1: 존재하지 않음
    if todo is None:
        return False, "오류: ..."

    # 실패 케이스 2: 이미 완료됨
    if todo.completed:
        return False, "알림: ..."

    # 성공 케이스
    return True, "완료: ..."
```

이 패턴은 `(성공 여부, 메시지)` 튜플을 반환하여 호출자가 결과를 쉽게 처리할 수 있게 합니다. 예외(Exception)를 던지는 대신 이 방식을 사용하면 **여러 작업을 연속으로 처리**할 때 하나의 실패가 전체를 중단시키지 않습니다.

### 프롬프트 7: delete 명령어

```
할일 삭제 기능을 구현해줘.
다음 기능이 필요해:
- 완료된 할일은 바로 삭제 가능
- 미완료 할일은 --force 옵션이 있어야 삭제 가능
- 완료 항목 일괄 삭제 (delete --done)
- 삭제 되돌리기 (undo) 기능
- 삭제 히스토리 관리
```

**예제 25-07: delete 명령어 구현**

```python
# examples/python/chapter06/ex25_07_delete_command.py
class TodoManager:
    """할일 관리자 - 삭제 기능에 집중"""

    def __init__(self) -> None:
        self.todos: list[Todo] = []
        self._deleted_history: list[Todo] = []  # 삭제 히스토리

    def delete(self, todo_id: int, force: bool = False) -> tuple[bool, str]:
        """할일을 삭제합니다."""
        todo = self.find_by_id(todo_id)

        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        # 미완료 할일 삭제 시 경고 (force가 아닌 경우)
        if not todo.completed and not force:
            return False, (
                f"경고: #{todo_id} '{todo.title}'은(는) 아직 미완료 상태입니다. "
                f"삭제하려면 --force 옵션을 사용하세요."
            )

        self.todos.remove(todo)
        self._deleted_history.append(todo)
        return True, f"삭제: #{todo_id} '{todo.title}'을(를) 삭제했습니다."

    def delete_completed(self) -> tuple[int, list[str]]:
        """완료된 할일을 일괄 삭제합니다."""
        completed_todos = [t for t in self.todos if t.completed]
        if not completed_todos:
            return 0, ["완료된 할일이 없습니다."]

        messages = []
        for todo in completed_todos:
            self.todos.remove(todo)
            self._deleted_history.append(todo)
            messages.append(f"  삭제: #{todo.id} '{todo.title}'")
        return len(completed_todos), messages

    def undo_last_delete(self) -> tuple[bool, str]:
        """마지막 삭제를 되돌립니다."""
        if not self._deleted_history:
            return False, "되돌릴 삭제 항목이 없습니다."

        todo = self._deleted_history.pop()
        self.todos.append(todo)
        self.todos.sort(key=lambda t: t.id)  # ID 순 재정렬
        return True, f"복원: #{todo.id} '{todo.title}'을(를) 복원했습니다."
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_07_delete_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - delete 명령어 데모
=======================================================

--- 1. 완료된 할일 삭제 ---
>>> todo delete 1
  삭제: #1 '우유 사기'을(를) 삭제했습니다.

--- 2. 미완료 할일 삭제 시도 (force 없음) ---
>>> todo delete 2
  경고: #2 '보고서 작성'은(는) 아직 미완료 상태입니다. 삭제하려면 --force 옵션을 사용하세요.

--- 3. 미완료 할일 강제 삭제 ---
>>> todo delete 2 --force
  삭제: #2 '보고서 작성'을(를) 삭제했습니다.

--- 5. 마지막 삭제 되돌리기 ---
>>> todo undo
  복원: #2 '보고서 작성'을(를) 복원했습니다.

--- 7. 완료 항목 일괄 삭제 ---
>>> todo delete --done
  삭제: #3 '운동하기'
  삭제: #6 '빨래 개기'
  총 2개 항목 삭제 완료
```

### 안전 장치 설계

`delete` 명령어에는 데이터 손실을 방지하기 위한 안전 장치가 여러 겹으로 설계되어 있습니다:

```
삭제 요청
    ↓
미완료 상태인가? ──YES──→ --force 옵션 필요 (안전 장치 1)
    ↓ NO
삭제 실행
    ↓
히스토리에 보관 ──────→ undo로 복원 가능 (안전 장치 2)
```

> **Tip:** 삭제 기능을 구현할 때는 항상 "실수로 삭제했을 때 복구할 수 있는가?"를 고려하세요. `_deleted_history`처럼 삭제 히스토리를 보관하는 것은 간단하지만 효과적인 안전 장치입니다.

---

## 25.7 Step 4: 파일 저장과 로드

지금까지의 코드는 프로그램을 종료하면 모든 데이터가 사라집니다. 이제 **JSON 파일로 데이터를 영구 저장**하는 기능을 추가합니다.

### 프롬프트 8: JSON 저장

```
할일 데이터를 JSON 파일로 저장하는 TodoStorage 클래스를 만들어줘.
요구사항:
- 한글이 깨지지 않도록 ensure_ascii=False 사용
- 사람이 읽을 수 있도록 indent=2 적용
- 메타데이터(저장 시각, 버전, 통계)도 함께 저장
- 디렉토리가 없으면 자동 생성
- 백업 파일 생성 기능
```

**예제 25-08: JSON 저장 기능**

```python
# examples/python/chapter06/ex25_08_json_save.py
import json
import os
from datetime import datetime


class TodoStorage:
    """할일 데이터를 JSON 파일로 저장하는 클래스"""

    FORMAT_VERSION = "1.0"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save(self, todos: list[Todo]) -> dict:
        """할일 목록을 JSON 파일로 저장합니다."""

        # 저장할 데이터 구성
        data = {
            "metadata": {
                "version": self.FORMAT_VERSION,
                "saved_at": datetime.now().isoformat(),
                "total_count": len(todos),
                "completed_count": sum(1 for t in todos if t.completed),
                "app": "CLI 할일 관리 앱",
            },
            "todos": [todo.to_dict() for todo in todos],
        }

        # 디렉토리 생성 (없으면)
        dir_path = os.path.dirname(self.file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # JSON 파일로 저장
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 저장 결과 정보 반환
        file_size = os.path.getsize(self.file_path)
        return {
            "file_path": self.file_path,
            "file_size": file_size,
            "todo_count": len(todos),
            "saved_at": data["metadata"]["saved_at"],
        }
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_08_json_save.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - JSON 저장 기능 데모
=======================================================

--- 저장할 할일 목록 ---
  #1 [완료] 우유 사기
  #2 [미완료] 보고서 작성
  #3 [미완료] 운동하기

--- 1. JSON 파일로 저장 ---
  저장 경로: /tmp/todo-cli-data/todos.json
  파일 크기: 1.2 KB
  저장 항목: 5개
  저장 시각: 2025-12-19T14:30:00.123456

--- 2. 저장된 JSON 내용 ---
{
  "metadata": {
    "version": "1.0",
    "saved_at": "2025-12-19T14:30:00.123456",
    "total_count": 5,
    "completed_count": 1,
    "app": "CLI 할일 관리 앱"
  },
  "todos": [
    {
      "id": 1,
      "title": "우유 사기",
      "priority": "low",
      "completed": true,
      "created_at": "2025-12-19T14:30:00.123456",
      "completed_at": "2025-12-19T14:30:00.123456",
      "due_date": null,
      "tags": ["장보기"]
    },
    ...
  ]
}
```

### JSON 저장 시 핵심 설정

```python
json.dump(data, f, ensure_ascii=False, indent=2)
```

이 한 줄에 세 가지 중요한 설정이 담겨 있습니다:

| 설정 | 값 | 역할 |
|------|-----|------|
| `ensure_ascii` | `False` | 한글을 `\uC6B0\uC720`가 아닌 `"우유"`로 저장 |
| `indent` | `2` | 들여쓰기 적용 (사람이 읽기 쉽게) |
| `encoding` | `"utf-8"` | 파일을 UTF-8로 저장 (한글 깨짐 방지) |

> **Warning:** `ensure_ascii=False`를 빠뜨리면 한글이 유니코드 이스케이프 시퀀스(`\uXXXX`)로 저장됩니다. 기능상 문제는 없지만, JSON 파일을 직접 열어볼 때 읽기 어렵습니다.

### 프롬프트 9: JSON 로드

```
JSON 파일에서 할일을 불러오는 load 메서드를 구현해줘.
다음 에러 상황을 처리해줘:
- 파일이 없는 경우
- 파일이 손상된 경우 (잘못된 JSON)
- 일부 항목이 잘못된 경우 (나머지는 복구)
- 버전 호환성 검사
왕복 테스트(save -> load)도 포함해줘.
```

**예제 25-09: JSON 로드 기능**

```python
# examples/python/chapter06/ex25_09_json_load.py

class LoadError:
    """로드 에러 정보를 담는 클래스"""
    def __init__(self, error_type: str, message: str) -> None:
        self.error_type = error_type
        self.message = message


class TodoStorage:
    """할일 데이터를 JSON 파일에서 불러오는 클래스"""

    SUPPORTED_VERSIONS = ["1.0"]

    def load(self) -> tuple[list[Todo], list[LoadError]]:
        """JSON 파일에서 할일 목록을 불러옵니다."""
        errors: list[LoadError] = []
        todos: list[Todo] = []

        # 1. 파일 존재 여부 확인
        if not os.path.exists(self.file_path):
            errors.append(LoadError("FILE_NOT_FOUND",
                f"파일을 찾을 수 없습니다: {self.file_path}"))
            return todos, errors

        # 2. 파일 읽기
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
        except PermissionError:
            errors.append(LoadError("PERMISSION_ERROR",
                f"파일 읽기 권한이 없습니다: {self.file_path}"))
            return todos, errors

        # 3. JSON 파싱
        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            errors.append(LoadError("JSON_PARSE_ERROR",
                f"JSON 파싱 실패 (줄 {e.lineno}, 열 {e.colno}): {e.msg}"))
            return todos, errors

        # 4. 버전 검사
        metadata = data.get("metadata", {})
        version = metadata.get("version", "unknown")
        if version not in self.SUPPORTED_VERSIONS:
            errors.append(LoadError("VERSION_MISMATCH",
                f"지원하지 않는 버전: {version}"))

        # 5. 각 할일 항목 변환 (에러 발생 시 건너뛰고 계속)
        for i, item in enumerate(data.get("todos", [])):
            try:
                if not isinstance(item, dict):
                    errors.append(LoadError("INVALID_ITEM",
                        f"항목 {i+1}: 딕셔너리가 아닙니다 (건너뜀)"))
                    continue
                if "id" not in item or "title" not in item:
                    errors.append(LoadError("MISSING_FIELD",
                        f"항목 {i+1}: 필수 필드 누락 (건너뜀)"))
                    continue
                todos.append(Todo.from_dict(item))
            except (ValueError, TypeError) as e:
                errors.append(LoadError("CONVERSION_ERROR",
                    f"항목 {i+1}: 변환 실패 - {e} (건너뜀)"))

        return todos, errors
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_09_json_load.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - JSON 로드 기능 데모
=======================================================

--- 1. 정상 JSON 파일 로드 ---
  메타데이터:
    버전: 1.0
    저장 시각: 2025-12-19T14:30:00.123456
    전체 항목: 3개
  로드 결과: 3개 할일, 0개 에러

--- 2. 존재하지 않는 파일 로드 ---
  로드 결과: 0개 할일, 1개 에러
    [FILE_NOT_FOUND] 파일을 찾을 수 없습니다: ...

--- 3. 손상된 JSON 파일 로드 ---
  로드 결과: 0개 할일, 1개 에러
    [JSON_PARSE_ERROR] JSON 파싱 실패 (줄 1, 열 51): ...

--- 4. 부분 손상 파일 로드 (최대한 복구) ---
  로드 결과: 2개 할일 복구, 2개 에러
  복구된 할일:
    #1 [미완료] 정상 항목
    #4 [미완료] 복구된 항목
  발생한 에러:
    [MISSING_FIELD] 항목 2: 필수 필드(id, title) 누락 (건너뜀)
    [INVALID_ITEM] 항목 3: 딕셔너리가 아닙니다 (건너뜀)

--- 5. 저장 후 로드 왕복 테스트 ---
  원본 항목 수: 2
  로드 항목 수: 2
  데이터 일치: 예
```

### "최대한 복구" 전략

로드 기능에서 가장 중요한 설계 결정은 **부분 에러가 발생해도 전체를 포기하지 않는 것**입니다:

```
JSON 파일 (4개 항목)
├── 항목 1: 정상      → 로드 성공
├── 항목 2: 필드 누락  → 건너뜀 + 에러 기록
├── 항목 3: 형식 오류  → 건너뜀 + 에러 기록
└── 항목 4: 정상      → 로드 성공

결과: 2개 복구, 2개 에러 → 데이터 최대한 보존!
```

이 접근법은 실전에서 매우 중요합니다. 사용자의 데이터는 **가능한 한 많이 보존**하는 것이 최선의 전략입니다.

> **Note:** 왕복 테스트(Round-trip test)는 "저장 -> 로드 -> 원본과 비교"하여 데이터 무결성을 검증하는 방법입니다. 직렬화(Serialization) 코드를 작성할 때 반드시 수행해야 합니다.

---

## 25.8 Step 5: 검색과 필터

기본 CRUD와 데이터 저장이 완성되었습니다. 이제 할일이 많아졌을 때 **원하는 항목을 빠르게 찾는** 기능을 추가합니다.

### 프롬프트 10: 검색 기능

```
키워드로 할일을 검색하는 기능을 구현해줘.
요구사항:
- 제목과 태그에서 검색
- 대소문자 구분 없이 검색
- 검색 키워드를 결과에서 하이라이트 표시
- 어디서 매칭되었는지 표시 (제목 vs 태그)
- 미완료만 검색하는 옵션
```

**예제 25-10: search 명령어 구현**

```python
# examples/python/chapter06/ex25_10_search_command.py

def highlight_text(text: str, keyword: str, use_color: bool = True) -> str:
    """텍스트에서 키워드를 하이라이트합니다."""
    if not keyword:
        return text

    text_lower = text.lower()
    keyword_lower = keyword.lower()

    if keyword_lower not in text_lower:
        return text

    result = []
    pos = 0

    while pos < len(text):
        idx = text_lower.find(keyword_lower, pos)
        if idx == -1:
            result.append(text[pos:])
            break
        result.append(text[pos:idx])
        matched = text[idx:idx + len(keyword)]
        if use_color:
            result.append(f"\033[43m\033[30m\033[1m{matched}\033[0m")
        else:
            result.append(f"[{matched}]")
        pos = idx + len(keyword)

    return "".join(result)


def search_todos(
    todos: list[Todo],
    keyword: str,
    search_in_tags: bool = True,
    include_completed: bool = True,
) -> list[tuple[Todo, list[str]]]:
    """할일을 키워드로 검색합니다."""
    keyword_lower = keyword.lower().strip()
    results = []

    for todo in todos:
        if not include_completed and todo.completed:
            continue

        matched_fields = []

        # 제목 검색
        if keyword_lower in todo.title.lower():
            matched_fields.append("제목")

        # 태그 검색
        if search_in_tags and todo.tags:
            for tag in todo.tags:
                if keyword_lower in tag.lower():
                    matched_fields.append(f"태그({tag})")
                    break

        if matched_fields:
            results.append((todo, matched_fields))

    return results
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_10_search_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - search 명령어 데모
=======================================================

--- 1. 제목에서 '작성' 검색 ---
>>> todo search 작성
  '작성' 검색 결과: 2개
  ──────────────────────────────────────────────────
  #2 [미완료] 보고서 [작성]하기 (제목)
  #6 [미완료] 팀 회의 자료 [작성] (제목)
  ──────────────────────────────────────────────────

--- 2. 태그에서 '업무' 검색 ---
>>> todo search 업무
  '업무' 검색 결과: 4개
  ──────────────────────────────────────────────────
  #2 [미완료] 보고서 작성하기 #업무 #급함 (태그(업무))
  #4 [미완료] 이메일 답장 보내기 #업무 #이메일 (태그(업무))
  #6 [미완료] 팀 회의 자료 작성 #업무 #회의 (태그(업무))
  #8 [완료] 파이썬 프로젝트 코드 리뷰 #업무 #파이썬 (태그(업무))
  ──────────────────────────────────────────────────

--- 3. '파이썬' 검색 (제목+태그) ---
>>> todo search 파이썬
  '파이썬' 검색 결과: 2개
  ──────────────────────────────────────────────────
  #5 [미완료] 책 읽기 - [파이썬] 기초 #공부 #파이썬 (제목, 태그(파이썬))
  #8 [완료] [파이썬] 프로젝트 코드 리뷰 #업무 #파이썬 (제목, 태그(파이썬))
  ──────────────────────────────────────────────────

--- 5. '파이썬' 검색 (미완료만) ---
>>> todo search 파이썬 --pending
  '파이썬' 검색 결과: 1개
  ──────────────────────────────────────────────────
  #5 [미완료] 책 읽기 - [파이썬] 기초 #공부 #파이썬 (제목, 태그(파이썬))
  ──────────────────────────────────────────────────

--- 6. 검색 결과 없음 ---
>>> todo search 여행
  '여행'에 대한 검색 결과가 없습니다.
```

검색 결과에서 `[파이썬]`처럼 대괄호로 감싸진 부분은 실제 터미널에서는 **노란색 배경으로 하이라이트**됩니다.

### 프롬프트 11: 필터 기능

```
할일 필터링 기능을 만들어줘.
메서드 체이닝 패턴으로 여러 필터를 조합할 수 있게 해줘:
- by_status(completed): 완료/미완료
- by_priority(priority): 우선순위
- by_tag(tag): 태그
- by_overdue(): 기한 초과
- by_due_within_days(days): N일 이내 마감
apply() 메서드로 모든 필터를 적용하고, 정렬 옵션도 지원해줘.
```

**예제 25-11: filter 명령어 구현**

```python
# examples/python/chapter06/ex25_11_filter_command.py

class TodoFilter:
    """할일 필터링 엔진"""

    def __init__(self, todos: list[Todo]) -> None:
        self._todos = todos
        self._filters: list[tuple[str, callable]] = []

    def by_status(self, completed: bool) -> "TodoFilter":
        """완료/미완료 상태로 필터링합니다."""
        label = "완료" if completed else "미완료"
        self._filters.append(
            (f"상태={label}", lambda t: t.completed == completed)
        )
        return self  # 메서드 체이닝 가능!

    def by_priority(self, priority: Priority) -> "TodoFilter":
        """우선순위로 필터링합니다."""
        self._filters.append(
            (f"우선순위={priority.to_korean()}",
             lambda t: t.priority == priority)
        )
        return self

    def by_tag(self, tag: str) -> "TodoFilter":
        """태그로 필터링합니다."""
        tag_lower = tag.lower()
        self._filters.append(
            (f"태그={tag}",
             lambda t: any(tg.lower() == tag_lower for tg in t.tags))
        )
        return self

    def by_overdue(self) -> "TodoFilter":
        """기한이 지난 할일만 필터링합니다."""
        self._filters.append(("기한초과", lambda t: t.is_overdue()))
        return self

    def apply(self, sort_by: str = "priority") -> list[Todo]:
        """모든 필터를 적용하고 결과를 반환합니다."""
        result = self._todos
        for name, filter_func in self._filters:
            result = [t for t in result if filter_func(t)]

        # 정렬
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        if sort_by == "priority":
            result.sort(key=lambda t: (priority_order[t.priority], t.id))
        elif sort_by == "due_date":
            result.sort(key=lambda t: (t.due_date or "9999-99-99", t.id))
        return result

    def get_filter_description(self) -> str:
        """적용된 필터 설명을 반환합니다."""
        if not self._filters:
            return "필터 없음 (전체)"
        return " + ".join(name for name, _ in self._filters)
```

**실행:**
```bash
$ python examples/python/chapter06/ex25_11_filter_command.py
```

**결과:**
```
=======================================================
CLI 할일 관리 앱 - filter 명령어 데모
=======================================================

--- 1. 미완료 할일 필터 ---
>>> todo filter --status pending
  필터: 상태=미완료
  결과: 8개 / 전체 10개
  ──────────────────────────────────────────────────
  #2 [미완료] !!! 보고서 작성 (마감: 2025-12-20) [#업무 #급함]
  #4 [미완료] !!! 이메일 답장 (마감: 2025-12-18) [#업무]
  #6 [미완료] !!! 팀 회의 준비 (마감: 2025-12-19) [#업무 #회의]
  ...
  ──────────────────────────────────────────────────

--- 6. 복합 필터: 미완료 + 높은 우선순위 ---
>>> todo filter --status pending --priority high
  필터: 상태=미완료 + 우선순위=높음
  결과: 4개 / 전체 10개
  ──────────────────────────────────────────────────
  #2 [미완료] !!! 보고서 작성 (마감: 2025-12-20) [#업무 #급함]
  #4 [미완료] !!! 이메일 답장 (마감: 2025-12-18) [#업무]
  #6 [미완료] !!! 팀 회의 준비 (마감: 2025-12-19) [#업무 #회의]
  #9 [미완료] !!! 코드 리뷰 (마감: 2025-12-20) [#업무 #개발]
  ──────────────────────────────────────────────────

--- 7. 복합 필터: 업무 태그 + 마감일 있음 ---
>>> todo filter --tag 업무 --has-due
  필터: 태그=업무 + 마감일=있음
  결과: 3개 / 전체 10개
```

### 메서드 체이닝 패턴

`TodoFilter` 클래스의 핵심은 **메서드 체이닝(Method Chaining)** 패턴입니다:

```python
# 각 필터 메서드가 self를 반환하므로 연쇄 호출 가능
result = (
    TodoFilter(todos)
    .by_status(completed=False)    # 미완료만
    .by_priority(Priority.HIGH)     # 높은 우선순위만
    .by_tag("업무")                 # '업무' 태그만
    .apply(sort_by="due_date")      # 마감일순 정렬
)
```

이 패턴은 SQL의 `WHERE` 절을 조합하는 것과 비슷합니다:

```sql
-- SQL로 표현하면:
SELECT * FROM todos
WHERE completed = false
  AND priority = 'high'
  AND '업무' IN (tags)
ORDER BY due_date;
```

> **Tip:** 메서드 체이닝은 코드를 읽기 쉽게 만들어줍니다. "미완료 + 높은 우선순위 + 업무 태그" 같은 복합 조건을 한 눈에 파악할 수 있습니다.

---

## 25.9 완성 및 테스트

모든 개별 기능이 동작하는 것을 확인했으니, 이제 **하나의 완성된 앱으로 통합**합니다.

### 프롬프트 12: 전체 통합

```
지금까지 만든 모든 기능을 하나의 완성된 CLI 앱으로 통합해줘.
파일 하나에 모든 코드를 넣어줘:
- Color: 색상 유틸리티
- Priority, Todo: 데이터 모델
- TodoStorage: JSON 저장/로드
- TodoManager: CRUD + 검색 + 필터 + 통계
- CLI 핸들러 함수들
- argparse 파서
- main() 진입점

실제 CLI로 사용할 수 있게 해줘:
  python todo.py add "할일" --priority high
  python todo.py list --all
  python todo.py complete 1 2 3
  python todo.py delete 1 --force
  python todo.py search "키워드"
  python todo.py filter --status pending --priority high
  python todo.py stats
```

**예제 25-12: 전체 통합 앱**

```python
# examples/python/chapter06/ex25_12_full_todo_app.py

# ============================================================
# 색상 유틸리티
# ============================================================

class Color:
    """터미널 ANSI 색상 코드"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    STRIKETHROUGH = "\033[9m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"

    @staticmethod
    def c(text: str, *codes: str) -> str:
        return f"{''.join(codes)}{text}{Color.RESET}"


# ============================================================
# 데이터 모델
# ============================================================

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def to_korean(self) -> str:
        return {"low": "낮음", "medium": "보통", "high": "높음"}[self.value]


@dataclass
class Todo:
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str | None = None
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    # ... to_dict(), from_dict(), is_overdue(), format_line() 등


# ============================================================
# 저장소 (Storage)
# ============================================================

class TodoStorage:
    def save(self, todos: list[Todo]) -> None: ...
    def load(self) -> list[Todo]: ...


# ============================================================
# 할일 관리자 (TodoManager)
# ============================================================

class TodoManager:
    def add(self, title, priority, due_date, tags) -> Todo: ...
    def complete(self, todo_id) -> Todo: ...
    def delete(self, todo_id, force) -> Todo: ...
    def search(self, keyword, include_completed) -> list[Todo]: ...
    def filter_todos(self, status, priority, tag, overdue) -> list[Todo]: ...
    def get_stats(self) -> dict: ...


# ============================================================
# CLI 파서
# ============================================================

def create_parser() -> argparse.ArgumentParser:
    """7개 서브커맨드(add, list, complete, delete, search, filter, stats)"""
    ...


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)
    storage = TodoStorage(args.data_file)
    manager = TodoManager(storage)
    handlers = {
        "add": handle_add,
        "list": handle_list,
        "complete": handle_complete,
        "delete": handle_delete,
        "search": handle_search,
        "filter": handle_filter,
        "stats": handle_stats,
    }
    handler = handlers.get(args.command)
    if handler:
        handler(args, manager)
```

위 코드는 구조만 보여주고 있습니다. 전체 코드는 예제 파일에서 확인할 수 있습니다.

### 통합 앱 실행 데모

**실행:**
```bash
$ python examples/python/chapter06/ex25_12_full_todo_app.py
```

**결과:**
```
============================================================
  CLI 할일 관리 앱 - 전체 통합 데모
============================================================

--- 1. 할일 추가 ---
>>> todo add 우유 사기 -t 장보기
추가 완료!
  [ ] #  1 [보통] 우유 사기 #장보기

>>> todo add 보고서 작성 -p high -d 2025-12-20 -t 업무 급함
추가 완료!
  [ ] #  2 [높음] 보고서 작성 (D-1) #업무 #급함

>>> todo add 운동하기 -t 건강 루틴
추가 완료!
  [ ] #  3 [보통] 운동하기 #건강 #루틴

>>> todo add 이메일 답장 -p high -d 2025-12-18 -t 업무
추가 완료!
  [ ] #  4 [높음] 이메일 답장 (기한 초과!) #업무

>>> todo add 책 읽기 - 파이썬 기초 -p low -d 2026-01-02 -t 공부 파이썬
추가 완료!
  [ ] #  5 [낮음] 책 읽기 - 파이썬 기초 (마감: 2026-01-02) #공부 #파이썬

>>> todo add 팀 회의 준비 -p high -d 2025-12-19 -t 업무 회의
추가 완료!
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!) #업무 #회의

--- 2. 할일 목록 보기 ---
>>> todo list
  할일 목록 | 전체: 6 | 완료: 0 | 미완료: 6
  기한 초과: 1개
  ───────────────────────────────────────────────────────
  [ ] #  4 [높음] 이메일 답장 (기한 초과!) #업무
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!) #업무 #회의
  [ ] #  2 [높음] 보고서 작성 (D-1) #업무 #급함
  [ ] #  1 [보통] 우유 사기 #장보기
  [ ] #  3 [보통] 운동하기 #건강 #루틴
  [ ] #  5 [낮음] 책 읽기 - 파이썬 기초 (마감: 2026-01-02) #공부 #파이썬
  ───────────────────────────────────────────────────────
  진행률: ░░░░░░░░░░░░░░░░░░░░ 0%

--- 3. 할일 완료 처리 ---
>>> todo complete 1
완료! #1 '우유 사기'

>>> todo complete 3
완료! #3 '운동하기'

--- 4. 전체 목록 (완료 포함) ---
>>> todo list --all
  할일 목록 | 전체: 6 | 완료: 2 | 미완료: 4
  ───────────────────────────────────────────────────────
  [ ] #  4 [높음] 이메일 답장 (기한 초과!) #업무
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!) #업무 #회의
  [ ] #  2 [높음] 보고서 작성 (D-1) #업무 #급함
  [ ] #  5 [낮음] 책 읽기 - 파이썬 기초 (마감: 2026-01-02) #공부 #파이썬
  [x] #  1 [보통] 우유 사기 #장보기
  [x] #  3 [보통] 운동하기 #건강 #루틴
  ───────────────────────────────────────────────────────
  진행률: ██████░░░░░░░░░░░░░░ 33%

--- 5. 키워드 검색 ---
>>> todo search 업무
  '업무' 검색 결과: 3개
  ──────────────────────────────────────────────────
  #2 [미완료] 보고서 작성 #업무 #급함
  #4 [미완료] 이메일 답장 #업무
  #6 [미완료] 팀 회의 준비 #업무 #회의
  ──────────────────────────────────────────────────

--- 6. 필터: 미완료 + 높은 우선순위 ---
>>> todo filter -s pending -p high
  필터: 상태=미완료 + 우선순위=높음
  결과: 3개 / 전체 6개
  ──────────────────────────────────────────────────
  [ ] #  2 [높음] 보고서 작성 (D-1) #업무 #급함
  [ ] #  4 [높음] 이메일 답장 (기한 초과!) #업무
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!) #업무 #회의
  ──────────────────────────────────────────────────

--- 7. 기한 초과 필터 ---
>>> todo filter --overdue
  필터: 기한초과
  결과: 1개 / 전체 6개
  ──────────────────────────────────────────────────
  [ ] #  4 [높음] 이메일 답장 (기한 초과!) #업무
  ──────────────────────────────────────────────────

--- 8. 완료된 할일 삭제 ---
>>> todo delete 1
삭제! #1 '우유 사기'

--- 9. 미완료 할일 강제 삭제 ---
>>> todo delete 4 --force
삭제! #4 '이메일 답장'

--- 10. 통계 보기 ---
>>> todo stats
  할일 통계
  ──────────────────────────────
  전체: 4
  완료: 1
  미완료: 3
  기한초과: 0
  완료율: 25%

--- 11. 최종 목록 ---
>>> todo list --all
  할일 목록 | 전체: 4 | 완료: 1 | 미완료: 3
  ───────────────────────────────────────────────────────
  [ ] #  6 [높음] 팀 회의 준비 (오늘 마감!) #업무 #회의
  [ ] #  2 [높음] 보고서 작성 (D-1) #업무 #급함
  [ ] #  5 [낮음] 책 읽기 - 파이썬 기초 (마감: 2026-01-02) #공부 #파이썬
  [x] #  3 [보통] 운동하기 #건강 #루틴
  ───────────────────────────────────────────────────────
  진행률: █████░░░░░░░░░░░░░░░ 25%
```

### 통합 앱의 아키텍처

완성된 앱의 전체 구조를 정리하면 다음과 같습니다:

```
CLI 할일 관리 앱 아키텍처
═══════════════════════════════════════════

사용자 입력 (터미널)
    │
    ▼
┌─────────────────────────────┐
│  argparse (CLI 파서)         │
│  - 명령어 분류               │
│  - 인자 파싱                 │
│  - 유효성 검사               │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Handler 함수               │
│  - handle_add()             │
│  - handle_list()            │
│  - handle_complete()        │
│  - handle_delete()          │
│  - handle_search()          │
│  - handle_filter()          │
│  - handle_stats()           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  TodoManager (비즈니스 로직) │
│  - CRUD 연산                │
│  - 검색 / 필터              │
│  - 통계 계산                │
└──────────┬──────────────────┘
           │
           ▼
┌──────────┴──────────────────┐
│  TodoStorage (데이터 계층)   │  ←→  todos.json
│  - save()                   │
│  - load()                   │
└─────────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Todo / Priority (모델)     │
│  - 데이터 구조              │
│  - 직렬화/역직렬화          │
│  - 표시 포맷팅              │
└─────────────────────────────┘
```

이 구조에서 각 계층은 **명확한 책임**을 가집니다:

1. **CLI 파서**: 사용자 입력을 구조화된 데이터로 변환
2. **Handler**: CLI와 비즈니스 로직을 연결하는 중간 계층
3. **Manager**: 핵심 비즈니스 로직 (데이터 조작)
4. **Storage**: 데이터 영구 저장 (파일 I/O)
5. **Model**: 데이터 구조 정의

> **Note:** 이 계층 구조는 나중에 웹 앱으로 전환할 때 큰 도움이 됩니다. CLI 파서와 Handler만 웹 프레임워크(Flask, FastAPI 등)의 라우트로 교체하면 Manager, Storage, Model은 그대로 재사용할 수 있습니다.

### 저장된 JSON 파일 구조

앱이 생성하는 JSON 파일의 구조는 다음과 같습니다:

```json
{
  "metadata": {
    "version": "1.0",
    "saved_at": "2025-12-19T14:30:00.123456",
    "total_count": 4,
    "completed_count": 1
  },
  "todos": [
    {
      "id": 2,
      "title": "보고서 작성",
      "priority": "high",
      "completed": false,
      "created_at": "2025-12-19T14:30:00.123456",
      "completed_at": null,
      "due_date": "2025-12-20",
      "tags": ["업무", "급함"]
    },
    ...
  ]
}
```

`metadata` 섹션에 버전 정보를 포함하는 이유는 **미래의 변경에 대비**하기 위해서입니다. 나중에 데이터 구조가 바뀌더라도 버전을 확인하여 적절한 마이그레이션을 수행할 수 있습니다.

---

## 25.10 바이브 코딩 회고

이 프로젝트에서 우리가 AI에게 보낸 프롬프트들을 돌아봅시다:

### 프롬프트 진행 패턴

```
프롬프트 1: "프로젝트 디렉토리 구조를 설계해줘"         → 뼈대
프롬프트 2: "argparse CLI 뼈대를 만들어줘"              → 인터페이스
프롬프트 3: "Todo 데이터 클래스를 만들어줘"              → 모델
프롬프트 4: "add 명령어를 구현해줘"                     → 기능 1
프롬프트 5: "list 명령어를 구현해줘"                    → 기능 2
프롬프트 6: "complete 명령어를 구현해줘"                → 기능 3
프롬프트 7: "delete 명령어를 구현해줘"                  → 기능 4
프롬프트 8: "JSON 저장 기능을 구현해줘"                 → 저장
프롬프트 9: "JSON 로드 기능을 구현해줘"                 → 로드
프롬프트 10: "검색 기능을 구현해줘"                     → 검색
프롬프트 11: "필터 기능을 구현해줘"                     → 필터
프롬프트 12: "모든 기능을 하나로 통합해줘"               → 완성
```

### 각 프롬프트에서 배운 교훈

| 단계 | 프롬프트 기법 | 효과 |
|------|-------------|------|
| 전체 설계 | 기능 목록을 먼저 나열 | AI가 전체 구조를 이해한 상태로 작업 |
| 뼈대 먼저 | "일단 출력만 하는 뼈대로" | 동작하는 코드를 빠르게 확보 |
| 구체적 요청 | 필드명, 메서드명, 반환형 명시 | 원하는 형태의 코드 생성 |
| 에러 케이스 | "존재하지 않을 때", "이미 완료일 때" | 견고한 에러 처리 |
| 시각적 요소 | "ANSI 색상", "진행률 바" | 사용하기 좋은 UX |
| 점진적 통합 | 개별 기능 확인 후 통합 | 버그 없는 통합 |

### 바이브 코딩 핵심 원칙 요약

이 프로젝트를 통해 체득한 바이브 코딩의 핵심 원칙을 정리합니다:

**1. 큰 문제를 작은 조각으로 나누기**
```
전체 앱을 한 번에 → 절대 하지 말 것
기능별로 하나씩   → 각 단계를 확인하며 전진
```

**2. 동작하는 코드를 항상 유지하기**
```
Step 1: 뼈대 → 실행 → 동작 확인
Step 2: 기능 추가 → 실행 → 동작 확인
Step 3: 또 추가 → 실행 → 동작 확인
...
```

**3. 구체적으로 요청하기**
```
나쁜 프롬프트: "할일 앱 만들어줘"
좋은 프롬프트: "TodoManager에 complete 메서드를 추가해줘.
              (성공여부, 메시지) 튜플을 반환하고,
              이미 완료된 경우와 ID가 없는 경우를 처리해줘."
```

**4. 에러 케이스를 먼저 생각하기**
```
정상 동작만 요청: 코드가 취약함
에러 케이스 포함: "파일이 없을 때", "손상되었을 때" → 견고한 코드
```

> **Tip:** 바이브 코딩은 "AI에게 모든 것을 맡기는 것"이 아닙니다. "내가 설계하고, AI가 구현하고, 내가 검증하는" 협업 과정입니다. 각 단계마다 코드를 실행하고 결과를 확인하는 것이 핵심입니다.

---

## 25.11 확장 아이디어

완성된 할일 관리 앱을 더 발전시킬 수 있는 방향을 소개합니다. 이 아이디어들은 다음 장의 프로젝트에서 활용할 수 있습니다.

### 기능 확장

| 확장 기능 | 설명 | AI 프롬프트 예시 |
|-----------|------|-----------------|
| **반복 할일** | 매일/매주 자동 생성 | "매주 반복되는 할일 기능을 추가해줘" |
| **서브태스크** | 할일 안에 세부 항목 | "할일에 하위 체크리스트를 추가해줘" |
| **알림** | 마감일 알림 | "마감일이 임박한 할일을 강조 표시해줘" |
| **내보내기** | CSV, Markdown 변환 | "할일 목록을 Markdown 표로 내보내줘" |
| **다중 프로젝트** | 프로젝트별 할일 분류 | "할일을 프로젝트별로 그룹화해줘" |

### 기술 확장

```
현재: Python + JSON 파일
  ↓
단계 1: SQLite 데이터베이스로 전환
단계 2: Flask/FastAPI로 웹 API 추가
단계 3: 웹 프론트엔드 연결
단계 4: 모바일 앱 연동
```

이러한 확장도 모두 바이브 코딩으로 단계적으로 구현할 수 있습니다!

---

## 정리

이 장에서는 **CLI 할일 관리 앱**을 처음부터 끝까지 바이브 코딩으로 완성했습니다.

### 핵심 요약

| 단계 | 구현 내용 | 핵심 기술 |
|------|-----------|-----------|
| **Step 1** | 프로젝트 구조 + CLI 뼈대 | `os.makedirs`, `argparse` |
| **Step 2** | 데이터 모델 + 추가/목록 | `dataclass`, `Enum`, ANSI 색상 |
| **Step 3** | 완료/삭제 기능 | 에러 처리, 안전 장치, 되돌리기 |
| **Step 4** | JSON 저장/로드 | `json`, 메타데이터, 부분 복구 |
| **Step 5** | 검색/필터 | 키워드 하이라이트, 메서드 체이닝 |
| **통합** | 완성된 앱 | 계층 아키텍처, 핸들러 패턴 |

### 배운 설계 원칙

1. **점진적 개발**: 작은 단위로 나누어 하나씩 구현하고 확인
2. **관심사의 분리**: Model, Storage, Manager, CLI를 독립된 계층으로 분리
3. **방어적 프로그래밍**: 잘못된 입력, 파일 손상 등 에러 상황에 대비
4. **사용자 경험**: 색상, 진행률, 명확한 에러 메시지로 사용 편의성 향상
5. **데이터 보존**: 삭제 히스토리, 부분 복구 등 데이터 손실 최소화

### 바이브 코딩 프로세스

```
1. 전체 기능 목록 작성
2. 단계별 프롬프트 설계
3. 각 단계: 프롬프트 → 코드 생성 → 실행 → 확인
4. 문제 발견 시: 구체적 수정 프롬프트
5. 전체 통합 및 최종 테스트
```

이 프로세스는 이후의 모든 프로젝트에도 동일하게 적용됩니다. 다음 장에서는 이 경험을 바탕으로 더 복잡한 프로젝트에 도전합니다.

> **Tip:** 이 장의 완성된 앱(`ex25_12_full_todo_app.py`)을 직접 실행해보세요. 할일을 추가하고, 완료하고, 검색해보면서 자신만의 할일을 관리해보는 것이 가장 좋은 학습 방법입니다.

---

**다음 장에서는** 정적 블로그 생성기 프로젝트를 통해 파일 처리, HTML 생성, 템플릿 엔진 등 더 다양한 기술을 바이브 코딩으로 다룹니다.
