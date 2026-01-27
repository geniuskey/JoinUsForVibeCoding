# Chapter 15: 파일 처리 자동화

프로그래밍에서 파일을 다루는 것은 가장 기본적이면서도 가장 자주 사용하는 기술입니다. 데이터를 읽고, 결과를 저장하고, 디렉토리를 정리하고, 백업을 만드는 모든 작업이 파일 처리에서 시작됩니다. 이번 챕터에서는 파이썬으로 파일을 자유자재로 다루는 방법을 배웁니다. 텍스트 파일부터 CSV, JSON까지, 그리고 디렉토리 탐색과 일괄 처리 자동화까지 실전에서 바로 활용할 수 있는 기술을 익혀봅시다.

---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- 텍스트 파일을 다양한 방법으로 읽고 쓸 수 있다
- 파일 열기 모드(r, w, a)의 차이를 이해하고 상황에 맞게 사용할 수 있다
- CSV와 JSON 형식의 파일을 읽고 쓸 수 있다
- os 모듈과 pathlib을 사용하여 디렉토리를 탐색할 수 있다
- glob 패턴으로 원하는 파일을 빠르게 찾을 수 있다
- 파일 메타데이터(크기, 수정일, 해시값)를 활용할 수 있다
- 파일 일괄 처리 자동화 스크립트를 작성할 수 있다
- 안전한 파일 처리 패턴(with 문, 백업)을 적용할 수 있다

---

## 15.1 파일 읽기의 다양한 방법

파일 읽기는 모든 파일 처리의 시작점입니다. 파이썬은 파일을 읽는 여러 가지 방법을 제공하며, 각 방법은 상황에 따라 장단점이 있습니다.

### 기본 파일 읽기: open()과 with 문

파이썬에서 파일을 열 때는 `open()` 함수를 사용합니다. 이때 반드시 `with` 문과 함께 사용하는 것이 좋습니다. `with` 문은 파일 작업이 끝나면 자동으로 파일을 닫아주기 때문에 실수로 파일을 닫지 않는 문제를 방지할 수 있습니다.

```python
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

> **Tip:** 한국어가 포함된 파일을 다룰 때는 반드시 `encoding="utf-8"`을 지정하세요. 인코딩을 생략하면 운영체제에 따라 글자가 깨질 수 있습니다.

### 네 가지 읽기 방법

예제 15-01은 파일을 읽는 네 가지 방법을 비교합니다. 각 방법의 특징과 적합한 상황을 이해하면 효율적인 코드를 작성할 수 있습니다.

**예제 15-01: 텍스트 파일 읽기**

```python
# examples/python/chapter04/ex15_01_read_text.py

# 방법 1: read() - 전체 내용을 한 번에 읽기
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 방법 2: readline() - 한 줄씩 읽기
with open(file_path, "r", encoding="utf-8") as f:
    line = f.readline()
    line_num = 1
    while line:
        print(f"[{line_num}줄] {line}", end="")
        line = f.readline()
        line_num += 1

# 방법 3: readlines() - 모든 줄을 리스트로 읽기
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(f"총 {len(lines)}줄이 있습니다.")
    for i, line in enumerate(lines):
        print(f"  lines[{i}] = {line.strip()!r}")

# 방법 4: for 루프로 한 줄씩 읽기 (권장)
with open(file_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.strip()}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_01_read_text.py
```

**결과:**

```
==================================================
방법 1: read() - 전체 내용을 한 번에 읽기
==================================================
안녕하세요, 바이브 코딩!
파이썬으로 파일을 다루는 법을 배워봅시다.
첫 번째 줄입니다.
두 번째 줄입니다.
세 번째 줄입니다.
파일 처리는 프로그래밍의 기본입니다.

==================================================
방법 2: readline() - 한 줄씩 읽기
==================================================
[1줄] 안녕하세요, 바이브 코딩!
[2줄] 파이썬으로 파일을 다루는 법을 배워봅시다.
[3줄] 첫 번째 줄입니다.
[4줄] 두 번째 줄입니다.
[5줄] 세 번째 줄입니다.
[6줄] 파일 처리는 프로그래밍의 기본입니다.

==================================================
방법 3: readlines() - 모든 줄을 리스트로 읽기
==================================================
총 6줄이 있습니다.
  lines[0] = '안녕하세요, 바이브 코딩!'
  lines[1] = '파이썬으로 파일을 다루는 법을 배워봅시다.'
  lines[2] = '첫 번째 줄입니다.'
  lines[3] = '두 번째 줄입니다.'
  lines[4] = '세 번째 줄입니다.'
  lines[5] = '파일 처리는 프로그래밍의 기본입니다.'

==================================================
방법 4: for 루프로 한 줄씩 읽기 (권장)
==================================================
  1: 안녕하세요, 바이브 코딩!
  2: 파이썬으로 파일을 다루는 법을 배워봅시다.
  3: 첫 번째 줄입니다.
  4: 두 번째 줄입니다.
  5: 세 번째 줄입니다.
  6: 파일 처리는 프로그래밍의 기본입니다.

모든 읽기 방법을 성공적으로 실행했습니다!
```

### 읽기 방법 비교 정리

| 방법 | 반환값 | 메모리 | 적합한 상황 |
|------|--------|--------|-------------|
| `read()` | 전체 문자열 | 높음 | 작은 파일, 전체 내용 필요 |
| `readline()` | 한 줄 문자열 | 낮음 | 특정 줄까지만 읽을 때 |
| `readlines()` | 줄 리스트 | 높음 | 줄 번호로 접근할 때 |
| `for` 루프 | 한 줄씩 반복 | 낮음 | **대부분의 상황 (권장)** |

> **Tip:** 대용량 파일을 다룰 때는 `read()`나 `readlines()` 대신 **`for` 루프**를 사용하세요. 파일을 한 줄씩 읽어 처리하기 때문에 메모리를 효율적으로 사용합니다. 수 GB 크기의 로그 파일도 문제없이 처리할 수 있습니다.

---

## 15.2 파일 쓰기와 모드

파일에 데이터를 저장하는 것은 프로그램의 결과를 영구적으로 보관하는 핵심 작업입니다. 파이썬의 파일 열기 모드를 정확히 이해하면, 데이터를 안전하게 기록할 수 있습니다.

### 쓰기 모드의 이해

예제 15-02는 쓰기 모드(`w`)와 추가 모드(`a`)의 차이를 명확하게 보여줍니다.

**예제 15-02: 텍스트 파일 쓰기**

```python
# examples/python/chapter04/ex15_02_write_text.py

