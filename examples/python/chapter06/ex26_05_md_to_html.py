"""
예제 26-05: 마크다운 -> HTML 변환

정규식을 사용하여 마크다운 텍스트를 HTML로 변환하는 간단한 파서입니다.
외부 라이브러리 없이 표준 라이브러리만으로 주요 마크다운 문법을 처리합니다.
"""

import re
import html


class MarkdownToHTML:
    """마크다운 텍스트를 HTML로 변환하는 파서 클래스입니다.

    지원하는 마크다운 문법:
    - 제목 (h1 ~ h6)
    - 볼드, 이탤릭, 인라인 코드
    - 순서 있는/없는 목록
    - 코드 블록
    - 인용문
    - 링크, 이미지
    - 수평선
    - 단락
    """

    def convert(self, markdown_text: str) -> str:
        """마크다운 텍스트를 HTML로 변환합니다.

        Args:
            markdown_text: 마크다운 형식의 텍스트

        Returns:
            HTML 문자열
        """
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

            # 순서 없는 목록 (- 또는 * 또는 + 시작)
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

            # 제목 (# ... ######)
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
            if heading_match:
                level = len(heading_match.group(1))
                text = self._process_inline(heading_match.group(2))
                # id 속성 생성 (한국어 포함 가능)
                slug = re.sub(r"[^\w가-힣-]", "", heading_match.group(2).replace(" ", "-").lower())
                html_parts.append(f'<h{level} id="{slug}">{text}</h{level}>')
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
        """인라인 마크다운 요소를 HTML로 변환합니다.

        Args:
            text: 인라인 마크다운 텍스트

        Returns:
            HTML 변환된 텍스트
        """
        # HTML 특수 문자 이스케이프 (단, 이미 마크다운 문법인 것은 제외)
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
        """코드 블록을 처리합니다.

        Args:
            lines: 전체 줄 리스트
            start: 시작 인덱스

        Returns:
            (HTML 문자열, 소비된 줄 수)
        """
        first_line = lines[start].strip()
        language = first_line[3:].strip()  # ``` 뒤의 언어 이름
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

    def _process_blockquote(self, lines: list, start: int) -> tuple:
        """인용문을 처리합니다.

        Args:
            lines: 전체 줄 리스트
            start: 시작 인덱스

        Returns:
            (HTML 문자열, 소비된 줄 수)
        """
        quote_lines = []
        i = start

        while i < len(lines) and lines[i].strip().startswith(">"):
            text = re.sub(r"^>\s*", "", lines[i].strip())
            quote_lines.append(self._process_inline(text))
            i += 1

        content = "<br>\n".join(quote_lines)
        result = f"<blockquote>\n<p>{content}</p>\n</blockquote>"
        return result, i - start

    def _process_unordered_list(self, lines: list, start: int) -> tuple:
        """순서 없는 목록을 처리합니다.

        Args:
            lines: 전체 줄 리스트
            start: 시작 인덱스

        Returns:
            (HTML 문자열, 소비된 줄 수)
        """
        items = []
        i = start

        while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
            text = re.sub(r"^\s*[-*+]\s+", "", lines[i])
            items.append(f"  <li>{self._process_inline(text.strip())}</li>")
            i += 1

        result = "<ul>\n" + "\n".join(items) + "\n</ul>"
        return result, i - start

    def _process_ordered_list(self, lines: list, start: int) -> tuple:
        """순서 있는 목록을 처리합니다.

        Args:
            lines: 전체 줄 리스트
            start: 시작 인덱스

        Returns:
            (HTML 문자열, 소비된 줄 수)
        """
        items = []
        i = start

        while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
            text = re.sub(r"^\s*\d+\.\s+", "", lines[i])
            items.append(f"  <li>{self._process_inline(text.strip())}</li>")
            i += 1

        result = "<ol>\n" + "\n".join(items) + "\n</ol>"
        return result, i - start

    def _process_paragraph(self, lines: list, start: int) -> tuple:
        """단락을 처리합니다.

        Args:
            lines: 전체 줄 리스트
            start: 시작 인덱스

        Returns:
            (HTML 문자열, 소비된 줄 수)
        """
        para_lines = []
        i = start

        while i < len(lines):
            line = lines[i].strip()
            # 빈 줄이나 다른 블록 요소를 만나면 단락 종료
            if not line or line.startswith("#") or line.startswith("```") or \
               line.startswith(">") or re.match(r"^[-*+]\s+", line) or \
               re.match(r"^\d+\.\s+", line) or re.match(r"^[-*_]{3,}$", line):
                break
            para_lines.append(line)
            i += 1

        text = " ".join(para_lines)
        result = f"<p>{self._process_inline(text)}</p>"
        return result, i - start


# 데모용 마크다운 샘플
SAMPLE_MARKDOWN = """\
# 바이브 코딩 입문 가이드

바이브 코딩은 **AI와 함께** 프로그래밍하는 *새로운 방식*입니다.
자세한 내용은 [공식 문서](https://example.com)를 참고하세요.

## 핵심 개념

바이브 코딩에서 가장 중요한 것은 ***자연어 소통 능력***입니다.

### 준비물

- AI 어시스턴트 (Claude 등)
- 터미널 또는 에디터
- **호기심**과 *인내심*

### 학습 단계

1. 기본 프롬프트 작성법 배우기
2. 간단한 프로그램 만들어보기
3. 점점 복잡한 프로젝트에 도전하기

---

## 첫 번째 예제

다음은 `greet()` 함수를 만드는 예제입니다:

```python
def greet(name):
    return f"안녕하세요, {name}님!"

print(greet("바이브 코더"))
```

> **Tip:** 프롬프트를 명확하게 작성할수록 더 좋은 결과를 얻습니다.
> 구체적인 요구사항을 포함하세요.

![바이브 코딩 로고](images/logo.png)

이것으로 기초 가이드를 마칩니다!
"""


if __name__ == "__main__":
    print("=" * 60)
    print("  마크다운 -> HTML 변환 데모")
    print("=" * 60)
    print()

    converter = MarkdownToHTML()

    # 마크다운 원본 미리보기
    print("[마크다운 원본 (처음 15줄)]")
    print("-" * 50)
    for line in SAMPLE_MARKDOWN.split("\n")[:15]:
        print(f"  {line}")
    print("  ...")
    print()

    # HTML 변환
    html_output = converter.convert(SAMPLE_MARKDOWN)

    print("[변환된 HTML]")
    print("-" * 50)
    for line in html_output.split("\n"):
        print(f"  {line}")
    print()

    # 변환 결과를 파일로 저장
    import os
    output_path = "/tmp/my-vibe-blog/output/md-to-html-demo.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    full_html = f"""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>마크다운 변환 데모</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #2d2d2d; color: #f8f8f2; padding: 16px; border-radius: 8px; overflow-x: auto; }}
        pre code {{ background: none; color: inherit; }}
        blockquote {{ border-left: 4px solid #ddd; margin-left: 0; padding-left: 16px; color: #666; }}
        img {{ max-width: 100%; }}
    </style>
</head>
<body>
{html_output}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"HTML 파일이 저장되었습니다: {output_path}")
    print(f"파일 크기: {os.path.getsize(output_path)} bytes")
    print()

    # 변환 통계
    print("[변환 통계]")
    print("-" * 50)
    tag_counts = {}
    for tag in re.findall(r"<(\w+)[\s>]", html_output):
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

    for tag, count in sorted(tag_counts.items()):
        print(f"  <{tag}>: {count}개")

    print()
    print("마크다운 -> HTML 변환 데모가 완료되었습니다!")
