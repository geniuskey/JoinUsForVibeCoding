#!/usr/bin/env python3
"""
예제 24-06: README 템플릿
- 프로젝트 README.md를 자동으로 생성하는 도구
- 프로젝트 정보를 입력받아 구조화된 README 마크다운 생성
- Python 표준 라이브러리만 사용
"""

import os
import textwrap
from string import Template
from datetime import datetime
from dataclasses import dataclass, field


# ============================================================
# 1. 프로젝트 정보 데이터 클래스
# ============================================================

@dataclass
class ProjectInfo:
    """프로젝트 메타 정보"""
    name: str                                  # 프로젝트 이름
    description: str                           # 프로젝트 설명
    version: str = "0.1.0"                     # 버전
    author: str = ""                           # 작성자
    license_type: str = "MIT"                  # 라이선스
    python_version: str = "3.10+"              # 필요한 Python 버전
    repo_url: str = ""                         # 저장소 URL
    features: list = field(default_factory=list)  # 주요 기능 목록
    install_steps: list = field(default_factory=list)  # 설치 단계
    usage_examples: list = field(default_factory=list)  # 사용 예시
    dependencies: list = field(default_factory=list)  # 의존성
    directory_structure: dict = field(default_factory=dict)  # 디렉토리 구조
    contributing: bool = True                  # 기여 가이드 포함 여부
    badges: list = field(default_factory=list)  # 뱃지 목록


# ============================================================
# 2. README 섹션 생성기들
# ============================================================

class ReadmeSection:
    """README의 개별 섹션을 생성하는 기본 클래스"""

    def __init__(self, title: str):
        self.title = title

    def render(self, info: ProjectInfo) -> str:
        """섹션 내용을 마크다운으로 렌더링 (서브클래스에서 구현)"""
        raise NotImplementedError


class HeaderSection(ReadmeSection):
    """프로젝트 헤더 (제목, 뱃지, 설명)"""

    def __init__(self):
        super().__init__("헤더")

    def render(self, info: ProjectInfo) -> str:
        lines = [f"# {info.name}", ""]

        # 뱃지
        if info.badges:
            badge_line = " ".join(info.badges)
            lines.append(badge_line)
            lines.append("")

        # 설명
        lines.append(f"> {info.description}")
        lines.append("")

        # 기본 정보 테이블
        lines.append("| 항목 | 내용 |")
        lines.append("|------|------|")
        lines.append(f"| 버전 | {info.version} |")
        if info.author:
            lines.append(f"| 작성자 | {info.author} |")
        lines.append(f"| 라이선스 | {info.license_type} |")
        lines.append(f"| Python | {info.python_version} |")
        lines.append("")

        return "\n".join(lines)


class FeaturesSection(ReadmeSection):
    """주요 기능 섹션"""

    def __init__(self):
        super().__init__("주요 기능")

    def render(self, info: ProjectInfo) -> str:
        if not info.features:
            return ""

        lines = ["## 주요 기능", ""]
        for feature in info.features:
            lines.append(f"- {feature}")
        lines.append("")

        return "\n".join(lines)


class InstallSection(ReadmeSection):
    """설치 방법 섹션"""

    def __init__(self):
        super().__init__("설치 방법")

    def render(self, info: ProjectInfo) -> str:
        lines = ["## 설치 방법", ""]

        # 기본 설치 단계
        if info.install_steps:
            for i, step in enumerate(info.install_steps, 1):
                lines.append(f"{i}. {step}")
        else:
            # 기본 설치 가이드
            lines.append("```bash")
            lines.append(f"# 저장소 클론")
            if info.repo_url:
                lines.append(f"git clone {info.repo_url}")
            else:
                lines.append(f"git clone https://github.com/username/{info.name.lower().replace(' ', '-')}.git")
            lines.append(f"cd {info.name.lower().replace(' ', '-')}")
            lines.append("")
            lines.append("# 가상환경 생성 및 활성화")
            lines.append("python -m venv venv")
            lines.append("source venv/bin/activate  # Linux/Mac")
            lines.append("# venv\\Scripts\\activate  # Windows")
            lines.append("")
            if info.dependencies:
                lines.append("# 의존성 설치")
                lines.append("pip install -r requirements.txt")
            lines.append("```")

        lines.append("")
        return "\n".join(lines)


