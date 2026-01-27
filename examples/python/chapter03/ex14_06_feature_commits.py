"""
예제 14-6: 기능별 커밋 만들기
================================
각 기능을 추가할 때마다 커밋하는 워크플로우를 보여줍니다.
바이브 코딩에서 "한 기능 = 한 커밋" 원칙은 매우 중요합니다.

AI에게 새 기능을 요청할 때마다 커밋하면,
문제가 생겼을 때 정확히 어느 시점으로 돌아갈지 알 수 있습니다.
"""


def show_commit_history():
    """기능별 커밋 히스토리를 시뮬레이션합니다."""

    commits = [
        {
            "hash": "a1b2c3d",
            "message": "feat: MVP 계산기 - 덧셈 기능 구현",
            "description": "v0.1 — add() 함수, 기본 입출력",
            "files_changed": ["calculator.py"],
            "prompt": "덧셈만 되는 간단한 계산기를 만들어줘",
        },
        {
            "hash": "e4f5g6h",
            "message": "feat: 사칙연산 추가 (뺄셈, 곱셈, 나눗셈)",
            "description": "v0.2 — subtract(), multiply(), divide() 추가",
            "files_changed": ["calculator.py"],
            "prompt": "계산기에 뺄셈, 곱셈, 나눗셈도 추가해줘",
        },
        {
            "hash": "i7j8k9l",
            "message": "feat: 계산 히스토리 기능 추가",
            "description": "v0.3 — history 리스트, 반복 계산 루프",
            "files_changed": ["calculator.py"],
            "prompt": "계산 기록을 저장하고 볼 수 있게 해줘",
        },
        {
            "hash": "m0n1o2p",
            "message": "feat: 히스토리 파일 저장/불러오기",
            "description": "v0.4 — JSON 파일 저장, 타임스탬프 추가",
            "files_changed": ["calculator.py"],
            "prompt": "계산 기록을 파일로 저장하고, 다시 시작할 때 불러와줘",
        },
        {
            "hash": "q3r4s5t",
            "message": "fix: 0으로 나누기 오류 처리 개선",
            "description": "버그 수정 — ZeroDivisionError 예외 처리",
            "files_changed": ["calculator.py"],
            "prompt": "0으로 나눌 때 에러 대신 친절한 메시지가 나오게 해줘",
        },
        {
            "hash": "u6v7w8x",
            "message": "docs: README.md 추가",
            "description": "문서 — 프로젝트 설명, 사용법, 설치 방법",
            "files_changed": ["README.md"],
            "prompt": "이 프로젝트의 README를 작성해줘",
        },
    ]

    # --- 커밋 히스토리 표시 (git log --oneline 스타일) ---
    print("=" * 60)
    print("  기능별 커밋 히스토리")
    print("  (git log --oneline 스타일)")
    print("=" * 60)

    for commit in commits:
        print(f"  {commit['hash']} {commit['message']}")

    # --- 상세 히스토리 ---
    print(f"\n{'='*60}")
    print("  상세 커밋 히스토리")
    print(f"{'='*60}")

    for i, commit in enumerate(commits, 1):
        print(f"\n  [{i}] {commit['hash']} — {commit['message']}")
        print(f"      설명: {commit['description']}")
        print(f"      변경 파일: {', '.join(commit['files_changed'])}")
        print(f"      AI 프롬프트: \"{commit['prompt']}\"")

    # --- 커밋 메시지 규칙 ---
    print(f"\n{'='*60}")
    print("  커밋 메시지 규칙 (Conventional Commits)")
    print(f"{'='*60}")

    conventions = [
        ("feat:", "새 기능 추가", "feat: 사칙연산 추가"),
        ("fix:", "버그 수정", "fix: 0으로 나누기 오류 처리"),
        ("docs:", "문서 변경", "docs: README 추가"),
        ("refactor:", "리팩토링", "refactor: 함수 분리"),
        ("test:", "테스트 추가", "test: 사칙연산 단위 테스트"),
        ("style:", "코드 스타일", "style: PEP8 포맷 적용"),
    ]

    for prefix, desc, example in conventions:
        print(f"  {prefix:<12} {desc:<16} 예) {example}")

    print(f"\n  핵심 원칙:")
    print(f"  - 한 커밋 = 하나의 논리적 변경")
    print(f"  - 동작하는 상태에서만 커밋")
    print(f"  - 메시지는 '무엇을 했는지' 명확하게")


if __name__ == "__main__":
    show_commit_history()
