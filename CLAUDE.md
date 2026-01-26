# CLAUDE.md - 함께해요 바이브 코딩 프로젝트 가이드

## 프로젝트 개요
"함께해요 바이브 코딩"은 AI와 함께하는 새로운 프로그래밍 패러다임인 바이브 코딩(Vibe Coding)을 소개하는 한국어 전자책입니다.

## 프로젝트 정보
- **프로젝트명**: 함께해요 바이브 코딩 (JoinUsForVibeCoding)
- **형식**: 마크다운(Markdown) 전자책
- **대상 독자**: 프로그래밍 입문자 ~ 중급 개발자
- **분량**: 약 300페이지
- **언어**: 한국어

## 디렉토리 구조
```
/
├── CLAUDE.md           # 이 파일 - Claude Code 가이드라인
├── PRD.md              # 제품 요구사항 문서
├── TRD.md              # 기술 요구사항 문서
├── TODO.md             # 작업 목록
├── PLAN.md             # 실행 계획서
├── book/               # 전자책 본문
│   ├── 00-preface/     # 서문
│   ├── 01-introduction/# Part 1: 바이브 코딩 소개
│   ├── 02-getting-started/ # Part 2: 시작하기
│   ├── 03-fundamentals/    # Part 3: 기초
│   ├── 04-practical/       # Part 4: 실전
│   ├── 05-advanced/        # Part 5: 심화
│   ├── 06-projects/        # Part 6: 프로젝트
│   └── 07-appendix/        # 부록
├── examples/           # CLI 예제 코드
│   ├── python/
│   ├── javascript/
│   ├── bash/
│   └── outputs/        # 예제 실행 결과
└── assets/             # 이미지, 다이어그램 등
```

## 작성 규칙

### 마크다운 스타일
- 각 챕터는 `##`로 시작
- 섹션은 `###`, 서브섹션은 `####` 사용
- 코드 블록은 언어 지정 필수: ```python, ```bash 등
- 중요 내용은 `> **Note:**` 또는 `> **Tip:**` 형식 사용
- 경고는 `> **Warning:**` 형식 사용

### 예제 코드 규칙
- 모든 예제는 CLI에서 실행 가능해야 함
- 예제 코드와 실행 결과를 함께 포함
- 예제 파일은 `/examples/` 디렉토리에 저장
- 실행 결과는 `/examples/outputs/`에 저장

### 예제 형식
```markdown
**예제: 간단한 인사 프로그램**

```python
# examples/python/hello.py
print("안녕하세요, 바이브 코딩!")
```

**실행:**
```bash
$ python examples/python/hello.py
```

**결과:**
```
안녕하세요, 바이브 코딩!
```
```

### 챕터 파일 명명 규칙
- 형식: `XX-chapter-name.md`
- 예: `01-what-is-vibe-coding.md`, `02-why-vibe-coding.md`

### 용어 통일
| 영어 | 한국어 |
|------|--------|
| Vibe Coding | 바이브 코딩 |
| AI Assistant | AI 어시스턴트 |
| Prompt | 프롬프트 |
| CLI | CLI (Command Line Interface) |
| Terminal | 터미널 |
| Code Generation | 코드 생성 |

## Claude Code 작업 지침

### 챕터 작성 시
1. TODO.md에서 현재 작업할 챕터 확인
2. 해당 챕터의 목차와 핵심 내용 파악
3. 예제 코드 작성 및 실행 결과 확인
4. 마크다운 문서 작성
5. 예제 파일 저장

### 예제 실행 시
1. `/examples/` 디렉토리에 코드 파일 생성
2. Bash 도구로 실행
3. 결과를 본문에 포함
4. 필요시 `/examples/outputs/`에 결과 저장

### 품질 체크리스트
- [ ] 마크다운 문법 오류 없음
- [ ] 모든 코드 예제 실행 가능
- [ ] 실행 결과가 정확함
- [ ] 용어가 일관되게 사용됨
- [ ] 초보자도 이해할 수 있는 설명

## 주요 명령어

### 책 빌드 (추후 구현)
```bash
# 마크다운을 PDF로 변환
./scripts/build-pdf.sh

# 마크다운을 EPUB으로 변환
./scripts/build-epub.sh
```

### 예제 실행
```bash
# Python 예제
python examples/python/example_name.py

# JavaScript 예제
node examples/javascript/example_name.js

# Bash 예제
bash examples/bash/example_name.sh
```

## 참고 자료
- Andrej Karpathy의 바이브 코딩 소개
- Claude Code 공식 문서
- 각종 AI 코딩 도구 문서
