# Chapter 26: 프로젝트 2 - 마크다운 블로그 생성기

두 번째 프로젝트로 **마크다운 블로그 생성기**를 만들어봅니다. 마크다운(.md) 파일에 글을 작성하면 자동으로 HTML 블로그 사이트를 생성하는 도구입니다. 이 프로젝트에서는 파일 처리, 문자열 파싱, 템플릿 시스템, 빌드 자동화 등 실전 프로그래밍의 핵심 기술을 바이브 코딩으로 구현합니다. 파이썬 표준 라이브러리만으로 완성되므로, 별도의 외부 패키지 설치가 필요 없습니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- **정적 사이트 생성기**의 원리와 구조를 이해할 수 있다
- `pathlib`, `os`를 사용하여 **프로젝트 디렉토리 구조**를 자동 생성할 수 있다
- `configparser`로 **설정 파일(INI)**을 읽고 관리할 수 있다
- **정규식(re)**을 활용하여 마크다운 문법을 파싱할 수 있다
- 마크다운을 **HTML로 변환**하는 파서를 구현할 수 있다
- `string.Template`로 **템플릿 시스템**을 만들 수 있다
- 인덱스 페이지와 **태그 페이지**를 자동 생성할 수 있다
- 전체 **빌드 파이프라인**을 하나의 스크립트로 자동화할 수 있다
- AI에게 **단계별로 프로젝트를 요청**하는 바이브 코딩 워크플로우를 익힐 수 있다

---

## 26.1 프로젝트 개요

### 정적 사이트 생성기란?

**정적 사이트 생성기(Static Site Generator, SSG)**는 마크다운 같은 텍스트 파일을 HTML 웹 페이지로 변환하는 도구입니다. 블로그, 문서 사이트, 포트폴리오 등을 만들 때 널리 사용됩니다.

```
[작성 흐름]

글 작성 (마크다운)  -->  변환 엔진  -->  HTML 블로그 사이트
   hello.md              파싱 +           index.html
   python-tips.md        템플릿 적용       posts/hello.html
   ...                                    tags/파이썬.html
```

유명한 정적 사이트 생성기로는 Jekyll, Hugo, Gatsby 등이 있습니다. 이번 프로젝트에서는 이런 도구의 **핵심 원리**를 직접 구현하면서, 파이썬 표준 라이브러리만으로 어디까지 가능한지 체험합니다.

### 완성 목표

우리가 만들 블로그 생성기는 다음 기능을 갖춥니다:

| 기능 | 설명 |
|------|------|
| 프로젝트 구조 생성 | 디렉토리와 기본 파일을 자동으로 만듬 |
| 설정 파일 관리 | INI 형식으로 블로그 설정을 관리 |
| 마크다운 파싱 | 프론트매터와 본문을 분리하고 분석 |
| HTML 변환 | 마크다운 문법을 HTML 태그로 변환 |
| 코드 하이라이팅 | 코드 블록에 구문 색상 적용 |
| 템플릿 시스템 | 일관된 레이아웃으로 페이지 생성 |
| 인덱스 페이지 | 최신 글 목록을 보여주는 메인 페이지 |
| 태그 페이지 | 태그별 글 분류 페이지 |
| 빌드 자동화 | 한 번의 실행으로 전체 사이트 생성 |

### 사용하는 표준 라이브러리

```
os, pathlib       - 파일/디렉토리 관리
re                - 정규식 (마크다운 파싱)
html              - HTML 특수문자 이스케이프
string.Template   - HTML 템플릿 시스템
configparser      - INI 설정 파일 관리
datetime          - 날짜 처리
collections       - defaultdict (태그 분류)
shutil            - 디렉토리 정리
time              - 빌드 시간 측정
```

> **Tip:** 이 프로젝트는 외부 라이브러리 없이 파이썬 표준 라이브러리만 사용합니다. 바이브 코딩에서는 "표준 라이브러리만 사용해서 만들어줘"라고 제약 조건을 명시하면 AI가 이를 준수합니다.

### 바이브 코딩 전략

이 프로젝트에서는 다음 전략으로 AI에게 요청합니다:

1. **작은 단위로 나누기** - 한 번에 전체를 요청하지 않고, 기능별로 나누어 요청
2. **이전 결과 참조하기** - "앞에서 만든 함수를 활용해서..." 형태로 연결
3. **구체적 입출력 명시** - 입력 형식과 기대 출력을 명확히 설명
4. **점진적 통합** - 각 모듈을 테스트한 후 최종적으로 통합

---

## 26.2 Step 1: 프로젝트 구조 설정

### AI에게 첫 번째 요청

프로젝트의 뼈대부터 만들겠습니다. AI에게 다음과 같이 요청합니다:

```
프롬프트: "마크다운 블로그 프로젝트의 디렉토리 구조를 자동으로 생성하는
파이썬 스크립트를 만들어줘. content/posts, templates, static/css,
output/posts 등의 폴더와 기본 config.ini 파일, 샘플 마크다운 파일을
함께 생성해줘. pathlib를 사용하고, 생성 결과를 트리 구조로 출력해줘."
```

### 디렉토리 구조 생성

**예제 26-01: 블로그 프로젝트 디렉토리 구조 생성**

```python
# examples/python/chapter06/ex26_01_directory_structure.py
import os
from pathlib import Path


def create_blog_structure(base_dir: str) -> dict:
    """블로그 프로젝트의 디렉토리 구조를 생성합니다.

    Args:
        base_dir: 블로그 프로젝트 루트 경로

    Returns:
        생성된 디렉토리 및 파일 목록
    """
    base = Path(base_dir)

    # 블로그 프로젝트 디렉토리 구조 정의
    directories = [
        "content/posts",       # 마크다운 글 저장소
        "content/drafts",      # 초안 저장소
        "templates",           # HTML 템플릿
        "static/css",          # CSS 스타일시트
        "static/images",       # 이미지 파일
        "static/js",           # JavaScript 파일
        "output/posts",        # 생성된 HTML 글
        "output/tags",         # 태그 페이지
        "output/static",       # 정적 파일 복사본
    ]

    # 기본 파일 정의 (파일명: 초기 내용)
    default_files = {
        "config.ini": (
            "[blog]\n"
            "title = 나의 바이브 코딩 블로그\n"
            "author = 바이브 코더\n"
            "description = AI와 함께하는 코딩 이야기\n"
            "url = https://myblog.example.com\n"
            "language = ko\n"
            "\n"
            "[build]\n"
            "output_dir = output\n"
            "content_dir = content/posts\n"
            "template_dir = templates\n"
        ),
        "content/posts/hello-world.md": (
            "---\n"
            "title: 첫 번째 글\n"
            "date: 2025-01-15\n"
            "tags: 시작, 블로그\n"
            "---\n"
            "\n"
            "# 안녕하세요!\n"
            "\n"
            "이것은 마크다운 블로그의 첫 번째 글입니다.\n"
        ),
    }

    created = {"directories": [], "files": []}

    # 디렉토리 생성
    for dir_path in directories:
        full_path = base / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        created["directories"].append(str(full_path))

    # 기본 파일 생성
    for file_path, content in default_files.items():
        full_path = base / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        created["files"].append(str(full_path))

    return created
```

핵심 포인트를 살펴보겠습니다:

- `Path`를 사용하면 운영체제에 관계없이 경로를 안전하게 다룰 수 있습니다
- `mkdir(parents=True, exist_ok=True)`는 중간 디렉토리까지 한꺼번에 생성하고, 이미 있어도 오류가 발생하지 않습니다
- `write_text()`로 간편하게 파일을 생성합니다

**실행:**

```bash
$ python examples/python/chapter06/ex26_01_directory_structure.py
```

**결과:**

