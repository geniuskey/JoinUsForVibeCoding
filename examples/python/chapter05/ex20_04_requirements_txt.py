"""
예제 20-04: requirements.txt 생성 및 파싱
프로젝트 의존성 관리의 핵심인 requirements.txt 파일을
생성하고, 읽고, 분석하는 방법을 배웁니다.
"""

import os
import tempfile
import re


def create_requirements_file(filepath, packages):
    """requirements.txt 파일을 생성합니다."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 프로젝트 의존성 목록\n")
        f.write("# pip install -r requirements.txt 명령으로 설치합니다\n")
        f.write("#\n")
        f.write(f"# 총 {len(packages)}개 패키지\n")
        f.write(f"# 생성일: 자동 생성됨\n\n")

        for pkg in packages:
            if "comment" in pkg:
                f.write(f"\n# {pkg['comment']}\n")
            f.write(f"{pkg['line']}\n")


def parse_requirements(filepath):
    """requirements.txt 파일을 파싱하여 패키지 정보를 추출합니다."""
    packages = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # 빈 줄이나 주석은 건너뛰기
            if not line or line.startswith("#"):
                continue

            # 인라인 주석 제거
            if " #" in line:
                line = line.split(" #")[0].strip()

            # 패키지 이름과 버전 조건 파싱
            # 지원 형식: pkg==1.0, pkg>=1.0, pkg~=1.0, pkg!=1.0, pkg 등
            match = re.match(
                r'^([a-zA-Z0-9_-]+)\s*(==|>=|<=|!=|~=|>|<)?\s*(.+)?$',
                line
            )

            if match:
                name = match.group(1)
                operator = match.group(2) or ""
                version = match.group(3) or ""
                packages.append({
                    "line_num": line_num,
                    "name": name,
                    "operator": operator,
                    "version": version.strip(),
                    "raw": line,
                })

    return packages


def analyze_requirements(packages):
    """파싱된 패키지 목록을 분석합니다."""
    analysis = {
        "total": len(packages),
        "pinned": 0,       # 정확한 버전 고정 (==)
        "minimum": 0,      # 최소 버전 (>=)
        "compatible": 0,   # 호환 버전 (~=)
        "unpinned": 0,     # 버전 미지정
        "other": 0,        # 기타
    }

    for pkg in packages:
        if pkg["operator"] == "==":
            analysis["pinned"] += 1
        elif pkg["operator"] == ">=":
            analysis["minimum"] += 1
        elif pkg["operator"] == "~=":
            analysis["compatible"] += 1
        elif pkg["operator"] == "":
            analysis["unpinned"] += 1
        else:
            analysis["other"] += 1

    return analysis


def generate_dev_requirements(base_packages):
    """개발용 requirements-dev.txt에 추가할 패키지 목록을 반환합니다."""
    dev_packages = [
        {"line": "-r requirements.txt", "comment": "기본 의존성 포함"},
        {"line": "pytest==7.4.0", "comment": "테스트 도구"},
        {"line": "pytest-cov>=4.1.0"},
        {"line": "black==23.7.0", "comment": "코드 포맷터"},
        {"line": "flake8>=6.0.0"},
        {"line": "mypy>=1.5.0", "comment": "타입 검사"},
    ]
    return dev_packages


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-04: requirements.txt 생성 및 파싱")
    print("=" * 60)
    print()

    # 임시 디렉토리에서 작업
    temp_dir = tempfile.mkdtemp()
    req_file = os.path.join(temp_dir, "requirements.txt")
    dev_req_file = os.path.join(temp_dir, "requirements-dev.txt")

    try:
        # --- 1단계: requirements.txt 생성 ---
        print("--- 1단계: requirements.txt 생성 ---")
        print()

        packages = [
            {"line": "flask==2.3.3", "comment": "웹 프레임워크"},
            {"line": "flask-cors>=4.0.0"},
            {"line": "sqlalchemy~=2.0.20", "comment": "데이터베이스 ORM"},
            {"line": "alembic>=1.11.0"},
            {"line": "pydantic==2.3.0", "comment": "데이터 검증"},
            {"line": "python-dotenv>=1.0.0", "comment": "환경 변수 관리"},
            {"line": "requests>=2.31.0", "comment": "HTTP 클라이언트"},
            {"line": "celery>=5.3.0", "comment": "비동기 작업 큐"},
            {"line": "redis>=5.0.0"},
            {"line": "gunicorn>=21.2.0", "comment": "WSGI 서버 (배포용)"},
        ]

        create_requirements_file(req_file, packages)
        print(f"  파일 생성 완료: requirements.txt")
        print()

        # 생성된 파일 내용 출력
        print("  생성된 파일 내용:")
        print("  " + "-" * 45)
        with open(req_file, "r", encoding="utf-8") as f:
            for line in f:
                print(f"  {line}", end="")
        print()
        print("  " + "-" * 45)
        print()

        # --- 2단계: requirements.txt 파싱 ---
        print("--- 2단계: requirements.txt 파싱 ---")
        print()

        parsed = parse_requirements(req_file)
        print(f"  파싱된 패키지 목록 ({len(parsed)}개):")
        print(f"  {'패키지명':<20s} {'조건':<5s} {'버전':<12s} {'원본'}")
        print(f"  {'-'*20} {'-'*5} {'-'*12} {'-'*25}")
        for pkg in parsed:
            print(f"  {pkg['name']:<20s} {pkg['operator']:<5s} {pkg['version']:<12s} {pkg['raw']}")
        print()

        # --- 3단계: 의존성 분석 ---
        print("--- 3단계: 의존성 분석 ---")
        print()

        analysis = analyze_requirements(parsed)
        print(f"  총 패키지 수: {analysis['total']}개")
        print(f"  버전 고정 (==): {analysis['pinned']}개  - 정확한 버전으로 재현 가능")
        print(f"  최소 버전 (>=): {analysis['minimum']}개  - 최소 호환 버전 보장")
        print(f"  호환 버전 (~=): {analysis['compatible']}개  - 마이너 버전 업데이트 허용")
        print(f"  버전 미지정:    {analysis['unpinned']}개  - 최신 버전 설치")
        print()

        # 권장사항
        if analysis["unpinned"] > 0:
            print("  주의: 버전 미지정 패키지가 있습니다.")
            print("  배포 환경에서는 모든 패키지 버전을 고정하는 것을 권장합니다.")
        print()

        # --- 4단계: requirements-dev.txt 생성 ---
        print("--- 4단계: requirements-dev.txt 생성 ---")
        print()

        dev_packages = generate_dev_requirements(packages)
        create_requirements_file(dev_req_file, dev_packages)

        print("  개발용 의존성 파일 생성 완료: requirements-dev.txt")
        print()
        print("  생성된 파일 내용:")
        print("  " + "-" * 45)
        with open(dev_req_file, "r", encoding="utf-8") as f:
            for line in f:
                print(f"  {line}", end="")
        print()
        print("  " + "-" * 45)
        print()

        # --- 사용법 안내 ---
        print("--- requirements.txt 활용 가이드 ---")
        print()
        print("  설치: pip install -r requirements.txt")
        print("  개발: pip install -r requirements-dev.txt")
        print("  생성: pip freeze > requirements.txt")
        print("  확인: pip list")
        print()

        print("requirements.txt 예제를 성공적으로 실행했습니다!")

    finally:
        # 임시 파일 정리
        for f in [req_file, dev_req_file]:
            if os.path.exists(f):
                os.remove(f)
        os.rmdir(temp_dir)
        print("(임시 파일 정리 완료)")
