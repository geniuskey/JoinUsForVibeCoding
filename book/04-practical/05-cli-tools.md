## Chapter 19: CLI 도구 만들기

터미널에서 명령어 하나로 원하는 작업을 처리하는 도구를 직접 만들 수 있다면 어떨까요? 파일을 한꺼번에 검색하고, 할일을 관리하고, 데이터를 분석하는 나만의 명령줄 도구를 파이썬으로 만드는 것은 생각보다 어렵지 않습니다. 이 장에서는 파이썬 표준 라이브러리인 `argparse`를 중심으로, 외부 패키지 없이 완성도 높은 CLI 도구를 만드는 방법을 배웁니다.

---

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- `argparse`를 사용하여 명령줄 인자를 처리하는 CLI 도구 만들기
- 위치 인자, 선택 인자, 플래그 옵션의 차이를 이해하고 활용하기
- 서브커맨드로 복잡한 CLI 도구 설계하기
- 입력값 타입 검증과 커스텀 검증 함수 작성하기
- 대화형 입력으로 사용자와 상호작용하기
- ANSI 이스케이프 코드로 터미널에 색상 출력하기
- 진행률 바와 스피너로 사용자 경험 향상시키기
- 실전 도구(파일 검색, TODO 관리 앱) 만들기

---

### 19.1 CLI 도구란?

**CLI(Command Line Interface)** 도구는 터미널(명령 프롬프트)에서 텍스트 명령을 입력하여 사용하는 프로그램입니다. 여러분이 이미 사용해 본 `python`, `git`, `pip` 같은 프로그램이 모두 CLI 도구입니다.

```bash
$ python script.py          # python CLI 도구
$ git status                # git CLI 도구
$ pip install requests      # pip CLI 도구
```

CLI 도구의 장점은 다음과 같습니다:

| 장점 | 설명 |
|------|------|
| **자동화** | 스크립트로 반복 작업을 자동화할 수 있음 |
| **파이프라인** | 여러 도구를 연결하여 복잡한 작업 수행 가능 |
| **경량** | GUI 없이 빠르게 실행됨 |
| **원격 작업** | SSH 등으로 원격 서버에서도 사용 가능 |
| **재현성** | 같은 명령을 다시 실행하면 같은 결과를 얻음 |

> **Note:** 바이브 코딩에서 CLI 도구를 만드는 것은 매우 실용적입니다. AI에게 "파일을 정리하는 CLI 도구를 만들어줘"라고 요청하면, 바로 사용할 수 있는 도구가 생성됩니다.

---

### 19.2 argparse 기본 사용법

파이썬 표준 라이브러리에 포함된 `argparse` 모듈은 CLI 도구를 만들기 위한 가장 기본적이고 강력한 도구입니다. 외부 패키지를 설치할 필요 없이 바로 사용할 수 있습니다.

가장 간단한 예제부터 시작해 봅시다.

**예제 19-1: 기본 argparse 사용**

```python
# examples/python/chapter04/ex19_01_basic_argparse.py
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="간단한 인사 프로그램입니다."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="세계",
        help="인사할 이름 (기본값: 세계)"
    )

    args = parser.parse_args()
    print(f"안녕하세요, {args.name}님! 바이브 코딩의 세계에 오신 것을 환영합니다!")


if __name__ == "__main__":
    main()
```

이 코드의 흐름을 하나씩 살펴보겠습니다:

1. **`ArgumentParser` 생성**: 프로그램의 설명을 포함한 파서 객체를 만듭니다.
2. **`add_argument`로 인자 추가**: `--name`이라는 선택 인자를 정의합니다. 기본값은 `"세계"`입니다.
3. **`parse_args`로 파싱**: 사용자가 입력한 명령줄 인자를 파싱합니다.
4. **`args.name`으로 접근**: 파싱된 값을 속성으로 접근합니다.

**실행:**
```bash
$ python examples/python/chapter04/ex19_01_basic_argparse.py
```

**결과:**
```
안녕하세요, 세계님! 바이브 코딩의 세계에 오신 것을 환영합니다!
```

이름을 지정하여 실행하면:
```bash
$ python examples/python/chapter04/ex19_01_basic_argparse.py --name 홍길동
```

**결과:**
```
안녕하세요, 홍길동님! 바이브 코딩의 세계에 오신 것을 환영합니다!
```

`argparse`는 `--help` 옵션도 자동으로 생성해 줍니다:
```bash
$ python examples/python/chapter04/ex19_01_basic_argparse.py --help
```

**결과:**
```
usage: ex19_01_basic_argparse.py [-h] [--name NAME]

간단한 인사 프로그램입니다.

options:
  -h, --help   show this help message and exit
  --name NAME  인사할 이름 (기본값: 세계)
```

> **Tip:** `argparse`는 `--help`(-h) 옵션을 자동으로 추가합니다. 따라서 도움말을 별도로 구현할 필요가 없습니다. 도움말 메시지는 `description`과 각 인자의 `help` 매개변수에서 자동으로 생성됩니다.

---

### 19.3 필수 인자와 선택 인자

CLI 도구에서 인자는 크게 두 종류로 나뉩니다:

- **위치 인자(Positional Argument)**: 반드시 입력해야 하는 필수 인자. 이름 앞에 `--`가 없습니다.
- **선택 인자(Optional Argument)**: 생략 가능한 인자. 이름 앞에 `--`가 붙습니다.

**예제 19-2: 필수/선택 인자**

```python
# examples/python/chapter04/ex19_02_required_optional.py
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="파일 정보를 출력하는 CLI 도구입니다."
    )

    # 위치 인자 (필수)
    parser.add_argument(
        "filename",
        help="처리할 파일 이름 (필수)"
    )

    # 선택 인자
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="파일 인코딩 (기본값: utf-8)"
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=10,
        help="출력할 최대 줄 수 (기본값: 10)"
    )

    args = parser.parse_args()

    print(f"[파일 정보]")
    print(f"  파일명  : {args.filename}")
    print(f"  인코딩  : {args.encoding}")
    print(f"  최대 줄 : {args.lines}줄")
    print()

    # 실제 파일 읽기 시도
    try:
        with open(args.filename, "r", encoding=args.encoding) as f:
            for i, line in enumerate(f, 1):
                if i > args.lines:
                    print(f"  ... (이하 생략, 최대 {args.lines}줄)")
                    break
                print(f"  {i:4d} | {line.rstrip()}")
    except FileNotFoundError:
        print(f"  [데모 모드] '{args.filename}' 파일이 없습니다.")
        print(f"  실제 파일 경로를 지정하면 내용을 출력합니다.")


if __name__ == "__main__":
    main()
```

