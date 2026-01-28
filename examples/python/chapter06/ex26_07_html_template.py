"""
예제 26-07: 기본 HTML 템플릿

string.Template을 사용하여 블로그용 HTML 페이지 템플릿을 관리합니다.
외부 템플릿 엔진 없이 표준 라이브러리만으로 템플릿 시스템을 구현합니다.
"""

import os
from string import Template
from pathlib import Path


# ============================================================
# 블로그 HTML 템플릿 정의
# ============================================================

# 기본 레이아웃 템플릿 (모든 페이지의 뼈대)
BASE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="${lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${description}">
    <meta name="author" content="${author}">
    <title>${title} - ${site_name}</title>
    <style>
${css}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title"><a href="/">${site_name}</a></h1>
            <nav class="site-nav">
                ${navigation}
            </nav>
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
        <div class="post-tags">
            ${tags_html}
        </div>
    </header>

    <div class="post-content">
        ${content}
    </div>

    <footer class="post-footer">
        <div class="post-nav">
            ${prev_link}
            ${next_link}
        </div>
    </footer>
</article>
""")

# 인덱스 페이지의 글 목록 아이템 템플릿
POST_LIST_ITEM_TEMPLATE = Template("""\
<article class="post-card">
    <h2 class="post-card-title">
        <a href="${url}">${title}</a>
    </h2>
    <div class="post-card-meta">
        <time datetime="${date}">${date_display}</time>
        <span class="post-card-author">| ${author}</span>
    </div>
    <p class="post-card-excerpt">${excerpt}</p>
    <div class="post-card-tags">
        ${tags_html}
    </div>
</article>
""")

# 네비게이션 링크 템플릿
NAV_LINK_TEMPLATE = Template("""\
<a href="${url}" class="nav-link">${text}</a>
""")

# 태그 링크 템플릿
TAG_LINK_TEMPLATE = Template("""\
<a href="/tags/${slug}.html" class="tag">#${name}</a>
""")

# 기본 CSS 스타일
DEFAULT_CSS = """\
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Noto Sans KR', -apple-system, sans-serif;
    line-height: 1.8;
    color: #333;
    background: #fafafa;
}
.container { max-width: 800px; margin: 0 auto; padding: 0 20px; }

