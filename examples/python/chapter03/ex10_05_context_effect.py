"""
예제 10-5: 맥락 제공의 효과
===========================
프로젝트 맥락을 함께 제공하면 AI가 프로젝트에 맞는
구체적이고 적합한 코드를 생성합니다.

프롬프트 비교:
  [맥락 없음] "설정 파일 읽는 함수 만들어줘"
  [맥락 있음] "우리 프로젝트는 Python 3.11 기반 웹 크롤러입니다.
              설정은 YAML 형식이고 URL 목록, 크롤링 간격,
              출력 디렉토리를 포함합니다.
              설정 파일을 읽고 검증하는 함수를 작성해줘."
"""

import json
import os
import tempfile


# --- 맥락 없음: 일반적인 결과 ---
# 프롬프트: "설정 파일 읽는 함수 만들어줘"

def read_config_no_context(filepath):
    """맥락 없는 결과: 단순한 파일 읽기"""
    with open(filepath) as f:
        return f.read()


# --- 맥락 있음: 프로젝트에 맞는 결과 ---
# 프롬프트: "우리 프로젝트는 Python 3.11 기반 웹 크롤러입니다.
#           설정은 JSON 형식이고 다음 항목을 포함합니다:
#           - urls: 크롤링할 URL 목록 (필수, 1개 이상)
#           - interval: 크롤링 간격 초 (선택, 기본값 60)
#           - output_dir: 결과 저장 경로 (선택, 기본값 ./output)
#           설정 파일을 읽고 각 필드를 검증하는 함수를 작성해줘.
#           검증 실패 시 구체적인 에러 메시지를 반환해줘."

DEFAULT_CONFIG = {
    "interval": 60,
    "output_dir": "./output",
}

REQUIRED_FIELDS = ["urls"]


def load_crawler_config(filepath):
    """
    웹 크롤러 설정 파일을 읽고 검증합니다.

    Args:
        filepath: JSON 설정 파일 경로
    Returns:
        dict: 검증된 설정 딕셔너리
    Raises:
        FileNotFoundError: 파일이 없을 때
        ValueError: 설정 검증 실패 시
    """
    # 1. 파일 존재 확인
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {filepath}")

    # 2. JSON 파싱
    try:
        with open(filepath, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 오류: {e}")

    # 3. 필수 필드 확인
    for field in REQUIRED_FIELDS:
        if field not in config:
            raise ValueError(f"필수 필드 '{field}'가 누락되었습니다.")

    # 4. urls 검증
    if not isinstance(config["urls"], list) or len(config["urls"]) == 0:
        raise ValueError("'urls'는 1개 이상의 URL을 포함하는 리스트여야 합니다.")

    for i, url in enumerate(config["urls"]):
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ValueError(f"urls[{i}] 값이 올바른 URL이 아닙니다: {url}")

    # 5. interval 검증 (선택, 기본값 적용)
    interval = config.get("interval", DEFAULT_CONFIG["interval"])
    if not isinstance(interval, (int, float)) or interval <= 0:
        raise ValueError(f"'interval'은 양수여야 합니다. 현재 값: {interval}")
    config["interval"] = interval

    # 6. output_dir 검증 (선택, 기본값 적용)
    config["output_dir"] = config.get("output_dir", DEFAULT_CONFIG["output_dir"])

    return config


# ── 실행 ──
if __name__ == "__main__":
    # 정상 설정 파일
    good_config = {
        "urls": ["https://example.com", "https://example.org"],
        "interval": 30,
        "output_dir": "./crawled_data"
    }

    # 잘못된 설정 파일
    bad_config = {
        "interval": -10
        # urls 누락!
    }

    # 임시 파일 생성
    tmp_good = tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                            delete=False, encoding="utf-8")
    json.dump(good_config, tmp_good, ensure_ascii=False, indent=2)
    tmp_good.close()

    tmp_bad = tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                           delete=False, encoding="utf-8")
    json.dump(bad_config, tmp_bad, ensure_ascii=False, indent=2)
    tmp_bad.close()

    print("=" * 60)
    print("[맥락 없음] 단순 파일 읽기")
    content = read_config_no_context(tmp_good.name)
    print(f"  결과 타입: {type(content).__name__}")
    print(f"  내용: {content[:60]}...")
    print("  → 문자열만 반환. 파싱/검증 없음\n")

    print("=" * 60)
    print("[맥락 있음] 크롤러 전용 설정 로더\n")

    print("  1) 정상 설정 파일:")
    result = load_crawler_config(tmp_good.name)
    for key, val in result.items():
        print(f"     {key}: {val}")

    print("\n  2) 잘못된 설정 파일:")
    try:
        load_crawler_config(tmp_bad.name)
    except ValueError as e:
        print(f"     [검증 오류] {e}")

    print("\n  3) 존재하지 않는 파일:")
    try:
        load_crawler_config("nonexistent.json")
    except FileNotFoundError as e:
        print(f"     [파일 오류] {e}")

    os.unlink(tmp_good.name)
    os.unlink(tmp_bad.name)