이 도구는 `filename`이라는 위치 인자를 반드시 받아야 합니다. `--encoding`과 `--lines`는 선택 인자로, 생략하면 기본값이 사용됩니다.

**실행:**
```bash
$ python examples/python/chapter04/ex19_02_required_optional.py mydata.txt
```

**결과:**
```
[파일 정보]
  파일명  : mydata.txt
  인코딩  : utf-8
  최대 줄 : 10줄

  [데모 모드] 'mydata.txt' 파일이 없습니다.
  실제 파일 경로를 지정하면 내용을 출력합니다.
```

선택 인자를 함께 지정하면:
```bash
$ python examples/python/chapter04/ex19_02_required_optional.py mydata.txt --encoding euc-kr --lines 5
```

**결과:**
```
[파일 정보]
  파일명  : mydata.txt
  인코딩  : euc-kr
  최대 줄 : 5줄

  [데모 모드] 'mydata.txt' 파일이 없습니다.
  실제 파일 경로를 지정하면 내용을 출력합니다.
```

위치 인자 없이 실행하면 `argparse`가 자동으로 오류를 출력합니다:
```bash
$ python examples/python/chapter04/ex19_02_required_optional.py
```

**결과:**
```
usage: ex19_02_required_optional.py [-h] [--encoding ENCODING] [--lines LINES] filename
ex19_02_required_optional.py: error: the following arguments are required: filename
```

> **Note:** 위치 인자와 선택 인자의 핵심 차이는 `--` 접두사입니다. `add_argument("filename")`은 위치 인자(필수)이고, `add_argument("--filename")`은 선택 인자입니다. 선택 인자를 필수로 만들고 싶다면 `required=True`를 추가하면 됩니다.

#### 인자 유형 정리

| 구분 | 문법 | 필수 여부 | 예 |
|------|------|-----------|-----|
| 위치 인자 | `add_argument("name")` | 필수 | `program hello` |
| 선택 인자 | `add_argument("--name")` | 선택 | `program --name hello` |
| 필수 선택 | `add_argument("--name", required=True)` | 필수 | `program --name hello` |

---

### 19.4 플래그 옵션과 상호 배타적 그룹

프로그램의 동작 모드를 전환하는 **플래그(flag)** 옵션은 값 없이 사용하는 인자입니다. `--verbose`처럼 지정하면 `True`, 생략하면 `False`가 됩니다.

**예제 19-3: 플래그 옵션**

```python
# examples/python/chapter04/ex19_03_flag_options.py
import argparse
import os


def get_directory_info(path, verbose=False, quiet=False):
    """디렉토리 정보를 수집합니다."""
    items = os.listdir(path)
    files = [f for f in items if os.path.isfile(os.path.join(path, f))]
    dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]

    if quiet:
        # 조용한 모드: 숫자만 출력
        print(f"{len(files)}개 파일, {len(dirs)}개 디렉토리")
        return

    print(f"디렉토리: {os.path.abspath(path)}")
    print(f"파일: {len(files)}개 | 디렉토리: {len(dirs)}개")

    if verbose:
        # 상세 모드: 모든 항목을 출력
        print()
        if dirs:
            print("[디렉토리 목록]")
            for d in sorted(dirs):
                full_path = os.path.join(path, d)
                sub_count = len(os.listdir(full_path))
                print(f"  {d}/ ({sub_count}개 항목)")
        if files:
            print("[파일 목록]")
            for f in sorted(files):
                full_path = os.path.join(path, f)
                size = os.path.getsize(full_path)
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f}KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f}MB"
                print(f"  -- {f} ({size_str})")


def main():
    parser = argparse.ArgumentParser(
        description="디렉토리 정보를 출력하는 도구입니다."
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="조회할 디렉토리 경로 (기본값: 현재 디렉토리)"
    )

    # 상호 배타적 그룹: --verbose와 --quiet는 동시 사용 불가
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="상세 모드: 모든 파일과 디렉토리를 출력"
    )
    group.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="조용한 모드: 개수만 출력"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"오류: '{args.path}'는 유효한 디렉토리가 아닙니다.")
        return

    get_directory_info(args.path, verbose=args.verbose, quiet=args.quiet)


if __name__ == "__main__":
    main()
```

이 예제에서 주목할 부분은 두 가지입니다:

**1. `action="store_true"`**: 인자가 지정되면 `True`, 생략되면 `False`가 됩니다. 별도의 값을 받지 않습니다.

**2. `add_mutually_exclusive_group()`**: `--verbose`와 `--quiet`는 동시에 사용할 수 없습니다. 이 그룹 안에 넣으면 `argparse`가 자동으로 이를 검증합니다.

**실행 - 기본 모드:**
```bash
$ python examples/python/chapter04/ex19_03_flag_options.py .
```

**결과:**
```
디렉토리: /home/user/JoinUsForVibeCoding
파일: 5개 | 디렉토리: 4개
```

**실행 - 상세 모드:**
```bash
$ python examples/python/chapter04/ex19_03_flag_options.py . --verbose
```

**결과:**
```
디렉토리: /home/user/JoinUsForVibeCoding
파일: 5개 | 디렉토리: 4개

[디렉토리 목록]
  assets/ (0개 항목)
  book/ (8개 항목)
  examples/ (4개 항목)
  ...
[파일 목록]
  -- CLAUDE.md (3.2KB)
  -- PRD.md (5.1KB)
  ...
```

**실행 - 조용한 모드:**
```bash
$ python examples/python/chapter04/ex19_03_flag_options.py . -q
```

**결과:**
```
5개 파일, 4개 디렉토리
```

동시 사용을 시도하면 오류가 발생합니다:
```bash
$ python examples/python/chapter04/ex19_03_flag_options.py . -v -q
```

**결과:**
```
usage: ex19_03_flag_options.py [-h] [-v | -q] [path]
ex19_03_flag_options.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
```

> **Tip:** 짧은 옵션 이름(`-v`)과 긴 옵션 이름(`--verbose`)을 함께 제공하면 사용자가 편리하게 선택할 수 있습니다. 관례적으로 `-v`는 verbose, `-q`는 quiet, `-h`는 help에 사용됩니다.

#### nargs 매개변수

`nargs="?"`는 위치 인자를 선택적으로 만들어 줍니다. `nargs`의 주요 값을 정리하면:

| 값 | 의미 | 예 |
|----|------|-----|
| `"?"` | 0개 또는 1개 | 생략 가능한 위치 인자 |
| `"*"` | 0개 이상 | 여러 파일을 한번에 지정 |
| `"+"` | 1개 이상 | 최소 1개는 필요 |
| `N` (정수) | 정확히 N개 | `nargs=3`이면 3개 필수 |

---

### 19.5 서브커맨드 구현

