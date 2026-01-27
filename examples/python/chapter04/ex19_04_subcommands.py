#!/usr/bin/env python3
"""
예제 19-4: 서브커맨드 구현
add_subparsers를 사용하여 add, list, delete 서브커맨드를 구현합니다.
"""

import argparse
import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex19_04_notes.json")


def load_notes():
    """저장된 메모 목록을 불러옵니다."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_notes(notes):
    """메모 목록을 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def cmd_add(args):
    """메모를 추가합니다."""
    notes = load_notes()
    note = {"id": len(notes) + 1, "content": args.content}
    notes.append(note)
    save_notes(notes)
    print(f"메모가 추가되었습니다: [{note['id']}] {note['content']}")


def cmd_list(args):
    """메모 목록을 출력합니다."""
    notes = load_notes()
    if not notes:
        print("저장된 메모가 없습니다.")
        return
    print(f"총 {len(notes)}개의 메모:")
    for note in notes:
        print(f"  [{note['id']}] {note['content']}")


def cmd_delete(args):
    """메모를 삭제합니다."""
    notes = load_notes()
    original_count = len(notes)
    notes = [n for n in notes if n["id"] != args.id]

    if len(notes) == original_count:
        print(f"오류: ID {args.id}인 메모를 찾을 수 없습니다.")
        return

    save_notes(notes)
    print(f"메모 [{args.id}]가 삭제되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description="간단한 메모 관리 CLI 도구"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="사용 가능한 명령어"
    )

    # add 서브커맨드
    parser_add = subparsers.add_parser("add", help="새 메모를 추가합니다")
    parser_add.add_argument("content", help="메모 내용")
    parser_add.set_defaults(func=cmd_add)

    # list 서브커맨드
    parser_list = subparsers.add_parser("list", help="메모 목록을 봅니다")
    parser_list.set_defaults(func=cmd_list)

    # delete 서브커맨드
    parser_delete = subparsers.add_parser("delete", help="메모를 삭제합니다")
    parser_delete.add_argument("id", type=int, help="삭제할 메모 ID")
    parser_delete.set_defaults(func=cmd_delete)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