```
==================================================
  마크다운 블로그 프로젝트 구조 생성기
==================================================

[생성된 디렉토리] (9개)
  + content/posts/
  + content/drafts/
  + templates/
  + static/css/
  + static/images/
  + static/js/
  + output/posts/
  + output/tags/
  + output/static/

[생성된 파일] (4개)
  + config.ini (254 bytes)
  + content/posts/hello-world.md (153 bytes)
  + templates/.gitkeep (0 bytes)
  + static/css/.gitkeep (0 bytes)

[디렉토리 트리]
my-vibe-blog/
├── content/
│   ├── drafts/
│   └── posts/
│       └── hello-world.md
├── output/
│   ├── posts/
│   ├── static/
│   └── tags/
├── static/
│   ├── css/
│   │   └── .gitkeep
│   ├── images/
│   └── js/
├── templates/
│   └── .gitkeep
└── config.ini

블로그 프로젝트 구조가 성공적으로 생성되었습니다!
```

프로젝트의 골격이 만들어졌습니다. 각 디렉토리의 역할을 정리하면:

| 디렉토리 | 역할 |
|----------|------|
| `content/posts/` | 마크다운으로 작성한 블로그 글 |
| `content/drafts/` | 아직 공개하지 않은 초안 |
| `templates/` | HTML 템플릿 파일 |
| `static/css/` | CSS 스타일시트 |
| `output/` | 빌드된 HTML 결과물 |

### 설정 파일 관리

다음으로 AI에게 설정 파일 관리를 요청합니다:

```
프롬프트: "configparser를 사용해서 블로그 설정을 관리하는 클래스를 만들어줘.
기본 설정 생성, 파일 읽기/쓰기, 값 조회(문자열/정수/불린)를 지원하고,
설정을 보기 좋게 출력하는 기능도 포함해줘."
```

**예제 26-02: 블로그 설정 파일 관리**

```python
# examples/python/chapter06/ex26_02_config_file.py
import configparser
from pathlib import Path


class BlogConfig:
    """블로그 설정을 관리하는 클래스입니다."""

    # 기본 설정값 정의
    DEFAULTS = {
        "blog": {
            "title": "나의 블로그",
            "author": "작성자",
            "description": "블로그 설명을 입력하세요",
            "url": "https://example.com",
            "language": "ko",
            "posts_per_page": "10",
        },
        "build": {
            "output_dir": "output",
            "content_dir": "content/posts",
            "template_dir": "templates",
            "static_dir": "static",
            "clean_before_build": "yes",
        },
        "style": {
            "theme": "default",
            "syntax_highlight": "yes",
            "show_date": "yes",
            "show_tags": "yes",
            "show_author": "yes",
        },
    }

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()

    def create_default(self):
        """기본 설정 파일을 생성합니다."""
        for section, values in self.DEFAULTS.items():
            self.config[section] = values
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def load(self) -> bool:
        """설정 파일을 읽어옵니다."""
        if not self.config_path.exists():
            return False
        self.config.read(str(self.config_path), encoding="utf-8")
        return True

    def get(self, section: str, key: str, fallback: str = "") -> str:
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        return self.config.getint(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)
```

`configparser`는 파이썬 표준 라이브러리로, INI 형식의 설정 파일을 쉽게 관리할 수 있습니다. 섹션(`[blog]`, `[build]`)으로 설정을 그룹화하고, `get_bool()`이나 `get_int()`로 자동 타입 변환도 지원합니다.

**실행:**

```bash
$ python examples/python/chapter06/ex26_02_config_file.py
```

**결과:**

```
==================================================
  블로그 설정 파일 관리 데모
==================================================

[1단계] 기본 설정 파일 생성
----------------------------------------
설정 파일이 생성되었습니다: /tmp/my-vibe-blog/config.ini

[2단계] 생성된 설정 파일 내용
----------------------------------------
[blog]
title = 나의 블로그
author = 작성자
description = 블로그 설명을 입력하세요
url = https://example.com
language = ko
posts_per_page = 10

[build]
output_dir = output
content_dir = content/posts
template_dir = templates
static_dir = static
clean_before_build = yes

[style]
theme = default
syntax_highlight = yes
show_date = yes
show_tags = yes
show_author = yes

[3단계] 설정값 읽기
----------------------------------------
  블로그 제목: 나의 블로그
  저자: 작성자
  페이지당 글 수: 10 (정수)
  빌드 전 정리: True (불린)
  태그 표시: True (불린)

[4단계] 설정 수정
----------------------------------------
설정이 수정되었습니다.

[5단계] 수정된 설정 확인
----------------------------------------
[blog]
  title = 바이브 코딩 블로그
  author = AI 개발자
  posts_per_page = 5

[style]
  theme = dark

[seo]
  enable_sitemap = yes
  enable_rss = yes
  keywords = 바이브코딩, AI, 프로그래밍

설정 파일 관리 데모가 완료되었습니다!
```

> **Note:** `configparser`의 `getboolean()` 메서드는 `yes/no`, `true/false`, `on/off`, `1/0`을 모두 불린 값으로 자동 변환합니다. 설정 파일에서 매우 유용한 기능입니다.

---

## 26.3 Step 2: 마크다운 파싱

### AI에게 두 번째 요청

프로젝트 구조가 준비되었으니, 이제 마크다운 파일을 읽고 분석하는 기능을 만듭니다.

```
프롬프트: "마크다운 파일을 읽어서 프론트매터(---로 둘러싸인 메타데이터)와
본문을 분리하고, 제목, 단락, 코드 블록 등의 구조를 분석하는 클래스를
만들어줘. 정규식을 사용하고, 파일과 문자열 두 가지 방식으로 초기화할 수
있게 해줘."
```

### 마크다운 파일 읽기

블로그 글은 다음과 같은 형식의 마크다운 파일입니다:

```markdown
---
title: 파이썬으로 배우는 바이브 코딩
date: 2025-03-10
tags: 파이썬, 바이브코딩, 입문
author: 바이브 코더
---

# 파이썬으로 배우는 바이브 코딩

바이브 코딩은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다.

## 바이브 코딩이란?
...
```

`---`로 둘러싸인 부분이 **프론트매터(Front Matter)**로, 글의 메타데이터(제목, 날짜, 태그 등)를 담습니다. 그 아래가 마크다운 **본문**입니다.

**예제 26-03: 마크다운 파일 읽기**

```python
# examples/python/chapter06/ex26_03_read_markdown.py
import re
from pathlib import Path


class MarkdownReader:
    """마크다운 파일을 읽고 구조를 분석하는 클래스입니다."""

    def __init__(self, content: str):
        self.raw_content = content
        self.frontmatter = {}
        self.body = ""
        self._parse()

    def _parse(self):
        """프론트매터와 본문을 분리합니다."""
        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.match(pattern, self.raw_content, re.DOTALL)

        if match:
            fm_text = match.group(1)
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    self.frontmatter[key.strip()] = value.strip()
            self.body = match.group(2).strip()
        else:
            self.body = self.raw_content.strip()

    @classmethod
    def from_file(cls, file_path: str) -> "MarkdownReader":
        """파일에서 마크다운을 읽어옵니다."""
        content = Path(file_path).read_text(encoding="utf-8")
        return cls(content)

    def get_title(self) -> str:
        """글의 제목을 반환합니다."""
        if "title" in self.frontmatter:
            return self.frontmatter["title"]
        match = re.search(r"^#\s+(.+)$", self.body, re.MULTILINE)
        return match.group(1).strip() if match else "제목 없음"

    def get_headings(self) -> list:
        """본문의 모든 제목(heading)을 추출합니다."""
        headings = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", self.body, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text))
        return headings

    def get_code_blocks(self) -> list:
        """본문의 코드 블록을 추출합니다."""
        blocks = []
        pattern = r"```(\w*)\n(.*?)```"
        for match in re.finditer(pattern, self.body, re.DOTALL):
            language = match.group(1) or "text"
            code = match.group(2).strip()
            blocks.append((language, code))
        return blocks

    def summary(self) -> dict:
        """마크다운 문서의 요약 정보를 반환합니다."""
        return {
            "제목": self.get_title(),
            "프론트매터 항목": len(self.frontmatter),
            "제목(heading) 수": len(self.get_headings()),
            "코드 블록 수": len(self.get_code_blocks()),
        }
```