실제 CLI 도구들은 대부분 **서브커맨드** 패턴을 사용합니다. `git commit`, `git push`, `docker run`, `docker build`처럼 하나의 프로그램 안에서 여러 기능을 제공하는 구조입니다.

`argparse`의 `add_subparsers`를 사용하면 이 패턴을 쉽게 구현할 수 있습니다.

**예제 19-4: 서브커맨드 구현**

```python
# examples/python/chapter04/ex19_04_subcommands.py
import argparse
import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex19_04_notes.json")


def load_notes():
    """저장된 메모 목록을 불러옵니다."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_notes(notes):
    """메모 목록을 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def cmd_add(args):
    """메모를 추가합니다."""
    notes = load_notes()
    note = {"id": len(notes) + 1, "content": args.content}
    notes.append(note)
    save_notes(notes)
    print(f"메모가 추가되었습니다: [{note['id']}] {note['content']}")


def cmd_list(args):
    """메모 목록을 출력합니다."""
    notes = load_notes()
    if not notes:
        print("저장된 메모가 없습니다.")
        return
    print(f"총 {len(notes)}개의 메모:")
    for note in notes:
        print(f"  [{note['id']}] {note['content']}")


def cmd_delete(args):
    """메모를 삭제합니다."""
    notes = load_notes()
    original_count = len(notes)
    notes = [n for n in notes if n["id"] != args.id]

    if len(notes) == original_count:
        print(f"오류: ID {args.id}인 메모를 찾을 수 없습니다.")
        return

    save_notes(notes)
    print(f"메모 [{args.id}]가 삭제되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description="간단한 메모 관리 CLI 도구"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="사용 가능한 명령어"
    )

    # add 서브커맨드
    parser_add = subparsers.add_parser("add", help="새 메모를 추가합니다")
    parser_add.add_argument("content", help="메모 내용")
    parser_add.set_defaults(func=cmd_add)

    # list 서브커맨드
    parser_list = subparsers.add_parser("list", help="메모 목록을 봅니다")
    parser_list.set_defaults(func=cmd_list)

    # delete 서브커맨드
    parser_delete = subparsers.add_parser("delete", help="메모를 삭제합니다")
    parser_delete.add_argument("id", type=int, help="삭제할 메모 ID")
    parser_delete.set_defaults(func=cmd_delete)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
```

서브커맨드 구현의 핵심 구조를 분석해 봅시다:

1. **`add_subparsers(dest="command")`**: 서브커맨드를 위한 서브파서 그룹을 만듭니다. `dest`는 선택된 서브커맨드 이름이 저장될 속성명입니다.
2. **`subparsers.add_parser("add")`**: 각 서브커맨드를 위한 파서를 만듭니다. 이 파서에 독립적으로 인자를 추가할 수 있습니다.
3. **`set_defaults(func=cmd_add)`**: 서브커맨드가 선택되면 호출할 함수를 지정합니다.
4. **`args.func(args)`**: 선택된 서브커맨드의 함수를 호출합니다.

**실행 - 메모 추가:**
```bash
$ python examples/python/chapter04/ex19_04_subcommands.py add "파이썬 공부하기"
```

**결과:**
```
메모가 추가되었습니다: [1] 파이썬 공부하기
```

**실행 - 메모 목록:**
```bash
$ python examples/python/chapter04/ex19_04_subcommands.py list
```

**결과:**
```
총 1개의 메모:
  [1] 파이썬 공부하기
```

**실행 - 메모 삭제:**
```bash
$ python examples/python/chapter04/ex19_04_subcommands.py delete 1
```

**결과:**
```
메모 [1]가 삭제되었습니다.
```

**실행 - 명령어 없이 실행하면 도움말 표시:**
```bash
$ python examples/python/chapter04/ex19_04_subcommands.py
```

**결과:**
```
usage: ex19_04_subcommands.py [-h] {add,list,delete} ...

간단한 메모 관리 CLI 도구

positional arguments:
  {add,list,delete}  사용 가능한 명령어
    add              새 메모를 추가합니다
    list             메모 목록을 봅니다
    delete           메모를 삭제합니다

options:
  -h, --help         show this help message and exit
```

> **Note:** 서브커맨드 패턴은 CLI 도구의 가장 일반적인 설계 패턴입니다. 하나의 프로그램 안에서 관련된 기능들을 체계적으로 묶을 수 있으며, 각 서브커맨드가 독립적인 인자를 가질 수 있어 매우 유연합니다.

---

### 19.6 타입 검증과 커스텀 검증

사용자 입력은 항상 검증해야 합니다. `argparse`는 `type`과 `choices` 매개변수로 기본적인 검증을 제공하며, 커스텀 함수를 만들어 더 정교한 검증도 가능합니다.

**예제 19-5: 타입 검증**

```python
# examples/python/chapter04/ex19_05_type_validation.py
import argparse


def positive_int(value):
    """양의 정수만 허용하는 커스텀 타입 함수"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}'는 정수가 아닙니다.")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"'{value}'는 양의 정수가 아닙니다. (1 이상 필요)")
    return ivalue


def main():
    parser = argparse.ArgumentParser(
        description="성적 계산기 — 타입 검증 예제"
    )

    parser.add_argument(
        "name",
        type=str,
        help="학생 이름"
    )
    parser.add_argument(
        "--score",
        type=int,
        required=True,
        help="점수 (0~100 사이의 정수)"
    )
    parser.add_argument(
        "--subject",
        type=str,
        choices=["math", "english", "science", "korean"],
        default="math",
        help="과목 선택 (math, english, science, korean)"
    )
    parser.add_argument(
        "--repeat",
        type=positive_int,
        default=1,
        help="출력 반복 횟수 (양의 정수, 기본값: 1)"
    )

    args = parser.parse_args()

    # 점수 범위 검증
    if not 0 <= args.score <= 100:
        parser.error(f"점수는 0~100 사이여야 합니다. (입력값: {args.score})")

    # 등급 계산
    if args.score >= 90:
        grade = "A"
    elif args.score >= 80:
        grade = "B"
    elif args.score >= 70:
        grade = "C"
    elif args.score >= 60:
        grade = "D"
    else:
        grade = "F"

    subject_names = {
        "math": "수학",
        "english": "영어",
        "science": "과학",
        "korean": "국어"
    }
    subject_kr = subject_names[args.subject]

    for i in range(args.repeat):
        if args.repeat > 1:
            print(f"--- 출력 {i + 1}/{args.repeat} ---")
        print(f"학생: {args.name}")
        print(f"과목: {subject_kr}")
        print(f"점수: {args.score}점")
        print(f"등급: {grade}")
        if i < args.repeat - 1:
            print()


if __name__ == "__main__":
    main()
```

이 예제에서 사용된 검증 기법을 정리합니다:

