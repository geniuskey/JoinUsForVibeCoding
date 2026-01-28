"""
예제 27-01: 데이터 대시보드 프로젝트 디렉토리 구조 생성

데이터 대시보드 CLI 프로젝트를 위한 디렉토리 구조를 자동으로 생성합니다.
프로젝트에 필요한 폴더와 초기 파일들을 체계적으로 만들어줍니다.
"""

import os
import datetime


def create_project_structure(base_dir):
    """데이터 대시보드 프로젝트의 디렉토리 구조를 생성합니다."""

    # 프로젝트 디렉토리 구조 정의
    directories = [
        "data/raw",          # 원본 데이터 저장
        "data/processed",    # 정제된 데이터 저장
        "data/cache",        # API 캐시 데이터
        "collectors",        # 데이터 수집 모듈
        "processors",        # 데이터 처리 모듈
        "analyzers",         # 데이터 분석 모듈
        "visualizers",       # 시각화 모듈
        "reports",           # 보고서 출력 디렉토리
        "config",            # 설정 파일
        "tests",             # 테스트 코드
    ]

    # 초기 파일 정의 (파일 경로: 파일 내용)
    initial_files = {
        "config/settings.py": '''"""대시보드 설정 파일"""

# 데이터 소스 설정
DATA_DIR = "data"
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CACHE_DIR = "data/cache"

# 보고서 설정
REPORT_DIR = "reports"
REPORT_FORMAT = "markdown"  # markdown, text, html

# 대시보드 설정
REFRESH_INTERVAL = 60  # 초 단위
MAX_ROWS_DISPLAY = 20  # 테이블 최대 표시 행 수

# 차트 설정
CHART_WIDTH = 50  # 텍스트 차트 너비
CHART_FILL_CHAR = "█"  # 차트 채우기 문자
''',
        "collectors/__init__.py": '"""데이터 수집 모듈"""\n',
        "processors/__init__.py": '"""데이터 처리 모듈"""\n',
        "analyzers/__init__.py": '"""데이터 분석 모듈"""\n',
        "visualizers/__init__.py": '"""시각화 모듈"""\n',
        "tests/__init__.py": '"""테스트 모듈"""\n',
        "README.md": f"""# 데이터 대시보드 CLI

AI와 함께 만드는 터미널 기반 데이터 대시보드

## 프로젝트 구조

```
dashboard-cli/
├── data/           # 데이터 저장소
│   ├── raw/        # 원본 데이터
│   ├── processed/  # 정제된 데이터
│   └── cache/      # API 캐시
├── collectors/     # 데이터 수집 모듈
├── processors/     # 데이터 처리 모듈
├── analyzers/      # 데이터 분석 모듈
├── visualizers/    # 시각화 모듈
├── reports/        # 보고서 출력
├── config/         # 설정 파일
└── tests/          # 테스트 코드
```

## 사용법

```bash
python dashboard.py --help
```

생성일: {datetime.datetime.now().strftime('%Y-%m-%d')}
""",
        "dashboard.py": '''"""데이터 대시보드 CLI 메인 모듈"""

import sys


def main():
    """대시보드 메인 실행 함수"""
    print("=" * 50)
    print("  데이터 대시보드 CLI v1.0")
    print("=" * 50)
    print()
    print("사용 가능한 명령어:")
    print("  collect  - 데이터 수집")
    print("  process  - 데이터 정제 및 변환")
    print("  analyze  - 데이터 분석")
    print("  report   - 보고서 생성")
    print("  dash     - 대시보드 실행")
    print()


if __name__ == "__main__":
    main()
''',
    }

    print("=" * 60)
    print("  데이터 대시보드 프로젝트 구조 생성기")
    print("=" * 60)
    print()
    print(f"프로젝트 경로: {base_dir}")
    print()

    # 디렉토리 생성
    print("📁 디렉토리 생성 중...")
    created_dirs = 0
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"  [생성] {directory}/")
            created_dirs += 1
        else:
            print(f"  [존재] {directory}/")

    print()

    # 파일 생성
    print("📄 초기 파일 생성 중...")
    created_files = 0
    for file_path, content in initial_files.items():
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [생성] {file_path}")
            created_files += 1
        else:
            print(f"  [존재] {file_path}")

    print()

    # 결과 요약
    print("-" * 60)
    print(f"생성 완료!")
    print(f"  - 디렉토리: {created_dirs}개 새로 생성")
    print(f"  - 파일: {created_files}개 새로 생성")
    print()

    # 최종 디렉토리 트리 출력
    print("최종 프로젝트 구조:")
    print_tree(base_dir)


def print_tree(directory, prefix="", max_depth=3, current_depth=0):
    """디렉토리 트리를 텍스트로 출력합니다."""
    if current_depth >= max_depth:
        return

    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return

    # 숨김 파일 제외, __pycache__ 제외
    entries = [e for e in entries if not e.startswith(".") and e != "__pycache__"]

    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "

        if os.path.isdir(path):
            print(f"{prefix}{connector}{entry}/")
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension, max_depth, current_depth + 1)
        else:
            print(f"{prefix}{connector}{entry}")


if __name__ == "__main__":
    # /tmp 디렉토리에 프로젝트 구조 생성
    project_dir = "/tmp/dashboard-cli"

    # 기존 디렉토리가 있으면 알림
    if os.path.exists(project_dir):
        print(f"기존 프로젝트 디렉토리가 발견되었습니다: {project_dir}")
        print("기존 파일을 유지하면서 누락된 구조를 추가합니다.")
        print()

    create_project_structure(project_dir)