정규식 `r"^---\s*\n(.*?)\n---\s*\n(.*)$"`가 핵심입니다. `re.DOTALL` 플래그와 함께 사용하면 줄 바꿈을 포함한 전체 텍스트를 매칭할 수 있습니다. `(.*?)`는 **비탐욕적(non-greedy)** 매칭으로, 첫 번째 `---`와 두 번째 `---` 사이의 최소한의 내용만 매칭합니다.

**실행:**

```bash
$ python examples/python/chapter06/ex26_03_read_markdown.py
```

**결과:**

```
==================================================
  마크다운 파일 읽기 데모
==================================================

샘플 파일 생성: /tmp/my-vibe-blog/content/posts/vibe-coding-intro.md

[프론트매터]
----------------------------------------
  title: 파이썬으로 배우는 바이브 코딩
  date: 2025-03-10
  tags: 파이썬, 바이브코딩, 입문
  author: 바이브 코더

[제목 구조 (목차)]
----------------------------------------
  # 파이썬으로 배우는 바이브 코딩
    ## 바이브 코딩이란?
      ### 핵심 원칙
    ## 첫 번째 예제
    ## 마무리

[코드 블록]
----------------------------------------
  블록 1 (언어: python):
    def greet(name):
        return f"안녕하세요, {name}님!"

    print(greet("바이브 코더"))

[문서 요약]
----------------------------------------
  제목: 파이썬으로 배우는 바이브 코딩
  프론트매터 항목: 4
  제목(heading) 수: 5
  코드 블록 수: 1

마크다운 파일 분석이 완료되었습니다!
```

### 프론트매터 파싱 고도화

기본 파싱은 문자열만 처리하지만, 실제 블로그에서는 날짜, 불린, 리스트 등 **다양한 타입**이 필요합니다. AI에게 추가 요청합니다:

```
프롬프트: "프론트매터 파서를 더 정교하게 만들어줘. 문자열뿐 아니라
날짜(2025-01-15), 불린(true/false), 정수, 쉼표 구분 리스트 등
다양한 타입을 자동 감지하고 변환하는 기능을 추가해줘.
외부 라이브러리(PyYAML 등) 없이 표준 라이브러리만 사용해줘."
```

**예제 26-04: 프론트매터 파싱**

```python
# examples/python/chapter06/ex26_04_frontmatter_parser.py
import re
from datetime import datetime
from typing import Any


def parse_frontmatter(content: str) -> tuple:
    """마크다운 콘텐츠에서 프론트매터와 본문을 분리합니다.

    Returns:
        (프론트매터 딕셔너리, 본문 문자열) 튜플
    """
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
    match = re.match(pattern, content.strip(), re.DOTALL)

    if not match:
        return {}, content.strip()

    fm_text = match.group(1)
    body = match.group(2).strip()
    metadata = _parse_yaml_like(fm_text)
    return metadata, body


def _parse_yaml_like(text: str) -> dict:
    """간단한 YAML 형식의 텍스트를 딕셔너리로 파싱합니다."""
    result = {}
    for line in text.split("\n"):
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        kv_match = re.match(r"^(\w[\w\s]*?):\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1).strip()
            value_str = kv_match.group(2).strip()

            if value_str:
                # 쉼표 구분 리스트 감지
                if "," in value_str and not value_str.startswith('"'):
                    items = [_convert_value(v.strip()) for v in value_str.split(",")]
                    result[key] = items
                else:
                    result[key] = _convert_value(value_str)

    return result


def _convert_value(value: str) -> Any:
    """문자열 값을 적절한 파이썬 타입으로 변환합니다."""
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

    # 날짜 (YYYY-MM-DD)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

    return value
```

이 파서는 프론트매터의 값을 **자동으로 적절한 타입으로 변환**합니다:

| 입력 | 변환 결과 | 타입 |
|------|----------|------|
| `바이브 코딩` | `"바이브 코딩"` | str |
| `2025-01-15` | `date(2025, 1, 15)` | date |
| `true`, `yes` | `True` | bool |
| `5` | `5` | int |
| `파이썬, AI, 코딩` | `["파이썬", "AI", "코딩"]` | list |

**실행:**

```bash
$ python examples/python/chapter06/ex26_04_frontmatter_parser.py
```

**결과:**

```
==================================================
  프론트매터 파싱 데모
==================================================

[샘플 1]
----------------------------------------
  프론트매터 항목:
    title: 바이브 코딩 시작하기 (str)
    date: 2025-01-15 (date)
    author: 바이브 코더 (str)
    tags: [입문, 바이브코딩, AI] (리스트)
    draft: False (bool)
    reading_time: 5 (int)
  본문 미리보기: # 바이브 코딩 시작하기  이 글에서는 바이브 코딩의 기초를 알아봅니다....

[샘플 2]
----------------------------------------
  프론트매터 항목:
    title: 고급 프롬프트 엔지니어링 (str)
    date: 2025-02-20 (date)
    author: AI 마스터 (str)
    tags: [프롬프트, 고급, 엔지니어링] (리스트)
    featured: True (bool)
    series: 바이브 코딩 마스터 (str)
    episode: 3 (int)

[샘플 3]
----------------------------------------
  프론트매터가 없습니다.
  본문 미리보기: # 프론트매터 없는 글  이 글에는 프론트매터가 없습니다....

프론트매터 파싱 데모가 완료되었습니다!
```

> **Warning:** 이 파서는 학습 목적으로 만든 간단한 버전입니다. 실무에서는 `PyYAML` 같은 전용 라이브러리를 사용하는 것이 안전합니다. 하지만 "외부 의존성 없이 가볍게 만들기"를 목표로 할 때는 이 방식이 충분히 효과적입니다.

---

## 26.4 Step 3: HTML 변환

### AI에게 세 번째 요청

마크다운을 읽을 수 있게 되었으니, 이제 HTML로 변환하는 핵심 엔진을 만듭니다.

```
프롬프트: "마크다운 텍스트를 HTML로 변환하는 파서 클래스를 만들어줘.
정규식을 사용하고, 표준 라이브러리만 사용해줘.
지원할 문법: 제목(h1~h6), 볼드/이탤릭, 인라인 코드, 순서 있는/없는 목록,
코드 블록, 인용문, 링크, 이미지, 수평선, 단락.
각 요소를 별도 메서드로 처리하는 구조로 만들어줘."
```

### 마크다운 -> HTML 변환기

**예제 26-05: 마크다운 -> HTML 변환**

```python
# examples/python/chapter06/ex26_05_md_to_html.py
import re
import html


class MarkdownToHTML:
    """마크다운 텍스트를 HTML로 변환하는 파서 클래스입니다."""

    def convert(self, markdown_text: str) -> str:
        """마크다운 텍스트를 HTML로 변환합니다."""
        lines = markdown_text.split("\n")
        html_parts = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # 코드 블록 (``` ... ```)
            if line.strip().startswith("```"):
                block_html, consumed = self._process_code_block(lines, i)
                html_parts.append(block_html)
                i += consumed
                continue

            # 인용문 (> ...)
            if line.strip().startswith(">"):
                block_html, consumed = self._process_blockquote(lines, i)
                html_parts.append(block_html)
                i += consumed
                continue

            # 순서 없는 목록 (- 또는 * 시작)
            if re.match(r"^\s*[-*+]\s+", line):
                block_html, consumed = self._process_unordered_list(lines, i)
                html_parts.append(block_html)
                i += consumed
                continue

            # 순서 있는 목록 (1. 시작)
            if re.match(r"^\s*\d+\.\s+", line):
                block_html, consumed = self._process_ordered_list(lines, i)
                html_parts.append(block_html)
                i += consumed
                continue

            # 수평선 (---, ***, ___)
            if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\1]*$", line):
                html_parts.append("<hr>")
                i += 1
                continue

            # 제목 (# ~ ######)
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
            if heading_match:
                level = len(heading_match.group(1))
                text = self._process_inline(heading_match.group(2))
                html_parts.append(f'<h{level}>{text}</h{level}>')
                i += 1
                continue

            # 빈 줄
            if not line.strip():
                i += 1
                continue

            # 일반 단락
            block_html, consumed = self._process_paragraph(lines, i)
            html_parts.append(block_html)
            i += consumed

        return "\n".join(html_parts)

    def _process_inline(self, text: str) -> str:
        """인라인 마크다운 요소를 HTML로 변환합니다."""
        # 볼드+이탤릭 (***text***)
        text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
        # 볼드 (**text**)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # 이탤릭 (*text*)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        # 인라인 코드 (`code`)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        # 이미지 (![alt](src))
        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
        # 링크 ([text](url))
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        return text

    def _process_code_block(self, lines: list, start: int) -> tuple:
        """코드 블록을 처리합니다."""
        first_line = lines[start].strip()
        language = first_line[3:].strip()
        code_lines = []
        i = start + 1

        while i < len(lines):
            if lines[i].strip() == "```":
                i += 1
                break
            code_lines.append(html.escape(lines[i]))
            i += 1

        code_text = "\n".join(code_lines)
        lang_attr = f' class="language-{language}"' if language else ""
        result = f"<pre><code{lang_attr}>{code_text}</code></pre>"
        return result, i - start
