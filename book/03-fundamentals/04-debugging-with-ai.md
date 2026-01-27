## Chapter 13: AI와 함께 디버깅하기

코드를 작성하다 보면 오류는 반드시 발생합니다. 숙련된 개발자도 예외가 아닙니다. 중요한 것은 오류를 두려워하지 않고, 오류 메시지를 읽고 이해하며, 문제를 체계적으로 해결하는 능력입니다.

바이브 코딩에서는 AI가 이 과정의 강력한 파트너가 됩니다. AI에게 오류 메시지를 보여주고 "이게 무슨 뜻이야?", "어떻게 고쳐야 해?"라고 물어보는 것만으로도 대부분의 버그를 빠르게 해결할 수 있습니다.

이번 장에서는 파이썬에서 자주 만나는 오류의 종류를 알아보고, AI에게 효과적으로 디버깅을 요청하는 방법을 익혀보겠습니다.

---

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 파이썬 오류의 세 가지 종류(구문 오류, 런타임 오류, 논리 오류)를 구분하기
- 오류 메시지를 AI에게 전달하여 원인과 해결책을 얻기
- 스택 트레이스를 읽고 오류 발생 지점을 추적하기
- 논리 오류처럼 오류 메시지가 없는 버그를 AI와 함께 찾기
- 예외 처리(try/except)를 활용하여 오류에 강한 코드를 작성하기
- 예방적 디버깅 전략으로 버그를 사전에 방지하기

---

### 13.1 오류의 종류 이해하기

프로그래밍에서 만나는 오류는 크게 세 가지로 나뉩니다. 각 유형의 특성을 이해하면 AI에게 도움을 요청할 때도 훨씬 정확하게 소통할 수 있습니다.

#### 1) 구문 오류 (SyntaxError)

**구문 오류**는 파이썬 문법 규칙을 지키지 않았을 때 발생합니다. 코드가 실행되기 전에 파이썬이 미리 발견하므로, 가장 빨리 알 수 있는 오류입니다. 사람으로 치면 "맞춤법 틀렸어요!"와 같습니다.

대표적인 구문 오류:
- 콜론(`:`) 누락
- 괄호 짝이 맞지 않음
- 들여쓰기 오류
- 따옴표 닫지 않음

**예제 13-1: SyntaxError -- if문에 콜론 누락**

```python
# examples/python/chapter03/ex13_01_syntax_error_buggy.py
score = 85

if score >= 90
    print("A학점입니다!")
elif score >= 80:
    print("B학점입니다!")
else:
    print("더 노력하세요!")
```

**실행하면 다음과 같은 오류가 발생합니다:**

```
  File "ex13_01_syntax_error_buggy.py", line 4
    if score >= 90
                  ^
SyntaxError: expected ':'
```

파이썬이 `if score >= 90` 뒤에 콜론(`:`)이 와야 한다고 알려주고 있습니다. 하지만 초보자에게 이 메시지가 낯설 수 있습니다.

**AI에게 요청하는 프롬프트:**

```
다음 파이썬 코드를 실행하니 SyntaxError가 발생합니다.
오류 원인을 설명해 주고 수정해 주세요.

[코드와 오류 메시지 붙여넣기]
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_01_syntax_error_fixed.py
score = 85

if score >= 90:        # <- 콜론(:) 추가!
    print("A학점입니다!")
elif score >= 80:
    print("B학점입니다!")
else:
    print("더 노력하세요!")
```

**실행 결과:**
```
B학점입니다!
```

> **Tip:** 구문 오류는 파이썬이 정확한 위치를 알려주기 때문에 AI 없이도 고칠 수 있는 경우가 많습니다. 하지만 오류 메시지가 영어라 해석이 어려울 때 AI에게 "이 오류 메시지가 무슨 뜻이야?"라고 물어보면 친절한 한국어 설명을 받을 수 있습니다.

---

#### 2) 런타임 오류 (Runtime Error)

**런타임 오류**는 문법은 올바르지만, 실행 도중에 발생하는 오류입니다. 코드가 어느 정도 실행된 뒤에야 특정 줄에서 문제가 터지기 때문에, 구문 오류보다 원인을 찾기가 더 어렵습니다.

파이썬에서 자주 만나는 런타임 오류를 하나씩 살펴보겠습니다.

---

**예제 13-2: NameError -- 변수 이름 오타**

```python
# examples/python/chapter03/ex13_02_name_error_buggy.py
user_name = "홍길동"
user_age = 25

# 'user_naem'은 정의되지 않은 변수 (올바른 이름: user_name)
print(f"이름: {user_naem}")
print(f"나이: {user_age}세")
print(f"{user_name}님, 환영합니다!")
```

**오류 메시지:**
```
Traceback (most recent call last):
  File "ex13_02_name_error_buggy.py", line 6, in <module>
    print(f"이름: {user_naem}")
                   ^^^^^^^^^
NameError: name 'user_naem' is not defined. Did you mean: 'user_name'?
```

**AI에게 요청하는 프롬프트:**

```
NameError: name 'user_naem' is not defined 오류가 발생합니다.
코드에서 무엇이 잘못되었는지 찾아서 수정해 주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_02_name_error_fixed.py
user_name = "홍길동"
user_age = 25

print(f"이름: {user_name}")    # <- user_naem -> user_name 수정!
print(f"나이: {user_age}세")
print(f"{user_name}님, 환영합니다!")
```

**실행 결과:**
```
이름: 홍길동
나이: 25세
홍길동님, 환영합니다!
```

