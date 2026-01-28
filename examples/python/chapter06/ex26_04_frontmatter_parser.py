"""
예제 26-04: 프론트매터 파싱

YAML과 유사한 프론트매터를 파이썬 표준 라이브러리만으로 파싱합니다.
블로그 글의 메타데이터(제목, 날짜, 태그, 저자 등)를
구조화된 딕셔너리로 변환합니다.
"""

import re
from datetime import datetime
from typing import Any, Optional


def parse_frontmatter(content: str) -> tuple:
    """마크다운 콘텐츠에서 프론트매터와 본문을 분리합니다.

    프론트매터는 문서 시작 부분의 --- 사이에 위치한
    key: value 형식의 메타데이터입니다.

    Args:
        content: 전체 마크다운 텍스트

    Returns:
        (프론트매터 딕셔너리, 본문 문자열) 튜플
    """
    # --- 로 둘러싸인 프론트매터 영역 감지
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
    match = re.match(pattern, content.strip(), re.DOTALL)

    if not match:
        return {}, content.strip()

    fm_text = match.group(1)
    body = match.group(2).strip()

    metadata = _parse_yaml_like(fm_text)
    return metadata, body


def _parse_yaml_like(text: str) -> dict:
    """간단한 YAML 형식의 텍스트를 딕셔너리로 파싱합니다.

    지원 형식:
    - key: value (문자열)
    - key: value1, value2 (쉼표 구분 리스트)
    - key: true/false (불린)
    - key: 123 (정수)
    - key: 2025-01-15 (날짜)

    Args:
        text: YAML 형식 텍스트

    Returns:
        파싱된 딕셔너리
    """
    result = {}
    current_key = None
    current_list = None

    for line in text.split("\n"):
        line = line.rstrip()

        # 빈 줄이나 주석 건너뛰기
        if not line.strip() or line.strip().startswith("#"):
            continue

        # 리스트 항목 (  - item 형식)
        list_match = re.match(r"^\s+-\s+(.+)$", line)
        if list_match and current_key:
            if current_list is None:
                current_list = []
            current_list.append(_convert_value(list_match.group(1).strip()))
            result[current_key] = current_list
            continue

        # key: value 형식
        kv_match = re.match(r"^(\w[\w\s]*?):\s*(.*)$", line)
        if kv_match:
            # 이전 리스트 저장
            if current_list is not None and current_key:
                result[current_key] = current_list

            current_key = kv_match.group(1).strip()
            value_str = kv_match.group(2).strip()
            current_list = None

            if value_str:
                # 쉼표 구분 리스트 감지
                if "," in value_str and not value_str.startswith('"'):
                    items = [_convert_value(v.strip()) for v in value_str.split(",")]
                    result[current_key] = items
                else:
                    result[current_key] = _convert_value(value_str)
            # value가 없으면 다음 줄의 리스트를 기대
            continue

    return result


def _convert_value(value: str) -> Any:
    """문자열 값을 적절한 파이썬 타입으로 변환합니다.

    Args:
        value: 변환할 문자열

    Returns:
        변환된 값 (str, int, float, bool, datetime)
    """
    # 따옴표 제거
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]

    # 불린
    if value.lower() in ("true", "yes"):
        return True
    if value.lower() in ("false", "no"):
        return False

    # 정수
    try:
        return int(value)
    except ValueError:
        pass

    # 실수
    try:
        return float(value)
    except ValueError:
        pass

    # 날짜 (YYYY-MM-DD 형식)
    date_match = re.match(r"^\d{4}-\d{2}-\d{2}$", value)
    if date_match:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

    # 날짜시간 (YYYY-MM-DD HH:MM 형식)
    datetime_match = re.match(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$", value)
    if datetime_match:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            pass

    return value


def format_frontmatter(metadata: dict) -> str:
    """딕셔너리를 프론트매터 문자열로 변환합니다.

    Args:
        metadata: 메타데이터 딕셔너리

    Returns:
        프론트매터 형식의 문자열
    """
    lines = ["---"]

    for key, value in metadata.items():
        if isinstance(value, list):
            # 리스트는 쉼표 구분으로 출력
            items = ", ".join(str(v) for v in value)
            lines.append(f"{key}: {items}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, datetime):
            lines.append(f"{key}: {value.strftime('%Y-%m-%d %H:%M')}")
        else:
            lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


# 테스트용 마크다운 샘플들
SAMPLE_POSTS = [
    # 기본 프론트매터
    """\
---
title: 바이브 코딩 시작하기
date: 2025-01-15
author: 바이브 코더
tags: 입문, 바이브코딩, AI
draft: false
reading_time: 5
---

# 바이브 코딩 시작하기

이 글에서는 바이브 코딩의 기초를 알아봅니다.
""",
    # 다양한 타입의 프론트매터
    """\
---
title: "고급 프롬프트 엔지니어링"
date: 2025-02-20
author: AI 마스터
tags: 프롬프트, 고급, 엔지니어링
featured: true
series: 바이브 코딩 마스터
episode: 3
---

# 고급 프롬프트 엔지니어링

프롬프트를 잘 작성하는 방법을 배워봅시다.
""",
    # 프론트매터가 없는 경우
    """\
# 프론트매터 없는 글

이 글에는 프론트매터가 없습니다.
그래도 정상적으로 처리할 수 있어야 합니다.
""",
]


if __name__ == "__main__":
    print("=" * 50)
    print("  프론트매터 파싱 데모")
    print("=" * 50)
    print()

    for i, sample in enumerate(SAMPLE_POSTS, 1):
        print(f"[샘플 {i}]")
        print("-" * 40)

        # 프론트매터 파싱
        metadata, body = parse_frontmatter(sample)

        if metadata:
            print("  프론트매터 항목:")
            for key, value in metadata.items():
                value_type = type(value).__name__
                if isinstance(value, list):
                    value_display = ", ".join(str(v) for v in value)
                    print(f"    {key}: [{value_display}] (리스트)")
                else:
                    print(f"    {key}: {value} ({value_type})")
        else:
            print("  프론트매터가 없습니다.")

        # 본문 미리보기
        preview = body[:80].replace("\n", " ")
        print(f"  본문 미리보기: {preview}...")
        print()

    # 프론트매터 생성 데모
    print("[프론트매터 생성 데모]")
    print("-" * 40)
    new_metadata = {
        "title": "새로운 블로그 글",
        "date": "2025-03-01",
        "author": "바이브 코더",
        "tags": ["파이썬", "블로그", "자동화"],
        "draft": False,
        "reading_time": 3,
    }

    fm_string = format_frontmatter(new_metadata)
    print("  생성된 프론트매터:")
    for line in fm_string.split("\n"):
        print(f"    {line}")
    print()

    # 왕복 검증: 생성 -> 파싱 -> 확인
    print("[왕복 검증 (생성 -> 파싱)]")
    print("-" * 40)
    full_content = fm_string + "\n\n본문 내용입니다."
    parsed_meta, parsed_body = parse_frontmatter(full_content)
    print("  파싱 결과:")
    for key, value in parsed_meta.items():
        print(f"    {key}: {value}")
    print(f"  본문: {parsed_body}")
    print()

    print("프론트매터 파싱 데모가 완료되었습니다!")
