"""
예제 23-09: 실습 - 취약한 코드 찾기
- 여러 보안 취약점이 있는 코드 + 수정 버전
- 독자가 직접 취약점을 찾아보는 실습

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
주의: 취약한 코드는 절대 실제 서비스에 사용하지 마세요!
"""

import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import subprocess
import tempfile
from pathlib import Path


# ============================================================
# ❌ 취약한 코드: 여러 보안 문제가 숨어 있는 웹앱 시뮬레이션
# (실습: 아래 코드에서 보안 취약점을 모두 찾아보세요!)
# ============================================================

class VulnerableApp:
    """
    ❌ 이 클래스에는 최소 8개의 보안 취약점이 있습니다.
    모두 찾을 수 있나요?

    힌트:
    1. 비밀 정보 관리
    2. 비밀번호 처리
    3. 데이터베이스 쿼리
    4. 파일 접근
    5. 외부 명령 실행
    6. 입력 검증
    7. 에러 처리
    8. 인증 토큰
    """

    # 취약점 1: 하드코딩된 비밀 정보
    SECRET_KEY = "my-super-secret-key-12345"
    DB_PASSWORD = "admin123"

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._setup_db()

    def _setup_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                email TEXT,
                role TEXT DEFAULT 'user'
            )
        """)
        conn.commit()
        conn.close()

    def register(self, username: str, password: str, email: str) -> dict:
        """사용자 등록 - 여러 취약점 포함"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 취약점 2: MD5로 비밀번호 해싱 (솔트 없음)
        password_hash = hashlib.md5(password.encode()).hexdigest()

        # 취약점 3: SQL 인젝션 - 문자열 포맷팅
        try:
            cursor.execute(
                f"INSERT INTO users (username, password, email) "
                f"VALUES ('{username}', '{password_hash}', '{email}')"
            )
            conn.commit()
            return {"status": "success", "username": username}
        except Exception as e:
            # 취약점 4: 상세한 에러 메시지 노출
            return {"status": "error", "detail": str(e),
                    "query": f"INSERT INTO users... '{username}'"}
        finally:
            conn.close()

    def login(self, username: str, password: str) -> dict:
        """로그인 - 여러 취약점 포함"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        password_hash = hashlib.md5(password.encode()).hexdigest()

        # 취약점 3 (반복): SQL 인젝션
        cursor.execute(
            f"SELECT * FROM users WHERE username = '{username}' "
            f"AND password = '{password_hash}'"
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            # 취약점 5: 예측 가능한 토큰 생성
            import random
            token = ''.join(random.choice('abcdef0123456789')
                           for _ in range(16))
            return {"status": "success", "token": token,
                    "user_id": user[0], "role": user[4]}
        return {"status": "failed"}

    def get_user_file(self, username: str, filename: str) -> str:
        """사용자 파일 읽기 - 경로 순회 취약점"""
        # 취약점 6: 경로 순회 방지 없음
        filepath = f"/tmp/userfiles/{username}/{filename}"
        try:
            with open(filepath, "r") as f:
                return f.read()
        except FileNotFoundError:
            return "파일 없음"

    def search_files(self, pattern: str) -> str:
        """파일 검색 - 명령어 인젝션 취약점"""
        # 취약점 7: 명령어 인젝션
        result = subprocess.run(
            f"find /tmp -name '{pattern}'",
            shell=True, capture_output=True, text=True
        )
        return result.stdout

    def update_profile(self, user_id: str, data: dict) -> dict:
        """프로필 업데이트 - 입력 검증 없음"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 취약점 8: 입력 검증 없음 (이메일 형식, 길이 등)
        if "email" in data:
            cursor.execute(
                f"UPDATE users SET email = '{data['email']}' "
                f"WHERE id = {user_id}"
            )

        conn.commit()
        conn.close()
        return {"status": "updated"}


# ============================================================
# ✅ 안전한 코드: 모든 취약점이 수정된 버전
# ============================================================