> **Warning:** `NameError`는 변수 이름 오타에서 가장 많이 발생합니다. 특히 `user_name`과 `user_naem`처럼 비슷하게 생긴 오타는 눈으로 찾기 어렵습니다. AI는 이런 미세한 차이를 정확하게 잡아냅니다.

---

**예제 13-3: TypeError -- 문자열과 정수 결합 오류**

```python
# examples/python/chapter03/ex13_03_type_error_buggy.py
product_name = "노트북"
price = 1500000
quantity = 3

total = price * quantity
print("상품: " + product_name)
print("수량: " + quantity + "개")           # <- 오류 발생!
print("총 금액: " + total + "원")           # <- 오류 발생!
```

**오류 메시지:**
```
Traceback (most recent call last):
  File "ex13_03_type_error_buggy.py", line 7, in <module>
    print("수량: " + quantity + "개")
          ~~~~~~~~~^~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

**AI에게 요청하는 프롬프트:**

```
문자열과 숫자를 + 연산자로 합치려고 하니 TypeError가 발생합니다.
이 문제를 해결하는 여러 가지 방법을 알려주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_03_type_error_fixed.py
product_name = "노트북"
price = 1500000
quantity = 3

total = price * quantity

# 방법 1: str()로 명시적 변환
print("상품: " + product_name)
print("수량: " + str(quantity) + "개")

# 방법 2: f-string 사용 (권장!)
print(f"총 금액: {total:,}원")

# 방법 3: print의 쉼표 구분 (자동 공백 추가됨)
print("결제 정보:", product_name, quantity, "개,", f"{total:,}원")
```

**실행 결과:**
```
상품: 노트북
수량: 3개
총 금액: 4,500,000원
결제 정보: 노트북 3 개, 4,500,000원
```

> **Tip:** AI는 단순히 오류만 고치는 것이 아니라, 여러 가지 해결 방법을 알려줍니다. 위 예제에서 `str()` 변환, f-string, 쉼표 구분 등 세 가지 방법을 모두 보여주었습니다. 이 중에서 **f-string**이 가장 현대적이고 권장되는 방법입니다.

---

**예제 13-4: IndexError -- 리스트 인덱스 범위 초과**

```python
# examples/python/chapter03/ex13_04_index_error_buggy.py
fruits = ["사과", "바나나", "딸기", "포도", "수박"]

print("과일 목록:")
print(f"  1번: {fruits[0]}")
print(f"  2번: {fruits[1]}")
print(f"  3번: {fruits[2]}")
print(f"  4번: {fruits[3]}")
print(f"  5번: {fruits[4]}")
print(f"  6번: {fruits[5]}")    # <- 오류! 인덱스는 0~4까지만 유효

# 반복문에서도 같은 실수 발생 가능
print("\n반복문으로 출력:")
for i in range(6):               # <- 오류! range(5) 또는 range(len(fruits)) 사용해야 함
    print(f"  {fruits[i]}")
```

**오류 메시지:**
```
IndexError: list index out of range
```

**AI에게 요청하는 프롬프트:**

```
리스트에 5개 항목이 있는데 fruits[5]에 접근하니 IndexError가 발생합니다.
안전하게 리스트를 순회하는 방법을 알려주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_04_index_error_fixed.py
fruits = ["사과", "바나나", "딸기", "포도", "수박"]

# 방법 1: len()으로 길이 확인
print(f"과일 목록 (총 {len(fruits)}개):")
for i in range(len(fruits)):     # <- len(fruits) = 5, range(5) = 0~4
    print(f"  {i + 1}번: {fruits[i]}")

# 방법 2: enumerate 사용 (더 파이썬다운 방법!)
print("\nenumerate로 출력:")
for idx, fruit in enumerate(fruits, start=1):
    print(f"  {idx}번: {fruit}")

# 방법 3: 인덱스 접근 전 범위 확인
target_index = 5
if target_index < len(fruits):
    print(f"\n{target_index}번 인덱스: {fruits[target_index]}")
else:
    print(f"\n{target_index}번 인덱스는 범위를 벗어났습니다! (유효 범위: 0~{len(fruits) - 1})")
```

**실행 결과:**
```
과일 목록 (총 5개):
  1번: 사과
  2번: 바나나
  3번: 딸기
  4번: 포도
  5번: 수박

enumerate로 출력:
  1번: 사과
  2번: 바나나
  3번: 딸기
  4번: 포도
  5번: 수박

5번 인덱스는 범위를 벗어났습니다! (유효 범위: 0~4)
```

> **Warning:** 파이썬의 인덱스는 **0부터** 시작합니다. 5개 항목이 있는 리스트의 유효 인덱스는 0, 1, 2, 3, 4입니다. `fruits[5]`는 6번째 항목을 가리키므로 존재하지 않습니다. 이 "하나 차이(off-by-one)" 실수는 초보자와 숙련자 모두에게 빈번하게 발생합니다.

---

**예제 13-5: KeyError -- 존재하지 않는 딕셔너리 키**

```python
# examples/python/chapter03/ex13_05_key_error_buggy.py
student = {
    "이름": "김철수",
    "나이": 20,
    "학과": "컴퓨터공학",
    "학년": 2
}

print("=== 학생 정보 ===")
print(f"이름: {student['이름']}")
print(f"나이: {student['나이']}")
print(f"학과: {student['학과']}")
print(f"학년: {student['학년']}")
print(f"학번: {student['학번']}")       # <- KeyError! '학번' 키가 없음
print(f"이메일: {student['email']}")    # <- KeyError! 'email' 키가 없음
```

**오류 메시지:**
```
KeyError: '학번'
```

**AI에게 요청하는 프롬프트:**

```
딕셔너리에 '학번' 키가 없어서 KeyError가 발생합니다.
키가 있을 수도 있고 없을 수도 있는 상황에서 안전하게 접근하는 방법을 알려주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_05_key_error_fixed.py
student = {
    "이름": "김철수",
    "나이": 20,
    "학과": "컴퓨터공학",
    "학년": 2
}

