## Chapter 7: CLI 기초

커맨드 라인 인터페이스(CLI)는 바이브 코딩의 핵심 도구입니다. AI 어시스턴트와 대화하듯 컴퓨터를 조작하는 첫 번째 단계, CLI의 세계로 들어가 봅시다.

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 터미널과 쉘의 개념을 이해한다
- 기본 탐색 명령어로 파일 시스템을 자유롭게 이동한다
- 파일과 디렉토리를 생성, 복사, 이동, 삭제한다
- 파일 내용을 확인하고 텍스트를 검색한다
- 파이프와 리다이렉션으로 명령어를 조합한다
- CLI만으로 프로젝트 구조를 만들 수 있다

---

### 7.1 터미널이란?

**터미널(Terminal)**은 텍스트 명령어로 컴퓨터를 조작하는 프로그램입니다. 마우스로 폴더를 클릭하는 대신, 글자를 입력해서 같은 작업을 수행합니다.

역사적으로 터미널은 컴퓨터와 소통하는 유일한 방법이었습니다. 1960~70년대에는 모니터와 키보드로 이루어진 물리적 장치가 터미널이었고, 사용자는 오직 텍스트 명령어만으로 컴퓨터를 다뤘습니다. 오늘날 우리가 사용하는 터미널은 그 물리적 장치를 소프트웨어로 구현한 **터미널 에뮬레이터**입니다.

터미널을 열면 그 안에서 동작하는 프로그램이 바로 **쉘(Shell)**입니다. 쉘은 사용자가 입력한 명령어를 해석하고 운영체제에 전달하는 역할을 합니다. 그리고 우리가 쉘에 입력하는 텍스트 기반 인터페이스를 **커맨드 라인(Command Line)**이라고 부릅니다.

정리하면 다음과 같습니다:

| 용어 | 설명 |
|------|------|
| 터미널 | 텍스트 입출력을 위한 프로그램(창) |
| 쉘 | 명령어를 해석하고 실행하는 프로그램 |
| 커맨드 라인 | 명령어를 입력하는 텍스트 인터페이스 |

> **Tip:** 바이브 코딩에서 AI 어시스턴트(예: Claude Code)는 터미널 위에서 동작합니다. CLI에 익숙해지면 AI와의 협업이 훨씬 자연스러워집니다.

---

### 7.2 쉘의 종류

쉘에는 여러 종류가 있습니다. 가장 많이 사용되는 쉘을 살펴봅시다.

| 쉘 | 설명 | 주요 환경 |
|----|------|-----------|
| **bash** | Bourne Again Shell. 가장 널리 쓰이는 쉘 | Linux 기본 |
| **zsh** | Z Shell. bash의 확장판으로 강력한 자동 완성 지원 | macOS 기본 |
| **PowerShell** | 마이크로소프트가 만든 쉘 | Windows 기본 |

이 책에서는 **bash**와 **zsh**를 중심으로 설명합니다. macOS 사용자는 zsh가, Linux 사용자는 bash가 기본 쉘입니다. 두 쉘은 기본 명령어가 거의 동일하므로 어느 쉘을 사용하든 이 장의 내용을 그대로 따라할 수 있습니다.

> **Note:** Windows 사용자는 WSL(Windows Subsystem for Linux)을 설치하면 bash/zsh를 사용할 수 있습니다. 또는 Git Bash를 설치하는 방법도 있습니다.

---

### 7.3 기본 탐색 명령어

파일 시스템을 탐색하는 가장 기본적인 세 가지 명령어를 배워봅시다: `pwd`, `ls`, `cd`.

#### 예제 7-1: pwd - 현재 위치 확인

`pwd`는 "Print Working Directory"의 약자로, 현재 내가 어디에 있는지 알려줍니다.

```bash
$ pwd
/home/user
```

터미널을 처음 열면 보통 **홈 디렉토리**에 위치합니다. 홈 디렉토리는 사용자의 개인 공간으로, Linux에서는 `/home/사용자이름`, macOS에서는 `/Users/사용자이름` 형태입니다.

> **Tip:** 길을 잃었다고 느낄 때마다 `pwd`를 입력하세요. 현재 위치를 정확히 파악하는 것이 CLI 작업의 시작입니다.

#### 예제 7-2: ls - 파일 목록 보기

`ls`는 "List"의 약자로, 현재 디렉토리의 파일과 폴더 목록을 보여줍니다.

