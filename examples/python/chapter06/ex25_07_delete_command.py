"""
예제 25-07: delete 명령어 구현
- 할일을 삭제하는 기능을 구현합니다.
- 단일 삭제, 다중 삭제, 완료된 항목 일괄 삭제를 지원합니다.
- 삭제 전 확인 및 강제 삭제 옵션을 포함합니다.
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
    due_date: str | None = None
    tags: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        status = "[완료]" if self.completed else "[미완료]"
        return f"#{self.id} {status} {self.title}"


class TodoManager:
    """할일 관리자 - 삭제 기능에 집중"""

    def __init__(self) -> None:
        self.todos: list[Todo] = []
        self._deleted_history: list[Todo] = []  # 삭제 히스토리 (되돌리기용)

    def find_by_id(self, todo_id: int) -> Todo | None:
        """ID로 할일을 찾습니다."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def delete(self, todo_id: int, force: bool = False) -> tuple[bool, str]:
        """
        할일을 삭제합니다.

        Args:
            todo_id: 삭제할 할일 ID
            force: True이면 확인 없이 삭제

        Returns:
            (성공 여부, 메시지) 튜플
        """
        todo = self.find_by_id(todo_id)

        if todo is None:
            return False, f"오류: #{todo_id} 할일을 찾을 수 없습니다."

        # 미완료 할일 삭제 시 경고 (force가 아닌 경우)
        if not todo.completed and not force:
            return False, (
                f"경고: #{todo_id} '{todo.title}'은(는) 아직 미완료 상태입니다. "
                f"삭제하려면 --force 옵션을 사용하세요."
            )

        # 삭제 실행
        self.todos.remove(todo)
        self._deleted_history.append(todo)

        return True, f"삭제: #{todo_id} '{todo.title}'을(를) 삭제했습니다."

    def delete_multiple(self, todo_ids: list[int], force: bool = False) -> list[tuple[int, bool, str]]:
        """여러 할일을 삭제합니다."""
        results = []
        for todo_id in todo_ids:
            success, message = self.delete(todo_id, force=force)
            results.append((todo_id, success, message))
        return results

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
        # ID 순으로 재정렬
        self.todos.sort(key=lambda t: t.id)

        return True, f"복원: #{todo.id} '{todo.title}'을(를) 복원했습니다."

    def show_all(self) -> None:
        """모든 할일을 표시합니다."""
        if not self.todos:
            print("  할일이 없습니다.")
            return
        for todo in self.todos:
            print(f"  {todo}")

    def show_deleted_history(self) -> None:
        """삭제 히스토리를 표시합니다."""
        if not self._deleted_history:
            print("  삭제 히스토리가 비어 있습니다.")
            return
        for i, todo in enumerate(self._deleted_history, 1):
            print(f"  {i}. #{todo.id} '{todo.title}'")


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - delete 명령어 데모")
    print("=" * 55)
    print()

    # 데모 데이터 준비
    manager = TodoManager()
    manager.todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW, completed=True),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM, completed=True),
        Todo(id=4, title="이메일 답장", priority=Priority.HIGH),
        Todo(id=5, title="책 읽기", priority=Priority.LOW),
        Todo(id=6, title="빨래 개기", priority=Priority.MEDIUM, completed=True),
    ]

    print("--- 초기 할일 목록 ---")
    manager.show_all()
    print()

    # 1. 완료된 할일 삭제
    print("--- 1. 완료된 할일 삭제 ---")
    print(">>> todo delete 1")
    success, message = manager.delete(1)
    print(f"  {message}")
    print()

    # 2. 미완료 할일 삭제 시도 (force 없이)
    print("--- 2. 미완료 할일 삭제 시도 (force 없음) ---")
    print(">>> todo delete 2")
    success, message = manager.delete(2)
    print(f"  {message}")
    print()

    # 3. 미완료 할일 강제 삭제
    print("--- 3. 미완료 할일 강제 삭제 ---")
    print(">>> todo delete 2 --force")
    success, message = manager.delete(2, force=True)
    print(f"  {message}")
    print()

    # 4. 존재하지 않는 할일 삭제
    print("--- 4. 존재하지 않는 할일 삭제 ---")
    print(">>> todo delete 99")
    success, message = manager.delete(99)
    print(f"  {message}")
    print()

    # 5. 삭제 되돌리기
    print("--- 5. 마지막 삭제 되돌리기 ---")
    print(">>> todo undo")
    success, message = manager.undo_last_delete()
    print(f"  {message}")
    print()

    # 6. 현재 상태 확인
    print("--- 현재 할일 목록 ---")
    manager.show_all()
    print()

    # 7. 완료 항목 일괄 삭제
    print("--- 7. 완료 항목 일괄 삭제 ---")
    print(">>> todo delete --done")
    count, messages = manager.delete_completed()
    for msg in messages:
        print(msg)
    print(f"  총 {count}개 항목 삭제 완료")
    print()

    # 8. 최종 상태
    print("--- 최종 할일 목록 ---")
    manager.show_all()
    print()

    # 9. 삭제 히스토리
    print("--- 삭제 히스토리 ---")
    manager.show_deleted_history()