print("=== 학생 정보 ===")
print(f"이름: {student['이름']}")
print(f"나이: {student['나이']}")
print(f"학과: {student['학과']}")
print(f"학년: {student['학년']}")

# 방법 1: .get()으로 기본값 지정
print(f"학번: {student.get('학번', '미등록')}")        # <- 키가 없으면 '미등록' 반환
print(f"이메일: {student.get('email', '미등록')}")     # <- 키가 없으면 '미등록' 반환

# 방법 2: in 키워드로 키 존재 여부 확인
print("\n=== 키 존재 여부 확인 ===")
for key in ["이름", "학번", "email", "학과"]:
    if key in student:
        print(f"  {key}: {student[key]}")
    else:
        print(f"  {key}: (정보 없음)")
```

**실행 결과:**
```
=== 학생 정보 ===
이름: 김철수
나이: 20
학과: 컴퓨터공학
학년: 2
학번: 미등록
이메일: 미등록

=== 키 존재 여부 확인 ===
  이름: 김철수
  학번: (정보 없음)
  email: (정보 없음)
  학과: 컴퓨터공학
```

> **Tip:** 딕셔너리의 `.get()` 메서드는 키가 없을 때 기본값을 반환해 줍니다. API 응답이나 설정 파일 등 데이터 구조가 불확실한 경우에 특히 유용합니다.

---

**예제 13-6: FileNotFoundError -- 존재하지 않는 파일**

```python
# examples/python/chapter03/ex13_06_file_not_found_buggy.py
filename = "학생명단.txt"

# 파일이 존재하지 않으면 FileNotFoundError 발생
file = open(filename, "r", encoding="utf-8")
content = file.read()
print(f"파일 내용:\n{content}")
file.close()
```

**오류 메시지:**
```
FileNotFoundError: [Errno 2] No such file or directory: '학생명단.txt'
```

**AI에게 요청하는 프롬프트:**

```
파일을 열려고 하는데 FileNotFoundError가 발생합니다.
파일이 없을 때도 프로그램이 안전하게 동작하도록 수정해 주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_06_file_not_found_fixed.py
import os

filename = "학생명단.txt"

# 방법 1: os.path.exists()로 사전 확인
print("=== 방법 1: 파일 존재 여부 사전 확인 ===")
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(f"파일 내용:\n{content}")
else:
    print(f"'{filename}' 파일을 찾을 수 없습니다.")
    print(f"현재 디렉토리: {os.getcwd()}")
    print(f"현재 디렉토리의 파일 목록:")
    for f in os.listdir("."):
        print(f"  - {f}")

# 방법 2: try/except로 예외 처리 (더 파이썬다운 방법!)
print("\n=== 방법 2: try/except 예외 처리 ===")
try:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(f"파일 내용:\n{content}")
except FileNotFoundError:
    print(f"오류: '{filename}' 파일이 존재하지 않습니다.")
    print("해결 방법:")
    print("  1. 파일 이름이 정확한지 확인하세요.")
    print("  2. 파일이 올바른 디렉토리에 있는지 확인하세요.")
    print("  3. 파일 경로를 절대 경로로 지정해 보세요.")
except PermissionError:
    print(f"오류: '{filename}' 파일에 대한 읽기 권한이 없습니다.")
```

> **Warning:** 파일 관련 오류를 처리할 때는 `FileNotFoundError`뿐만 아니라 `PermissionError`(권한 오류)도 함께 처리하는 것이 좋습니다. 실제 환경에서는 파일이 존재하더라도 읽기 권한이 없는 경우가 종종 있습니다.

---

#### 3) 논리 오류 (Logic Error)

**논리 오류**는 가장 까다로운 유형입니다. 코드가 오류 없이 정상적으로 실행되지만, **결과가 잘못된** 경우입니다. 파이썬이 오류 메시지를 보여주지 않기 때문에, 개발자가 직접 "이 결과가 맞나?"를 확인하지 않으면 버그를 발견할 수 없습니다.

바로 이런 상황에서 AI가 큰 도움이 됩니다.

**예제 13-9: 논리 오류 -- 성적 계산기의 잘못된 조건문 순서**

```python
# examples/python/chapter03/ex13_09_logic_error_buggy.py
def calculate_grade(score):
    """점수를 받아 학점을 반환 (잘못된 버전)"""
    if score >= 60:       # <- 버그! 60점 이상이면 모두 여기에 걸림
        grade = "A"
    elif score >= 70:     # <- 도달 불가능!
        grade = "B"
    elif score >= 80:     # <- 도달 불가능!
        grade = "C"
    elif score >= 90:     # <- 도달 불가능!
        grade = "D"
    else:
        grade = "F"
    return grade


# 테스트
print("=== 성적 계산기 (버그 있는 버전) ===")
test_scores = [95, 85, 75, 65, 55]

for score in test_scores:
    grade = calculate_grade(score)
    print(f"  {score}점 -> {grade}학점")
```

**실행 결과 (잘못된 결과):**
```
=== 성적 계산기 (버그 있는 버전) ===
  95점 -> A학점
  85점 -> A학점
  75점 -> A학점
  65점 -> A학점
  55점 -> F학점
