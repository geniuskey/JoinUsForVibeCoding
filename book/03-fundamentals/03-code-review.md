# Chapter 12: 코드 리뷰와 수정

AI가 생성한 코드를 받았을 때 가장 먼저 해야 할 일은 무엇일까요? 바로 **코드를 검토하는 것**입니다. 바이브 코딩은 AI에게 코드 생성을 맡기지만, 그 코드의 품질을 판단하고 개선을 요청하는 것은 여전히 우리의 몫입니다. 이번 챕터에서는 AI가 생성한 코드를 효과적으로 검토하고, 더 나은 코드로 개선하는 방법을 배웁니다. 직접 코드를 수정하는 것이 아니라 AI에게 올바른 방향으로 수정을 요청하는 것이 바이브 코딩의 핵심입니다.

---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- AI가 생성한 코드를 비판적으로 검토할 수 있다
- 체크리스트를 활용하여 코드 품질을 체계적으로 평가할 수 있다
- AI에게 "이 코드 설명해줘"라고 요청하여 코드를 이해할 수 있다
- 구체적인 개선 요청으로 코드 품질을 높일 수 있다
- 코드 스타일을 일관되게 맞출 수 있다
- AI에게 리팩토링을 요청하여 코드 구조를 개선할 수 있다

---

## 12.1 AI 생성 코드, 믿어도 될까?

AI가 생성한 코드는 대부분의 경우 잘 동작합니다. 하지만 **"동작하는 코드"와 "좋은 코드"는 다릅니다.** AI가 만든 코드를 그대로 사용하면 다음과 같은 문제가 발생할 수 있습니다.

### 왜 검토가 필요한가?

**첫째, AI는 맥락을 완벽히 이해하지 못할 수 있습니다.** AI는 여러분의 프로젝트 전체 구조, 팀의 코딩 컨벤션, 비즈니스 요구사항의 미묘한 차이를 알지 못합니다. 결과적으로 기능은 맞지만 프로젝트에 어울리지 않는 코드가 나올 수 있습니다.

**둘째, 변수명과 함수명이 불명확할 수 있습니다.** AI는 종종 `a`, `b`, `temp` 같은 짧은 변수명을 사용하거나, 기능에 비해 너무 일반적인 이름을 붙이기도 합니다.

**셋째, 코드가 필요 이상으로 복잡할 수 있습니다.** AI는 때때로 단순한 문제에 과도하게 복잡한 해결책을 제시하거나, 반대로 에러 처리를 생략하기도 합니다.

### 검토의 세 가지 원칙

바이브 코딩에서 코드를 검토할 때 기억해야 할 세 가지 원칙이 있습니다.

1. **이해하지 못하는 코드는 사용하지 않는다** -- AI가 생성한 코드라도 각 줄이 무슨 일을 하는지 이해해야 합니다. 이해하지 못하면 AI에게 설명을 요청하세요.

2. **동작 확인은 필수다** -- 코드를 받으면 반드시 실행하여 기대한 결과가 나오는지 확인합니다. 다양한 입력 값으로 테스트해 보세요.

3. **개선은 대화로 한다** -- 문제를 발견하면 직접 코드를 수정하기보다, AI에게 구체적으로 무엇이 문제인지 설명하고 개선을 요청하는 것이 바이브 코딩의 방식입니다.

> **Note:** AI가 생성한 코드를 무조건 의심하라는 것이 아닙니다. 다만 "맹목적 신뢰"보다는 "검증된 신뢰"가 중요합니다. 처음에는 꼼꼼히 검토하되, AI의 패턴을 이해하게 되면 점차 효율적으로 검토할 수 있게 됩니다.

---

## 12.2 코드 검토 체크리스트

AI가 생성한 코드를 받았을 때, 무엇부터 확인해야 할지 막막할 수 있습니다. 다음 체크리스트를 활용하면 체계적으로 코드를 검토할 수 있습니다.

### 기본 검토 항목

| 검토 항목 | 확인 질문 | 중요도 |
|-----------|-----------|--------|
| **정확성** | 코드가 요청한 기능을 올바르게 수행하는가? | 필수 |
| **실행 가능성** | 에러 없이 실행되는가? | 필수 |
| **가독성** | 코드를 읽고 이해할 수 있는가? | 높음 |
| **변수명** | 변수와 함수의 이름이 의미를 잘 전달하는가? | 높음 |
| **에러 처리** | 잘못된 입력이나 예외 상황을 처리하는가? | 높음 |
| **코드 스타일** | 프로젝트의 코딩 컨벤션과 일치하는가? | 중간 |
| **중복** | 불필요하게 반복되는 코드가 있는가? | 중간 |
| **효율성** | 불필요하게 느리거나 메모리를 많이 사용하는가? | 낮음 |

### 단계별 검토 흐름

검토는 다음 순서로 진행하는 것이 효율적입니다.

**1단계: 먼저 실행한다.** 코드를 받으면 바로 실행하여 기본 동작을 확인합니다. 에러가 발생하면 AI에게 에러 메시지를 전달하고 수정을 요청합니다.

**2단계: 코드를 읽는다.** 실행이 성공하면 코드를 처음부터 끝까지 읽습니다. 이해가 되지 않는 부분이 있으면 AI에게 설명을 요청합니다.

**3단계: 이름을 확인한다.** 변수명, 함수명, 클래스명이 명확한지 확인합니다. `a`, `tmp`, `data` 같은 모호한 이름이 있으면 개선을 요청합니다.

**4단계: 구조를 점검한다.** 하나의 함수가 너무 많은 일을 하고 있지는 않은지, 중복 코드가 있지는 않은지 확인합니다.

**5단계: 엣지 케이스를 테스트한다.** 빈 입력, 매우 큰 값, 잘못된 타입 등 예외적인 상황에서도 코드가 올바르게 동작하는지 확인합니다.

> **Tip:** 모든 항목을 매번 완벽하게 검토할 필요는 없습니다. 코드의 중요도와 복잡도에 따라 검토의 깊이를 조절하세요. 간단한 유틸리티 함수는 1~2단계만으로도 충분할 수 있고, 핵심 비즈니스 로직은 5단계까지 꼼꼼히 검토해야 합니다.

---

## 12.3 "이 코드 설명해줘" 활용

AI가 생성한 코드가 복잡하거나 이해하기 어려울 때, 가장 효과적인 방법은 AI에게 직접 설명을 요청하는 것입니다. "이 코드 설명해줘"라는 간단한 요청만으로 코드의 동작 원리를 단계별로 파악할 수 있습니다.

