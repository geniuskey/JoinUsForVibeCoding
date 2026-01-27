## Chapter 3: 전통적 코딩 vs 바이브 코딩

프로그래밍의 세계에는 이제 두 가지 길이 있습니다. 수십 년간 이어져 온 **전통적 코딩**과 AI 시대에 등장한 **바이브 코딩**입니다. 이 장에서는 두 접근법을 나란히 놓고 비교하며, 각각의 강점과 적합한 상황을 살펴봅니다. 나아가 두 방식을 결합한 **하이브리드 접근법**까지 알아보겠습니다.

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 전통적 코딩과 바이브 코딩의 프로세스 차이를 설명할 수 있다
- 두 접근법의 장단점을 다양한 기준으로 비교할 수 있다
- 상황에 따라 적절한 접근법을 선택할 수 있다
- 하이브리드 접근법을 활용하여 효율적으로 개발할 수 있다

---

### 3.1 전통적 개발 프로세스

전통적 소프트웨어 개발은 오랜 시간에 걸쳐 검증된 체계적인 프로세스를 따릅니다. 일반적으로 다음 다섯 단계로 이루어집니다:

```
요구사항 분석 → 설계 → 구현 → 테스트 → 배포
(Requirements)  (Design) (Implementation) (Testing) (Deployment)
```

**1단계: 요구사항 분석 (Requirements)**
무엇을 만들어야 하는지 정의합니다. 사용자의 요구를 파악하고, 기능 명세서를 작성합니다.

**2단계: 설계 (Design)**
어떻게 만들지 계획합니다. 아키텍처를 결정하고, 데이터 구조와 알고리즘을 선택합니다.

**3단계: 구현 (Implementation)**
설계를 바탕으로 코드를 한 줄씩 직접 작성합니다. 문법, 로직, 자료구조를 모두 개발자가 다룹니다.

**4단계: 테스트 (Testing)**
작성한 코드가 올바르게 동작하는지 검증합니다. 단위 테스트, 통합 테스트 등을 수행합니다.

**5단계: 배포 (Deployment)**
완성된 소프트웨어를 사용자에게 전달합니다.

> **Note:** 전통적 코딩에서는 **개발자가 모든 단계의 주체**입니다. 알고리즘을 이해하고, 문법을 외우고, 디버깅 기술을 갖추어야 합니다.

---

### 3.2 바이브 코딩 프로세스

바이브 코딩은 AI와의 협업을 중심으로 한 새로운 프로세스를 따릅니다:

```
아이디어 → 프롬프트 → 생성 → 검증 → 반복
(Idea)     (Prompt)   (Generate) (Verify) (Iterate)
```

**1단계: 아이디어 (Idea)**
무엇을 만들고 싶은지 떠올립니다. 구체적인 구현 방법은 아직 몰라도 됩니다.

**2단계: 프롬프트 (Prompt)**
AI에게 원하는 것을 자연어로 설명합니다. "리스트를 정렬하는 함수를 만들어줘"처럼 일상적인 말로 요청합니다.

**3단계: 생성 (Generate)**
AI가 코드를 생성합니다. 문법, 알고리즘, 구조를 AI가 처리합니다.

**4단계: 검증 (Verify)**
생성된 코드를 실행하고 결과를 확인합니다. 원하는 대로 동작하는지 점검합니다.

**5단계: 반복 (Iterate)**
부족한 부분이 있으면 추가 요청을 합니다. "에러 처리를 추가해줘", "성능을 개선해줘" 등으로 개선합니다.

> **Tip:** 바이브 코딩에서는 **개발자의 역할이 "구현자"에서 "지휘자"로 바뀝니다.** 코드를 직접 타이핑하는 대신, 무엇을 만들지 방향을 제시하고 결과를 판단합니다.

이 차이를 실제 예제로 확인해보겠습니다.

---

### 3.3 예제로 비교하기: 정렬 알고리즘

같은 문제를 두 가지 방식으로 풀어보면 차이가 명확해집니다. 버블 정렬 알고리즘을 전통적 코딩과 바이브 코딩으로 각각 구현해보겠습니다.

