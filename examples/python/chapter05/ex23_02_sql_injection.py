"""
예제 23-02: SQL 인젝션 취약 코드 vs 안전한 코드
- sqlite3 파라미터화 쿼리로 SQL 인젝션 방지
- 바이브 코딩에서 AI가 생성한 DB 코드의 보안 확인하기

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
주의: 취약한 코드는 절대 실제 서비스에 사용하지 마세요!
"""

import sqlite3
import os
import tempfile


def setup_database(db_path: str) -> None:
    """테스트용 데이터베이스 설정"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 사용자 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    """)

    # 테스트 데이터 삽입
    test_users = [
        ("admin", "super_secret_123", "admin@example.com", "admin"),
        ("alice", "alice_pass_456", "alice@example.com", "user"),
        ("bob", "bob_pass_789", "bob@example.com", "user"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
        test_users
    )

    conn.commit()
    conn.close()


# ============================================================
# ❌ 취약한 코드: 문자열 포맷팅으로 SQL 쿼리 생성
# ============================================================

def vulnerable_login(db_path: str, username: str, password: str) -> list:
    """
    ❌ 취약: 사용자 입력을 SQL 쿼리에 직접 삽입
    공격자가 username이나 password에 SQL 코드를 삽입할 수 있음

    예: username = "' OR '1'='1" 으로 모든 사용자 정보 유출 가능
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ❌ 절대 이렇게 하면 안 됩니다!
    # 문자열 포맷팅으로 SQL 쿼리를 구성하면 SQL 인젝션에 취약합니다
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    print(f"  [실행된 쿼리] {query}")
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


def vulnerable_search(db_path: str, search_term: str) -> list:
    """
    ❌ 취약: 검색어를 SQL 쿼리에 직접 삽입
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ❌ 문자열 연결로 쿼리 구성 - 취약!
    query = "SELECT username, email FROM users WHERE username LIKE '%" + search_term + "%'"

    print(f"  [실행된 쿼리] {query}")
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()
    return results


# ============================================================
# ✅ 안전한 코드: 파라미터화 쿼리 사용
# ============================================================

def safe_login(db_path: str, username: str, password: str) -> list:
    """
    ✅ 안전: 파라미터화 쿼리(Parameterized Query) 사용
    - ? 플레이스홀더를 사용하여 값을 별도로 전달
    - sqlite3가 자동으로 이스케이프 처리
    - SQL 인젝션이 불가능
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ 파라미터화 쿼리: ? 자리에 값이 안전하게 바인딩됨
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    results = cursor.fetchall()

    conn.close()
    return results


def safe_search(db_path: str, search_term: str) -> list:
    """
    ✅ 안전: LIKE 쿼리도 파라미터화
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ LIKE 패턴도 파라미터로 전달
    query = "SELECT username, email FROM users WHERE username LIKE ?"
    cursor.execute(query, (f"%{search_term}%",))
    results = cursor.fetchall()

    conn.close()
    return results


def safe_insert(db_path: str, username: str, password: str,
                email: str) -> bool:
    """
    ✅ 안전: INSERT도 파라미터화 쿼리 사용
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # ✅ INSERT도 파라미터화
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"  삽입 실패: {e}")
        return False
    finally:
        conn.close()


def safe_update(db_path: str, user_id: int, new_email: str) -> bool:
    """
    ✅ 안전: UPDATE도 파라미터화 쿼리 사용
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ UPDATE도 파라미터화
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-02: SQL 인젝션 취약 코드 vs 안전한 코드")
    print("=" * 60)

    # 임시 데이터베이스 생성
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    try:
        setup_database(db_path)

        # --- ❌ 취약한 코드 시연 ---
        print("\n--- ❌ 취약한 코드: SQL 인젝션 공격 시연 ---")

        # 정상 로그인
        print("\n[1] 정상 로그인 시도:")
        results = vulnerable_login(db_path, "alice", "alice_pass_456")
        print(f"  결과: {len(results)}명 찾음 - {'성공' if results else '실패'}")

        # SQL 인젝션 공격 1: 인증 우회
        print("\n[2] ❌ SQL 인젝션 공격 - 인증 우회:")
        print("  공격 입력: username = \"' OR '1'='1' --\"")
        results = vulnerable_login(db_path, "' OR '1'='1' --", "아무거나")
        print(f"  결과: {len(results)}명의 정보가 유출됨!")
        for user in results:
            print(f"    -> ID:{user[0]}, 이름:{user[1]}, 비밀번호:{user[2]}, "
                  f"이메일:{user[3]}, 역할:{user[4]}")

        # SQL 인젝션 공격 2: 검색을 통한 정보 유출
        print("\n[3] ❌ SQL 인젝션 공격 - 검색 악용:")
        print("  공격 입력: search = \"' UNION SELECT password, role FROM users --\"")
        results = vulnerable_search(
            db_path,
            "' UNION SELECT password, role FROM users --"
        )
        print(f"  결과: {len(results)}개 레코드 유출!")
        for row in results:
            print(f"    -> {row}")

        # --- ✅ 안전한 코드 시연 ---
        print("\n\n--- ✅ 안전한 코드: 파라미터화 쿼리 ---")

        # 정상 로그인
        print("\n[1] 정상 로그인 시도:")
        results = safe_login(db_path, "alice", "alice_pass_456")
        print(f"  결과: {len(results)}명 찾음 - {'성공' if results else '실패'}")

        # 같은 공격 시도 -> 차단됨
        print("\n[2] ✅ 같은 SQL 인젝션 공격 시도 -> 차단:")
        print("  공격 입력: username = \"' OR '1'='1' --\"")
        results = safe_login(db_path, "' OR '1'='1' --", "아무거나")
        print(f"  결과: {len(results)}명 찾음 - 공격 차단! (0명이어야 정상)")

        # 안전한 검색
        print("\n[3] ✅ 같은 검색 인젝션 시도 -> 차단:")
        results = safe_search(
            db_path,
            "' UNION SELECT password, role FROM users --"
        )
        print(f"  결과: {len(results)}개 - 공격 차단! (0개이어야 정상)")

        # 안전한 정상 검색
        print("\n[4] ✅ 정상 검색:")
        results = safe_search(db_path, "ali")
        print(f"  'ali' 검색 결과: {results}")

    finally:
        # 임시 데이터베이스 삭제
        os.unlink(db_path)

    print("\n" + "=" * 60)
    print("핵심 원칙: SQL 쿼리에 사용자 입력을 직접 넣지 마세요!")
    print("항상 파라미터화 쿼리(?)를 사용하세요.")
    print("바이브 코딩 팁: AI에게 '파라미터화 쿼리로 바꿔줘'라고 요청하세요.")
    print("=" * 60)