### 예제 12-1: 생성된 코드 설명 요청

AI가 "연속으로 증가하는 가장 긴 구간을 찾는 함수"를 생성했다고 가정합시다. 처음 보면 복잡해 보이는 이 코드를 AI에게 설명해달라고 요청합니다.

**AI에게 보낸 요청:**

```
이 코드가 무엇을 하는지 설명해줘
```

**원본 코드 (처음 보면 복잡해 보임):**

```python
# examples/python/chapter03/ex12_01_explain_code.py
def find_longest_streak(data):
    """연속으로 증가하는 가장 긴 구간을 찾습니다."""
    if not data:
        return []

    best_start, best_length = 0, 1
    curr_start, curr_length = 0, 1

    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            curr_length += 1
        else:
            if curr_length > best_length:
                best_start = curr_start
                best_length = curr_length
            curr_start = i
            curr_length = 1

    if curr_length > best_length:
        best_start = curr_start
        best_length = curr_length

    return data[best_start:best_start + best_length]
```

**AI가 설명을 추가한 버전:**

```python
# examples/python/chapter03/ex12_01_explain_code.py
def find_longest_streak_explained(data):
    """
    [AI 설명] 연속으로 증가하는 가장 긴 구간을 찾는 함수입니다.

    동작 원리:
    1. 리스트를 처음부터 끝까지 순회합니다.
    2. 현재 값이 이전 값보다 크면 → 연속 증가 구간이 계속됩니다.
    3. 현재 값이 이전 값 이하이면 → 증가 구간이 끊어집니다.
    4. 끊어질 때마다, 지금까지 가장 긴 구간과 비교합니다.
    5. 최종적으로 가장 긴 연속 증가 구간을 반환합니다.

    예시: [3, 1, 2, 4, 7, 2, 5] → [1, 2, 4, 7] (길이 4)
    """
    if not data:
        return []

    # 가장 긴 구간의 시작 위치와 길이
    best_start = 0
    best_length = 1

    # 현재 탐색 중인 구간의 시작 위치와 길이
    curr_start = 0
    curr_length = 1

    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            # 아직 증가 중 → 현재 구간 연장
            curr_length += 1
        else:
            # 증가가 끊김 → 최장 기록 갱신 확인
            if curr_length > best_length:
                best_start = curr_start
                best_length = curr_length
            # 새로운 구간 시작
            curr_start = i
            curr_length = 1

    # 마지막 구간이 최장일 수 있으므로 한 번 더 확인
    if curr_length > best_length:
        best_start = curr_start
        best_length = curr_length

    return data[best_start:best_start + best_length]
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_01_explain_code.py
```

**결과:**

```
=======================================================
[예제 12-1] 생성된 코드 설명 요청
=======================================================

입력 데이터: [3, 1, 2, 4, 7, 2, 5]

[원본 코드 실행 결과]
  가장 긴 연속 증가 구간: [1, 2, 4, 7]

[설명 추가 버전 실행 결과]
  가장 긴 연속 증가 구간: [1, 2, 4, 7]

[추가 테스트]
  [5, 4, 3, 2, 1] → [5]
  [1, 2, 3, 4, 5] → [1, 2, 3, 4, 5]
  [10, 20, 5, 6, 7, 8, 9, 1] → [5, 6, 7, 8, 9]

Tip: AI에게 '이 코드 설명해줘'라고 요청하면
     복잡한 코드도 단계별로 이해할 수 있습니다.
```

AI가 설명을 추가한 버전을 보면, 원래 코드와 완전히 동일한 동작을 하면서도 각 단계의 역할이 주석으로 명확하게 표현되어 있습니다. `best_start, best_length = 0, 1`이라는 한 줄이 "가장 긴 구간의 시작 위치와 길이"라는 설명 덕분에 훨씬 쉽게 이해됩니다.

### 예제 12-2: 각 줄 주석 추가 요청

코드의 전체적인 흐름뿐만 아니라, 특정 줄의 의미를 하나하나 이해하고 싶을 때는 "각 줄마다 주석을 달아줘"라고 요청할 수 있습니다.

**AI에게 보낸 요청:**

```
각 줄마다 주석을 달아서 설명해줘
```

**주석 없는 원본 코드:**

```python
# examples/python/chapter03/ex12_02_add_comments.py
def caesar_cipher_original(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            result += char
    return result
```

**주석이 추가된 버전:**

```python
# examples/python/chapter03/ex12_02_add_comments.py
def caesar_cipher_commented(text, shift):
    # 암호화된 결과를 저장할 빈 문자열
    result = ""

    # 입력 텍스트의 각 문자를 순회
    for char in text:
        # 알파벳 문자인 경우에만 암호화 수행
        if char.isalpha():
            # 대문자면 'A'(65), 소문자면 'a'(97)를 기준점으로 설정
            base = ord('A') if char.isupper() else ord('a')

            # 현재 문자를 기준점 기준 상대 위치로 변환 후 shift만큼 이동
            # % 26으로 알파벳 범위(0~25) 내에서 순환되도록 처리
            shifted = (ord(char) - base + shift) % 26

            # 이동된 위치를 다시 문자로 변환하여 결과에 추가
            result += chr(base + shifted)
        else:
            # 알파벳이 아닌 문자(공백, 숫자, 특수문자)는 그대로 유지
            result += char

    # 완성된 암호화 문자열 반환
    return result
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_02_add_comments.py
```

**결과:**

```
=======================================================
[예제 12-2] 각 줄 주석 추가 요청
=======================================================

원본 텍스트: Hello, Vibe Coding!
시프트 값:   3

[주석 없는 버전] 암호화: Khoor, Yleh Frglqj!
[주석 있는 버전] 암호화: Khoor, Yleh Frglqj!

복호화 결과: Hello, Vibe Coding!

[비교: 주석 전 vs 후]
-------------------------------------------------------
주석 없는 코드:
  shifted = (ord(char) - base + shift) % 26

주석 있는 코드:
  # 현재 문자를 기준점 기준 상대 위치로 변환 후 shift만큼 이동
  # % 26으로 알파벳 범위(0~25) 내에서 순환되도록 처리
  shifted = (ord(char) - base + shift) % 26

Tip: 주석이 있으면 나중에 코드를 다시 볼 때
     훨씬 빠르게 이해할 수 있습니다.
```

