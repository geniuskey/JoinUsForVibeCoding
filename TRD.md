# TRD (Technical Requirements Document)
# 함께해요 바이브 코딩 - 기술 요구사항 문서

**버전**: 1.0
**작성일**: 2026-01-26
**상태**: Draft

---

## 1. 기술 개요 (Technical Overview)

### 1.1 프로젝트 기술 스택
```
┌─────────────────────────────────────────────────────────┐
│                    콘텐츠 레이어                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Markdown   │  │   예제코드    │  │   Assets    │     │
│  │   (.md)     │  │ (py,js,sh)  │  │  (images)   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                    빌드 레이어                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Pandoc     │  │   mdbook    │  │  Scripts    │     │
│  │ (PDF/EPUB)  │  │   (HTML)    │  │   (Bash)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                    실행 환경                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Python     │  │   Node.js   │  │    Bash     │     │
│  │   3.10+     │  │    18+      │  │    5.0+     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

### 1.2 개발 도구
| 도구 | 버전 | 용도 |
|------|------|------|
| Git | 2.40+ | 버전 관리 |
| Python | 3.10+ | 예제 실행 |
| Node.js | 18+ | JavaScript 예제 |
| Bash | 5.0+ | 쉘 스크립트 |
| Pandoc | 3.0+ | 문서 변환 |

---

## 2. 디렉토리 구조 상세 (Directory Structure)

```
JoinUsForVibeCoding/
├── .github/
│   └── workflows/
│       └── build.yml           # CI/CD 파이프라인
│
├── book/                        # 전자책 본문
│   ├── 00-preface/
│   │   └── 00-preface.md       # 서문
│   │
│   ├── 01-introduction/         # Part 1: 바이브 코딩 소개
│   │   ├── 01-what-is-vibe-coding.md
│   │   ├── 02-history-and-origin.md
│   │   ├── 03-traditional-vs-vibe.md
│   │   ├── 04-ai-assistants.md
│   │   └── 05-future-of-coding.md
│   │
│   ├── 02-getting-started/      # Part 2: 시작하기
│   │   ├── 01-environment-setup.md
│   │   ├── 02-cli-basics.md
│   │   ├── 03-installing-ai-tools.md
│   │   └── 04-first-vibe-coding.md
│   │
│   ├── 03-fundamentals/         # Part 3: 기초
│   │   ├── 01-prompt-engineering.md
│   │   ├── 02-conversation-with-ai.md
│   │   ├── 03-code-review.md
│   │   ├── 04-debugging-with-ai.md
│   │   └── 05-iterative-development.md
│   │
│   ├── 04-practical/            # Part 4: 실전
│   │   ├── 01-file-automation.md
│   │   ├── 02-data-processing.md
│   │   ├── 03-api-integration.md
│   │   ├── 04-web-scraping.md
│   │   └── 05-cli-tools.md
│   │
│   ├── 05-advanced/             # Part 5: 심화
│   │   ├── 01-project-management.md
│   │   ├── 02-test-driven-vibe.md
│   │   ├── 03-performance.md
│   │   ├── 04-security.md
│   │   └── 05-best-practices.md
│   │
│   ├── 06-projects/             # Part 6: 프로젝트
│   │   ├── 01-todo-cli-app.md
│   │   ├── 02-markdown-blog-generator.md
│   │   └── 03-data-dashboard.md
│   │
│   └── 07-appendix/             # 부록
│       ├── A-tool-comparison.md
│       ├── B-prompt-templates.md
│       ├── C-troubleshooting.md
│       └── D-glossary.md
│
├── examples/                    # 예제 코드
│   ├── python/
│   │   ├── chapter03/
│   │   ├── chapter04/
│   │   ├── chapter05/
│   │   └── projects/
│   │
│   ├── javascript/
│   │   ├── chapter03/
│   │   ├── chapter04/
│   │   ├── chapter05/
│   │   └── projects/
│   │
│   ├── bash/
│   │   ├── chapter02/
│   │   ├── chapter04/
│   │   └── scripts/
│   │
│   └── outputs/                 # 예제 실행 결과
│       ├── python/
│       ├── javascript/
│       └── bash/
│
├── assets/                      # 정적 자원
│   ├── images/
│   │   ├── diagrams/
│   │   └── screenshots/
│   └── templates/
│
├── scripts/                     # 빌드 및 유틸리티 스크립트
│   ├── build-pdf.sh
│   ├── build-epub.sh
│   ├── build-html.sh
│   ├── test-examples.sh
│   └── validate-markdown.sh
│
├── config/                      # 설정 파일
│   ├── pandoc.yaml
│   └── mdbook.toml
│
├── CLAUDE.md                    # Claude Code 가이드라인
├── PRD.md                       # 제품 요구사항
├── TRD.md                       # 기술 요구사항 (이 문서)
├── TODO.md                      # 작업 목록
├── PLAN.md                      # 실행 계획
├── README.md                    # 프로젝트 소개
└── .gitignore                   # Git 제외 파일
```

---

## 3. 마크다운 규격 (Markdown Specification)

### 3.1 파일 구조
각 챕터 파일은 다음 구조를 따릅니다:

```markdown
# 챕터 제목