# 쓰기 모드 (w): 새로 작성 - 기존 내용이 사라집니다!
with open(file_path, "w", encoding="utf-8") as f:
    f.write("첫 번째 줄을 작성합니다.\n")
    f.write("두 번째 줄을 작성합니다.\n")
    f.write("세 번째 줄을 작성합니다.\n")

# 추가 모드 (a): 기존 내용 뒤에 추가
with open(file_path, "a", encoding="utf-8") as f:
    f.write("추가된 첫 번째 줄입니다.\n")
    f.write("추가된 두 번째 줄입니다.\n")

# writelines()로 여러 줄 한번에 쓰기
lines = ["가\n", "나\n", "다\n", "라\n", "마\n"]
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_02_write_text.py
```

**결과:**

```
==================================================
1단계: 쓰기 모드(w)로 파일 생성
==================================================
[현재 파일 내용]
첫 번째 줄을 작성합니다.
두 번째 줄을 작성합니다.
세 번째 줄을 작성합니다.

==================================================
2단계: 쓰기 모드(w)로 다시 열면 기존 내용이 사라집니다
==================================================
[현재 파일 내용]
완전히 새로운 내용으로 교체되었습니다.

==================================================
3단계: 추가 모드(a)로 내용 덧붙이기
==================================================
[현재 파일 내용]
완전히 새로운 내용으로 교체되었습니다.
추가된 첫 번째 줄입니다.
추가된 두 번째 줄입니다.

==================================================
4단계: writelines()로 리스트 한번에 쓰기
==================================================
[현재 파일 내용]
가
나
다
라
마

==================================================
파일 열기 모드 요약
==================================================
  'r'  : 읽기 전용 (파일이 없으면 오류)
  'w'  : 쓰기 전용 (파일이 없으면 생성, 있으면 덮어쓰기)
  'a'  : 추가 전용 (파일이 없으면 생성, 있으면 끝에 추가)
  'r+' : 읽기+쓰기 (파일이 없으면 오류)
  'w+' : 쓰기+읽기 (파일이 없으면 생성, 있으면 덮어쓰기)
  'a+' : 추가+읽기 (파일이 없으면 생성, 있으면 끝에 추가)

파일 쓰기 예제를 성공적으로 완료했습니다!
```

> **Warning:** 쓰기 모드(`"w"`)로 파일을 열면 **기존 내용이 모두 삭제**됩니다. 중요한 데이터가 있는 파일을 `"w"` 모드로 열기 전에 반드시 백업하세요. 기존 내용을 유지하면서 추가하고 싶다면 추가 모드(`"a"`)를 사용하세요.

### 구조화된 데이터 파일: CSV

텍스트 파일 외에도 프로그래밍에서 자주 다루는 파일 형식이 있습니다. 그중 CSV(Comma-Separated Values)는 표 형태의 데이터를 저장하는 가장 간단한 형식입니다.

**예제 15-03: CSV 파일 읽기/쓰기**

```python
# examples/python/chapter04/ex15_03_csv_files.py
import csv

# CSV 파일 쓰기
students = [
    ["이름", "나이", "점수", "학과"],
    ["김민수", 22, 95, "컴퓨터공학"],
    ["이서연", 21, 88, "디자인"],
    ["박지훈", 23, 92, "경영학"],
    ["최예진", 20, 97, "수학"],
    ["정도현", 22, 85, "물리학"],
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(students)

# DictReader로 읽기 (딕셔너리 형태)
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['이름']}님 - 나이: {row['나이']}, 점수: {row['점수']}")