class UsageSection(ReadmeSection):
    """사용법 섹션"""

    def __init__(self):
        super().__init__("사용법")

    def render(self, info: ProjectInfo) -> str:
        lines = ["## 사용법", ""]

        if info.usage_examples:
            for example in info.usage_examples:
                if isinstance(example, dict):
                    lines.append(f"### {example.get('title', '예시')}")
                    lines.append("")
                    if "description" in example:
                        lines.append(example["description"])
                        lines.append("")
                    lines.append(f"```{example.get('language', 'python')}")
                    lines.append(example.get("code", ""))
                    lines.append("```")
                    lines.append("")
                else:
                    lines.append(f"- {example}")
        else:
            lines.append("```python")
            module_name = info.name.lower().replace(" ", "_").replace("-", "_")
            lines.append(f"from {module_name} import main")
            lines.append("")
            lines.append("# 기본 사용법")
            lines.append("result = main()")
            lines.append("print(result)")
            lines.append("```")

        lines.append("")
        return "\n".join(lines)


class DirectorySection(ReadmeSection):
    """디렉토리 구조 섹션"""

    def __init__(self):
        super().__init__("디렉토리 구조")

    def render(self, info: ProjectInfo) -> str:
        if not info.directory_structure:
            return ""

        lines = ["## 프로젝트 구조", "", "```"]
        self._render_tree(lines, info.directory_structure, prefix="")
        lines.append("```")
        lines.append("")

        return "\n".join(lines)

    def _render_tree(self, lines: list, structure: dict,
                     prefix: str, is_last: bool = True):
        """디렉토리 트리를 텍스트로 렌더링"""
        items = list(structure.items())
        for i, (name, children) in enumerate(items):
            is_final = (i == len(items) - 1)
            connector = "└── " if is_final else "├── "
            lines.append(f"{prefix}{connector}{name}")

            if isinstance(children, dict) and children:
                extension = "    " if is_final else "│   "
                self._render_tree(lines, children, prefix + extension, is_final)


class DependenciesSection(ReadmeSection):
    """의존성 섹션"""

    def __init__(self):
        super().__init__("의존성")

    def render(self, info: ProjectInfo) -> str:
        if not info.dependencies:
            return ""

        lines = ["## 의존성", "", "| 패키지 | 용도 |", "|--------|------|"]
        for dep in info.dependencies:
            if isinstance(dep, dict):
                lines.append(f"| {dep['name']} | {dep.get('purpose', '-')} |")
            else:
                lines.append(f"| {dep} | - |")
        lines.append("")

        return "\n".join(lines)


class ContributingSection(ReadmeSection):
    """기여 가이드 섹션"""

    def __init__(self):
        super().__init__("기여 가이드")

    def render(self, info: ProjectInfo) -> str:
        if not info.contributing:
            return ""

        lines = [
            "## 기여 방법",
            "",
            "프로젝트에 기여해 주셔서 감사합니다! 다음 단계를 따라주세요:",
            "",
            "1. 이 저장소를 Fork합니다",
            "2. 새 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)",
            "3. 변경사항을 커밋합니다 (`git commit -m 'feat: 놀라운 기능 추가'`)",
            "4. 브랜치에 Push합니다 (`git push origin feature/amazing-feature`)",
            "5. Pull Request를 생성합니다",
            "",
            "### 커밋 메시지 규칙",
            "",
            "| 접두사 | 설명 |",
            "|--------|------|",
            "| feat | 새로운 기능 추가 |",
            "| fix | 버그 수정 |",
            "| docs | 문서 수정 |",
            "| style | 코드 포맷팅 |",
            "| refactor | 리팩토링 |",
            "| test | 테스트 추가/수정 |",
            "",
        ]

        return "\n".join(lines)


class LicenseSection(ReadmeSection):
    """라이선스 섹션"""

    def __init__(self):
        super().__init__("라이선스")

    def render(self, info: ProjectInfo) -> str:
        year = datetime.now().year
        author = info.author or "저자명"
        lines = [
            "## 라이선스",
            "",
            f"이 프로젝트는 {info.license_type} 라이선스 하에 배포됩니다.",
            f"자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.",
            "",
            "---",
            "",
            f"*Copyright (c) {year} {author}*",
            "",
        ]

        return "\n".join(lines)