#### 예제 3-1: [전통적 코딩] 버블 정렬 직접 구현

전통적 코딩에서는 개발자가 알고리즘의 원리를 이해하고, 반복문과 조건문을 직접 작성합니다.

```python
# examples/python/chapter01/01_traditional_bubble_sort.py
# 예제 3-1: [전통적 코딩] 버블 정렬 직접 구현
# 개발자가 알고리즘을 이해하고 한 줄씩 직접 작성한 코드

def bubble_sort(arr):
    """버블 정렬: 인접한 두 요소를 비교하여 정렬"""
    # 원본 배열을 변경하지 않기 위해 복사
    result = arr.copy()
    n = len(result)

    # 바깥 루프: 전체 패스 횟수
    for i in range(n - 1):
        # 안쪽 루프: 인접 요소 비교
        for j in range(n - 1 - i):
            # 앞 요소가 뒤 요소보다 크면 교환
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


# 테스트 데이터
numbers = [64, 34, 25, 12, 22, 11, 90]

print("=== 전통적 코딩: 버블 정렬 ===")
print(f"정렬 전: {numbers}")
sorted_numbers = bubble_sort(numbers)
print(f"정렬 후: {sorted_numbers}")
```

**실행:**

```bash
$ python examples/python/chapter01/01_traditional_bubble_sort.py
```

**결과:**

```
=== 전통적 코딩: 버블 정렬 ===
정렬 전: [64, 34, 25, 12, 22, 11, 90]
정렬 후: [11, 12, 22, 25, 34, 64, 90]
```

이 코드를 작성하려면 개발자는 다음을 알아야 합니다:
- 버블 정렬 알고리즘의 원리
- 이중 `for` 루프 사용법
- 파이썬의 다중 대입(swap) 문법
- 리스트 복사 개념

#### 예제 3-2: [바이브 코딩] 정렬 AI에게 요청

바이브 코딩에서는 AI에게 자연어로 요청합니다.

**프롬프트:**
> "리스트를 정렬하는 함수를 만들어줘. 버블 정렬 알고리즘을 사용하고, 각 단계를 출력해줘"

AI가 생성한 결과:

```python
# examples/python/chapter01/02_vibe_bubble_sort.py
# 예제 3-2: [바이브 코딩] 정렬 AI에게 요청
#
# 프롬프트: "리스트를 정렬하는 함수를 만들어줘.
#           버블 정렬 알고리즘을 사용하고, 각 단계를 출력해줘"
#
# 아래는 AI가 생성한 결과물입니다.

def bubble_sort_with_steps(arr):
    """
    버블 정렬을 수행하며 각 단계를 시각적으로 출력합니다.

    Args:
        arr: 정렬할 숫자 리스트
    Returns:
        정렬된 리스트
    """
    result = arr.copy()
    n = len(result)
    total_swaps = 0

    print(f"초기 상태: {result}")
    print(f"배열 길이: {n}")
    print("-" * 50)

    for i in range(n - 1):
        swapped = False
        print(f"\n[패스 {i + 1}]")

        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                print(f"  {result[j]} > {result[j + 1]} -> 교환!", end="")
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
                total_swaps += 1
                print(f"  결과: {result}")
            else:
                print(f"  {result[j]} <= {result[j + 1]} -> 유지")

        if not swapped:
            print("  교환 없음 - 정렬 완료!")
            break

    print("-" * 50)
    print(f"총 교환 횟수: {total_swaps}")
    return result


# 실행
numbers = [64, 34, 25, 12, 22, 11, 90]
print("=== 바이브 코딩: 버블 정렬 (단계별 출력) ===\n")
sorted_numbers = bubble_sort_with_steps(numbers)
print(f"\n최종 결과: {sorted_numbers}")
```

**실행:**

```bash
$ python examples/python/chapter01/02_vibe_bubble_sort.py
```

**결과:**