#### 1) `type` 매개변수

`type=int`를 지정하면 `argparse`가 자동으로 문자열을 정수로 변환하고, 변환할 수 없으면 오류를 발생시킵니다.

#### 2) `choices` 매개변수

`choices=["math", "english", "science", "korean"]`은 입력값을 지정된 목록으로 제한합니다.

#### 3) 커스텀 타입 함수

`positive_int` 함수는 값을 정수로 변환하고 양수인지 확인합니다. `argparse.ArgumentTypeError`를 발생시키면 사용자에게 의미 있는 오류 메시지가 출력됩니다.

#### 4) `parser.error()`

`parse_args()` 이후에 추가 검증이 필요하면 `parser.error()`를 호출합니다. 이 함수는 오류 메시지를 출력하고 프로그램을 종료합니다.

**실행 - 정상 입력:**
```bash
$ python examples/python/chapter04/ex19_05_type_validation.py 김철수 --score 95 --subject math
```

**결과:**
```
학생: 김철수
과목: 수학
점수: 95점
등급: A
```

**실행 - 잘못된 과목 입력:**
```bash
$ python examples/python/chapter04/ex19_05_type_validation.py 김철수 --score 80 --subject history
```

**결과:**
```
usage: ex19_05_type_validation.py [-h] --score SCORE [--subject {math,english,science,korean}] [--repeat REPEAT] name
ex19_05_type_validation.py: error: argument --subject: invalid choice: 'history' (choose from 'math', 'english', 'science', 'korean')
```

**실행 - 잘못된 반복 횟수:**
```bash
$ python examples/python/chapter04/ex19_05_type_validation.py 김철수 --score 80 --repeat -3
```

**결과:**
```
usage: ex19_05_type_validation.py [-h] --score SCORE [--subject {math,english,science,korean}] [--repeat REPEAT] name
ex19_05_type_validation.py: error: argument --repeat: '-3'는 양의 정수가 아닙니다. (1 이상 필요)
```

> **Warning:** 사용자 입력을 항상 검증하세요. 검증 없이 입력을 사용하면 프로그램이 예상치 못한 동작을 할 수 있습니다. `argparse`의 `type`, `choices`, 커스텀 검증 함수를 적극 활용하세요.

---

### 19.7 대화형 입력

모든 CLI 도구가 명령줄 인자만 받는 것은 아닙니다. 때로는 프로그램 실행 후 사용자와 대화하며 입력을 받아야 할 때가 있습니다. 파이썬의 `input()` 함수를 사용하면 이런 대화형 인터페이스를 만들 수 있습니다.

**예제 19-6: 대화형 입력**

```python
# examples/python/chapter04/ex19_06_interactive_input.py
import sys


def get_validated_input(prompt, validator, error_msg, max_attempts=3):
    """검증 루프를 사용하여 올바른 입력을 받습니다."""
    for attempt in range(1, max_attempts + 1):
        try:
            value = input(prompt)
            if validator(value):
                return value
            else:
                print(f"  오류: {error_msg}")
        except (EOFError, KeyboardInterrupt):
            print("\n입력이 취소되었습니다.")
            sys.exit(0)

        remaining = max_attempts - attempt
        if remaining > 0:
            print(f"  (남은 시도: {remaining}회)")
        else:
            print(f"  최대 시도 횟수를 초과했습니다.")
            return None

    return None


def main():
    print("=" * 40)
    print("  간단한 프로필 등록 프로그램")
    print("=" * 40)
    print()

    # 이름 입력 (빈 문자열 불가)
    name = get_validated_input(
        "이름을 입력하세요: ",
        lambda v: len(v.strip()) > 0,
        "이름은 비어 있을 수 없습니다."
    )
    if name is None:
        return

    # 나이 입력 (1~150 사이 정수)
    age_str = get_validated_input(
        "나이를 입력하세요 (1~150): ",
        lambda v: v.isdigit() and 1 <= int(v) <= 150,
        "1에서 150 사이의 숫자를 입력해주세요."
    )
    if age_str is None:
        return
    age = int(age_str)

    # 이메일 입력 (@ 포함 여부 확인)
    email = get_validated_input(
        "이메일을 입력하세요: ",
        lambda v: "@" in v and "." in v.split("@")[-1],
        "올바른 이메일 형식이 아닙니다. (예: user@example.com)"
    )
    if email is None:
        return

    # 관심 분야 선택
    print()
    print("관심 분야를 선택하세요:")
    interests = ["웹 개발", "데이터 분석", "AI/ML", "게임 개발", "모바일 앱"]
    for i, interest in enumerate(interests, 1):
        print(f"  {i}. {interest}")

    choice_str = get_validated_input(
        f"번호를 입력하세요 (1~{len(interests)}): ",
        lambda v: v.isdigit() and 1 <= int(v) <= len(interests),
        f"1에서 {len(interests)} 사이의 번호를 입력해주세요."
    )
    if choice_str is None:
        return
    interest = interests[int(choice_str) - 1]

    # 결과 출력
    print()
    print("=" * 40)
    print("  등록된 프로필 정보")
    print("=" * 40)
    print(f"  이름    : {name.strip()}")
    print(f"  나이    : {age}세")
    print(f"  이메일  : {email}")
    print(f"  관심분야: {interest}")
    print("=" * 40)
    print("프로필 등록이 완료되었습니다!")


if __name__ == "__main__":
    main()
```

이 예제의 핵심은 `get_validated_input()` 함수입니다. 이 함수는 다음 기능을 제공합니다:

- **검증 루프**: 올바른 입력이 들어올 때까지 반복합니다.
- **최대 시도 제한**: `max_attempts`로 무한 루프를 방지합니다.
- **예외 처리**: Ctrl+C(KeyboardInterrupt)나 EOF(파이프 입력 종료)를 처리합니다.
- **유연한 검증**: `validator` 매개변수로 어떤 검증 로직이든 전달할 수 있습니다.

**실행:**
```bash
$ python examples/python/chapter04/ex19_06_interactive_input.py
```

**결과 (사용자 입력 포함):**
```
========================================
  간단한 프로필 등록 프로그램
========================================

이름을 입력하세요: 홍길동
나이를 입력하세요 (1~150): 25
이메일을 입력하세요: hong@example.com

관심 분야를 선택하세요:
  1. 웹 개발
  2. 데이터 분석
  3. AI/ML
  4. 게임 개발
  5. 모바일 앱
번호를 입력하세요 (1~5): 3

========================================
  등록된 프로필 정보
========================================
  이름    : 홍길동
  나이    : 25세
  이메일  : hong@example.com
  관심분야: AI/ML
========================================
프로필 등록이 완료되었습니다!
```

