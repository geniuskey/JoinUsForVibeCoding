#!/usr/bin/env python3
"""
예제 19-10: 미니 할일 관리 CLI
add, list, done, delete 서브커맨드를 갖춘 완전한 미니 할일 관리 앱입니다.
JSON 파일을 사용하여 데이터를 저장합니다.
표준 라이브러리만 사용합니다.
"""

import argparse
import json
import os
import sys
import time

# ANSI 색상 코드
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_RED = "\033[91m"
BRIGHT_YELLOW = "\033[93m"

# 데이터 파일 경로
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex19_10_todos.json")


def load_todos():
    """할일 목록을 JSON 파일에서 불러옵니다."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"next_id": 1, "todos": []}


def save_todos(data):
    """할일 목록을 JSON 파일에 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def colorize(text, color):
    """터미널 색상을 적용합니다."""
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"


def find_todo(data, todo_id):
    """ID로 할일을 찾습니다."""
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            return todo
    return None


# ─── 서브커맨드 핸들러 ───────────────────────────────────

def cmd_add(args):
    """새 할일을 추가합니다."""
    data = load_todos()
    priority = getattr(args, "priority", "medium")

    todo = {
        "id": data["next_id"],
        "title": args.title,
        "done": False,
        "priority": priority,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "done_at": None,
    }
    data["todos"].append(todo)
    data["next_id"] += 1
    save_todos(data)

    priority_display = {"high": "높음", "medium": "보통", "low": "낮음"}
    print(colorize("✓ 할일이 추가되었습니다!", BRIGHT_GREEN))
    print(f"  ID: {todo['id']}")
    print(f"  제목: {todo['title']}")
    print(f"  우선순위: {priority_display.get(priority, priority)}")


def cmd_list(args):
    """할일 목록을 출력합니다."""
    data = load_todos()
    todos = data["todos"]

    show_all = getattr(args, "all", False)

    if not show_all:
        todos = [t for t in todos if not t["done"]]

    if not todos:
        if show_all:
            print(colorize("등록된 할일이 없습니다.", DIM))
        else:
            print(colorize("미완료 할일이 없습니다. (--all 옵션으로 전체 보기)", DIM))
        return

    # 우선순위 순서로 정렬
    priority_order = {"high": 0, "medium": 1, "low": 2}
    todos.sort(key=lambda t: (t["done"], priority_order.get(t.get("priority", "medium"), 1)))

    total = len(data["todos"])
    done_count = sum(1 for t in data["todos"] if t["done"])

    print(colorize(f"  할일 목록 ({done_count}/{total} 완료)", BOLD + CYAN))
    print("─" * 50)

    priority_colors = {"high": RED, "medium": YELLOW, "low": BLUE}
    priority_labels = {"high": "높음", "medium": "보통", "low": "낮음"}

    for todo in todos:
        todo_id = todo["id"]
        title = todo["title"]
        done = todo["done"]
        priority = todo.get("priority", "medium")

        if done:
            status = colorize("✓", BRIGHT_GREEN)
            title_display = colorize(title, DIM)
        else:
            status = colorize("○", BRIGHT_YELLOW)
            title_display = title

        pri_color = priority_colors.get(priority, YELLOW)
        pri_label = priority_labels.get(priority, priority)
        pri_display = colorize(f"[{pri_label}]", pri_color)

        print(f"  {status} {todo_id:3d}. {pri_display} {title_display}")

    print("─" * 50)


def cmd_done(args):
    """할일을 완료 처리합니다."""
    data = load_todos()
    todo = find_todo(data, args.id)

    if todo is None:
        print(colorize(f"오류: ID {args.id}인 할일을 찾을 수 없습니다.", BRIGHT_RED))
        return

    if todo["done"]:
        print(colorize(f"'{todo['title']}'은(는) 이미 완료된 항목입니다.", YELLOW))
        return

    todo["done"] = True
    todo["done_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_todos(data)

    print(colorize("✓ 할일이 완료되었습니다!", BRIGHT_GREEN))
    print(f"  [{todo['id']}] {todo['title']}")


def cmd_delete(args):
    """할일을 삭제합니다."""
    data = load_todos()
    todo = find_todo(data, args.id)

    if todo is None:
        print(colorize(f"오류: ID {args.id}인 할일을 찾을 수 없습니다.", BRIGHT_RED))
        return

    data["todos"] = [t for t in data["todos"] if t["id"] != args.id]
    save_todos(data)

    print(colorize("✗ 할일이 삭제되었습니다.", BRIGHT_RED))
    print(f"  [{todo['id']}] {todo['title']}")


def cmd_clear(args):
    """완료된 할일을 모두 삭제합니다."""
    data = load_todos()
    before_count = len(data["todos"])
    data["todos"] = [t for t in data["todos"] if not t["done"]]
    after_count = len(data["todos"])
    removed = before_count - after_count

    if removed == 0:
        print(colorize("삭제할 완료 항목이 없습니다.", DIM))
        return

    save_todos(data)
    print(colorize(f"✓ 완료된 할일 {removed}개가 삭제되었습니다.", BRIGHT_GREEN))


# ─── 메인 함수 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="미니 할일 관리 CLI — 할일을 추가, 조회, 완료, 삭제합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""사용 예:
  python ex19_10_todo_cli.py add "파이썬 공부하기"
  python ex19_10_todo_cli.py add "긴급 버그 수정" --priority high
  python ex19_10_todo_cli.py list
  python ex19_10_todo_cli.py list --all
  python ex19_10_todo_cli.py done 1
  python ex19_10_todo_cli.py delete 2
  python ex19_10_todo_cli.py clear"""
    )

    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # add
    sp_add = subparsers.add_parser("add", help="새 할일을 추가합니다")
    sp_add.add_argument("title", help="할일 제목")
    sp_add.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low"],
        default="medium",
        help="우선순위 (기본값: medium)"
    )
    sp_add.set_defaults(func=cmd_add)

    # list
    sp_list = subparsers.add_parser("list", help="할일 목록을 봅니다")
    sp_list.add_argument(
        "--all", "-a",
        action="store_true",
        help="완료된 항목도 함께 표시"
    )
    sp_list.set_defaults(func=cmd_list)

    # done
    sp_done = subparsers.add_parser("done", help="할일을 완료 처리합니다")
    sp_done.add_argument("id", type=int, help="완료할 할일 ID")
    sp_done.set_defaults(func=cmd_done)

    # delete
    sp_delete = subparsers.add_parser("delete", help="할일을 삭제합니다")
    sp_delete.add_argument("id", type=int, help="삭제할 할일 ID")
    sp_delete.set_defaults(func=cmd_delete)

    # clear
    sp_clear = subparsers.add_parser("clear", help="완료된 할일을 모두 삭제합니다")
    sp_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