```

변환기의 핵심 구조는 **줄 단위 순회**입니다. 현재 줄이 어떤 마크다운 요소인지 판별하고, 해당하는 처리 메서드를 호출합니다:

```
while i < len(lines):
    line = lines[i]

    if 코드 블록?    --> _process_code_block()
    if 인용문?       --> _process_blockquote()
    if 순서 없는 목록? --> _process_unordered_list()
    if 순서 있는 목록? --> _process_ordered_list()
    if 제목?         --> 직접 처리 (한 줄)
    else             --> _process_paragraph()
```

각 블록 처리 메서드는 `(HTML 문자열, 소비한 줄 수)` 튜플을 반환하여, 다음에 처리할 줄의 위치를 알려줍니다.

**실행:**

```bash
$ python examples/python/chapter06/ex26_05_md_to_html.py
```

**결과:**

```
============================================================
  마크다운 -> HTML 변환 데모
============================================================

[마크다운 원본 (처음 15줄)]
--------------------------------------------------
  # 바이브 코딩 입문 가이드

  바이브 코딩은 **AI와 함께** 프로그래밍하는 *새로운 방식*입니다.
  자세한 내용은 [공식 문서](https://example.com)를 참고하세요.

  ## 핵심 개념
  ...

[변환된 HTML]
--------------------------------------------------
  <h1 id="바이브-코딩-입문-가이드">바이브 코딩 입문 가이드</h1>
  <p>바이브 코딩은 <strong>AI와 함께</strong> 프로그래밍하는 <em>새로운 방식</em>입니다.
     자세한 내용은 <a href="https://example.com">공식 문서</a>를 참고하세요.</p>
  <h2 id="핵심-개념">핵심 개념</h2>
  <p>바이브 코딩에서 가장 중요한 것은 <strong><em>자연어 소통 능력</em></strong>입니다.</p>
  <h3 id="준비물">준비물</h3>
  <ul>
    <li>AI 어시스턴트 (Claude 등)</li>
    <li>터미널 또는 에디터</li>
    <li><strong>호기심</strong>과 <em>인내심</em></li>
  </ul>
  ...

[변환 통계]
--------------------------------------------------
  <h1>: 1개, <h2>: 2개, <h3>: 2개
  <p>: 6개, <ul>: 1개, <ol>: 1개
  <pre>: 1개, <blockquote>: 1개
  <strong>: 4개, <em>: 3개

마크다운 -> HTML 변환 데모가 완료되었습니다!
```

변환기가 마크다운의 주요 문법을 올바르게 HTML로 변환하고 있습니다.

### 코드 하이라이팅

블로그에 코드가 포함될 때, 키워드에 색상을 입히면 가독성이 크게 좋아집니다.

```
프롬프트: "코드 블록에 구문 하이라이팅을 적용하는 함수를 만들어줘.
Python, JavaScript, Bash 언어의 키워드, 문자열, 주석, 숫자에
CSS 클래스를 적용하는 방식으로 구현해줘. 정규식을 사용하고,
문자열과 주석이 키워드 하이라이팅에 영향받지 않도록 보호해줘."
```

**예제 26-06: 코드 하이라이팅**

```python
# examples/python/chapter06/ex26_06_code_highlight.py
import re
import html as html_module

# 언어별 키워드 정의
LANGUAGE_KEYWORDS = {
    "python": {
        "keywords": [
            "def", "class", "if", "elif", "else", "for", "while",
            "return", "import", "from", "as", "try", "except",
            "finally", "with", "yield", "lambda", "pass", "break",
            "continue", "raise", "and", "or", "not", "in", "is",
            "True", "False", "None", "async", "await", "print",
        ],
        "comment": r"#.*$",
        "string": r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')',
        "number": r"\b\d+(?:\.\d+)?\b",
    },
    "javascript": {
        "keywords": [
            "function", "const", "let", "var", "if", "else", "for",
            "while", "return", "class", "import", "export", "from",
            "new", "this", "try", "catch", "async", "await",
            "true", "false", "null", "undefined",
        ],
        "comment": r"//.*$",
        "string": r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)',
        "number": r"\b\d+(?:\.\d+)?\b",
    },
}


def highlight_code(code: str, language: str = "text") -> str:
    """코드에 구문 하이라이팅을 적용하여 HTML을 생성합니다."""
    escaped = html_module.escape(code)

    if language not in LANGUAGE_KEYWORDS:
        return f'<pre><code class="language-{language}">{escaped}</code></pre>'

    lang_config = LANGUAGE_KEYWORDS[language]
    result = escaped

    # 1단계: 문자열 보호 (플레이스홀더로 임시 대체)
    string_placeholders = {}
    counter = [0]

    def replace_string(match):
        placeholder = f"__STR_{counter[0]}__"
        string_placeholders[placeholder] = (
            f'<span class="hl-string">{match.group(0)}</span>'
        )
        counter[0] += 1
        return placeholder

    if "string" in lang_config:
        result = re.sub(lang_config["string"], replace_string, result)

    # 2단계: 주석 하이라이팅 (플레이스홀더 보호)
    comment_placeholders = {}

    def replace_comment(match):
        placeholder = f"__CMT_{counter[0]}__"
        comment_placeholders[placeholder] = (
            f'<span class="hl-comment">{match.group(0)}</span>'
        )
        counter[0] += 1
        return placeholder

    if "comment" in lang_config:
        result = re.sub(lang_config["comment"], replace_comment,
                        result, flags=re.MULTILINE)

    # 3단계: 키워드 하이라이팅
    for keyword in lang_config["keywords"]:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        result = re.sub(
            pattern,
            f'<span class="hl-keyword">{keyword}</span>',
            result
        )

    # 4단계: 플레이스홀더 복원
    for ph, replacement in comment_placeholders.items():
        result = result.replace(ph, replacement)
    for ph, replacement in string_placeholders.items():
        result = result.replace(ph, replacement)

    return f'<pre><code class="language-{language}">{result}</code></pre>'
```

하이라이팅의 핵심 기법은 **플레이스홀더 보호** 패턴입니다:

```
1. 문자열 찾기 --> 임시 코드로 대체 (__STR_0__, __STR_1__, ...)
2. 주석 찾기   --> 임시 코드로 대체 (__CMT_0__, __CMT_1__, ...)
3. 키워드 처리 --> 문자열/주석 안의 키워드는 이미 보호됨!
4. 임시 코드를 원래 하이라이팅된 HTML로 복원
```

이렇게 하면 문자열 `"return value"` 안의 `return`이 키워드로 잘못 처리되는 것을 방지할 수 있습니다.

**실행:**

```bash
$ python examples/python/chapter06/ex26_06_code_highlight.py
```

**결과:**

```
============================================================
  코드 하이라이팅 데모
============================================================

[PYTHON 코드 하이라이팅]
--------------------------------------------------
  키워드: 7개
  문자열: 0개
  주석: 3개
  숫자: 0개
  HTML 크기: 973 bytes

[JAVASCRIPT 코드 하이라이팅]
--------------------------------------------------
  키워드: 14개
  문자열: 1개
  주석: 1개
  숫자: 0개
  HTML 크기: 1377 bytes