# ============================================================
# 3. README 생성기
# ============================================================

class ReadmeGenerator:
    """README.md 파일을 자동으로 생성하는 도구"""

    def __init__(self):
        self.sections = [
            HeaderSection(),
            FeaturesSection(),
            InstallSection(),
            UsageSection(),
            DirectorySection(),
            DependenciesSection(),
            ContributingSection(),
            LicenseSection(),
        ]

    def generate(self, info: ProjectInfo) -> str:
        """프로젝트 정보를 바탕으로 README.md 내용 생성"""
        parts = []

        for section in self.sections:
            content = section.render(info)
            if content:
                parts.append(content)

        return "\n".join(parts)


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-06: README 템플릿 자동 생성 도구")
    print("=" * 60)

    # 프로젝트 정보 정의
    project = ProjectInfo(
        name="바이브 코딩 도우미",
        description="AI와 함께하는 코딩을 더 쉽고 효율적으로 만드는 CLI 도구",
        version="1.0.0",
        author="바이브 코더",
        license_type="MIT",
        python_version="3.10+",
        repo_url="https://github.com/vibecoder/vibe-coding-helper",
        features=[
            "프롬프트 템플릿 관리 및 자동 생성",
            "코드 품질 자동 검사 (린팅, 포맷팅)",
            "docstring 자동 생성 및 검사",
            "프로젝트 구조 분석 및 시각화",
            "다국어 지원 (한국어, 영어)",
        ],
        usage_examples=[
            {
                "title": "프롬프트 템플릿 사용",
                "language": "python",
                "description": "미리 정의된 템플릿으로 프롬프트를 빠르게 생성합니다.",
                "code": textwrap.dedent("""\
                    from vibe_helper import PromptLibrary

                    library = PromptLibrary()
                    prompt = library.render("기능_구현",
                        feature_name="로그인 시스템",
                        language="Python"
                    )
                    print(prompt)"""),
            },
            {
                "title": "코드 품질 검사",
                "language": "bash",
                "description": "CLI에서 코드 품질을 검사합니다.",
                "code": textwrap.dedent("""\
                    # 단일 파일 검사
                    python -m vibe_helper lint mycode.py

                    # 프로젝트 전체 검사
                    python -m vibe_helper lint ./src/"""),
            },
        ],
        dependencies=[
            {"name": "Python 3.10+", "purpose": "런타임 환경"},
            {"name": "ast (내장)", "purpose": "코드 분석"},
            {"name": "textwrap (내장)", "purpose": "텍스트 포맷팅"},
        ],
        directory_structure={
            "vibe-coding-helper/": {
                "src/": {
                    "vibe_helper/": {
                        "__init__.py": None,
                        "prompt.py": None,
                        "linter.py": None,
                        "formatter.py": None,
                        "docstring.py": None,
                    }
                },
                "tests/": {
                    "test_prompt.py": None,
                    "test_linter.py": None,
                },
                "docs/": {
                    "guide.md": None,
                    "api.md": None,
                },
                "README.md": None,
                "setup.py": None,
                "requirements.txt": None,
            }
        },
        contributing=True,
    )

    # README 생성
    generator = ReadmeGenerator()
    readme_content = generator.generate(project)

    # 생성된 README 출력
    print("\n생성된 README.md 내용:")
    print("=" * 60)
    print(readme_content)
    print("=" * 60)

    # 통계
    lines = readme_content.split("\n")
    sections = [l for l in lines if l.startswith("## ")]
    print(f"\n[생성 통계]")
    print(f"  - 총 줄 수: {len(lines)}줄")
    print(f"  - 섹션 수: {len(sections)}개")
    for section in sections:
        print(f"    - {section}")
    print(f"  - 문자 수: {len(readme_content)}자")

    print(f"\n모범 사례: 프로젝트 시작 시 README를 먼저 작성하면")
    print(f"프로젝트의 목표와 구조를 명확히 할 수 있습니다!")
    print(f"(README-Driven Development)")