```
=== 바이브 코딩: 버블 정렬 (단계별 출력) ===

초기 상태: [64, 34, 25, 12, 22, 11, 90]
배열 길이: 7
--------------------------------------------------

[패스 1]
  64 > 34 -> 교환!  결과: [34, 64, 25, 12, 22, 11, 90]
  64 > 25 -> 교환!  결과: [34, 25, 64, 12, 22, 11, 90]
  64 > 12 -> 교환!  결과: [34, 25, 12, 64, 22, 11, 90]
  64 > 22 -> 교환!  결과: [34, 25, 12, 22, 64, 11, 90]
  64 > 11 -> 교환!  결과: [34, 25, 12, 22, 11, 64, 90]
  64 <= 90 -> 유지

[패스 2]
  34 > 25 -> 교환!  결과: [25, 34, 12, 22, 11, 64, 90]
  34 > 12 -> 교환!  결과: [25, 12, 34, 22, 11, 64, 90]
  ...

[패스 6]
  11 <= 12 -> 유지
  교환 없음 - 정렬 완료!
--------------------------------------------------
총 교환 횟수: 14

최종 결과: [11, 12, 22, 25, 34, 64, 90]
```

> **Note:** 같은 버블 정렬이지만 AI가 생성한 버전은 **단계별 시각화**, **조기 종료 최적화(swapped 플래그)**, **교환 횟수 카운팅**, **docstring 문서화**까지 포함합니다. 프롬프트 한 줄로 더 풍부한 결과를 얻었습니다.

---

### 3.4 예제로 비교하기: 단어 빈도 분석

이번에는 텍스트에서 단어 빈도를 분석하는 프로그램을 두 가지 방식으로 만들어보겠습니다.

#### 예제 3-3: [전통적 코딩] 단어 빈도 분석 직접 구현

```python
# examples/python/chapter01/03_traditional_word_frequency.py
# 예제 3-3: [전통적 코딩] 단어 빈도 분석 직접 구현
# 개발자가 문자열 처리 로직을 직접 작성

def count_words(text):
    """텍스트에서 단어 빈도를 분석한다"""
    # 소문자로 변환
    text = text.lower()

    # 구두점 제거
    punctuation = ".,!?;:\"'()-"
    for char in punctuation:
        text = text.replace(char, "")

    # 공백 기준으로 분리
    words = text.split()

    # 빈도 딕셔너리 구성
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


# 테스트 텍스트
sample_text = """
Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.
"""

print("=== 전통적 코딩: 단어 빈도 분석 ===")
print(f"입력 텍스트: {sample_text.strip()}")
print()

result = count_words(sample_text)
print("단어 빈도:")
for word, count in result.items():
    print(f"  {word}: {count}")
```

**실행:**

```bash
$ python examples/python/chapter01/03_traditional_word_frequency.py
```

**결과:**

```
=== 전통적 코딩: 단어 빈도 분석 ===
입력 텍스트: Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.

단어 빈도:
  python: 4
  is: 3
  a: 1
  great: 1
  language: 1
  easy: 1
  to: 1
  learn: 1
  many: 1
  developers: 1
  love: 1
  because: 1
  versatile: 1
```

전통적 방식에서는 문자열 처리, 딕셔너리 조작 등을 모두 직접 구현합니다. 결과는 정확하지만 정렬이나 시각화 기능은 개발자가 추가로 구현해야 합니다.

#### 예제 3-4: [바이브 코딩] 단어 빈도 분석 AI에게 요청

**프롬프트:**
> "텍스트에서 단어 빈도를 분석하는 프로그램을 만들어줘. 빈도순으로 정렬하고, 막대 그래프로 보여줘. 불용어(the, is, a 등)는 제외해줘."

