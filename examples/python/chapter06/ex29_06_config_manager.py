#!/usr/bin/env python3
"""
예제 29-06: 설정 관리
- configparser를 사용한 비서 앱 설정 관리
- 사용자 프로필, 표시 옵션, 알림 설정 등
- INI 형식 설정 파일 생성 및 수정
- 설정 가져오기/내보내기 지원
"""

import configparser
import json
import os
from datetime import datetime
from pathlib import Path


# ── 설정 ─────────────────────────────────────────────────────────────────

CONFIG_DIR = Path("/tmp/personal_assistant_config")
CONFIG_FILE = CONFIG_DIR / "settings.ini"
CONFIG_BACKUP_FILE = CONFIG_DIR / "settings_backup.ini"


# ── 기본 설정값 ──────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "사용자": {
        "이름": "사용자",
        "이메일": "",
        "도시": "서울",
        "언어": "한국어",
    },
    "화면": {
        "테마": "기본",        # 기본, 어두운, 밝은
        "색상_사용": "true",
        "날짜_형식": "YYYY-MM-DD",
        "시간_형식": "24시간",  # 24시간, 12시간
        "주_시작일": "월요일",   # 월요일, 일요일
    },
    "날씨": {
        "기본_도시": "서울",
        "온도_단위": "섭씨",    # 섭씨, 화씨
        "자동_갱신": "true",
        "갱신_간격_분": "30",
    },
    "일정": {
        "기본_카테고리": "일반",
        "미리_알림_분": "10",
        "주간_표시_일수": "7",
        "완료_자동_삭제": "false",
        "삭제_후_유지_일수": "30",
    },
    "메모": {
        "저장_디렉토리": "/tmp/personal_assistant_memos",
        "최대_메모_수": "1000",
        "자동_태그_추출": "true",
        "기본_편집기": "내장",
    },
    "알림": {
        "소리_사용": "true",
        "뽀모도로_작업_분": "25",
        "뽀모도로_휴식_분": "5",
        "뽀모도로_긴_휴식_분": "15",
        "뽀모도로_세트_수": "4",
    },
    "데이터": {
        "저장_디렉토리": "/tmp/personal_assistant",
        "자동_백업": "true",
        "백업_간격_시간": "24",
        "최대_백업_수": "5",
    },
}


# ── 설정 관리 클래스 ─────────────────────────────────────────────────────