[BASH 코드 하이라이팅]
--------------------------------------------------
  키워드: 8개
  문자열: 0개
  주석: 4개
  숫자: 1개
  HTML 크기: 940 bytes

코드 하이라이팅 데모가 완료되었습니다!
```

> **Tip:** 하이라이팅에서 사용하는 CSS 클래스(`hl-keyword`, `hl-string`, `hl-comment` 등)는 나중에 CSS 파일에서 색상을 지정합니다. 다크 테마라면 키워드는 파란색(`#569cd6`), 문자열은 주황색(`#ce9178`), 주석은 초록색(`#6a9955`) 같은 VS Code 스타일이 인기 있습니다.

---

## 26.5 Step 4: 템플릿 시스템

### AI에게 네 번째 요청

변환된 HTML 본문을 블로그 페이지로 완성하려면 **레이아웃 템플릿**이 필요합니다.

```
프롬프트: "string.Template을 사용해서 블로그용 HTML 템플릿 시스템을 만들어줘.
기본 레이아웃(헤더, 네비게이션, 푸터), 글 페이지, 글 목록 카드,
태그 링크 등의 템플릿을 정의하고, TemplateManager 클래스로 관리해줘.
기본 CSS 스타일도 포함해줘. 한국어 블로그에 맞게 디자인해줘."
```

### HTML 템플릿 정의

**예제 26-07: 기본 HTML 템플릿**

```python
# examples/python/chapter06/ex26_07_html_template.py
from string import Template

# 기본 레이아웃 템플릿 (모든 페이지의 뼈대)
BASE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="${lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${description}">
    <title>${title} - ${site_name}</title>
    <style>
${css}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title"><a href="/">${site_name}</a></h1>
            <nav class="site-nav">${navigation}</nav>
        </div>
    </header>
    <main class="container">
        ${content}
    </main>
    <footer class="site-footer">
        <div class="container">
            <p>&copy; ${year} ${author}. ${footer_text}</p>
        </div>
    </footer>
</body>
</html>
""")

# 글 페이지 템플릿
POST_TEMPLATE = Template("""\
<article class="post">
    <header class="post-header">
        <h1 class="post-title">${title}</h1>
        <div class="post-meta">
            <time datetime="${date}">${date_display}</time>
            <span class="post-author">| ${author}</span>
        </div>
        <div class="post-tags">${tags_html}</div>
    </header>
    <div class="post-content">${content}</div>
</article>
""")

# 태그 링크 템플릿
TAG_LINK_TEMPLATE = Template("""\
<a href="/tags/${slug}.html" class="tag">#${name}</a>
""")
```

`string.Template`은 파이썬 표준 라이브러리의 간단한 템플릿 엔진입니다. `${변수명}` 형식으로 자리표시자를 만들고, `substitute()` 메서드로 실제 값을 채워 넣습니다.

```python
class TemplateManager:
    """블로그 HTML 템플릿을 관리하는 클래스입니다."""

    def __init__(self, site_config: dict):
        self.config = site_config

    def render_tag_links(self, tags: list) -> str:
        """태그 목록을 HTML 링크로 변환합니다."""
        links = []
        for tag in tags:
            tag_name = tag.strip()
            tag_slug = tag_name.replace(" ", "-").lower()
            links.append(TAG_LINK_TEMPLATE.substitute(
                slug=tag_slug, name=tag_name
            ))
        return " ".join(links)

    def render_base(self, title: str, content: str, description: str = "") -> str:
        """기본 레이아웃으로 페이지를 렌더링합니다."""
        return BASE_TEMPLATE.substitute(
            lang=self.config.get("language", "ko"),
            title=title,
            site_name=self.config.get("title", "내 블로그"),
            description=description,
            author=self.config.get("author", ""),
            year=self.config.get("year", "2025"),
            navigation='<a href="/">홈</a> <a href="/tags/">태그</a>',
            content=content,
            css=DEFAULT_CSS,
            footer_text="바이브 코딩으로 만든 블로그",
        )
```

**실행:**

```bash
$ python examples/python/chapter06/ex26_07_html_template.py
```

**결과:**

```
============================================================
  HTML 템플릿 시스템 데모
============================================================

[1] 태그 링크 HTML
----------------------------------------
  <a href="/tags/파이썬.html" class="tag">#파이썬</a>
  <a href="/tags/바이브코딩.html" class="tag">#바이브코딩</a>
  <a href="/tags/ai.html" class="tag">#AI</a>

[2] 글 카드 HTML
----------------------------------------
  <article class="post-card">
      <h2 class="post-card-title">
          <a href="/posts/hello-world.html">바이브 코딩 시작하기</a>
      </h2>
      <div class="post-card-meta">
          <time datetime="2025-01-15">2025년 1월 15일</time>
          <span class="post-card-author">| 바이브 코더</span>
      </div>
      <p class="post-card-excerpt">바이브 코딩은 AI와 자연어로 소통하며...</p>
  </article>

[4] 전체 페이지 렌더링
----------------------------------------
  전체 HTML 크기: 4277 bytes
  전체 줄 수: 154줄

[5] 템플릿 파일 저장
----------------------------------------
  저장됨: base.html (816 bytes)
  저장됨: post.html (568 bytes)
  저장됨: post_list_item.html (391 bytes)
  저장됨: style.css (2618 bytes)

HTML 템플릿 시스템 데모가 완료되었습니다!
```

### 템플릿 렌더링 파이프라인

이제 앞서 만든 모듈들을 **통합**합니다. 마크다운 파일을 읽어서 프론트매터 파싱, HTML 변환, 템플릿 적용까지 한 번에 처리하는 렌더러를 만듭니다.

```
프롬프트: "앞에서 만든 프론트매터 파서, 마크다운-HTML 변환기, 템플릿
시스템을 통합해서, 마크다운 파일을 완전한 블로그 HTML 페이지로
렌더링하는 BlogRenderer 클래스를 만들어줘.
render_post(markdown_content)와 render_file(input_path, output_path)
메서드를 제공해줘."
```

**예제 26-08: 템플릿 렌더링**

```python
# examples/python/chapter06/ex26_08_template_render.py
from datetime import datetime
from pathlib import Path

class BlogRenderer:
    """마크다운 파일을 완전한 블로그 HTML 페이지로 렌더링합니다."""

    def __init__(self, site_name: str = "바이브 코딩 블로그",
                 author: str = "바이브 코더"):
        self.site_name = site_name
        self.author = author

    def render_post(self, markdown_content: str) -> str:
        """마크다운 콘텐츠를 완전한 HTML 페이지로 렌더링합니다."""
        # 1. 프론트매터 파싱
        metadata, body = parse_frontmatter(markdown_content)

        # 2. 마크다운 -> HTML 변환
        body_html = markdown_to_html(body)

        # 3. 메타데이터 추출
        title = metadata.get("title", "제목 없음")
        date = metadata.get("date", "")
        author = metadata.get("author", self.author)
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        # 4. 날짜 포맷
        date_display = date
        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                date_display = dt.strftime("%Y년 %m월 %d일")
            except ValueError:
                pass

        # 5. 태그 HTML 생성
        tags_html = ""
        if tags:
            tag_links = [f'<span class="tag">#{t}</span>' for t in tags]
            tags_html = "| " + " ".join(tag_links)

        # 6. 템플릿에 렌더링
        return PAGE_TEMPLATE.substitute(
            title=title, site_name=self.site_name,
            date_display=date_display, author=author,
            tags_html=tags_html, content=body_html,
            year=datetime.now().year,
        )

    def render_file(self, input_path: str, output_path: str) -> dict:
        """마크다운 파일을 읽어 HTML 파일로 렌더링합니다."""
        md_content = Path(input_path).read_text(encoding="utf-8")
        html_content = self.render_post(md_content)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html_content, encoding="utf-8")

        metadata, _ = parse_frontmatter(md_content)
        return {
            "input": input_path,
            "output": output_path,
            "title": metadata.get("title", "제목 없음"),
            "size": output.stat().st_size,
        }
```

렌더링 파이프라인은 다음 단계를 거칩니다:

```
마크다운 파일 (.md)
    │
    ├── 1. 파일 읽기 (Path.read_text)
    │
    ├── 2. 프론트매터 분리 (parse_frontmatter)
    │       → 메타데이터: {title, date, tags, author}
    │       → 본문: 마크다운 텍스트
    │
    ├── 3. 마크다운 → HTML (markdown_to_html)
    │       → 본문 HTML
    │
    ├── 4. 메타데이터 가공
    │       → 날짜 포맷, 태그 링크 생성
    │
    └── 5. 템플릿 적용 (PAGE_TEMPLATE.substitute)
            → 완전한 HTML 페이지
```

**실행:**

```bash
$ python examples/python/chapter06/ex26_08_template_render.py
```

**결과:**

```
============================================================
  블로그 템플릿 렌더링 데모
============================================================

[1단계] 샘플 마크다운 파일 생성
----------------------------------------
  생성: vibe-coding-intro.md
  생성: python-tips.md

[2단계] HTML 렌더링
----------------------------------------
  변환: hello-world.md -> hello-world.html
         제목: 첫 번째 글
         크기: 1894 bytes

  변환: python-tips.md -> python-tips.html
         제목: 바이브 코딩을 위한 파이썬 팁
         크기: 2676 bytes

  변환: vibe-coding-intro.md -> vibe-coding-intro.html
         제목: 바이브 코딩이란 무엇인가
         크기: 2858 bytes

[결과 요약]
----------------------------------------
  변환된 글: 3개
  총 HTML 크기: 7,428 bytes

블로그 렌더링 데모가 완료되었습니다!
```

> **Note:** 각 모듈을 독립적으로 테스트한 후 통합하는 방식은 바이브 코딩에서 매우 효과적입니다. AI에게 "앞에서 만든 `parse_frontmatter`와 `markdown_to_html` 함수를 사용해서 통합 렌더러를 만들어줘"라고 요청하면, AI가 기존 코드의 인터페이스를 이해하고 자연스럽게 연결합니다.

---

## 26.6 Step 5: 인덱스 및 태그 페이지 생성

### AI에게 다섯 번째 요청

개별 글 페이지는 완성되었습니다. 이제 블로그의 **메인 페이지(인덱스)**와 **태그별 분류 페이지**를 만듭니다.

```
프롬프트: "블로그의 인덱스(메인) 페이지를 생성하는 기능을 만들어줘.
content/posts/ 디렉토리의 모든 마크다운 파일을 읽어서,
글 제목, 날짜, 요약(첫 150자), 태그를 카드 형태로 보여주는
목록 페이지를 만들어줘. 날짜 역순(최신 글이 위)으로 정렬해줘."
```

### 글 목록(인덱스) 페이지

**예제 26-09: 글 목록(인덱스) 페이지 생성**

```python
# examples/python/chapter06/ex26_09_index_page.py
import re
from pathlib import Path
from datetime import datetime


def extract_excerpt(body: str, max_length: int = 150) -> str:
    """본문에서 요약(발췌)을 추출합니다."""
    # 제목 제거
    text = re.sub(r"^#{1,6}\s+.+$", "", body, flags=re.MULTILINE)
    # 코드 블록 제거
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # 마크다운 문법 제거
    text = re.sub(r"[*_`\[\]()!#]", "", text)
    # 공백 정리
    text = " ".join(text.split()).strip()

    if len(text) > max_length:
        text = text[:max_length]
        last_space = text.rfind(" ")
        if last_space > max_length // 2:
            text = text[:last_space]
        text += "..."

    return text


def collect_posts(posts_dir: str) -> list:
    """디렉토리에서 모든 마크다운 글의 메타데이터를 수집합니다."""
    posts = []
    posts_path = Path(posts_dir)

    for md_file in posts_path.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)

        # 날짜 파싱
        date_str = metadata.get("date", "")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            date_obj = datetime.min

        # 태그 처리
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        post_info = {
            "filename": md_file.stem,
            "title": metadata.get("title", md_file.stem),
            "date": date_str,
            "date_obj": date_obj,
            "date_display": date_obj.strftime("%Y년 %m월 %d일"),
            "author": metadata.get("author", ""),
            "tags": tags,
            "excerpt": extract_excerpt(body),
            "url": f"/posts/{md_file.stem}.html",
        }
        posts.append(post_info)

    # 날짜 역순 정렬 (최신 글이 위로)
    posts.sort(key=lambda p: p["date_obj"], reverse=True)
    return posts
```

`extract_excerpt()` 함수는 마크다운 본문에서 **읽기 좋은 요약**을 추출합니다. 코드 블록과 마크다운 문법을 제거한 후 일정 길이로 자릅니다. 단어 중간이 아닌 **단어 경계에서 자르는** 것이 포인트입니다.

**실행:**

```bash
$ python examples/python/chapter06/ex26_09_index_page.py
```

**결과:**

```
============================================================
  글 목록(인덱스) 페이지 생성 데모
============================================================

[2단계] 글 목록 수집 (날짜 역순)
----------------------------------------
  1. [2025-03-01] 마크다운 블로그 생성기 만들기
     태그: 프로젝트, 파이썬, 블로그
     요약: 파이썬 표준 라이브러리만으로 정적 블로그 생성기를 만들어봅시다...

  2. [2025-02-15] 효과적인 프롬프트 작성법
     태그: 프롬프트, 고급, 바이브코딩
     요약: 좋은 프롬프트를 작성하면 AI로부터 더 나은 결과를 얻을 수 있습니다...

  3. [2025-02-01] 바이브 코딩을 위한 파이썬 팁
     태그: 파이썬, 팁, 초급
     요약: 바이브 코딩에서 자주 사용하는 파이썬 패턴을 소개합니다...

  4. [2025-01-15] 바이브 코딩이란 무엇인가
     태그: 바이브코딩, 입문, AI

[3단계] 인덱스 페이지 생성
----------------------------------------
  인덱스 페이지 저장: /tmp/my-vibe-blog/output/index.html
  파일 크기: 6,700 bytes
  포함된 글 수: 5개

인덱스 페이지 생성 데모가 완료되었습니다!
```

### 태그 페이지

블로그 글을 태그별로 분류하면 독자가 관심 주제를 쉽게 찾을 수 있습니다.

```
프롬프트: "글을 태그별로 분류해서, 전체 태그 목록 페이지(태그 클라우드)와
각 태그별 개별 페이지를 생성하는 기능을 만들어줘.
collections.defaultdict를 사용하고, 태그를 글 수 내림차순으로
정렬해줘. 한국어 태그도 슬러그로 변환하는 함수를 포함해줘."
```

**예제 26-10: 태그 페이지 생성**

```python
# examples/python/chapter06/ex26_10_tag_page.py
from collections import defaultdict


def collect_posts_by_tag(posts_dir: str) -> tuple:
    """글을 태그별로 분류합니다.

    Returns:
        (태그별 글 딕셔너리, 전체 글 리스트) 튜플
    """
    tags_map = defaultdict(list)  # {태그이름: [글 정보 리스트]}
    all_posts = []

    for md_file in sorted(Path(posts_dir).glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)

        # 태그 파싱
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        post_info = {
            "filename": md_file.stem,
            "title": metadata.get("title", md_file.stem),
            "date": metadata.get("date", ""),
            "author": metadata.get("author", ""),
            "tags": tags,
            "url": f"/posts/{md_file.stem}.html",
        }
        all_posts.append(post_info)

        # 각 태그에 글 추가
        for tag in tags:
            tags_map[tag].append(post_info)

    return dict(tags_map), all_posts


def tag_slug(tag_name: str) -> str:
    """태그 이름을 URL 슬러그로 변환합니다."""
    return tag_name.strip().replace(" ", "-").lower()
```

`defaultdict(list)`는 존재하지 않는 키에 접근하면 자동으로 빈 리스트를 생성합니다. 태그별 글 분류처럼 **그룹핑** 작업에 매우 유용합니다:

```python
# 일반 딕셔너리 (번거로움)
tags = {}
if tag not in tags:
    tags[tag] = []
tags[tag].append(post)

