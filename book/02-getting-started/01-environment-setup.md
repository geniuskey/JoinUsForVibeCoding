## 제6장: 개발 환경 설정

바이브 코딩을 시작하기 전에, 우리의 작업 공간을 먼저 준비해야 합니다. 목수가 작업대를 정리하고 도구를 준비하듯이, 프로그래머도 개발 환경을 갖추는 것이 첫 번째 단계입니다. 이 장에서는 여러분의 컴퓨터에 바이브 코딩에 필요한 모든 도구를 설치하고 설정하는 과정을 안내합니다.

### 학습 목표

이 장을 마치면 다음을 할 수 있게 됩니다:

- 자신의 운영체제에 맞는 개발 환경을 구성할 수 있다
- VS Code 텍스트 에디터를 설치하고 기본 설정을 할 수 있다
- 터미널을 열고 기본 명령어를 실행할 수 있다
- Python과 Node.js를 설치하고 정상 동작을 확인할 수 있다
- pip와 npm 패키지 매니저를 사용하여 패키지를 설치할 수 있다
- Python 가상환경을 생성하고 활성화할 수 있다
- 전체 개발 환경이 올바르게 설정되었는지 검증할 수 있다

---

### 6.1 운영체제별 준비

바이브 코딩은 어떤 운영체제에서든 가능합니다. 하지만 운영체제마다 초기 준비 과정이 조금 다릅니다. 자신의 환경에 맞는 섹션을 확인하세요.

#### Windows 사용자

Windows에서 바이브 코딩을 하려면 **WSL(Windows Subsystem for Linux)**을 설치하는 것을 강력히 권장합니다. WSL을 사용하면 Windows 안에서 Linux 환경을 그대로 사용할 수 있어, 대부분의 개발 도구와 명령어가 매끄럽게 동작합니다.

WSL 설치 방법은 간단합니다. PowerShell을 관리자 권한으로 열고 다음 명령어를 실행하세요:

```bash
wsl --install
```

설치가 완료되면 컴퓨터를 재시작하고, Ubuntu 사용자 이름과 비밀번호를 설정하면 됩니다.

> **Tip:** WSL을 설치하면 이후의 모든 과정이 macOS나 Linux 사용자와 동일해집니다. 이 책의 예제도 WSL 환경 기준으로 작성되었습니다.

#### macOS 사용자

macOS는 기본적으로 Unix 기반이므로 별도의 준비가 거의 필요 없습니다. 다만, 개발 도구 모음인 **Xcode Command Line Tools**를 설치하면 더 편리합니다:

```bash
xcode-select --install
```

이후 **Homebrew** 패키지 매니저를 설치하면 각종 도구 설치가 훨씬 쉬워집니다:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Linux 사용자

Linux는 이미 개발에 최적화된 환경입니다. 대부분의 배포판에 터미널과 기본 개발 도구가 포함되어 있습니다. 패키지 매니저를 통해 필요한 도구를 설치하면 됩니다.

Ubuntu/Debian 계열이라면 먼저 패키지 목록을 업데이트하세요:

```bash
sudo apt update && sudo apt upgrade -y
```

> **Note:** 이 책의 예제는 Ubuntu 22.04 LTS 기준으로 작성되었지만, 다른 배포판에서도 대부분 동일하게 동작합니다.

---

### 6.2 텍스트 에디터 설치

코드를 작성하려면 텍스트 에디터가 필요합니다. 여러 선택지가 있지만, 이 책에서는 **Visual Studio Code(VS Code)**를 추천합니다.

VS Code를 추천하는 이유는 다음과 같습니다:

- **무료**이며 오픈 소스입니다
- **초보자 친화적**인 직관적 인터페이스를 제공합니다
- **확장 기능**이 풍부하여 필요한 도구를 쉽게 추가할 수 있습니다
- **통합 터미널**이 내장되어 있어 에디터 안에서 바로 명령어를 실행할 수 있습니다
- **AI 코딩 도구**와의 연동이 뛰어납니다

VS Code 설치 방법:

1. [https://code.visualstudio.com](https://code.visualstudio.com)에 접속합니다
2. 자신의 운영체제에 맞는 버전을 다운로드합니다
3. 설치 파일을 실행하고 안내에 따라 설치합니다

설치 후 추천하는 확장 기능:

| 확장 기능 | 설명 |
|-----------|------|
| Python | Python 언어 지원 및 디버깅 |
| Prettier | 코드 자동 정리 |
| Korean Language Pack | 한국어 인터페이스 |
| GitHub Copilot | AI 코드 어시스턴트 |

> **Tip:** VS Code에서 `Ctrl+`` (백틱) 키를 누르면 통합 터미널이 열립니다. 에디터와 터미널을 한 화면에서 사용할 수 있어 매우 편리합니다.

---

### 6.3 터미널 설정

터미널은 바이브 코딩의 핵심 도구입니다. 텍스트 명령어로 컴퓨터와 대화하는 창이라고 생각하면 됩니다. 각 운영체제에서 터미널을 여는 방법을 알아봅시다.

**Windows (WSL):**
- 시작 메뉴에서 "Ubuntu" 또는 "WSL"을 검색하여 실행합니다
- 또는 Windows Terminal 앱을 설치하면 더 나은 경험을 할 수 있습니다

**macOS:**
- `Cmd + Space`로 Spotlight를 열고 "Terminal"을 검색합니다
- 또는 `응용 프로그램 > 유틸리티 > 터미널`에서 찾을 수 있습니다

**Linux:**
- `Ctrl + Alt + T` 단축키로 터미널을 엽니다
- 또는 응용 프로그램 메뉴에서 "터미널"을 검색합니다

터미널이 열리면, 프롬프트가 나타납니다. 이것이 여러분의 명령을 기다리는 상태입니다. 간단한 명령어를 입력해서 터미널이 잘 동작하는지 확인해 보세요:

```bash
echo "안녕하세요, 바이브 코딩!"
```

화면에 `안녕하세요, 바이브 코딩!`이라는 메시지가 출력되면 터미널이 정상적으로 동작하는 것입니다.

---

### 6.4 Python 설치 및 확인

Python은 바이브 코딩에서 가장 많이 사용하는 프로그래밍 언어 중 하나입니다. 이 책에서는 **Python 3.10 이상** 버전을 사용합니다.

#### 설치 방법

**macOS (Homebrew 사용):**
```bash
brew install python@3.12
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv
```

**Windows (WSL):**
WSL의 Ubuntu에서 위의 Ubuntu 명령어를 동일하게 사용하세요.

#### 예제 6-1: Python 버전 확인

설치가 완료되면, Python이 올바르게 설치되었는지 확인합니다.

```bash
# examples/bash/chapter02/check_python.sh
# Python 버전 확인
python3 --version
```

**실행:**
```bash
$ python3 --version
```

**결과:**
```
Python 3.12.3
```

> **Note:** 버전 번호는 설치 시점에 따라 다를 수 있습니다. `Python 3.10` 이상이면 이 책의 모든 예제를 실행할 수 있습니다.

Python이 제대로 동작하는지 한 줄짜리 코드로도 확인해 볼 수 있습니다:

```bash
python3 -c "print('Python이 정상적으로 설치되었습니다!')"
```

**결과:**
```
Python이 정상적으로 설치되었습니다!
```

---

### 6.5 Node.js 설치 및 확인

Node.js는 JavaScript를 터미널에서 실행할 수 있게 해주는 도구입니다. 웹 개발이나 다양한 CLI 도구를 사용하려면 필요합니다. 이 책에서는 **Node.js 18 이상** 버전을 사용합니다.

#### 설치 방법

**macOS (Homebrew 사용):**
```bash
brew install node
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

#### 예제 6-2: Node.js 버전 확인

Node.js와 함께 설치되는 npm(패키지 매니저)도 함께 확인합니다.

```bash
# examples/bash/chapter02/check_node.sh
# Node.js 버전 확인
node --version

# npm 버전 확인
npm --version
```

**실행:**
```bash
$ node --version
$ npm --version
```

**결과:**
```
v20.11.1
10.2.4
```

> **Note:** Node.js를 설치하면 npm도 자동으로 설치됩니다. 두 명령어 모두 버전 번호가 출력되면 정상입니다.

Node.js가 제대로 동작하는지 간단히 테스트해 볼 수 있습니다:

```bash
node -e "console.log('Node.js가 정상적으로 설치되었습니다!')"
```

**결과:**
```
Node.js가 정상적으로 설치되었습니다!
```

---

### 6.6 pip와 npm 기초

프로그래밍에서 **패키지 매니저**는 다른 사람이 만든 도구나 라이브러리를 쉽게 설치하고 관리할 수 있게 해주는 프로그램입니다. 마치 스마트폰의 앱스토어처럼, 필요한 소프트웨어를 검색하고 설치할 수 있습니다.

- **pip**: Python의 패키지 매니저
- **npm**: Node.js의 패키지 매니저

#### 예제 6-3: pip로 패키지 설치

Python에서 가장 많이 사용하는 HTTP 라이브러리인 `requests`를 설치해 봅시다.

```bash
# examples/bash/chapter02/pip_install.sh
# pip로 requests 패키지 설치
pip install requests
```

**실행:**
```bash
$ pip install requests
```

**결과:**
```
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting charset-normalizer<4,>=2
Collecting idna<4,>=2.5
Collecting urllib3<3,>=1.21.1
Collecting certifi>=2017.4.17
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests
Successfully installed certifi-2024.2.2 charset-normalizer-3.3.2 idna-3.6 requests-2.31.0 urllib3-2.2.1
```

설치가 완료되면, Python에서 해당 패키지를 사용할 수 있는지 확인합니다:

```python
# examples/python/chapter02/verify_requests.py
# requests 패키지가 정상적으로 설치되었는지 확인
import requests

print(f"requests 버전: {requests.__version__}")
print("패키지가 정상적으로 설치되었습니다!")
```

**실행:**
```bash
$ python3 examples/python/chapter02/verify_requests.py
```

**결과:**
```
requests 버전: 2.31.0
패키지가 정상적으로 설치되었습니다!
```

#### 예제 6-4: npm으로 패키지 설치

npm을 사용하여 터미널에서 재미있는 텍스트를 출력하는 `cowsay` 패키지를 전역으로 설치해 봅시다.

```bash
# examples/bash/chapter02/npm_install.sh
# npm으로 cowsay 패키지를 전역(-g)으로 설치
npm install -g cowsay
```

**실행:**
```bash
$ npm install -g cowsay
```

**결과:**
```
added 41 packages in 3s
```

설치 후 바로 사용해 볼 수 있습니다:

```bash
$ cowsay "바이브 코딩 시작!"
```

**결과:**
```
 ____________________
< 바이브 코딩 시작! >
 --------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

> **Tip:** `npm install -g`의 `-g` 옵션은 "global(전역)"을 의미합니다. 전역으로 설치하면 어디서든 해당 명령어를 사용할 수 있습니다. 반면 `-g` 없이 설치하면 현재 프로젝트 폴더에만 설치됩니다.

자주 사용하는 pip 및 npm 명령어를 정리하면 다음과 같습니다:

| 작업 | pip (Python) | npm (Node.js) |
|------|-------------|---------------|
| 패키지 설치 | `pip install 패키지명` | `npm install 패키지명` |
| 전역 설치 | `pip install 패키지명` | `npm install -g 패키지명` |
| 패키지 삭제 | `pip uninstall 패키지명` | `npm uninstall 패키지명` |
| 설치 목록 확인 | `pip list` | `npm list` |
| 패키지 검색 | `pip search 패키지명` | `npm search 패키지명` |

---

### 6.7 가상환경 이해

Python 프로젝트를 진행하다 보면, 프로젝트마다 서로 다른 버전의 패키지가 필요한 경우가 있습니다. 예를 들어, 프로젝트 A는 `requests 2.28`을, 프로젝트 B는 `requests 2.31`을 사용해야 할 수 있습니다.

**가상환경(Virtual Environment)**은 이런 문제를 해결합니다. 각 프로젝트마다 독립된 Python 환경을 만들어, 패키지들이 서로 충돌하지 않게 합니다. 마치 각 프로젝트에 전용 방을 만들어주는 것과 같습니다.

#### 예제 6-5: 가상환경 생성

Python에 내장된 `venv` 모듈을 사용하여 가상환경을 생성하고 활성화합니다.

```bash
# examples/bash/chapter02/create_venv.sh
# 가상환경 생성
python3 -m venv myenv

# 가상환경 활성화 (Linux/macOS)
source myenv/bin/activate

# 가상환경이 활성화되었는지 확인
which python

# 가상환경 내에서 패키지 설치
pip install requests

# 설치된 패키지 확인
pip list

# 가상환경 비활성화
deactivate
```

**실행:**
```bash
$ python3 -m venv myenv
$ source myenv/bin/activate
(myenv) $ which python
```

**결과:**
```
/home/user/myenv/bin/python
```

가상환경이 활성화되면 터미널 프롬프트 앞에 `(myenv)`라는 표시가 나타납니다. 이 상태에서 설치하는 모든 패키지는 이 가상환경에만 저장됩니다.

```bash
(myenv) $ pip list
```

**결과:**
```
Package    Version
---------- -------
pip        24.0
requests   2.31.0
```

비활성화하려면 `deactivate` 명령어를 입력합니다:

```bash
(myenv) $ deactivate
$
```

> **Warning:** 가상환경을 활성화하지 않고 패키지를 설치하면 시스템 전체 Python에 영향을 줄 수 있습니다. 프로젝트 작업 시에는 반드시 가상환경을 활성화한 후에 작업하세요.

가상환경의 기본 사용 흐름을 정리하면 다음과 같습니다:

1. `python3 -m venv 환경이름` — 가상환경 생성
2. `source 환경이름/bin/activate` — 가상환경 활성화
3. `pip install 패키지명` — 필요한 패키지 설치
4. 코딩 작업 수행
5. `deactivate` — 작업 완료 후 가상환경 비활성화

---

### 6.8 환경 변수와 PATH

개발을 하다 보면 **환경 변수**라는 개념을 자주 만나게 됩니다. 환경 변수는 운영체제가 프로그램에게 전달하는 설정 값으로, 비밀번호나 경로 같은 정보를 저장하는 데 사용됩니다.

그중에서도 **PATH**는 가장 중요한 환경 변수입니다. PATH는 운영체제가 명령어를 찾는 디렉토리 목록입니다. 터미널에서 `python3`이라고 입력하면, 운영체제는 PATH에 등록된 디렉토리들을 순서대로 탐색하여 `python3` 프로그램을 찾습니다.

#### 예제 6-6: 환경 변수 설정

터미널에서 환경 변수를 설정하고, Python에서 읽어보는 방법을 알아봅시다.

```bash
# examples/bash/chapter02/env_variable.sh
# 환경 변수 설정
export MY_PROJECT="바이브코딩프로젝트"

# 환경 변수 확인
echo $MY_PROJECT
```

**실행:**
```bash
$ export MY_PROJECT="바이브코딩프로젝트"
$ echo $MY_PROJECT
```

**결과:**
```
바이브코딩프로젝트
```

Python에서도 환경 변수를 읽을 수 있습니다:

```python
# examples/python/chapter02/read_env.py
# Python에서 환경 변수 읽기
import os

project_name = os.environ.get("MY_PROJECT", "설정되지 않음")
home_dir = os.environ.get("HOME", "알 수 없음")

print(f"프로젝트 이름: {project_name}")
print(f"홈 디렉토리: {home_dir}")
```

**실행:**
```bash
$ export MY_PROJECT="바이브코딩프로젝트"
$ python3 examples/python/chapter02/read_env.py
```

**결과:**
```
프로젝트 이름: 바이브코딩프로젝트
홈 디렉토리: /home/user
```

> **Tip:** `os.environ.get()` 함수의 두 번째 인자는 환경 변수가 설정되지 않았을 때 사용할 기본값입니다. 이렇게 하면 환경 변수가 없어도 프로그램이 오류 없이 동작합니다.

#### 예제 6-7: PATH 확인

현재 시스템의 PATH 설정과 특정 프로그램의 위치를 확인해 봅시다.

```bash
# examples/bash/chapter02/check_path.sh
# PATH 환경 변수 전체 출력
echo $PATH

# Python3의 실행 파일 위치 확인
which python3

# Node.js의 실행 파일 위치 확인
which node
```

**실행:**
```bash
$ echo $PATH
```

**결과:**
```
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

```bash
$ which python3
```

**결과:**
```
/usr/bin/python3
```

```bash
$ which node
```

**결과:**
```
/usr/bin/node
```

> **Note:** `which` 명령어는 해당 프로그램이 PATH 상의 어느 디렉토리에 위치하는지 알려줍니다. 명령어가 찾아지지 않으면 설치가 안 되었거나 PATH에 등록되지 않은 것입니다.

---

### 6.9 환경 확인 종합 스크립트

지금까지 설치한 모든 도구가 정상적으로 설치되었는지 한 번에 확인할 수 있는 스크립트를 만들어 봅시다.

#### 예제 6-8: 전체 환경 확인 스크립트

이 스크립트는 Python 버전, Node.js 버전, 설치된 pip 패키지 등을 종합적으로 점검하고 결과를 보기 좋게 출력합니다.

```python
# examples/python/chapter02/env_check.py
# 개발 환경 종합 확인 스크립트

import sys
import subprocess
import shutil

def check_command(command):
    """명령어가 시스템에 설치되어 있는지 확인합니다."""
    return shutil.which(command) is not None

def get_version(command, args=["--version"]):
    """명령어의 버전 정보를 가져옵니다."""
    try:
        result = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() or result.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "확인 불가"

def get_pip_packages():
    """설치된 pip 패키지 목록을 가져옵니다."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=columns"],
            capture_output=True,
            text=True,
            timeout=30
        )
        lines = result.stdout.strip().split("\n")
        # 헤더 2줄 제외
        return len(lines) - 2 if len(lines) > 2 else 0
    except Exception:
        return 0

def main():
    print("=" * 50)
    print("   바이브 코딩 - 개발 환경 확인 리포트")
    print("=" * 50)
    print()

    # 1. Python 확인
    print("[1] Python 확인")
    python_version = f"Python {sys.version.split()[0]}"
    major, minor = sys.version_info.major, sys.version_info.minor
    if major >= 3 and minor >= 10:
        status = "OK"
    else:
        status = "업그레이드 필요 (3.10 이상 권장)"
    print(f"    버전: {python_version}")
    print(f"    경로: {sys.executable}")
    print(f"    상태: {status}")
    print()

    # 2. Node.js 확인
    print("[2] Node.js 확인")
    if check_command("node"):
        node_version = get_version("node")
        print(f"    버전: {node_version}")
        print(f"    경로: {shutil.which('node')}")
        print(f"    상태: OK")
    else:
        print("    상태: 설치되지 않음")
    print()

    # 3. npm 확인
    print("[3] npm 확인")
    if check_command("npm"):
        npm_version = get_version("npm")
        print(f"    버전: npm {npm_version}")
        print(f"    상태: OK")
    else:
        print("    상태: 설치되지 않음")
    print()

    # 4. pip 확인
    print("[4] pip 확인")
    pip_version = get_version(sys.executable, ["-m", "pip", "--version"])
    package_count = get_pip_packages()
    print(f"    버전: {pip_version}")
    print(f"    설치된 패키지 수: {package_count}개")
    print()

    # 5. Git 확인
    print("[5] Git 확인")
    if check_command("git"):
        git_version = get_version("git")
        print(f"    버전: {git_version}")
        print(f"    상태: OK")
    else:
        print("    상태: 설치되지 않음")
    print()

    # 6. VS Code 확인
    print("[6] VS Code 확인")
    if check_command("code"):
        code_version = get_version("code")
        print(f"    버전: {code_version}")
        print(f"    상태: OK")
    else:
        print("    상태: 설치되지 않음 (선택 사항)")
    print()

    # 종합 결과
    print("=" * 50)
    essential = ["python3", "node", "npm"]
    installed = sum(1 for cmd in essential if check_command(cmd))
    total = len(essential)

    if installed == total:
        print("  결과: 모든 필수 도구가 설치되어 있습니다!")
        print("  바이브 코딩을 시작할 준비가 완료되었습니다!")
    else:
        print(f"  결과: {total}개 중 {installed}개 설치됨")
        print("  누락된 도구를 설치해 주세요.")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

**실행:**
```bash
$ python3 examples/python/chapter02/env_check.py
```

**결과:**
```
==================================================
   바이브 코딩 - 개발 환경 확인 리포트
==================================================

[1] Python 확인
    버전: Python 3.12.3
    경로: /usr/bin/python3
    상태: OK

[2] Node.js 확인
    버전: v20.11.1
    경로: /usr/bin/node
    상태: OK

[3] npm 확인
    버전: npm 10.2.4
    상태: OK

[4] pip 확인
    버전: pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
    설치된 패키지 수: 12개

[5] Git 확인
    버전: git version 2.43.0
    상태: OK

[6] VS Code 확인
    상태: 설치되지 않음 (선택 사항)

==================================================
  결과: 모든 필수 도구가 설치되어 있습니다!
  바이브 코딩을 시작할 준비가 완료되었습니다!
==================================================
```

> **Tip:** 이 스크립트를 저장해두고 새 컴퓨터에서 개발 환경을 설정할 때마다 실행하면, 어떤 도구가 빠졌는지 빠르게 확인할 수 있습니다.

---

### 정리

이 장에서 우리는 바이브 코딩에 필요한 개발 환경을 처음부터 설정하는 방법을 배웠습니다. 핵심 내용을 정리하면 다음과 같습니다:

- **운영체제 준비**: Windows는 WSL, macOS는 Xcode 도구, Linux는 기본 상태로 시작할 수 있습니다
- **텍스트 에디터**: VS Code는 초보자에게 가장 적합한 에디터이며, 통합 터미널과 확장 기능을 지원합니다
- **터미널**: 각 운영체제에서 터미널을 열고 명령어를 실행하는 방법을 배웠습니다
- **Python과 Node.js**: 두 가지 핵심 프로그래밍 도구를 설치하고 버전을 확인했습니다
- **패키지 매니저**: pip와 npm을 사용하여 외부 패키지를 설치하는 방법을 익혔습니다
- **가상환경**: Python 가상환경으로 프로젝트별 독립 환경을 구성하는 방법을 배웠습니다
- **환경 변수와 PATH**: 시스템 설정을 이해하고 확인하는 방법을 알게 되었습니다
- **환경 확인 스크립트**: 모든 설정이 올바른지 자동으로 점검하는 스크립트를 만들었습니다

> **Note:** 개발 환경 설정은 처음에는 복잡하게 느껴질 수 있지만, 한 번 제대로 설정해두면 이후의 모든 작업이 훨씬 수월해집니다. 이 장의 환경 확인 스크립트를 실행하여 모든 도구가 정상적으로 설치되었는지 반드시 확인하세요.

---

### 다음 장 예고

다음 장에서는 드디어 **첫 번째 AI 어시스턴트 사용하기**를 다룹니다. 이 장에서 설정한 개발 환경 위에서, AI와 대화하며 코드를 작성하는 바이브 코딩의 핵심 경험을 시작하게 됩니다. 프롬프트를 작성하고, AI가 생성한 코드를 실행하고, 결과를 확인하는 전체 흐름을 직접 체험해 봅시다.