```python
# examples/python/chapter01/04_vibe_word_frequency.py
# 예제 3-4: [바이브 코딩] 단어 빈도 분석 AI에게 요청
#
# 프롬프트: "텍스트에서 단어 빈도를 분석하는 프로그램을 만들어줘.
#           빈도순으로 정렬하고, 막대 그래프로 보여줘.
#           불용어(the, is, a 등)는 제외해줘."
#
# 아래는 AI가 생성한 결과물입니다.

import re
from collections import Counter


# 영어 불용어 목록
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "being", "to", "of", "in", "for", "on", "with", "at", "by",
    "it", "and", "or", "but", "not", "that", "this", "from"
}


def analyze_word_frequency(text, top_n=10, exclude_stop_words=True):
    """
    텍스트의 단어 빈도를 분석하고 시각화합니다.

    Args:
        text: 분석할 텍스트
        top_n: 상위 N개 단어만 표시
        exclude_stop_words: 불용어 제외 여부
    Returns:
        빈도순 정렬된 (단어, 빈도) 리스트
    """
    # 소문자 변환 및 단어 추출 (정규표현식 사용)
    words = re.findall(r'[a-z]+', text.lower())

    # 불용어 필터링
    if exclude_stop_words:
        words = [w for w in words if w not in STOP_WORDS]

    # 빈도 계산 및 정렬
    counter = Counter(words)
    top_words = counter.most_common(top_n)

    return top_words


def display_bar_chart(word_counts, bar_char="█"):
    """단어 빈도를 막대 그래프로 출력합니다."""
    if not word_counts:
        print("  (표시할 데이터 없음)")
        return

    max_count = max(count for _, count in word_counts)
    max_word_len = max(len(word) for word, _ in word_counts)
    bar_width = 30

    for word, count in word_counts:
        bar_length = int((count / max_count) * bar_width)
        bar = bar_char * bar_length
        print(f"  {word:<{max_word_len}} | {bar} ({count})")


# 실행
sample_text = """
Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.
"""

print("=== 바이브 코딩: 단어 빈도 분석 (시각화 포함) ===")
print(f"입력 텍스트: {sample_text.strip()}")
print()

results = analyze_word_frequency(sample_text)

print("단어 빈도 (불용어 제외, 빈도순):")
display_bar_chart(results)
print()
print(f"총 {len(results)}개 단어 분석 완료")
```

**실행:**

```bash
$ python examples/python/chapter01/04_vibe_word_frequency.py
```

**결과:**

```
=== 바이브 코딩: 단어 빈도 분석 (시각화 포함) ===
입력 텍스트: Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.

단어 빈도 (불용어 제외, 빈도순):
  python     | ██████████████████████████████ (4)
  great      | ███████ (1)
  language   | ███████ (1)
  easy       | ███████ (1)
  learn      | ███████ (1)
  many       | ███████ (1)
  developers | ███████ (1)
  love       | ███████ (1)
  because    | ███████ (1)
  versatile  | ███████ (1)

총 10개 단어 분석 완료
```

> **Tip:** AI가 생성한 버전은 **정규표현식**, **Counter 클래스**, **불용어 필터링**, **막대 그래프 시각화**까지 포함합니다. 프롬프트에 원하는 기능을 명시했더니 AI가 적절한 라이브러리와 구조를 선택해주었습니다. 바이브 코딩에서는 **무엇을 원하는지 명확하게 전달하는 것**이 핵심입니다.

---

### 3.5 비교 분석표

두 접근법을 다양한 기준으로 비교해보겠습니다:

| 비교 항목 | 전통적 코딩 | 바이브 코딩 |
|-----------|------------|------------|
| **학습 곡선** | 가파름 (문법, 알고리즘 학습 필요) | 완만함 (자연어로 시작 가능) |
| **개발 속도** | 느림 (한 줄씩 직접 작성) | 빠름 (AI가 초안 즉시 생성) |
| **코드 품질** | 개발자 실력에 비례 | 일정 수준 이상 보장 (AI 학습 기반) |
| **디버깅** | 직접 원인 분석 필요 | AI에게 오류 분석 요청 가능 |
| **유연성** | 완전한 제어 가능 | 프롬프트 표현의 한계 존재 |
| **깊은 이해** | 구현 과정에서 자연히 습득 | 별도 학습 노력 필요 |
| **창의성** | 개발자의 창의력에 의존 | AI가 다양한 패턴 제안 |
| **재현성** | 동일 코드 = 동일 결과 | 같은 프롬프트라도 결과 다를 수 있음 |
| **유지보수** | 작성자가 코드를 잘 이해함 | 생성된 코드 이해에 추가 노력 필요 |

