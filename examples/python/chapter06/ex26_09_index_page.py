"""
예제 26-09: 글 목록(인덱스) 페이지 생성

블로그의 메인 페이지를 생성합니다.
모든 글의 제목, 날짜, 요약을 보여주는 목록 페이지를
날짜 역순으로 정렬하여 HTML로 만듭니다.
"""

import os
import re
from string import Template
from pathlib import Path
from datetime import datetime


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


def extract_excerpt(body: str, max_length: int = 150) -> str:
    """본문에서 요약(발췌)을 추출합니다.

    마크다운 문법을 제거하고 첫 번째 단락에서 지정된 길이만큼 추출합니다.

    Args:
        body: 마크다운 본문
        max_length: 최대 글자 수

    Returns:
        요약 텍스트
    """
    # 제목 제거
    text = re.sub(r"^#{1,6}\s+.+$", "", body, flags=re.MULTILINE)
    # 코드 블록 제거
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # 인용문 기호 제거
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # 마크다운 문법 제거
    text = re.sub(r"[*_`\[\]()!#]", "", text)
    # 공백 정리
    text = " ".join(text.split()).strip()

    if len(text) > max_length:
        # 단어 경계에서 자르기
        text = text[:max_length]
        last_space = text.rfind(" ")
        if last_space > max_length // 2:
            text = text[:last_space]
        text += "..."

    return text


def collect_posts(posts_dir: str) -> list:
    """디렉토리에서 모든 마크다운 글의 메타데이터를 수집합니다.

    Args:
        posts_dir: 마크다운 글이 있는 디렉토리 경로

    Returns:
        글 정보 딕셔너리의 리스트 (날짜 역순)
    """
    posts = []
    posts_path = Path(posts_dir)

    if not posts_path.exists():
        return posts

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
            "date_display": date_obj.strftime("%Y년 %m월 %d일") if date_obj != datetime.min else "",
            "author": metadata.get("author", ""),
            "tags": tags,
            "excerpt": extract_excerpt(body),
            "url": f"/posts/{md_file.stem}.html",
        }
        posts.append(post_info)

    # 날짜 역순 정렬 (최신 글이 위로)
    posts.sort(key=lambda p: p["date_obj"], reverse=True)
    return posts