잘못된 입력이 들어오면 검증이 동작합니다:
```
이름을 입력하세요:
  오류: 이름은 비어 있을 수 없습니다.
  (남은 시도: 2회)
이름을 입력하세요: 홍길동
```

> **Tip:** `argparse`의 명령줄 인자와 `input()`의 대화형 입력은 상황에 따라 조합하여 사용할 수 있습니다. 예를 들어 필수 인자는 명령줄로 받고, 추가 확인이 필요한 부분만 대화형으로 처리하는 것이 좋은 패턴입니다.

---

### 19.8 ANSI 색상으로 터미널 꾸미기

터미널 출력에 색상을 추가하면 정보를 더 쉽게 구분할 수 있습니다. 성공 메시지는 초록색, 오류 메시지는 빨간색, 경고는 노란색으로 표시하면 사용자가 한눈에 상태를 파악할 수 있습니다.

외부 라이브러리 없이 **ANSI 이스케이프 코드**를 직접 사용하면 됩니다.

**예제 19-7: ANSI 색상 출력**

```python
# examples/python/chapter04/ex19_07_ansi_colors.py
import sys


# ANSI 이스케이프 코드 상수
class Color:
    """ANSI 색상 코드 모음"""
    # 리셋
    RESET = "\033[0m"

    # 기본 전경색
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 밝은 전경색
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"

    # 스타일
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"

    # 배경색
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colorize(text, *styles):
    """텍스트에 ANSI 스타일을 적용합니다."""
    style_str = "".join(styles)
    return f"{style_str}{text}{Color.RESET}"
```

#### ANSI 이스케이프 코드의 구조

ANSI 코드는 `\033[` (ESC 문자 + `[`)로 시작하며, 숫자로 색상과 스타일을 지정합니다:

| 코드 | 효과 | 예 |
|------|------|-----|
| `\033[0m` | 리셋 (모든 스타일 해제) | 필수: 색상 적용 후 항상 리셋 |
| `\033[1m` | 굵게 | **굵은 텍스트** |
| `\033[2m` | 흐리게 | 흐린 텍스트 |
| `\033[4m` | 밑줄 | 밑줄 텍스트 |
| `\033[31m` | 빨간색 전경 | 빨간 텍스트 |
| `\033[32m` | 초록색 전경 | 초록 텍스트 |
| `\033[33m` | 노란색 전경 | 노란 텍스트 |
| `\033[41m` | 빨간색 배경 | 빨간 배경 |

`colorize()` 함수는 여러 스타일을 한 번에 적용할 수 있습니다:

```python
# 굵은 빨간색 텍스트
print(colorize("오류 발생!", Color.BOLD, Color.RED))

# 밑줄 파란색 텍스트
print(colorize("링크 텍스트", Color.UNDERLINE, Color.BLUE))
```

이 예제는 실행하면 다음과 같은 색상 데모를 보여줍니다:

**실행:**
```bash
$ python examples/python/chapter04/ex19_07_ansi_colors.py
```

**결과 (터미널에서 색상으로 표시됨):**
```
=== ANSI 색상 출력 데모 ===

[1] 기본 색상
  빨강  초록  노랑  파랑  마젠타  시안

[2] 밝은 색상
  밝은 빨강  밝은 초록  밝은 노랑  밝은 파랑  밝은 마젠타  밝은 시안

[3] 텍스트 스타일
  굵은 텍스트
  흐린 텍스트
  밑줄 텍스트
  반전 텍스트

[4] 스타일 조합
  굵은 빨강
  밑줄 파랑
  굵은 밑줄 초록

[5] 실용 예제: 로그 메시지
  [성공] 파일이 저장되었습니다.
  [경고] 디스크 공간이 부족합니다.
  [오류] 파일을 찾을 수 없습니다.
  [정보] 시스템이 시작되었습니다.
```

> **Warning:** ANSI 색상은 대부분의 터미널에서 지원되지만, Windows 구형 명령 프롬프트(cmd.exe)에서는 동작하지 않을 수 있습니다. Windows 10 이상의 Windows Terminal이나 PowerShell에서는 정상 동작합니다. 출력이 파이프로 리다이렉트될 때는 색상 코드를 비활성화하는 것이 좋습니다. `sys.stdout.isatty()`로 터미널 출력 여부를 확인할 수 있습니다.

---

### 19.9 진행률 바와 스피너

시간이 오래 걸리는 작업을 처리할 때 진행률 바나 스피너를 보여주면 사용자가 프로그램이 정상적으로 동작하고 있다는 것을 확인할 수 있습니다.

**예제 19-8: 프로그레스 바**

```python
# examples/python/chapter04/ex19_08_progress_bar.py
import sys
import time


def progress_bar(current, total, bar_length=40, prefix="진행"):
    """텍스트 기반 진행률 바를 출력합니다."""
    fraction = current / total
    filled = int(bar_length * fraction)
    bar = "█" * filled + "░" * (bar_length - filled)
    percent = fraction * 100
    sys.stdout.write(f"\r{prefix}: [{bar}] {percent:5.1f}% ({current}/{total})")
    sys.stdout.flush()


def spinner(duration=3, message="처리 중"):
    """회전 스피너 애니메이션을 표시합니다."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start = time.time()
    i = 0
    while time.time() - start < duration:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{frame} {message}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r✓ {message} 완료!   \n")
    sys.stdout.flush()


def countdown(seconds):
    """카운트다운을 표시합니다."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r카운트다운: {remaining}초 남음... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r카운트다운: 완료!          \n")
    sys.stdout.flush()


def multi_task_progress():
    """여러 작업의 진행률을 순차적으로 표시합니다."""
    tasks = [
        ("파일 검색", 30),
        ("데이터 분석", 50),
        ("결과 저장", 20),
    ]

    for task_name, steps in tasks:
        for i in range(steps + 1):
            progress_bar(i, steps, bar_length=30, prefix=f"{task_name:8s}")
            time.sleep(0.02)
        print("  ✓")
```

이 코드의 핵심은 **`\r` (캐리지 리턴)** 문자입니다. 줄바꿈(`\n`) 대신 `\r`을 사용하면 커서가 현재 줄의 맨 앞으로 돌아가서 같은 줄을 덮어쓰게 됩니다. 이 원리를 이용해 진행률이 업데이트되는 것처럼 보이게 합니다.

#### 핵심 기법 분석

**진행률 바의 원리:**
```python
sys.stdout.write(f"\r진행: [{bar}] {percent:5.1f}%")
sys.stdout.flush()
```

- `\r`: 커서를 줄 맨 앞으로 이동 (줄바꿈 없이)
- `sys.stdout.write()`: `print()`와 달리 자동 줄바꿈을 하지 않음
- `sys.stdout.flush()`: 출력 버퍼를 즉시 비워서 화면에 표시