```bash
$ ls
Desktop  Documents  Downloads  Music  Pictures

$ ls -la
total 36
drwxr-xr-x  6 user user 4096 Jan 15 10:00 .
drwxr-xr-x  3 root root 4096 Jan 10 09:00 ..
-rw-r--r--  1 user user  220 Jan 10 09:00 .bashrc
drwxr-xr-x  2 user user 4096 Jan 12 14:30 Desktop
drwxr-xr-x  3 user user 4096 Jan 14 16:20 Documents
drwxr-xr-x  2 user user 4096 Jan 15 10:00 Downloads

$ ls -lh Documents/
total 12K
-rw-r--r-- 1 user user 2.5K Jan 14 16:20 report.txt
-rw-r--r-- 1 user user 1.1K Jan 13 11:00 notes.md
drwxr-xr-x 2 user user 4.0K Jan 12 09:00 projects
```

주요 옵션 정리:

| 옵션 | 의미 |
|------|------|
| `-l` | 상세 정보(권한, 크기, 날짜) 표시 |
| `-a` | 숨김 파일(`.`으로 시작)까지 표시 |
| `-h` | 파일 크기를 읽기 쉬운 단위(KB, MB)로 표시 |
| `-la` | `-l`과 `-a`를 합친 것 |

#### 예제 7-3: cd - 디렉토리 이동

`cd`는 "Change Directory"의 약자로, 다른 디렉토리로 이동합니다.

```bash
$ cd Documents
$ pwd
/home/user/Documents

$ cd ..
$ pwd
/home/user

$ cd ~
$ pwd
/home/user

$ cd /tmp
$ pwd
/tmp

$ cd -
$ pwd
/home/user
```

핵심 사용법:

| 명령어 | 의미 |
|--------|------|
| `cd 폴더명` | 해당 폴더로 이동 |
| `cd ..` | 상위(부모) 디렉토리로 이동 |
| `cd ~` | 홈 디렉토리로 이동 |
| `cd -` | 직전 디렉토리로 되돌아가기 |
| `cd /경로` | 절대 경로로 이동 |

> **Tip:** `cd -`는 두 디렉토리를 오가며 작업할 때 매우 편리합니다. 마치 TV 리모컨의 "이전 채널" 버튼과 같습니다.

---

### 7.4 파일과 디렉토리 다루기

이제 파일과 디렉토리를 생성, 복사, 이동, 삭제하는 방법을 배워봅시다.

#### 예제 7-4: mkdir - 디렉토리 생성

`mkdir`은 "Make Directory"의 약자로, 새 디렉토리(폴더)를 만듭니다.

```bash
$ mkdir myproject
$ ls
myproject

$ mkdir -p myapp/src/components
$ ls -R myapp/
myapp/:
src

myapp/src:
components

myapp/src/components:
```

`-p` 옵션은 중간 경로의 디렉토리가 없으면 함께 생성합니다. 중첩된 폴더 구조를 한 번에 만들 때 유용합니다.

#### 예제 7-5: touch - 빈 파일 생성

`touch`는 빈 파일을 생성하거나, 이미 존재하는 파일의 수정 시간을 갱신합니다.

```bash
$ touch hello.py
$ ls
hello.py

$ touch file1.txt file2.txt file3.txt
$ ls
file1.txt  file2.txt  file3.txt  hello.py
```

> **Note:** `touch`는 기존 파일의 내용을 변경하지 않습니다. 이미 있는 파일에 `touch`를 실행하면 수정 시간만 현재 시각으로 업데이트됩니다.

#### 예제 7-6: cp - 파일 복사

`cp`는 "Copy"의 약자로, 파일이나 디렉토리를 복사합니다.

```bash
$ cp file1.txt file1_backup.txt
$ ls
file1.txt  file1_backup.txt

$ cp -r myproject myproject_backup
$ ls
myproject  myproject_backup
```

| 사용법 | 의미 |
|--------|------|
| `cp 원본 사본` | 파일 복사 |
| `cp -r 원본폴더 사본폴더` | 디렉토리 전체 복사 (`-r`은 recursive) |

#### 예제 7-7: mv - 파일 이동/이름 변경

`mv`는 "Move"의 약자로, 파일을 이동하거나 이름을 변경합니다.

```bash
$ mv old.txt new.txt
$ ls
new.txt

$ mv new.txt ../
$ ls ../new.txt
../new.txt
```