# 인덱스 페이지 템플릿
INDEX_PAGE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${site_name}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: sans-serif; line-height: 1.8; color: #333; background: #fafafa; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }

        .site-header {
            background: #2c3e50; color: white;
            padding: 30px 0; margin-bottom: 40px;
        }
        .site-title { font-size: 28px; margin-bottom: 8px; }
        .site-description { color: #bdc3c7; font-size: 16px; }
        .site-nav { margin-top: 12px; }
        .site-nav a { color: #ecf0f1; text-decoration: none; margin-right: 16px; }

        .post-count { color: #7f8c8d; margin-bottom: 24px; font-size: 14px; }

        .post-card {
            background: white; padding: 24px; margin-bottom: 20px;
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            transition: transform 0.2s;
        }
        .post-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.12); }
        .post-card-title { font-size: 22px; margin-bottom: 8px; }
        .post-card-title a { color: #2c3e50; text-decoration: none; }
        .post-card-title a:hover { color: #3498db; }
        .post-card-meta { color: #7f8c8d; font-size: 13px; margin-bottom: 10px; }
        .post-card-excerpt { color: #555; font-size: 15px; margin-bottom: 12px; }
        .tag {
            display: inline-block; background: #ecf0f1; color: #2c3e50;
            padding: 2px 10px; border-radius: 12px; font-size: 12px;
            text-decoration: none; margin-right: 4px;
        }

        .site-footer {
            margin-top: 40px; padding: 20px 0;
            text-align: center; color: #999; font-size: 13px;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title">${site_name}</h1>
            <p class="site-description">${site_description}</p>
            <nav class="site-nav">
                <a href="/">홈</a>
                <a href="/tags/">태그</a>
                <a href="/about.html">소개</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <p class="post-count">총 ${post_count}개의 글</p>
        ${post_list_html}
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; ${year} ${author}. 바이브 코딩으로 만든 블로그</p>
        </div>
    </footer>
</body>
</html>
""")

# 글 카드 템플릿
POST_CARD_TEMPLATE = Template("""\
        <article class="post-card">
            <h2 class="post-card-title">
                <a href="${url}">${title}</a>
            </h2>
            <div class="post-card-meta">
                ${date_display} ${author_display}
            </div>
            <p class="post-card-excerpt">${excerpt}</p>
            <div class="post-card-tags">
                ${tags_html}
            </div>
        </article>
""")


def generate_index_page(posts: list, site_config: dict) -> str:
    """글 목록 인덱스 페이지 HTML을 생성합니다.

    Args:
        posts: 글 정보 딕셔너리의 리스트
        site_config: 사이트 설정 딕셔너리

    Returns:
        완전한 HTML 페이지 문자열
    """
    # 각 글의 카드 HTML 생성
    cards_html = []
    for post in posts:
        tags_html = " ".join(
            f'<a href="/tags/{t.replace(" ", "-").lower()}.html" class="tag">#{t}</a>'
            for t in post["tags"]
        )
        author_display = f'| {post["author"]}' if post["author"] else ""

        card = POST_CARD_TEMPLATE.substitute(
            url=post["url"],
            title=post["title"],
            date_display=post["date_display"],
            author_display=author_display,
            excerpt=post["excerpt"],
            tags_html=tags_html,
        )
        cards_html.append(card)

    post_list_html = "\n".join(cards_html)

    # 전체 페이지 렌더링
    return INDEX_PAGE_TEMPLATE.substitute(
        site_name=site_config.get("title", "내 블로그"),
        site_description=site_config.get("description", ""),
        author=site_config.get("author", ""),
        post_count=len(posts),
        post_list_html=post_list_html,
        year=datetime.now().year,
    )


# 데모용 샘플 글
SAMPLE_POSTS_DATA = {
    "vibe-coding-intro.md": """\
---
title: 바이브 코딩이란 무엇인가
date: 2025-01-15
tags: 바이브코딩, 입문, AI
author: 바이브 코더
---

# 바이브 코딩이란 무엇인가

바이브 코딩은 AI와 자연어로 소통하며 프로그래밍하는 새로운 방식입니다.
기존의 코딩 방식과 달리, 자연어 프롬프트를 통해 AI에게 의도를 전달합니다.
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
리스트 컴프리헨션, f-string, 딕셔너리 등의 기능을 활용하면
AI에게 더 정확한 코드를 요청할 수 있습니다.
""",
    "prompt-engineering.md": """\
---
title: 효과적인 프롬프트 작성법
date: 2025-02-15
tags: 프롬프트, 고급, 바이브코딩
author: 프롬프트 전문가
---

# 효과적인 프롬프트 작성법

좋은 프롬프트를 작성하면 AI로부터 더 나은 결과를 얻을 수 있습니다.
구체적인 요구사항, 예시, 제약 조건을 포함하면 효과적입니다.
이 글에서는 실전에서 바로 활용할 수 있는 프롬프트 작성 기법을 소개합니다.
""",
    "blog-generator.md": """\
---
title: 마크다운 블로그 생성기 만들기
date: 2025-03-01
tags: 프로젝트, 파이썬, 블로그
author: 바이브 코더
---

# 마크다운 블로그 생성기 만들기

파이썬 표준 라이브러리만으로 정적 블로그 생성기를 만들어봅시다.
마크다운 파일을 HTML로 변환하고, 템플릿을 적용하여
완전한 블로그 사이트를 생성하는 프로젝트입니다.
""",
}


if __name__ == "__main__":
    print("=" * 60)
    print("  글 목록(인덱스) 페이지 생성 데모")
    print("=" * 60)
    print()

    base_dir = "/tmp/my-vibe-blog"
    posts_dir = os.path.join(base_dir, "content", "posts")
    output_dir = os.path.join(base_dir, "output")

    # 샘플 마크다운 파일 생성
    print("[1단계] 샘플 마크다운 파일 생성")
    print("-" * 40)
    os.makedirs(posts_dir, exist_ok=True)

    for filename, content in SAMPLE_POSTS_DATA.items():
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  생성: {filename}")
    print()

    # 글 목록 수집
    print("[2단계] 글 목록 수집 (날짜 역순)")
    print("-" * 40)
    posts = collect_posts(posts_dir)

    for i, post in enumerate(posts, 1):
        print(f"  {i}. [{post['date']}] {post['title']}")
        print(f"     태그: {', '.join(post['tags'])}")
        print(f"     요약: {post['excerpt'][:50]}...")
        print()

    # 인덱스 페이지 생성
    print("[3단계] 인덱스 페이지 생성")
    print("-" * 40)

    site_config = {
        "title": "바이브 코딩 블로그",
        "description": "AI와 함께하는 코딩 이야기",
        "author": "바이브 코더",
    }

    index_html = generate_index_page(posts, site_config)

    # 저장
    index_path = os.path.join(output_dir, "index.html")
    os.makedirs(output_dir, exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    print(f"  인덱스 페이지 저장: {index_path}")
    print(f"  파일 크기: {os.path.getsize(index_path):,} bytes")
    print(f"  포함된 글 수: {len(posts)}개")
    print()

    # HTML 구조 확인
    print("[4단계] 생성된 HTML 구조 확인")
    print("-" * 40)
    # post-card 수 확인
    card_count = index_html.count("post-card-title")
    tag_count = index_html.count("class=\"tag\"")
    print(f"  글 카드: {card_count}개")
    print(f"  태그 링크: {tag_count}개")
    print(f"  HTML 총 줄 수: {len(index_html.splitlines())}줄")
    print()

    print("인덱스 페이지 생성 데모가 완료되었습니다!")