> **Note:** 어느 한쪽이 절대적으로 우월한 것이 아닙니다. **상황에 따라 적절한 도구를 선택하는 것**이 현명한 개발자의 자세입니다.

---

### 3.6 언제 전통적 코딩을 사용할까?

전통적 코딩이 더 적합한 상황이 있습니다:

**1. 안전이 중요한 시스템 (Safety-Critical Systems)**
의료 장비, 항공 시스템, 자율주행 소프트웨어처럼 오류가 생명과 직결되는 분야에서는 모든 코드 라인을 개발자가 직접 이해하고 검증해야 합니다.

**2. 성능이 중요한 시스템 (Performance-Critical)**
게임 엔진, 실시간 처리 시스템 등에서는 메모리 관리와 알고리즘 최적화를 개발자가 세밀하게 제어해야 합니다.

**3. 깊은 이해가 필요한 학습 과정**
컴퓨터 과학의 기초를 배울 때는 직접 구현해보는 과정이 중요합니다. 자료구조와 알고리즘을 손으로 짜봐야 원리를 체득할 수 있습니다.

**4. 기존 코드베이스 유지보수**
레거시 시스템의 복잡한 의존성을 가진 코드를 수정할 때는 전체 맥락을 이해한 개발자의 판단이 필요합니다.

---

### 3.7 언제 바이브 코딩을 사용할까?

바이브 코딩이 빛을 발하는 상황들입니다:

**1. 프로토타이핑 (Prototyping)**
아이디어를 빠르게 구현하여 검증하고 싶을 때, 바이브 코딩으로 몇 분 만에 동작하는 프로토타입을 만들 수 있습니다.

**2. 자동화 스크립트 (Automation Scripts)**
파일 정리, 데이터 변환, 반복 작업 자동화 등 일회성 또는 단순 반복 스크립트를 만들 때 효율적입니다.

**3. 학습 도구로 활용 (Learning)**
새로운 프로그래밍 언어나 라이브러리를 배울 때, AI에게 예제를 요청하고 설명을 받으면 학습 속도가 빨라집니다.

**4. 보일러플레이트 코드 (Boilerplate)**
반복적인 설정 코드, CRUD 작업, 폼 검증 로직 등 패턴이 정해진 코드를 AI에게 맡기면 시간을 절약할 수 있습니다.

---

### 3.8 예제로 비교하기: FizzBuzz

같은 문제를 두 가지 접근법으로 풀었을 때 어떤 차이가 나는지 확인해보겠습니다.

#### 예제 3-5: [비교] 같은 문제, 다른 접근법

FizzBuzz는 프로그래밍 면접에서 자주 나오는 문제입니다. 1부터 N까지 숫자를 출력하되, 3의 배수이면 "Fizz", 5의 배수이면 "Buzz", 15의 배수이면 "FizzBuzz"를 출력합니다.