`(ord(char) - base + shift) % 26`이라는 수식은 처음 보면 무슨 뜻인지 파악하기 어렵습니다. 하지만 "현재 문자를 기준점 기준 상대 위치로 변환 후 shift만큼 이동"이라는 주석이 달리면, 이 코드가 시저 암호의 문자 이동 로직이라는 것을 바로 이해할 수 있습니다.

> **Tip:** "이 코드 설명해줘"와 "각 줄마다 주석을 달아줘"는 학습 도구로도 매우 유용합니다. AI가 생성한 코드의 패턴을 반복적으로 학습하면, 시간이 지남에 따라 비슷한 코드를 직접 이해할 수 있게 됩니다.

---

## 12.4 개선 요청하기

AI가 생성한 코드가 동작은 하지만 품질이 만족스럽지 않을 때, 구체적인 개선을 요청할 수 있습니다. 핵심은 **무엇이 문제인지를 명확하게 설명하는 것**입니다.

### 예제 12-3: 변수명 개선 요청

가장 흔한 개선 요청 중 하나는 변수명 개선입니다. AI가 의미 없는 짧은 변수명을 사용했다면, "변수명을 더 의미 있게 바꿔줘"라고 요청합니다.

**AI에게 보낸 요청:**

```
변수명을 더 의미 있게 바꿔줘
```

**개선 전 -- 의미 없는 변수명:**

```python
# examples/python/chapter03/ex12_03_improve_names.py
def calc_before(a, b, c, d):
    """무엇을 계산하는지 변수명만으로는 알 수 없음"""
    t = a * b
    t2 = c * d
    r = t + t2
    p = r * 0.1
    f = r + p
    return f
```

**개선 후 -- 명확한 변수명:**

```python
# examples/python/chapter03/ex12_03_improve_names.py
def calculate_total_price(item_price, item_quantity, shipping_fee, shipping_count):
    """주문 총액을 계산합니다 (상품 금액 + 배송비 + 세금 포함)."""
    item_subtotal = item_price * item_quantity
    shipping_subtotal = shipping_fee * shipping_count
    order_total_before_tax = item_subtotal + shipping_subtotal
    tax_amount = order_total_before_tax * 0.1
    final_total = order_total_before_tax + tax_amount
    return final_total
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_03_improve_names.py
```

**결과:**

```
=======================================================
[예제 12-3] 변수명 개선 요청
=======================================================

[개선 전] calc_before(15000, 3, 3000, 1)
  결과: 52,800원
  → 함수명과 변수명만으로는 의미 파악 불가

[개선 후] calculate_total_price(15000, 3, 3000, 1)
  결과: 52,800원
  → 함수명과 변수명으로 의미가 명확함

[변수명 비교표]
-------------------------------------------------------
  개선 전       개선 후                      의미
  ---------- ------------------------- ------------
  a          item_price                상품 단가
  b          item_quantity             상품 수량
  c          shipping_fee              배송비 단가
  d          shipping_count            배송 횟수
  t          item_subtotal             상품 소계
  t2         shipping_subtotal         배송비 소계
  r          order_total_before_tax    세전 합계
  p          tax_amount                세금
  f          final_total               최종 합계

Tip: 변수명은 '6개월 후의 내가 봐도 이해할 수 있는가?'를
     기준으로 작성하세요.
```

두 코드의 실행 결과는 동일하게 52,800원입니다. 하지만 개선 전 코드에서는 `a`, `b`, `c`, `d`가 각각 무엇을 의미하는지 함수를 읽는 것만으로는 알 수 없습니다. 개선 후 코드에서는 `item_price`, `item_quantity`처럼 변수명 자체가 역할을 설명합니다.

### 예제 12-4: 함수 분리 요청

하나의 함수가 유효성 검사, 가격 계산, 할인 적용, 배송비 계산, 영수증 출력까지 모든 것을 담당하고 있다면, AI에게 기능별로 함수를 분리해달라고 요청할 수 있습니다.

**AI에게 보낸 요청:**

```
이 함수가 너무 길어. 기능별로 함수를 분리해줘
```

**개선 전 -- 하나의 거대한 함수:**

```python
# examples/python/chapter03/ex12_04_extract_functions.py
def process_order_before(items, customer_name):
    """하나의 함수가 너무 많은 일을 합니다."""
    # 유효성 검사
    if not items:
        print("오류: 주문 항목이 비어 있습니다.")
        return None
    if not customer_name:
        print("오류: 고객 이름이 비어 있습니다.")
        return None

    # 가격 계산
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]

    # 할인 적용
    if subtotal >= 50000:
        discount = subtotal * 0.1
    elif subtotal >= 30000:
        discount = subtotal * 0.05
    else:
        discount = 0

    total = subtotal - discount

    # 배송비 계산
    if total >= 30000:
        shipping = 0
    else:
        shipping = 3000

    final_total = total + shipping

    # 영수증 출력
    print(f"===== 주문 영수증 =====")
    print(f"고객: {customer_name}")
    # ... (출력 코드 계속)
    return final_total
```

**개선 후 -- 기능별로 분리된 함수:**

```python
# examples/python/chapter03/ex12_04_extract_functions.py
def validate_order(items, customer_name):
    """주문 유효성을 검사합니다."""
    if not items:
        print("오류: 주문 항목이 비어 있습니다.")
        return False
    if not customer_name:
        print("오류: 고객 이름이 비어 있습니다.")
        return False
    return True


def calculate_subtotal(items):
    """상품 소계를 계산합니다."""
    return sum(item["price"] * item["quantity"] for item in items)


def calculate_discount(subtotal):
    """금액에 따른 할인액을 계산합니다."""
    if subtotal >= 50000:
        return subtotal * 0.1
    elif subtotal >= 30000:
        return subtotal * 0.05
    return 0


def calculate_shipping(total_after_discount):
    """배송비를 계산합니다 (3만원 이상 무료배송)."""
    return 0 if total_after_discount >= 30000 else 3000


def process_order_after(items, customer_name):
    """주문을 처리합니다 (분리된 함수 활용)."""
    if not validate_order(items, customer_name):
        return None

    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal)
    total_after_discount = subtotal - discount
    shipping = calculate_shipping(total_after_discount)
    final_total = total_after_discount + shipping

    print_receipt(customer_name, items, subtotal, discount, shipping, final_total)
    return final_total
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_04_extract_functions.py
```

**결과:**

