"""
예제 25-10: search 명령어 구현
- 키워드로 할일을 검색하는 기능을 구현합니다.
- 제목, 태그에서 대소문자 구분 없이 검색합니다.
- 검색 결과를 하이라이트하여 표시합니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
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


# ANSI 색상 코드
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BG_YELLOW = "\033[43m"
BLACK = "\033[30m"


def highlight_text(text: str, keyword: str, use_color: bool = True) -> str:
    """
    텍스트에서 키워드를 하이라이트합니다.
    대소문자 구분 없이 모든 매칭 부분을 강조합니다.
    """
    if not keyword:
        return text

    # 대소문자 구분 없이 매칭 위치 찾기
    text_lower = text.lower()
    keyword_lower = keyword.lower()

    if keyword_lower not in text_lower:
        return text

    result = []
    pos = 0

    while pos < len(text):
        idx = text_lower.find(keyword_lower, pos)
        if idx == -1:
            result.append(text[pos:])
            break

        # 매칭 전 텍스트
        result.append(text[pos:idx])

        # 매칭된 텍스트 (원본 대소문자 유지)
        matched = text[idx:idx + len(keyword)]
        if use_color:
            result.append(f"{BG_YELLOW}{BLACK}{BOLD}{matched}{RESET}")
        else:
            result.append(f"[{matched}]")

        pos = idx + len(keyword)

    return "".join(result)


def search_todos(
    todos: list[Todo],
    keyword: str,
    search_in_tags: bool = True,
    include_completed: bool = True,
) -> list[tuple[Todo, list[str]]]:
    """
    할일을 키워드로 검색합니다.

    Args:
        todos: 검색할 할일 목록
        keyword: 검색 키워드
        search_in_tags: 태그에서도 검색할지 여부
        include_completed: 완료된 항목도 포함할지 여부

    Returns:
        (할일, 매칭된 필드 목록) 튜플의 리스트
    """
    if not keyword or not keyword.strip():
        return [(todo, ["전체"]) for todo in todos]

    keyword_lower = keyword.lower().strip()
    results: list[tuple[Todo, list[str]]] = []

    for todo in todos:
        # 완료된 항목 필터링
        if not include_completed and todo.completed:
            continue

        matched_fields: list[str] = []

        # 제목 검색
        if keyword_lower in todo.title.lower():
            matched_fields.append("제목")

        # 태그 검색
        if search_in_tags and todo.tags:
            for tag in todo.tags:
                if keyword_lower in tag.lower():
                    matched_fields.append(f"태그({tag})")
                    break  # 한 태그에서만 매칭되면 충분

        if matched_fields:
            results.append((todo, matched_fields))

    return results


def display_search_results(
    results: list[tuple[Todo, list[str]]],
    keyword: str,
    use_color: bool = True,
) -> None:
    """검색 결과를 포맷팅하여 출력합니다."""

    if not results:
        msg = f"'{keyword}'에 대한 검색 결과가 없습니다."
        if use_color:
            print(f"  {YELLOW}{msg}{RESET}")
        else:
            print(f"  {msg}")
        return

    # 헤더
    count_str = f"{len(results)}개"
    if use_color:
        print(f"  '{BOLD}{keyword}{RESET}' 검색 결과: {GREEN}{count_str}{RESET}")
    else:
        print(f"  '{keyword}' 검색 결과: {count_str}")
    print(f"  {'─' * 50}")

    for todo, matched_fields in results:
        # 상태 표시
        if todo.completed:
            status = f"{GREEN}[완료]{RESET}" if use_color else "[완료]"
        else:
            status = "[미완료]"

        # 제목에 하이라이트 적용
        title = highlight_text(todo.title, keyword, use_color)

        # 매칭 필드 표시
        fields = ", ".join(matched_fields)
        if use_color:
            fields_str = f"{CYAN}({fields}){RESET}"
        else:
            fields_str = f"({fields})"

        # 태그 표시
        tag_str = ""
        if todo.tags:
            highlighted_tags = []
            for tag in todo.tags:
                h_tag = highlight_text(tag, keyword, use_color)
                highlighted_tags.append(f"#{h_tag}")
            if use_color:
                tag_str = f" {CYAN}{' '.join(highlighted_tags)}{RESET}"
            else:
                tag_str = f" {' '.join(highlighted_tags)}"

        print(f"  #{todo.id} {status} {title}{tag_str} {fields_str}")

    print(f"  {'─' * 50}")


if __name__ == "__main__":
    print("=" * 55)
    print("CLI 할일 관리 앱 - search 명령어 데모")
    print("=" * 55)
    print()

    # 데모 데이터 생성
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    todos = [
        Todo(id=1, title="우유 사기", priority=Priority.LOW,
             completed=True, tags=["장보기", "마트"]),
        Todo(id=2, title="보고서 작성하기", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "급함"]),
        Todo(id=3, title="운동하기 - 헬스장", priority=Priority.MEDIUM,
             tags=["건강", "루틴"]),
        Todo(id=4, title="이메일 답장 보내기", priority=Priority.HIGH,
             due_date=tomorrow, tags=["업무", "이메일"]),
        Todo(id=5, title="책 읽기 - 파이썬 기초", priority=Priority.LOW,
             due_date=next_week, tags=["공부", "파이썬"]),
        Todo(id=6, title="팀 회의 자료 작성", priority=Priority.HIGH,
             tags=["업무", "회의"]),
        Todo(id=7, title="저녁 장보기", priority=Priority.MEDIUM,
             tags=["장보기"]),
        Todo(id=8, title="파이썬 프로젝트 코드 리뷰", priority=Priority.MEDIUM,
             completed=True, tags=["업무", "파이썬"]),
    ]

    # 1. 제목 검색
    print("--- 1. 제목에서 '작성' 검색 ---")
    print(">>> todo search 작성")
    results = search_todos(todos, "작성")
    display_search_results(results, "작성")
    print()

    # 2. 태그 검색
    print("--- 2. 태그에서 '업무' 검색 ---")
    print(">>> todo search 업무")
    results = search_todos(todos, "업무")
    display_search_results(results, "업무")
    print()

    # 3. 제목+태그 복합 검색
    print("--- 3. '파이썬' 검색 (제목+태그) ---")
    print(">>> todo search 파이썬")
    results = search_todos(todos, "파이썬")
    display_search_results(results, "파이썬")
    print()

    # 4. '장보기' 검색
    print("--- 4. '장보기' 검색 ---")
    print(">>> todo search 장보기")
    results = search_todos(todos, "장보기")
    display_search_results(results, "장보기")
    print()

    # 5. 미완료만 검색
    print("--- 5. '파이썬' 검색 (미완료만) ---")
    print(">>> todo search 파이썬 --pending")
    results = search_todos(todos, "파이썬", include_completed=False)
    display_search_results(results, "파이썬")
    print()

    # 6. 검색 결과 없음
    print("--- 6. 검색 결과 없음 ---")
    print(">>> todo search 여행")
    results = search_todos(todos, "여행")
    display_search_results(results, "여행")
    print()

    # 7. 색상 없는 출력
    print("--- 7. 색상 없는 출력 ('업무' 검색) ---")
    results = search_todos(todos, "업무")
    display_search_results(results, "업무", use_color=False)
