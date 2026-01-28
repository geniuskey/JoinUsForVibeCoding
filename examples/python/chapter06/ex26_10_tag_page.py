"""
예제 26-10: 태그 페이지 생성

블로그 글을 태그별로 분류하고, 각 태그에 대한 개별 페이지와
전체 태그 목록 페이지를 생성합니다.
"""

import os
import re
from string import Template
from pathlib import Path
from datetime import datetime
from collections import defaultdict


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


def collect_posts_by_tag(posts_dir: str) -> tuple:
    """글을 태그별로 분류합니다.

    Args:
        posts_dir: 마크다운 글 디렉토리 경로

    Returns:
        (태그별 글 딕셔너리, 전체 글 리스트) 튜플
    """
    tags_map = defaultdict(list)  # {태그이름: [글 정보 리스트]}
    all_posts = []
    posts_path = Path(posts_dir)

    if not posts_path.exists():
        return dict(tags_map), all_posts

    for md_file in sorted(posts_path.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)

        # 날짜 파싱
        date_str = metadata.get("date", "")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            date_obj = datetime.min

        # 태그 파싱
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
            "url": f"/posts/{md_file.stem}.html",
        }

        all_posts.append(post_info)

        # 각 태그에 글 추가
        for tag in tags:
            tags_map[tag].append(post_info)

    # 각 태그의 글을 날짜 역순 정렬
    for tag in tags_map:
        tags_map[tag].sort(key=lambda p: p["date_obj"], reverse=True)

    return dict(tags_map), all_posts


def tag_slug(tag_name: str) -> str:
    """태그 이름을 URL 슬러그로 변환합니다.

    Args:
        tag_name: 태그 이름 (한국어 가능)

    Returns:
        슬러그 문자열
    """
    return tag_name.strip().replace(" ", "-").lower()


