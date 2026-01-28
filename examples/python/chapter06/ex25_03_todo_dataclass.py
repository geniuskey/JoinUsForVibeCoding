"""
예제 25-03: Todo 데이터 클래스
- dataclasses 모듈을 사용하여 할일 데이터 구조를 정의합니다.
- 할일의 속성(제목, 우선순위, 상태 등)을 체계적으로 관리합니다.
"""

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
    """
    할일 데이터 클래스

    Attributes:
        id: 할일 고유 번호
        title: 할일 제목
        priority: 우선순위 (low, medium, high)
        completed: 완료 여부
        created_at: 생성 일시
        completed_at: 완료 일시 (완료한 경우)
        due_date: 마감일 (선택)
        tags: 태그 목록 (선택)
    """
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

    def mark_incomplete(self) -> None:
        """할일을 미완료 상태로 되돌립니다."""
        self.completed = False
        self.completed_at = None

    def is_overdue(self) -> bool:
        """마감일이 지났는지 확인합니다."""
        if not self.due_date:
            return False
        due = datetime.fromisoformat(self.due_date)
        return not self.completed and datetime.now() > due

    def to_dict(self) -> dict:
        """딕셔너리로 변환합니다 (JSON 저장용)."""
        data = asdict(self)
        # Enum 값을 문자열로 변환
        data["priority"] = self.priority.value
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

    def __str__(self) -> str:
        return self.summary()


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - Todo 데이터 클래스 데모")
    print("=" * 55)
    print()

    # 1. 기본 할일 생성
    print("--- 1. 기본 할일 생성 ---")
    todo1 = Todo(id=1, title="우유 사기")
    print(f"할일 1: {todo1}")
    print(f"  우선순위: {todo1.priority.to_korean()}")
    print(f"  완료 여부: {todo1.completed}")
    print()

    # 2. 우선순위와 마감일이 있는 할일
    print("--- 2. 상세 할일 생성 ---")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    todo2 = Todo(
        id=2,
        title="보고서 작성",
        priority=Priority.HIGH,
        due_date=tomorrow,
        tags=["업무", "급함"],
    )
    print(f"할일 2: {todo2}")
    print(f"  기한 초과: {todo2.is_overdue()}")
    print()

    # 3. 기한이 지난 할일
    print("--- 3. 기한 초과 할일 ---")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    todo3 = Todo(
        id=3,
        title="이메일 답장",
        priority=Priority.HIGH,
        due_date=yesterday,
        tags=["업무"],
    )
    print(f"할일 3: {todo3}")
    print(f"  기한 초과: {todo3.is_overdue()}")
    print()

    # 4. 할일 완료 처리
    print("--- 4. 할일 완료 처리 ---")
    print(f"완료 전: {todo1}")
    todo1.mark_complete()
    print(f"완료 후: {todo1}")
    print(f"  완료 시각: {todo1.completed_at}")
    print()

    # 5. 딕셔너리 변환 (JSON 저장용)
    print("--- 5. 딕셔너리 변환 ---")
    todo_dict = todo2.to_dict()
    print(f"딕셔너리: {todo_dict}")
    print()

    # 6. 딕셔너리에서 복원
    print("--- 6. 딕셔너리에서 복원 ---")
    restored = Todo.from_dict(todo_dict)
    print(f"복원된 할일: {restored}")
    print(f"  원본과 동일: {restored.title == todo2.title}")
    print()

    # 7. 여러 할일 목록
    print("--- 7. 할일 목록 ---")
    todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW, tags=["장보기"]),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH, due_date=tomorrow, tags=["업무"]),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM, tags=["건강"]),
        Todo(id=4, title="책 읽기", priority=Priority.LOW),
    ]
    todos[0].mark_complete()  # 첫 번째 할일 완료

    for todo in todos:
        print(f"  {todo}")
