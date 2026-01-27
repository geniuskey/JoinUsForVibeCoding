## Chapter 8: AI 도구 설치 및 설정

바이브 코딩을 시작하려면 먼저 AI 도구를 올바르게 설치하고 설정해야 합니다. 이 장에서는 대표적인 AI CLI 도구인 Claude Code를 중심으로 설치부터 첫 실행까지의 전 과정을 안내합니다. 또한 API 키를 안전하게 관리하는 방법과 다른 AI 도구들도 함께 살펴봅니다.

### 학습 목표

- Claude Code를 설치하고 정상 동작을 확인할 수 있다
- 첫 실행 시 인증 과정을 이해하고 완료할 수 있다
- AI CLI 도구의 기본 사용법을 익힌다
- 설정 파일의 위치와 역할을 파악한다
- API 키를 안전하게 관리하는 방법을 실천할 수 있다

---

### 8.1 Claude Code 설치

Claude Code는 npm(Node Package Manager)을 통해 설치합니다. 설치 전에 반드시 **Node.js 18 이상**이 시스템에 설치되어 있어야 합니다.

#### 사전 요구사항

| 항목 | 최소 버전 | 권장 버전 |
|------|-----------|-----------|
| Node.js | 18.0.0 | 20 LTS 이상 |
| npm | 9.0.0 | 10 이상 |
| 운영체제 | macOS, Linux, Windows (WSL) | macOS 또는 Linux |

> **Note:** Windows 사용자는 WSL(Windows Subsystem for Linux)을 통해 사용하는 것을 권장합니다. 네이티브 Windows 환경에서는 일부 기능이 제한될 수 있습니다.

Node.js가 설치되어 있는지 먼저 확인합니다.

```bash
node --version
npm --version
```