```python
# examples/python/chapter01/05_comparison_fizzbuzz.py
# 예제 3-5: [비교] 같은 문제, 다른 접근법 - FizzBuzz
# 전통적 코딩과 바이브 코딩으로 각각 구현한 결과를 비교합니다.

# ─── 방법 1: 전통적 코딩 ───
# 개발자가 조건문 로직을 직접 작성
def fizzbuzz_traditional(n):
    """전통적 방식: 직접 조건문 작성"""
    results = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            results.append("FizzBuzz")
        elif i % 3 == 0:
            results.append("Fizz")
        elif i % 5 == 0:
            results.append("Buzz")
        else:
            results.append(str(i))
    return results


# ─── 방법 2: 바이브 코딩 ───
# 프롬프트: "FizzBuzz를 만들어줘. 규칙을 쉽게 추가할 수 있게 해줘."
# AI가 생성한 코드: 확장 가능한 구조
def fizzbuzz_vibe(n, rules=None):
    """바이브 코딩 방식: 확장 가능한 규칙 기반 구조"""
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]

    results = []
    for i in range(1, n + 1):
        output = ""
        for divisor, word in rules:
            if i % divisor == 0:
                output += word
        results.append(output if output else str(i))
    return results


# ─── 비교 실행 ───
print("=== FizzBuzz 비교: 전통적 코딩 vs 바이브 코딩 ===\n")

n = 20

# 전통적 방식 실행
print("[전통적 코딩] 결과:")
traditional = fizzbuzz_traditional(n)
print(", ".join(traditional))

print()

# 바이브 코딩 방식 실행 (기본 규칙)
print("[바이브 코딩] 기본 규칙 결과:")
vibe_basic = fizzbuzz_vibe(n)
print(", ".join(vibe_basic))

# 바이브 코딩 방식 실행 (규칙 확장)
print()
print("[바이브 코딩] 규칙 확장 (7=Jazz 추가) 결과:")
custom_rules = [(3, "Fizz"), (5, "Buzz"), (7, "Jazz")]
vibe_extended = fizzbuzz_vibe(n, rules=custom_rules)
print(", ".join(vibe_extended))

print()
print("─" * 50)
print("비교 요약:")
print("  전통적 코딩: 간단명료하지만 규칙 추가 시 코드 수정 필요")
print("  바이브 코딩:  확장 가능한 구조로 규칙 추가가 쉬움")
```

**실행:**

```bash
$ python examples/python/chapter01/05_comparison_fizzbuzz.py
```

**결과:**

```
=== FizzBuzz 비교: 전통적 코딩 vs 바이브 코딩 ===

[전통적 코딩] 결과:
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, 16, 17, Fizz, 19, Buzz

[바이브 코딩] 기본 규칙 결과:
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, 16, 17, Fizz, 19, Buzz

[바이브 코딩] 규칙 확장 (7=Jazz 추가) 결과:
1, 2, Fizz, 4, Buzz, Fizz, Jazz, 8, Fizz, Buzz, 11, Fizz, 13, Jazz, FizzBuzz, 16, 17, Fizz, 19, Buzz

──────────────────────────────────────────────────
비교 요약:
  전통적 코딩: 간단명료하지만 규칙 추가 시 코드 수정 필요
  바이브 코딩:  확장 가능한 구조로 규칙 추가가 쉬움
```

두 방식 모두 기본 FizzBuzz를 정확히 수행합니다. 하지만 바이브 코딩으로 생성된 버전은 **규칙 기반(rule-based) 구조**를 갖추고 있어, 새로운 규칙(7의 배수에 "Jazz")을 코드 수정 없이 데이터만으로 추가할 수 있습니다.

> **Tip:** 바이브 코딩의 강점은 단순히 코드를 빨리 만드는 것이 아닙니다. AI는 다양한 코드 패턴을 학습했기 때문에, **더 확장 가능하고 유지보수하기 좋은 구조**를 제안하는 경우가 많습니다.

---

### 3.9 하이브리드 접근법

실제 개발 현장에서는 전통적 코딩과 바이브 코딩을 **함께 사용하는 하이브리드 접근법**이 가장 효과적입니다.

하이브리드 접근법의 핵심 원리는 다음과 같습니다:

```
AI가 초안을 생성한다 → 개발자가 검토한다 → 개발자가 직접 개선한다
```

이 접근법이 강력한 이유는:
- **AI의 강점** (빠른 생성, 다양한 패턴 활용)과
- **사람의 강점** (맥락 이해, 품질 판단, 엣지 케이스 처리)을

동시에 활용할 수 있기 때문입니다.

#### 예제 3-6: [하이브리드] AI 초안 + 수동 개선

온도 변환기를 하이브리드 방식으로 만들어보겠습니다. AI가 기본 변환 로직을 생성하고, 개발자가 입력 검증과 에러 처리를 추가합니다.