class SecureApp:
    """
    ✅ 모든 보안 취약점이 수정된 안전한 버전

    수정 내용:
    1. 비밀 정보 -> 환경 변수
    2. 비밀번호 -> PBKDF2 해싱
    3. SQL 쿼리 -> 파라미터화
    4. 에러 처리 -> 안전한 메시지
    5. 토큰 -> secrets 모듈
    6. 파일 접근 -> 경로 검증
    7. 명령 실행 -> 리스트 인자
    8. 입력 -> 검증 추가
    """

    def __init__(self, db_path: str):
        # 수정 1: 환경 변수에서 비밀 가져오기
        self.secret_key = os.environ.get("APP_SECRET_KEY", "")
        if not self.secret_key:
            print("  경고: APP_SECRET_KEY가 설정되지 않았습니다")

        self.db_path = db_path
        self.user_files_dir = Path(tempfile.mkdtemp(prefix="secure_files_"))
        self._setup_db()

    def _setup_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'user'
            )
        """)
        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        """수정 2: PBKDF2 비밀번호 해싱"""
        salt = secrets.token_bytes(32)
        iterations = 600_000
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                  salt, iterations)
        return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

    def _verify_password(self, password: str, stored: str) -> bool:
        """수정 2: 안전한 비밀번호 검증"""
        parts = stored.split("$")
        if len(parts) != 4:
            return False
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        stored_hash = parts[3]
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                  salt, iterations)
        return hmac.compare_digest(dk.hex(), stored_hash)

    def _validate_username(self, username: str) -> str:
        """수정 8: 사용자 이름 검증"""
        if not isinstance(username, str) or len(username) < 3 or len(username) > 30:
            raise ValueError("사용자 이름은 3~30자여야 합니다")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("사용자 이름은 영문, 숫자, 밑줄만 가능합니다")
        return username.strip()

    def _validate_email(self, email: str) -> str:
        """수정 8: 이메일 검증"""
        if not isinstance(email, str) or len(email) > 254:
            raise ValueError("올바른 이메일을 입력하세요")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("올바른 이메일 형식이 아닙니다")
        return email.strip().lower()

    def _validate_password(self, password: str) -> str:
        """수정 8: 비밀번호 강도 검증"""
        if len(password) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다")
        if not re.search(r'[A-Z]', password):
            raise ValueError("비밀번호에 대문자가 포함되어야 합니다")
        if not re.search(r'[0-9]', password):
            raise ValueError("비밀번호에 숫자가 포함되어야 합니다")
        return password

    def register(self, username: str, password: str, email: str) -> dict:
        """✅ 안전한 사용자 등록"""
        try:
            # 수정 8: 입력 검증
            username = self._validate_username(username)
            password = self._validate_password(password)
            email = self._validate_email(email)
        except ValueError as e:
            return {"status": "error", "message": str(e)}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 수정 2: PBKDF2 해싱
        password_hash = self._hash_password(password)

        try:
            # 수정 3: 파라미터화 쿼리
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            conn.commit()
            return {"status": "success", "username": username}
        except sqlite3.IntegrityError:
            # 수정 4: 안전한 에러 메시지 (내부 정보 미노출)
            return {"status": "error", "message": "이미 존재하는 사용자입니다"}
        except Exception:
            return {"status": "error", "message": "등록에 실패했습니다"}
        finally:
            conn.close()

    def login(self, username: str, password: str) -> dict:
        """✅ 안전한 로그인"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 수정 3: 파라미터화 쿼리
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and self._verify_password(password, user[2]):
            # 수정 5: secrets 모듈로 안전한 토큰 생성
            token = secrets.token_urlsafe(32)
            return {"status": "success", "token": token, "role": user[4]}

        # 수정 4: 로그인 실패 시 어떤 필드가 틀렸는지 알려주지 않음
        return {"status": "failed", "message": "사용자 이름 또는 비밀번호가 올바르지 않습니다"}

    def get_user_file(self, username: str, filename: str) -> str:
        """✅ 안전한 사용자 파일 읽기"""
        # 수정 6: 경로 순회 방지
        try:
            username = self._validate_username(username)
        except ValueError:
            return "잘못된 사용자 이름입니다"

        user_dir = (self.user_files_dir / username).resolve()
        file_path = (user_dir / filename).resolve()

        # 경로가 허용된 범위 안에 있는지 확인
        try:
            file_path.relative_to(self.user_files_dir.resolve())
        except ValueError:
            return "접근 거부: 허용되지 않은 경로입니다"

        if not file_path.is_file():
            return "파일을 찾을 수 없습니다"

        return file_path.read_text()

    def search_files(self, pattern: str) -> str:
        """✅ 안전한 파일 검색"""
        # 수정 7: shell=False + 리스트 인자 + 입력 검증
        if not re.match(r'^[a-zA-Z0-9._\-*?]+$', pattern):
            return "검색 패턴에 허용되지 않은 문자가 포함되어 있습니다"

        try:
            result = subprocess.run(
                ["find", str(self.user_files_dir), "-name", pattern, "-type", "f"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout if result.stdout else "(결과 없음)"
        except subprocess.TimeoutExpired:
            return "검색 시간이 초과되었습니다"

    def update_profile(self, user_id: int, data: dict) -> dict:
        """✅ 안전한 프로필 업데이트"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # 수정 8: 입력 검증
            if "email" in data:
                email = self._validate_email(data["email"])
                # 수정 3: 파라미터화 쿼리
                cursor.execute(
                    "UPDATE users SET email = ? WHERE id = ?",
                    (email, int(user_id))
                )

            conn.commit()
            return {"status": "updated"}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": str(e)}
        finally:
            conn.close()


# ============================================================
# 취약점 대조표
# ============================================================

def print_vulnerability_comparison():
    """취약점과 수정 사항을 대조하여 출력"""
    vulnerabilities = [
        {
            "num": 1,
            "name": "하드코딩된 비밀 정보",
            "vulnerable": 'SECRET_KEY = "my-super-secret-key-12345"',
            "secure": 'self.secret_key = os.environ.get("APP_SECRET_KEY")',
            "explanation": "비밀 정보를 코드에 직접 작성하면 Git에 영구 기록됩니다.",
        },
        {
            "num": 2,
            "name": "약한 비밀번호 해싱",
            "vulnerable": "hashlib.md5(password.encode()).hexdigest()",
            "secure": "hashlib.pbkdf2_hmac('sha256', password, salt, 600000)",
            "explanation": "MD5는 깨진 해시이고 솔트 없이 레인보우 테이블에 취약합니다.",
        },
        {
            "num": 3,
            "name": "SQL 인젝션",
            "vulnerable": "f\"SELECT * FROM users WHERE username = '{username}'\"",
            "secure": "cursor.execute('SELECT * FROM users WHERE username = ?', (username,))",
            "explanation": "사용자 입력을 SQL에 직접 삽입하면 인증 우회가 가능합니다.",
        },
        {
            "num": 4,
            "name": "에러 정보 노출",
            "vulnerable": '{"detail": str(e), "query": "INSERT INTO..."}',
            "secure": '{"message": "등록에 실패했습니다"}',
            "explanation": "상세한 에러 메시지로 DB 구조, 쿼리 등이 유출됩니다.",
        },
        {
            "num": 5,
            "name": "예측 가능한 토큰",
            "vulnerable": "random.choice('abcdef0123456789')",
            "secure": "secrets.token_urlsafe(32)",
            "explanation": "random 모듈은 예측 가능하여 세션 탈취가 가능합니다.",
        },
        {
            "num": 6,
            "name": "경로 순회",
            "vulnerable": 'f"/tmp/userfiles/{username}/{filename}"',
            "secure": "file_path.relative_to(allowed_dir) 검증",
            "explanation": "../를 사용하여 허용 디렉토리 밖의 파일에 접근 가능합니다.",
        },
        {
            "num": 7,
            "name": "명령어 인젝션",
            "vulnerable": 'subprocess.run(f"find ... \'{pattern}\'", shell=True)',
            "secure": 'subprocess.run(["find", dir, "-name", pattern])',
            "explanation": "shell=True와 문자열 포맷팅으로 임의 명령 실행이 가능합니다.",
        },
        {
            "num": 8,
            "name": "입력 검증 부재",
            "vulnerable": "검증 없이 data['email']을 DB에 저장",
            "secure": "정규식으로 이메일 형식, 길이 등 검증",
            "explanation": "검증 없는 입력은 XSS, 인젝션 등 다양한 공격에 활용됩니다.",
        },
    ]

    print("\n--- 취약점 대조표 ---")
    print("=" * 60)

    for v in vulnerabilities:
        print(f"\n취약점 #{v['num']}: {v['name']}")
        print(f"  ❌ 취약: {v['vulnerable']}")
        print(f"  ✅ 안전: {v['secure']}")
        print(f"  설명: {v['explanation']}")


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-09: 실습 - 취약한 코드 찾기")
    print("=" * 60)

    # 임시 데이터베이스
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    # 데모용 환경 변수 설정
    os.environ["APP_SECRET_KEY"] = "demo-secret-for-testing"

    try:
        # --- ❌ 취약한 앱 시연 ---
        print("\n--- ❌ 취약한 앱(VulnerableApp) 시연 ---")
        vuln_app = VulnerableApp(db_path)

        # 정상 등록
        print("\n[1] 사용자 등록:")
        result = vuln_app.register("alice", "pass123", "alice@test.com")
        print(f"  결과: {result}")

        # SQL 인젝션으로 등록
        print("\n[2] ❌ SQL 인젝션 공격:")
        malicious_name = "evil','hack','evil@x.com','admin')--"
        result = vuln_app.register(malicious_name, "x", "x@x.com")
        print(f"  결과: {result}")

        # 로그인
        print("\n[3] 정상 로그인:")
        result = vuln_app.login("alice", "pass123")
        print(f"  결과: {result}")
        if "token" in result:
            print(f"  -> 토큰이 짧고 예측 가능: {result['token']}")

        # 경로 순회
        print("\n[4] ❌ 경로 순회 공격:")
        result = vuln_app.get_user_file("alice", "../../../etc/hostname")
        print(f"  결과: {result}")

        # --- ✅ 안전한 앱 시연 ---
        print("\n\n--- ✅ 안전한 앱(SecureApp) 시연 ---")

        # 새 DB로 시작
        os.unlink(db_path)
        db_fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(db_fd)

        safe_app = SecureApp(db_path)

        # 정상 등록
        print("\n[1] 사용자 등록:")
        result = safe_app.register("alice", "Pass1234", "alice@test.com")
        print(f"  결과: {result}")

        # 약한 비밀번호 거부
        print("\n[2] ✅ 약한 비밀번호 거부:")
        result = safe_app.register("bob", "123", "bob@test.com")
        print(f"  결과: {result}")

        # 잘못된 이메일 거부
        print("\n[3] ✅ 잘못된 이메일 거부:")
        result = safe_app.register("charlie", "Pass1234", "not-email")
        print(f"  결과: {result}")

        # SQL 인젝션 차단
        print("\n[4] ✅ SQL 인젝션 차단:")
        result = safe_app.register("evil'--", "Pass1234", "evil@test.com")
        print(f"  결과: {result}")

        # 안전한 로그인
        print("\n[5] 안전한 로그인:")
        result = safe_app.login("alice", "Pass1234")
        print(f"  결과: 상태={result['status']}")
        if "token" in result:
            print(f"  -> 안전한 토큰 (32바이트): {result['token'][:20]}...")

        # 로그인 실패 (정보 미노출)
        print("\n[6] ✅ 로그인 실패 (정보 미노출):")
        result = safe_app.login("alice", "wrong_password")
        print(f"  결과: {result}")

        # 경로 순회 차단
        print("\n[7] ✅ 경로 순회 차단:")
        result = safe_app.get_user_file("alice", "../../../etc/passwd")
        print(f"  결과: {result}")

        # 명령어 인젝션 차단
        print("\n[8] ✅ 명령어 인젝션 차단:")
        result = safe_app.search_files("*.txt; rm -rf /")
        print(f"  결과: {result}")

    finally:
        os.unlink(db_path)
        if "APP_SECRET_KEY" in os.environ:
            del os.environ["APP_SECRET_KEY"]

    # 취약점 대조표 출력
    print_vulnerability_comparison()

    print("\n\n" + "=" * 60)
    print("실습 과제:")
    print("  1. VulnerableApp 코드에서 8개 취약점을 모두 찾으셨나요?")
    print("  2. 각 취약점이 어떤 공격으로 이어질 수 있는지 설명해보세요")
    print("  3. SecureApp의 수정 방법을 자신의 코드에 적용해보세요")
    print("")
    print("바이브 코딩 팁: AI에게 '내 코드에서 보안 취약점을 찾아서")
    print("              수정된 버전을 만들어줘'라고 요청하세요.")
    print("=" * 60)