> 한 줄 요약 또는 인용구

## 학습 목표
이 장을 마치면 다음을 할 수 있습니다:
- 목표 1
- 목표 2
- 목표 3

---

## 섹션 1

### 서브섹션 1.1

내용...

---

## 섹션 2

### 서브섹션 2.1

내용...

---

## 실습

### 실습 1: 제목

**목표**: 실습 목표 설명

**코드**:
```python
# 코드 내용
```

**실행**:
```bash
$ python example.py
```

**예상 결과**:
```
출력 결과
```

---

## 정리

이 장에서 배운 내용:
- 요점 1
- 요점 2
- 요점 3

## 다음 장 예고

다음 장에서는...
```

### 3.2 코드 블록 규칙

#### 인라인 코드
```markdown
변수 `count`를 사용하여...
`print()` 함수는...
```

#### 코드 블록
```markdown
```python
# 파일: examples/python/hello.py
def greet(name):
    return f"안녕하세요, {name}님!"

print(greet("바이브"))
```
```

#### 실행 명령어
```markdown
```bash
$ python examples/python/hello.py
```
```

#### 실행 결과
```markdown
```
안녕하세요, 바이브님!
```
```

### 3.3 특수 블록

#### 정보 박스
```markdown
> **Note:** 참고할 정보입니다.
```

#### 팁 박스
```markdown
> **Tip:** 유용한 팁입니다.
```

#### 경고 박스
```markdown
> **Warning:** 주의해야 할 사항입니다.
```

#### 프롬프트 예시
```markdown
> **Prompt:**
> "Python으로 1부터 10까지 합을 구하는 프로그램을 작성해줘"
```

---

## 4. 예제 코드 규격 (Example Code Specification)

### 4.1 파일 명명 규칙
```
examples/
├── python/
│   ├── chapter03/
│   │   ├── 01_hello_world.py
│   │   ├── 02_variables.py
│   │   └── 03_functions.py
│   └── ...
```

**명명 규칙**:
- 소문자와 언더스코어 사용
- 번호 접두사로 순서 표시
- 명확한 설명적 이름

### 4.2 코드 템플릿

#### Python 예제 템플릿
```python
#!/usr/bin/env python3
"""
예제: [예제 제목]
챕터: [챕터 번호]
설명: [간단한 설명]
"""

def main():
    # 메인 로직
    pass

if __name__ == "__main__":
    main()
```

#### JavaScript 예제 템플릿
```javascript
#!/usr/bin/env node
/**
 * 예제: [예제 제목]
 * 챕터: [챕터 번호]
 * 설명: [간단한 설명]
 */

function main() {
    // 메인 로직
}

main();
```

#### Bash 예제 템플릿
```bash
#!/bin/bash
# 예제: [예제 제목]
# 챕터: [챕터 번호]
# 설명: [간단한 설명]

main() {
    # 메인 로직
    echo "Hello, Vibe Coding!"
}

main
```

### 4.3 결과 저장 형식
```
examples/outputs/
├── python/
│   └── chapter03/
│       ├── 01_hello_world.txt
│       └── 02_variables.txt
```

결과 파일 내용:
```
=== 실행 정보 ===
파일: examples/python/chapter03/01_hello_world.py
실행일: 2026-01-26
Python: 3.10.12

=== 실행 결과 ===
안녕하세요, 바이브 코딩!

=== 종료 코드 ===
0
```

---

## 5. 빌드 시스템 (Build System)

### 5.1 PDF 빌드
```bash
#!/bin/bash
# scripts/build-pdf.sh

BOOK_DIR="book"
OUTPUT_DIR="output"
OUTPUT_FILE="함께해요_바이브_코딩.pdf"

# 모든 마크다운 파일 수집
find "$BOOK_DIR" -name "*.md" -type f | sort > /tmp/book_files.txt

# Pandoc으로 PDF 생성
pandoc \
    --from=markdown \
    --to=pdf \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    --metadata-file=config/pandoc.yaml \
    --output="$OUTPUT_DIR/$OUTPUT_FILE" \
    $(cat /tmp/book_files.txt)
```

### 5.2 EPUB 빌드
```bash
#!/bin/bash
# scripts/build-epub.sh

BOOK_DIR="book"
OUTPUT_DIR="output"
OUTPUT_FILE="함께해요_바이브_코딩.epub"

pandoc \
    --from=markdown \
    --to=epub3 \
    --toc \
    --toc-depth=3 \
    --metadata-file=config/pandoc.yaml \
    --output="$OUTPUT_DIR/$OUTPUT_FILE" \
    $(find "$BOOK_DIR" -name "*.md" | sort)