```

95점이 A인 것은 맞지만, 65점도 A학점이 나옵니다! 오류 메시지가 전혀 없기 때문에, 실행 결과를 주의 깊게 확인하지 않으면 이 버그를 놓칠 수 있습니다.

**AI에게 요청하는 프롬프트:**

```
성적 계산기를 만들었는데 모든 60점 이상 학생이 A학점으로 나옵니다.
90점 이상 A, 80점 이상 B, 70점 이상 C, 60점 이상 D, 60 미만 F가 되어야 합니다.
코드를 확인하고 문제를 찾아주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_09_logic_error_fixed.py
def calculate_grade(score):
    """점수를 받아 학점을 반환 (올바른 버전)"""
    if score >= 90:       # <- 가장 높은 기준부터 확인!
        grade = "A"
    elif score >= 80:     # 90 미만이면서 80 이상
        grade = "B"
    elif score >= 70:     # 80 미만이면서 70 이상
        grade = "C"
    elif score >= 60:     # 70 미만이면서 60 이상
        grade = "D"
    else:                 # 60 미만
        grade = "F"
    return grade


# 테스트
print("=== 성적 계산기 (수정된 버전) ===")
test_scores = [95, 85, 75, 65, 55]

for score in test_scores:
    grade = calculate_grade(score)
    print(f"  {score}점 -> {grade}학점")
```

**실행 결과:**
```
=== 성적 계산기 (수정된 버전) ===
  95점 -> A학점
  85점 -> B학점
  75점 -> C학점
  65점 -> D학점
  55점 -> F학점
```

> **Warning:** `if/elif` 조건문에서는 **검사 순서**가 매우 중요합니다. 넓은 범위의 조건(`>= 60`)을 먼저 검사하면 그 아래의 좁은 범위 조건(`>= 70`, `>= 80` 등)에는 절대 도달하지 않습니다. 범위 조건을 사용할 때는 반드시 **가장 좁은(높은) 조건부터** 검사해야 합니다.

---

#### 오류 종류 요약

| 종류 | 발생 시점 | 오류 메시지 | 발견 난이도 | 예시 |
|------|-----------|-------------|-------------|------|
| **구문 오류** | 실행 전 | 있음 (정확한 위치 표시) | 쉬움 | 콜론 누락, 괄호 불일치 |
| **런타임 오류** | 실행 중 | 있음 (스택 트레이스) | 보통 | NameError, TypeError |
| **논리 오류** | 실행 완료 | **없음** | 어려움 | 조건문 순서 잘못, 계산 오류 |

---

### 13.2 오류 메시지 분석 요청하기

AI에게 디버깅을 요청할 때, 효과적인 프롬프트 작성법이 있습니다. 단순히 "코드가 안 돼요"라고 말하는 것보다 구체적인 정보를 제공할수록 더 정확한 답변을 받을 수 있습니다.

#### 효과적인 디버깅 요청 템플릿

```
[상황 설명]
다음 코드를 실행하면 오류가 발생합니다.

[코드]
(전체 코드 붙여넣기)

[오류 메시지]
(전체 오류 메시지 붙여넣기)

[요청]
1. 오류의 원인을 설명해 주세요.
2. 수정된 코드를 보여주세요.
3. 같은 실수를 방지하는 방법도 알려주세요.
```

#### 좋은 요청과 나쁜 요청 비교

**나쁜 요청:**
```
코드가 안 돼요. 고쳐주세요.
```

**좋은 요청:**
```
파이썬으로 학생 성적 프로그램을 만들었는데 TypeError가 발생합니다.
오류 메시지: TypeError: can only concatenate str (not "int") to str
아래 코드에서 문제를 찾아서 수정해 주세요.

[코드 붙여넣기]
```

핵심은 다음 세 가지를 포함하는 것입니다:

1. **코드 전체** -- 일부만 보여주면 AI가 문맥을 파악하기 어렵습니다
2. **오류 메시지 전체** -- 스택 트레이스를 포함하면 더 정확한 분석이 가능합니다
3. **기대하는 동작** -- "어떤 결과를 원하는지" 설명하면 논리 오류도 잡아줍니다

> **Tip:** 오류 메시지를 복사할 때는 **전체를 복사**하세요. `Traceback (most recent call last):`부터 마지막 오류 줄까지 모두 포함하면 AI가 훨씬 정확하게 분석할 수 있습니다.

---

### 13.3 스택 트레이스 해석하기

여러 함수가 서로를 호출하는 복잡한 코드에서 오류가 발생하면, 파이썬은 **스택 트레이스(Stack Trace)**를 출력합니다. 스택 트레이스는 "오류가 어떤 경로를 거쳐 발생했는지"를 보여주는 지도와 같습니다.

**예제 13-10: 중첩 함수 호출에서의 스택 트레이스**

```python
# examples/python/chapter03/ex13_10_stack_trace_buggy.py
def calculate_average(numbers):
    """평균을 계산하는 함수"""
    total = sum(numbers)
    average = total / len(numbers)    # <- 빈 리스트이면 ZeroDivisionError!
    return average


def get_class_average(students):
    """반 전체 평균을 계산하는 함수"""
    all_scores = []
    for student in students:
        all_scores.extend(student["scores"])
    return calculate_average(all_scores)


def generate_report(class_name, students):
    """성적 보고서를 생성하는 함수"""
    print(f"=== {class_name} 성적 보고서 ===")
    avg = get_class_average(students)
    print(f"반 평균: {avg:.1f}점")
    return avg


# 실행 -- 학생 데이터에 점수가 없는 경우
students = [
    {"name": "김철수", "scores": []},   # <- 점수가 비어 있음!
    {"name": "이영희", "scores": []},   # <- 점수가 비어 있음!
]