```python
# examples/python/chapter01/06_hybrid_temperature.py
# 예제 3-6: [하이브리드] AI 초안 + 수동 개선
# 1단계: AI가 생성한 온도 변환기 초안
# 2단계: 개발자가 입력 검증 및 에러 처리를 수동으로 추가

# ─── 1단계: AI 생성 초안 (기본 기능) ───
def convert_temperature_draft(value, from_unit, to_unit):
    """AI가 생성한 초안: 기본 온도 변환"""
    if from_unit == "C" and to_unit == "F":
        return value * 9 / 5 + 32
    elif from_unit == "F" and to_unit == "C":
        return (value - 32) * 5 / 9
    elif from_unit == "C" and to_unit == "K":
        return value + 273.15
    elif from_unit == "K" and to_unit == "C":
        return value - 273.15
    elif from_unit == "F" and to_unit == "K":
        return (value - 32) * 5 / 9 + 273.15
    elif from_unit == "K" and to_unit == "F":
        return (value - 273.15) * 9 / 5 + 32
    elif from_unit == to_unit:
        return value
    else:
        return None


# ─── 2단계: 개발자가 개선한 버전 (검증 + 에러 처리) ───
VALID_UNITS = {"C": "섭씨(Celsius)", "F": "화씨(Fahrenheit)", "K": "켈빈(Kelvin)"}
ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67, "K": 0}


def convert_temperature(value, from_unit, to_unit):
    """개선된 버전: 입력 검증 + 에러 처리 추가"""
    # [수동 추가] 단위 유효성 검증
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if from_unit not in VALID_UNITS:
        raise ValueError(
            f"잘못된 입력 단위: '{from_unit}'. "
            f"가능한 단위: {', '.join(VALID_UNITS.keys())}"
        )
    if to_unit not in VALID_UNITS:
        raise ValueError(
            f"잘못된 출력 단위: '{to_unit}'. "
            f"가능한 단위: {', '.join(VALID_UNITS.keys())}"
        )

    # [수동 추가] 숫자 타입 검증
    if not isinstance(value, (int, float)):
        raise TypeError(f"숫자를 입력해야 합니다. 입력값: {value}")

    # [수동 추가] 절대 영도 이하 검증
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ValueError(
            f"절대 영도({ABSOLUTE_ZERO[from_unit]}{from_unit}) 이하의 "
            f"온도는 존재할 수 없습니다. 입력값: {value}{from_unit}"
        )

    # [AI 초안] 변환 로직
    result = convert_temperature_draft(value, from_unit, to_unit)
    return round(result, 2)


# ─── 테스트 실행 ───
print("=== 하이브리드 접근법: AI 초안 + 수동 개선 ===\n")

# 정상 변환 테스트
test_cases = [
    (100, "C", "F"),
    (212, "F", "C"),
    (0, "C", "K"),
    (300, "K", "C"),
]

print("[정상 변환 테스트]")
for value, from_u, to_u in test_cases:
    result = convert_temperature(value, from_u, to_u)
    print(f"  {value}{from_u} -> {result}{to_u}")

# 에러 처리 테스트 (수동 개선 부분)
print("\n[에러 처리 테스트 - 수동 개선 부분]")

error_cases = [
    ("잘못된 단위", 100, "X", "F"),
    ("절대 영도 이하", -300, "C", "F"),
    ("잘못된 타입", "뜨거움", "C", "F"),
]

for desc, *args in error_cases:
    try:
        convert_temperature(*args)
    except (ValueError, TypeError) as e:
        print(f"  {desc}: {e}")

print("\n" + "─" * 50)
print("하이브리드 접근법 요약:")
print("  AI 기여  -> 변환 공식 및 기본 구조 생성")
print("  사람 기여 -> 입력 검증, 에러 처리, 경계값 확인 추가")
```

**실행:**

```bash
$ python examples/python/chapter01/06_hybrid_temperature.py
```

**결과:**