**스피너의 원리:**
```python
frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
```

유니코드 점자 문자를 순서대로 출력하면 회전하는 것처럼 보입니다.

**실행:**
```bash
$ python examples/python/chapter04/ex19_08_progress_bar.py
```

**결과 (터미널에서 애니메이션으로 표시됨):**
```
============================================================
  진행률 표시 데모
============================================================

[1] 기본 진행률 바
진행: [████████████████████████████████████████] 100.0% (50/50)  완료!

[2] 스피너 애니메이션
✓ 데이터 로딩 완료!

[3] 카운트다운
카운트다운: 완료!

[4] 다중 작업 진행률
파일 검색  : [██████████████████████████████] 100.0% (30/30)  ✓
데이터 분석: [██████████████████████████████] 100.0% (50/50)  ✓
결과 저장  : [██████████████████████████████] 100.0% (20/20)  ✓

모든 데모가 완료되었습니다!
```

> **Tip:** 진행률 바는 작업의 전체 양을 알 때 사용하고, 스피너는 전체 양을 모를 때(예: 네트워크 요청 대기) 사용합니다. 두 가지를 적절히 조합하면 사용자 경험이 크게 향상됩니다.

---

### 19.10 실전 프로젝트 1: 파일 검색 도구

지금까지 배운 내용을 종합하여 실제로 유용한 파일 검색 CLI 도구를 만들어 봅시다. 이 도구는 디렉토리에서 파일 이름, 확장자, 크기 조건으로 파일을 검색하며, 정렬 기능도 제공합니다.

**예제 19-9: 파일 검색 도구**

```python
# examples/python/chapter04/ex19_09_file_search.py
import argparse
import os
import time


def format_size(size_bytes):
    """바이트를 읽기 좋은 크기 문자열로 변환합니다."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f}GB"


def search_files(directory, name=None, ext=None, min_size=None, max_size=None, recursive=True):
    """조건에 맞는 파일을 검색합니다."""
    results = []

    if recursive:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                if matches(filepath, filename, name, ext, min_size, max_size):
                    results.append(filepath)
    else:
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    if matches(filepath, filename, name, ext, min_size, max_size):
                        results.append(filepath)
        except PermissionError:
            print(f"경고: '{directory}' 접근 권한이 없습니다.")

    return results


def matches(filepath, filename, name, ext, min_size, max_size):
    """파일이 검색 조건에 맞는지 확인합니다."""
    if name and name.lower() not in filename.lower():
        return False
    if ext:
        target_ext = ext if ext.startswith(".") else f".{ext}"
        if not filename.lower().endswith(target_ext.lower()):
            return False
    try:
        size = os.path.getsize(filepath)
        if min_size is not None and size < min_size:
            return False
        if max_size is not None and size > max_size:
            return False
    except OSError:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="파일 검색 CLI 도구 — 이름, 확장자, 크기로 파일을 검색합니다.",
        epilog="사용 예: python ex19_09_file_search.py . --ext .py --name test"
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="검색할 디렉토리 (기본값: 현재 디렉토리)"
    )
    parser.add_argument("--name", "-n", type=str, help="파일 이름에 포함된 문자열")
    parser.add_argument("--ext", "-e", type=str, help="파일 확장자 (예: .py, .txt, .md)")
    parser.add_argument("--min-size", type=int, default=None, help="최소 파일 크기 (바이트)")
    parser.add_argument("--max-size", type=int, default=None, help="최대 파일 크기 (바이트)")
    parser.add_argument("--no-recursive", action="store_true", help="하위 디렉토리를 탐색하지 않음")
    parser.add_argument(
        "--sort",
        choices=["name", "size", "modified"],
        default="name",
        help="정렬 기준 (기본값: name)"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"오류: '{args.directory}'는 유효한 디렉토리가 아닙니다.")
        return

    # 검색 실행 및 결과 출력
    results = search_files(
        args.directory,
        name=args.name,
        ext=args.ext,
        min_size=args.min_size,
        max_size=args.max_size,
        recursive=not args.no_recursive
    )

    # 정렬
    if args.sort == "name":
        results.sort(key=lambda f: os.path.basename(f).lower())
    elif args.sort == "size":
        results.sort(key=lambda f: os.path.getsize(f))
    elif args.sort == "modified":
        results.sort(key=lambda f: os.path.getmtime(f), reverse=True)

    # 결과 출력
    total_size = 0
    for filepath in results:
        size = os.path.getsize(filepath)
        mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(filepath)))
        total_size += size
        rel_path = os.path.relpath(filepath, args.directory)
        print(f"  {format_size(size):>8s}  {mtime}  {rel_path}")

    print("-" * 60)
    print(f"검색 결과: {len(results)}개 파일 (총 {format_size(total_size)})")
```

이 도구는 지금까지 배운 여러 기법을 조합합니다:

- **위치 인자** (`directory`): `nargs="?"`로 선택적으로 만듦
- **선택 인자** (`--name`, `--ext`, `--min-size`, `--max-size`): 다양한 검색 조건
- **플래그 옵션** (`--no-recursive`): `action="store_true"`
- **choices** (`--sort`): 정렬 기준을 지정된 목록으로 제한
- **epilog**: 사용 예시를 도움말 하단에 표시

**실행 - Python 파일 검색:**
```bash
$ python examples/python/chapter04/ex19_09_file_search.py . --ext .py --name ex19
```

**결과:**
```
검색 디렉토리: /home/user/JoinUsForVibeCoding
검색 조건: 이름 포함: 'ex19', 확장자: .py
------------------------------------------------------------
    859B  2026-01-26 23:38  examples/python/chapter04/ex19_01_basic_argparse.py
   1.4KB  2026-01-26 23:38  examples/python/chapter04/ex19_02_required_optional.py
   2.0KB  2026-01-26 23:38  examples/python/chapter04/ex19_03_flag_options.py
   2.3KB  2026-01-26 23:38  examples/python/chapter04/ex19_04_subcommands.py
   ...
------------------------------------------------------------
검색 결과: 10개 파일 (총 18.5KB)
```

**실행 - 크기 기준으로 정렬:**
```bash
$ python examples/python/chapter04/ex19_09_file_search.py . --ext .md --sort size
```

**실행 - 특정 디렉토리만 검색 (하위 디렉토리 제외):**
```bash
$ python examples/python/chapter04/ex19_09_file_search.py examples/python/chapter04 --ext .py --no-recursive
```

> **Tip:** `os.walk()`는 디렉토리를 재귀적으로 탐색하는 강력한 함수입니다. `os.listdir()`은 현재 디렉토리의 항목만 반환합니다. 두 함수의 차이를 이해하면 파일 시스템 관련 도구를 효과적으로 만들 수 있습니다.

