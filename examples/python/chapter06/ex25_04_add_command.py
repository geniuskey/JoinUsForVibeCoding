"""
예제 25-04: add 명령어 구현
- 할일을 추가하는 기능을 구현합니다.
- 제목, 우선순위, 마감일, 태그를 지정할 수 있습니다.
- 추가된 할일은 리스트에 저장됩니다.
"""

import argparse
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def to_korean(self) -> str:
        return {"low": "낮음", "medium": "보통", "high": "높음"}[self.value]


@dataclass
class Todo:
    """할일 데이터 클래스"""
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        symbols = {"low": "!", "medium": "!!", "high": "!!!"}
        status = "[완료]" if self.completed else "[미완료]"
        p = symbols[self.priority.value]
        result = f"#{self.id} {status} {p} {self.title}"
        if self.due_date:
            result += f" (마감: {self.due_date})"
        if self.tags:
            result += " [" + " ".join(f"#{t}" for t in self.tags) + "]"
        return result


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
                # 과거 날짜 경고
                if parsed_date.date() < datetime.now().date():
                    print(f"  주의: 마감일({due_date})이 과거 날짜입니다.")
            except ValueError:
                raise ValueError(f"잘못된 날짜 형식: '{due_date}' (YYYY-MM-DD 형식 필요)")

        # 우선순위 변환
        try:
            priority_enum = Priority(priority)
        except ValueError:
            raise ValueError(f"잘못된 우선순위: '{priority}' (low/medium/high 중 선택)")

        # 할일 객체 생성
        todo = Todo(
            id=self._next_id,
            title=title,
            priority=priority_enum,
            due_date=due_date,
            tags=tags or [],
        )

        # 목록에 추가
        self.todos.append(todo)
        self._next_id += 1

        return todo

    def show_all(self) -> None:
        """모든 할일을 표시합니다."""
        if not self.todos:
            print("  할일이 없습니다.")
            return
        for todo in self.todos:
            print(f"  {todo}")


def create_add_parser() -> argparse.ArgumentParser:
    """add 명령어 전용 파서를 생성합니다."""
    parser = argparse.ArgumentParser(
        prog="todo add",
        description="새로운 할일을 추가합니다.",
    )
    parser.add_argument("title", help="할일 제목")
    parser.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="우선순위 (기본값: medium)",
    )
    parser.add_argument(
        "-d", "--due",
        help="마감일 (YYYY-MM-DD)",
    )
    parser.add_argument(
        "-t", "--tags",
        nargs="+",
        default=[],
        help="태그 (공백으로 구분)",
    )
    return parser


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - add 명령어 데모")
    print("=" * 55)
    print()

    manager = TodoManager()
    parser = create_add_parser()

    # 다양한 add 명령어 시뮬레이션
    demo_commands = [
        (
            "기본 추가",
            ["우유 사기"],
        ),
        (
            "높은 우선순위로 추가",
            ["보고서 작성", "--priority", "high"],
        ),
        (
            "마감일 포함 추가",
            ["프레젠테이션 준비", "-p", "high", "-d", "2025-12-31"],
        ),
        (
            "태그 포함 추가",
            ["운동하기", "-t", "건강", "루틴"],
        ),
        (
            "모든 옵션 포함",
            ["팀 회의 자료 준비", "-p", "high", "-d", "2025-11-15", "-t", "업무", "급함"],
        ),
    ]

    for description, cmd_args in demo_commands:
        print(f"--- {description} ---")
        print(f">>> todo add {' '.join(cmd_args)}")

        args = parser.parse_args(cmd_args)
        try:
            todo = manager.add(
                title=args.title,
                priority=args.priority,
                due_date=args.due,
                tags=args.tags,
            )
            print(f"  추가 완료: {todo}")
        except ValueError as e:
            print(f"  오류: {e}")
        print()

    # 전체 목록 확인
    print("--- 현재 할일 목록 ---")
    manager.show_all()
    print()
    print(f"총 {len(manager.todos)}개의 할일이 등록되었습니다.")