`mv`는 이름 변경과 이동 두 가지 역할을 합니다:
- **이름 변경**: `mv old.txt new.txt` — 같은 위치에서 이름만 변경
- **이동**: `mv file.txt ../` — 파일을 다른 디렉토리로 이동

#### 예제 7-8: rm - 파일 삭제

`rm`은 "Remove"의 약자로, 파일이나 디렉토리를 삭제합니다.

```bash
$ rm file1.txt
$ ls
file2.txt  file3.txt

$ rm -r myproject_backup/
$ ls
file2.txt  file3.txt
```

| 사용법 | 의미 |
|--------|------|
| `rm 파일명` | 파일 삭제 |
| `rm -r 폴더명` | 디렉토리와 그 안의 모든 내용 삭제 |
| `rm -i 파일명` | 삭제 전 확인 질문 |

> **Warning:** `rm`으로 삭제한 파일은 휴지통을 거치지 않고 **영구 삭제**됩니다. 특히 `rm -rf /`와 같은 명령어는 시스템 전체를 삭제할 수 있으므로 **절대 실행하지 마세요**. `rm` 명령어를 사용할 때는 항상 삭제 대상을 정확히 확인하세요.

---

### 7.5 파일 내용 보기

파일 안에 무엇이 들어 있는지 확인하는 명령어들을 알아봅시다.

#### 예제 7-9: cat - 파일 내용 보기

`cat`은 "Concatenate"의 약자로, 파일 내용을 화면에 출력합니다.

```bash
$ cat hello.py
# 간단한 인사 프로그램
def greet(name):
    print(f"안녕하세요, {name}님!")

greet("바이브 코더")
```

`cat`은 짧은 파일을 빠르게 확인할 때 적합합니다. 파일이 길 경우에는 `less`, `head`, `tail`을 사용하는 것이 좋습니다.

자주 사용하는 관련 명령어:

| 명령어 | 설명 |
|--------|------|
| `less 파일명` | 파일을 페이지 단위로 탐색 (q로 종료) |
| `head 파일명` | 파일의 처음 10줄 출력 |
| `head -n 5 파일명` | 파일의 처음 5줄 출력 |
| `tail 파일명` | 파일의 마지막 10줄 출력 |
| `tail -n 3 파일명` | 파일의 마지막 3줄 출력 |

> **Tip:** `less`에서는 방향키로 스크롤하고, `/검색어`로 내용을 검색할 수 있습니다. 종료할 때는 `q`를 누르세요.

---

### 7.6 텍스트 처리 기초

텍스트를 출력하고 검색하는 두 가지 핵심 명령어를 배워봅시다.

#### 예제 7-10: echo - 텍스트 출력

`echo`는 텍스트를 화면에 출력하거나, 파일에 내용을 쓸 때 사용합니다.

```bash
$ echo "Hello, Vibe Coding!"
Hello, Vibe Coding!

$ echo $HOME
/home/user

$ echo "print('hello')" > hello.py
$ cat hello.py
print('hello')
```

`echo`는 단순해 보이지만 매우 다양한 상황에서 활용됩니다:
- 텍스트 메시지 출력
- 환경 변수 값 확인 (`$HOME`, `$PATH` 등)
- 파일에 내용 쓰기 (`>` 리다이렉션과 함께)

#### 예제 7-11: grep - 텍스트 검색

`grep`은 파일 안에서 특정 텍스트를 검색하는 강력한 명령어입니다.

```bash
$ grep "def" hello.py
def greet(name):

$ grep -n "error" log.txt
3:error: 파일을 찾을 수 없습니다
7:error: 네트워크 연결 실패
15:error: 권한이 없습니다

$ grep -r "TODO" .
./src/main.py:# TODO: 로그인 기능 구현
./src/utils.py:# TODO: 에러 처리 추가
./tests/test_main.py:# TODO: 테스트 케이스 추가
```

주요 옵션:

| 옵션 | 의미 |
|------|------|
| `-n` | 일치하는 줄의 줄 번호 표시 |
| `-r` | 하위 디렉토리까지 재귀적으로 검색 |
| `-i` | 대소문자 구분 없이 검색 |
| `-c` | 일치하는 줄의 개수만 출력 |

> **Tip:** `grep`은 바이브 코딩에서 코드를 분석할 때 자주 사용됩니다. AI 어시스턴트에게 코드 수정을 요청하기 전에 `grep`으로 관련 코드를 먼저 찾아보면 더 정확한 프롬프트를 작성할 수 있습니다.

