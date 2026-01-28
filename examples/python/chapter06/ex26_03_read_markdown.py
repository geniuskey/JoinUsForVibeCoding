"""
예제 26-03: 마크다운 파일 읽기

마크다운 파일을 읽고 구조를 분석합니다.
파일의 메타데이터(프론트매터)와 본문을 분리하고,
제목, 단락, 코드 블록 등의 요소를 식별합니다.
"""

import os
import re
from pathlib import Path
from typing import Optional


# 데모용 샘플 마크다운 콘텐츠
SAMPLE_MARKDOWN = """\
---
title: 파이썬으로 배우는 바이브 코딩
date: 2025-03-10
tags: 파이썬, 바이브코딩, 입문
author: 바이브 코더
---

# 파이썬으로 배우는 바이브 코딩

바이브 코딩은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다.

## 바이브 코딩이란?

바이브 코딩은 Andrej Karpathy가 소개한 개념으로,
**자연어 프롬프트**를 통해 AI에게 코드를 작성하도록 요청하는 방식입니다.

### 핵심 원칙

1. 자연어로 의도를 설명한다
2. AI가 코드를 생성한다
3. 결과를 검토하고 피드백한다

## 첫 번째 예제

다음은 간단한 인사 프로그램입니다:

```python
def greet(name):
    return f"안녕하세요, {name}님!"

print(greet("바이브 코더"))
```

> **Tip:** 프롬프트를 명확하게 작성할수록 더 좋은 코드가 생성됩니다.

## 마무리

이 글에서 바이브 코딩의 기초를 알아보았습니다.
다음 글에서는 실전 예제를 살펴보겠습니다.
"""


class MarkdownReader:
    """마크다운 파일을 읽고 구조를 분석하는 클래스입니다."""

    def __init__(self, content: str):
        """마크다운 콘텐츠로 초기화합니다.

        Args:
            content: 마크다운 텍스트
        """
        self.raw_content = content
        self.frontmatter = {}
        self.body = ""
        self._parse()

    def _parse(self):
        """프론트매터와 본문을 분리합니다."""
        # --- 로 둘러싸인 프론트매터 감지
        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.match(pattern, self.raw_content, re.DOTALL)

        if match:
            # 프론트매터 파싱 (간단한 key: value 형식)
            fm_text = match.group(1)
            for line in fm_text.strip().split("\n"):
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    self.frontmatter[key.strip()] = value.strip()
            self.body = match.group(2).strip()
        else:
            self.body = self.raw_content.strip()

    @classmethod
    def from_file(cls, file_path: str) -> "MarkdownReader":
        """파일에서 마크다운을 읽어옵니다.

        Args:
            file_path: 마크다운 파일 경로

        Returns:
            MarkdownReader 인스턴스
        """
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        return cls(content)

    def get_title(self) -> str:
        """글의 제목을 반환합니다. 프론트매터 또는 첫 번째 h1에서 추출합니다."""
        # 프론트매터에서 먼저 확인
        if "title" in self.frontmatter:
            return self.frontmatter["title"]

        # 본문의 첫 번째 # 제목에서 추출
        match = re.search(r"^#\s+(.+)$", self.body, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return "제목 없음"

    def get_headings(self) -> list:
        """본문의 모든 제목(heading)을 추출합니다.

        Returns:
            (레벨, 제목 텍스트) 튜플의 리스트
        """
        headings = []
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", self.body, re.MULTILINE):
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text))
        return headings

    def get_paragraphs(self) -> list:
        """본문의 단락을 추출합니다.

        Returns:
            단락 텍스트의 리스트
        """
        # 코드 블록 제거 후 단락 추출
        body_no_code = re.sub(r"```.*?```", "", self.body, flags=re.DOTALL)
        # 제목 줄 제거
        body_no_headings = re.sub(r"^#{1,6}\s+.+$", "", body_no_code, flags=re.MULTILINE)
        # 인용문 제거
        body_no_quotes = re.sub(r"^>.*$", "", body_no_headings, flags=re.MULTILINE)

        paragraphs = []
        current = []
        for line in body_no_quotes.split("\n"):
            stripped = line.strip()
            if stripped:
                current.append(stripped)
            elif current:
                paragraphs.append(" ".join(current))
                current = []

        if current:
            paragraphs.append(" ".join(current))

        return paragraphs

    def get_code_blocks(self) -> list:
        """본문의 코드 블록을 추출합니다.

        Returns:
            (언어, 코드) 튜플의 리스트
        """
        blocks = []
        pattern = r"```(\w*)\n(.*?)```"
        for match in re.finditer(pattern, self.body, re.DOTALL):
            language = match.group(1) or "text"
            code = match.group(2).strip()
            blocks.append((language, code))
        return blocks

    def get_word_count(self) -> int:
        """본문의 글자 수를 반환합니다 (한국어 기준)."""
        # 코드 블록 제거
        text = re.sub(r"```.*?```", "", self.body, flags=re.DOTALL)
        # 마크다운 기호 제거
        text = re.sub(r"[#*>\-\[\]()!`]", "", text)
        # 공백 제거 후 글자 수 카운트
        text = text.replace(" ", "").replace("\n", "")
        return len(text)

    def summary(self) -> dict:
        """마크다운 문서의 요약 정보를 반환합니다."""
        return {
            "제목": self.get_title(),
            "프론트매터 항목": len(self.frontmatter),
            "제목(heading) 수": len(self.get_headings()),
            "단락 수": len(self.get_paragraphs()),
            "코드 블록 수": len(self.get_code_blocks()),
            "글자 수": self.get_word_count(),
        }


if __name__ == "__main__":
    print("=" * 50)
    print("  마크다운 파일 읽기 데모")
    print("=" * 50)
    print()

    # 샘플 마크다운 파일 생성
    sample_path = "/tmp/my-vibe-blog/content/posts/vibe-coding-intro.md"
    os.makedirs(os.path.dirname(sample_path), exist_ok=True)
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_MARKDOWN)
    print(f"샘플 파일 생성: {sample_path}")
    print()

    # 파일에서 읽기
    reader = MarkdownReader.from_file(sample_path)

    # 1. 프론트매터 정보
    print("[프론트매터]")
    print("-" * 40)
    for key, value in reader.frontmatter.items():
        print(f"  {key}: {value}")
    print()

    # 2. 제목 구조
    print("[제목 구조 (목차)]")
    print("-" * 40)
    for level, text in reader.get_headings():
        indent = "  " * (level - 1)
        marker = "#" * level
        print(f"  {indent}{marker} {text}")
    print()

    # 3. 코드 블록
    print("[코드 블록]")
    print("-" * 40)
    for i, (lang, code) in enumerate(reader.get_code_blocks(), 1):
        print(f"  블록 {i} (언어: {lang}):")
        for line in code.split("\n"):
            print(f"    {line}")
        print()

    # 4. 단락
    print("[단락]")
    print("-" * 40)
    for i, para in enumerate(reader.get_paragraphs(), 1):
        preview = para[:60] + "..." if len(para) > 60 else para
        print(f"  {i}. {preview}")
    print()

    # 5. 요약 정보
    print("[문서 요약]")
    print("-" * 40)
    for key, value in reader.summary().items():
        print(f"  {key}: {value}")
    print()

    print("마크다운 파일 분석이 완료되었습니다!")
