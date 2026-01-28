"""
예제 25-02: 기본 CLI 뼈대
- argparse 모듈을 사용하여 CLI 명령어 구조를 만듭니다.
- add, list, complete, delete 서브커맨드의 뼈대를 구성합니다.
"""

import argparse
import sys


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
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    # 서브커맨드 그룹 생성
    subparsers = parser.add_subparsers(
        title="명령어",
        description="사용 가능한 명령어",
        dest="command",
    )

    # --- add 서브커맨드 ---
    add_parser = subparsers.add_parser(
        "add",
        help="새로운 할일을 추가합니다",
    )
    add_parser.add_argument(
        "title",
        help="할일 제목",
    )
    add_parser.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="우선순위 (기본값: medium)",
    )
    add_parser.add_argument(
        "-d", "--due",
        help="마감일 (YYYY-MM-DD 형식)",
    )
    add_parser.set_defaults(func=handle_add)

    # --- list 서브커맨드 ---
    list_parser = subparsers.add_parser(
        "list",
        help="할일 목록을 표시합니다",
    )
    list_parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="완료된 항목도 함께 표시",
    )
    list_parser.set_defaults(func=handle_list)

    # --- complete 서브커맨드 ---
    complete_parser = subparsers.add_parser(
        "complete",
        help="할일을 완료 처리합니다",
    )
    complete_parser.add_argument(
        "id",
        type=int,
        help="완료할 할일 번호",
    )
    complete_parser.set_defaults(func=handle_complete)

    # --- delete 서브커맨드 ---
    delete_parser = subparsers.add_parser(
        "delete",
        help="할일을 삭제합니다",
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="삭제할 할일 번호",
    )
    delete_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="확인 없이 삭제",
    )
    delete_parser.set_defaults(func=handle_delete)

    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI 진입점"""
    parser = create_parser()
    args = parser.parse_args(argv)

    # 명령어가 지정되지 않으면 도움말 표시
    if not args.command:
        parser.print_help()
        return

    # 해당 명령어의 핸들러 함수 호출
    args.func(args)


if __name__ == "__main__":
    print("=" * 50)
    print("CLI 할일 관리 앱 - 기본 CLI 뼈대 데모")
    print("=" * 50)
    print()

    # 다양한 명령어 시뮬레이션
    demo_commands = [
        # (설명, 명령어 인자 리스트)
        ("할일 추가", ["add", "우유 사기", "--priority", "high"]),
        ("할일 추가 (마감일 포함)", ["add", "보고서 작성", "-d", "2025-12-31"]),
        ("할일 목록 (미완료만)", ["list"]),
        ("할일 목록 (전체)", ["list", "--all"]),
        ("할일 완료", ["complete", "1"]),
        ("할일 삭제 (강제)", ["delete", "2", "--force"]),
    ]

    for description, cmd_args in demo_commands:
        print(f">>> todo {' '.join(cmd_args)}")
        main(cmd_args)
        print()

    # 도움말 출력 시연
    print("--- 도움말 출력 ---")
    print(">>> todo --help")
    try:
        main(["--help"])
    except SystemExit:
        pass  # --help는 SystemExit을 발생시킴
