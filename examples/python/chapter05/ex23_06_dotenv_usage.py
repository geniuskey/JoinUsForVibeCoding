"""
예제 23-06: .env 파일 사용
- 표준 라이브러리만으로 .env 파일 파싱 구현
- 외부 패키지(python-dotenv) 없이 .env 파일 로드
- .gitignore에 .env 추가하는 방법

이 예제는 교육 목적으로 .env 파일을 안전하게 사용하는 방법을 보여줍니다.
"""

import os
import tempfile
from pathlib import Path


# ============================================================
# ✅ 표준 라이브러리로 .env 파일 파서 구현
# ============================================================

def load_dotenv(filepath: str = ".env", override: bool = False) -> dict:
    """
    ✅ .env 파일을 파싱하여 환경 변수로 설정

    지원하는 .env 형식:
    - KEY=value
    - KEY="quoted value"
    - KEY='single quoted value'
    - # 주석
    - 빈 줄 무시
    - export KEY=value (export 접두어 지원)

    Args:
        filepath: .env 파일 경로
        override: True이면 기존 환경 변수를 덮어씀
    Returns:
        파싱된 키-값 딕셔너리
    """
    env_vars = {}
    env_path = Path(filepath)

    if not env_path.is_file():
        print(f"  경고: .env 파일을 찾을 수 없습니다: {filepath}")
        return env_vars

    with open(env_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # 빈 줄과 주석 건너뛰기
            if not line or line.startswith("#"):
                continue

            # 'export ' 접두어 제거
            if line.startswith("export "):
                line = line[7:]

            # KEY=VALUE 분리
            if "=" not in line:
                print(f"  경고: {line_num}번째 줄 형식 오류 (무시됨): {line}")
                continue

            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()

            # 키 유효성 검사
            if not key or not key.replace("_", "").isalnum():
                print(f"  경고: {line_num}번째 줄 잘못된 키 (무시됨): {key}")
                continue

            # 따옴표 제거
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            # 인라인 주석 제거 (따옴표 밖의 #)
            if not (value.startswith('"') or value.startswith("'")):
                comment_idx = value.find(" #")
                if comment_idx >= 0:
                    value = value[:comment_idx].strip()

            env_vars[key] = value

            # 환경 변수 설정
            if override or key not in os.environ:
                os.environ[key] = value

    return env_vars


def create_env_example(filepath: str = ".env.example") -> None:
    """
    ✅ .env.example 파일 생성
    - 실제 비밀 값 대신 예시/설명을 포함
    - Git에 커밋하여 필요한 환경 변수를 문서화
    """
    example_content = """# ===========================================
# 애플리케이션 설정
# ===========================================
# 이 파일을 .env로 복사하고 실제 값을 입력하세요:
#   cp .env.example .env
#
# 주의: .env 파일은 절대 Git에 커밋하지 마세요!

# 앱 환경 (development, staging, production)
APP_ENV=development

# 디버그 모드 (true/false)
DEBUG=true

# ===========================================
# 데이터베이스 설정
# ===========================================
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=your_db_username
DB_PASSWORD=your_db_password_here

# ===========================================
# API 키
# ===========================================
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here

# ===========================================
# JWT 설정
# ===========================================
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRY=3600
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(example_content)


def create_gitignore_entry() -> str:
    """
    ✅ .gitignore에 추가해야 할 항목 반환
    """
    return """# 환경 변수 파일 - 절대 커밋하지 마세요!
.env
.env.local
.env.production
.env.*.local

# .env.example은 커밋해도 됩니다 (실제 비밀 없음)
!.env.example
"""


# ============================================================
# ✅ 설정 관리 클래스
# ============================================================

class AppConfig:
    """
    ✅ .env 기반 애플리케이션 설정 관리

    사용법:
        config = AppConfig()     # .env 파일 자동 로드
        db_host = config.db_host
    """

    def __init__(self, env_file: str = ".env"):
        self._env_vars = load_dotenv(env_file)

    @property
    def app_env(self) -> str:
        return os.environ.get("APP_ENV", "development")

    @property
    def is_debug(self) -> bool:
        return os.environ.get("DEBUG", "false").lower() == "true"

    @property
    def db_host(self) -> str:
        return os.environ.get("DB_HOST", "localhost")

    @property
    def db_port(self) -> int:
        return int(os.environ.get("DB_PORT", "5432"))

    @property
    def db_name(self) -> str:
        value = os.environ.get("DB_NAME")
        if not value:
            raise EnvironmentError("DB_NAME이 설정되지 않았습니다")
        return value

    @property
    def db_connection_string(self) -> str:
        """✅ 비밀번호가 포함된 연결 문자열 (로그에 출력하지 말 것!)"""
        user = os.environ.get("DB_USER", "")
        password = os.environ.get("DB_PASSWORD", "")
        return f"postgresql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def db_connection_string_safe(self) -> str:
        """✅ 로그용 연결 문자열 (비밀번호 마스킹)"""
        user = os.environ.get("DB_USER", "")
        return f"postgresql://{user}:****@{self.db_host}:{self.db_port}/{self.db_name}"

    def show_config(self) -> None:
        """✅ 설정 출력 (비밀 값 마스킹)"""
        print(f"  APP_ENV: {self.app_env}")
        print(f"  DEBUG: {self.is_debug}")
        print(f"  DB 연결: {self.db_connection_string_safe}")

    def validate(self) -> list:
        """✅ 필수 설정 누락 확인"""
        errors = []
        required = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]

        for var in required:
            if not os.environ.get(var):
                errors.append(f"필수 환경 변수 누락: {var}")

        return errors


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-06: .env 파일 사용 (표준 라이브러리)")
    print("=" * 60)

    # 임시 디렉토리에서 작업
    with tempfile.TemporaryDirectory() as tmpdir:

        # --- .env 파일 생성 (데모용) ---
        env_path = os.path.join(tmpdir, ".env")
        env_content = """# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_dev
DB_USER=dev_user
DB_PASSWORD="my_secret_pass_123"

# API 설정
API_KEY='sk-demo-key-abcdef'
export API_SECRET=demo_secret_xyz

# 앱 설정
APP_ENV=development
DEBUG=true

# JWT
JWT_SECRET=dev-jwt-secret-key
JWT_EXPIRY=3600
"""
        with open(env_path, "w") as f:
            f.write(env_content)

        print("\n--- .env 파일 내용 ---")
        print(env_content)

        # --- .env 파일 로드 ---
        print("--- .env 파일 파싱 결과 ---")
        env_vars = load_dotenv(env_path)

        for key, value in env_vars.items():
            # 비밀 정보는 마스킹
            if any(s in key for s in ["PASSWORD", "SECRET", "KEY"]):
                display = value[:2] + "*" * (len(value) - 2)
            else:
                display = value
            print(f"  {key}={display}")

        # --- AppConfig 클래스 사용 ---
        print("\n--- AppConfig 클래스 사용 ---")
        config = AppConfig(env_path)
        config.show_config()

        # 설정 검증
        print("\n--- 설정 검증 ---")
        errors = config.validate()
        if errors:
            for err in errors:
                print(f"  오류: {err}")
        else:
            print("  모든 필수 설정이 올바르게 로드되었습니다!")

        # --- .env.example 생성 ---
        print("\n--- .env.example 파일 생성 ---")
        example_path = os.path.join(tmpdir, ".env.example")
        create_env_example(example_path)
        with open(example_path, "r") as f:
            print(f.read()[:500] + "...")

        # --- .gitignore 항목 ---
        print("\n--- .gitignore에 추가할 내용 ---")
        print(create_gitignore_entry())

        # --- 다양한 .env 형식 테스트 ---
        print("--- 다양한 .env 형식 파싱 테스트 ---")
        test_env_path = os.path.join(tmpdir, ".env.test")
        test_content = """# 다양한 형식 테스트
SIMPLE=value
QUOTED_DOUBLE="hello world"
QUOTED_SINGLE='hello world'
WITH_EXPORT=exported_value
EMPTY_VALUE=
WITH_COMMENT=real_value # 이것은 주석
SPECIAL_CHARS="hello=world&foo=bar"
KOREAN_VALUE="안녕하세요"
URL_VALUE=https://example.com/api/v1
"""
        with open(test_env_path, "w") as f:
            f.write(test_content)

        test_vars = load_dotenv(test_env_path, override=True)
        for key, value in test_vars.items():
            print(f"  {key} = '{value}'")

        # 환경 변수 정리 (데모 후)
        for key in list(env_vars.keys()) + list(test_vars.keys()):
            if key in os.environ:
                del os.environ[key]

    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. .env 파일에 비밀 정보를 저장하세요")
    print("  2. .env 파일은 절대 Git에 커밋하지 마세요")
    print("  3. .env.example 파일로 필요한 변수를 문서화하세요")
    print("  4. .gitignore에 .env를 반드시 추가하세요")
    print("")
    print("사용 순서:")
    print("  1. cp .env.example .env")
    print("  2. .env 파일에 실제 값 입력")
    print("  3. 코드에서 os.environ으로 읽기")
    print("")
    print("바이브 코딩 팁: AI에게 '.env 파일 설정과 .gitignore를")
    print("              만들어줘'라고 요청하세요.")
    print("=" * 60)
