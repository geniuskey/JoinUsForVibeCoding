"""
예제 20-06: 환경별 설정 관리
개발(development), 테스트(testing), 운영(production) 환경을
분리하여 관리하는 방법을 배웁니다. os.environ을 활용합니다.
"""

import os
import json
import tempfile


# ============================================================
# 환경 설정 클래스 (클래스 상속 방식)
# ============================================================

class BaseConfig:
    """모든 환경에 공통인 기본 설정"""
    APP_NAME = "바이브코딩앱"
    APP_VERSION = "1.0.0"
    ENCODING = "utf-8"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

    def to_dict(self):
        """설정을 딕셔너리로 변환합니다."""
        return {
            key: getattr(self, key)
            for key in dir(self)
            if key.isupper() and not key.startswith("_")
        }


class DevelopmentConfig(BaseConfig):
    """개발 환경 설정"""
    ENV_NAME = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///dev.db"
    HOST = "localhost"
    PORT = 5000
    RELOAD = True
    CACHE_ENABLED = False


class TestingConfig(BaseConfig):
    """테스트 환경 설정"""
    ENV_NAME = "testing"
    DEBUG = True
    LOG_LEVEL = "WARNING"
    DATABASE_URL = "sqlite:///test.db"
    HOST = "localhost"
    PORT = 5001
    RELOAD = False
    CACHE_ENABLED = False


class ProductionConfig(BaseConfig):
    """운영 환경 설정"""
    ENV_NAME = "production"
    DEBUG = False
    LOG_LEVEL = "ERROR"
    DATABASE_URL = "postgresql://user:pass@db-server:5432/prod_db"
    HOST = "0.0.0.0"
    PORT = 8000
    RELOAD = False
    CACHE_ENABLED = True


# 환경 이름으로 설정 클래스를 가져오는 매핑
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(env_name=None):
    """환경 이름에 맞는 설정 객체를 반환합니다."""
    if env_name is None:
        # 환경 변수에서 읽기 (기본값: development)
        env_name = os.environ.get("APP_ENV", "development")

    config_class = CONFIG_MAP.get(env_name)
    if config_class is None:
        raise ValueError(
            f"알 수 없는 환경: '{env_name}'. "
            f"사용 가능: {list(CONFIG_MAP.keys())}"
        )

    return config_class()


# ============================================================
# 환경 변수 기반 설정 (os.environ 활용)
# ============================================================

class EnvConfig:
    """환경 변수에서 설정을 읽는 클래스"""

    def __init__(self):
        # 환경 변수에서 값을 읽되, 기본값 제공
        self.app_name = os.environ.get("APP_NAME", "기본앱")
        self.debug = os.environ.get("APP_DEBUG", "false").lower() == "true"
        self.port = int(os.environ.get("APP_PORT", "8000"))
        self.db_url = os.environ.get("DATABASE_URL", "sqlite:///default.db")
        self.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")
        self.log_level = os.environ.get("LOG_LEVEL", "INFO")

    def display(self):
        """현재 설정을 출력합니다 (민감 정보 마스킹)."""
        print(f"  APP_NAME    = {self.app_name}")
        print(f"  APP_DEBUG   = {self.debug}")
        print(f"  APP_PORT    = {self.port}")
        print(f"  DATABASE_URL= {self._mask_url(self.db_url)}")
        print(f"  SECRET_KEY  = {self._mask_secret(self.secret_key)}")
        print(f"  LOG_LEVEL   = {self.log_level}")

    @staticmethod
    def _mask_secret(value):
        """비밀 값을 마스킹합니다."""
        if len(value) <= 4:
            return "****"
        return value[:2] + "*" * (len(value) - 4) + value[-2:]

    @staticmethod
    def _mask_url(url):
        """URL에서 비밀번호를 마스킹합니다."""
        if ":pass@" in url:
            return url.replace(":pass@", ":****@")
        return url


# ============================================================
# .env 파일 파서 (python-dotenv 없이 직접 구현)
# ============================================================

def parse_env_file(filepath):
    """간단한 .env 파일 파서"""
    env_vars = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            # 빈 줄이나 주석 건너뛰기
            if not line or line.startswith("#"):
                continue
            # KEY=VALUE 형식 파싱
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # 따옴표 제거
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env_vars[key] = value
    return env_vars


