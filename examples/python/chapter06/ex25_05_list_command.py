"""
예제 25-05: list 명령어 구현
- 할일 목록을 보기 좋게 표시합니다.
- ANSI 색상 코드를 사용하여 우선순위별 색상을 표현합니다.
- 완료/미완료 상태를 시각적으로 구분합니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# === ANSI 색상 코드 ===
class Color:
    """터미널 ANSI 색상 코드"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    STRIKETHROUGH = "\033[9m"

    # 전경색
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    # 배경색
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"

    @staticmethod
    def colorize(text: str, *codes: str) -> str:
        """텍스트에 색상 코드를 적용합니다."""
        combined = "".join(codes)
        return f"{combined}{text}{Color.RESET}"


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


def format_todo_line(todo: Todo, use_color: bool = True) -> str:
    """할일 한 줄을 포맷팅합니다."""
    # 체크박스
    if todo.completed:
        checkbox = "[x]" if not use_color else Color.colorize("[x]", Color.GREEN)
    else:
        checkbox = "[ ]"

    # ID
    id_str = f"#{todo.id:>3}"
    if use_color:
        id_str = Color.colorize(id_str, Color.GRAY)

    # 우선순위 라벨
    priority_map = {
        Priority.HIGH: ("높음", Color.RED, Color.BOLD),
        Priority.MEDIUM: ("보통", Color.YELLOW,),
        Priority.LOW: ("낮음", Color.BLUE,),
    }
    label, *colors = priority_map[todo.priority]
    if use_color:
        priority_str = Color.colorize(f"[{label}]", *colors)
    else:
        priority_str = f"[{label}]"

    # 제목 (완료 시 취소선 + 흐리게)
    if todo.completed and use_color:
        title_str = Color.colorize(todo.title, Color.DIM, Color.STRIKETHROUGH)
    elif todo.completed:
        title_str = f"~{todo.title}~"
    else:
        title_str = todo.title

    # 마감일
    due_str = ""
    if todo.due_date:
        try:
            due = datetime.strptime(todo.due_date, "%Y-%m-%d")
            days_left = (due.date() - datetime.now().date()).days
            if todo.completed:
                due_str = f"(마감: {todo.due_date})"
                if use_color:
                    due_str = Color.colorize(due_str, Color.DIM)
            elif days_left < 0:
                due_str = f"(기한 초과 {abs(days_left)}일!)"
                if use_color:
                    due_str = Color.colorize(due_str, Color.RED, Color.BOLD)
            elif days_left == 0:
                due_str = "(오늘 마감!)"
                if use_color:
                    due_str = Color.colorize(due_str, Color.RED)
            elif days_left <= 3:
                due_str = f"(D-{days_left})"
                if use_color:
                    due_str = Color.colorize(due_str, Color.YELLOW)
            else:
                due_str = f"(마감: {todo.due_date})"
                if use_color:
                    due_str = Color.colorize(due_str, Color.GRAY)
        except ValueError:
            due_str = f"(마감: {todo.due_date})"

    # 태그
    tag_str = ""
    if todo.tags:
        tags = " ".join(f"#{t}" for t in todo.tags)
        if use_color:
            tag_str = Color.colorize(tags, Color.CYAN)
        else:
            tag_str = tags

    # 조합
    parts = [checkbox, id_str, priority_str, title_str]
    if due_str:
        parts.append(due_str)
    if tag_str:
        parts.append(tag_str)

    return " ".join(parts)


def display_todo_list(
    todos: list[Todo],
    show_completed: bool = False,
    use_color: bool = True,
) -> None:
    """할일 목록을 표시합니다."""

    # 필터링
    if show_completed:
        filtered = todos
    else:
        filtered = [t for t in todos if not t.completed]

    if not filtered:
        msg = "표시할 할일이 없습니다."
        if use_color:
            print(f"  {Color.colorize(msg, Color.GRAY)}")
        else:
            print(f"  {msg}")
        return

    # 헤더
    total = len(todos)
    done = sum(1 for t in todos if t.completed)
    pending = total - done

    if use_color:
        header = (
            f"  {Color.colorize('할일 목록', Color.BOLD, Color.WHITE)} "
            f"| 전체: {Color.colorize(str(total), Color.BOLD)} "
            f"| 완료: {Color.colorize(str(done), Color.GREEN)} "
            f"| 미완료: {Color.colorize(str(pending), Color.YELLOW)}"
        )
    else:
        header = f"  할일 목록 | 전체: {total} | 완료: {done} | 미완료: {pending}"

    print(header)
    print(f"  {'─' * 50}")

    # 정렬: 미완료 먼저, 우선순위 높은 것 먼저
    priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
    sorted_todos = sorted(
        filtered,
        key=lambda t: (t.completed, priority_order[t.priority], t.id),
    )

    # 출력
    for todo in sorted_todos:
        line = format_todo_line(todo, use_color=use_color)
        print(f"  {line}")

    print(f"  {'─' * 50}")

    # 진행률 바
    if total > 0:
        progress = done / total
        bar_length = 20
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        percentage = f"{progress:.0%}"

        if use_color:
            bar_color = Color.GREEN if progress == 1.0 else Color.YELLOW
            print(f"  진행률: {Color.colorize(bar, bar_color)} {percentage}")
        else:
            print(f"  진행률: [{bar}] {percentage}")


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - list 명령어 데모")
    print("=" * 55)
    print()

    # 데모 데이터 생성
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW,
             completed=True, tags=["장보기"]),
        Todo(id=2, title="보고서 작성", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "급함"]),
        Todo(id=3, title="운동하기", priority=Priority.MEDIUM,
             tags=["건강"]),
        Todo(id=4, title="이메일 답장", priority=Priority.HIGH,
             due_date=yesterday, tags=["업무"]),
        Todo(id=5, title="책 읽기", priority=Priority.LOW,
             due_date=next_week),
        Todo(id=6, title="팀 회의 준비", priority=Priority.HIGH,
             due_date=today, tags=["업무"]),
        Todo(id=7, title="빨래 개기", priority=Priority.MEDIUM,
             completed=True, tags=["집안일"]),
    ]

    # 1. 색상 출력 - 미완료만
    print("--- 1. 미완료 할일만 표시 (색상 출력) ---")
    display_todo_list(todos, show_completed=False, use_color=True)
    print()

    # 2. 색상 출력 - 전체
    print("--- 2. 전체 할일 표시 (색상 출력) ---")
    display_todo_list(todos, show_completed=True, use_color=True)
    print()

    # 3. 일반 출력 (색상 없음) - 파일 저장 등에 유용
    print("--- 3. 전체 할일 표시 (색상 없음) ---")
    display_todo_list(todos, show_completed=True, use_color=False)
