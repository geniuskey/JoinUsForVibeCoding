"""
예제 23-05: 환경 변수로 비밀 관리
- os.environ을 활용한 비밀 정보 관리
- 하드코딩된 비밀 vs 환경 변수 사용

이 예제는 교육 목적으로 취약한 코드와 안전한 코드를 모두 보여줍니다.
"""

import os
import sys


# ============================================================
# ❌ 취약한 코드: 비밀 정보를 코드에 하드코딩
# ============================================================

def vulnerable_database_config() -> dict:
    """
    ❌ 취약: 비밀번호, API 키 등을 코드에 직접 작성
    - 소스 코드가 유출되면 비밀 정보도 함께 유출
    - Git 저장소에 비밀 정보가 기록됨
    - 환경(개발/운영)별로 코드를 수정해야 함
    """
    # ❌ 절대 이렇게 하지 마세요!
    config = {
        "db_host": "production-db.example.com",
        "db_port": 5432,
        "db_name": "myapp",
        "db_user": "admin",
        "db_password": "SuperSecret123!@#",      # ❌ 비밀번호 하드코딩
        "api_key": "sk-1234567890abcdef",         # ❌ API 키 하드코딩
        "jwt_secret": "my-super-secret-jwt-key",  # ❌ JWT 시크릿 하드코딩
    }
    return config


def vulnerable_send_email() -> None:
    """
    ❌ 취약: 이메일 자격증명을 코드에 직접 작성
    """
    # ❌ 절대 이렇게 하지 마세요!
    smtp_password = "EmailPass456!"
    print(f"  이메일 비밀번호가 코드에 노출됨: {smtp_password}")


# ============================================================
# ✅ 안전한 코드: 환경 변수로 비밀 관리
# ============================================================

def get_required_env(key: str) -> str:
    """
    ✅ 필수 환경 변수를 안전하게 가져오기
    - 환경 변수가 없으면 명확한 오류 메시지와 함께 종료
    - 빈 값도 거부
    """
    value = os.environ.get(key)

    if value is None:
        raise EnvironmentError(
            f"필수 환경 변수 '{key}'가 설정되지 않았습니다.\n"
            f"설정 방법: export {key}=값"
        )

    if not value.strip():
        raise EnvironmentError(
            f"환경 변수 '{key}'가 비어 있습니다."
        )

    return value


def get_optional_env(key: str, default: str = "") -> str:
    """
    ✅ 선택적 환경 변수를 기본값과 함께 가져오기
    """
    return os.environ.get(key, default)


def safe_database_config() -> dict:
    """
    ✅ 안전: 모든 비밀 정보를 환경 변수에서 가져옴
    - 코드에 비밀 정보가 없음
    - 환경별로 다른 설정 가능
    - Git에 비밀 정보가 저장되지 않음
    """
    config = {
        "db_host": get_required_env("DB_HOST"),
        "db_port": int(get_optional_env("DB_PORT", "5432")),
        "db_name": get_required_env("DB_NAME"),
        "db_user": get_required_env("DB_USER"),
        "db_password": get_required_env("DB_PASSWORD"),
        "api_key": get_required_env("API_KEY"),
        "jwt_secret": get_required_env("JWT_SECRET"),
    }
    return config


def safe_check_config() -> dict:
    """
    ✅ 안전: 설정 확인 시 비밀 값을 마스킹
    """
    config = {}

    required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD",
                     "API_KEY", "JWT_SECRET"]
    optional_vars = {"DB_PORT": "5432", "DEBUG": "false"}

    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # ✅ 비밀 값은 마스킹하여 표시
            config[var] = mask_secret(value)
        else:
            config[var] = "(미설정 - 필수!)"

    for var, default in optional_vars.items():
        value = os.environ.get(var, default)
        config[var] = value  # 비밀이 아닌 값은 그대로 표시

    return config


def mask_secret(value: str) -> str:
    """
    ✅ 비밀 값을 마스킹 (처음 2자만 표시)
    """
    if len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 2)


# ============================================================
# ✅ 안전한 설정 관리 클래스
# ============================================================