generate_report("3학년 1반", students)
```

**오류 메시지 (스택 트레이스):**
```
=== 3학년 1반 성적 보고서 ===
Traceback (most recent call last):
  File "ex13_10_stack_trace_buggy.py", line 31, in <module>
    generate_report("3학년 1반", students)
  File "ex13_10_stack_trace_buggy.py", line 20, in generate_report
    avg = get_class_average(students)
  File "ex13_10_stack_trace_buggy.py", line 14, in get_class_average
    return calculate_average(all_scores)
  File "ex13_10_stack_trace_buggy.py", line 4, in calculate_average
    average = total / len(numbers)
ZeroDivisionError: division by zero
```

#### 스택 트레이스 읽는 법

스택 트레이스는 **아래에서 위로** 읽으면 쉽습니다:

| 순서 | 위치 | 의미 |
|------|------|------|
| 4 (최초) | `<module>` 31줄 | `generate_report()` 함수를 호출 |
| 3 | `generate_report` 20줄 | `get_class_average()` 함수를 호출 |
| 2 | `get_class_average` 14줄 | `calculate_average()` 함수를 호출 |
| 1 (오류 발생) | `calculate_average` 4줄 | `total / len(numbers)`에서 0으로 나눔 |

가장 아래의 `ZeroDivisionError: division by zero`가 실제 오류이고, 그 위의 호출 순서를 따라 올라가면 원인을 추적할 수 있습니다.

**AI에게 요청하는 프롬프트:**

```
아래 스택 트레이스가 발생했습니다.
오류의 원인을 단계별로 설명하고, 빈 리스트가 전달되어도
안전하게 동작하도록 코드를 수정해 주세요.

[스택 트레이스 전체 붙여넣기]
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_10_stack_trace_fixed.py
def calculate_average(numbers):
    """평균을 계산하는 함수 (안전한 버전)"""
    if not numbers:                  # <- 빈 리스트 체크 추가!
        print("  경고: 점수 데이터가 없습니다.")
        return 0.0
    total = sum(numbers)
    average = total / len(numbers)
    return average


def get_class_average(students):
    """반 전체 평균을 계산하는 함수 (안전한 버전)"""
    all_scores = []
    for student in students:
        scores = student.get("scores", [])    # <- .get()으로 안전 접근
        all_scores.extend(scores)
    return calculate_average(all_scores)


def generate_report(class_name, students):
    """성적 보고서를 생성하는 함수 (안전한 버전)"""
    print(f"=== {class_name} 성적 보고서 ===")
    try:
        avg = get_class_average(students)
        if avg > 0:
            print(f"반 평균: {avg:.1f}점")
        else:
            print("반 평균: 데이터 없음")
    except Exception as e:
        print(f"보고서 생성 중 오류 발생: {e}")
    print()
```

**수정 포인트 정리:**

1. `calculate_average()`에 빈 리스트 체크를 추가하여 `ZeroDivisionError` 방지
2. `student.get("scores", [])`로 키가 없는 경우에도 안전하게 접근
3. `generate_report()`에 `try/except`를 추가하여 예상치 못한 오류도 처리

> **Tip:** 스택 트레이스를 처음 보면 길고 복잡하게 느껴지지만, 가장 **마지막 줄(오류 종류와 메시지)**부터 읽으면 핵심을 빠르게 파악할 수 있습니다. AI에게 스택 트레이스 전체를 보여주면 "이 오류는 이런 흐름으로 발생했고, 이렇게 고치면 됩니다"라고 상세히 설명해 줍니다.

---

### 13.4 논리 오류 찾기

논리 오류는 오류 메시지가 없기 때문에 AI에게 요청할 때 **기대하는 결과**와 **실제 결과**를 함께 알려주는 것이 중요합니다.

#### Off-by-one 오류

가장 흔한 논리 오류 중 하나가 "하나 차이(off-by-one)" 오류입니다.

**예제 13-8: range() 범위 실수**

```python
# examples/python/chapter03/ex13_08_off_by_one_buggy.py
print("1부터 10까지의 합 계산")
print("=" * 35)

total = 0
numbers = []

for i in range(1, 10):           # <- 버그! range(1, 10)은 1~9까지만 포함
    total += i
    numbers.append(i)

print(f"더한 숫자: {numbers}")
print(f"계산 결과: {total}")
print(f"기대 결과: 55")          # 1+2+...+10 = 55
print(f"결과 일치: {total == 55}")  # False!
```

**실행 결과:**
```
1부터 10까지의 합 계산
===================================
더한 숫자: [1, 2, 3, 4, 5, 6, 7, 8, 9]
계산 결과: 45
기대 결과: 55
결과 일치: False
```

오류 메시지는 없지만, 계산 결과가 55가 아닌 45입니다. 10이 빠져 있는 것이죠.

**AI에게 요청하는 프롬프트:**

```
1부터 10까지 합을 구하는 코드인데 결과가 55가 아닌 45가 나옵니다.
어디가 잘못된 건지 확인하고 수정해 주세요.
range()의 동작 원리도 함께 설명해 주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_08_off_by_one_fixed.py
print("1부터 10까지의 합 계산")
print("=" * 35)

total = 0
numbers = []

for i in range(1, 11):           # <- 수정! range(1, 11)은 1~10까지 포함
    total += i
    numbers.append(i)

