"""
예제 14-5: git init과 첫 커밋 시뮬레이션
==========================================
Git의 기본 흐름을 보여주는 교육용 스크립트입니다.
실제 git 명령어를 실행하지 않고, 각 단계에서
어떤 명령어를 사용하는지 설명합니다.

바이브 코딩에서 Git은 "안전망" 역할을 합니다.
AI가 생성한 코드가 마음에 들면 커밋하고,
문제가 생기면 이전 상태로 되돌릴 수 있습니다.
"""


def show_git_workflow():
    """Git 초기화부터 첫 커밋까지의 워크플로우를 보여줍니다."""

    steps = [
        {
            "title": "1단계: 프로젝트 폴더 생성",
            "commands": [
                "mkdir my-calculator",
                "cd my-calculator",
            ],
            "explanation": "새 프로젝트를 위한 빈 폴더를 만듭니다.",
        },
        {
            "title": "2단계: Git 저장소 초기화",
            "commands": [
                "git init",
            ],
            "explanation": (
                "현재 폴더를 Git 저장소로 만듭니다.\n"
                "    → .git 폴더가 생성되어 버전 관리가 시작됩니다."
            ),
        },
        {
            "title": "3단계: .gitignore 파일 생성",
            "commands": [
                'echo "__pycache__/" > .gitignore',
                'echo "*.pyc" >> .gitignore',
                'echo ".env" >> .gitignore',
            ],
            "explanation": (
                "추적하지 않을 파일 패턴을 지정합니다.\n"
                "    → 캐시 파일, 환경 변수 파일 등을 제외합니다."
            ),
        },
        {
            "title": "4단계: MVP 코드 작성",
            "commands": [
                "# AI에게 요청: 'MVP 계산기를 만들어줘. 덧셈만 되면 돼.'",
                "# → calculator.py 파일이 생성됨",
            ],
            "explanation": (
                "바이브 코딩으로 첫 번째 코드를 생성합니다.\n"
                "    → 가장 단순한 버전(MVP)부터 시작합니다."
            ),
        },
        {
            "title": "5단계: 변경 사항 확인",
            "commands": [
                "git status",
            ],
            "explanation": (
                "어떤 파일이 변경되었는지 확인합니다.\n"
                "    → 새 파일: .gitignore, calculator.py"
            ),
        },
        {
            "title": "6단계: 스테이징 (변경 사항 준비)",
            "commands": [
                "git add .",
            ],
            "explanation": (
                "모든 변경 사항을 커밋 준비 상태로 만듭니다.\n"
                "    → 또는 git add calculator.py 처럼 개별 파일 지정 가능"
            ),
        },
        {
            "title": "7단계: 첫 커밋!",
            "commands": [
                'git commit -m "feat: MVP 계산기 - 덧셈 기능 구현"',
            ],
            "explanation": (
                "현재 상태를 저장합니다. 이제 언제든 이 시점으로\n"
                "    되돌아올 수 있습니다!"
            ),
        },
        {
            "title": "8단계: 커밋 확인",
            "commands": [
                "git log --oneline",
            ],
            "explanation": (
                "커밋 이력을 확인합니다.\n"
                '    → abc1234 feat: MVP 계산기 - 덧셈 기능 구현'
            ),
        },
    ]

    print("=" * 55)
    print("  Git 초기화 & 첫 커밋 워크플로우")
    print("  (바이브 코딩의 안전망 만들기)")
    print("=" * 55)

    for step in steps:
        print(f"\n--- {step['title']} ---")
        print(f"  설명: {step['explanation']}")
        print(f"  명령어:")
        for cmd in step["commands"]:
            print(f"    $ {cmd}")

    print("\n" + "=" * 55)
    print("  첫 커밋 완료! 이제 안전하게 코드를 발전시킬 수 있습니다.")
    print("=" * 55)


if __name__ == "__main__":
    show_git_workflow()