```
=======================================================
[예제 12-4] 함수 분리 요청
=======================================================

[개선 전] 하나의 큰 함수로 처리
------------------------------
===== 주문 영수증 =====
고객: 김바이브
-----------------------
  키보드 x1: 25,000원
  마우스 x2: 30,000원
-----------------------
소계:         55,000원
할인:         -5,500원
배송비:            0원
=======================
총액:         49,500원

[개선 후] 기능별로 분리된 함수로 처리
------------------------------
===== 주문 영수증 =====
고객: 김바이브
-----------------------
  키보드 x1: 25,000원
  마우스 x2: 30,000원
-----------------------
소계:         55,000원
할인:         -5,500원
배송비:            0원
=======================
총액:         49,500원

[함수 분리 결과]
  process_order_before → 1개 함수 (약 40줄)
  process_order_after  → 6개 함수 (각 5~15줄)

  분리된 함수 목록:
    1. validate_order()      — 유효성 검사
    2. calculate_subtotal()  — 소계 계산
    3. calculate_discount()  — 할인 계산
    4. calculate_shipping()  — 배송비 계산
    5. print_receipt()       — 영수증 출력
    6. process_order_after() — 전체 흐름 관리

Tip: 함수는 '하나의 함수 = 하나의 역할' 원칙을 따르세요.
     이름만 보고도 무엇을 하는 함수인지 알 수 있어야 합니다.
```

개선 전에는 약 40줄짜리 하나의 함수가 유효성 검사부터 영수증 출력까지 모든 일을 담당했습니다. 개선 후에는 6개의 작은 함수로 나뉘어 각 함수가 하나의 역할만 수행합니다. 결과는 동일하지만, 나중에 할인 정책을 변경하고 싶다면 `calculate_discount()` 함수만 수정하면 됩니다.

### 효과적인 개선 요청 패턴

AI에게 개선을 요청할 때, 다음과 같은 구체적인 표현을 사용하면 더 좋은 결과를 얻을 수 있습니다.

| 상황 | 요청 예시 |
|------|-----------|
| 변수명이 불명확할 때 | "변수명을 더 의미 있는 이름으로 바꿔줘" |
| 함수가 너무 길 때 | "이 함수를 기능별로 작은 함수로 분리해줘" |
| 중복 코드가 있을 때 | "중복되는 코드를 공통 함수로 묶어줘" |
| 조건문이 복잡할 때 | "중첩된 if문을 얼리 리턴으로 바꿔줘" |
| 에러 처리가 없을 때 | "예외 상황에 대한 에러 처리를 추가해줘" |
| 주석이 없을 때 | "각 함수에 docstring과 주석을 추가해줘" |

> **Note:** 개선 요청은 한 번에 하나씩 하는 것이 좋습니다. "변수명도 바꾸고, 함수도 분리하고, 에러 처리도 추가해줘"라고 한꺼번에 요청하면 AI가 혼란스러워할 수 있습니다. 단계별로 하나씩 요청하고, 각 단계의 결과를 확인한 후 다음 요청을 진행하세요.

---

## 12.5 코드 스타일 맞추기

코드 스타일이 일관되지 않으면 여러 사람이 작성한 것처럼 보이고, 읽기 어려워집니다. AI가 생성한 코드는 때때로 스타일이 뒤섞여 있을 수 있습니다. 이때 AI에게 스타일 통일을 요청하면 깔끔하게 정리할 수 있습니다.

### 예제 12-5: 코드 스타일 통일 요청

다음 코드는 의도적으로 다양한 명명 규칙이 혼용된 예시입니다. 클래스명은 camelCase, 메서드명은 PascalCase, 딕셔너리 키는 세 가지 스타일이 뒤섞여 있습니다.

**AI에게 보낸 요청:**

```
코드 스타일이 뒤섞여 있어. PEP8 기준으로 통일해줘
```

**개선 전 -- 스타일이 뒤섞인 코드:**

```python
# examples/python/chapter03/ex12_05_consistent_style.py
class userProfile:                      # 클래스명: camelCase (잘못됨)
    def __init__(self, UserName, email): # 매개변수: PascalCase 혼용
        self.UserName=UserName           # 공백 없음
        self.email = email
        self.loginCount=0                # 공백 없음

    def GetDisplayName(self):            # 메서드: PascalCase (잘못됨)
        return self.UserName

    def get_info_dict(self):
        return {"userName": self.UserName,  # 키: camelCase
                "Email": self.email,         # 키: PascalCase
                "login_count": self.loginCount}  # 키: snake_case
```

**개선 후 -- PEP8 규칙이 적용된 코드:**

```python
# examples/python/chapter03/ex12_05_consistent_style.py
class UserProfile:                              # PascalCase 클래스명
    """사용자 프로필을 관리하는 클래스."""

    def __init__(self, username, email):         # snake_case 매개변수
        self.username = username                 # 공백 일관됨
        self.email = email
        self.login_count = 0                     # snake_case 속성

    def get_display_name(self):                  # snake_case 메서드
        """화면에 표시할 이름을 반환합니다."""
        return self.username

    def get_info_dict(self):
        """프로필 정보를 딕셔너리로 반환합니다."""
        return {
            "username": self.username,           # snake_case 키 통일
            "email": self.email,
            "login_count": self.login_count,
        }
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_05_consistent_style.py
```

**결과:**

```
=======================================================
[예제 12-5] 코드 스타일 통일 요청
=======================================================

[개선 전] 스타일이 뒤섞인 코드
----------------------------------------
  클래스명:   userProfile (camelCase)
  메서드명:   GetDisplayName (PascalCase)
  표시 이름:  홍길동
  정보 딕셔너리: {'userName': '홍길동', 'Email': 'hong@example.com', 'login_count': 2}
  → 키 스타일이 뒤섞임: userName, Email, login_count

[개선 후] PEP8 통일 코드
----------------------------------------
  클래스명:   UserProfile (PascalCase)
  메서드명:   get_display_name (snake_case)
  표시 이름:  홍길동
  정보 딕셔너리: {'username': '홍길동', 'email': 'hong@example.com', 'login_count': 2}
  → 키 스타일 통일: username, email, login_count

[PEP8 명명 규칙 요약]
-------------------------------------------------------
  항목           잘못된 예              올바른 예                규칙
  ------------ ------------------ -------------------- ------------
  클래스명         userProfile        UserProfile          PascalCase
  함수/메서드       GetDisplayName     get_display_name     snake_case
  변수/속성        loginCount         login_count          snake_case
  매개변수         UserName           username             snake_case
  상수           maxRetry           MAX_RETRY            UPPER_SNAKE

Tip: AI에게 'PEP8 스타일로 통일해줘'라고 요청하면
     일관된 코드 스타일을 쉽게 적용할 수 있습니다.
```