# 태그 인덱스 페이지 템플릿 (모든 태그 목록)
TAG_INDEX_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>태그 목록 - ${site_name}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: sans-serif; line-height: 1.8; color: #333; background: #fafafa; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
        .header { background: #2c3e50; color: white; padding: 30px 0; margin-bottom: 40px; }
        .header h1 { font-size: 28px; }
        .header nav { margin-top: 10px; }
        .header nav a { color: #ecf0f1; text-decoration: none; margin-right: 16px; }
        h2 { margin-bottom: 20px; color: #2c3e50; }
        .tag-cloud { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 40px; }
        .tag-badge {
            display: inline-flex; align-items: center; gap: 6px;
            background: white; border: 1px solid #ddd; padding: 8px 16px;
            border-radius: 20px; text-decoration: none; color: #2c3e50;
            font-size: 14px; transition: all 0.2s;
        }
        .tag-badge:hover { background: #3498db; color: white; border-color: #3498db; }
        .tag-count {
            background: #ecf0f1; color: #7f8c8d; padding: 2px 8px;
            border-radius: 10px; font-size: 12px;
        }
        .tag-badge:hover .tag-count { background: rgba(255,255,255,0.3); color: white; }
        .stats { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        footer { margin-top: 40px; padding: 20px 0; text-align: center; color: #999; font-size: 13px; border-top: 1px solid #eee; }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>${site_name}</h1>
            <nav>
                <a href="/">홈</a>
                <a href="/tags/">태그</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <h2>태그 목록</h2>
        <p class="stats">총 ${tag_count}개의 태그, ${post_count}개의 글</p>
        <div class="tag-cloud">
            ${tag_badges}
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; ${year} ${author}. 바이브 코딩으로 만든 블로그</p>
        </div>
    </footer>
</body>
</html>
""")

# 개별 태그 페이지 템플릿
TAG_PAGE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#${tag_name} - ${site_name}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: sans-serif; line-height: 1.8; color: #333; background: #fafafa; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
        .header { background: #2c3e50; color: white; padding: 30px 0; margin-bottom: 40px; }
        .header h1 { font-size: 28px; }
        .header nav { margin-top: 10px; }
        .header nav a { color: #ecf0f1; text-decoration: none; margin-right: 16px; }
        .tag-title { color: #2c3e50; margin-bottom: 8px; }
        .tag-title .hash { color: #3498db; }
        .post-count { color: #7f8c8d; font-size: 14px; margin-bottom: 24px; }
        .post-item {
            background: white; padding: 20px; margin-bottom: 12px;
            border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .post-item h3 { font-size: 18px; margin-bottom: 4px; }
        .post-item h3 a { color: #2c3e50; text-decoration: none; }
        .post-item h3 a:hover { color: #3498db; }
        .post-item .meta { color: #7f8c8d; font-size: 13px; }
        .back-link { display: inline-block; margin-top: 24px; color: #3498db; text-decoration: none; }
        footer { margin-top: 40px; padding: 20px 0; text-align: center; color: #999; font-size: 13px; border-top: 1px solid #eee; }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>${site_name}</h1>
            <nav>
                <a href="/">홈</a>
                <a href="/tags/">태그</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <h2 class="tag-title"><span class="hash">#</span>${tag_name}</h2>
        <p class="post-count">${post_count}개의 글</p>
        ${post_list_html}
        <a href="/tags/" class="back-link">&larr; 모든 태그 보기</a>
    </main>

    <footer>
        <div class="container">
            <p>&copy; ${year} ${author}. 바이브 코딩으로 만든 블로그</p>
        </div>
    </footer>
</body>
</html>
""")


def generate_tag_index(tags_map: dict, site_config: dict) -> str:
    """태그 인덱스 페이지(전체 태그 목록)를 생성합니다.

    Args:
        tags_map: 태그별 글 딕셔너리
        site_config: 사이트 설정

    Returns:
        HTML 문자열
    """
    # 태그를 글 수 내림차순 정렬
    sorted_tags = sorted(tags_map.items(), key=lambda x: len(x[1]), reverse=True)

    # 태그 배지 HTML
    badges = []
    for tag_name, posts in sorted_tags:
        slug = tag_slug(tag_name)
        badges.append(
            f'<a href="/tags/{slug}.html" class="tag-badge">'
            f'#{tag_name} <span class="tag-count">{len(posts)}</span></a>'
        )

    total_posts = sum(len(posts) for posts in tags_map.values())

    return TAG_INDEX_TEMPLATE.substitute(
        site_name=site_config.get("title", "내 블로그"),
        author=site_config.get("author", ""),
        tag_count=len(tags_map),
        post_count=total_posts,
        tag_badges="\n            ".join(badges),
        year=datetime.now().year,
    )


def generate_tag_page(tag_name: str, posts: list, site_config: dict) -> str:
    """개별 태그 페이지를 생성합니다.

    Args:
        tag_name: 태그 이름
        posts: 해당 태그의 글 리스트
        site_config: 사이트 설정

    Returns:
        HTML 문자열
    """
    # 글 목록 HTML
    items = []
    for post in posts:
        items.append(
            f'<div class="post-item">\n'
            f'    <h3><a href="{post["url"]}">{post["title"]}</a></h3>\n'
            f'    <div class="meta">{post["date_display"]} | {post["author"]}</div>\n'
            f'</div>'
        )

    return TAG_PAGE_TEMPLATE.substitute(
        site_name=site_config.get("title", "내 블로그"),
        author=site_config.get("author", ""),
        tag_name=tag_name,
        post_count=len(posts),
        post_list_html="\n        ".join(items),
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

바이브 코딩의 기초를 소개합니다.
""",
    "python-tips.md": """\
---
title: 바이브 코딩을 위한 파이썬 팁
date: 2025-02-01
tags: 파이썬, 팁, 바이브코딩
author: AI 마스터
---

파이썬 활용 팁을 소개합니다.
""",
    "prompt-engineering.md": """\
---
title: 효과적인 프롬프트 작성법
date: 2025-02-15
tags: 프롬프트, 고급, AI
author: 프롬프트 전문가
---

프롬프트를 잘 작성하는 방법입니다.
""",
    "blog-generator.md": """\
---
title: 마크다운 블로그 생성기 만들기
date: 2025-03-01
tags: 프로젝트, 파이썬, 바이브코딩
author: 바이브 코더
---

블로그 생성기 프로젝트를 진행합니다.
""",
    "ai-future.md": """\
---
title: AI 코딩의 미래
date: 2025-03-10
tags: AI, 미래, 바이브코딩, 고급
author: AI 연구원
---

AI 코딩의 미래를 전망합니다.
""",
}


if __name__ == "__main__":
    print("=" * 60)
    print("  태그 페이지 생성 데모")
    print("=" * 60)
    print()

    base_dir = "/tmp/my-vibe-blog"
    posts_dir = os.path.join(base_dir, "content", "posts")
    tags_output_dir = os.path.join(base_dir, "output", "tags")

    # 샘플 마크다운 생성
    print("[1단계] 샘플 마크다운 파일 생성")
    print("-" * 40)
    os.makedirs(posts_dir, exist_ok=True)
    for filename, content in SAMPLE_POSTS_DATA.items():
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  생성: {filename}")
    print()

    # 태그별 글 수집
    print("[2단계] 태그별 글 분류")
    print("-" * 40)
    tags_map, all_posts = collect_posts_by_tag(posts_dir)

    for tag_name, posts in sorted(tags_map.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  #{tag_name} ({len(posts)}개)")
        for post in posts:
            print(f"    - {post['title']} ({post['date']})")
    print()

    # 사이트 설정
    site_config = {
        "title": "바이브 코딩 블로그",
        "author": "바이브 코더",
    }

    # 태그 인덱스 페이지 생성
    print("[3단계] 태그 인덱스 페이지 생성")
    print("-" * 40)
    os.makedirs(tags_output_dir, exist_ok=True)

    index_html = generate_tag_index(tags_map, site_config)
    index_path = os.path.join(tags_output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  저장: {index_path} ({os.path.getsize(index_path):,} bytes)")
    print()

    # 개별 태그 페이지 생성
    print("[4단계] 개별 태그 페이지 생성")
    print("-" * 40)
    for tag_name, posts in tags_map.items():
        slug = tag_slug(tag_name)
        tag_html = generate_tag_page(tag_name, posts, site_config)
        tag_path = os.path.join(tags_output_dir, f"{slug}.html")
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(tag_html)
        print(f"  #{tag_name} -> {slug}.html ({os.path.getsize(tag_path):,} bytes, {len(posts)}개 글)")
    print()

    # 결과 요약
    print("[결과 요약]")
    print("-" * 40)
    print(f"  총 태그 수: {len(tags_map)}개")
    print(f"  총 글 수: {len(all_posts)}개")
    total_size = sum(
        os.path.getsize(os.path.join(tags_output_dir, f))
        for f in os.listdir(tags_output_dir) if f.endswith(".html")
    )
    file_count = len([f for f in os.listdir(tags_output_dir) if f.endswith(".html")])
    print(f"  생성된 HTML 파일: {file_count}개")
    print(f"  총 파일 크기: {total_size:,} bytes")
    print()

    # 생성된 파일 목록
    print("[생성된 파일]")
    print("-" * 40)
    for f in sorted(os.listdir(tags_output_dir)):
        if f.endswith(".html"):
            size = os.path.getsize(os.path.join(tags_output_dir, f))
            print(f"  {f} ({size:,} bytes)")
    print()

    print("태그 페이지 생성 데모가 완료되었습니다!")
