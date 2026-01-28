"""
예제 25-12: 전체 통합 앱
- 모든 기능을 통합한 완성된 CLI 할일 관리 앱입니다.
- argparse 서브커맨드를 사용하여 add, list, complete, delete, search, filter를 지원합니다.
- JSON 파일로 데이터를 영구 저장합니다.
- 실제 CLI 도구처럼 사용할 수 있습니다.

사용법:
    python ex25_12_full_todo_app.py add "할일 제목" --priority high
    python ex25_12_full_todo_app.py list
    python ex25_12_full_todo_app.py complete 1
    python ex25_12_full_todo_app.py delete 1
    python ex25_12_full_todo_app.py search "키워드"
    python ex25_12_full_todo_app.py filter --priority high --status pending
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path


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
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"
    BG_YELLOW = "\033[43m"
    BLACK = "\033[30m"

    @staticmethod
    def c(text: str, *codes: str) -> str:
        """텍스트에 색상을 적용합니다."""
        return f"{''.join(codes)}{text}{Color.RESET}"


# ============================================================
# 데이터 모델
# ============================================================

class Priority(Enum):
    """할일 우선순위"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def to_korean(self) -> str:
        return {"low": "낮음", "medium": "보통", "high": "높음"}[self.value]

    def to_symbol(self) -> str:
        return {"low": "!", "medium": "!!", "high": "!!!"}[self.value]


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

    def to_dict(self) -> dict:
        data = asdict(self)
        data["priority"] = self.priority.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        data = data.copy()
        data["priority"] = Priority(data.get("priority", "medium"))
        return cls(**data)

    def is_overdue(self) -> bool:
        if not self.due_date or self.completed:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            return datetime.now() > due + timedelta(days=1)
        except ValueError:
            return False

    def format_line(self, use_color: bool = True) -> str:
        """할일 한 줄을 포맷팅합니다."""
        # 체크박스
        if self.completed:
            cb = Color.c("[x]", Color.GREEN) if use_color else "[x]"
        else:
            cb = "[ ]"

        # ID
        id_str = f"#{self.id:>3}"
        if use_color:
            id_str = Color.c(id_str, Color.GRAY)

        # 우선순위
        p_map = {
            Priority.HIGH: ("높음", Color.RED, Color.BOLD),
            Priority.MEDIUM: ("보통", Color.YELLOW),
            Priority.LOW: ("낮음", Color.BLUE),
        }
        label, *colors = p_map[self.priority]
        p_str = Color.c(f"[{label}]", *colors) if use_color else f"[{label}]"

        # 제목
        if self.completed and use_color:
            title = Color.c(self.title, Color.DIM, Color.STRIKETHROUGH)
        else:
            title = self.title

        # 마감일
        due_str = ""
        if self.due_date:
            if self.completed:
                due_str = f"(마감: {self.due_date})"
                if use_color:
                    due_str = Color.c(due_str, Color.DIM)
            elif self.is_overdue():
                due_str = "(기한 초과!)"
                if use_color:
                    due_str = Color.c(due_str, Color.RED, Color.BOLD)
            else:
                try:
                    due = datetime.strptime(self.due_date, "%Y-%m-%d")
                    days = (due.date() - datetime.now().date()).days
                    if days == 0:
                        due_str = "(오늘 마감!)"
                        if use_color:
                            due_str = Color.c(due_str, Color.RED)
                    elif days <= 3:
                        due_str = f"(D-{days})"
                        if use_color:
                            due_str = Color.c(due_str, Color.YELLOW)
                    else:
                        due_str = f"(마감: {self.due_date})"
                        if use_color:
                            due_str = Color.c(due_str, Color.GRAY)
                except ValueError:
                    due_str = f"(마감: {self.due_date})"

        # 태그
        tag_str = ""
        if self.tags:
            tags_text = " ".join(f"#{t}" for t in self.tags)
            tag_str = Color.c(tags_text, Color.CYAN) if use_color else tags_text

        parts = [cb, id_str, p_str, title]
        if due_str:
            parts.append(due_str)
        if tag_str:
            parts.append(tag_str)
        return " ".join(parts)


