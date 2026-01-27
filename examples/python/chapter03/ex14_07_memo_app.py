"""
예제 14-7: 실습 — 메모장 앱 점진적 개발
==========================================
4단계에 걸쳐 메모장 앱을 점진적으로 개발합니다.
각 단계는 독립적으로 동작하는 '완성된' 버전입니다.

Stage 1: 메모 생성 (create)
Stage 2: 메모 목록 (list)
Stage 3: 메모 검색 (search)
Stage 4: 메모 삭제 (delete)

이 예제는 4단계를 모두 포함한 최종 버전입니다.
각 단계별 진화 과정은 주석으로 표시되어 있습니다.
"""

import json
import os
from datetime import datetime

MEMO_FILE = "memos.json"


# ── Stage 1: 메모 생성 ──────────────────────────
# 첫 번째 바이브 코딩 요청:
# "간단한 메모를 생성하는 프로그램을 만들어줘.
#  제목과 내용을 입력받아 저장해줘."

def create_memo(memos):
    """새 메모를 생성합니다. [Stage 1에서 추가]"""
    title = input("  제목: ").strip()
    if not title:
        print("  오류: 제목을 입력해주세요.")
        return

    content = input("  내용: ").strip()

    memo = {
        "id": len(memos) + 1,
        "title": title,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    memos.append(memo)
    save_memos(memos)
    print(f"  메모 '{title}' 생성 완료! (ID: {memo['id']})")


# ── Stage 2: 메모 목록 ──────────────────────────
# 두 번째 바이브 코딩 요청:
# "저장된 메모를 목록으로 보여주는 기능을 추가해줘.
#  번호, 제목, 생성 날짜가 보이면 좋겠어."

def list_memos(memos):
    """모든 메모를 목록으로 표시합니다. [Stage 2에서 추가]"""
    if not memos:
        print("  저장된 메모가 없습니다.")
        return

    print(f"\n  {'ID':<4} {'제목':<20} {'생성일':<16}")
    print(f"  {'-'*4} {'-'*20} {'-'*16}")
    for memo in memos:
        print(f"  {memo['id']:<4} {memo['title']:<20} {memo['created_at']:<16}")
    print(f"\n  총 {len(memos)}개의 메모")


# ── Stage 3: 메모 검색 ──────────────────────────
# 세 번째 바이브 코딩 요청:
# "메모를 키워드로 검색하는 기능을 추가해줘.
#  제목과 내용에서 모두 검색되면 좋겠어."

def search_memos(memos):
    """키워드로 메모를 검색합니다. [Stage 3에서 추가]"""
    keyword = input("  검색어: ").strip()
    if not keyword:
        print("  오류: 검색어를 입력해주세요.")
        return

    results = [
        m for m in memos
        if keyword.lower() in m["title"].lower()
        or keyword.lower() in m["content"].lower()
    ]

    if not results:
        print(f"  '{keyword}'에 대한 검색 결과가 없습니다.")
        return

    print(f"\n  '{keyword}' 검색 결과 ({len(results)}건):")
    print(f"  {'-'*40}")
    for memo in results:
        print(f"  [{memo['id']}] {memo['title']}")
        print(f"       {memo['content'][:50]}...")
        print()


# ── Stage 4: 메모 삭제 ──────────────────────────
# 네 번째 바이브 코딩 요청:
# "메모를 ID로 삭제하는 기능을 추가해줘.
#  삭제 전에 확인 질문을 해줘."

def delete_memo(memos):
    """메모를 삭제합니다. [Stage 4에서 추가]"""
    try:
        memo_id = int(input("  삭제할 메모 ID: "))
    except ValueError:
        print("  오류: 숫자를 입력해주세요.")
        return

    target = None
    for memo in memos:
        if memo["id"] == memo_id:
            target = memo
            break

    if target is None:
        print(f"  오류: ID {memo_id}번 메모를 찾을 수 없습니다.")
        return

    print(f"  제목: {target['title']}")
    print(f"  내용: {target['content']}")
    confirm = input("  정말 삭제하시겠습니까? (y/n): ").strip().lower()

    if confirm == "y":
        memos.remove(target)
        save_memos(memos)
        print(f"  메모 '{target['title']}' 삭제 완료!")
    else:
        print("  삭제를 취소했습니다.")


# ── 파일 저장/불러오기 유틸리티 ──────────────────

def load_memos():
    """파일에서 메모를 불러옵니다."""
    if os.path.exists(MEMO_FILE):
        with open(MEMO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memos(memos):
    """메모를 파일로 저장합니다."""
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)


# ── 메인 프로그램 ──────────────────────────────

def main():
    print("=" * 45)
    print("  메모장 v1.0 — 점진적 개발 완성본")
    print("=" * 45)
    print("  명령어: create | list | search | delete | quit")
    print()

    memos = load_memos()
    if memos:
        print(f"  ({len(memos)}개의 저장된 메모를 불러왔습니다)\n")

    commands = {
        "create": ("메모 생성", create_memo),
        "list": ("메모 목록", list_memos),
        "search": ("메모 검색", search_memos),
        "delete": ("메모 삭제", delete_memo),
    }

    while True:
        command = input("[메모장] > ").strip().lower()

        if command == "quit":
            print(f"\n  메모장을 종료합니다. (총 {len(memos)}개 메모)")
            break
        elif command in commands:
            name, func = commands[command]
            print(f"\n  --- {name} ---")
            func(memos)
            print()
        elif command == "":
            continue
        else:
            print(f"  알 수 없는 명령어: '{command}'")
            print("  사용 가능: create | list | search | delete | quit\n")


if __name__ == "__main__":
    main()