# defaultdict (간결함)
tags = defaultdict(list)
tags[tag].append(post)  # 키가 없어도 자동 생성!
```

**실행:**

```bash
$ python examples/python/chapter06/ex26_10_tag_page.py
```

**결과:**

```
============================================================
  태그 페이지 생성 데모
============================================================

[2단계] 태그별 글 분류
----------------------------------------
  #바이브코딩 (4개)
    - AI 코딩의 미래 (2025-03-10)
    - 마크다운 블로그 생성기 만들기 (2025-03-01)
    - 바이브 코딩을 위한 파이썬 팁 (2025-02-01)
    - 바이브 코딩이란 무엇인가 (2025-01-15)
  #AI (3개)
    - AI 코딩의 미래 (2025-03-10)
    - 효과적인 프롬프트 작성법 (2025-02-15)
    - 바이브 코딩이란 무엇인가 (2025-01-15)
  #고급 (2개)
    - AI 코딩의 미래 (2025-03-10)
    - 효과적인 프롬프트 작성법 (2025-02-15)
  #파이썬 (2개)
    - 마크다운 블로그 생성기 만들기 (2025-03-01)
    - 바이브 코딩을 위한 파이썬 팁 (2025-02-01)

[3단계] 태그 인덱스 페이지 생성
----------------------------------------
  저장: /tmp/my-vibe-blog/output/tags/index.html (3,484 bytes)

[4단계] 개별 태그 페이지 생성
----------------------------------------
  #바이브코딩 -> 바이브코딩.html (3,007 bytes, 4개 글)
  #AI -> ai.html (2,790 bytes, 3개 글)
  #고급 -> 고급.html (2,599 bytes, 2개 글)
  #파이썬 -> 파이썬.html (2,625 bytes, 2개 글)

[결과 요약]
----------------------------------------
  총 태그 수: 11개
  총 글 수: 6개
  생성된 HTML 파일: 12개

태그 페이지 생성 데모가 완료되었습니다!
```

태그 시스템이 완성되었습니다. 태그 인덱스 페이지에는 모든 태그가 글 수와 함께 **태그 클라우드** 형태로 표시되고, 각 태그를 클릭하면 해당 태그의 글 목록 페이지로 이동합니다.

> **Tip:** 태그 이름이 한국어인 경우 URL에 한국어가 포함됩니다. 실제 서비스에서는 `urllib.parse.quote()`로 URL 인코딩하거나, 영문 슬러그를 별도로 지정하는 것이 좋습니다. 이 프로젝트에서는 학습 목적으로 간단히 처리합니다.

---

## 26.7 Step 6: 빌드 자동화

### AI에게 마지막 요청

모든 모듈이 준비되었습니다. 마지막으로 전체를 통합하는 **빌드 스크립트**를 만듭니다.

```
프롬프트: "앞에서 만든 모든 모듈(프론트매터 파서, 마크다운 변환기,
템플릿 시스템, 인덱스/태그 페이지 생성기)을 하나로 통합하는
BlogBuilder 클래스를 만들어줘.
build() 메서드 하나로 전체 빌드를 자동 실행하고,
빌드 통계(글 수, 태그 수, 총 페이지 수, 소요 시간)를 출력해줘.
빌드 전에 기존 output 디렉토리를 정리하는 기능도 포함해줘."
```

### 전체 빌드 스크립트

**예제 26-11: 블로그 빌드 스크립트**

```python
# examples/python/chapter06/ex26_11_build_script.py
import os
import re
import html as html_module
import shutil
import time
from string import Template
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class BlogBuilder:
    """블로그 전체 빌드를 관리하는 클래스입니다."""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.content_dir = self.project_dir / "content" / "posts"
        self.output_dir = self.project_dir / "output"
        self.posts_output = self.output_dir / "posts"
        self.tags_output = self.output_dir / "tags"
        self.static_output = self.output_dir / "static"

        self.site_config = {
            "title": "바이브 코딩 블로그",
            "author": "바이브 코더",
            "description": "AI와 함께하는 코딩 이야기",
            "year": str(datetime.now().year),
        }

        self.stats = {
            "posts": 0,
            "tags": 0,
            "pages": 0,
            "total_size": 0,
        }

    def clean(self):
        """기존 출력 디렉토리를 정리합니다."""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def setup(self):
        """출력 디렉토리 구조를 생성합니다."""
        for d in [self.posts_output, self.tags_output, self.static_output]:
            d.mkdir(parents=True, exist_ok=True)

    def build_posts(self) -> list:
        """모든 마크다운 글을 HTML로 빌드합니다."""
        posts = []
        for md_file in sorted(self.content_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)

            title = metadata.get("title", md_file.stem)
            date_str = metadata.get("date", "")
            author = metadata.get("author", self.site_config["author"])
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]

            # 본문 변환 및 페이지 생성
            body_html = markdown_to_html(body)
            page_html = self._page_wrap(title, body_html)

            # 저장
            output_path = self.posts_output / f"{md_file.stem}.html"
            output_path.write_text(page_html, encoding="utf-8")

            posts.append({
                "filename": md_file.stem,
                "title": title,
                "date": date_str,
                "author": author,
                "tags": tags,
                "excerpt": extract_excerpt(body),
                "url": f"/posts/{md_file.stem}.html",
                "size": output_path.stat().st_size,
            })

        posts.sort(key=lambda p: p.get("date", ""), reverse=True)
        self.stats["posts"] = len(posts)
        self.stats["pages"] += len(posts)
        return posts

    def build_index(self, posts: list):
        """인덱스(메인) 페이지를 빌드합니다."""
        # 글 카드 HTML 생성 후 페이지로 조합
        # ... (상세 구현은 예제 파일 참조)
        pass

    def build_tags(self, posts: list):
        """태그 페이지들을 빌드합니다."""
        # 태그별 분류 후 인덱스 + 개별 태그 페이지 생성
        # ... (상세 구현은 예제 파일 참조)
        pass

    def build(self) -> dict:
        """전체 빌드를 실행합니다."""
        start_time = time.time()

        print("  [1/5] 출력 디렉토리 정리...")
        self.clean()

        print("  [2/5] 디렉토리 구조 생성...")
        self.setup()

        print("  [3/5] 글 HTML 빌드...")
        posts = self.build_posts()
        for post in posts:
            print(f"        + {post['filename']}.html ({post['size']:,} bytes)")

        print("  [4/5] 인덱스 및 태그 페이지 빌드...")
        self.build_index(posts)
        self.build_tags(posts)

        print("  [5/5] CSS 파일 생성...")
        self.build_css()

        elapsed = time.time() - start_time
        self.stats["elapsed"] = round(elapsed, 3)

        return self.stats
```

빌드 파이프라인의 전체 흐름을 정리하면:

```
[빌드 파이프라인]

[1/5] clean()       : output/ 디렉토리 삭제
        │
[2/5] setup()       : output/posts/, output/tags/, output/static/ 생성
        │
[3/5] build_posts() : 각 .md 파일 → 프론트매터 파싱 → HTML 변환 → 템플릿 적용 → .html 저장
        │
[4/5] build_index() : 전체 글 목록 → 인덱스 페이지 생성
      build_tags()  : 태그 분류 → 태그 인덱스 + 개별 태그 페이지 생성
        │
[5/5] build_css()   : CSS 스타일시트 생성
```

**실행:**

```bash
$ python examples/python/chapter06/ex26_11_build_script.py
```

**결과:**

```
============================================================
  블로그 빌드 스크립트 데모
============================================================

[준비] 샘플 마크다운 파일 생성
----------------------------------------
  생성: vibe-coding-intro.md
  생성: python-basics.md
  생성: prompt-tips.md
  생성: blog-project.md

[빌드 시작]
----------------------------------------
  [1/5] 출력 디렉토리 정리...
  [2/5] 디렉토리 구조 생성...
  [3/5] 글 HTML 빌드...
        + blog-project.html (2,151 bytes)
        + prompt-tips.html (2,024 bytes)
        + python-basics.html (2,137 bytes)
        + vibe-coding-intro.html (2,307 bytes)
  [4/5] 인덱스 및 태그 페이지 빌드...
  [5/5] CSS 파일 생성...