print(f"더한 숫자: {numbers}")
print(f"계산 결과: {total}")
print(f"기대 결과: 55")
print(f"결과 일치: {total == 55}")  # True!
```

**실행 결과:**
```
1부터 10까지의 합 계산
===================================
더한 숫자: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
계산 결과: 55
기대 결과: 55
결과 일치: True
```

AI는 `range()`의 동작 원리도 함께 설명해 줍니다:

```
range() 동작 원리:
  range(5)     -> [0, 1, 2, 3, 4]        # 0부터 4까지
  range(1, 5)  -> [1, 2, 3, 4]           # 1부터 4까지
  range(1, 6)  -> [1, 2, 3, 4, 5]        # 1부터 5까지
  range(1, 11) -> [1, 2, 3, 4, ..., 10]  # 1부터 10까지

핵심: range(a, b)는 a 이상 b '미만'!
```

> **Warning:** `range(a, b)`는 `a` 이상 `b` **미만**입니다. 즉, `b`는 포함되지 않습니다. "1부터 10까지"를 원하면 `range(1, 11)`을 사용해야 합니다. 이것은 파이썬에서 가장 흔한 논리 오류 중 하나입니다.

---

#### 무한 루프

논리 오류의 또 다른 대표적인 유형이 무한 루프입니다. 프로그램이 끝나지 않고 영원히 반복되는 상황입니다.

**예제 13-7: while 루프에서 증감 누락**

```python
# examples/python/chapter03/ex13_07_infinite_loop_buggy.py (개념 코드)
print("1부터 5까지 출력합니다:")

count = 1
while count <= 5:
    print(f"  현재 값: {count}")
    # count += 1  <- 이 줄이 빠져 있어서 count가 계속 1!
```

이 코드를 실행하면 `count`가 영원히 1인 채로 `현재 값: 1`이 무한히 출력됩니다. `Ctrl+C`를 눌러 강제 종료해야 합니다.

**AI에게 요청하는 프롬프트:**

```
while 루프로 1부터 5까지 출력하려고 했는데 프로그램이 끝나지 않고
계속 반복됩니다. 무한 루프가 발생한 것 같은데 원인을 찾아주세요.
```

**AI가 수정한 코드:**

```python
# examples/python/chapter03/ex13_07_infinite_loop_fixed.py
print("1부터 5까지 출력합니다:")

count = 1
while count <= 5:
    print(f"  현재 값: {count}")
    count += 1                    # <- 이 줄을 추가하여 무한 루프 해결!

print(f"완료! (마지막 count 값: {count})")

# 더 안전한 방법: for 루프 사용
print("\nfor 루프로 같은 작업:")
for i in range(1, 6):
    print(f"  현재 값: {i}")

print("완료!")
```

**실행 결과:**
```
1부터 5까지 출력합니다:
  현재 값: 1
  현재 값: 2
  현재 값: 3
  현재 값: 4
  현재 값: 5
완료! (마지막 count 값: 6)

for 루프로 같은 작업:
  현재 값: 1
  현재 값: 2
  현재 값: 3
  현재 값: 4
  현재 값: 5
완료!
```

> **Warning:** `while` 루프를 사용할 때는 반드시 **종료 조건이 언젠가 충족되는지** 확인하세요. 루프 안에서 조건에 영향을 주는 변수를 반드시 변경해야 합니다. 카운터가 필요한 반복이라면 `for` 루프를 사용하는 것이 더 안전합니다.

---

### 13.5 디버깅 전략: 실전 종합 실습

지금까지 개별 오류를 하나씩 다루었습니다. 실제 프로그래밍에서는 하나의 코드에 여러 종류의 버그가 동시에 있는 경우가 많습니다. 이런 상황에서 AI를 활용하여 체계적으로 디버깅하는 방법을 연습해 보겠습니다.

**예제 13-11: 버그 5개가 숨어있는 쇼핑 카트 프로그램**

다음은 쇼핑 카트 프로그램인데, 5개의 버그가 숨어 있습니다.

```python
# examples/python/chapter03/ex13_11_five_bugs_buggy.py
products = {
    "사과": 1500,
    "우유": 2500,
    "빵": 3000,
    "계란": 5000,
    "치즈": 4500
}

cart = []


def add_to_cart(product_name, qty):
    """상품을 카트에 추가"""
    # 버그 1: 존재하지 않는 상품에 접근하면 KeyError
    price = products[product_name]
    item = {
        "name": product_name,
        "price": price,
        "quantity": qty
    }
    cart.append(item)
    print(f"  '{product_name}' {qty}개 추가 (개당 {price}원)")


def calculate_total():
    """카트 총 금액 계산"""
    total = 0
    for item in cart:
        # 버그 2: 수량을 곱하지 않음
        total += item["price"]
    return total


def apply_discount(total, discount_percent):
    """할인 적용"""
    # 버그 3: 할인 계산 공식 오류 (할인율을 100으로 나누지 않음)
    discount_amount = total * discount_percent
    final_price = total - discount_amount
    return final_price


def print_receipt():
    """영수증 출력"""
    print("\n" + "=" * 40)
    print("           영수증")
    print("=" * 40)

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        # 버그 4: f-string에서 변수명 오타 (sub_total vs subtotal)
        print(f"  {item['name']:8s} x{item['quantity']}  = {sub_total:>8,}원")

    total = calculate_total()
    print("-" * 40)
    print(f"  소계:                    {total:>8,}원")

    # 10% 할인 적용
    final = apply_discount(total, 10)
    print(f"  할인 (10%):              -{total - final:>7,}원")
    print(f"  최종 금액:               {final:>8,}원")
    print("=" * 40)


# 실행
print("=== 쇼핑 시작 ===")
add_to_cart("사과", 3)
add_to_cart("우유", 2)
add_to_cart("빵", 1)
add_to_cart("커피", 1)        # 버그 5: 상품 목록에 없는 상품 추가 시도
```

이 코드를 실행하면 여러 오류가 연쇄적으로 발생합니다.

**AI에게 요청하는 프롬프트:**

```
아래 쇼핑 카트 프로그램에 버그가 여러 개 있습니다.
모든 버그를 찾아서 하나씩 설명하고, 전체 코드를 수정해 주세요.

