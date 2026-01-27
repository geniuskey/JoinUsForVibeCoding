"""
예제 10-4: 역할 지정의 효과
===========================
역할을 부여하면 AI가 해당 전문가의 관점에서 더 전문적이고
상세한 코드를 생성합니다.

프롬프트 비교:
  [역할 없음] "로그인 함수 만들어줘"
  [역할 있음] "당신은 10년 경력의 시니어 Python 보안 개발자입니다.
              보안 모범 사례를 준수하는 로그인 검증 함수를 작성해주세요."
"""

import hashlib
import re
from datetime import datetime


# --- 역할 없음: 일반적인 결과 ---
# 프롬프트: "로그인 함수 만들어줘"

def basic_login(username, password):
    """기본적인 로그인 — 보안 고려 없음"""
    if username == "admin" and password == "1234":
        return True
    return False


# --- 역할 있음: 시니어 보안 개발자 관점 ---
# 프롬프트: "당신은 10년 경력의 시니어 Python 보안 개발자입니다.
#           보안 모범 사례를 준수하는 로그인 검증 함수를 작성해주세요.
#           비밀번호 해싱, 입력 검증, 로그 기록을 포함해주세요."

# 간이 사용자 저장소 (실제로는 DB 사용)
_USER_STORE = {
    "admin": {
        "password_hash": hashlib.sha256("SecureP@ss1!".encode()).hexdigest(),
        "failed_attempts": 0,
        "locked_until": None,
    }
}

MAX_FAILED_ATTEMPTS = 5


def secure_login(username, password):
    """
    보안 모범 사례를 준수하는 로그인 검증 함수.

    - 입력값 검증 (SQL Injection 등 방어)
    - 비밀번호 해싱 비교
    - 로그인 시도 횟수 제한
    - 감사 로그 기록

    Args:
        username: 사용자 이름
        password: 비밀번호 (평문)
    Returns:
        dict: {"success": bool, "message": str}
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "action": "login_attempt",
    }

    # 1. 입력값 검증
    if not username or not password:
        log_entry["result"] = "FAIL - 빈 입력값"
        _write_log(log_entry)
        return {"success": False, "message": "사용자 이름과 비밀번호를 입력해주세요."}

    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        log_entry["result"] = "FAIL - 잘못된 사용자 이름 형식"
        _write_log(log_entry)
        return {"success": False, "message": "사용자 이름 형식이 올바르지 않습니다."}

    # 2. 사용자 존재 여부 확인 (타이밍 공격 방지를 위해 동일 시간 소요)
    user = _USER_STORE.get(username)
    if not user:
        # 존재하지 않는 사용자도 해싱 수행 (타이밍 공격 방지)
        hashlib.sha256(password.encode()).hexdigest()
        log_entry["result"] = "FAIL - 사용자 없음"
        _write_log(log_entry)
        return {"success": False, "message": "사용자 이름 또는 비밀번호가 올바르지 않습니다."}

    # 3. 계정 잠금 확인
    if user.get("locked_until"):
        lock_time = datetime.fromisoformat(user["locked_until"])
        if datetime.now() < lock_time:
            log_entry["result"] = "FAIL - 계정 잠금"
            _write_log(log_entry)
            return {"success": False, "message": "계정이 일시적으로 잠겼습니다."}
        else:
            user["failed_attempts"] = 0
            user["locked_until"] = None

    # 4. 비밀번호 해싱 비교
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    if input_hash != user["password_hash"]:
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= MAX_FAILED_ATTEMPTS:
            user["locked_until"] = datetime.now().isoformat()
            log_entry["result"] = f"FAIL - 계정 잠금 ({MAX_FAILED_ATTEMPTS}회 실패)"
        else:
            remaining = MAX_FAILED_ATTEMPTS - user["failed_attempts"]
            log_entry["result"] = f"FAIL - 비밀번호 불일치 (남은 시도: {remaining}회)"
        _write_log(log_entry)
        return {"success": False, "message": "사용자 이름 또는 비밀번호가 올바르지 않습니다."}

    # 5. 성공
    user["failed_attempts"] = 0
    log_entry["result"] = "SUCCESS"
    _write_log(log_entry)
    return {"success": True, "message": f"환영합니다, {username}님!"}


def _write_log(entry):
    """감사 로그를 출력합니다."""
    print(f"  [LOG] {entry['timestamp']} | {entry['username']} | {entry.get('result', 'N/A')}")


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 60)
    print("[역할 없음] 기본 로그인 함수")
    print(f"  admin/1234 → {basic_login('admin', '1234')}")
    print(f"  admin/wrong → {basic_login('admin', 'wrong')}")
    print("  → 하드코딩된 비밀번호, 보안 없음\n")

    print("=" * 60)
    print("[역할 있음] 시니어 보안 개발자의 로그인 함수\n")

    tests = [
        ("admin", "SecureP@ss1!"),    # 올바른 비밀번호
        ("admin", "wrongpass"),        # 틀린 비밀번호
        ("", "test"),                  # 빈 사용자 이름
        ("a'OR 1=1--", "hack"),       # SQL Injection 시도
    ]

    for uname, pwd in tests:
        display_pwd = pwd if pwd else "(빈 값)"
        print(f"  로그인 시도: {uname or '(빈 값)'} / {display_pwd}")
        result = secure_login(uname, pwd)
        print(f"  결과: {result}\n")
