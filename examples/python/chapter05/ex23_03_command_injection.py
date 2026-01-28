"""
예제 23-03: 명령어 인젝션 취약 코드 vs 안전한 코드
- subprocess 모듈의 안전한 사용법
- shell=True의 위험성과 대안

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
주의: 취약한 코드는 절대 실제 서비스에 사용하지 마세요!
"""

import subprocess
import shlex
import os
import tempfile


# ============================================================
# ❌ 취약한 코드: shell=True와 문자열 결합
# ============================================================

def vulnerable_ping(host: str) -> str:
    """
    ❌ 취약: 사용자 입력을 셸 명령에 직접 삽입
    공격자가 host에 "; rm -rf /" 같은 명령을 넣을 수 있음

    예: host = "127.0.0.1; cat /etc/passwd"
    """
    # ❌ shell=True + 문자열 포맷팅 = 명령어 인젝션 취약!
    command = f"echo '[시뮬레이션] ping -c 1 {host}'"
    print(f"  [실행될 명령] {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def vulnerable_file_info(filename: str) -> str:
    """
    ❌ 취약: 파일명을 셸 명령에 직접 삽입
    """
    # ❌ os.system은 항상 셸을 통해 실행 - 매우 위험!
    command = f"echo '[시뮬레이션] file {filename}'"
    print(f"  [실행될 명령] {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def vulnerable_grep(pattern: str, filepath: str) -> str:
    """
    ❌ 취약: 검색 패턴을 셸 명령에 직접 삽입
    """
    # ❌ 사용자 입력이 셸 해석기를 거침
    command = f"echo '[시뮬레이션] grep {pattern} {filepath}'"
    print(f"  [실행될 명령] {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


# ============================================================
# ✅ 안전한 코드: 리스트 형태 인자와 shell=False
# ============================================================

def safe_ping(host: str) -> str:
    """
    ✅ 안전: subprocess에 리스트로 인자 전달 (shell=False 기본값)
    - 셸 해석 없이 직접 프로그램 실행
    - 인자가 개별 항목으로 전달되어 인젝션 불가
    """
    # 입력 검증: 호스트명에 허용된 문자만 포함
    import re
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        return f"오류: 올바른 호스트명이 아닙니다: '{host}'"

    # ✅ 리스트 형태로 인자 전달 - 셸 해석 없음
    command = ["echo", f"[시뮬레이션] ping -c 1 {host}"]
    print(f"  [실행될 명령] {command}")
    result = subprocess.run(command, capture_output=True, text=True,
                            timeout=10)  # ✅ 타임아웃 설정
    return result.stdout


def safe_file_info(filename: str) -> str:
    """
    ✅ 안전: 파일명을 리스트 인자로 전달
    """
    # 입력 검증: 파일 존재 확인
    if not os.path.isfile(filename):
        return f"오류: 파일을 찾을 수 없습니다: '{filename}'"

    # ✅ 리스트 형태로 인자 전달
    command = ["echo", f"[시뮬레이션] file {filename}"]
    print(f"  [실행될 명령] {command}")
    result = subprocess.run(command, capture_output=True, text=True,
                            timeout=10)
    return result.stdout


def safe_grep(pattern: str, filepath: str) -> str:
    """
    ✅ 안전: 검색 패턴과 파일 경로를 리스트 인자로 전달
    """
    if not os.path.isfile(filepath):
        return f"오류: 파일을 찾을 수 없습니다: '{filepath}'"

    # ✅ 리스트 형태로 전달 - 패턴이 셸에 의해 해석되지 않음
    command = ["grep", "--", pattern, filepath]
    print(f"  [실행될 명령] {command}")

    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=10)
        return result.stdout if result.stdout else "(일치 항목 없음)"
    except FileNotFoundError:
        return "(grep 명령을 찾을 수 없음 - 시스템에 설치 필요)"


def safe_shell_command(user_input: str) -> str:
    """
    ✅ 불가피하게 shell=True를 써야 하는 경우: shlex.quote() 사용
    하지만 가능하면 shell=False(리스트 인자)를 사용하는 것이 좋습니다.
    """
    # ✅ shlex.quote()로 셸 이스케이프
    safe_input = shlex.quote(user_input)
    command = f"echo '입력값:' {safe_input}"
    print(f"  [이스케이프된 명령] {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-03: 명령어 인젝션 취약 코드 vs 안전한 코드")
    print("=" * 60)

    # --- ❌ 취약한 코드 시연 ---
    print("\n--- ❌ 취약한 코드: 명령어 인젝션 가능 ---")

    # 정상 입력
    print("\n[1] 정상 입력:")
    output = vulnerable_ping("127.0.0.1")
    print(f"  결과: {output.strip()}")

    # 명령어 인젝션 공격
    print("[2] ❌ 명령어 인젝션 공격:")
    malicious_host = "127.0.0.1; echo '해킹 성공! 시스템 명령 실행됨'"
    output = vulnerable_ping(malicious_host)
    print(f"  결과: {output.strip()}")
    print("  -> 세미콜론(;) 뒤의 명령도 실행되었습니다!")

    # 파일 정보 인젝션
    print("\n[3] ❌ 파일 명령 인젝션:")
    malicious_file = "test.txt; echo '비밀 데이터 유출'"
    output = vulnerable_file_info(malicious_file)
    print(f"  결과: {output.strip()}")

    # --- ✅ 안전한 코드 시연 ---
    print("\n\n--- ✅ 안전한 코드: 명령어 인젝션 차단 ---")

    # 정상 입력
    print("\n[1] 정상 입력:")
    output = safe_ping("127.0.0.1")
    print(f"  결과: {output.strip()}")

    # 같은 공격 시도 -> 차단됨
    print("\n[2] ✅ 같은 인젝션 공격 시도 -> 차단:")
    malicious_host = "127.0.0.1; echo '해킹 성공!'"
    output = safe_ping(malicious_host)
    print(f"  결과: {output.strip()}")
    print("  -> 입력 검증에 의해 차단되었습니다!")

    # shlex.quote() 시연
    print("\n\n--- ✅ shlex.quote()로 안전한 셸 사용 ---")

    print("\n[1] 정상 입력:")
    output = safe_shell_command("hello world")
    print(f"  결과: {output.strip()}")

    print("\n[2] 악의적 입력도 안전하게 처리:")
    output = safe_shell_command("test'; rm -rf /; echo '")
    print(f"  결과: {output.strip()}")
    print("  -> shlex.quote()가 특수문자를 안전하게 이스케이프했습니다!")

    # 안전한 grep 시연
    print("\n\n--- ✅ 안전한 grep 실행 ---")

    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                      delete=False) as f:
        f.write("사과\n바나나\n포도\n수박\n사과주스\n")
        temp_path = f.name

    try:
        print(f"\n테스트 파일 내용: 사과, 바나나, 포도, 수박, 사과주스")
        output = safe_grep("사과", temp_path)
        print(f"  '사과' 검색 결과: {output.strip()}")
    finally:
        os.unlink(temp_path)

    # 핵심 정리
    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. subprocess는 항상 리스트 인자 + shell=False 사용")
    print("  2. os.system()은 사용하지 마세요")
    print("  3. 불가피한 경우 shlex.quote()로 이스케이프")
    print("  4. 사용자 입력은 반드시 검증 후 사용")
    print("바이브 코딩 팁: AI에게 'shell=True를 제거하고 안전하게 바꿔줘'")
    print("              라고 요청하세요.")
    print("=" * 60)