개선 전 코드에서는 `userProfile`(camelCase), `GetDisplayName`(PascalCase), `login_count`(snake_case) 등 세 가지 이상의 명명 규칙이 뒤섞여 있었습니다. 개선 후에는 Python의 공식 스타일 가이드인 PEP8에 맞추어 클래스명은 PascalCase, 함수와 변수는 snake_case로 통일되었습니다.

### 예제 12-8: PEP8 포맷팅 적용

명명 규칙뿐만 아니라 공백, import 순서, 세미콜론 같은 포맷팅 규칙도 AI에게 정리를 요청할 수 있습니다.

**AI에게 보낸 요청:**

```
이 코드를 PEP8 스타일로 포맷팅해줘
```

**개선 전 -- PEP8 위반이 가득한 코드:**

```python
# examples/python/chapter03/ex12_08_pep8_formatting.py
import json,os,sys                         # ← import를 콤마로 묶음 (위반)
import math
MAX_RETRY=3                                # ← 연산자 주위 공백 없음 (위반)
default_timeout = 30;                      # ← 세미콜론 사용 (위반)
def connect_to_server( host,port,timeout=default_timeout ):  # ← 괄호 안 공백 (위반)
    url=f"http://{host}:{port}"            # ← 공백 없음 (위반)
    for i in range(MAX_RETRY) :            # ← 콜론 앞 공백 (위반)
        print(f"시도 {i+1}/{MAX_RETRY}...")
        if timeout>0 :                     # ← 연산자/콜론 공백 (위반)
            print( f"타임아웃: {timeout}초" )  # ← 괄호 안 공백 (위반)
            return {"url":url,"status":"connected","attempts":i+1}
    return {"url":url,"status":"failed","attempts":MAX_RETRY}
```

**개선 후 -- PEP8이 적용된 코드:**

```python
# examples/python/chapter03/ex12_08_pep8_formatting.py
import json
import os
import sys
import math

MAX_RETRY = 3
DEFAULT_TIMEOUT = 30


def connect_to_server(host, port, timeout=DEFAULT_TIMEOUT):
    """서버에 연결을 시도합니다."""
    url = f"http://{host}:{port}"
    for i in range(MAX_RETRY):
        print(f"시도 {i + 1}/{MAX_RETRY}...")
        if timeout > 0:
            print(f"타임아웃: {timeout}초")
            return {
                "url": url,
                "status": "connected",
                "attempts": i + 1,
            }
    return {
        "url": url,
        "status": "failed",
        "attempts": MAX_RETRY,
    }
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_08_pep8_formatting.py
```

**결과:**

```
=======================================================
[예제 12-8] PEP8 스타일 적용 요청
=======================================================

[개선 후 코드 실행 결과]
-------------------------------------------------------
시도 1/3...
타임아웃: 30초
{
  "url": "http://localhost:8080",
  "status": "connected",
  "attempts": 1
}

[PEP8 주요 포맷팅 규칙]
-------------------------------------------------------
  1. import 분리
     잘못: import json,os,sys
     올바: import json\nimport os\nimport sys

  2. 연산자 공백
     잘못: MAX_RETRY=3
     올바: MAX_RETRY = 3

  3. 세미콜론 금지
     잘못: timeout = 30;
     올바: timeout = 30

  4. 괄호 안 공백
     잘못: func( a, b )
     올바: func(a, b)

  5. 콜론 앞 공백
     잘못: if x > 0 :
     올바: if x > 0:

  6. 딕셔너리 공백
     잘못: {"key":"val"}
     올바: {"key": "val"}

  7. 줄 길이
     잘못: 79자 이하 권장
     올바: 긴 줄은 괄호로 분리
```

> **Tip:** 실제 프로젝트에서는 `black`, `ruff` 같은 자동 포맷터를 사용하면 PEP8을 자동으로 적용할 수 있습니다. 하지만 AI에게 "PEP8으로 포맷팅해줘"라고 요청하는 것도 학습 초기에는 좋은 방법입니다. AI가 무엇을 어떻게 바꾸었는지 비교하면서 PEP8 규칙을 자연스럽게 익힐 수 있기 때문입니다.

---

## 12.6 리팩토링 요청하기

리팩토링이란 코드의 **외부 동작은 그대로 유지하면서 내부 구조를 개선**하는 것을 말합니다. AI에게 리팩토링을 요청하면 복잡한 코드를 깔끔하게 정리하면서도 동일한 결과를 보장받을 수 있습니다.

### 예제 12-6: 중복 코드 제거

같은 패턴의 코드가 여러 번 반복되는 것은 대표적인 리팩토링 대상입니다. AI에게 "중복 코드를 공통 함수로 묶어줘"라고 요청하면, 반복되는 로직을 하나의 함수로 추출해 줍니다.

**AI에게 보낸 요청:**

```
중복되는 코드가 많아. 공통 함수로 묶어줘
```

**개선 전 -- 중복 코드가 가득한 버전:**

```python
# examples/python/chapter03/ex12_06_remove_duplication.py
def process_students_before():
    """학생 데이터 처리 — 중복 코드가 많은 버전"""
    students = [
        {"name": "김철수", "korean": 85, "english": 90, "math": 78},
        {"name": "이영희", "korean": 92, "english": 88, "math": 95},
        {"name": "박민수", "korean": 76, "english": 82, "math": 88},
    ]

    # 국어 평균 계산 (중복 패턴 1)
    korean_total = 0
    for student in students:
        korean_total += student["korean"]
    korean_avg = korean_total / len(students)

    # 영어 평균 계산 (중복 패턴 2 — 같은 구조 반복)
    english_total = 0
    for student in students:
        english_total += student["english"]
    english_avg = english_total / len(students)

    # 수학 평균 계산 (중복 패턴 3 — 같은 구조 반복)
    math_total = 0
    for student in students:
        math_total += student["math"]
    math_avg = math_total / len(students)
    # ... (최고 점수 찾기도 같은 패턴이 3번 반복)
```

**개선 후 -- 공통 함수로 중복 제거:**