#### 설계 포인트

이 파일 검색 도구의 설계에서 주목할 점을 정리합니다:

| 설계 요소 | 구현 방법 | 이유 |
|-----------|-----------|------|
| 검색 로직 분리 | `search_files()`, `matches()` 함수 | 재사용성과 테스트 용이성 |
| 크기 포맷팅 | `format_size()` 함수 | 사람이 읽기 쉬운 형태로 변환 |
| 상대 경로 출력 | `os.path.relpath()` | 출력이 간결하고 이해하기 쉬움 |
| 에러 처리 | `PermissionError`, `OSError` 처리 | 접근 불가 파일을 건너뜀 |

---

### 19.11 실전 프로젝트 2: TODO CLI 앱

이 장의 마지막 예제로, 지금까지 배운 모든 기법을 종합한 **미니 할일(TODO) 관리 CLI 앱**을 만들어 봅시다. 이 앱은 서브커맨드, ANSI 색상, JSON 파일 저장, 우선순위 관리 등 실전에서 필요한 기능을 모두 갖추고 있습니다.

**예제 19-10: TODO CLI 앱**

```python
# examples/python/chapter04/ex19_10_todo_cli.py
import argparse
import json
import os
import sys
import time

# ANSI 색상 코드
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_RED = "\033[91m"
BRIGHT_YELLOW = "\033[93m"

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex19_10_todos.json")


def load_todos():
    """할일 목록을 JSON 파일에서 불러옵니다."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"next_id": 1, "todos": []}


def save_todos(data):
    """할일 목록을 JSON 파일에 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def colorize(text, color):
    """터미널 색상을 적용합니다."""
    if not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"
```

이 TODO 앱은 5개의 서브커맨드를 지원합니다:

#### 1) `add` - 할일 추가

```python
def cmd_add(args):
    """새 할일을 추가합니다."""
    data = load_todos()
    priority = getattr(args, "priority", "medium")

    todo = {
        "id": data["next_id"],
        "title": args.title,
        "done": False,
        "priority": priority,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "done_at": None,
    }
    data["todos"].append(todo)
    data["next_id"] += 1
    save_todos(data)

    priority_display = {"high": "높음", "medium": "보통", "low": "낮음"}
    print(colorize("✓ 할일이 추가되었습니다!", BRIGHT_GREEN))
    print(f"  ID: {todo['id']}")
    print(f"  제목: {todo['title']}")
    print(f"  우선순위: {priority_display.get(priority, priority)}")
```

#### 2) `list` - 할일 목록 조회

```python
def cmd_list(args):
    """할일 목록을 출력합니다."""
    data = load_todos()
    todos = data["todos"]

    show_all = getattr(args, "all", False)
    if not show_all:
        todos = [t for t in todos if not t["done"]]

    # 우선순위 순서로 정렬
    priority_order = {"high": 0, "medium": 1, "low": 2}
    todos.sort(key=lambda t: (t["done"], priority_order.get(t.get("priority", "medium"), 1)))

    # ... 색상과 함께 출력
```

#### 3) `done` - 할일 완료 처리

```python
def cmd_done(args):
    """할일을 완료 처리합니다."""
    data = load_todos()
    todo = find_todo(data, args.id)
    if todo is None:
        print(colorize(f"오류: ID {args.id}인 할일을 찾을 수 없습니다.", BRIGHT_RED))
        return
    todo["done"] = True
    todo["done_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_todos(data)
    print(colorize("✓ 할일이 완료되었습니다!", BRIGHT_GREEN))
```

#### 4) `delete` - 할일 삭제

#### 5) `clear` - 완료된 할일 일괄 삭제

전체 메인 함수에서는 이들을 서브커맨드로 등록합니다:

```python
def main():
    parser = argparse.ArgumentParser(
        description="미니 할일 관리 CLI — 할일을 추가, 조회, 완료, 삭제합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""사용 예:
  python ex19_10_todo_cli.py add "파이썬 공부하기"
  python ex19_10_todo_cli.py add "긴급 버그 수정" --priority high
  python ex19_10_todo_cli.py list
  python ex19_10_todo_cli.py list --all
  python ex19_10_todo_cli.py done 1
  python ex19_10_todo_cli.py delete 2
  python ex19_10_todo_cli.py clear"""
    )

    subparsers = parser.add_subparsers(dest="command", help="사용 가능한 명령어")

    # add
    sp_add = subparsers.add_parser("add", help="새 할일을 추가합니다")
    sp_add.add_argument("title", help="할일 제목")
    sp_add.add_argument(
        "--priority", "-p",
        choices=["high", "medium", "low"],
        default="medium",
        help="우선순위 (기본값: medium)"
    )
    sp_add.set_defaults(func=cmd_add)

    # list
    sp_list = subparsers.add_parser("list", help="할일 목록을 봅니다")
    sp_list.add_argument("--all", "-a", action="store_true", help="완료된 항목도 함께 표시")
    sp_list.set_defaults(func=cmd_list)

    # done
    sp_done = subparsers.add_parser("done", help="할일을 완료 처리합니다")
    sp_done.add_argument("id", type=int, help="완료할 할일 ID")
    sp_done.set_defaults(func=cmd_done)

    # delete
    sp_delete = subparsers.add_parser("delete", help="할일을 삭제합니다")
    sp_delete.add_argument("id", type=int, help="삭제할 할일 ID")
    sp_delete.set_defaults(func=cmd_delete)

    # clear
    sp_clear = subparsers.add_parser("clear", help="완료된 할일을 모두 삭제합니다")
    sp_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)
```

**실행 - 할일 추가:**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py add "파이썬 공부하기"
```

**결과:**
```
✓ 할일이 추가되었습니다!
  ID: 1
  제목: 파이썬 공부하기
  우선순위: 보통
```

**실행 - 높은 우선순위로 추가:**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py add "긴급 버그 수정" --priority high
```

**결과:**
```
✓ 할일이 추가되었습니다!
  ID: 2
  제목: 긴급 버그 수정
  우선순위: 높음
```

**실행 - 할일 목록 조회:**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py list
```

**결과:**
```
  할일 목록 (0/2 완료)
──────────────────────────────────────────────────
  ○   2. [높음] 긴급 버그 수정
  ○   1. [보통] 파이썬 공부하기
──────────────────────────────────────────────────
```

**실행 - 할일 완료:**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py done 2
```

**결과:**
```
✓ 할일이 완료되었습니다!
  [2] 긴급 버그 수정
```

**실행 - 전체 목록 조회 (완료 포함):**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py list --all
```

**결과:**
```
  할일 목록 (1/2 완료)
──────────────────────────────────────────────────
  ○   1. [보통] 파이썬 공부하기
  ✓   2. [높음] 긴급 버그 수정
