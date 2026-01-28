"""
예제 26-11: 블로그 빌드 스크립트

마크다운 블로그의 전체 빌드를 자동화하는 스크립트입니다.
마크다운 파일 읽기, HTML 변환, 템플릿 적용, 인덱스/태그 페이지 생성까지
전체 빌드 파이프라인을 하나의 스크립트로 실행합니다.
"""

import os
import re
import html as html_module
import shutil
import time
from string import Template
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ============================================================
# 핵심 함수들 (앞선 예제에서 통합)
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
            if "," in value and not value.startswith('"'):
                metadata[key] = [v.strip() for v in value.split(",")]
            else:
                metadata[key] = value
    return metadata, match.group(2).strip()


def markdown_to_html(text: str) -> str:
    """마크다운을 HTML로 변환합니다 (간략화 버전)."""
    lines = text.split("\n")
    parts = []
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
            parts.append(f"<pre><code{lang_cls}>{code}</code></pre>")
            continue

        # 인용문
        if line.strip().startswith(">"):
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(re.sub(r"^>\s*", "", lines[i].strip()))
                i += 1
            parts.append(f"<blockquote><p>{'<br>'.join(q)}</p></blockquote>")
            continue

        # 순서 없는 목록
        if re.match(r"^\s*[-*+]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
                items.append(f"<li>{_inline(re.sub(r'^\\s*[-*+]\\s+', '', lines[i]))}</li>")
                i += 1
            parts.append("<ul>" + "".join(items) + "</ul>")
            continue

        # 순서 있는 목록
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(f"<li>{_inline(re.sub(r'^\\s*\\d+\\.\\s+', '', lines[i]))}</li>")
                i += 1
            parts.append("<ol>" + "".join(items) + "</ol>")
            continue

        # 수평선
        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\1]*$", line):
            parts.append("<hr>")
            i += 1
            continue

        # 제목
        h = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if h:
            level = len(h.group(1))
            parts.append(f"<h{level}>{_inline(h.group(2))}</h{level}>")
            i += 1
            continue

        # 빈 줄
        if not line.strip():
            i += 1
            continue

        # 단락
        p = []
        while i < len(lines) and lines[i].strip() and \
              not lines[i].strip().startswith(("#", "```", ">")):
            p.append(lines[i].strip())
            i += 1
        parts.append(f"<p>{_inline(' '.join(p))}</p>")

    return "\n".join(parts)