[빌드 완료 - 결과 요약]
----------------------------------------
  글 수: 4개
  태그 수: 8개
  총 페이지 수: 14개
  총 파일 크기: 26,385 bytes
  소요 시간: 0.012초

[생성된 파일 목록]
----------------------------------------
  output/
    index.html (3,548 bytes)
    posts/
      blog-project.html (2,151 bytes)
      prompt-tips.html (2,024 bytes)
      python-basics.html (2,137 bytes)
      vibe-coding-intro.html (2,307 bytes)
    static/
      style.css (1,592 bytes)
    tags/
      index.html (1,986 bytes)
      ai.html (1,521 bytes)
      바이브코딩.html (1,755 bytes)
      파이썬.html (1,573 bytes)
      ...

블로그 빌드가 성공적으로 완료되었습니다!
```

4개의 마크다운 글로부터 **14개의 HTML 페이지**가 자동 생성되었습니다. 글 페이지 4개, 인덱스 1개, 태그 인덱스 1개, 개별 태그 페이지 8개, 그리고 CSS 파일까지 모두 포함됩니다. 빌드 소요 시간은 0.012초로, 순식간에 전체 블로그가 생성됩니다.

---

## 26.8 프로젝트 전체 구조 되돌아보기

### 모듈 관계도

이 프로젝트에서 만든 모듈들의 관계를 정리하면:

```
[모듈 의존성]

ex26_01 디렉토리 구조 ──┐
ex26_02 설정 파일 관리 ──┤
                         ├── ex26_11 빌드 스크립트 (통합)
ex26_03 마크다운 읽기 ───┤          │
ex26_04 프론트매터 파싱 ─┤     build() 실행
ex26_05 HTML 변환 ───────┤          │
ex26_06 코드 하이라이팅 ─┤     ┌────┴────┐
ex26_07 HTML 템플릿 ─────┤     │         │
ex26_08 템플릿 렌더링 ───┤  글 페이지  인덱스/태그
ex26_09 인덱스 페이지 ───┤
ex26_10 태그 페이지 ─────┘
```

### 핵심 기술 요약

| 모듈 | 핵심 기술 | 표준 라이브러리 |
|------|----------|----------------|
| 디렉토리 구조 | 경로 관리, 트리 출력 | `pathlib`, `os` |
| 설정 파일 | INI 파일 읽기/쓰기 | `configparser` |
| 마크다운 읽기 | 파일 I/O, 구조 분석 | `pathlib`, `re` |
| 프론트매터 파싱 | 정규식, 타입 변환 | `re`, `datetime` |
| HTML 변환 | 줄 단위 파싱, 인라인 변환 | `re`, `html` |
| 코드 하이라이팅 | 플레이스홀더 패턴, 토큰화 | `re`, `html` |
| HTML 템플릿 | 문자열 치환 템플릿 | `string.Template` |
| 템플릿 렌더링 | 파이프라인 통합 | (위 모듈 조합) |
| 인덱스 페이지 | 데이터 수집, 정렬, 요약 추출 | `pathlib`, `datetime` |
| 태그 페이지 | 그룹핑, 슬러그 변환 | `collections.defaultdict` |
| 빌드 스크립트 | 자동화, 통계, 시간 측정 | `shutil`, `time` |

---

## 26.9 확장 아이디어

이 블로그 생성기를 더 발전시킬 수 있는 아이디어입니다. 바이브 코딩으로 AI에게 요청해보세요:

### 기능 확장

```
1. "RSS 피드(XML)를 자동 생성하는 기능을 추가해줘"
2. "검색 기능을 위한 search.json 파일을 만들어줘"
3. "이전 글/다음 글 네비게이션을 추가해줘"
4. "글 수정 날짜를 감지해서 변경된 글만 다시 빌드하는 증분 빌드를 만들어줘"
5. "sitemap.xml을 자동 생성하는 기능을 추가해줘"
```

### 디자인 개선

```
1. "다크 모드를 지원하는 CSS를 만들어줘"
2. "모바일에서도 잘 보이도록 반응형 디자인을 적용해줘"
3. "코드 블록에 복사 버튼을 추가해줘"
4. "읽기 예상 시간을 자동 계산해서 표시해줘"
```

### 운영 기능

```
1. "파일 변경을 감시해서 자동으로 빌드하는 watch 모드를 만들어줘"
2. "http.server를 사용한 로컬 미리보기 서버를 만들어줘"
3. "빌드된 사이트를 GitHub Pages에 배포하는 스크립트를 만들어줘"
```

> **Tip:** 프로젝트를 확장할 때도 바이브 코딩의 핵심 원칙을 기억하세요. "한 번에 하나의 기능"을 요청하고, 동작을 확인한 후 다음 기능으로 넘어갑니다. 작은 성공을 쌓아가는 것이 큰 프로젝트를 완성하는 비결입니다.

---

## 26.10 바이브 코딩 회고

이 프로젝트를 통해 배운 바이브 코딩 패턴을 정리합니다.

### 효과적이었던 프롬프트 패턴

**1. 제약 조건 명시**

```
"파이썬 표준 라이브러리만 사용해줘" (외부 의존성 제한)
"정규식을 사용해줘" (구현 방법 지정)
"한국어 블로그에 맞게" (대상 환경 명시)
```

**2. 이전 결과 참조**

```
"앞에서 만든 parse_frontmatter 함수를 사용해서..." (기존 코드 연결)
"ex26_05에서 가져온 핵심 로직을..." (모듈 간 통합)
```

**3. 구체적인 인터페이스 명시**

```
"render_post(markdown_content)와 render_file(input_path, output_path)
 메서드를 제공해줘" (함수 시그니처 지정)
"(프론트매터 딕셔너리, 본문 문자열) 튜플을 반환해줘" (반환 타입 지정)
```

### 프로젝트에서 배운 것

| 배운 점 | 설명 |
|---------|------|
| 점진적 개발 | 작은 모듈부터 만들어 점차 통합 |
| 파이프라인 설계 | 입력 -> 처리 -> 출력의 명확한 흐름 |
| 표준 라이브러리 활용 | `re`, `pathlib`, `configparser`, `string.Template` 등 |
| 정규식의 힘 | 마크다운 파싱의 핵심 도구 |
| 데이터 구조 설계 | 딕셔너리로 메타데이터 관리 |
| 자동화 사고 | 반복 작업을 코드로 해결 |

---

## 정리

이 장에서 우리는 파이썬 표준 라이브러리만으로 **마크다운 블로그 생성기**를 완성했습니다.

### 프로젝트 요약

- **Step 1** (ex26_01 ~ ex26_02): 프로젝트 디렉토리 구조와 설정 파일 관리
- **Step 2** (ex26_03 ~ ex26_04): 마크다운 파일 읽기와 프론트매터 파싱
- **Step 3** (ex26_05 ~ ex26_06): 마크다운 -> HTML 변환과 코드 하이라이팅
- **Step 4** (ex26_07 ~ ex26_08): HTML 템플릿 시스템과 렌더링 파이프라인
- **Step 5** (ex26_09 ~ ex26_10): 인덱스 페이지와 태그 페이지 생성
- **Step 6** (ex26_11): 전체 빌드 자동화 스크립트

### 핵심 교훈

> **"큰 프로젝트도 작은 단계의 연속이다."**

바이브 코딩에서 가장 중요한 것은 **한 번에 모든 것을 만들려고 하지 않는 것**입니다. 이 프로젝트에서 보았듯이, 디렉토리 구조 만들기 -> 마크다운 읽기 -> HTML 변환 -> 템플릿 적용 -> 인덱스/태그 -> 빌드 자동화로 차근차근 진행하면, AI와 함께 완성도 높은 프로젝트를 만들 수 있습니다.

각 단계에서 AI에게 명확한 요구사항과 제약 조건을 전달하고, 결과를 확인한 후 다음 단계로 나아가는 것이 바이브 코딩의 핵심 워크플로우입니다.

다음 장에서는 세 번째 프로젝트로 **데이터 분석 도구**를 만들어보겠습니다.
