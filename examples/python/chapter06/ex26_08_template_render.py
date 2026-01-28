"""
예제 26-08: 템플릿 렌더링

마크다운 파일을 읽어 HTML로 변환하고,
블로그 템플릿에 렌더링하여 완전한 블로그 페이지를 생성합니다.
앞서 만든 모듈들의 기능을 통합하여 전체 렌더링 파이프라인을 구현합니다.
"""

import os
import re
import html as html_module
from string import Template
from pathlib import Path
from datetime import datetime


# ============================================================
# 1. 프론트매터 파싱 (ex26_04에서 가져온 핵심 로직)
# ============================================================

def parse_frontmatter(content: str) -> tuple:
    """마크다운에서 프론트매터와 본문을 분리합니다."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n?(.*)$"
    match = re.match(pattern, content.strip(), re.DOTALL)
    if not match:
        return {}, content.strip()

    metadata = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            # 쉼표 구분 리스트
            if "," in value and not value.startswith('"'):
                metadata[key] = [v.strip() for v in value.split(",")]
            else:
                metadata[key] = value
    return metadata, match.group(2).strip()


# ============================================================
# 2. 마크다운 -> HTML 변환 (ex26_05에서 가져온 핵심 로직)
# ============================================================

def markdown_to_html(text: str) -> str:
    """마크다운 텍스트를 HTML로 변환합니다."""
    lines = text.split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 코드 블록
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(html_module.escape(lines[i]))
                i += 1
            i += 1
            code = "\n".join(code_lines)
            lang_cls = f' class="language-{lang}"' if lang else ""
            html_parts.append(f"<pre><code{lang_cls}>{code}</code></pre>")
            continue

        # 인용문
        if line.strip().startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^>\s*", "", lines[i].strip()))
                i += 1
            html_parts.append(f"<blockquote><p>{'<br>'.join(quote_lines)}</p></blockquote>")
            continue

        # 목록 (순서 없는)
        if re.match(r"^\s*[-*+]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
                text_item = re.sub(r"^\s*[-*+]\s+", "", lines[i])
                items.append(f"<li>{_inline(text_item)}</li>")
                i += 1
            html_parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        # 목록 (순서 있는)
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                text_item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                items.append(f"<li>{_inline(text_item)}</li>")
                i += 1
            html_parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        # 수평선
        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\1]*$", line):
            html_parts.append("<hr>")
            i += 1
            continue

        # 제목
        h_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if h_match:
            level = len(h_match.group(1))
            text_h = _inline(h_match.group(2))
            html_parts.append(f"<h{level}>{text_h}</h{level}>")
            i += 1
            continue

        # 빈 줄
        if not line.strip():
            i += 1
            continue

        # 단락
        para_lines = []
        while i < len(lines) and lines[i].strip() and \
              not lines[i].strip().startswith("#") and \
              not lines[i].strip().startswith("```") and \
              not lines[i].strip().startswith(">"):
            para_lines.append(lines[i].strip())
            i += 1
        html_parts.append(f"<p>{_inline(' '.join(para_lines))}</p>")

    return "\n".join(html_parts)


def _inline(text: str) -> str:
    """인라인 마크다운 요소를 변환합니다."""
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# ============================================================
# 3. 블로그 렌더러 (통합)
# ============================================================

# HTML 템플릿 정의
PAGE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} - ${site_name}</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.8; color: #333; }
        header { border-bottom: 2px solid #2c3e50; padding-bottom: 10px; margin-bottom: 30px; }
        .site-title { color: #2c3e50; }
        .post-meta { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        .tag { background: #ecf0f1; padding: 2px 10px; border-radius: 12px; font-size: 13px; text-decoration: none; color: #2c3e50; }
        pre { background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; overflow-x: auto; }
        code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        pre code { background: none; color: inherit; }
        blockquote { border-left: 4px solid #3498db; padding-left: 16px; color: #555; font-style: italic; margin: 16px 0; }
        footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 13px; text-align: center; }
    </style>
</head>
<body>
    <header>
        <h1 class="site-title">${site_name}</h1>
        <nav>
            <a href="/">홈</a> | <a href="/tags/">태그</a>
        </nav>
    </header>

    <article>
        <h1>${title}</h1>
        <div class="post-meta">
            ${date_display} | ${author} ${tags_html}
        </div>
        <div class="post-content">
${content}
        </div>
    </article>

    <footer>
        <p>&copy; ${year} ${author}. 바이브 코딩으로 만든 블로그</p>
    </footer>
</body>
</html>
""")