---

### 7.7 파이프와 리다이렉션

명령어들을 연결하고 결과를 저장하는 방법을 배워봅시다. 이것은 CLI의 진정한 힘이 드러나는 부분입니다.

#### 예제 7-12: | (파이프)

파이프(`|`)는 앞 명령어의 출력을 뒷 명령어의 입력으로 전달합니다. 마치 공장의 컨베이어 벨트처럼 데이터를 흘려보내는 것입니다.

```bash
$ ls -la | grep ".py"
-rw-r--r-- 1 user user   95 Jan 15 10:30 hello.py
-rw-r--r-- 1 user user  142 Jan 15 11:00 utils.py

$ cat file.txt | wc -l
42
```

| 조합 | 의미 |
|------|------|
| `ls -la \| grep ".py"` | 파일 목록에서 `.py` 파일만 필터링 |
| `cat file.txt \| wc -l` | 파일의 총 줄 수 세기 |
| `history \| grep "git"` | 명령어 기록에서 git 관련 명령어 찾기 |

> **Note:** `wc`는 "Word Count"의 약자입니다. `-l`은 줄 수, `-w`는 단어 수, `-c`는 바이트 수를 셉니다.

#### 예제 7-13: > >> 리다이렉션

리다이렉션은 명령어의 출력을 화면 대신 파일로 보냅니다.

```bash
$ echo "hello" > file.txt
$ cat file.txt
hello

$ echo "world" >> file.txt
$ cat file.txt
hello
world

$ python3 script.py > output.txt
```

| 기호 | 의미 |
|------|------|
| `>` | 출력을 파일로 저장 (기존 내용 **덮어쓰기**) |
| `>>` | 출력을 파일에 추가 (기존 내용 **유지**) |

> **Warning:** `>`는 기존 파일 내용을 완전히 지우고 새로 씁니다. 내용을 추가하고 싶다면 반드시 `>>`를 사용하세요.

---

### 7.8 종합 실습

지금까지 배운 명령어들을 모두 활용하여 실제 프로젝트를 구성해봅시다.

#### 예제 7-14: CLI로 프로젝트 구조 만들기

Python 웹 프로젝트의 기본 구조를 CLI만으로 생성해봅시다.

```bash
$ mkdir -p my-web-app/src/templates
$ mkdir -p my-web-app/src/static/css
$ mkdir -p my-web-app/src/static/js
$ mkdir -p my-web-app/tests
$ mkdir -p my-web-app/docs

$ touch my-web-app/src/app.py
$ touch my-web-app/src/config.py
$ touch my-web-app/src/templates/index.html
$ touch my-web-app/src/static/css/style.css
$ touch my-web-app/src/static/js/main.js
$ touch my-web-app/tests/test_app.py
$ touch my-web-app/README.md
$ touch my-web-app/requirements.txt

$ echo "# My Web App" > my-web-app/README.md
$ echo "flask==3.0.0" > my-web-app/requirements.txt

$ ls -R my-web-app/
my-web-app/:
README.md  docs  requirements.txt  src  tests

my-web-app/docs:

my-web-app/src:
app.py  config.py  static  templates

my-web-app/src/static:
css  js

my-web-app/src/static/css:
style.css

my-web-app/src/static/js:
main.js

my-web-app/src/templates:
index.html

my-web-app/tests:
test_app.py
```

이렇게 CLI 몇 줄만으로 체계적인 프로젝트 구조가 완성됩니다. GUI에서 폴더를 하나하나 클릭하며 만드는 것보다 훨씬 빠르고 정확합니다.

> **Tip:** 바이브 코딩에서는 AI 어시스턴트에게 "Python Flask 프로젝트 구조를 만들어줘"라고 요청하면, 위와 같은 명령어를 자동으로 실행해줍니다. 하지만 기본 명령어를 이해하고 있으면 AI의 작업을 검증하고 수정할 수 있습니다.

#### 예제 7-15: 종합 실습 - 파일 정리

여러 종류의 파일을 확장자별로 폴더에 정리하는 쉘 스크립트를 만들어봅시다.