# ============================================================
# 저장소 (Storage)
# ============================================================

class TodoStorage:
    """JSON 파일 기반 할일 저장소"""

    FORMAT_VERSION = "1.0"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save(self, todos: list[Todo]) -> None:
        """할일 목록을 JSON 파일로 저장합니다."""
        data = {
            "metadata": {
                "version": self.FORMAT_VERSION,
                "saved_at": datetime.now().isoformat(),
                "total_count": len(todos),
                "completed_count": sum(1 for t in todos if t.completed),
            },
            "todos": [t.to_dict() for t in todos],
        }
        dir_path = os.path.dirname(self.file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> list[Todo]:
        """JSON 파일에서 할일 목록을 불러옵니다."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Todo.from_dict(item) for item in data.get("todos", [])]
        except (json.JSONDecodeError, KeyError, TypeError):
            return []


# ============================================================
# 할일 관리자 (TodoManager)
# ============================================================

class TodoManager:
    """할일 CRUD 및 검색/필터 기능을 제공하는 관리자 클래스"""

    def __init__(self, storage: TodoStorage) -> None:
        self.storage = storage
        self.todos: list[Todo] = storage.load()

    def _next_id(self) -> int:
        """다음 사용할 ID를 반환합니다."""
        if not self.todos:
            return 1
        return max(t.id for t in self.todos) + 1

    def _save(self) -> None:
        """현재 상태를 파일에 저장합니다."""
        self.storage.save(self.todos)

    # --- CRUD 명령어 ---

    def add(self, title: str, priority: str = "medium",
            due_date: str | None = None, tags: list[str] | None = None) -> Todo:
        """할일을 추가합니다."""
        title = title.strip()
        if not title:
            raise ValueError("할일 제목은 비어 있을 수 없습니다.")

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"잘못된 날짜 형식: '{due_date}' (YYYY-MM-DD 필요)")

        todo = Todo(
            id=self._next_id(),
            title=title,
            priority=Priority(priority),
            due_date=due_date,
            tags=tags or [],
        )
        self.todos.append(todo)
        self._save()
        return todo

    def complete(self, todo_id: int) -> Todo:
        """할일을 완료 처리합니다."""
        todo = self._find(todo_id)
        if todo.completed:
            raise ValueError(f"#{todo_id} '{todo.title}'은(는) 이미 완료 상태입니다.")
        todo.completed = True
        todo.completed_at = datetime.now().isoformat()
        self._save()
        return todo

    def delete(self, todo_id: int, force: bool = False) -> Todo:
        """할일을 삭제합니다."""
        todo = self._find(todo_id)
        if not todo.completed and not force:
            raise ValueError(
                f"#{todo_id} '{todo.title}'은(는) 미완료 상태입니다. "
                f"--force 옵션으로 삭제하세요."
            )
        self.todos.remove(todo)
        self._save()
        return todo

    def _find(self, todo_id: int) -> Todo:
        """ID로 할일을 찾습니다."""
        for t in self.todos:
            if t.id == todo_id:
                return t
        raise ValueError(f"#{todo_id} 할일을 찾을 수 없습니다.")

    # --- 검색/필터 ---

    def search(self, keyword: str, include_completed: bool = True) -> list[Todo]:
        """키워드로 할일을 검색합니다."""
        kw = keyword.lower()
        results = []
        for t in self.todos:
            if not include_completed and t.completed:
                continue
            if kw in t.title.lower() or any(kw in tag.lower() for tag in t.tags):
                results.append(t)
        return results

    def filter_todos(
        self,
        status: str | None = None,
        priority: str | None = None,
        tag: str | None = None,
        overdue: bool = False,
    ) -> list[Todo]:
        """조건으로 할일을 필터링합니다."""
        result = self.todos

        if status == "pending":
            result = [t for t in result if not t.completed]
        elif status == "done":
            result = [t for t in result if t.completed]

        if priority:
            p = Priority(priority)
            result = [t for t in result if t.priority == p]

        if tag:
            tag_lower = tag.lower()
            result = [t for t in result if any(tg.lower() == tag_lower for tg in t.tags)]

        if overdue:
            result = [t for t in result if t.is_overdue()]

        # 우선순위 순 정렬
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        result.sort(key=lambda t: (t.completed, order[t.priority], t.id))
        return result

    def get_stats(self) -> dict:
        """통계를 반환합니다."""
        total = len(self.todos)
        done = sum(1 for t in self.todos if t.completed)
        overdue = sum(1 for t in self.todos if t.is_overdue())
        return {
            "전체": total,
            "완료": done,
            "미완료": total - done,
            "기한초과": overdue,
            "완료율": f"{done/total*100:.0f}%" if total > 0 else "0%",
        }


# ============================================================
# CLI 핸들러 함수
# ============================================================

def handle_add(args: argparse.Namespace, manager: TodoManager) -> None:
    """add 명령어 처리"""
    try:
        todo = manager.add(
            title=args.title,
            priority=args.priority,
            due_date=args.due,
            tags=args.tags or [],
        )
        print(Color.c("추가 완료!", Color.GREEN, Color.BOLD))
        print(f"  {todo.format_line()}")
    except ValueError as e:
        print(Color.c(f"오류: {e}", Color.RED))


def handle_list(args: argparse.Namespace, manager: TodoManager) -> None:
    """list 명령어 처리"""
    todos = manager.todos
    if not args.all:
        display = [t for t in todos if not t.completed]
    else:
        display = todos

    if not display:
        print(Color.c("표시할 할일이 없습니다.", Color.GRAY))
        return

    # 통계 헤더
    stats = manager.get_stats()
    print(
        f"  {Color.c('할일 목록', Color.BOLD)} "
        f"| 전체: {Color.c(str(stats['전체']), Color.BOLD)} "
        f"| 완료: {Color.c(str(stats['완료']), Color.GREEN)} "
        f"| 미완료: {Color.c(str(stats['미완료']), Color.YELLOW)}"
    )
    if stats["기한초과"] > 0:
        print(f"  {Color.c(f'기한 초과: {stats[\"기한초과\"]}개', Color.RED, Color.BOLD)}")
    print(f"  {'─' * 55}")

    # 정렬: 미완료 먼저, 우선순위 순
    order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
    display.sort(key=lambda t: (t.completed, order[t.priority], t.id))

    for todo in display:
        print(f"  {todo.format_line()}")
    print(f"  {'─' * 55}")

    # 진행률 바
    total = stats["전체"]
    done = stats["완료"]
    if total > 0:
        pct = done / total
        filled = int(20 * pct)
        bar = "█" * filled + "░" * (20 - filled)
        bar_color = Color.GREEN if pct == 1.0 else Color.YELLOW
        print(f"  진행률: {Color.c(bar, bar_color)} {pct:.0%}")


def handle_complete(args: argparse.Namespace, manager: TodoManager) -> None:
    """complete 명령어 처리"""
    for todo_id in args.ids:
        try:
            todo = manager.complete(todo_id)
            print(Color.c(f"완료!", Color.GREEN) + f" #{todo.id} '{todo.title}'")
        except ValueError as e:
            print(Color.c(f"오류: {e}", Color.RED))


def handle_delete(args: argparse.Namespace, manager: TodoManager) -> None:
    """delete 명령어 처리"""
    try:
        todo = manager.delete(args.id, force=args.force)
        print(Color.c(f"삭제!", Color.RED) + f" #{todo.id} '{todo.title}'")
    except ValueError as e:
        print(Color.c(f"오류: {e}", Color.RED))


def handle_search(args: argparse.Namespace, manager: TodoManager) -> None:
    """search 명령어 처리"""
    results = manager.search(args.keyword, include_completed=not args.pending)
    keyword = args.keyword

    if not results:
        print(Color.c(f"'{keyword}'에 대한 검색 결과가 없습니다.", Color.YELLOW))
        return

    print(f"  '{Color.c(keyword, Color.BOLD)}' 검색 결과: {Color.c(str(len(results)), Color.GREEN)}개")
    print(f"  {'─' * 50}")
    for todo in results:
        # 키워드 하이라이트
        title = todo.title
        kw_lower = keyword.lower()
        title_lower = title.lower()
        if kw_lower in title_lower:
            idx = title_lower.find(kw_lower)
            matched = title[idx:idx + len(keyword)]
            title = title[:idx] + Color.c(matched, Color.BG_YELLOW, Color.BLACK, Color.BOLD) + title[idx + len(keyword):]

        status = Color.c("[완료]", Color.GREEN) if todo.completed else "[미완료]"
        tags = ""
        if todo.tags:
            tag_parts = []
            for tg in todo.tags:
                if kw_lower in tg.lower():
                    tag_parts.append(Color.c(f"#{tg}", Color.BG_YELLOW, Color.BLACK))
                else:
                    tag_parts.append(Color.c(f"#{tg}", Color.CYAN))
            tags = " " + " ".join(tag_parts)
        print(f"  #{todo.id} {status} {title}{tags}")
    print(f"  {'─' * 50}")


def handle_filter(args: argparse.Namespace, manager: TodoManager) -> None:
    """filter 명령어 처리"""
    results = manager.filter_todos(
        status=args.status,
        priority=args.priority,
        tag=args.tag,
        overdue=args.overdue,
    )

    # 필터 설명 생성
    filters = []
    if args.status:
        filters.append(f"상태={'미완료' if args.status == 'pending' else '완료'}")
    if args.priority:
        filters.append(f"우선순위={Priority(args.priority).to_korean()}")
    if args.tag:
        filters.append(f"태그={args.tag}")
    if args.overdue:
        filters.append("기한초과")
    filter_desc = " + ".join(filters) if filters else "전체"

    print(f"  필터: {Color.c(filter_desc, Color.CYAN)}")
    print(f"  결과: {len(results)}개 / 전체 {len(manager.todos)}개")
    print(f"  {'─' * 50}")
    if not results:
        print(Color.c("  (조건에 맞는 할일이 없습니다)", Color.GRAY))
    else:
        for todo in results:
            print(f"  {todo.format_line()}")
    print(f"  {'─' * 50}")


def handle_stats(args: argparse.Namespace, manager: TodoManager) -> None:
    """stats 명령어 처리"""
    stats = manager.get_stats()
    print(f"  {Color.c('할일 통계', Color.BOLD)}")
    print(f"  {'─' * 30}")
    for key, value in stats.items():
        print(f"  {key}: {Color.c(str(value), Color.BOLD)}")


# ============================================================
# CLI 파서 구성
# ============================================================

def create_parser() -> argparse.ArgumentParser:
    """CLI 파서를 생성합니다."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="CLI 할일 관리 앱 - 터미널에서 할일을 관리하세요!",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument(
        "--data-file",
        default="/tmp/todo-cli-app-data/todos.json",
        help="데이터 파일 경로",
    )

    subs = parser.add_subparsers(title="명령어", dest="command")

    # add
    p_add = subs.add_parser("add", help="새 할일 추가")
    p_add.add_argument("title", help="할일 제목")
    p_add.add_argument("-p", "--priority", choices=["low", "medium", "high"],
                       default="medium", help="우선순위")
    p_add.add_argument("-d", "--due", help="마감일 (YYYY-MM-DD)")
    p_add.add_argument("-t", "--tags", nargs="+", help="태그들")

    # list
    p_list = subs.add_parser("list", help="할일 목록")
    p_list.add_argument("-a", "--all", action="store_true", help="완료 항목 포함")

    # complete
    p_comp = subs.add_parser("complete", help="할일 완료")
    p_comp.add_argument("ids", type=int, nargs="+", help="완료할 할일 번호들")

    # delete
    p_del = subs.add_parser("delete", help="할일 삭제")
    p_del.add_argument("id", type=int, help="삭제할 할일 번호")
    p_del.add_argument("-f", "--force", action="store_true", help="강제 삭제")

    # search
    p_search = subs.add_parser("search", help="할일 검색")
    p_search.add_argument("keyword", help="검색 키워드")
    p_search.add_argument("--pending", action="store_true", help="미완료만")

    # filter
    p_filter = subs.add_parser("filter", help="할일 필터")
    p_filter.add_argument("-s", "--status", choices=["pending", "done"], help="상태 필터")
    p_filter.add_argument("-p", "--priority", choices=["low", "medium", "high"], help="우선순위 필터")
    p_filter.add_argument("--tag", help="태그 필터")
    p_filter.add_argument("--overdue", action="store_true", help="기한 초과만")

    # stats
    subs.add_parser("stats", help="통계 보기")

    return parser