def _inline(text: str) -> str:
    """인라인 마크다운 변환."""
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def extract_excerpt(body: str, max_length: int = 150) -> str:
    """본문에서 요약을 추출합니다."""
    text = re.sub(r"^#{1,6}\s+.+$", "", body, flags=re.MULTILINE)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`\[\]()!#]", "", text)
    text = " ".join(text.split()).strip()
    if len(text) > max_length:
        text = text[:max_length].rsplit(" ", 1)[0] + "..."
    return text


# ============================================================
# 빌드 스크립트 클래스
# ============================================================

class BlogBuilder:
    """블로그 전체 빌드를 관리하는 클래스입니다."""

    # 기본 CSS (간략화)
    CSS = """\
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: sans-serif; line-height: 1.8; color: #333; background: #fafafa; }
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
.header { background: #2c3e50; color: white; padding: 20px 0; margin-bottom: 30px; }
.header h1 { font-size: 24px; }
.header h1 a { color: white; text-decoration: none; }
.header nav { margin-top: 8px; }
.header nav a { color: #ecf0f1; text-decoration: none; margin-right: 14px; }
.post-title { color: #2c3e50; margin-bottom: 8px; }
.post-meta { color: #7f8c8d; font-size: 14px; margin-bottom: 16px; }
.tag { display: inline-block; background: #ecf0f1; padding: 2px 10px; border-radius: 12px; font-size: 12px; text-decoration: none; color: #2c3e50; margin-right: 4px; }
.tag:hover { background: #3498db; color: white; }
.post-card { background: white; padding: 20px; margin-bottom: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.post-card h2 { font-size: 20px; margin-bottom: 6px; }
.post-card h2 a { color: #2c3e50; text-decoration: none; }
.post-card .excerpt { color: #555; font-size: 14px; margin: 8px 0; }
pre { background: #1e1e1e; color: #d4d4d4; padding: 14px; border-radius: 8px; overflow-x: auto; margin: 12px 0; }
code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
pre code { background: none; color: inherit; }
blockquote { border-left: 4px solid #3498db; padding-left: 14px; color: #555; font-style: italic; margin: 12px 0; }
footer { margin-top: 40px; padding: 20px 0; text-align: center; color: #999; font-size: 13px; border-top: 1px solid #eee; }
.tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }
.tag-badge { background: white; border: 1px solid #ddd; padding: 6px 14px; border-radius: 16px; text-decoration: none; color: #333; font-size: 14px; }
.tag-badge:hover { background: #3498db; color: white; }
.tag-count { background: #eee; padding: 1px 6px; border-radius: 8px; font-size: 11px; margin-left: 4px; }
"""

    def __init__(self, project_dir: str):
        """빌드 설정을 초기화합니다.

        Args:
            project_dir: 블로그 프로젝트 루트 디렉토리
        """
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

    def _page_wrap(self, title: str, content: str) -> str:
        """HTML 페이지 래퍼를 적용합니다."""
        cfg = self.site_config
        return f"""\
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - {cfg['title']}</title>
<style>{self.CSS}</style>
</head>
<body>
<header class="header"><div class="container">
<h1><a href="/index.html">{cfg['title']}</a></h1>
<nav><a href="/index.html">홈</a> <a href="/tags/index.html">태그</a></nav>
</div></header>
<main class="container">{content}</main>
<footer><div class="container"><p>&copy; {cfg['year']} {cfg['author']}</p></div></footer>
</body></html>"""

    def build_posts(self) -> list:
        """모든 마크다운 글을 HTML로 빌드합니다.

        Returns:
            글 정보 딕셔너리 리스트
        """
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

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_display = date_obj.strftime("%Y년 %m월 %d일")
            except (ValueError, TypeError):
                date_obj = datetime.min
                date_display = ""

            # 본문 변환
            body_html = markdown_to_html(body)

            # 태그 HTML
            tags_html = " ".join(
                f'<a href="/tags/{t.replace(" ", "-").lower()}.html" class="tag">#{t}</a>'
                for t in tags
            )

            # 글 페이지 HTML
            post_content = f"""\
<article>
<h1 class="post-title">{title}</h1>
<div class="post-meta">{date_display} | {author} {tags_html}</div>
<div class="post-body">{body_html}</div>
</article>"""

            page_html = self._page_wrap(title, post_content)

            # 저장
            output_path = self.posts_output / f"{md_file.stem}.html"
            output_path.write_text(page_html, encoding="utf-8")

            post_info = {
                "filename": md_file.stem,
                "title": title,
                "date": date_str,
                "date_obj": date_obj,
                "date_display": date_display,
                "author": author,
                "tags": tags,
                "excerpt": extract_excerpt(body),
                "url": f"/posts/{md_file.stem}.html",
                "size": output_path.stat().st_size,
            }
            posts.append(post_info)
            self.stats["total_size"] += post_info["size"]

        posts.sort(key=lambda p: p["date_obj"], reverse=True)
        self.stats["posts"] = len(posts)
        self.stats["pages"] += len(posts)
        return posts

    def build_index(self, posts: list):
        """인덱스(메인) 페이지를 빌드합니다."""
        cards = []
        for post in posts:
            tags_html = " ".join(
                f'<a href="/tags/{t.replace(" ", "-").lower()}.html" class="tag">#{t}</a>'
                for t in post["tags"]
            )
            cards.append(f"""\
<div class="post-card">
<h2><a href="{post['url']}">{post['title']}</a></h2>
<div class="post-meta">{post['date_display']} | {post['author']}</div>
<p class="excerpt">{post['excerpt']}</p>
<div>{tags_html}</div>
</div>""")

        content = f"""\
<h2>최근 글</h2>
<p style="color:#7f8c8d;font-size:14px;margin-bottom:20px">총 {len(posts)}개의 글</p>
{''.join(cards)}"""

        page_html = self._page_wrap("홈", content)
        index_path = self.output_dir / "index.html"
        index_path.write_text(page_html, encoding="utf-8")
        self.stats["pages"] += 1
        self.stats["total_size"] += index_path.stat().st_size

    def build_tags(self, posts: list):
        """태그 페이지들을 빌드합니다."""
        tags_map = defaultdict(list)
        for post in posts:
            for tag in post["tags"]:
                tags_map[tag].append(post)

        # 태그 인덱스 페이지
        sorted_tags = sorted(tags_map.items(), key=lambda x: len(x[1]), reverse=True)
        badges = " ".join(
            f'<a href="/tags/{t.replace(" ", "-").lower()}.html" class="tag-badge">'
            f'#{t}<span class="tag-count">{len(p)}</span></a>'
            for t, p in sorted_tags
        )
        index_content = f"""\
<h2>태그 목록</h2>
<p style="color:#7f8c8d;font-size:14px;margin-bottom:16px">총 {len(tags_map)}개의 태그</p>
<div class="tag-cloud">{badges}</div>"""

        idx_html = self._page_wrap("태그", index_content)
        idx_path = self.tags_output / "index.html"
        idx_path.write_text(idx_html, encoding="utf-8")
        self.stats["pages"] += 1
        self.stats["total_size"] += idx_path.stat().st_size

        # 개별 태그 페이지
        for tag_name, tag_posts in tags_map.items():
            slug = tag_name.replace(" ", "-").lower()
            items = "".join(
                f'<div class="post-card"><h2><a href="{p["url"]}">{p["title"]}</a></h2>'
                f'<div class="post-meta">{p["date_display"]} | {p["author"]}</div></div>'
                for p in tag_posts
            )
            tag_content = f"""\
<h2>#{tag_name}</h2>
<p style="color:#7f8c8d;font-size:14px;margin-bottom:16px">{len(tag_posts)}개의 글</p>
{items}
<p style="margin-top:20px"><a href="/tags/index.html">&larr; 모든 태그</a></p>"""

            tag_html = self._page_wrap(f"#{tag_name}", tag_content)
            tag_path = self.tags_output / f"{slug}.html"
            tag_path.write_text(tag_html, encoding="utf-8")
            self.stats["pages"] += 1
            self.stats["total_size"] += tag_path.stat().st_size

        self.stats["tags"] = len(tags_map)

    def build_css(self):
        """CSS 파일을 생성합니다."""
        css_path = self.static_output / "style.css"
        css_path.write_text(self.CSS, encoding="utf-8")
        self.stats["total_size"] += css_path.stat().st_size

    def build(self) -> dict:
        """전체 빌드를 실행합니다.

        Returns:
            빌드 통계 딕셔너리
        """
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

**바이브 코딩**은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다.

## 핵심 아이디어

자연어 프롬프트를 통해 AI에게 의도를 전달하고,
AI가 코드를 생성합니다.

```python
def greet(name):
    return f"안녕하세요, {name}님!"
