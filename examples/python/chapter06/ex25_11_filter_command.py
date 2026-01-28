"""
예제 25-11: filter 명령어 구현
- 할일을 상태(완료/미완료), 우선순위, 태그, 마감일로 필터링합니다.
- 여러 조건을 조합하여 복합 필터링을 지원합니다.
- 필터 결과를 정렬하여 표시합니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


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
        return self

    def by_priority(self, priority: Priority) -> "TodoFilter":
        """우선순위로 필터링합니다."""
        self._filters.append(
            (f"우선순위={priority.to_korean()}", lambda t: t.priority == priority)
        )
        return self

    def by_priorities(self, priorities: list[Priority]) -> "TodoFilter":
        """여러 우선순위로 필터링합니다."""
        labels = ", ".join(p.to_korean() for p in priorities)
        self._filters.append(
            (f"우선순위=[{labels}]", lambda t: t.priority in priorities)
        )
        return self

    def by_tag(self, tag: str) -> "TodoFilter":
        """태그로 필터링합니다."""
        tag_lower = tag.lower()
        self._filters.append(
            (f"태그={tag}", lambda t: any(tg.lower() == tag_lower for tg in t.tags))
        )
        return self

    def by_has_due_date(self, has_due: bool = True) -> "TodoFilter":
        """마감일 유무로 필터링합니다."""
        label = "있음" if has_due else "없음"
        self._filters.append(
            (f"마감일={label}", lambda t: (t.due_date is not None) == has_due)
        )
        return self

    def by_overdue(self) -> "TodoFilter":
        """기한이 지난 할일만 필터링합니다."""
        now = datetime.now()

        def is_overdue(t: Todo) -> bool:
            if not t.due_date or t.completed:
                return False
            try:
                due = datetime.strptime(t.due_date, "%Y-%m-%d")
                return due < now
            except ValueError:
                return False

        self._filters.append(("기한초과", is_overdue))
        return self

    def by_due_within_days(self, days: int) -> "TodoFilter":
        """지정된 일수 이내에 마감인 할일만 필터링합니다."""
        now = datetime.now()
        deadline = now + timedelta(days=days)

        def due_within(t: Todo) -> bool:
            if not t.due_date or t.completed:
                return False
            try:
                due = datetime.strptime(t.due_date, "%Y-%m-%d")
                return now <= due <= deadline
            except ValueError:
                return False

        self._filters.append((f"마감임박({days}일내)", due_within))
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
        elif sort_by == "id":
            result.sort(key=lambda t: t.id)
        elif sort_by == "created":
            result.sort(key=lambda t: t.created_at)

        return result

    def get_filter_description(self) -> str:
        """적용된 필터 설명을 반환합니다."""
        if not self._filters:
            return "필터 없음 (전체)"
        return " + ".join(name for name, _ in self._filters)

    def reset(self) -> "TodoFilter":
        """필터를 초기화합니다."""
        self._filters = []
        return self


def display_filtered(
    todos: list[Todo],
    filter_desc: str,
    total_count: int,
) -> None:
    """필터링 결과를 표시합니다."""
    print(f"  필터: {filter_desc}")
    print(f"  결과: {len(todos)}개 / 전체 {total_count}개")
    print(f"  {'─' * 50}")
    if not todos:
        print("  (조건에 맞는 할일이 없습니다)")
    else:
        for todo in todos:
            print(f"  {todo}")
    print(f"  {'─' * 50}")


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - filter 명령어 데모")
    print("=" * 55)
    print()

    # 데모 데이터 생성
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    in_3_days = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW,
             completed=True, tags=["장보기"]),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "급함"]),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM,
             tags=["건강", "루틴"]),
        Todo(id=4, title="이메일 답장", priority=Priority.HIGH,
             due_date=yesterday, tags=["업무"]),
        Todo(id=5, title="책 읽기", priority=Priority.LOW,
             due_date=next_month),
        Todo(id=6, title="팀 회의 준비", priority=Priority.HIGH,
             due_date=today, tags=["업무", "회의"]),
        Todo(id=7, title="빨래 개기", priority=Priority.MEDIUM,
             completed=True, tags=["집안일"]),
        Todo(id=8, title="저녁 장보기", priority=Priority.MEDIUM,
             due_date=in_3_days, tags=["장보기"]),
        Todo(id=9, title="코드 리뷰", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "개발"]),
        Todo(id=10, title="일기 쓰기", priority=Priority.LOW,
              tags=["루틴"]),
    ]

    total = len(todos)

    # 1. 미완료 할일만
    print("--- 1. 미완료 할일 필터 ---")
    print(">>> todo filter --status pending")
    f = TodoFilter(todos).by_status(completed=False)
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 2. 높은 우선순위만
    print("--- 2. 높은 우선순위 필터 ---")
    print(">>> todo filter --priority high")
    f = TodoFilter(todos).by_priority(Priority.HIGH)
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 3. 태그로 필터
    print("--- 3. '업무' 태그 필터 ---")
    print(">>> todo filter --tag 업무")
    f = TodoFilter(todos).by_tag("업무")
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 4. 기한 초과 할일
    print("--- 4. 기한 초과 할일 ---")
    print(">>> todo filter --overdue")
    f = TodoFilter(todos).by_overdue()
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 5. 3일 이내 마감
    print("--- 5. 3일 이내 마감 할일 ---")
    print(">>> todo filter --due-within 3")
    f = TodoFilter(todos).by_due_within_days(3)
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 6. 복합 필터: 미완료 + 높은 우선순위
    print("--- 6. 복합 필터: 미완료 + 높은 우선순위 ---")
    print(">>> todo filter --status pending --priority high")
    f = TodoFilter(todos).by_status(False).by_priority(Priority.HIGH)
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 7. 복합 필터: 업무 태그 + 마감일 있음
    print("--- 7. 복합 필터: 업무 태그 + 마감일 있음 ---")
    print(">>> todo filter --tag 업무 --has-due")
    f = TodoFilter(todos).by_tag("업무").by_has_due_date(True)
    result = f.apply(sort_by="due_date")
    display_filtered(result, f.get_filter_description(), total)
    print()

    # 8. 완료된 할일만
    print("--- 8. 완료된 할일 필터 ---")
    print(">>> todo filter --status done")
    f = TodoFilter(todos).by_status(completed=True)
    result = f.apply()
    display_filtered(result, f.get_filter_description(), total)
