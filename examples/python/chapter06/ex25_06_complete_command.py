"""
예제 25-06: complete 명령어 구현
- 할일을 완료 상태로 변경하는 기능을 구현합니다.
- ID로 단일 할일 완료, 여러 할일 동시 완료, 완료 취소 기능을 포함합니다.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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

    def __str__(self) -> str:
        status = "[완료]" if self.completed else "[미완료]"
        return f"#{self.id} {status} {self.title}"


class TodoManager:
    """할일 관리자 - 완료 기능에 집중"""

    def __init__(self) -> None:
        self.todos: list[Todo] = []

    def find_by_id(self, todo_id: int) -> Todo | None:
        """ID로 할일을 찾습니다."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def complete(self, todo_id: int) -> tuple[bool, str]:
        """
        할일을 완료 처리합니다.

        Returns:
            (성공 여부, 메시지) 튜플
        """
        todo = self.find_by_id(todo_id)

        # 할일이 존재하지 않는 경우
        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        # 이미 완료된 경우
        if todo.completed:
            return False, f"알림: #{todo_id} '{todo.title}'은(는) 이미 완료 상태입니다."

        # 완료 처리
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
        """
        할일 완료를 취소합니다 (미완료로 되돌림).

        Returns:
            (성공 여부, 메시지) 튜플
        """
        todo = self.find_by_id(todo_id)

        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        if not todo.completed:
            return False, f"알림: #{todo_id} '{todo.title}'은(는) 이미 미완료 상태입니다."

        todo.completed = False
        todo.completed_at = None

        return True, f"되돌림: #{todo_id} '{todo.title}'을(를) 미완료로 변경했습니다."

    def show_all(self) -> None:
        """모든 할일을 표시합니다."""
        if not self.todos:
            print("  할일이 없습니다.")
            return
        for todo in self.todos:
            completion_time = ""
            if todo.completed and todo.completed_at:
                # ISO 형식에서 시간만 추출
                try:
                    dt = datetime.fromisoformat(todo.completed_at)
                    completion_time = f" (완료: {dt.strftime('%H:%M:%S')})"
                except ValueError:
                    completion_time = ""
            print(f"  {todo}{completion_time}")

    def get_stats(self) -> dict:
        """할일 통계를 반환합니다."""
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t.completed)
        return {
            "전체": total,
            "완료": completed,
            "미완료": total - completed,
            "완료율": f"{completed/total*100:.1f}%" if total > 0 else "0%",
        }


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - complete 명령어 데모")
    print("=" * 55)
    print()

    # 데모 데이터 준비
    manager = TodoManager()
    demo_todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM),
        Todo(id=4, title="이메일 답장", priority=Priority.HIGH),
        Todo(id=5, title="책 읽기", priority=Priority.LOW),
    ]
    manager.todos = demo_todos

    print("--- 초기 할일 목록 ---")
    manager.show_all()
    print()

    # 1. 단일 할일 완료
    print("--- 1. 단일 할일 완료 ---")
    print(">>> todo complete 1")
    success, message = manager.complete(1)
    print(f"  {message}")
    print()

    # 2. 이미 완료된 할일 재완료 시도
    print("--- 2. 이미 완료된 할일 재완료 시도 ---")
    print(">>> todo complete 1")
    success, message = manager.complete(1)
    print(f"  {message}")
    print()

    # 3. 존재하지 않는 할일 완료 시도
    print("--- 3. 존재하지 않는 할일 완료 시도 ---")
    print(">>> todo complete 99")
    success, message = manager.complete(99)
    print(f"  {message}")
    print()

    # 4. 여러 할일 동시 완료
    print("--- 4. 여러 할일 동시 완료 ---")
    print(">>> todo complete 2 3 4")
    results = manager.complete_multiple([2, 3, 4])
    for todo_id, success, message in results:
        status = "성공" if success else "실패"
        print(f"  [{status}] {message}")
    print()

    # 5. 완료 취소
    print("--- 5. 완료 취소 ---")
    print(">>> todo uncomplete 3")
    success, message = manager.uncomplete(3)
    print(f"  {message}")
    print()

    # 6. 최종 상태
    print("--- 최종 할일 목록 ---")
    manager.show_all()
    print()

    # 7. 통계
    print("--- 통계 ---")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