```
=== 하이브리드 접근법: AI 초안 + 수동 개선 ===

[정상 변환 테스트]
  100C -> 212.0F
  212F -> 100.0C
  0C -> 273.15K
  300K -> 26.85C

[에러 처리 테스트 - 수동 개선 부분]
  잘못된 단위: 잘못된 입력 단위: 'X'. 가능한 단위: C, F, K
  절대 영도 이하: 절대 영도(-273.15C) 이하의 온도는 존재할 수 없습니다. 입력값: -300C
  잘못된 타입: 숫자를 입력해야 합니다. 입력값: 뜨거움

──────────────────────────────────────────────────
하이브리드 접근법 요약:
  AI 기여  -> 변환 공식 및 기본 구조 생성
  사람 기여 -> 입력 검증, 에러 처리, 경계값 확인 추가
```

이 예제에서 주목할 점은 코드 내의 `[수동 추가]`와 `[AI 초안]` 주석입니다. AI가 만든 부분과 개발자가 추가한 부분이 명확히 구분됩니다:

- **AI 기여**: 6가지 온도 단위 간 변환 공식, 기본 함수 구조
- **사람 기여**: 유효하지 않은 단위 검증, 절대 영도 경계값 확인, 타입 검증, 에러 메시지 한국어화

> **Note:** 하이브리드 접근법에서 개발자의 핵심 역할은 **"AI가 놓치기 쉬운 부분을 채워 넣는 것"**입니다. AI는 정상 경로(happy path)는 잘 처리하지만, 엣지 케이스와 에러 처리는 도메인 지식을 가진 개발자가 보완하는 것이 효과적입니다.

---

### 실습: 나만의 비교 실험

다음 과제를 직접 수행해보세요:

1. **직접 구현**: 1부터 100까지의 소수(Prime Number)를 출력하는 프로그램을 전통적 코딩 방식으로 직접 작성해보세요.
2. **AI에게 요청**: 같은 프로그램을 AI에게 요청해보세요. "1부터 100까지의 소수를 찾아서 출력하는 프로그램을 만들어줘"
3. **비교**: 두 코드의 차이점을 분석해보세요.
   - 어떤 알고리즘을 사용했나요?
   - 코드 길이는 어떻게 다른가요?
   - 어떤 추가 기능이 포함되었나요?
4. **하이브리드**: AI가 생성한 코드에 직접 기능을 추가해보세요 (예: 소수의 개수 표시, 쌍둥이 소수 찾기 등).

---

### 정리

이 장에서 배운 핵심 내용을 정리합니다:

**전통적 코딩과 바이브 코딩의 차이**
- 전통적 코딩: 요구사항 분석 → 설계 → 구현 → 테스트 → 배포
- 바이브 코딩: 아이디어 → 프롬프트 → 생성 → 검증 → 반복
- 개발자의 역할이 "구현자"에서 "지휘자"로 변화

**각 접근법의 적합한 상황**
- 전통적 코딩: 안전 중요 시스템, 성능 최적화, 깊은 학습, 레거시 유지보수
- 바이브 코딩: 프로토타이핑, 자동화 스크립트, 학습 도구, 보일러플레이트 코드

**하이브리드 접근법**
- AI가 초안을 생성하고, 사람이 검토하고 개선하는 방식
- AI의 속도와 사람의 판단력을 동시에 활용
- 실무에서 가장 효과적인 접근법

> **Tip:** 좋은 개발자는 도구를 가리지 않습니다. 전통적 코딩과 바이브 코딩은 경쟁 관계가 아니라 **상호 보완 관계**입니다. 상황에 맞는 도구를 선택하는 능력이야말로 AI 시대 개발자의 핵심 역량입니다.

---

### 다음 장 예고

**Chapter 4: AI 어시스턴트 이해하기**에서는 바이브 코딩의 핵심 파트너인 AI 어시스턴트를 자세히 살펴봅니다. Claude Code, GitHub Copilot, Cursor 등 주요 도구의 특징을 비교하고, AI의 강점과 한계를 이해하여 더 효과적으로 협업하는 방법을 배웁니다.
