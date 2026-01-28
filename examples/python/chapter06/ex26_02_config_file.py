"""
예제 26-02: 블로그 설정 파일 관리

configparser 모듈을 사용하여 블로그의 설정을 읽고, 쓰고, 수정합니다.
설정 파일(INI 형식)로 블로그의 제목, 저자, 빌드 옵션 등을 관리합니다.
"""

import configparser
import os
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
        """설정 파일 경로를 받아 초기화합니다.

        Args:
            config_path: 설정 파일(INI) 경로
        """
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()

    def create_default(self):
        """기본 설정 파일을 생성합니다."""
        for section, values in self.DEFAULTS.items():
            self.config[section] = values

        # 디렉토리가 없으면 생성
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # 파일에 저장
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def load(self) -> bool:
        """설정 파일을 읽어옵니다.

        Returns:
            읽기 성공 여부
        """
        if not self.config_path.exists():
            print(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
            return False

        self.config.read(str(self.config_path), encoding="utf-8")
        return True

    def save(self):
        """현재 설정을 파일에 저장합니다."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def get(self, section: str, key: str, fallback: str = "") -> str:
        """설정값을 가져옵니다.

        Args:
            section: 섹션 이름
            key: 키 이름
            fallback: 기본값

        Returns:
            설정값 문자열
        """
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """불린 설정값을 가져옵니다.

        Args:
            section: 섹션 이름
            key: 키 이름
            fallback: 기본값

        Returns:
            불린 값
        """
        return self.config.getboolean(section, key, fallback=fallback)

    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """정수 설정값을 가져옵니다.

        Args:
            section: 섹션 이름
            key: 키 이름
            fallback: 기본값

        Returns:
            정수 값
        """
        return self.config.getint(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        """설정값을 변경합니다.

        Args:
            section: 섹션 이름
            key: 키 이름
            value: 새로운 값
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)

    def display(self):
        """현재 설정을 보기 좋게 출력합니다."""
        for section in self.config.sections():
            print(f"[{section}]")
            for key, value in self.config.items(section):
                print(f"  {key} = {value}")
            print()


if __name__ == "__main__":
    config_path = "/tmp/my-vibe-blog/config.ini"

    print("=" * 50)
    print("  블로그 설정 파일 관리 데모")
    print("=" * 50)
    print()

    # 1. 기본 설정 생성
    print("[1단계] 기본 설정 파일 생성")
    print("-" * 40)
    blog_config = BlogConfig(config_path)
    blog_config.create_default()
    print(f"설정 파일이 생성되었습니다: {config_path}")
    print()

    # 2. 설정 파일 내용 확인
    print("[2단계] 생성된 설정 파일 내용")
    print("-" * 40)
    with open(config_path, "r", encoding="utf-8") as f:
        print(f.read())

    # 3. 설정 읽기
    print("[3단계] 설정값 읽기")
    print("-" * 40)
    blog_config.load()

    title = blog_config.get("blog", "title")
    author = blog_config.get("blog", "author")
    posts_per_page = blog_config.get_int("blog", "posts_per_page")
    clean_build = blog_config.get_bool("build", "clean_before_build")
    show_tags = blog_config.get_bool("style", "show_tags")

    print(f"  블로그 제목: {title}")
    print(f"  저자: {author}")
    print(f"  페이지당 글 수: {posts_per_page} (정수)")
    print(f"  빌드 전 정리: {clean_build} (불린)")
    print(f"  태그 표시: {show_tags} (불린)")
    print()

    # 4. 설정 수정
    print("[4단계] 설정 수정")
    print("-" * 40)
    blog_config.set("blog", "title", "바이브 코딩 블로그")
    blog_config.set("blog", "author", "AI 개발자")
    blog_config.set("blog", "posts_per_page", "5")
    blog_config.set("style", "theme", "dark")

    # 새로운 섹션 추가
    blog_config.set("seo", "enable_sitemap", "yes")
    blog_config.set("seo", "enable_rss", "yes")
    blog_config.set("seo", "keywords", "바이브코딩, AI, 프로그래밍")

    blog_config.save()
    print("설정이 수정되었습니다.")
    print()

    # 5. 수정된 설정 확인
    print("[5단계] 수정된 설정 확인")
    print("-" * 40)
    blog_config.load()
    blog_config.display()

    print("설정 파일 관리 데모가 완료되었습니다!")