/* 헤더 */
.site-header {
    background: #2c3e50;
    color: white;
    padding: 20px 0;
    margin-bottom: 40px;
}
.site-title { font-size: 24px; }
.site-title a { color: white; text-decoration: none; }
.site-nav { margin-top: 10px; }
.nav-link { color: #ecf0f1; text-decoration: none; margin-right: 16px; }
.nav-link:hover { text-decoration: underline; }

/* 글 */
.post { margin-bottom: 40px; }
.post-title { font-size: 32px; margin-bottom: 12px; color: #2c3e50; }
.post-meta { color: #7f8c8d; font-size: 14px; margin-bottom: 8px; }
.post-tags { margin-bottom: 24px; }
.tag {
    display: inline-block;
    background: #ecf0f1;
    color: #2c3e50;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 13px;
    text-decoration: none;
    margin-right: 6px;
}
.tag:hover { background: #3498db; color: white; }
.post-content { font-size: 16px; }
.post-content h2 { margin-top: 32px; margin-bottom: 12px; color: #2c3e50; }
.post-content p { margin-bottom: 16px; }
.post-content pre {
    background: #1e1e1e; color: #d4d4d4;
    padding: 16px; border-radius: 8px;
    overflow-x: auto; margin-bottom: 16px;
}
.post-content code {
    background: #f0f0f0; padding: 2px 6px;
    border-radius: 3px; font-size: 14px;
}
.post-content pre code { background: none; color: inherit; }
.post-content blockquote {
    border-left: 4px solid #3498db;
    padding-left: 16px; margin: 16px 0;
    color: #555; font-style: italic;
}

/* 글 카드 목록 */
.post-card {
    background: white;
    padding: 24px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.post-card-title { font-size: 22px; margin-bottom: 8px; }
.post-card-title a { color: #2c3e50; text-decoration: none; }
.post-card-title a:hover { color: #3498db; }
.post-card-meta { color: #7f8c8d; font-size: 13px; margin-bottom: 8px; }
.post-card-excerpt { color: #555; margin-bottom: 10px; }

/* 푸터 */
.site-footer {
    margin-top: 60px;
    padding: 20px 0;
    text-align: center;
    color: #7f8c8d;
    font-size: 14px;
    border-top: 1px solid #eee;
}

/* 이전/다음 글 네비게이션 */
.post-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
.post-nav a { color: #3498db; text-decoration: none; }
.post-nav a:hover { text-decoration: underline; }
"""


class TemplateManager:
    """블로그 HTML 템플릿을 관리하는 클래스입니다."""

    def __init__(self, site_config: dict):
        """사이트 기본 설정으로 초기화합니다.

        Args:
            site_config: 사이트 설정 딕셔너리
        """
        self.config = site_config

    def render_tag_links(self, tags: list) -> str:
        """태그 목록을 HTML 링크로 변환합니다.

        Args:
            tags: 태그 문자열 리스트

        Returns:
            태그 링크 HTML
        """
        links = []
        for tag in tags:
            tag_name = tag.strip()
            tag_slug = tag_name.replace(" ", "-").lower()
            links.append(TAG_LINK_TEMPLATE.substitute(slug=tag_slug, name=tag_name))
        return " ".join(links)

    def render_navigation(self, nav_items: list) -> str:
        """네비게이션 메뉴를 렌더링합니다.

        Args:
            nav_items: (텍스트, URL) 튜플의 리스트

        Returns:
            네비게이션 HTML
        """
        links = []
        for text, url in nav_items:
            links.append(NAV_LINK_TEMPLATE.substitute(text=text, url=url))
        return " ".join(links)

    def render_base(self, title: str, content: str, description: str = "") -> str:
        """기본 레이아웃으로 페이지를 렌더링합니다.

        Args:
            title: 페이지 제목
            content: 본문 HTML
            description: 페이지 설명

        Returns:
            완성된 HTML 페이지
        """
        nav_items = [
            ("홈", "/"),
            ("태그", "/tags/"),
            ("소개", "/about.html"),
        ]

        return BASE_TEMPLATE.substitute(
            lang=self.config.get("language", "ko"),
            title=title,
            site_name=self.config.get("title", "내 블로그"),
            description=description or self.config.get("description", ""),
            author=self.config.get("author", ""),
            year=self.config.get("year", "2025"),
            navigation=self.render_navigation(nav_items),
            content=content,
            css=DEFAULT_CSS,
            footer_text="바이브 코딩으로 만든 블로그",
        )

    def save_template_files(self, output_dir: str):
        """템플릿 파일들을 디스크에 저장합니다.

        Args:
            output_dir: 저장 디렉토리
        """
        templates_dir = Path(output_dir) / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        # CSS 파일 저장
        css_path = templates_dir / "style.css"
        css_path.write_text(DEFAULT_CSS, encoding="utf-8")

        # 각 템플릿을 텍스트 파일로 저장
        templates = {
            "base.html": BASE_TEMPLATE.template,
            "post.html": POST_TEMPLATE.template,
            "post_list_item.html": POST_LIST_ITEM_TEMPLATE.template,
        }

        for filename, content in templates.items():
            filepath = templates_dir / filename
            filepath.write_text(content, encoding="utf-8")

        return templates_dir


if __name__ == "__main__":
    print("=" * 60)
    print("  HTML 템플릿 시스템 데모")
    print("=" * 60)
    print()

    # 사이트 설정
    site_config = {
        "title": "바이브 코딩 블로그",
        "author": "바이브 코더",
        "description": "AI와 함께하는 코딩 이야기",
        "language": "ko",
        "year": "2025",
    }

    tm = TemplateManager(site_config)

    # 1. 태그 링크 생성
    print("[1] 태그 링크 HTML")
    print("-" * 40)
    tags_html = tm.render_tag_links(["파이썬", "바이브코딩", "AI"])
    print(f"  {tags_html.strip()}")
    print()

    # 2. 글 카드 생성
    print("[2] 글 카드 HTML")
    print("-" * 40)
    card_html = POST_LIST_ITEM_TEMPLATE.substitute(
        url="/posts/hello-world.html",
        title="바이브 코딩 시작하기",
        date="2025-01-15",
        date_display="2025년 1월 15일",
        author="바이브 코더",
        excerpt="바이브 코딩은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다...",
        tags_html=tags_html,
    )
    for line in card_html.strip().split("\n"):
        print(f"  {line}")
    print()

    # 3. 글 페이지 생성
    print("[3] 글 페이지 HTML")
    print("-" * 40)
    post_html = POST_TEMPLATE.substitute(
        title="바이브 코딩 시작하기",
        date="2025-01-15",
        date_display="2025년 1월 15일",
        author="바이브 코더",
        tags_html=tags_html,
        content="<p>바이브 코딩은 AI와 함께 프로그래밍하는 새로운 패러다임입니다.</p>",
        prev_link='<a href="/posts/prev.html">&larr; 이전 글</a>',
        next_link='<a href="/posts/next.html">다음 글 &rarr;</a>',
    )
    # 미리보기 (첫 10줄)
    for line in post_html.strip().split("\n")[:10]:
        print(f"  {line}")
    print("  ...")
    print()

    # 4. 전체 페이지 렌더링
    print("[4] 전체 페이지 렌더링")
    print("-" * 40)
    full_page = tm.render_base(
        title="바이브 코딩 시작하기",
        content=post_html,
        description="바이브 코딩을 처음 시작하는 방법을 알아봅니다.",
    )
    print(f"  전체 HTML 크기: {len(full_page)} bytes")
    print(f"  전체 줄 수: {len(full_page.split(chr(10)))}줄")
    print()

    # 5. 파일로 저장
    print("[5] 템플릿 파일 저장")
    print("-" * 40)
    output_dir = "/tmp/my-vibe-blog"
    templates_dir = tm.save_template_files(output_dir)

    for f in sorted(templates_dir.iterdir()):
        size = f.stat().st_size
        print(f"  저장됨: {f.name} ({size} bytes)")
    print()

    # HTML 파일 저장
    html_path = Path(output_dir) / "output" / "template-demo.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(full_page, encoding="utf-8")
    print(f"  데모 페이지 저장: {html_path}")
    print(f"  파일 크기: {html_path.stat().st_size} bytes")
    print()

    print("HTML 템플릿 시스템 데모가 완료되었습니다!")