# DictWriter로 쓰기 (딕셔너리 형태)
products = [
    {"상품명": "노트북", "가격": 1200000, "재고": 15},
    {"상품명": "마우스", "가격": 35000, "재고": 120},
]
fieldnames = ["상품명", "가격", "재고"]
with open(csv_path2, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_03_csv_files.py
```

**결과:**

```
==================================================
1단계: CSV 파일 쓰기
==================================================
CSV 파일이 생성되었습니다: students.csv
총 5명의 학생 데이터를 저장했습니다.

==================================================
2단계: CSV 파일 읽기 (csv.reader)
==================================================
  헤더: ['이름', '나이', '점수', '학과']
  데이터: ['김민수', '22', '95', '컴퓨터공학']
  데이터: ['이서연', '21', '88', '디자인']
  데이터: ['박지훈', '23', '92', '경영학']
  데이터: ['최예진', '20', '97', '수학']
  데이터: ['정도현', '22', '85', '물리학']

==================================================
5단계: CSV 데이터 통계 계산
==================================================
  학생 수: 5명
  평균 점수: 91.4
  최고 점수: 97
  최저 점수: 85

CSV 파일 처리 예제를 성공적으로 완료했습니다!
```

> **Tip:** CSV 파일을 쓸 때 Windows에서는 `newline=""`을 반드시 지정해야 합니다. 그렇지 않으면 줄 사이에 빈 줄이 삽입되는 문제가 발생합니다.

### 구조화된 데이터 파일: JSON

JSON(JavaScript Object Notation)은 웹 API와 설정 파일에서 가장 많이 사용되는 데이터 형식입니다. 파이썬의 딕셔너리/리스트와 구조가 거의 같아서 다루기 매우 편리합니다.

**예제 15-04: JSON 파일 읽기/쓰기**

```python
# examples/python/chapter04/ex15_04_json_files.py
import json

# JSON 파일 쓰기
config = {
    "앱_이름": "바이브 코딩 도우미",
    "버전": "2.1.0",
    "설정": {
        "테마": "다크",
        "언어": "한국어",
        "자동저장": True,
        "글꼴_크기": 14
    },
    "최근_파일": ["project_a.py", "project_b.py", "notes.md"]
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# JSON 파일 읽기
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(f"  앱 이름: {loaded['앱_이름']}")
print(f"  테마: {loaded['설정']['테마']}")

# Python 객체를 JSON 문자열로 변환
json_str = json.dumps(user_data, ensure_ascii=False, indent=2)

# JSON 문자열을 Python 객체로 변환
json_input = '{"도시": "서울", "인구": 9700000, "수도": true}'
parsed = json.loads(json_input)
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_04_json_files.py
```

**결과:**

```
==================================================
1단계: JSON 파일 쓰기
==================================================
config.json 파일이 생성되었습니다.

==================================================
2단계: JSON 파일 읽기
==================================================
  앱 이름: 바이브 코딩 도우미
  버전: 2.1.0
  테마: 다크
  언어: 한국어
  자동저장: True
  최근 파일: project_a.py, project_b.py, notes.md

==================================================
4단계: json.loads()로 문자열 파싱
==================================================
  원본 문자열: {"도시": "서울", "인구": 9700000, "수도": true}
  파싱 결과: {'도시': '서울', '인구': 9700000, '수도': True}
  도시: 서울, 인구: 9,700,000명

JSON 파일 처리 예제를 성공적으로 완료했습니다!
```

> **Tip:** JSON에서 한국어를 사용할 때는 `ensure_ascii=False`를 반드시 넣어야 합니다. 이 옵션이 없으면 한국어가 `\uD55C\uAE00` 같은 유니코드 이스케이프로 저장되어 읽기 어려워집니다.

### json.dump()와 json.dumps()의 차이

| 함수 | 용도 | 대상 |
|------|------|------|
| `json.dump()` | 파일에 저장 | 파일 객체 |
| `json.dumps()` | 문자열로 변환 | 메모리(변수) |
| `json.load()` | 파일에서 읽기 | 파일 객체 |
| `json.loads()` | 문자열에서 파싱 | 문자열 변수 |

함수 이름 끝의 `s`는 **string**을 의미합니다. `s`가 붙으면 문자열과 관련된 작업, 없으면 파일과 관련된 작업이라고 기억하면 편합니다.

---

## 15.3 디렉토리 탐색

파일 하나를 다루는 것을 넘어서, 디렉토리 전체를 탐색하고 처리하는 방법을 배워봅시다. 파이썬은 디렉토리를 탐색하는 여러 도구를 제공합니다.

### 현재 디렉토리 파일 목록 조회

예제 15-05는 디렉토리 내 파일 목록을 확인하는 세 가지 방법을 비교합니다. 전통적인 `os` 모듈과 현대적인 `pathlib` 모듈을 모두 다룹니다.

**예제 15-05: 디렉토리 내 파일 목록 조회**

```python
# examples/python/chapter04/ex15_05_list_directory.py
import os
from pathlib import Path

# 방법 1: os.listdir() - 간단하지만 이름만 반환
items = os.listdir(sample_dir)
for item in sorted(items):
    full_path = os.path.join(sample_dir, item)
    item_type = "디렉토리" if os.path.isdir(full_path) else "파일"
    print(f"  [{item_type:>4s}] {item}")

# 방법 2: os.scandir() - 더 효율적, 메타데이터 포함
with os.scandir(sample_dir) as entries:
    for entry in sorted(entries, key=lambda e: e.name):
        entry_type = "디렉토리" if entry.is_dir() else "파일"
        if entry.is_file():
            size = entry.stat().st_size
            print(f"  [{entry_type:>4s}] {entry.name} ({size} bytes)")

# 방법 3: pathlib.Path.iterdir() - 현대적 방법 (권장)
project_path = Path(sample_dir)
for item in project_path.iterdir():
    if item.is_file():
        print(f"  {item.name} (확장자: {item.suffix or '없음'})")
    elif item.is_dir():
        print(f"  {item.name}/")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_05_list_directory.py
```

**결과:**

```
==================================================
방법 1: os.listdir()
==================================================
항목 수: 11
  [디렉토리] docs/
  [디렉토리] src/
  [디렉토리] tests/
  [  파일] .gitignore
  [  파일] README.md
  [  파일] config.json
  [  파일] data.csv
  [  파일] main.py
  [  파일] requirements.txt
  [  파일] test_main.py
  [  파일] utils.py

==================================================
방법 3: pathlib.Path.iterdir() (현대적 방법)
==================================================
디렉토리: 3개
파일: 8개

파이썬 파일만 필터링
==================================================
Python 파일 (3개):
  main.py
  test_main.py
  utils.py

디렉토리 탐색 예제를 성공적으로 완료했습니다!
```

### os 모듈 vs pathlib: 어떤 것을 사용할까?

| 기능 | os 모듈 | pathlib |
|------|---------|---------|
| 경로 결합 | `os.path.join(a, b)` | `Path(a) / b` |
| 파일 목록 | `os.listdir()` | `path.iterdir()` |
| 파일 존재 확인 | `os.path.exists()` | `path.exists()` |
| 확장자 확인 | `os.path.splitext()` | `path.suffix` |
| 파일 이름 | `os.path.basename()` | `path.name` |
| 디렉토리 확인 | `os.path.isdir()` | `path.is_dir()` |

> **Tip:** 새 프로젝트에서는 `pathlib`을 사용하는 것을 권장합니다. 객체 지향적이고 직관적인 문법 덕분에 코드가 훨씬 읽기 좋아집니다. 특히 경로를 `/` 연산자로 결합하는 것이 `os.path.join()`보다 깔끔합니다.

### 재귀적 파일 탐색: 하위 디렉토리까지

실제 프로젝트에서는 하위 디렉토리를 포함하여 모든 파일을 탐색해야 할 때가 많습니다. `os.walk()`와 `pathlib.rglob()`이 이 작업을 처리합니다.

**예제 15-06: 재귀적 파일 탐색**

```python
# examples/python/chapter04/ex15_06_recursive_walk.py
import os
from pathlib import Path

# 방법 1: os.walk() - 전통적 방법
for dirpath, dirnames, filenames in os.walk(project):
    rel_dir = os.path.relpath(dirpath, project)
    level = rel_dir.count(os.sep)
    indent = "  " * level
    dir_name = os.path.basename(dirpath)
    print(f"{indent}[{dir_name}/]")
    for filename in sorted(filenames):
        print(f"{indent}  {filename}")

# 방법 2: pathlib.rglob() - 모든 파일 재귀 탐색
project_path = Path(project)
all_files = sorted(project_path.rglob("*"))
for item in all_files:
    rel = item.relative_to(project_path)
    if item.is_dir():
        print(f"  [DIR]  {rel}/")
    else:
        print(f"  [FILE] {rel}")

# 특정 확장자 파일만 재귀적으로 찾기
python_files = sorted(project_path.rglob("*.py"))
print(f"Python 파일 ({len(python_files)}개):")
for pf in python_files:
    print(f"  {pf.relative_to(project_path)}")

# os.walk()에서 특정 디렉토리 제외하기
exclude_dirs = {"tests", "docs"}
for dirpath, dirnames, filenames in os.walk(project):
    dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
    for filename in sorted(filenames):
        print(f"  {os.path.relpath(os.path.join(dirpath, filename), project)}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_06_recursive_walk.py
```

**결과:**

```
==================================================
방법 1: os.walk()로 모든 파일 탐색
==================================================
[web_project/]
  app.js
  index.html
  style.css
  [src/]
    main.py
    utils.py
    [models/]
      product.py
      user.py
  [tests/]
    test_main.py
    test_utils.py
  [docs/]
    api.md
    guide.md
  [data/]
    config.json
    users.csv

총 디렉토리: 5개, 총 파일: 12개

==================================================
Python 파일만 재귀적으로 찾기 (rglob)
==================================================
Python 파일 (6개):
  src/main.py
  src/utils.py
  src/models/product.py
  src/models/user.py
  tests/test_main.py
  tests/test_utils.py

재귀적 파일 탐색 예제를 성공적으로 완료했습니다!
```

> **Tip:** `os.walk()`에서 `dirnames[:] = [...]`처럼 **슬라이스 할당**을 사용하면 탐색 대상에서 특정 디렉토리를 아예 제외할 수 있습니다. `.git`이나 `__pycache__` 같은 디렉토리를 건너뛰고 싶을 때 유용합니다.

---

## 15.4 파일 패턴 매칭과 glob

디렉토리에서 특정 조건에 맞는 파일만 찾고 싶을 때 glob 패턴을 사용합니다. 와일드카드 문자를 활용하여 원하는 파일을 빠르게 필터링할 수 있습니다.

### glob 패턴 기본 문법

| 패턴 | 의미 | 예시 |
|------|------|------|
| `*` | 모든 문자열 (슬래시 제외) | `*.py` -- 모든 파이썬 파일 |
| `?` | 한 글자 | `file?.txt` -- file1.txt, fileA.txt |
| `[abc]` | 대괄호 안의 문자 중 하나 | `[abc].py` -- a.py, b.py, c.py |
| `**` | 모든 하위 디렉토리 (재귀) | `**/*.py` -- 모든 하위의 .py 파일 |

### 확장자별 파일 분류

예제 15-07은 glob과 `pathlib`을 활용하여 디렉토리 내 파일을 확장자별로 그룹화하고 통계를 보여줍니다.

**예제 15-07: 확장자별 파일 분류**

```python
# examples/python/chapter04/ex15_07_classify_by_ext.py
from pathlib import Path
from collections import defaultdict

ext_groups = defaultdict(list)
project_path = Path(project_dir)

for file_path in project_path.iterdir():
    if file_path.is_file():
        ext = file_path.suffix.lower() if file_path.suffix else "(확장자 없음)"
        size = file_path.stat().st_size
        ext_groups[ext].append((file_path.name, size))

# 카테고리별 분류
categories = {
    "코드": [".py", ".js"],
    "웹": [".html", ".css"],
    "데이터": [".json", ".csv", ".txt"],
    "문서": [".md"],
    "이미지": [".png", ".jpg", ".svg"],
}

for category, extensions in categories.items():
    cat_files = []
    for ext in extensions:
        if ext in ext_groups:
            cat_files.extend(ext_groups[ext])
    if cat_files:
        cat_size = sum(s for _, s in cat_files)
        pct = (len(cat_files) / total_files) * 100
        print(f"  {category:>6s}: {len(cat_files):>2}개 ({pct:5.1f}%)")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_07_classify_by_ext.py
```

**결과:**

```
==================================================
확장자별 파일 분류 결과
==================================================

  .py 파일 (4개, 7,680 bytes)
  ----------------------------------------
    main.py                  3,400 bytes
    report.py                1,200 bytes
    test_main.py             2,100 bytes
    utils.py                   980 bytes

  .html 파일 (2개, 8,800 bytes)
  ----------------------------------------
    about.html               3,200 bytes
    index.html               5,600 bytes

  .js 파일 (2개, 3,800 bytes)
  ----------------------------------------
    app.js                   2,700 bytes
    helpers.js               1,100 bytes

==================================================
통계 요약
==================================================
  총 파일 수: 20개
  총 크기: 126,690 bytes (123.7 KB)
  확장자 종류: 10가지

카테고리별 분류:
    코드:  6개 ( 30.0%)
     웹:  4개 ( 20.0%)
  데이터:  4개 ( 20.0%)
    문서:  2개 ( 10.0%)
  이미지:  4개 ( 20.0%)

확장자별 파일 분류 예제를 성공적으로 완료했습니다!
```

> **Tip:** `defaultdict(list)`를 사용하면 키가 존재하지 않을 때 자동으로 빈 리스트를 생성해줍니다. 파일을 그룹화할 때 매우 편리합니다. `if key not in dict:` 같은 확인 코드를 쓸 필요가 없습니다.

---

## 15.5 파일 메타데이터 활용

파일의 내용뿐 아니라, 파일 자체의 정보(크기, 수정일, 해시값 등)도 프로그래밍에서 중요하게 활용됩니다. 파일 메타데이터를 활용하면 중복 파일을 찾거나, 최근 수정된 파일을 확인하거나, 파일의 무결성을 검증할 수 있습니다.

### 파일 정보 확인하기

`pathlib`의 `stat()` 메서드를 사용하면 파일의 다양한 정보를 확인할 수 있습니다.

```python
from pathlib import Path
from datetime import datetime

file_path = Path("example.py")
stat = file_path.stat()

print(f"파일 크기: {stat.st_size} bytes")
print(f"수정 시간: {datetime.fromtimestamp(stat.st_mtime)}")
print(f"생성 시간: {datetime.fromtimestamp(stat.st_ctime)}")
print(f"확장자: {file_path.suffix}")
print(f"파일 이름(확장자 제외): {file_path.stem}")
```

### 해시값으로 중복 파일 찾기

예제 15-09는 파일 크기와 SHA-256 해시값을 비교하여 내용이 동일한 중복 파일을 자동으로 찾습니다. 이름이 다르더라도 내용이 같으면 중복으로 판별합니다.

**예제 15-09: 중복 파일 찾기**

```python
# examples/python/chapter04/ex15_09_find_duplicates.py
import hashlib
from pathlib import Path
from collections import defaultdict

def get_file_hash(filepath, algorithm="sha256"):
    """파일의 해시값을 계산합니다."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# 1단계: 파일 크기별 그룹화 (빠른 사전 필터링)
size_groups = defaultdict(list)
for f in test_path.iterdir():
    if f.is_file():
        size = f.stat().st_size
        size_groups[size].append(f)

# 같은 크기의 파일이 2개 이상인 그룹만 필터
potential_dupes = {
    size: files for size, files in size_groups.items()
    if len(files) >= 2
}

# 2단계: 해시값으로 정확한 중복 확인
hash_groups = defaultdict(list)
for size, files in potential_dupes.items():
    for f in files:
        file_hash = get_file_hash(f)
        hash_groups[file_hash].append(f)

duplicates = {
    h: files for h, files in hash_groups.items()
    if len(files) >= 2
}
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_09_find_duplicates.py
```

**결과:**

```
============================================================
중복 파일 찾기
============================================================

검사 대상: 10개 파일

------------------------------------------------------------
1단계: 파일 크기별 그룹화
------------------------------------------------------------
  같은 크기의 파일 그룹: 3개

------------------------------------------------------------
2단계: 해시값(SHA-256)으로 정확한 중복 확인
------------------------------------------------------------

============================================================
중복 파일 검사 결과
============================================================

  중복 그룹 1:
  해시: a1b2c3d4e5f6...
  크기: 50 bytes
    (원본) report_final.txt
    (중복) report_copy.txt
    (중복) report_backup.txt

  중복 그룹 2:
  해시: f6e5d4c3b2a1...
  크기: 32 bytes
    (원본) memo.txt
    (중복) meeting_notes.txt

  ========================================
  중복 그룹 수: 3
  중복 파일 수: 5개
  낭비 공간: 214 bytes

중복 파일 찾기 예제를 성공적으로 완료했습니다!
```

> **Tip:** 중복 파일을 찾을 때 **2단계 전략**을 사용하면 효율적입니다. 먼저 파일 크기로 빠르게 후보군을 줄이고, 크기가 같은 파일에 대해서만 해시값을 계산합니다. 해시 계산은 파일 전체를 읽어야 하므로 비용이 크기 때문에, 이 사전 필터링이 성능에 큰 차이를 만듭니다.

---

## 15.6 일괄 처리 패턴

지금까지 배운 파일 읽기, 쓰기, 디렉토리 탐색 기술을 조합하면 강력한 자동화 스크립트를 만들 수 있습니다. 이 섹션에서는 실전에서 자주 사용하는 일괄 처리 패턴을 살펴봅니다.

### 파일 일괄 이름변경

예제 15-08은 여러 파일의 이름을 규칙에 따라 한꺼번에 변경하는 방법을 보여줍니다. 실수를 방지하기 위해 먼저 시뮬레이션을 수행하는 패턴이 핵심입니다.

**예제 15-08: 파일 일괄 이름변경 (시뮬레이션)**

```python
# examples/python/chapter04/ex15_08_batch_rename.py
from pathlib import Path
import re

# 패턴 1: 접두사 추가
prefix = "여행_"
for f in sorted(photo_path.iterdir()):
    new_name = prefix + f.name
    print(f"  {f.name:>35s}  -->  {new_name}")

# 패턴 2: 공백 및 특수문자를 밑줄로 교체
for f in sorted(photo_path.iterdir()):
    new_name = re.sub(r'[\s()\[\]]+', '_', f.stem)
    new_name = re.sub(r'_+', '_', new_name)  # 중복 밑줄 제거
    new_name = new_name.strip('_') + f.suffix

# 패턴 3: 순번으로 일괄 변경
base_name = "travel_photo"
for i, f in enumerate(files_sorted, start=1):
    new_name = f"{base_name}_{i:03d}{f.suffix}"
    print(f"  {f.name:>35s}  -->  {new_name}")

# 실제 적용시 사용할 함수
def batch_rename(directory, pattern_func, dry_run=True):
    """파일 일괄 이름변경 함수"""
    target = Path(directory)
    changes = []
    for f in sorted(target.iterdir()):
        if f.is_file():
            new_name = pattern_func(f)
            if new_name != f.name:
                changes.append((f, f.parent / new_name))
    for old, new in changes:
        if dry_run:
            print(f"  [시뮬레이션] {old.name} --> {new.name}")
        else:
            old.rename(new)
            print(f"  [완료] {old.name} --> {new.name}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_08_batch_rename.py
```

**결과:**

```
==================================================
패턴 1: 접두사 추가 (시뮬레이션)
==================================================
     DSC_1001.png  -->  여행_DSC_1001.png
     DSC_1002.png  -->  여행_DSC_1002.png
  IMG_20240315_001.jpg  -->  여행_IMG_20240315_001.jpg
  IMG_20240315_002.jpg  -->  여행_IMG_20240315_002.jpg
  IMG_20240316_001.jpg  -->  여행_IMG_20240316_001.jpg

==================================================
패턴 2: 공백 및 특수문자를 밑줄로 교체 (시뮬레이션)
==================================================
  Screenshot 2024-03-15.png  -->  Screenshot_2024-03-15.png
            photo (1).jpg  -->  photo_1.jpg
            photo (2).jpg  -->  photo_2.jpg

==================================================
패턴 3: 순번으로 일괄 변경 (시뮬레이션)
==================================================
     DSC_1001.png  -->  travel_photo_001.png
     DSC_1002.png  -->  travel_photo_002.png
  IMG_20240315_001.jpg  -->  travel_photo_003.jpg

파일 일괄 이름변경 시뮬레이션 예제를 성공적으로 완료했습니다!
```

> **Warning:** 파일 이름을 일괄 변경할 때는 반드시 `dry_run=True`로 **시뮬레이션을 먼저 실행**하세요. 변경 결과를 눈으로 확인한 뒤에 `dry_run=False`로 실제 변경을 수행해야 합니다. 이름변경은 되돌리기가 어렵습니다.

### 로그 파일 분석

예제 15-10은 파일 읽기와 정규표현식, 데이터 집계를 결합하여 로그 파일을 자동으로 분석하는 실전 예제입니다.

**예제 15-10: 로그 파일 분석기**

```python
# examples/python/chapter04/ex15_10_log_analyzer.py
import re
from collections import Counter, defaultdict

# 로그 패턴 정의 (정규표현식)
log_pattern = re.compile(
    r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+\[(\w+)\]\s+(.*)"
)

# 로그 파싱
entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        match = log_pattern.match(line)
        if match:
            date, time, level, message = match.groups()
            entries.append({
                "date": date, "time": time,
                "level": level, "message": message,
            })

# 로그 레벨별 통계
level_counts = Counter(e["level"] for e in entries)
for level in ["CRITICAL", "ERROR", "WARNING", "INFO"]:
    count = level_counts.get(level, 0)
    pct = (count / len(entries)) * 100
    bar = "#" * int(pct)
    print(f"  {level:>10s}: {count:>3}개 ({pct:5.1f}%) {bar}")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_10_log_analyzer.py
```

**결과:**

```
============================================================
로그 파일 분석기
============================================================

총 로그 항목: 24개

------------------------------------------------------------
1. 로그 레벨별 통계
------------------------------------------------------------
  CRITICAL:   1개 (  4.2%) ####
     ERROR:   5개 ( 20.8%) ####################
   WARNING:   5개 ( 20.8%) ####################
      INFO:  13개 ( 54.2%) ######################################################

------------------------------------------------------------
2. 오류(ERROR) 상세 목록
------------------------------------------------------------
  [1] 08:04:12 - 파일을 찾을 수 없습니다: /data/config.yml
  [2] 08:06:45 - 데이터베이스 쿼리 실패: timeout
  [3] 08:09:00 - 인증 실패: 잘못된 토큰
  [4] 08:11:30 - 외부 API 호출 실패: connection refused
  [5] 08:13:30 - 파일 쓰기 실패: 권한 부족

------------------------------------------------------------
4. 심각(CRITICAL) 이벤트
------------------------------------------------------------
  *** 08:10:00 - 서버 메모리 부족! 긴급 조치 필요 ***

============================================================
분석 요약 보고서
============================================================
  분석 기간: 2024-03-15
  시작 시간: 08:00:01
  종료 시간: 08:14:30
  총 이벤트: 24건
  오류 비율: 20.8%
  경고 비율: 20.8%
  *** 심각 이벤트 1건 발생! 즉시 확인 필요 ***

로그 파일 분석기 예제를 성공적으로 완료했습니다!
```

### 파일 자동 정리기

예제 15-11은 다운로드 폴더처럼 여러 종류의 파일이 섞여 있는 디렉토리를 확장자별 폴더로 자동 분류하는 스크립트입니다.

**예제 15-11: 파일 정리기 (시뮬레이션)**

```python
# examples/python/chapter04/ex15_11_image_organizer.py
from pathlib import Path
from collections import defaultdict

# 분류 규칙 정의
category_rules = {
    "이미지": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"],
    "문서": [".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".xls", ".ppt"],
    "코드": [".py", ".html", ".css", ".js", ".ts", ".java", ".cpp"],
    "데이터": [".csv", ".json", ".xml", ".sql", ".db"],
    "미디어": [".mp3", ".mp4", ".avi", ".wav", ".mkv", ".mov"],
    "압축": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "텍스트": [".txt", ".md", ".log"],
}

def get_category(filename):
    """파일의 확장자를 기반으로 카테고리를 결정합니다."""
    ext = Path(filename).suffix.lower()
    if filename.endswith(".tar.gz"):
        return "압축"
    for category, extensions in category_rules.items():
        if ext in extensions:
            return category
    return "기타"

# 분류 계획 수립
plan = defaultdict(list)
for f in download_path.iterdir():
    if f.is_file():
        category = get_category(f.name)
        plan[category].append((f.name, f.stat().st_size))
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_11_image_organizer.py
```

**결과:**

```
============================================================
파일 정리기 - 시뮬레이션
============================================================

대상 폴더: Downloads/
총 파일: 24개

------------------------------------------------------------
정리 계획
------------------------------------------------------------

  [이미지] 폴더 (-> Downloads/이미지/)
  ..................................................
    logo_design.svg           (    45,000 bytes)
    profile_photo.gif         (    89,000 bytes)
    screenshot_01.png         (   180,000 bytes)
    screenshot_02.png         (   220,000 bytes)
    vacation_001.jpg          (   250,000 bytes)
    vacation_002.jpg          (   310,000 bytes)
  소계: 6개 파일, 1,094,000 bytes

  [코드] 폴더 (-> Downloads/코드/)
  ..................................................
    app.js                    (     4,200 bytes)
    index.html                (     5,600 bytes)
    main.py                   (     3,400 bytes)
    style.css                 (     2,100 bytes)
  소계: 4개 파일, 15,300 bytes

============================================================
정리 요약
============================================================
  정리 대상: 24개 파일
  생성 폴더: 7개
    - 압축/ (2개)
    - 데이터/ (3개)
    - 미디어/ (2개)
    - 문서/ (3개)
    - 이미지/ (6개)
    - 코드/ (4개)
    - 텍스트/ (2개)

  ※ 이 결과는 시뮬레이션입니다.
    실제 적용하려면 shutil.move()를 사용하세요.

이미지 파일 정리기 시뮬레이션 예제를 성공적으로 완료했습니다!
```

> **Tip:** 파일을 자동 정리할 때는 항상 시뮬레이션을 먼저 실행하는 습관을 들이세요. 파일 이동은 되돌리기 어렵고, 실수로 중요한 파일이 잘못된 폴더로 이동될 수 있습니다. 시뮬레이션 결과를 확인한 후에 실제 이동을 수행하면 안전합니다.

---

## 15.7 안전한 파일 처리

파일을 다루는 프로그램에서 가장 중요한 것은 **데이터를 잃지 않는 것**입니다. 이 섹션에서는 안전하게 파일을 처리하는 패턴과 백업 전략을 배웁니다.

### with 문을 반드시 사용하세요

파일을 열 때 `with` 문을 사용하지 않으면, 프로그램에 오류가 발생했을 때 파일이 제대로 닫히지 않을 수 있습니다.

```python
# 나쁜 예: 오류 발생 시 파일이 닫히지 않을 수 있음
f = open("data.txt", "r")
content = f.read()
process(content)  # 여기서 오류가 발생하면?
f.close()         # 이 줄이 실행되지 않음!

# 좋은 예: with 문으로 자동 정리
with open("data.txt", "r") as f:
    content = f.read()
    process(content)  # 오류가 발생해도 파일은 자동으로 닫힘
```

### 파일 존재 여부 확인

파일을 읽기 전에 존재 여부를 확인하거나, 예외 처리를 해두면 프로그램이 갑자기 종료되는 것을 방지할 수 있습니다.

```python
from pathlib import Path

file_path = Path("config.json")

# 방법 1: 존재 여부 확인
if file_path.exists():
    with open(file_path, "r") as f:
        config = json.load(f)
else:
    print("설정 파일이 없습니다. 기본값을 사용합니다.")
    config = {"theme": "light", "language": "ko"}

# 방법 2: 예외 처리 (EAFP 스타일 - 더 파이썬스러운 방식)
try:
    with open(file_path, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print("설정 파일이 없습니다. 기본값을 사용합니다.")
    config = {"theme": "light", "language": "ko"}
except json.JSONDecodeError:
    print("설정 파일 형식이 올바르지 않습니다.")
    config = {}
```

> **Tip:** 파이썬에서는 "허락을 구하기보다 용서를 구하라(EAFP: Easier to Ask Forgiveness than Permission)" 원칙에 따라 `try/except`를 사용하는 것이 더 관용적입니다. 파일이 존재하는지 확인하는 시점과 실제로 여는 시점 사이에 파일이 삭제될 수도 있기 때문에, 예외 처리가 더 안전합니다.

### 백업 스크립트

예제 15-12는 파일과 디렉토리를 안전하게 백업하는 세 가지 전략을 보여줍니다.

**예제 15-12: 백업 스크립트**

```python
# examples/python/chapter04/ex15_12_backup_script.py
import shutil
from pathlib import Path
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 방법 1: 개별 파일에 타임스탬프 붙여 백업
for f in sorted(project_path.iterdir()):
    if f.is_file():
        new_name = f"{f.stem}_{timestamp}{f.suffix}"
        dest = individual_backup / new_name
        shutil.copy2(f, dest)
        print(f"  {f.name:>15s}  ->  {new_name}")

# 방법 2: 디렉토리 통째로 백업 (폴더 복사)
folder_backup_name = f"my_project_backup_{timestamp}"
shutil.copytree(project_dir, backup_path / folder_backup_name)

# 방법 3: 변경된 파일만 백업 (증분 백업)
for f in sorted(project_path.iterdir()):
    if f.is_file():
        backup_copy = folder_backup_dest / f.name
        if backup_copy.exists():
            if f.stat().st_size != backup_copy.stat().st_size:
                shutil.copy2(f, incremental_dir / f.name)
                print(f"  [변경됨] {f.name} -> 백업")
            else:
                print(f"  [동일함] {f.name} -> 건너뜀")
        else:
            shutil.copy2(f, incremental_dir / f.name)
            print(f"  [새파일] {f.name} -> 백업")
```

**실행:**

```bash
$ python examples/python/chapter04/ex15_12_backup_script.py
```

**결과:**

```
============================================================
파일 백업 스크립트
============================================================

프로젝트 디렉토리: my_project/
백업 디렉토리: backups/
프로젝트 파일: 5개

------------------------------------------------------------
방법 1: 개별 파일에 타임스탬프 붙여 백업
------------------------------------------------------------
       README.md  ->  README_20240315_142530.md
       config.json  ->  config_20240315_142530.json
        data.csv  ->  data_20240315_142530.csv
         main.py  ->  main_20240315_142530.py
        utils.py  ->  utils_20240315_142530.py

  총 5개 파일 백업 완료

------------------------------------------------------------
방법 2: 디렉토리 통째로 백업 (폴더 복사)
------------------------------------------------------------
  백업 폴더: my_project_backup_20240315_142530/
  백업된 파일: 5개

------------------------------------------------------------
방법 3: 변경된 파일만 백업 (증분 백업)
------------------------------------------------------------
  [동일함] README.md -> 건너뜀
  [동일함] config.json -> 건너뜀
  [동일함] data.csv -> 건너뜀
  [변경됨] main.py -> 백업
  [동일함] utils.py -> 건너뜀

  변경/신규: 1개, 건너뜀: 4개

============================================================
백업 현황 요약
============================================================
  백업 위치: backups/
  백업 폴더 수: 3개
  전체 백업 크기: 1,234 bytes
  백업 시간: 2024-03-15 14:25:30

백업 스크립트 예제를 성공적으로 완료했습니다!
```

### 백업 전략 비교

| 방법 | 장점 | 단점 | 적합한 상황 |
|------|------|------|-------------|
| 개별 파일 백업 | 특정 파일의 이력 추적 가능 | 파일 수가 많으면 관리 어려움 | 설정 파일, 중요 문서 |
| 전체 디렉토리 백업 | 간단하고 완전한 복원 가능 | 용량을 많이 차지함 | 주기적 전체 백업 |
| 증분 백업 | 용량 절약, 빠른 속도 | 복원 시 여러 백업 필요 | 일상적 백업, 대용량 프로젝트 |

> **Warning:** `shutil.copy()`는 파일 내용만 복사하고, `shutil.copy2()`는 **파일의 메타데이터(수정 시간 등)까지 함께 복사**합니다. 백업 목적이라면 `copy2()`를 사용하여 원본 파일의 정보를 보존하세요.

### 안전한 파일 쓰기 패턴

파일을 쓰는 도중에 프로그램이 중단되면 파일이 손상될 수 있습니다. 이를 방지하는 안전한 패턴은 임시 파일에 먼저 쓰고, 완료 후에 원본 파일을 교체하는 것입니다.

```python
import tempfile
import os
from pathlib import Path

def safe_write(file_path, content):
    """안전한 파일 쓰기: 임시 파일에 먼저 쓰고 교체"""
    file_path = Path(file_path)

    # 1. 같은 디렉토리에 임시 파일 생성
    fd, tmp_path = tempfile.mkstemp(
        dir=file_path.parent,
        suffix=".tmp"
    )

    try:
        # 2. 임시 파일에 내용 쓰기
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)

        # 3. 임시 파일을 원본 위치로 이동 (원자적 교체)
        os.replace(tmp_path, file_path)
    except Exception:
        # 실패 시 임시 파일 정리
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
```

> **Tip:** `os.replace()`는 대부분의 운영체제에서 **원자적(atomic) 연산**으로 동작합니다. 즉, 파일이 중간 상태 없이 한 번에 교체됩니다. 이 패턴을 사용하면 쓰기 도중 정전이나 프로그램 강제 종료가 발생해도 원본 파일이 손상되지 않습니다.

---

## 정리

이번 챕터에서는 파이썬으로 파일을 자유자재로 다루는 방법을 배웠습니다. 핵심 내용을 정리합니다.

### 파일 읽기/쓰기

- **읽기**: `read()`, `readline()`, `readlines()`, `for` 루프 중 상황에 맞는 방법 선택
- **쓰기**: 쓰기 모드(`w`), 추가 모드(`a`)의 차이를 정확히 이해
- **CSV/JSON**: 구조화된 데이터는 전용 모듈(`csv`, `json`)로 처리

### 디렉토리 탐색

- **현재 디렉토리**: `Path.iterdir()` 또는 `os.scandir()`
- **재귀 탐색**: `Path.rglob()` 또는 `os.walk()`
- **패턴 매칭**: glob 패턴(`*.py`, `**/*.txt`)으로 필터링

### 파일 메타데이터

- `stat()`으로 크기, 수정 시간 등 확인
- 해시값(`hashlib`)으로 파일 내용 비교 및 중복 검출

### 일괄 처리 자동화

- 파일 이름 일괄 변경, 로그 분석, 파일 정리 등 반복 작업 자동화
- **시뮬레이션(dry_run)**을 먼저 실행하는 습관

### 안전한 파일 처리

- `with` 문으로 파일 자동 닫기
- 예외 처리(`try/except`)로 오류 대비
- 임시 파일 + 교체 패턴으로 데이터 손상 방지
- 정기적 백업으로 데이터 보호

---

## 다음 장 예고

**Chapter 16: 데이터 처리와 분석**에서는 이번 챕터에서 배운 파일 처리 기술을 바탕으로 실제 데이터를 분석하는 방법을 배웁니다. CSV 데이터의 통계 계산, 필터링과 정렬, JSON 데이터 가공, 그리고 텍스트 기반 차트로 결과를 시각화하는 기술까지 다룹니다. 파일에서 데이터를 읽어 의미 있는 정보로 변환하는 전체 과정을 경험해봅시다.