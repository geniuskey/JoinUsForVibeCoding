"""
예제 20-08: 실습 - 패키지로 배포 준비
setup.py와 pyproject.toml 파일을 생성하여
파이썬 패키지를 배포할 수 있도록 준비합니다.
"""

import os
import tempfile
import shutil


def create_setup_py(project_dir, package_info):
    """전통적인 setup.py 파일을 생성합니다."""
    content = f'''"""
{package_info["name"]} 패키지 설치 스크립트
"""
from setuptools import setup, find_packages

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # --- 기본 정보 ---
    name="{package_info["name"]}",
    version="{package_info["version"]}",
    author="{package_info["author"]}",
    author_email="{package_info["email"]}",
    description="{package_info["description"]}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="{package_info["url"]}",

    # --- 패키지 설정 ---
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires=">={package_info["python_requires"]}",

    # --- 의존성 ---
    install_requires=[
        # 런타임 의존성
    ],
    extras_require={{
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
        "docs": [
            "sphinx>=7.0",
            "sphinx-rtd-theme>=1.0",
        ],
    }},

    # --- 분류 정보 (PyPI) ---
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],

    # --- 키워드 ---
    keywords="{package_info["keywords"]}",

    # --- 진입점 (CLI 명령어) ---
    entry_points={{
        "console_scripts": [
            "{package_info["name"]}={package_info["name"]}.cli:main",
        ],
    }},
)
'''

    filepath = os.path.join(project_dir, "setup.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def create_pyproject_toml(project_dir, package_info):
    """현대적인 pyproject.toml 파일을 생성합니다."""
    content = f'''# pyproject.toml - 현대적인 파이썬 프로젝트 설정 파일
# PEP 518, PEP 621 표준을 따릅니다

# ========================================
# 빌드 시스템 설정
# ========================================
[build-system]
requires = ["setuptools>=68.0", "wheel>=0.41"]
build-backend = "setuptools.backends._legacy:_Backend"

# ========================================
# 프로젝트 메타데이터
# ========================================
[project]
name = "{package_info["name"]}"
version = "{package_info["version"]}"
description = "{package_info["description"]}"
readme = "README.md"
license = {{text = "MIT"}}
requires-python = ">={package_info["python_requires"]}"

authors = [
    {{name = "{package_info["author"]}", email = "{package_info["email"]}"}},
]

keywords = [{", ".join(f'"{k}"' for k in package_info["keywords"].split(", "))}]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

# 런타임 의존성
dependencies = []

# ========================================
# 선택적 의존성
# ========================================
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
]
docs = [
    "sphinx>=7.0",
    "sphinx-rtd-theme>=1.0",
]

# ========================================
# CLI 진입점
# ========================================
[project.scripts]
{package_info["name"]} = "{package_info["name"]}.cli:main"

# ========================================
# URL 링크
# ========================================
[project.urls]
Homepage = "{package_info["url"]}"
Documentation = "{package_info["url"]}/docs"
Repository = "{package_info["url"]}"
"Bug Tracker" = "{package_info["url"]}/issues"

# ========================================
# 도구 설정
# ========================================
[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
'''

    filepath = os.path.join(project_dir, "pyproject.toml")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def create_manifest(project_dir):
    """MANIFEST.in 파일을 생성합니다 (배포에 포함할 파일 지정)."""
    content = """# MANIFEST.in - 소스 배포에 포함할 추가 파일

# 문서 파일 포함
include README.md
include LICENSE
include CHANGELOG.md

# 설정 파일 포함
include pyproject.toml
include setup.cfg

# 테스트 파일 포함
recursive-include tests *.py

# 불필요한 파일 제외
global-exclude *.pyc
global-exclude __pycache__
global-exclude *.egg-info
"""
    filepath = os.path.join(project_dir, "MANIFEST.in")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def create_license(project_dir, author):
    """MIT 라이선스 파일을 생성합니다."""
    content = f"""MIT License

Copyright (c) 2024 {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    filepath = os.path.join(project_dir, "LICENSE")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def create_readme(project_dir, package_info):
    """README.md 파일을 생성합니다."""
    content = f"""# {package_info["name"]}

{package_info["description"]}

## 설치

```bash
pip install {package_info["name"]}
```

## 개발 환경 설치

```bash
pip install -e ".[dev]"
```

## 사용법

```python
import {package_info["name"]}
```

## 라이선스

MIT License
"""
    filepath = os.path.join(project_dir, "README.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def create_package_source(project_dir, package_name):
    """패키지 소스 코드를 생성합니다."""
    src_dir = os.path.join(project_dir, "src", package_name)
    os.makedirs(src_dir, exist_ok=True)

    # __init__.py
    init_content = f'"""{package_name} 패키지"""\n\n__version__ = "0.1.0"\n'
    with open(os.path.join(src_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(init_content)

    # cli.py
    cli_content = f'''"""CLI 진입점"""

def main():
    """메인 CLI 함수"""
    print("{package_name} v0.1.0")

if __name__ == "__main__":
    main()
'''
    with open(os.path.join(src_dir, "cli.py"), "w", encoding="utf-8") as f:
        f.write(cli_content)

    # tests 디렉토리
    tests_dir = os.path.join(project_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")
    with open(os.path.join(tests_dir, "test_main.py"), "w", encoding="utf-8") as f:
        f.write(f'"""기본 테스트"""\n\ndef test_import():\n    import {package_name}\n    assert {package_name}.__version__ == "0.1.0"\n')


def print_tree(directory, prefix="", is_last=True, is_root=True):
    """디렉토리 구조를 tree 형태로 출력합니다."""
    basename = os.path.basename(directory)

    if is_root:
        print(f"  {basename}/")
    else:
        connector = "└── " if is_last else "├── "
        if os.path.isdir(directory):
            print(f"  {prefix}{connector}{basename}/")
        else:
            print(f"  {prefix}{connector}{basename}")

    if os.path.isdir(directory):
        entries = sorted(os.listdir(directory))
        dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
        sorted_entries = dirs + files

        for i, entry in enumerate(sorted_entries):
            entry_path = os.path.join(directory, entry)
            is_last_entry = (i == len(sorted_entries) - 1)
            new_prefix = prefix + ("    " if is_last or is_root else "│   ")
            print_tree(entry_path, new_prefix, is_last_entry, is_root=False)


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-08: 패키지로 배포 준비")
    print("=" * 60)
    print()

    # 패키지 정보 정의
    package_info = {
        "name": "vibecoding_utils",
        "version": "0.1.0",
        "author": "바이브 코더",
        "email": "vibe@example.com",
        "description": "바이브 코딩을 위한 유틸리티 패키지",
        "url": "https://github.com/vibecoder/vibecoding-utils",
        "python_requires": "3.9",
        "keywords": "vibe, coding, utility, python",
    }

    temp_dir = tempfile.mkdtemp()
    project_dir = os.path.join(temp_dir, package_info["name"])
    os.makedirs(project_dir)

    try:
        # --- 1단계: 배포 파일 생성 ---
        print("--- 1단계: 배포용 파일 생성 ---")
        print()

        created_files = []

        # setup.py 생성
        filepath = create_setup_py(project_dir, package_info)
        created_files.append("setup.py")
        print(f"  생성: setup.py (전통적 설치 스크립트)")

        # pyproject.toml 생성
        filepath = create_pyproject_toml(project_dir, package_info)
        created_files.append("pyproject.toml")
        print(f"  생성: pyproject.toml (현대적 프로젝트 설정)")

        # MANIFEST.in 생성
        filepath = create_manifest(project_dir)
        created_files.append("MANIFEST.in")
        print(f"  생성: MANIFEST.in (배포 포함 파일 목록)")

        # LICENSE 생성
        filepath = create_license(project_dir, package_info["author"])
        created_files.append("LICENSE")
        print(f"  생성: LICENSE (MIT 라이선스)")

        # README.md 생성
        filepath = create_readme(project_dir, package_info)
        created_files.append("README.md")
        print(f"  생성: README.md (프로젝트 설명)")

        # 소스 코드 생성
        create_package_source(project_dir, package_info["name"])
        print(f"  생성: src/{package_info['name']}/ (패키지 소스)")
        print(f"  생성: tests/ (테스트 코드)")
        print()

        # --- 2단계: 프로젝트 구조 확인 ---
        print("--- 2단계: 생성된 프로젝트 구조 ---")
        print()
        print_tree(project_dir)
        print()

        # --- 3단계: setup.py 내용 확인 ---
        print("--- 3단계: setup.py 주요 내용 ---")
        print()
        setup_path = os.path.join(project_dir, "setup.py")
        with open(setup_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 핵심 부분만 출력
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
                print(f"  {line}")
        print()

        # --- 4단계: pyproject.toml 내용 확인 ---
        print("--- 4단계: pyproject.toml 주요 내용 ---")
        print()
        toml_path = os.path.join(project_dir, "pyproject.toml")
        with open(toml_path, "r", encoding="utf-8") as f:
            in_section = False
            for line in f:
                line = line.rstrip()
                if line.startswith("[") or (line.strip() and not line.startswith("#")):
                    print(f"  {line}")

        print()

        # --- 5단계: setup.py vs pyproject.toml 비교 ---
        print("--- 5단계: setup.py vs pyproject.toml 비교 ---")
        print()
        print(f"  {'항목':<20s} {'setup.py':<22s} {'pyproject.toml'}")
        print(f"  {'-'*20} {'-'*22} {'-'*22}")
        comparisons = [
            ("형식", "Python 코드", "TOML 설정 파일"),
            ("표준", "전통적 방식", "PEP 621 표준"),
            ("유연성", "높음 (코드 실행)", "제한적 (선언적)"),
            ("도구 설정", "별도 파일 필요", "통합 관리 가능"),
            ("권장 여부", "레거시 지원용", "신규 프로젝트 권장"),
        ]
        for item, setup, toml in comparisons:
            print(f"  {item:<20s} {setup:<22s} {toml}")
        print()

        # --- 6단계: 배포 명령어 안내 ---
        print("--- 6단계: 배포 명령어 안내 ---")
        print()
        print("  개발 모드 설치:")
        print("    pip install -e .")
        print()
        print("  배포 패키지 빌드:")
        print("    python -m build")
        print()
        print("  PyPI에 업로드:")
        print("    python -m twine upload dist/*")
        print()
        print("  테스트 PyPI에 먼저 업로드 (테스트용):")
        print("    python -m twine upload --repository testpypi dist/*")
        print()

        print("패키지 배포 준비 예제를 성공적으로 실행했습니다!")

    finally:
        shutil.rmtree(temp_dir)
        print("(임시 파일 정리 완료)")
