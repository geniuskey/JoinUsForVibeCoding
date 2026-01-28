"""
예제 20-05: 설정 파일 관리
configparser를 사용하여 config.ini 파일을 읽고 쓰는 방법을 배웁니다.
프로젝트 설정을 체계적으로 관리하는 방법을 시연합니다.
"""

import configparser
import os
import tempfile


def create_config(filepath):
    """기본 설정 파일(config.ini)을 생성합니다."""
    config = configparser.ConfigParser()

    # 기본 섹션 설정
    config["DEFAULT"] = {
        "debug": "false",
        "log_level": "INFO",
        "encoding": "utf-8",
    }

    # 앱 설정
    config["app"] = {
        "name": "바이브코딩앱",
        "version": "1.0.0",
        "description": "AI와 함께하는 코딩 프로젝트",
        "port": "8000",
        "host": "localhost",
    }

    # 데이터베이스 설정
    config["database"] = {
        "engine": "sqlite",
        "name": "app.db",
        "pool_size": "5",
        "timeout": "30",
    }

    # 로그 설정
    config["logging"] = {
        "log_file": "app.log",
        "max_size_mb": "10",
        "backup_count": "3",
        "format": "%%(asctime)s - %%(levelname)s - %%(message)s",
    }

    # 보안 설정
    config["security"] = {
        "session_timeout": "3600",
        "max_login_attempts": "5",
        "password_min_length": "8",
    }

    # 파일에 저장
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 프로젝트 설정 파일\n")
        f.write("# configparser를 사용하여 관리합니다\n\n")
        config.write(f)

    return config


def read_config(filepath):
    """설정 파일을 읽어서 반환합니다."""
    config = configparser.ConfigParser()
    config.read(filepath, encoding="utf-8")
    return config


def display_config(config):
    """설정 내용을 보기 좋게 출력합니다."""
    for section in config.sections():
        print(f"  [{section}]")
        for key, value in config.items(section):
            # DEFAULT 섹션의 값이 상속되므로 구분 표시
            is_default = key in config.defaults() and config.defaults()[key] == value
            marker = " (기본값)" if is_default else ""
            print(f"    {key} = {value}{marker}")
        print()


def update_config(config, filepath, section, key, value):
    """설정값을 업데이트하고 파일에 저장합니다."""
    if section not in config:
        config[section] = {}
    old_value = config.get(section, key, fallback="(없음)")
    config[section][key] = value

    with open(filepath, "w", encoding="utf-8") as f:
        config.write(f)

    return old_value


class ConfigManager:
    """설정 파일을 관리하는 클래스입니다."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        if os.path.exists(filepath):
            self.config.read(filepath, encoding="utf-8")

    def get(self, section, key, fallback=None):
        """설정값을 가져옵니다."""
        return self.config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=0):
        """정수형 설정값을 가져옵니다."""
        return self.config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        """불리언 설정값을 가져옵니다."""
        return self.config.getboolean(section, key, fallback=fallback)

    def set(self, section, key, value):
        """설정값을 변경합니다."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)

    def save(self):
        """설정을 파일에 저장합니다."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            self.config.write(f)

    def sections(self):
        """모든 섹션 목록을 반환합니다."""
        return self.config.sections()

    def has_section(self, section):
        """섹션 존재 여부를 확인합니다."""
        return self.config.has_section(section)

    def remove_section(self, section):
        """섹션을 삭제합니다."""
        return self.config.remove_section(section)


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-05: 설정 파일 관리 (configparser)")
    print("=" * 60)
    print()

    # 임시 디렉토리에서 작업
    temp_dir = tempfile.mkdtemp()
    config_file = os.path.join(temp_dir, "config.ini")

    try:
        # --- 1단계: 설정 파일 생성 ---
        print("--- 1단계: 설정 파일 생성 ---")
        config = create_config(config_file)
        print(f"  설정 파일이 생성되었습니다: config.ini")
        print()

        # 파일 내용 출력
        print("  생성된 config.ini 내용:")
        print("  " + "-" * 45)
        with open(config_file, "r", encoding="utf-8") as f:
            for line in f:
                print(f"  {line}", end="")
        print("  " + "-" * 45)
        print()

        # --- 2단계: 설정 파일 읽기 ---
        print("--- 2단계: 설정 파일 읽기 ---")
        print()
        config = read_config(config_file)
        display_config(config)

        # --- 3단계: 다양한 타입으로 읽기 ---
        print("--- 3단계: 다양한 타입으로 읽기 ---")
        print()
        print(f"  문자열: app.name = '{config.get('app', 'name')}'")
        print(f"  정수:   database.pool_size = {config.getint('database', 'pool_size')}")
        print(f"  불리언: DEFAULT.debug = {config.getboolean('DEFAULT', 'debug')}")
        print(f"  기본값: app.없는키 = '{config.get('app', 'missing_key', fallback='기본값')}'")
        print()

        # --- 4단계: 설정값 수정 ---
        print("--- 4단계: 설정값 수정 ---")
        print()

        # ConfigManager 클래스 사용
        mgr = ConfigManager(config_file)

        # 설정값 변경
        changes = [
            ("app", "port", "9000"),
            ("app", "debug", "true"),
            ("database", "pool_size", "10"),
        ]

        for section, key, new_value in changes:
            old_value = mgr.get(section, key, fallback="(없음)")
            mgr.set(section, key, new_value)
            print(f"  {section}.{key}: '{old_value}' -> '{new_value}'")

        # 새 섹션 추가
        mgr.set("cache", "backend", "memory")
        mgr.set("cache", "ttl", "300")
        mgr.set("cache", "max_size", "1000")
        print(f"  새 섹션 [cache] 추가됨")

        mgr.save()
        print()
        print("  변경사항이 저장되었습니다.")
        print()

        # --- 5단계: 변경된 설정 확인 ---
        print("--- 5단계: 변경된 설정 확인 ---")
        print()

        # 파일을 다시 읽어서 확인
        mgr2 = ConfigManager(config_file)
        print(f"  app.port = {mgr2.get('app', 'port')}")
        print(f"  app.debug = {mgr2.get_bool('app', 'debug')}")
        print(f"  database.pool_size = {mgr2.get_int('database', 'pool_size')}")
        print(f"  cache.backend = {mgr2.get('cache', 'backend')}")
        print(f"  cache.ttl = {mgr2.get_int('cache', 'ttl')}")
        print(f"  cache 섹션 존재: {mgr2.has_section('cache')}")
        print()

        # --- 6단계: 섹션 삭제 ---
        print("--- 6단계: 섹션 삭제 ---")
        print()
        mgr2.remove_section("cache")
        mgr2.save()
        print(f"  [cache] 섹션이 삭제되었습니다.")
        print(f"  cache 섹션 존재: {mgr2.has_section('cache')}")
        print(f"  남은 섹션: {mgr2.sections()}")
        print()

        print("설정 파일 관리 예제를 성공적으로 실행했습니다!")

    finally:
        # 임시 파일 정리
        if os.path.exists(config_file):
            os.remove(config_file)
        os.rmdir(temp_dir)
        print("(임시 파일 정리 완료)")