```bash
# examples/bash/chapter02/organize_files.sh

#!/bin/bash
# 파일 정리 스크립트 - 확장자별로 폴더에 분류합니다

echo "=== 파일 정리 스크립트 ==="
echo ""

# 작업 디렉토리 생성
WORK_DIR="/tmp/organize_demo"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# 샘플 파일 생성
echo "1단계: 샘플 파일 생성 중..."
touch report.txt notes.txt memo.txt
touch photo1.jpg photo2.jpg screenshot.png
touch app.py utils.py test.py
touch style.css index.html script.js
echo "  → 12개 파일 생성 완료"
echo ""

# 현재 파일 목록 확인
echo "2단계: 현재 파일 목록"
ls -1
echo ""

# 확장자별 폴더 생성
echo "3단계: 확장자별 폴더 생성 중..."
mkdir -p documents images python web
echo "  → 4개 폴더 생성 완료"
echo ""

# 파일 분류
echo "4단계: 파일 분류 중..."
mv *.txt documents/
echo "  → .txt 파일 → documents/"
mv *.jpg *.png images/
echo "  → .jpg, .png 파일 → images/"
mv *.py python/
echo "  → .py 파일 → python/"
mv *.css *.html *.js web/
echo "  → .css, .html, .js 파일 → web/"
echo ""

# 결과 확인
echo "5단계: 정리 결과"
echo "---"
for dir in documents images python web; do
    count=$(ls "$dir" | wc -l)
    echo "📂 $dir/ ($count개 파일)"
    ls "$dir" | while read file; do
        echo "   - $file"
    done
done
echo "---"
echo ""
echo "=== 파일 정리 완료! ==="
```

**실행:**
```bash
$ bash examples/bash/chapter02/organize_files.sh
```

**결과:**
```
=== 파일 정리 스크립트 ===

1단계: 샘플 파일 생성 중...
  → 12개 파일 생성 완료

2단계: 현재 파일 목록
app.py
index.html
memo.txt
notes.txt
photo1.jpg
photo2.jpg
report.txt
screenshot.png
script.js
style.css
test.py
utils.py

3단계: 확장자별 폴더 생성 중...
  → 4개 폴더 생성 완료

4단계: 파일 분류 중...
  → .txt 파일 → documents/
  → .jpg, .png 파일 → images/
  → .py 파일 → python/
  → .css, .html, .js 파일 → web/

5단계: 정리 결과
---
📂 documents/ (3개 파일)
   - memo.txt
   - notes.txt
   - report.txt
📂 images/ (3개 파일)
   - photo1.jpg
   - photo2.jpg
   - screenshot.png
📂 python/ (3개 파일)
   - app.py
   - test.py
   - utils.py
📂 web/ (3개 파일)
   - index.html
   - script.js
   - style.css
---

=== 파일 정리 완료! ===
```

이 스크립트는 지금까지 배운 `mkdir`, `touch`, `mv`, `ls`, `echo`, 파이프(`|`), 그리고 변수와 반복문까지 활용합니다. 이처럼 CLI 명령어들을 조합하면 반복적인 작업을 자동화할 수 있습니다.

---

### 정리

이 장에서 배운 CLI 핵심 명령어를 정리합니다:

| 분류 | 명령어 | 기능 |
|------|--------|------|
| **탐색** | `pwd` | 현재 디렉토리 확인 |
| | `ls` | 파일 목록 보기 |
| | `cd` | 디렉토리 이동 |
| **파일 관리** | `mkdir` | 디렉토리 생성 |
| | `touch` | 빈 파일 생성 |
| | `cp` | 복사 |
| | `mv` | 이동/이름 변경 |
| | `rm` | 삭제 |
| **내용 확인** | `cat` | 파일 내용 출력 |
| | `less` | 페이지 단위 보기 |
| | `head`/`tail` | 처음/마지막 부분 보기 |
| **텍스트** | `echo` | 텍스트 출력 |
| | `grep` | 텍스트 검색 |
| **조합** | `\|` | 파이프 (명령어 연결) |
| | `>`/`>>` | 리다이렉션 (출력 저장) |

> **Tip:** 이 명령어들을 외우려고 하지 마세요. 자주 사용하다 보면 자연스럽게 손에 익습니다. 처음에는 이 표를 참고하면서 하나씩 연습해보세요.

---

### 다음 장 예고

다음 장에서는 **패키지 관리자와 개발 환경 설정**을 다룹니다. `pip`, `npm` 같은 패키지 관리자를 사용하는 방법과 Python, Node.js 등 프로그래밍 언어별 개발 환경을 CLI로 설정하는 방법을 배워봅시다. 이번 장에서 익힌 CLI 기본기가 그 토대가 될 것입니다.