class BlogRenderer:
    """마크다운 파일을 완전한 블로그 HTML 페이지로 렌더링합니다."""

    def __init__(self, site_name: str = "바이브 코딩 블로그",
                 author: str = "바이브 코더"):
        self.site_name = site_name
        self.author = author

    def render_post(self, markdown_content: str) -> str:
        """마크다운 콘텐츠를 완전한 HTML 페이지로 렌더링합니다.

        Args:
            markdown_content: 프론트매터를 포함한 마크다운 텍스트

        Returns:
            완전한 HTML 페이지 문자열
        """
        # 프론트매터 파싱
        metadata, body = parse_frontmatter(markdown_content)

        # 마크다운 -> HTML 변환
        body_html = markdown_to_html(body)

        # 메타데이터 추출
        title = metadata.get("title", "제목 없음")
        date = metadata.get("date", "")
        author = metadata.get("author", self.author)
        tags = metadata.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        # 날짜 포맷
        date_display = date
        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                date_display = dt.strftime("%Y년 %m월 %d일")
            except ValueError:
                pass

        # 태그 HTML 생성
        tags_html = ""
        if tags:
            tag_links = [f'<span class="tag">#{t}</span>' for t in tags]
            tags_html = "| " + " ".join(tag_links)

        # 템플릿에 렌더링
        return PAGE_TEMPLATE.substitute(
            title=title,
            site_name=self.site_name,
            date_display=date_display,
            author=author,
            tags_html=tags_html,
            content=body_html,
            year=datetime.now().year,
        )

    def render_file(self, input_path: str, output_path: str) -> dict:
        """마크다운 파일을 읽어 HTML 파일로 렌더링합니다.

        Args:
            input_path: 입력 마크다운 파일 경로
            output_path: 출력 HTML 파일 경로

        Returns:
            렌더링 결과 정보 딕셔너리
        """
        # 마크다운 읽기
        md_content = Path(input_path).read_text(encoding="utf-8")

        # 렌더링
        html_content = self.render_post(md_content)

        # 저장
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html_content, encoding="utf-8")

        # 결과 정보
        metadata, _ = parse_frontmatter(md_content)
        return {
            "input": input_path,
            "output": output_path,
            "title": metadata.get("title", "제목 없음"),
            "size": output.stat().st_size,
        }


# 데모용 마크다운 샘플
SAMPLE_POSTS = {
    "vibe-coding-intro.md": """\
---
title: 바이브 코딩이란 무엇인가
date: 2025-01-15
tags: 바이브코딩, 입문, AI
author: 바이브 코더
---

# 바이브 코딩이란 무엇인가

**바이브 코딩(Vibe Coding)**은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다.

## 핵심 아이디어

기존 프로그래밍은 프로그래머가 코드를 직접 작성했습니다.
바이브 코딩에서는 *자연어 프롬프트*로 AI에게 의도를 전달합니다.

### 예시

```python
# "사용자 이름을 받아 인사하는 함수를 만들어줘"
def greet(name):
    return f"안녕하세요, {name}님! 바이브 코딩에 오신 것을 환영합니다."
```

> **Tip:** 프롬프트가 구체적일수록 더 좋은 결과를 얻을 수 있습니다.

## 장점

1. 빠른 프로토타이핑
2. 낮은 진입 장벽
3. 창의적 문제 해결

바이브 코딩으로 여러분의 아이디어를 실현해보세요!
""",
    "python-tips.md": """\
---
title: 바이브 코딩을 위한 파이썬 팁
date: 2025-02-01
tags: 파이썬, 팁, 초급
author: AI 마스터
---

# 바이브 코딩을 위한 파이썬 팁

바이브 코딩에서 자주 사용하는 파이썬 패턴을 소개합니다.

## 리스트 컴프리헨션

리스트를 간결하게 생성하는 방법입니다:

```python
# 1부터 10까지 짝수만 골라 제곱
squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(squares)  # [4, 16, 36, 64, 100]
```

## f-string 포맷팅

파이썬 3.6+에서 사용할 수 있는 편리한 문자열 포맷팅:

```python
name = "바이브 코더"
level = 42
print(f"{name}님의 레벨은 {level}입니다.")
```

> 이 팁들을 활용하면 AI에게 더 정확한 코드를 요청할 수 있습니다.
""",
}


if __name__ == "__main__":
    print("=" * 60)
    print("  블로그 템플릿 렌더링 데모")
    print("=" * 60)
    print()

    base_dir = "/tmp/my-vibe-blog"
    posts_dir = os.path.join(base_dir, "content", "posts")
    output_dir = os.path.join(base_dir, "output", "posts")

    # 샘플 마크다운 파일 생성
    print("[1단계] 샘플 마크다운 파일 생성")
    print("-" * 40)
    os.makedirs(posts_dir, exist_ok=True)
    for filename, content in SAMPLE_POSTS.items():
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  생성: {filename}")
    print()

    # 렌더러 생성
    renderer = BlogRenderer(
        site_name="바이브 코딩 블로그",
        author="바이브 코더",
    )

    # 모든 마크다운 파일을 HTML로 렌더링
    print("[2단계] HTML 렌더링")
    print("-" * 40)
    results = []

    for md_file in sorted(Path(posts_dir).glob("*.md")):
        html_filename = md_file.stem + ".html"
        output_path = os.path.join(output_dir, html_filename)

        result = renderer.render_file(str(md_file), output_path)
        results.append(result)

        print(f"  변환: {md_file.name} -> {html_filename}")
        print(f"         제목: {result['title']}")
        print(f"         크기: {result['size']} bytes")
        print()

    # 결과 요약
    print("[결과 요약]")
    print("-" * 40)
    print(f"  변환된 글: {len(results)}개")
    total_size = sum(r['size'] for r in results)
    print(f"  총 HTML 크기: {total_size:,} bytes")
    print()

    # 첫 번째 HTML 내용 미리보기
    if results:
        print("[첫 번째 글 HTML 미리보기 (본문 부분)]")
        print("-" * 40)
        with open(results[0]["output"], "r", encoding="utf-8") as f:
            html_content = f.read()

        # <article> 부분만 추출하여 미리보기
        article_match = re.search(r"<article>(.*?)</article>", html_content, re.DOTALL)
        if article_match:
            article = article_match.group(1).strip()
            lines = article.split("\n")
            for line in lines[:20]:
                print(f"  {line.strip()}")
            if len(lines) > 20:
                print(f"  ... (총 {len(lines)}줄)")
        print()

    print("블로그 렌더링 데모가 완료되었습니다!")