# ============================================================
# 메인 진입점
# ============================================================

def main(argv: list[str] | None = None) -> None:
    """CLI 메인 진입점"""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

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


if __name__ == "__main__":
    # 데모 모드: 인자가 없으면 시연용 시나리오 실행
    if len(sys.argv) > 1:
        # 실제 CLI 모드
        main()
    else:
        # 데모 시나리오
        import shutil

        data_file = "/tmp/todo-cli-demo-full/todos.json"
        data_dir = os.path.dirname(data_file)

        # 기존 데이터 초기화
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)

        print("=" * 60)
        print("  CLI 할일 관리 앱 - 전체 통합 데모")
        print("=" * 60)
        print()

        demo_steps = [
            ("1. 할일 추가", [
                ["add", "우유 사기", "-t", "장보기", "--data-file", data_file],
                ["add", "보고서 작성", "-p", "high", "-d",
                 (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                 "-t", "업무", "급함", "--data-file", data_file],
                ["add", "운동하기", "-t", "건강", "루틴", "--data-file", data_file],
                ["add", "이메일 답장", "-p", "high", "-d",
                 (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                 "-t", "업무", "--data-file", data_file],
                ["add", "책 읽기 - 파이썬 기초", "-p", "low", "-d",
                 (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                 "-t", "공부", "파이썬", "--data-file", data_file],
                ["add", "팀 회의 준비", "-p", "high", "-d",
                 datetime.now().strftime("%Y-%m-%d"),
                 "-t", "업무", "회의", "--data-file", data_file],
            ]),
            ("2. 할일 목록 보기", [
                ["list", "--data-file", data_file],
            ]),
            ("3. 할일 완료 처리", [
                ["complete", "1", "--data-file", data_file],
                ["complete", "3", "--data-file", data_file],
            ]),
            ("4. 전체 목록 (완료 포함)", [
                ["list", "--all", "--data-file", data_file],
            ]),
            ("5. 키워드 검색", [
                ["search", "업무", "--data-file", data_file],
            ]),
            ("6. 필터: 미완료 + 높은 우선순위", [
                ["filter", "-s", "pending", "-p", "high", "--data-file", data_file],
            ]),
            ("7. 기한 초과 필터", [
                ["filter", "--overdue", "--data-file", data_file],
            ]),
            ("8. 완료된 할일 삭제", [
                ["delete", "1", "--data-file", data_file],
            ]),
            ("9. 미완료 할일 강제 삭제", [
                ["delete", "4", "--force", "--data-file", data_file],
            ]),
            ("10. 통계 보기", [
                ["stats", "--data-file", data_file],
            ]),
            ("11. 최종 목록", [
                ["list", "--all", "--data-file", data_file],
            ]),
        ]

        for step_name, commands in demo_steps:
            print(f"--- {step_name} ---")
            for cmd in commands:
                # --data-file을 제외한 사용자 가시 명령어 표시
                visible = [c for c in cmd if c != "--data-file" and c != data_file]
                print(f">>> todo {' '.join(visible)}")
                main(cmd)
            print()

        # 저장된 JSON 파일 확인
        print("--- 저장된 데이터 파일 ---")
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                print(f.read())

        # 정리
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)
        print("데모 완료! 임시 파일을 정리했습니다.")