```

> **Tip:** 프롬프트가 구체적일수록 결과가 좋습니다.
""",
    "python-basics.md": """\
---
title: 바이브 코딩을 위한 파이썬 기초
date: 2025-02-01
tags: 파이썬, 기초, 바이브코딩
author: AI 마스터
---

# 바이브 코딩을 위한 파이썬 기초

파이썬의 기본 문법을 바이브 코딩 관점에서 살펴봅니다.

## 변수와 자료형

파이썬은 동적 타입 언어입니다.

```python
name = "바이브 코더"
level = 42
skills = ["파이썬", "프롬프트", "AI"]
```
""",
    "prompt-tips.md": """\
---
title: 프롬프트 작성 실전 팁
date: 2025-02-15
tags: 프롬프트, 팁, AI, 고급
author: 프롬프트 전문가
---

# 프롬프트 작성 실전 팁

효과적인 프롬프트를 작성하는 방법을 알아봅니다.

## 구체적으로 작성하기

- 원하는 결과를 명확히 설명
- 예시를 포함
- 제약 조건을 명시
""",
    "blog-project.md": """\
---
title: 마크다운 블로그 생성기 프로젝트
date: 2025-03-01
tags: 프로젝트, 파이썬, 블로그, 바이브코딩
author: 바이브 코더
---

# 마크다운 블로그 생성기 프로젝트

파이썬 표준 라이브러리만으로 정적 블로그 생성기를 만듭니다.

## 주요 기능

1. 마크다운을 HTML로 변환
2. 템플릿 시스템
3. 태그 분류
4. 자동 빌드
""",
}


if __name__ == "__main__":
    print("=" * 60)
    print("  블로그 빌드 스크립트 데모")
    print("=" * 60)
    print()

    project_dir = "/tmp/my-vibe-blog"
    posts_dir = os.path.join(project_dir, "content", "posts")

    # 샘플 마크다운 생성
    print("[준비] 샘플 마크다운 파일 생성")
    print("-" * 40)
    os.makedirs(posts_dir, exist_ok=True)
    for filename, content in SAMPLE_POSTS.items():
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  생성: {filename}")
    print()

    # 빌드 실행
    print("[빌드 시작]")
    print("-" * 40)
    builder = BlogBuilder(project_dir)
    stats = builder.build()
    print()

    # 빌드 결과 요약
    print("[빌드 완료 - 결과 요약]")
    print("-" * 40)
    print(f"  글 수: {stats['posts']}개")
    print(f"  태그 수: {stats['tags']}개")
    print(f"  총 페이지 수: {stats['pages']}개")
    print(f"  총 파일 크기: {stats['total_size']:,} bytes")
    print(f"  소요 시간: {stats['elapsed']}초")
    print()

    # 생성된 파일 목록
    print("[생성된 파일 목록]")
    print("-" * 40)
    output_dir = Path(project_dir) / "output"
    for root, dirs, files in os.walk(output_dir):
        level = len(Path(root).relative_to(output_dir).parts)
        indent = "  " * level
        dirname = os.path.basename(root)
        print(f"  {indent}{dirname}/")
        for f in sorted(files):
            filepath = os.path.join(root, f)
            size = os.path.getsize(filepath)
            print(f"  {indent}  {f} ({size:,} bytes)")
    print()

    print("블로그 빌드가 성공적으로 완료되었습니다!")
