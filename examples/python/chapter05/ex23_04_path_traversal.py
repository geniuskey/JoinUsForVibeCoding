"""
예제 23-04: 경로 순회(Path Traversal) 방지
- pathlib으로 안전한 경로 처리
- ../를 이용한 디렉토리 탈출 공격 방지

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
주의: 취약한 코드는 절대 실제 서비스에 사용하지 마세요!
"""

import os
import tempfile
from pathlib import Path


# ============================================================
# 테스트 환경 설정
# ============================================================

def setup_test_environment() -> str:
    """테스트용 디렉토리 구조 생성"""
    base_dir = tempfile.mkdtemp(prefix="secure_app_")

    # 허용된 uploads 디렉토리
    uploads_dir = os.path.join(base_dir, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # 테스트 파일 생성
    with open(os.path.join(uploads_dir, "photo.txt"), "w") as f:
        f.write("이것은 업로드된 파일입니다.")

    with open(os.path.join(uploads_dir, "document.txt"), "w") as f:
        f.write("이것은 문서 파일입니다.")

    # 비밀 파일 (uploads 밖)
    with open(os.path.join(base_dir, "secret_config.txt"), "w") as f:
        f.write("DB_PASSWORD=super_secret_123")

    return base_dir


def cleanup_test_environment(base_dir: str) -> None:
    """테스트 환경 정리"""
    import shutil
    shutil.rmtree(base_dir, ignore_errors=True)


# ============================================================
# ❌ 취약한 코드: 경로 순회 공격에 취약
# ============================================================

def vulnerable_read_file(base_dir: str, filename: str) -> str:
    """
    ❌ 취약: 파일명을 검증 없이 경로에 연결
    공격자가 ../를 사용하여 허용 디렉토리 밖의 파일에 접근 가능

    예: filename = "../../etc/passwd"
    """
    uploads_dir = os.path.join(base_dir, "uploads")

    # ❌ 단순 문자열 연결 - 경로 순회에 취약!
    filepath = os.path.join(uploads_dir, filename)
    print(f"  [요청 경로] {filepath}")

    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "(파일 없음)"
    except Exception as e:
        return f"(오류: {e})"


def vulnerable_save_file(base_dir: str, filename: str, content: str) -> str:
    """
    ❌ 취약: 파일 저장 시 경로를 검증하지 않음
    공격자가 ../를 사용하여 임의 위치에 파일 생성 가능
    """
    uploads_dir = os.path.join(base_dir, "uploads")

    # ❌ 경로 검증 없이 저장
    filepath = os.path.join(uploads_dir, filename)
    print(f"  [저장 경로] {filepath}")

    # 실제로 저장하지는 않음 (시연 목적)
    return f"파일이 {filepath}에 저장됩니다 (시뮬레이션)"


# ============================================================
# ✅ 안전한 코드: pathlib을 사용한 경로 순회 방지
# ============================================================

def safe_read_file(base_dir: str, filename: str) -> str:
    """
    ✅ 안전: pathlib으로 경로를 정규화하고 허용 범위 확인
    - resolve()로 실제 절대 경로 계산
    - 허용된 디렉토리 내에 있는지 확인
    """
    uploads_dir = Path(base_dir) / "uploads"

    # 1. 요청된 경로 구성
    requested_path = (uploads_dir / filename).resolve()

    # 2. ✅ 핵심: 정규화된 경로가 허용된 디렉토리 안에 있는지 확인
    uploads_resolved = uploads_dir.resolve()

    print(f"  [허용 디렉토리] {uploads_resolved}")
    print(f"  [정규화된 경로] {requested_path}")

    # is_relative_to: Python 3.9+
    # 이전 버전에서는 str(requested_path).startswith(str(uploads_resolved)) 사용
    try:
        requested_path.relative_to(uploads_resolved)
    except ValueError:
        return "접근 거부: 허용된 디렉토리 밖의 파일입니다!"

    # 3. 파일 존재 확인
    if not requested_path.is_file():
        return "파일을 찾을 수 없습니다."

    # 4. 안전하게 파일 읽기
    return requested_path.read_text()


def safe_save_file(base_dir: str, filename: str, content: str) -> str:
    """
    ✅ 안전: 파일 저장 시 경로 검증
    """
    uploads_dir = Path(base_dir) / "uploads"

    # 1. 파일명에서 위험한 요소 제거
    safe_filename = sanitize_filename(filename)

    # 2. 경로 구성 및 검증
    target_path = (uploads_dir / safe_filename).resolve()
    uploads_resolved = uploads_dir.resolve()

    try:
        target_path.relative_to(uploads_resolved)
    except ValueError:
        return "접근 거부: 허용된 디렉토리 밖에 저장할 수 없습니다!"

    print(f"  [안전한 경로] {target_path}")
    return f"파일이 안전하게 {target_path}에 저장됩니다 (시뮬레이션)"


def sanitize_filename(filename: str) -> str:
    """
    ✅ 파일명 정제
    - 경로 구분자 제거
    - 숨김 파일(.으로 시작) 방지
    - 허용된 문자만 유지
    """
    import re

    # Path 컴포넌트에서 파일명만 추출
    name = Path(filename).name

    # 숨김 파일 방지
    name = name.lstrip(".")

    # 위험한 문자 제거 (영문, 숫자, 점, 하이픈, 밑줄만 허용)
    name = re.sub(r'[^a-zA-Z0-9가-힣._\-]', '_', name)

    # 빈 이름 방지
    if not name:
        name = "unnamed_file"

    return name


# ============================================================
# ✅ 추가: 안전한 디렉토리 목록 조회
# ============================================================

def safe_list_files(base_dir: str, subdir: str = "") -> list:
    """
    ✅ 안전: 허용된 디렉토리 내의 파일만 목록 표시
    """
    uploads_dir = Path(base_dir) / "uploads"

    target_dir = (uploads_dir / subdir).resolve()
    uploads_resolved = uploads_dir.resolve()

    try:
        target_dir.relative_to(uploads_resolved)
    except ValueError:
        print("  접근 거부: 허용된 디렉토리 밖입니다!")
        return []

    if not target_dir.is_dir():
        print("  디렉토리를 찾을 수 없습니다.")
        return []

    return [f.name for f in target_dir.iterdir() if f.is_file()]


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-04: 경로 순회(Path Traversal) 방지")
    print("=" * 60)

    base_dir = setup_test_environment()

    try:
        print(f"\n테스트 환경:")
        print(f"  기본 디렉토리: {base_dir}")
        print(f"  업로드 디렉토리: {base_dir}/uploads/")
        print(f"  허용된 파일: photo.txt, document.txt")
        print(f"  비밀 파일: {base_dir}/secret_config.txt (uploads 밖)")

        # --- ❌ 취약한 코드 시연 ---
        print("\n\n--- ❌ 취약한 코드: 경로 순회 공격 가능 ---")

        # 정상 접근
        print("\n[1] 정상 파일 접근:")
        content = vulnerable_read_file(base_dir, "photo.txt")
        print(f"  내용: {content}")

        # 경로 순회 공격
        print("\n[2] ❌ 경로 순회 공격 (../로 상위 디렉토리 접근):")
        content = vulnerable_read_file(base_dir, "../secret_config.txt")
        print(f"  내용: {content}")
        print("  -> 업로드 디렉토리 밖의 비밀 파일에 접근 성공!")

        # 파일 저장 공격
        print("\n[3] ❌ 경로 순회로 임의 위치에 파일 저장:")
        result = vulnerable_save_file(base_dir, "../evil.txt", "악성 내용")
        print(f"  결과: {result}")
        print("  -> 업로드 디렉토리 밖에 파일을 생성할 수 있습니다!")

        # --- ✅ 안전한 코드 시연 ---
        print("\n\n--- ✅ 안전한 코드: pathlib으로 경로 순회 차단 ---")

        # 정상 접근
        print("\n[1] 정상 파일 접근:")
        content = safe_read_file(base_dir, "photo.txt")
        print(f"  내용: {content}")

        # 같은 공격 시도 -> 차단됨
        print("\n[2] ✅ 같은 경로 순회 공격 시도 -> 차단:")
        content = safe_read_file(base_dir, "../secret_config.txt")
        print(f"  결과: {content}")

        # 더 교묘한 공격 시도 -> 차단됨
        print("\n[3] ✅ 인코딩을 이용한 공격 시도 -> 차단:")
        content = safe_read_file(base_dir, "..%2F..%2Fetc%2Fpasswd")
        print(f"  결과: {content}")

        # 안전한 파일 저장
        print("\n[4] ✅ 경로 순회 저장 시도 -> 차단:")
        result = safe_save_file(base_dir, "../evil.txt", "악성 내용")
        print(f"  결과: {result}")

        # 파일명 정제 시연
        print("\n\n--- ✅ 파일명 정제(Sanitization) ---")
        test_filenames = [
            "normal_file.txt",
            "../../../etc/passwd",
            ".hidden_file",
            "file with spaces.txt",
            "<script>alert.js",
            "hello/world.txt",
        ]

        for original in test_filenames:
            safe = sanitize_filename(original)
            print(f"  '{original}' -> '{safe}'")

        # 안전한 디렉토리 목록
        print("\n\n--- ✅ 안전한 디렉토리 목록 조회 ---")
        print("\n[1] 정상 조회:")
        files = safe_list_files(base_dir)
        print(f"  파일 목록: {files}")

        print("\n[2] ✅ 상위 디렉토리 접근 시도 -> 차단:")
        files = safe_list_files(base_dir, "../")
        print(f"  결과: {files}")

    finally:
        cleanup_test_environment(base_dir)

    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. pathlib.resolve()로 경로를 정규화하세요")
    print("  2. 정규화된 경로가 허용 디렉토리 안에 있는지 확인하세요")
    print("  3. 파일명을 항상 정제(sanitize)하세요")
    print("  4. os.path.join()만으로는 안전하지 않습니다!")
    print("바이브 코딩 팁: AI에게 '경로 순회 방지 코드를 추가해줘'")
    print("              라고 요청하세요.")
    print("=" * 60)