[코드 붙여넣기]
```

**AI가 찾아낸 5가지 버그와 수정:**

| 번호 | 버그 | 유형 | 수정 방법 |
|------|------|------|-----------|
| 1 | 존재하지 않는 상품 접근 시 `KeyError` | 런타임 | 상품 존재 여부 확인 후 추가 |
| 2 | `calculate_total()`에서 수량 미반영 | 논리 | `item["price"] * item["quantity"]` |
| 3 | 할인율을 100으로 나누지 않음 | 논리 | `discount_percent / 100` |
| 4 | 변수명 오타 `sub_total` | 런타임 | `subtotal`로 수정 |
| 5 | 목록에 없는 "커피" 추가 시도 | 런타임 | 존재 여부 확인 로직 추가 |

**AI가 수정한 전체 코드:**

```python
# examples/python/chapter03/ex13_11_five_bugs_fixed.py
products = {
    "사과": 1500,
    "우유": 2500,
    "빵": 3000,
    "계란": 5000,
    "치즈": 4500
}

cart = []


def add_to_cart(product_name, qty):
    """상품을 카트에 추가"""
    # 수정 1 & 5: 상품 존재 여부 확인
    if product_name not in products:
        print(f"  '{product_name}'은(는) 상품 목록에 없습니다. 건너뜁니다.")
        return

    price = products[product_name]
    item = {
        "name": product_name,
        "price": price,
        "quantity": qty
    }
    cart.append(item)
    print(f"  '{product_name}' {qty}개 추가 (개당 {price:,}원)")


def calculate_total():
    """카트 총 금액 계산"""
    total = 0
    for item in cart:
        # 수정 2: 가격 x 수량으로 계산
        total += item["price"] * item["quantity"]
    return total


def apply_discount(total, discount_percent):
    """할인 적용"""
    # 수정 3: 할인율을 100으로 나누어 퍼센트 적용
    discount_amount = total * (discount_percent / 100)
    final_price = total - discount_amount
    return final_price


def print_receipt():
    """영수증 출력"""
    print("\n" + "=" * 40)
    print("           영수증")
    print("=" * 40)

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        # 수정 4: sub_total -> subtotal (올바른 변수명)
        print(f"  {item['name']:8s} x{item['quantity']}  = {subtotal:>8,}원")

    total = calculate_total()
    print("-" * 40)
    print(f"  소계:                    {total:>8,}원")

    # 10% 할인 적용
    final = apply_discount(total, 10)
    print(f"  할인 (10%):              -{total - final:>7,}원")
    print(f"  최종 금액:               {final:>8,.0f}원")
    print("=" * 40)


# 실행
print("=== 쇼핑 시작 ===")
add_to_cart("사과", 3)
add_to_cart("우유", 2)
add_to_cart("빵", 1)
add_to_cart("커피", 1)        # 수정 5: 없는 상품 -> 경고 메시지 출력
```

**실행 결과:**
```
=== 쇼핑 시작 ===
  '사과' 3개 추가 (개당 1,500원)
  '우유' 2개 추가 (개당 2,500원)
  '빵' 1개 추가 (개당 3,000원)
  '커피'은(는) 상품 목록에 없습니다. 건너뜁니다.

========================================
           영수증
========================================
  사과       x3  =    4,500원
  우유       x2  =    5,000원
  빵        x1  =    3,000원
----------------------------------------
  소계:                      12,500원
  할인 (10%):              -  1,250원
  최종 금액:                11,250원
========================================
```

> **Tip:** 복잡한 코드에서 여러 버그를 동시에 고쳐야 할 때는, AI에게 "모든 버그를 찾아주세요"라고 요청하면 됩니다. AI는 코드를 처음부터 끝까지 분석하며 구문 오류, 런타임 오류, 논리 오류를 모두 찾아냅니다.

---

### 13.6 예방적 디버깅: 오류를 미리 막는 코드 작성

최고의 디버깅은 버그가 발생하지 않도록 미리 방지하는 것입니다. AI에게 "이 코드에 예외 처리를 추가해 줘"라고 요청하면, 다양한 오류 상황에 대비하는 견고한 코드를 작성해 줍니다.

#### try/except로 예외 처리하기

**예제 13-12: 예외 처리 없는 계산기 vs 견고한 계산기**

먼저, 예외 처리가 없는 기본 계산기를 살펴보겠습니다.

```python
# examples/python/chapter03/ex13_12_exception_handling_bare.py
def divide(a, b):
    """나눗셈"""
    return a / b


def calculate():
    """사용자 입력을 받아 계산 수행"""
    print("=== 간단한 계산기 ===")
    print("두 숫자와 연산자를 입력하세요.\n")

    num1 = float(input("첫 번째 숫자: "))
    num2 = float(input("두 번째 숫자: "))
    operator = input("연산자 (+, -, *, /): ")

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = divide(num1, num2)

    print(f"\n결과: {num1} {operator} {num2} = {result}")