class ConfigManager:
    """configparser 기반 설정 관리 클래스"""

    def __init__(self, config_file=CONFIG_FILE):
        """
        설정 관리자를 초기화합니다.

        Args:
            config_file: 설정 파일 경로
        """
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()
        # 대소문자 유지 (기본값은 소문자로 변환)
        self.config.optionxform = str
        self._load_or_create()

    def _load_or_create(self):
        """설정 파일을 불러오거나 기본값으로 새로 생성합니다."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        if self.config_file.exists():
            self.config.read(self.config_file, encoding="utf-8")
            print(f"  [설정 로드] {self.config_file}")
        else:
            self._apply_defaults()
            self._save()
            print(f"  [설정 생성] 기본 설정으로 초기화: {self.config_file}")

    def _apply_defaults(self):
        """기본 설정값을 적용합니다."""
        for section, values in DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in values.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, str(value))

    def _save(self):
        """설정을 파일에 저장합니다."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)

    # ── 설정 조회 ────────────────────────────────────────────

    def get(self, section, key, fallback=None):
        """
        설정값을 가져옵니다.

        Args:
            section: 섹션 이름
            key: 설정 키
            fallback: 기본값 (키가 없을 때)

        Returns:
            str: 설정값
        """
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        """불리언 설정값을 가져옵니다."""
        value = self.get(section, key, str(fallback))
        return value.lower() in ("true", "yes", "1", "on")

    def get_int(self, section, key, fallback=0):
        """정수 설정값을 가져옵니다."""
        try:
            return int(self.get(section, key, str(fallback)))
        except (ValueError, TypeError):
            return fallback

    def get_section(self, section):
        """
        특정 섹션의 모든 설정을 딕셔너리로 반환합니다.

        Args:
            section: 섹션 이름

        Returns:
            dict: 섹션의 키-값 쌍
        """
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}

    def list_sections(self):
        """모든 섹션 목록을 반환합니다."""
        return self.config.sections()

    # ── 설정 수정 ────────────────────────────────────────────

    def set(self, section, key, value):
        """
        설정값을 변경합니다.

        Args:
            section: 섹션 이름
            key: 설정 키
            value: 새로운 값
        """
        if not self.config.has_section(section):
            self.config.add_section(section)

        old_value = self.config.get(section, key, fallback=None)
        self.config.set(section, key, str(value))
        self._save()

        if old_value is not None:
            print(f"  [설정 변경] [{section}] {key}: '{old_value}' -> '{value}'")
        else:
            print(f"  [설정 추가] [{section}] {key} = '{value}'")

    def remove(self, section, key):
        """설정 항목을 제거합니다."""
        if self.config.has_option(section, key):
            self.config.remove_option(section, key)
            self._save()
            print(f"  [설정 제거] [{section}] {key}")
            return True
        print(f"  [오류] [{section}] {key}을(를) 찾을 수 없습니다.")
        return False

    def remove_section(self, section):
        """섹션 전체를 제거합니다."""
        if self.config.has_section(section):
            self.config.remove_section(section)
            self._save()
            print(f"  [섹션 제거] [{section}]")
            return True
        print(f"  [오류] [{section}] 섹션을 찾을 수 없습니다.")
        return False

    def reset_to_defaults(self):
        """모든 설정을 기본값으로 초기화합니다."""
        # 기존 설정 백업
        self.backup()

        # 설정 초기화
        for section in self.config.sections():
            self.config.remove_section(section)
        self._apply_defaults()
        self._save()
        print("  [초기화] 모든 설정이 기본값으로 복원되었습니다.")

    # ── 백업 / 내보내기 ──────────────────────────────────────

    def backup(self, backup_path=None):
        """설정 파일을 백업합니다."""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.config_file.parent / f"settings_backup_{timestamp}.ini"

        backup_path = Path(backup_path)
        with open(backup_path, "w", encoding="utf-8") as f:
            self.config.write(f)
        print(f"  [백업 완료] {backup_path}")
        return backup_path

    def export_json(self, output_path=None):
        """
        설정을 JSON 형식으로 내보냅니다.

        Args:
            output_path: 출력 파일 경로

        Returns:
            dict: 내보낸 설정 데이터
        """
        data = {}
        for section in self.config.sections():
            data[section] = dict(self.config.items(section))

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [JSON 내보내기] {output_path}")

        return data

    def import_json(self, input_path):
        """
        JSON 파일에서 설정을 가져옵니다.

        Args:
            input_path: JSON 설정 파일 경로
        """
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for section, values in data.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in values.items():
                self.config.set(section, key, str(value))

        self._save()
        print(f"  [JSON 가져오기] {input_path} -> 설정 적용 완료")

    # ── 검증 ─────────────────────────────────────────────────

    def validate(self):
        """설정값의 유효성을 검사합니다."""
        print("\n  ── 설정 검증 ──")
        issues = []

        # 필수 섹션 확인
        for section in DEFAULT_CONFIG:
            if not self.config.has_section(section):
                issues.append(f"  [누락] 섹션 '{section}'이(가) 없습니다.")

        # 값 범위 확인
        pomodoro_work = self.get_int("알림", "뽀모도로_작업_분")
        if pomodoro_work < 1 or pomodoro_work > 120:
            issues.append(f"  [범위] 뽀모도로 작업 시간이 비정상적: {pomodoro_work}분")

        reminder_min = self.get_int("일정", "미리_알림_분")
        if reminder_min < 0:
            issues.append(f"  [범위] 미리 알림 시간이 음수: {reminder_min}분")

        max_memos = self.get_int("메모", "최대_메모_수")
        if max_memos < 1:
            issues.append(f"  [범위] 최대 메모 수가 0 이하: {max_memos}")

        # 디렉토리 접근 확인
        data_dir = self.get("데이터", "저장_디렉토리")
        if data_dir:
            p = Path(data_dir)
            if p.exists() and not os.access(p, os.W_OK):
                issues.append(f"  [권한] 데이터 디렉토리 쓰기 불가: {data_dir}")

        if issues:
            print("  발견된 문제:")
            for issue in issues:
                print(f"    {issue}")
        else:
            print("  모든 설정이 유효합니다!")

        return len(issues) == 0


# ── 출력 함수들 ──────────────────────────────────────────────────────────

def display_all_settings(config_manager):
    """모든 설정을 보기 좋게 출력합니다."""
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         개인 비서 설정 현황               ║")
    print("  ╚══════════════════════════════════════════╝")

    for section in config_manager.list_sections():
        print(f"\n  [{section}]")
        items = config_manager.get_section(section)
        for key, value in items.items():
            # 불리언 값 한국어 표시
            display_value = value
            if value.lower() in ("true", "yes"):
                display_value = f"{value} (사용)"
            elif value.lower() in ("false", "no"):
                display_value = f"{value} (미사용)"

            print(f"    {key:<20} = {display_value}")

    print()


def display_section(config_manager, section):
    """특정 섹션의 설정을 출력합니다."""
    items = config_manager.get_section(section)
    if not items:
        print(f"  [{section}] 섹션을 찾을 수 없습니다.")
        return

    print(f"\n  ── [{section}] 설정 ──")
    for key, value in items.items():
        print(f"  {key}: {value}")
    print()


# ── 설정 마법사 (대화형 데모) ─────────────────────────────────────────────