def create_env_files(temp_dir):
    """환경별 .env 파일을 생성합니다."""
    # .env (기본/개발용)
    env_default = """# 기본 환경 설정
APP_NAME=바이브코딩앱
APP_ENV=development
APP_DEBUG=true
APP_PORT=5000

# 데이터베이스
DATABASE_URL=sqlite:///dev.db

# 보안
SECRET_KEY="dev-secret-key-not-for-production"
"""

    # .env.production (운영용)
    env_production = """# 운영 환경 설정
APP_NAME=바이브코딩앱
APP_ENV=production
APP_DEBUG=false
APP_PORT=8000

# 데이터베이스
DATABASE_URL="postgresql://user:pass@db-server:5432/prod_db"

# 보안
SECRET_KEY="super-secret-production-key-abc123"
"""

    files = {
        ".env": env_default,
        ".env.production": env_production,
    }

    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return files


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-06: 환경별 설정 관리")
    print("=" * 60)
    print()

    temp_dir = tempfile.mkdtemp()

    # 원래 환경 변수를 보존하기 위한 백업
    original_env = {}

    try:
        # --- 1단계: 클래스 기반 환경 설정 ---
        print("--- 1단계: 클래스 기반 환경 설정 ---")
        print()

        for env_name in ["development", "testing", "production"]:
            config = get_config(env_name)
            print(f"  [{config.ENV_NAME}]")
            print(f"    DEBUG       = {config.DEBUG}")
            print(f"    LOG_LEVEL   = {config.LOG_LEVEL}")
            print(f"    DATABASE_URL= {config.DATABASE_URL}")
            print(f"    HOST:PORT   = {config.HOST}:{config.PORT}")
            print(f"    RELOAD      = {config.RELOAD}")
            print(f"    CACHE       = {config.CACHE_ENABLED}")
            print()

        # --- 2단계: 환경 변수로 설정 전환 ---
        print("--- 2단계: 환경 변수로 설정 전환 ---")
        print()

        # 현재 APP_ENV 환경 변수 확인
        current_env = os.environ.get("APP_ENV", "(설정되지 않음)")
        print(f"  현재 APP_ENV: {current_env}")
        print()

        # 환경 변수 설정 시뮬레이션
        env_key = "APP_ENV"
        original_env[env_key] = os.environ.get(env_key)

        for env_name in ["development", "production"]:
            os.environ[env_key] = env_name
            config = get_config()  # 환경 변수에서 자동으로 읽음
            print(f"  APP_ENV={env_name} -> {config.ENV_NAME} 설정 로드됨")
            print(f"    DEBUG={config.DEBUG}, PORT={config.PORT}")
        print()

        # --- 3단계: .env 파일 관리 ---
        print("--- 3단계: .env 파일 관리 ---")
        print()

        create_env_files(temp_dir)

        for filename in [".env", ".env.production"]:
            filepath = os.path.join(temp_dir, filename)
            print(f"  파일: {filename}")
            print(f"  " + "-" * 40)
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line_stripped = line.strip()
                    if line_stripped and not line_stripped.startswith("#"):
                        print(f"    {line_stripped}")
            print()

        # --- 4단계: .env 파일 파싱 ---
        print("--- 4단계: .env 파일 파싱 및 적용 ---")
        print()

        env_file = os.path.join(temp_dir, ".env")
        env_vars = parse_env_file(env_file)

        print("  .env 파일에서 파싱된 설정:")
        for key, value in env_vars.items():
            print(f"    {key} = {value}")
        print()

        # 환경 변수에 적용
        for key, value in env_vars.items():
            if key not in original_env:
                original_env[key] = os.environ.get(key)
            os.environ[key] = value

        # EnvConfig로 읽기
        print("  EnvConfig에서 읽은 설정:")
        env_config = EnvConfig()
        env_config.display()
        print()

        # --- 5단계: 운영 환경으로 전환 ---
        print("--- 5단계: 운영 환경(.env.production)으로 전환 ---")
        print()

        prod_env_file = os.path.join(temp_dir, ".env.production")
        prod_vars = parse_env_file(prod_env_file)

        for key, value in prod_vars.items():
            os.environ[key] = value

        print("  운영 환경 설정 적용 후:")
        prod_config = EnvConfig()
        prod_config.display()
        print()

        # --- 환경 관리 모범 사례 ---
        print("--- 환경별 설정 관리 모범 사례 ---")
        print()
        print("  1. .env 파일은 .gitignore에 추가하세요")
        print("  2. .env.example 파일로 필요한 변수를 문서화하세요")
        print("  3. 운영 환경 비밀 정보는 환경 변수로 주입하세요")
        print("  4. 기본값을 항상 제공하여 설정 누락을 방지하세요")
        print("  5. 민감 정보는 로그에 출력하지 마세요")
        print()

        print("환경별 설정 관리 예제를 성공적으로 실행했습니다!")

    finally:
        # 환경 변수 원상 복구
        for key, original_value in original_env.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

        # 임시 파일 정리
        for filename in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, filename))
        os.rmdir(temp_dir)
        print("(환경 변수 복구 및 임시 파일 정리 완료)")