Node.js가 설치되어 있지 않다면 [공식 웹사이트](https://nodejs.org)에서 LTS 버전을 다운로드하거나, 아래 명령어로 설치할 수 있습니다.

```bash
# macOS (Homebrew 사용)
brew install node

# Ubuntu/Debian
sudo apt update && sudo apt install -y nodejs npm
```

#### 예제 8-1: npm으로 Claude Code 설치

Claude Code를 글로벌 패키지로 설치하고, 설치가 정상적으로 완료되었는지 확인합니다.

**설치 명령:**

```bash
# Claude Code 글로벌 설치
npm install -g @anthropic-ai/claude-code
```

**실행 결과:**

```
added 1 package in 12s

1 package is looking for funding
  run `npm fund` for details
```

**설치 확인:**

```bash
# 설치 경로 확인
which claude
```

**실행 결과:**

```
/usr/local/bin/claude
```

> **Tip:** 설치 중 권한 오류가 발생하면 `sudo npm install -g @anthropic-ai/claude-code`를 사용하거나, npm의 기본 디렉토리 권한을 변경하세요. 가능하면 `nvm`(Node Version Manager)을 사용해 Node.js를 관리하면 권한 문제를 피할 수 있습니다.

---

### 8.2 버전 확인 및 기본 명령어

설치가 완료되면 버전을 확인하고 도움말을 통해 사용 가능한 명령어를 살펴봅니다.

#### 예제 8-2: 버전 확인 및 도움말

**버전 확인:**

```bash
claude --version
```

**실행 결과:**

```
claude v1.0.16
```

**도움말 확인:**

```bash
claude --help
```

**실행 결과:**

```
Usage: claude [options] [prompt]

AI assistant for the command line

Options:
  -V, --version          output the version number
  -p, --print            print response without interactive mode
  --model <model>        specify the AI model to use
  --output-format <fmt>  output format (text, json, stream-json)
  -v, --verbose          enable verbose output
  --max-turns <n>        maximum conversation turns
  -h, --help             display help for command

Commands:
  config                 manage configuration
  mcp                    manage MCP servers
```

> **Note:** 버전 번호와 사용 가능한 옵션은 업데이트에 따라 달라질 수 있습니다. 항상 최신 버전 사용을 권장합니다.

---

### 8.3 첫 실행과 인증

Claude Code를 처음 실행하면 인증 과정을 거쳐야 합니다. Anthropic 계정을 통해 인증하며, 브라우저가 자동으로 열려 로그인을 진행합니다.

#### 예제 8-3: 첫 인증 과정

터미널에서 `claude`를 입력하여 첫 실행을 시작합니다.

**명령:**

```bash
claude
```

**실행 결과 (인증 전):**

```
Welcome to Claude Code v1.0.16

To get started, you need to authenticate with your Anthropic account.

? How would you like to authenticate?
❯ Login with Anthropic account (opens browser)
  Use API key
  Cancel

Opening browser for authentication...
Please log in and authorize Claude Code.

✔ Authentication successful!
Welcome, user@example.com

╭──────────────────────────────────────╮
│ Claude Code                          │
│                                      │
│ /help for available commands         │
│ /exit to leave                       │
╰──────────────────────────────────────╯

>
```

인증 과정은 다음과 같이 진행됩니다.

1. `claude` 명령 실행
2. 인증 방법 선택 (브라우저 로그인 또는 API 키 직접 입력)
3. 브라우저 로그인을 선택하면 기본 브라우저가 열림
4. Anthropic 계정으로 로그인 및 권한 승인
5. 터미널로 돌아오면 인증 완료 메시지 표시
6. 대화형 세션이 시작됨

> **Tip:** 인증 정보는 로컬에 안전하게 저장되므로 매번 다시 인증할 필요가 없습니다. 인증 정보를 초기화하려면 `claude config` 명령을 사용하세요.

---

### 8.4 기본 사용법

인증이 완료되면 Claude Code와 대화를 시작할 수 있습니다. 질문하기, 파일 생성, 코드 실행 등 다양한 작업이 가능합니다.

#### 대화형 모드

`claude`를 실행하면 대화형 모드로 진입합니다. 자연어로 질문하거나 작업을 요청할 수 있습니다.

```bash
# 대화형 모드 시작
claude
```

#### 단일 명령 모드

간단한 질문은 `-p` 플래그를 사용해 바로 결과를 받을 수 있습니다.

```bash
# 단일 질문 모드
claude -p "Python으로 피보나치 수열 함수를 작성해줘"
```

#### 주요 대화 명령어

| 명령어 | 설명 |
|--------|------|
| `/help` | 사용 가능한 명령어 목록 표시 |
| `/exit` | 세션 종료 |
| `/clear` | 대화 기록 초기화 |
| `/model` | 사용 중인 모델 확인 또는 변경 |

---

### 8.5 설정 파일 이해

Claude Code는 설정 정보를 여러 위치에 저장합니다. 설정 파일의 위치와 역할을 이해하면 작업 환경을 더 효율적으로 관리할 수 있습니다.

#### 설정 파일 위치

| 파일/디렉토리 | 위치 | 용도 |
|---------------|------|------|
| 전역 설정 | `~/.claude/` | 인증 정보, 전역 환경설정 |
| 프로젝트 설정 | `.claude/` (프로젝트 루트) | 프로젝트별 설정 |
| CLAUDE.md | 프로젝트 루트 | 프로젝트 컨텍스트 및 지침 |

#### 주요 설정 항목

```bash
# 현재 설정 확인
claude config

# 모델 변경
claude config set model claude-opus-4-5-20251101

# 설정 목록 보기
claude config list
```

> **Tip:** 프로젝트 루트에 `CLAUDE.md` 파일을 작성하면 Claude Code가 프로젝트의 구조, 코딩 규칙, 기술 스택 등을 자동으로 파악합니다. 프로젝트에 맞는 더 정확한 응답을 받을 수 있으므로 적극 활용하세요.

---

### 8.6 기타 AI CLI 도구 소개

Claude Code 외에도 다양한 AI CLI 도구가 있습니다. 각 도구의 특징을 간략히 살펴보겠습니다.

| 도구 | 특징 | 설치 명령 |
|------|------|-----------|
| GitHub Copilot CLI | GitHub 통합, 명령어 추천 | `gh extension install github/gh-copilot` |
| Aider | Git 연동, 다중 파일 편집 | `pip install aider-chat` |
| Cursor | AI 내장 코드 에디터 | 공식 사이트에서 다운로드 |
| Continue | VS Code/JetBrains 확장 | 확장 마켓에서 설치 |

각 도구는 고유한 강점이 있으므로, 프로젝트 성격과 개인 선호에 맞게 선택하면 됩니다. 이 책에서는 Claude Code를 중심으로 바이브 코딩을 배워 나가겠습니다.

---

### 8.7 API 키 안전하게 관리하기

AI 도구를 사용할 때 가장 중요한 것 중 하나가 **API 키 보안**입니다. API 키가 유출되면 무단 사용으로 인한 비용 발생과 보안 위협이 생길 수 있습니다.

> **Warning:** API 키는 절대로 소스 코드에 직접 작성하거나, Git 저장소에 커밋하지 마세요. 키가 유출되면 즉시 해당 키를 폐기하고 새로운 키를 발급받아야 합니다.

#### 안전한 관리 원칙

1. **환경변수 사용**: API 키는 환경변수로 설정하여 코드와 분리
2. **.env 파일 활용**: 로컬 개발 시 `.env` 파일에 저장하고 `.gitignore`에 반드시 추가
3. **절대 커밋 금지**: Git 커밋 전 API 키가 포함되지 않았는지 확인
4. **키 회전**: 정기적으로 API 키를 교체하여 보안 강화

#### 예제 8-4: 환경변수로 API 키 설정

터미널에서 환경변수를 설정하고, Python 스크립트에서 안전하게 읽어오는 방법입니다.

**환경변수 설정 (터미널):**

```bash
# examples/bash/chapter02/set_api_key.sh

# 셸 프로필에 환경변수 추가 (bash 사용 시)
echo 'export ANTHROPIC_API_KEY="sk-ant-xxxxx-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# 현재 세션에서만 설정하려면
export ANTHROPIC_API_KEY="sk-ant-xxxxx-your-key-here"
```

> **Warning:** 위 예제의 `sk-ant-xxxxx-your-key-here`는 자리 표시자입니다. 절대로 실제 API 키를 공유하거나 문서에 기록하지 마세요.

**Python에서 안전하게 API 키 읽기:**

```python
# examples/python/chapter02/safe_api_key.py
import os
import sys

def get_api_key():
    """환경변수에서 API 키를 안전하게 가져옵니다."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("오류: ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("다음 명령어로 설정하세요:")
        print('  export ANTHROPIC_API_KEY="sk-ant-xxxxx-your-key-here"')
        sys.exit(1)

    # 키의 앞 10자만 표시하여 확인 (보안을 위해 전체를 출력하지 않음)
    masked_key = api_key[:10] + "..." + api_key[-4:]
    print(f"API 키가 확인되었습니다: {masked_key}")
    return api_key

if __name__ == "__main__":
    key = get_api_key()
    print("API 키를 사용할 준비가 되었습니다!")
```

**실행 결과:**

```
API 키가 확인되었습니다: sk-ant-xxx...here
API 키를 사용할 준비가 되었습니다!
```

#### .env 파일과 .gitignore 설정

프로젝트 루트에 `.env` 파일을 만들고, 반드시 `.gitignore`에 추가합니다.

```bash
# .env 파일 생성
echo 'ANTHROPIC_API_KEY=sk-ant-xxxxx-your-key-here' > .env

# .gitignore에 추가 (이미 없다면)
echo '.env' >> .gitignore
```

> **Tip:** `python-dotenv` 패키지를 사용하면 Python에서 `.env` 파일의 변수를 자동으로 불러올 수 있습니다. `pip install python-dotenv` 후 코드에서 `load_dotenv()`를 호출하세요.

---

### 8.8 첫 연결 테스트

모든 설치와 설정이 끝났다면, Claude Code가 정상적으로 동작하는지 테스트해 봅시다.

#### 예제 8-5: 첫 연결 테스트 대화

Claude Code를 시작하고 간단한 요청을 보내 정상 동작을 확인합니다.

**명령:**

```bash
claude
```

**대화 진행:**

```
╭──────────────────────────────────────╮
│ Claude Code                          │
│                                      │
│ /help for available commands         │
│ /exit to leave                       │
╰──────────────────────────────────────╯

> 안녕하세요, 간단한 Python 스크립트를 만들어주세요

네, 간단한 Python 스크립트를 만들어드리겠습니다!

hello_vibe.py 파일을 생성하겠습니다:

  import datetime

  def greet():
      now = datetime.datetime.now()
      hour = now.hour

      if hour < 12:
          greeting = "좋은 아침이에요!"
      elif hour < 18:
          greeting = "좋은 오후에요!"
      else:
          greeting = "좋은 저녁이에요!"

      print(f"안녕하세요! {greeting}")
      print("바이브 코딩의 세계에 오신 것을 환영합니다!")
      print(f"현재 시각: {now.strftime('%Y-%m-%d %H:%M')}")

  if __name__ == "__main__":
      greet()

파일을 생성했습니다. 실행해 볼까요?

> 네, 실행해주세요

$ python hello_vibe.py

안녕하세요! 좋은 오후에요!
바이브 코딩의 세계에 오신 것을 환영합니다!
현재 시각: 2026-01-15 14:30

스크립트가 정상적으로 실행되었습니다! 현재 시간대에 맞는
인사말을 출력하는 간단한 프로그램입니다.
```

축하합니다! Claude Code가 정상적으로 설치되고 동작하는 것을 확인했습니다. 이제 바이브 코딩을 본격적으로 시작할 준비가 되었습니다.

> **Tip:** Claude Code는 파일을 생성하거나 수정하기 전에 항상 사용자의 승인을 요청합니다. 안심하고 다양한 요청을 시도해 보세요.

---

### 정리

이 장에서 배운 내용을 정리하겠습니다.

- **Claude Code 설치**: Node.js 18 이상이 필요하며, `npm install -g @anthropic-ai/claude-code` 명령으로 설치합니다.
- **인증**: 첫 실행 시 브라우저를 통해 Anthropic 계정으로 인증하며, 인증 정보는 로컬에 안전하게 저장됩니다.
- **기본 사용법**: 대화형 모드와 단일 명령 모드(`-p` 플래그)를 사용할 수 있습니다.
- **설정 파일**: 전역 설정은 `~/.claude/`에, 프로젝트 설정은 프로젝트 루트의 `.claude/`와 `CLAUDE.md`에 저장됩니다.
- **다른 도구들**: GitHub Copilot CLI, Aider 등 다양한 AI CLI 도구가 있으며, 필요에 따라 선택할 수 있습니다.
- **API 키 보안**: 환경변수 또는 `.env` 파일로 관리하고, 절대로 소스 코드에 직접 포함하거나 Git에 커밋하지 않습니다.

---

### 다음 장 예고

다음 장에서는 **효과적인 프롬프트 작성법**을 다룹니다. AI에게 원하는 결과를 정확히 얻기 위한 프롬프트 구조, 맥락 제공 방법, 그리고 반복적으로 개선해 나가는 기법을 배워보겠습니다. 좋은 프롬프트는 바이브 코딩의 핵심 기술입니다.