```python
# examples/python/chapter03/ex12_06_remove_duplication.py
def calculate_subject_average(students, subject):
    """특정 과목의 평균 점수를 계산합니다."""
    total = sum(student[subject] for student in students)
    return total / len(students)


def find_top_student(students, subject):
    """특정 과목의 최고 점수 학생을 찾습니다."""
    top = max(students, key=lambda s: s[subject])
    return top["name"], top[subject]


def process_students_after():
    """학생 데이터 처리 — 중복 제거 버전"""
    students = [
        {"name": "김철수", "korean": 85, "english": 90, "math": 78},
        {"name": "이영희", "korean": 92, "english": 88, "math": 95},
        {"name": "박민수", "korean": 76, "english": 82, "math": 88},
    ]
    subjects = ["korean", "english", "math"]
    subject_names = {"korean": "국어", "english": "영어", "math": "수학"}

    # 평균 계산 — 공통 함수 활용
    print("  과목별 평균:")
    avgs = []
    for subj in subjects:
        avg = calculate_subject_average(students, subj)
        avgs.append(f"{subject_names[subj]}: {avg:.1f}")
    print(f"    {'  '.join(avgs)}")
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_06_remove_duplication.py
```

**결과:**

```
=======================================================
[예제 12-6] 중복 코드 제거 요청
=======================================================

[개선 전] 중복 코드 (약 40줄)
----------------------------------------
  과목별 평균:
    국어: 84.3  영어: 86.7  수학: 87.0
  과목별 최고 점수:
    국어: 이영희(92)  영어: 김철수(90)  수학: 이영희(95)

[개선 후] 공통 함수 활용 (약 15줄 + 함수 2개)
----------------------------------------
  과목별 평균:
    국어: 84.3  영어: 86.7  수학: 87.0
  과목별 최고 점수:
    국어: 이영희(92)  영어: 김철수(90)  수학: 이영희(95)

[코드량 비교]
  개선 전: 약 40줄 (동일 패턴 6회 반복)
  개선 후: 약 20줄 (공통 함수 2개 + 루프)
  절감율: 약 50%

Tip: 비슷한 코드가 3번 이상 반복되면 함수로 추출하세요.
     AI에게 '중복 코드를 묶어줘'라고 요청하면 됩니다.
```

개선 전에는 국어, 영어, 수학 각각에 대해 평균 계산과 최고 점수 찾기를 별도로 작성하여 동일한 패턴이 6번 반복되었습니다. 개선 후에는 `calculate_subject_average()`와 `find_top_student()`이라는 공통 함수를 만들고 과목명만 바꾸어 호출하는 방식으로 코드량을 약 50% 줄였습니다. 새로운 과목이 추가되더라도 `subjects` 리스트에 항목을 하나만 추가하면 됩니다.

### 예제 12-7: 가독성 개선 -- 얼리 리턴 패턴

깊게 중첩된 조건문은 읽기 어렵고 "화살표 코드(arrow code)"라고 불립니다. AI에게 "중첩을 줄여줘"라고 요청하면 얼리 리턴(early return) 패턴으로 평탄화해 줍니다.

**AI에게 보낸 요청:**

```
if문이 너무 깊게 중첩돼 있어. 가독성을 개선해줘
```

**개선 전 -- 깊은 중첩 (최대 6단계):**

```python
# examples/python/chapter03/ex12_07_improve_readability.py
def process_payment_before(user, amount, payment_method):
    """결제 처리 — 중첩 조건문 버전 (화살표 코드)"""
    result = {"success": False, "message": ""}

    if user is not None:
        if user.get("is_active"):
            if amount > 0:
                if amount <= user.get("balance", 0):
                    if payment_method in ["card", "bank", "point"]:
                        if payment_method == "point" and amount > user.get("points", 0):
                            result["message"] = "포인트가 부족합니다."
                        else:
                            user["balance"] -= amount
                            result["success"] = True
                            result["message"] = f"{amount:,}원 결제 완료"
                    else:
                        result["message"] = "지원하지 않는 결제 수단입니다."
                else:
                    result["message"] = "잔액이 부족합니다."
            else:
                result["message"] = "결제 금액이 올바르지 않습니다."
        else:
            result["message"] = "비활성 계정입니다."
    else:
        result["message"] = "사용자 정보가 없습니다."

    return result
```

**개선 후 -- 얼리 리턴 (최대 1단계):**

```python
# examples/python/chapter03/ex12_07_improve_readability.py
def process_payment_after(user, amount, payment_method):
    """결제 처리 — 얼리 리턴 버전 (평탄한 구조)"""
    # 가드 절: 잘못된 입력을 빨리 걸러냄
    if user is None:
        return {"success": False, "message": "사용자 정보가 없습니다."}

    if not user.get("is_active"):
        return {"success": False, "message": "비활성 계정입니다."}

    if amount <= 0:
        return {"success": False, "message": "결제 금액이 올바르지 않습니다."}

    if amount > user.get("balance", 0):
        return {"success": False, "message": "잔액이 부족합니다."}

    valid_methods = ["card", "bank", "point"]
    if payment_method not in valid_methods:
        return {"success": False, "message": "지원하지 않는 결제 수단입니다."}

    if payment_method == "point" and amount > user.get("points", 0):
        return {"success": False, "message": "포인트가 부족합니다."}

    # 모든 검증을 통과한 경우 — 결제 처리
    user["balance"] -= amount
    return {"success": True, "message": f"{amount:,}원 결제 완료"}
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_07_improve_readability.py
```

**결과:**

```
=======================================================
[예제 12-7] 가독성 개선 요청 — 얼리 리턴
=======================================================

  테스트 1: 사용자 없음
    중첩 버전: 사용자 정보가 없습니다.
    얼리 리턴: 사용자 정보가 없습니다.
    결과 일치: 예

  테스트 2: 비활성 계정
    중첩 버전: 비활성 계정입니다.
    얼리 리턴: 비활성 계정입니다.
    결과 일치: 예

  테스트 3: 잘못된 금액
    중첩 버전: 결제 금액이 올바르지 않습니다.
    얼리 리턴: 결제 금액이 올바르지 않습니다.
    결과 일치: 예
  ...
  테스트 7: 정상 결제
    중첩 버전: 10,000원 결제 완료
    얼리 리턴: 10,000원 결제 완료
    결과 일치: 예

[구조 비교]
-------------------------------------------------------
  중첩 버전: 최대 6단계 깊이 (화살표 모양)
  얼리 리턴: 최대 1단계 깊이 (평탄한 구조)
```

7개의 테스트 케이스 모두에서 두 버전의 결과가 일치합니다. 하지만 얼리 리턴 버전은 위에서부터 아래로 순서대로 읽을 수 있어 훨씬 이해하기 쉽습니다. "사용자가 없으면 바로 실패를 반환한다, 비활성이면 바로 실패를 반환한다..." 이렇게 하나씩 조건을 걸러내고, 모든 검증을 통과한 경우에만 마지막에 결제를 처리합니다.