```

### 5.3 HTML 빌드 (mdBook)
```toml
# config/mdbook.toml
[book]
title = "함께해요 바이브 코딩"
authors = ["저자명"]
language = "ko"
src = "book"

[output.html]
default-theme = "light"
git-repository-url = "https://github.com/..."
```

---

## 6. 테스트 시스템 (Testing System)

### 6.1 예제 코드 테스트
```bash
#!/bin/bash
# scripts/test-examples.sh

set -e

echo "=== Python 예제 테스트 ==="
for file in examples/python/**/*.py; do
    echo "Testing: $file"
    python "$file" > /dev/null 2>&1
    echo "✓ Passed"
done

echo "=== JavaScript 예제 테스트 ==="
for file in examples/javascript/**/*.js; do
    echo "Testing: $file"
    node "$file" > /dev/null 2>&1
    echo "✓ Passed"
done

echo "=== Bash 예제 테스트 ==="
for file in examples/bash/**/*.sh; do
    echo "Testing: $file"
    bash "$file" > /dev/null 2>&1
    echo "✓ Passed"
done

echo "=== 모든 테스트 통과 ==="
```

### 6.2 마크다운 검증
```bash
#!/bin/bash
# scripts/validate-markdown.sh

echo "=== 마크다운 문법 검사 ==="
for file in book/**/*.md; do
    echo "Checking: $file"
    # markdownlint 또는 다른 린터 사용
done
```

---

## 7. 의존성 (Dependencies)

### 7.1 Python 패키지
```
# requirements.txt
requests>=2.28.0      # HTTP 요청
beautifulsoup4>=4.12  # 웹 스크래핑
pandas>=2.0.0         # 데이터 처리
click>=8.1.0          # CLI 도구
rich>=13.0.0          # 터미널 출력
```

### 7.2 Node.js 패키지
```json
// package.json
{
  "dependencies": {
    "axios": "^1.6.0",
    "commander": "^11.0.0",
    "chalk": "^5.3.0"
  }
}
```

### 7.3 시스템 도구
```bash
# 필수 시스템 도구
- git
- python3
- node
- npm
- bash

# 빌드 도구 (선택)
- pandoc
- xelatex (texlive)
- mdbook
```

---

## 8. CI/CD 파이프라인

### 8.1 GitHub Actions
```yaml
# .github/workflows/build.yml
name: Build Book

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Run example tests
        run: ./scripts/test-examples.sh

  build-pdf:
    needs: test-examples
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Pandoc
        run: sudo apt-get install -y pandoc texlive-xetex

      - name: Build PDF
        run: ./scripts/build-pdf.sh

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: book-pdf
          path: output/*.pdf
```

---

## 9. 보안 고려사항 (Security Considerations)

### 9.1 예제 코드 보안
- API 키, 비밀번호 등 민감 정보 하드코딩 금지
- 환경 변수 또는 설정 파일 사용 예시 제공
- 실제 동작하는 예제는 안전한 대상(로컬, 테스트 서버)만 사용

### 9.2 사용자 입력 처리
```python
# 나쁜 예
user_input = input("명령어: ")
os.system(user_input)  # 위험!

# 좋은 예
import shlex
import subprocess

user_input = input("파일명: ")
sanitized = shlex.quote(user_input)
subprocess.run(["cat", sanitized], check=True)
```

---

## 10. 버전 관리 전략

### 10.1 브랜치 전략
```
main                 # 안정 버전
├── develop          # 개발 버전
│   ├── feature/*    # 기능 개발
│   └── fix/*        # 버그 수정
└── release/*        # 릴리스 준비
```

### 10.2 커밋 메시지 규칙
```
type(scope): subject

- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- style: 포맷팅
- refactor: 리팩토링
- test: 테스트
- chore: 기타 작업

예시:
feat(chapter03): 프롬프트 엔지니어링 챕터 추가
fix(examples): Python 예제 실행 오류 수정
docs(readme): 설치 가이드 업데이트
```

---

## 11. 페이지 추정 (Page Estimation)

### 11.1 페이지 계산 기준
- A4 기준, 11pt 폰트
- 한 페이지당 약 500-600자 (한국어)
- 코드 블록은 약 30줄/페이지

### 11.2 파트별 페이지 배분
| 파트 | 챕터 수 | 예상 페이지 |
|------|---------|-------------|
| 서문 | 1 | 5 |
| Part 1: 소개 | 5 | 40 |
| Part 2: 시작하기 | 4 | 30 |
| Part 3: 기초 | 5 | 50 |
| Part 4: 실전 | 5 | 60 |
| Part 5: 심화 | 5 | 50 |
| Part 6: 프로젝트 | 3 | 50 |
| 부록 | 4 | 20 |
| **총계** | **32** | **305** |