──────────────────────────────────────────────────
```

**실행 - 완료된 할일 일괄 삭제:**
```bash
$ python examples/python/chapter04/ex19_10_todo_cli.py clear
```

**결과:**
```
✓ 완료된 할일 1개가 삭제되었습니다.
```

> **Note:** 이 TODO 앱에서 `sys.stdout.isatty()`를 사용하여 파이프 환경에서는 ANSI 색상을 자동으로 비활성화합니다. 이렇게 하면 `python todo_cli.py list > output.txt`처럼 파일로 리다이렉트할 때 깨진 색상 코드가 포함되지 않습니다.

#### 이 프로젝트에서 사용된 기법 총정리

| 기법 | 섹션 | 적용 |
|------|------|------|
| argparse 기본 | 19.2 | 파서 생성 및 인자 정의 |
| 위치 인자 | 19.3 | `title`, `id` |
| 선택 인자 | 19.3 | `--priority` |
| 플래그 옵션 | 19.4 | `--all` |
| 서브커맨드 | 19.5 | add, list, done, delete, clear |
| choices 검증 | 19.6 | `--priority`의 high/medium/low |
| ANSI 색상 | 19.8 | 성공/오류 메시지 색상 |
| JSON 저장 | - | 데이터 영속화 |
| epilog | - | 사용 예시 도움말 |
| formatter_class | - | RawDescriptionHelpFormatter |

---

### 19.12 CLI 도구 설계 베스트 프랙티스

이 장에서 배운 내용을 바탕으로, 좋은 CLI 도구를 만들기 위한 실전 가이드를 정리합니다.

#### 1) 명확한 도움말 제공

```python
parser = argparse.ArgumentParser(
    description="프로그램이 무엇을 하는지 간결하게 설명",
    epilog="사용 예:\n  python tool.py --input data.csv --output result.json"
)
```

모든 인자에 `help` 매개변수를 추가하세요.

#### 2) 합리적인 기본값 설정

사용자가 아무 옵션 없이 실행해도 유용한 동작을 하도록 기본값을 설정하세요:

```python
parser.add_argument("path", nargs="?", default=".", help="경로 (기본값: 현재 디렉토리)")
parser.add_argument("--encoding", default="utf-8", help="인코딩 (기본값: utf-8)")
```

#### 3) 오류 메시지를 명확하게

사용자가 잘못된 입력을 했을 때 무엇이 잘못되었고 어떻게 고쳐야 하는지 알려주세요:

```python
# 나쁜 예
parser.error("잘못된 입력")

# 좋은 예
parser.error(f"점수는 0~100 사이여야 합니다. (입력값: {args.score})")
```

#### 4) 종료 코드 사용

성공/실패를 종료 코드로 알려주면 다른 스크립트에서 활용할 수 있습니다:

```python
import sys

if error_occurred:
    print("오류 메시지", file=sys.stderr)
    sys.exit(1)  # 실패

sys.exit(0)  # 성공
```

#### 5) 파이프 친화적 설계

출력이 파이프로 연결될 수 있음을 고려하세요:

```python
import sys

# 터미널이면 색상 출력, 파이프면 일반 텍스트
if sys.stdout.isatty():
    print("\033[32m성공\033[0m")
else:
    print("성공")
```

---

### 정리

이 장에서 우리는 파이썬 표준 라이브러리만으로 완성도 높은 CLI 도구를 만드는 방법을 배웠습니다.

| 주제 | 핵심 내용 |
|------|-----------|
| **argparse 기본** | `ArgumentParser`, `add_argument`, `parse_args` |
| **인자 유형** | 위치 인자(필수), 선택 인자(`--`), 플래그(`action="store_true"`) |
| **상호 배타적 그룹** | `add_mutually_exclusive_group()`으로 동시 사용 방지 |
| **서브커맨드** | `add_subparsers()`로 git/docker 스타일의 CLI 구현 |
| **타입 검증** | `type`, `choices`, 커스텀 검증 함수, `parser.error()` |
| **대화형 입력** | `input()`, 검증 루프, 예외 처리 |
| **ANSI 색상** | 이스케이프 코드로 색상/스타일 적용 |
| **진행률 표시** | `\r`과 `sys.stdout`으로 진행률 바/스피너 구현 |
| **실전 도구** | 파일 검색 도구, TODO CLI 앱 |

바이브 코딩에서 CLI 도구를 만드는 것은 특히 효과적입니다. AI에게 "파일 이름을 일괄 변경하는 CLI 도구를 만들어줘"라고 요청하면, `argparse` 기반의 완성된 도구를 빠르게 얻을 수 있습니다. 이 장에서 배운 구조와 패턴을 이해하고 있으면, AI가 생성한 코드를 더 잘 이해하고 수정할 수 있습니다.

---

### 연습 문제

**연습 1: 단위 변환기 CLI**

`argparse`를 사용하여 단위 변환 CLI 도구를 만들어 보세요. 다음 기능을 포함해야 합니다:
- 위치 인자: 변환할 값 (숫자)
- `--from` 옵션: 원래 단위 (km, m, cm, mm)
- `--to` 옵션: 변환할 단위 (km, m, cm, mm)
- 잘못된 입력에 대한 오류 처리

```bash
# 사용 예
$ python converter.py 1500 --from m --to km
1500m = 1.5km
```

**연습 2: 파일 통계 도구**

파일이나 디렉토리의 통계를 보여주는 CLI 도구를 만들어 보세요:
- 서브커맨드: `count` (파일 수), `size` (총 크기), `types` (확장자별 분류)
- `--verbose` 플래그로 상세 정보 출력
- ANSI 색상으로 결과를 보기 좋게 표시

```bash
# 사용 예
$ python filestats.py count ./project --ext .py
Python 파일 수: 42개

$ python filestats.py types ./project
.py   : 42개 (68%)
.md   : 12개 (19%)
.json :  8개 (13%)
```

**연습 3: TODO 앱 확장**

예제 19-10의 TODO CLI 앱에 다음 기능을 추가해 보세요:
- `edit` 서브커맨드: 기존 할일의 제목을 수정
- `search` 서브커맨드: 키워드로 할일 검색
- `stats` 서브커맨드: 완료율, 우선순위별 통계 출력
- 마감일(`--due`) 옵션 추가: 마감일이 지난 항목을 빨간색으로 표시

> **Tip:** 연습 문제가 어렵게 느껴진다면, AI에게 "단위 변환 CLI 도구를 argparse로 만들어줘"라고 요청해 보세요. 생성된 코드를 이 장에서 배운 내용과 비교하며 학습하는 것도 좋은 방법입니다. 이것이 바로 바이브 코딩의 장점입니다!