> **Note:** 얼리 리턴 패턴은 "만약 ~가 아니면 빨리 빠져나간다"는 사고방식입니다. 가드 절(guard clause)이라고도 부르며, 복잡한 비즈니스 로직에서 가독성을 크게 향상시킵니다. AI에게 "중첩을 줄여줘" 또는 "얼리 리턴으로 바꿔줘"라고 요청하면 적용됩니다.

### 예제 12-9: 스파게티 코드 리팩토링 실습

실전에서는 여러 가지 문제가 한꺼번에 뒤엉킨 "스파게티 코드"를 마주하게 됩니다. 이런 경우 AI에게 전체적인 리팩토링을 요청할 수 있습니다.

**AI에게 보낸 요청:**

```
이 코드가 너무 지저분해. 깔끔하게 리팩토링해줘
```

**개선 전 -- 스파게티 코드:**

```python
# examples/python/chapter03/ex12_09_refactor_spaghetti.py
def run_spaghetti_version():
    """스파게티 코드 버전 (모든 것이 뒤엉킨 상태)"""
    data = [
        ("김철수", 85, 90, 78),
        ("이영희", 92, 88, 95),
        ("박민수", 76, 65, 88),
        ("정수진", 98, 95, 92),
        ("최동욱", 45, 50, 55),
    ]
    print("===== 성적 처리 결과 =====")
    total_k = 0
    total_e = 0
    total_m = 0
    cnt = 0
    for d in data:
        cnt = cnt + 1
        total_k = total_k + d[1]
        total_e = total_e + d[2]
        total_m = total_m + d[3]
    avg_k = total_k / cnt
    avg_e = total_e / cnt
    avg_m = total_m / cnt
    print(f"과목 평균 — 국어: {avg_k:.1f}, 영어: {avg_e:.1f}, 수학: {avg_m:.1f}")
    for d in data:
        s = d[1] + d[2] + d[3]
        a = s / 3
        if a >= 90:
            g = "A"
        else:
            if a >= 80:
                g = "B"
            else:
                if a >= 70:
                    g = "C"
                else:
                    if a >= 60:
                        g = "D"
                    else:
                        g = "F"
        if g == "F":
            w = " [경고: 재시험 대상]"
        else:
            w = ""
        print(f"  {d[0]}: 합계={s}, 평균={a:.1f}, 등급={g}{w}")
```

이 코드에는 여러 가지 문제가 있습니다. 튜플 인덱스(`d[1]`, `d[2]`)로 데이터에 접근하여 의미를 알 수 없고, 변수명이 `d`, `s`, `a`, `g`, `w` 등으로 모호하며, 등급 판정이 5단계 중첩 if문으로 되어 있고, 합계/평균 계산이 중복됩니다.

**개선 후 -- 리팩토링된 코드:**

```python
# examples/python/chapter03/ex12_09_refactor_spaghetti.py
def create_student(name, korean, english, math):
    """학생 데이터를 딕셔너리로 생성합니다."""
    return {"name": name, "korean": korean, "english": english, "math": math}


def calculate_total(student):
    """학생의 총점을 계산합니다."""
    return student["korean"] + student["english"] + student["math"]


def calculate_average(student):
    """학생의 평균을 계산합니다."""
    return calculate_total(student) / 3


def determine_grade(average):
    """평균 점수에 따른 등급을 결정합니다."""
    thresholds = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]
    for threshold, grade in thresholds:
        if average >= threshold:
            return grade
    return "F"
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_09_refactor_spaghetti.py
```

**결과:**

```
=======================================================
[예제 12-9] 스파게티 코드 리팩토링
=======================================================

[개선 전] 스파게티 코드
----------------------------------------
===== 성적 처리 결과 =====
과목 평균 — 국어: 79.2, 영어: 77.6, 수학: 81.6
  김철수: 합계=253, 평균=84.3, 등급=B
  이영희: 합계=275, 평균=91.7, 등급=A
  박민수: 합계=229, 평균=76.3, 등급=C
  정수진: 합계=285, 평균=95.0, 등급=A
  최동욱: 합계=150, 평균=50.0, 등급=F [경고: 재시험 대상]
수석: 정수진 (평균: 95.0)

[개선 후] 리팩토링된 코드
----------------------------------------
===== 성적 처리 결과 =====
과목 평균 — 국어: 79.2, 영어: 77.6, 수학: 81.6
  김철수: 합계=253, 평균=84.3, 등급=B
  이영희: 합계=275, 평균=91.7, 등급=A
  박민수: 합계=229, 평균=76.3, 등급=C
  정수진: 합계=285, 평균=95.0, 등급=A
  최동욱: 합계=150, 평균=50.0, 등급=F [경고: 재시험 대상]
수석: 정수진 (평균: 95.0)

[리팩토링 요약]
-------------------------------------------------------
  튜플 → 딕셔너리          d[1] → student['korean']       → 의미 명확
  중첩 if → 테이블        if/else 5단계 → 리스트 순회           → 확장 용이
  중복 계산 제거           합계/평균 2회 → 함수 호출               → 유지보수 쉬움
  함수 분리              1개 블록 → 7개 함수                  → 테스트 가능
  매직 넘버 제거           3, 90, 80... → 명명된 구조          → 의미 명확
```

리팩토링 전후의 출력 결과는 완전히 동일합니다. 하지만 코드의 내부 구조는 크게 달라졌습니다. 1개의 뒤엉킨 블록이 7개의 명확한 함수로 분리되었고, 각 함수는 이름만 보고도 역할을 알 수 있습니다.

### 예제 12-10: 레거시 코드 현대화

오래된 스타일의 Python 코드를 현대적인 Python으로 업데이트하는 것도 리팩토링의 일종입니다. AI에게 "최신 Python 스타일로 바꿔줘"라고 요청하면, 구식 문법을 현대적인 패턴으로 변환해 줍니다.

**AI에게 보낸 요청:**

```
이 코드가 옛날 스타일이야. 최신 Python 스타일로 바꿔줘
```

**개선 전 -- 레거시 스타일:**