class SecureConfig:
    """
    ✅ 환경 변수 기반 안전한 설정 관리 클래스

    사용법:
        config = SecureConfig()
        db_password = config.get_secret("DB_PASSWORD")
    """

    def __init__(self):
        self._cache: dict = {}

    def get_secret(self, key: str) -> str:
        """필수 비밀 환경 변수 가져오기"""
        if key not in self._cache:
            self._cache[key] = get_required_env(key)
        return self._cache[key]

    def get_optional(self, key: str, default: str = "") -> str:
        """선택적 환경 변수 가져오기"""
        return os.environ.get(key, default)

    def is_production(self) -> bool:
        """운영 환경인지 확인"""
        env = self.get_optional("APP_ENV", "development")
        return env.lower() == "production"

    def show_status(self) -> None:
        """설정 상태 출력 (값은 마스킹)"""
        print("  설정 상태:")
        for key, value in sorted(self._cache.items()):
            print(f"    {key}: {mask_secret(value)}")

    def __repr__(self):
        """✅ repr에서도 비밀 노출 방지"""
        return f"SecureConfig(loaded_keys={list(self._cache.keys())})"


# ============================================================
# 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("예제 23-05: 환경 변수로 비밀 관리")
    print("=" * 60)

    # --- ❌ 취약한 코드 시연 ---
    print("\n--- ❌ 취약한 코드: 하드코딩된 비밀 ---")
    config = vulnerable_database_config()
    print("  하드코딩된 설정:")
    for key, value in config.items():
        print(f"    {key}: {value}")
    print("  -> 코드에 비밀번호와 API 키가 노출되어 있습니다!")
    print("  -> Git에 커밋하면 영구적으로 기록됩니다!")

    # --- ✅ 안전한 코드 시연 ---
    print("\n\n--- ✅ 안전한 코드: 환경 변수 사용 ---")

    # 데모를 위한 환경 변수 설정 (실제로는 셸에서 설정)
    demo_env = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "myapp_dev",
        "DB_USER": "dev_user",
        "DB_PASSWORD": "dev_password_123",
        "API_KEY": "sk-demo-key-abcdef",
        "JWT_SECRET": "dev-jwt-secret-xyz",
        "APP_ENV": "development",
        "DEBUG": "true",
    }

    # 환경 변수 설정 (데모용)
    print("\n[환경 변수 설정 (데모용)]:")
    for key, value in demo_env.items():
        os.environ[key] = value
        print(f"  export {key}={mask_secret(value) if 'PASSWORD' in key or 'KEY' in key or 'SECRET' in key else value}")

    # 안전한 설정 가져오기
    print("\n[안전한 설정 로드]:")
    try:
        config = safe_database_config()
        print("  설정 로드 성공!")
        for key, value in config.items():
            display = mask_secret(str(value)) if any(
                s in key for s in ['password', 'key', 'secret']
            ) else value
            print(f"    {key}: {display}")
    except EnvironmentError as e:
        print(f"  설정 오류: {e}")

    # 설정 확인 (마스킹)
    print("\n[설정 상태 확인 (마스킹됨)]:")
    status = safe_check_config()
    for key, value in status.items():
        print(f"    {key}: {value}")

    # SecureConfig 클래스 사용
    print("\n[SecureConfig 클래스 사용]:")
    secure = SecureConfig()
    try:
        db_pass = secure.get_secret("DB_PASSWORD")
        print(f"  DB_PASSWORD 로드: {mask_secret(db_pass)}")
        api_key = secure.get_secret("API_KEY")
        print(f"  API_KEY 로드: {mask_secret(api_key)}")
        print(f"  운영 환경: {secure.is_production()}")
        secure.show_status()
        print(f"  repr: {secure}")
    except EnvironmentError as e:
        print(f"  오류: {e}")

    # 없는 환경 변수 요청 시
    print("\n[필수 환경 변수 누락 테스트]:")
    # 기존 데모 환경 변수 정리
    if "MISSING_VAR" in os.environ:
        del os.environ["MISSING_VAR"]
    try:
        get_required_env("MISSING_VAR")
    except EnvironmentError as e:
        print(f"  올바른 오류 발생: {e}")

    # 데모용 환경 변수 정리
    for key in demo_env:
        if key in os.environ:
            del os.environ[key]

    print("\n" + "=" * 60)
    print("핵심 원칙:")
    print("  1. 비밀 정보는 절대 코드에 하드코딩하지 마세요")
    print("  2. 환경 변수(os.environ)를 사용하세요")
    print("  3. 로그/출력에 비밀 값을 노출하지 마세요 (마스킹)")
    print("  4. .gitignore에 .env 파일을 추가하세요")
    print("")
    print("실제 설정 방법:")
    print("  $ export DB_PASSWORD='my_secure_password'")
    print("  $ python my_app.py")
    print("")
    print("바이브 코딩 팁: AI에게 '하드코딩된 비밀을 환경 변수로")
    print("              바꿔줘'라고 요청하세요.")
    print("=" * 60)