```

이 코드는 정상적인 입력에서는 잘 동작하지만, 다음과 같은 상황에서 오류가 발생합니다:

| 상황 | 발생하는 오류 |
|------|---------------|
| 숫자 대신 "abc" 입력 | `ValueError` |
| 0으로 나누기 시도 | `ZeroDivisionError` |
| 잘못된 연산자 "%" 입력 | `UnboundLocalError` (result 미정의) |
| Ctrl+C로 중단 | `KeyboardInterrupt` |

**AI에게 요청하는 프롬프트:**

```
아래 계산기 프로그램에 예외 처리를 추가해 주세요.
숫자가 아닌 입력, 0으로 나누기, 잘못된 연산자 등
모든 오류 상황에서 프로그램이 안전하게 동작해야 합니다.
```

**AI가 수정한 견고한 계산기:**

```python
# examples/python/chapter03/ex13_12_exception_handling_robust.py
def divide(a, b):
    """나눗셈 (0으로 나누기 방지)"""
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다!")
    return a / b


def get_number(prompt):
    """숫자 입력을 안전하게 받는 함수"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("  올바른 숫자를 입력해 주세요. (예: 10, 3.14)")


def get_operator():
    """연산자 입력을 안전하게 받는 함수"""
    valid_operators = ["+", "-", "*", "/"]
    while True:
        op = input("연산자 (+, -, *, /): ").strip()
        if op in valid_operators:
            return op
        print(f"  올바른 연산자를 입력해 주세요: {', '.join(valid_operators)}")


def calculate():
    """사용자 입력을 받아 계산 수행 (견고한 버전)"""
    print("=== 간단한 계산기 (견고한 버전) ===")
    print("두 숫자와 연산자를 입력하세요.")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    try:
        num1 = get_number("첫 번째 숫자: ")
        num2 = get_number("두 번째 숫자: ")
        operator = get_operator()

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            try:
                result = divide(num1, num2)
            except ZeroDivisionError as e:
                print(f"\n오류: {e}")
                return

        # 결과가 정수인 경우 깔끔하게 출력
        if result == int(result):
            result = int(result)

        print(f"\n결과: {num1} {operator} {num2} = {result}")

    except KeyboardInterrupt:
        print("\n\n계산기를 종료합니다. 안녕히 가세요!")
```

#### 예방적 디버깅의 핵심 원칙

AI에게 다음과 같이 요청하면 예방적 디버깅을 적용할 수 있습니다:

**1. 입력값 검증 요청**
```
이 함수에 잘못된 입력이 들어올 수 있는 경우를 모두 생각해서
입력값 검증 코드를 추가해 줘.
```

**2. 방어적 코딩 요청**
```
이 코드에서 발생할 수 있는 모든 예외 상황을 처리해 줘.
```

**3. 경계값 테스트 요청**
```
이 함수가 빈 리스트, None, 음수, 0 등 극단적인 입력에서도
안전하게 동작하는지 확인하고 수정해 줘.
```

#### 예방적 디버깅 체크리스트

코드를 작성하거나 AI에게 코드를 받았을 때, 다음 항목을 확인하세요:

| 항목 | 확인 사항 |
|------|-----------|
| 입력값 | 빈 값, None, 잘못된 타입이 들어오면? |
| 리스트/딕셔너리 | 빈 컬렉션, 존재하지 않는 키/인덱스 접근은? |
| 파일 작업 | 파일이 없거나, 권한이 없거나, 경로가 잘못되면? |
| 나눗셈 | 0으로 나누는 경우는? |
| 네트워크 | 연결 실패, 타임아웃, 잘못된 응답은? |
| 반복문 | 종료 조건이 확실히 충족되는가? |

> **Warning:** `except Exception`처럼 너무 넓은 범위로 예외를 잡으면, 의도치 않은 오류까지 숨겨져서 디버깅이 더 어려워질 수 있습니다. 가능하면 `except ValueError`, `except KeyError`처럼 **구체적인 예외 타입**을 지정하세요.

---

### 정리

이번 장에서 배운 핵심 내용을 정리합니다.

**오류의 세 가지 종류:**

1. **구문 오류 (SyntaxError)** -- 문법 규칙 위반. 파이썬이 위치를 정확히 알려줌
2. **런타임 오류 (Runtime Error)** -- 실행 중 발생. 스택 트레이스로 추적 가능
3. **논리 오류 (Logic Error)** -- 오류 메시지 없이 잘못된 결과. 가장 찾기 어려움

**AI에게 디버깅 요청하는 핵심 포인트:**

- 오류 메시지와 코드를 **함께** 보여주세요
- **기대하는 결과**와 **실제 결과**를 알려주세요
- 스택 트레이스가 있다면 **전체를 복사**하세요
- "왜 이런 오류가 발생했는지 설명해 달라"고 요청하면 학습에도 도움이 됩니다

**예방적 디버깅:**

- `try/except`로 예상 가능한 오류를 미리 처리하세요
- 입력값 검증으로 잘못된 데이터가 깊숙이 들어가는 것을 막으세요
- AI에게 "이 코드에서 발생할 수 있는 오류를 모두 찾아줘"라고 요청하세요

> **Note:** 디버깅은 프로그래밍에서 피할 수 없는 과정입니다. 하지만 AI와 함께라면 두렵지 않습니다. 오류 메시지를 AI에게 보여주는 습관만 들이면, 어떤 버그든 빠르게 해결할 수 있습니다. 실수를 두려워하지 마세요. 모든 실수는 배움의 기회입니다.

---

### 다음 장 예고

**Chapter 14: 버전 관리의 첫걸음 -- Git과 AI**

코드를 작성하고 수정하다 보면 "어제 버전이 더 나았는데..."라는 생각이 들 때가 있습니다. 다음 장에서는 코드의 변경 이력을 관리하는 **Git**을 AI와 함께 배워봅니다. AI에게 "Git 초기화해 줘", "변경 사항 커밋해 줘"라고 말하는 것만으로 버전 관리를 시작할 수 있습니다.