```python
# examples/python/chapter03/ex12_10_modernize_legacy.py
# 1. 문자열 포맷: % 연산자
greeting = "안녕하세요, %s님! 나이는 %d세입니다." % (name, age)

# 2. 문자열 결합: + 연산자
result = ""
for i in range(len(items)):
    result = result + str(i + 1) + ". " + items[i] + "\n"

# 3. 딕셔너리 접근: 수동 존재 확인
if "host" in config:
    host = config["host"]
else:
    host = "127.0.0.1"

# 4. 리스트 생성: 수동 루프
even_squares = []
for n in numbers:
    if n % 2 == 0:
        even_squares.append(n * n)

# 5. None 비교: == 연산자
if value == None:
    print("값이 None입니다")

# 6. 타입 확인: type() == 비교
if type(data) == str:
    print("문자열 타입입니다")
```

**개선 후 -- 현대적 스타일:**

```python
# examples/python/chapter03/ex12_10_modernize_legacy.py
# 1. 문자열 포맷: f-string
greeting = f"안녕하세요, {name}님! 나이는 {age}세입니다."

# 2. 문자열 결합: enumerate + f-string + join
result = "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))

# 3. 딕셔너리 접근: .get() 메서드
host = config.get("host", "127.0.0.1")

# 4. 리스트 생성: 리스트 컴프리헨션
even_squares = [n ** 2 for n in numbers if n % 2 == 0]

# 5. None 비교: is 연산자
if value is None:
    print("값이 None입니다")

# 6. 타입 확인: isinstance()
if isinstance(data, str):
    print("문자열 타입입니다")
```

**실행:**

```bash
$ python examples/python/chapter03/ex12_10_modernize_legacy.py
```

**결과:**

```
=======================================================
[예제 12-10] 레거시 코드 현대화
=======================================================

[개선 전] 레거시 Python 스타일
----------------------------------------
안녕하세요, 김바이브님! 나이는 25세입니다.
1. 사과
2. 바나나
3. 딸기

서버: localhost, 타임아웃: 30
짝수의 제곱: [4, 16, 36, 64, 100]

[개선 후] 현대적 Python 스타일
----------------------------------------
안녕하세요, 김바이브님! 나이는 25세입니다.
1. 사과
2. 바나나
3. 딸기

서버: localhost, 타임아웃: 30
짝수의 제곱: [4, 16, 36, 64, 100]

[현대화 변환 요약]
-------------------------------------------------------
  항목             레거시                          현대적
  -------------- ---------------------------- -------------------------
  문자열 포맷         "Hello %s" % name            f"Hello {name}"
  문자열 결합         result + str(i)              f"{i}. {item}"
  딕셔너리 접근        if "key" in d: d["key"]      d.get("key", default)
  리스트 생성         for + append                 [x for x in ...]
  파일 처리          f = open(); f.close()        with open() as f:
  None 비교        if x == None                 if x is None
  타입 확인          type(x) == str               isinstance(x, str)
  타입 힌트          def func(x):                 def func(x: int) -> str:
```

레거시 코드와 현대적 코드의 실행 결과는 동일하지만, 현대적 스타일은 더 간결하고 Pythonic(파이썬다운)합니다. 특히 f-string, 리스트 컴프리헨션, `.get()` 메서드, `is None` 비교, `isinstance()` 등은 현대 Python에서 표준적으로 사용되는 패턴입니다.

> **Tip:** AI에게 리팩토링을 요청할 때는 구체적으로 어떤 부분이 불만인지 말해주면 더 좋은 결과를 얻습니다. "이 코드를 리팩토링해줘"보다는 "중첩 if를 줄여줘", "함수로 분리해줘", "최신 Python 스타일로 바꿔줘"처럼 구체적인 방향을 제시하세요.

---

## 정리

이번 챕터에서는 AI가 생성한 코드를 검토하고 개선하는 방법을 배웠습니다. 핵심 내용을 정리합니다.

### 핵심 원칙

1. **이해하지 못하는 코드는 사용하지 않는다.** AI에게 "이 코드 설명해줘" 또는 "각 줄마다 주석을 달아줘"라고 요청하여 코드를 충분히 이해한 후 사용하세요.

2. **체크리스트를 활용하라.** 정확성, 가독성, 변수명, 에러 처리, 코드 스타일, 중복 여부를 체계적으로 검토하세요.

3. **개선 요청은 구체적으로 하라.** "코드 좀 고쳐줘" 대신 "변수명을 의미 있게 바꿔줘", "함수를 분리해줘", "중복 코드를 묶어줘"처럼 구체적으로 요청하세요.

4. **스타일은 일관되게 유지하라.** PEP8 같은 표준 스타일 가이드를 기준으로 AI에게 통일을 요청하세요.

5. **리팩토링은 동작을 보존한다.** 리팩토링 전후의 결과가 동일한지 반드시 확인하세요.

### 이번 챕터에서 배운 AI 요청 패턴

| 상황 | 요청 예시 |
|------|-----------|
| 코드 이해 | "이 코드가 무엇을 하는지 설명해줘" |
| 주석 추가 | "각 줄마다 주석을 달아서 설명해줘" |
| 변수명 개선 | "변수명을 더 의미 있게 바꿔줘" |
| 함수 분리 | "기능별로 함수를 분리해줘" |
| 중복 제거 | "중복 코드를 공통 함수로 묶어줘" |
| 가독성 개선 | "중첩된 if문을 얼리 리턴으로 바꿔줘" |
| 스타일 통일 | "PEP8 기준으로 스타일을 통일해줘" |
| 현대화 | "최신 Python 스타일로 바꿔줘" |
| 전면 리팩토링 | "이 코드를 깔끔하게 리팩토링해줘" |

> **Note:** 코드 리뷰 능력은 바이브 코딩에서 가장 중요한 역량 중 하나입니다. AI가 코드를 생성하는 속도는 빠르지만, 그 코드의 품질을 판단하고 올바른 방향으로 개선을 이끄는 것은 사람의 역할입니다. 지금 배운 검토 습관과 요청 패턴을 꾸준히 연습하면, AI와의 협업 효율이 크게 향상될 것입니다.

---

## 다음 장 예고

**Chapter 13: 디버깅과 에러 해결**에서는 코드가 예상대로 동작하지 않을 때 AI를 활용하여 버그를 찾고 수정하는 방법을 배웁니다. 에러 메시지를 읽는 법, AI에게 에러를 설명하는 법, 그리고 일반적인 Python 에러 유형별 해결 전략을 다룹니다. 코드 리뷰가 "예방"이라면, 디버깅은 "치료"에 해당합니다. 두 가지를 모두 익히면 AI와 함께 안정적인 코드를 만들어 나갈 수 있습니다.