def setup_wizard_demo(config_manager):
    """설정 마법사 데모 (자동 실행)를 보여줍니다."""
    print("\n  ═══ 초기 설정 마법사 (데모) ═══")
    print()

    # 시뮬레이션: 사용자 입력 없이 자동으로 설정
    demo_settings = [
        ("사용자", "이름", "홍길동"),
        ("사용자", "이메일", "hong@example.com"),
        ("사용자", "도시", "서울"),
        ("화면", "테마", "어두운"),
        ("화면", "시간_형식", "24시간"),
        ("날씨", "기본_도시", "서울"),
        ("날씨", "온도_단위", "섭씨"),
        ("알림", "뽀모도로_작업_분", "25"),
        ("알림", "뽀모도로_휴식_분", "5"),
    ]

    for section, key, value in demo_settings:
        config_manager.set(section, key, value)

    print("\n  초기 설정이 완료되었습니다!")


# ── 메인 데모 ────────────────────────────────────────────────────────────

def main():
    """설정 관리 기능 데모를 실행합니다."""
    print("=" * 55)
    print("  개인 비서 - 설정 관리 데모")
    print("=" * 55)

    # 기존 설정 초기화
    import shutil
    if CONFIG_DIR.exists():
        shutil.rmtree(CONFIG_DIR)

    # ── 1. 설정 파일 생성 ──
    print("\n--- [1단계] 설정 파일 생성 ---")
    config = ConfigManager()

    # ── 2. 전체 설정 표시 ──
    print("\n--- [2단계] 기본 설정 확인 ---")
    display_all_settings(config)

    # ── 3. 초기 설정 마법사 ──
    print("\n--- [3단계] 초기 설정 마법사 ---")
    setup_wizard_demo(config)

    # ── 4. 개별 설정 조회 ──
    print("\n--- [4단계] 개별 설정 조회 ---")
    user_name = config.get("사용자", "이름")
    city = config.get("날씨", "기본_도시")
    auto_tag = config.get_bool("메모", "자동_태그_추출")
    pomodoro = config.get_int("알림", "뽀모도로_작업_분")

    print(f"  사용자 이름: {user_name}")
    print(f"  기본 도시: {city}")
    print(f"  자동 태그 추출: {auto_tag}")
    print(f"  뽀모도로 작업 시간: {pomodoro}분")

    # ── 5. 특정 섹션 조회 ──
    print("\n--- [5단계] 섹션별 조회 ---")
    display_section(config, "알림")
    display_section(config, "사용자")

    # ── 6. 설정 변경 ──
    print("\n--- [6단계] 설정 변경 ---")
    config.set("화면", "테마", "밝은")
    config.set("날씨", "갱신_간격_분", "15")
    config.set("일정", "미리_알림_분", "15")

    # ── 7. 커스텀 설정 추가 ──
    print("\n--- [7단계] 커스텀 설정 추가 ---")
    config.set("단축키", "날씨_확인", "Ctrl+W")
    config.set("단축키", "일정_추가", "Ctrl+S")
    config.set("단축키", "메모_작성", "Ctrl+M")
    config.set("단축키", "타이머_시작", "Ctrl+T")

    # ── 8. 설정 검증 ──
    print("\n--- [8단계] 설정 검증 ---")
    config.validate()

    # ── 9. JSON 내보내기/가져오기 ──
    print("\n--- [9단계] JSON 내보내기/가져오기 ---")
    json_path = CONFIG_DIR / "settings_export.json"
    exported = config.export_json(json_path)
    print(f"  내보낸 섹션 수: {len(exported)}")

    # JSON 파일 내용 미리보기
    print(f"\n  JSON 파일 내용 (일부):")
    json_str = json.dumps(exported, ensure_ascii=False, indent=2)
    lines = json_str.split("\n")
    for line in lines[:15]:
        print(f"    {line}")
    if len(lines) > 15:
        print(f"    ... (총 {len(lines)}줄)")

    # 가져오기 테스트
    print()
    config.import_json(json_path)

    # ── 10. 백업 ──
    print("\n--- [10단계] 설정 백업 ---")
    backup_path = config.backup()

    # ── 11. 설정 초기화 테스트 ──
    print("\n--- [11단계] 설정 초기화 ---")
    config.reset_to_defaults()

    # ── 12. 최종 설정 파일 내용 ──
    print("\n--- [최종] 설정 파일 내용 ---")
    if CONFIG_FILE.exists():
        print(f"\n  파일: {CONFIG_FILE}")
        print("  " + "-" * 45)
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                print(f"  {line}", end="")
        print()
        print("  " + "-" * 45)

    # 파일 정보
    print(f"\n  ── 생성된 파일 목록 ──")
    for f in sorted(CONFIG_DIR.iterdir()):
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

    print()
    print("  설정 관리 데모가 완료되었습니다!")


if __name__ == "__main__":
    main()
