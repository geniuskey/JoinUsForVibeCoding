## Chapter 21: 테스트 주도 바이브 코딩

"코드가 동작하는 것 같은데... 정말 맞을까?"

프로그래밍을 하다 보면 이런 불안감이 찾아옵니다. 함수 하나를 수정했는데 다른 곳에서 문제가 생기지는 않을까? 새로운 기능을 추가했는데 기존 기능이 망가지지는 않았을까? 이런 걱정은 초보자뿐 아니라 숙련된 개발자에게도 익숙한 감정입니다.

**테스트 코드**는 이 불안감을 해소해 주는 가장 확실한 방법입니다. 코드가 올바르게 동작하는지 자동으로 검증해 주는 코드를 미리 작성해 두면, 언제든지 "내 코드가 맞는지" 확인할 수 있습니다.

바이브 코딩에서 테스트는 더욱 특별한 의미를 가집니다. AI에게 "이 기능의 테스트를 먼저 작성해 줘"라고 요청하고, 그 테스트를 통과하는 구현을 다시 AI에게 맡기면, AI가 만든 코드의 품질을 객관적으로 검증할 수 있기 때문입니다. 테스트는 AI와 협업할 때 **신뢰의 다리** 역할을 합니다.

이번 장에서는 파이썬 표준 라이브러리에 포함된 `unittest`를 사용하여 테스트 코드를 작성하고, 테스트 주도 개발(TDD)의 핵심 사이클을 바이브 코딩에 적용하는 방법을 배워보겠습니다.

---

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 테스트 코드가 왜 중요한지 이해하고, 바이브 코딩에서의 역할을 설명하기
- `unittest` 모듈을 사용하여 단위 테스트를 작성하고 실행하기
- 다양한 `assert` 메서드를 상황에 맞게 활용하기
- 예외 발생을 테스트하고, 테스트 픽스처로 환경을 설정하기
- AI에게 "테스트 먼저"를 요청하는 TDD 패턴을 적용하기
- Red-Green-Refactor 사이클을 이해하고 실습하기
- 테스트 커버리지의 개념을 이해하고 활용하기

---

### 21.1 테스트의 중요성

#### 왜 테스트 코드를 작성해야 할까?

다음과 같은 상황을 상상해 보세요:

1. **기능 추가 후 기존 기능 확인**: 장바구니에 할인 기능을 추가했는데, 기존의 가격 계산이 정상인지 어떻게 확인할까요?
2. **코드 수정 후 안전 확인**: 함수의 내부 구조를 개선했는데, 결과가 달라지지 않았는지 어떻게 보장할까요?
3. **AI가 생성한 코드 검증**: AI에게 받은 코드가 정말 올바르게 동작하는지 어떻게 확신할까요?

매번 직접 실행해서 눈으로 확인하는 것은 비효율적이고, 실수를 놓치기도 쉽습니다. 테스트 코드가 있으면 **버튼 하나로** 모든 것을 자동으로 확인할 수 있습니다.

#### 바이브 코딩에서 테스트가 특별히 중요한 이유

바이브 코딩에서는 AI가 코드를 생성합니다. 하지만 AI가 생성한 코드가 항상 완벽하지는 않습니다. 테스트 코드는 다음과 같은 역할을 합니다:

| 역할 | 설명 |
|------|------|
| **AI 코드 검증** | AI가 생성한 코드가 기대대로 동작하는지 자동 확인 |
| **요구사항 명세** | 테스트 코드가 곧 "이 기능은 이렇게 동작해야 해"라는 명세서 |
| **안전한 리팩토링** | 코드를 개선해도 기존 동작이 보장됨 |
| **회귀 방지** | 새 기능 추가 시 기존 기능이 깨지지 않음을 보장 |
| **소통 도구** | AI에게 "이 테스트를 통과시켜 줘"라고 요청할 수 있음 |

> **Note:** "테스트를 작성하는 것은 시간 낭비"라고 생각할 수도 있습니다. 하지만 실제로는 **테스트가 없을 때 버그를 찾고 고치는 시간**이 훨씬 더 많이 들어갑니다. 테스트는 미래의 나를 위한 투자입니다.

---

### 21.2 단위 테스트 기초 -- 첫 번째 테스트 작성하기

파이썬에는 `unittest`라는 테스트 프레임워크가 표준 라이브러리에 포함되어 있습니다. 별도의 설치 없이 바로 사용할 수 있습니다.

#### unittest의 기본 구조

`unittest`로 테스트를 작성하려면 세 가지만 기억하면 됩니다:

1. `unittest.TestCase`를 상속받는 **테스트 클래스**를 만듭니다
2. 클래스 안에 `test_`로 시작하는 **테스트 메서드**를 작성합니다
3. `self.assertEqual()` 등의 **assert 메서드**로 결과를 검증합니다

**예제 21-1: 첫 번째 테스트 작성**

```python
# examples/python/chapter05/ex21_01_first_test.py
import unittest


# 테스트할 함수: 두 수를 더하는 간단한 함수
def add(a, b):
    """두 수를 더해서 반환합니다."""
    return a + b


def multiply(a, b):
    """두 수를 곱해서 반환합니다."""
    return a * b


# 테스트 클래스: unittest.TestCase를 상속받아 테스트를 작성합니다
class TestBasicMath(unittest.TestCase):
    """기본 수학 함수에 대한 테스트"""

    def test_add_positive_numbers(self):
        """양수 두 개를 더하는 테스트"""
        result = add(3, 5)
        self.assertEqual(result, 8)  # 3 + 5 = 8이어야 합니다

    def test_add_negative_numbers(self):
        """음수를 포함하는 덧셈 테스트"""
        result = add(-1, -2)
        self.assertEqual(result, -3)  # -1 + (-2) = -3이어야 합니다

    def test_add_zero(self):
        """0을 더하는 테스트"""
        result = add(10, 0)
        self.assertEqual(result, 10)  # 10 + 0 = 10이어야 합니다

    def test_multiply_basic(self):
        """기본 곱셈 테스트"""
        result = multiply(4, 3)
        self.assertEqual(result, 12)  # 4 x 3 = 12이어야 합니다

    def test_multiply_by_zero(self):
        """0을 곱하는 테스트"""
        result = multiply(5, 0)
        self.assertEqual(result, 0)  # 5 x 0 = 0이어야 합니다


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

**실행:**
```bash
$ python examples/python/chapter05/ex21_01_first_test.py
```

**결과:**
```
test_add_negative_numbers (__main__.TestBasicMath.test_add_negative_numbers)
음수를 포함하는 덧셈 테스트 ... ok
test_add_positive_numbers (__main__.TestBasicMath.test_add_positive_numbers)
양수 두 개를 더하는 테스트 ... ok
test_add_zero (__main__.TestBasicMath.test_add_zero)
0을 더하는 테스트 ... ok
test_multiply_basic (__main__.TestBasicMath.test_multiply_basic)
기본 곱셈 테스트 ... ok
test_multiply_by_zero (__main__.TestBasicMath.test_multiply_by_zero)
0을 곱하는 테스트 ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

5개의 테스트가 모두 `ok`로 통과했습니다! 각 줄의 의미를 살펴보겠습니다:

- **`test_add_positive_numbers ... ok`**: 테스트 메서드 이름과 함께 통과 여부를 보여줍니다
- **`Ran 5 tests`**: 총 5개의 테스트를 실행했습니다
- **`OK`**: 모든 테스트가 통과했다는 최종 결과입니다

> **Tip:** `unittest.main(verbosity=2)`에서 `verbosity=2`는 각 테스트의 이름과 설명(독스트링)을 함께 보여주는 상세 모드입니다. `verbosity=1`(기본값)이면 각 테스트를 `.`(점)으로만 표시합니다.

#### 테스트가 실패하면 어떻게 될까?

만약 `add(3, 5)`가 8이 아닌 다른 값을 반환한다면, `assertEqual`이 실패하면서 어디서 무엇이 잘못되었는지 정확히 알려줍니다:

```
FAIL: test_add_positive_numbers (__main__.TestBasicMath)
----------------------------------------------------------------------
AssertionError: 7 != 8

----------------------------------------------------------------------
Ran 5 tests in 0.001s

FAILED (failures=1)
```

이렇게 **어떤 테스트**에서 **어떤 값**이 기대와 달랐는지를 자동으로 보고해 줍니다.

---

### 21.3 unittest 사용법 심화

#### TestRunner와 TestSuite 활용하기

`unittest`는 테스트를 수집하고 실행하는 다양한 방법을 제공합니다. 프로그래밍 방식으로 테스트를 실행하면 결과를 분석하거나 특정 테스트만 골라서 실행할 수 있습니다.

**예제 21-2: unittest 실행 -- TestRunner 활용**

```python
# examples/python/chapter05/ex21_02_unittest_run.py
import unittest


def celsius_to_fahrenheit(celsius):
    """섭씨를 화씨로 변환합니다."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """화씨를 섭씨로 변환합니다."""
    return (fahrenheit - 32) * 5 / 9


class TestTemperatureConversion(unittest.TestCase):
    """온도 변환 함수 테스트"""

    def test_freezing_point(self):
        """물의 어는점 변환 테스트"""
        self.assertEqual(celsius_to_fahrenheit(0), 32)

    def test_boiling_point(self):
        """물의 끓는점 변환 테스트"""
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_body_temperature(self):
        """체온 변환 테스트"""
        self.assertAlmostEqual(celsius_to_fahrenheit(36.5), 97.7)

    def test_round_trip(self):
        """왕복 변환 테스트 (섭씨 -> 화씨 -> 섭씨)"""
        original = 25
        converted = celsius_to_fahrenheit(original)
        back = fahrenheit_to_celsius(converted)
        self.assertAlmostEqual(back, original)
```

**실행 결과:**
```
test_boiling_point ... ok
test_body_temperature ... ok
test_freezing_point ... ok
test_round_trip ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

이 예제에서 주목할 점은 세 가지 실행 방식입니다:

| 방법 | 설명 | 사용 시점 |
|------|------|-----------|
| `TestLoader` | 테스트 클래스에서 테스트를 자동 수집 | 전체 테스트 실행 |
| `TestSuite` | 여러 테스트를 하나의 그룹으로 묶기 | 특정 테스트만 선택 실행 |
| `TextTestRunner` | 테스트를 실행하고 결과를 출력 | 결과 분석이 필요할 때 |

프로그래밍 방식으로 특정 테스트만 골라서 실행할 수도 있습니다:

```python
# 특정 테스트만 골라서 실행
custom_suite = unittest.TestSuite()
custom_suite.addTest(TestTemperatureConversion("test_freezing_point"))
custom_suite.addTest(TestTemperatureConversion("test_boiling_point"))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(custom_suite)
print(f"실행한 테스트 수: {result.testsRun}")
print(f"전체 통과 여부: {'통과' if result.wasSuccessful() else '실패'}")
```

> **Tip:** 일반적으로는 `python -m unittest` 명령어로 실행하는 것이 가장 간편합니다. 커맨드라인에서 `python -m unittest discover`를 실행하면 프로젝트 내의 모든 테스트 파일을 자동으로 찾아서 실행해 줍니다.

---

#### 다양한 assert 메서드 활용하기

`unittest.TestCase`는 다양한 상황에 맞는 검증 메서드를 제공합니다. 상황에 맞는 assert 메서드를 사용하면 테스트 실패 시 더 명확한 메시지를 받을 수 있습니다.

**예제 21-3: 다양한 assert 메서드 활용**

```python
# examples/python/chapter05/ex21_03_multiple_tests.py
import unittest


def get_grade(score):
    """점수에 따른 학점을 반환합니다."""
    if not isinstance(score, (int, float)):
        raise TypeError("점수는 숫자여야 합니다")
    if score < 0 or score > 100:
        raise ValueError("점수는 0~100 사이여야 합니다")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def is_even(n):
    """짝수인지 확인합니다."""
    return n % 2 == 0


def find_max(numbers):
    """리스트에서 최대값을 찾습니다. 빈 리스트면 None을 반환합니다."""
    if not numbers:
        return None
    return max(numbers)


class TestGrade(unittest.TestCase):
    """학점 계산 함수 테스트 - assertEqual / assertNotEqual 사용"""

    def test_grade_a(self):
        """90점 이상은 A학점"""
        self.assertEqual(get_grade(95), "A")
        self.assertEqual(get_grade(90), "A")
        self.assertEqual(get_grade(100), "A")

    def test_grade_b(self):
        """80~89점은 B학점"""
        self.assertEqual(get_grade(85), "B")
        self.assertNotEqual(get_grade(85), "A")  # B는 A가 아닙니다

    def test_grade_f(self):
        """60점 미만은 F학점"""
        self.assertEqual(get_grade(50), "F")
        self.assertEqual(get_grade(0), "F")


class TestEvenOdd(unittest.TestCase):
    """짝수/홀수 판별 테스트 - assertTrue / assertFalse 사용"""

    def test_even_numbers(self):
        """짝수 확인"""
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(100))

    def test_odd_numbers(self):
        """홀수 확인"""
        self.assertFalse(is_even(1))
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(99))


class TestCollectionOperations(unittest.TestCase):
    """컬렉션 관련 테스트 - assertIn / assertIsNone 등 사용"""

    def test_find_max_with_values(self):
        """최대값 찾기 - 값이 있는 경우"""
        result = find_max([3, 7, 1, 9, 4])
        self.assertIsNotNone(result)       # None이 아니어야 함
        self.assertEqual(result, 9)

    def test_find_max_empty(self):
        """최대값 찾기 - 빈 리스트인 경우"""
        result = find_max([])
        self.assertIsNone(result)          # None이어야 함


class TestNumericComparisons(unittest.TestCase):
    """수치 비교 테스트 - assertGreater / assertAlmostEqual 등 사용"""

    def test_almost_equal(self):
        """부동소수점 비교 테스트 (근사값 비교)"""
        result = 0.1 + 0.2
        # self.assertEqual(result, 0.3)  # 이건 실패할 수 있음!
        self.assertAlmostEqual(result, 0.3, places=7)  # 소수 7자리까지 비교

    def test_is_instance(self):
        """타입 확인 테스트"""
        self.assertIsInstance(get_grade(95), str)   # 결과가 문자열인지 확인
```

**실행 결과:**
```
test_grade_a ... ok
test_grade_b ... ok
test_grade_f ... ok
test_even_numbers ... ok
test_odd_numbers ... ok
test_find_max_empty ... ok
test_find_max_with_values ... ok
test_almost_equal ... ok
test_is_instance ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK
```

#### assert 메서드 총정리

다음은 가장 자주 사용되는 assert 메서드입니다:

| 메서드 | 검증 내용 | 사용 예 |
|--------|-----------|---------|
| `assertEqual(a, b)` | a == b | 반환값이 기대값과 같은지 |
| `assertNotEqual(a, b)` | a != b | 반환값이 특정 값이 아닌지 |
| `assertTrue(x)` | x가 True | 조건이 참인지 |
| `assertFalse(x)` | x가 False | 조건이 거짓인지 |
| `assertIn(a, b)` | a가 b에 포함 | 특정 항목이 컬렉션에 있는지 |
| `assertNotIn(a, b)` | a가 b에 없음 | 특정 항목이 컬렉션에 없는지 |
| `assertIsNone(x)` | x가 None | 결과가 None인지 |
| `assertIsNotNone(x)` | x가 None이 아님 | 결과가 None이 아닌지 |
| `assertGreater(a, b)` | a > b | 크기 비교 |
| `assertAlmostEqual(a, b)` | a 와 b가 거의 같음 | 부동소수점 비교 |
| `assertIsInstance(a, T)` | a가 타입 T | 반환 타입 확인 |
| `assertRaises(E)` | 예외 E가 발생 | 예외 테스트 |

> **Tip:** `assertEqual` 하나만으로도 대부분의 테스트를 작성할 수 있지만, 상황에 맞는 assert 메서드를 사용하면 테스트 실패 시 **더 명확한 에러 메시지**를 받을 수 있습니다. 예를 들어 `assertTrue(a == b)` 대신 `assertEqual(a, b)`를 쓰면 실패 시 `3 != 5`처럼 구체적인 값을 보여줍니다.

---

#### 예외 테스트하기

올바른 코드는 잘못된 입력에 대해 적절한 예외를 발생시켜야 합니다. `assertRaises`를 사용하면 "이 코드가 예외를 제대로 던지는지"를 테스트할 수 있습니다.

**예제 21-4: 예외 테스트 (assertRaises)**

```python
# examples/python/chapter05/ex21_04_exception_test.py
import unittest


def divide(a, b):
    """나눗셈을 수행합니다. 0으로 나누면 예외를 발생시킵니다."""
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return a / b


def parse_age(value):
    """문자열을 나이(정수)로 변환합니다."""
    if not isinstance(value, str):
        raise TypeError("문자열을 입력해야 합니다")
    try:
        age = int(value)
    except ValueError:
        raise ValueError(f"'{value}'는 유효한 숫자가 아닙니다")
    if age < 0:
        raise ValueError("나이는 0 이상이어야 합니다")
    if age > 150:
        raise ValueError("나이는 150 이하여야 합니다")
    return age


class TestDivide(unittest.TestCase):
    """나눗셈 함수의 예외 테스트"""

    def test_normal_division(self):
        """정상적인 나눗셈"""
        self.assertEqual(divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        """0으로 나누면 ZeroDivisionError가 발생해야 합니다"""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_divide_by_zero_message(self):
        """예외 메시지도 확인합니다"""
        with self.assertRaises(ZeroDivisionError) as context:
            divide(10, 0)
        self.assertIn("0으로 나눌 수 없습니다", str(context.exception))


class TestParseAge(unittest.TestCase):
    """나이 파싱 함수의 예외 테스트"""

    def test_valid_age(self):
        """유효한 나이 문자열"""
        self.assertEqual(parse_age("25"), 25)
        self.assertEqual(parse_age("0"), 0)

    def test_non_string_input(self):
        """문자열이 아닌 입력 -> TypeError"""
        with self.assertRaises(TypeError):
            parse_age(25)

    def test_non_numeric_string(self):
        """숫자가 아닌 문자열 -> ValueError"""
        with self.assertRaises(ValueError) as context:
            parse_age("스물다섯")
        self.assertIn("유효한 숫자가 아닙니다", str(context.exception))

    def test_negative_age(self):
        """음수 나이 -> ValueError"""
        with self.assertRaises(ValueError) as context:
            parse_age("-5")
        self.assertIn("0 이상", str(context.exception))
```

**실행 결과:**
```
test_normal_division ... ok
test_divide_by_zero ... ok
test_divide_by_zero_message ... ok
test_valid_age ... ok
test_non_string_input ... ok
test_non_numeric_string ... ok
test_negative_age ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

예외 테스트에서 핵심은 `with self.assertRaises(예외타입):` 구문입니다. 이 블록 안의 코드가 해당 예외를 발생시키면 테스트가 통과하고, 예외가 발생하지 않으면 테스트가 실패합니다. `as context`를 추가하면 발생한 예외 객체에 접근하여 에러 메시지까지 검증할 수 있습니다.

> **Note:** 예외 테스트는 "잘못된 입력에 대해 적절한 에러를 반환하는지" 확인하는 중요한 과정입니다. 좋은 코드는 정상 동작뿐만 아니라, 오류 상황에서도 예측 가능하게 동작해야 합니다.

---

#### 테스트 픽스처 -- setUp과 tearDown

테스트를 작성하다 보면 여러 테스트가 같은 준비 작업을 반복하는 경우가 있습니다. 예를 들어 "장바구니 객체를 만들고 상품을 추가하는" 작업을 매 테스트마다 반복해야 할 수 있습니다.

이때 **픽스처(Fixture)**를 사용합니다. `setUp()` 메서드에 준비 작업을, `tearDown()` 메서드에 정리 작업을 넣으면, 각 테스트 메서드 실행 전후에 자동으로 호출됩니다.

**예제 21-5: 테스트 픽스처 (setUp / tearDown)**

```python
# examples/python/chapter05/ex21_05_test_fixture.py
import unittest


class ShoppingCart:
    """장바구니 클래스"""

    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        """상품을 장바구니에 추가합니다."""
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def remove_item(self, name):
        """상품을 장바구니에서 제거합니다."""
        self.items = [item for item in self.items if item["name"] != name]

    def get_total(self):
        """총 가격을 계산합니다."""
        return sum(item["price"] * item["quantity"] for item in self.items)

    def get_item_count(self):
        """상품 종류 수를 반환합니다."""
        return len(self.items)

    def clear(self):
        """장바구니를 비웁니다."""
        self.items = []


class TestShoppingCart(unittest.TestCase):
    """장바구니 테스트 - setUp/tearDown 활용"""

    def setUp(self):
        """각 테스트 메서드 실행 전에 호출됩니다."""
        self.cart = ShoppingCart()
        self.cart.add_item("사과", 1000, 3)
        self.cart.add_item("바나나", 1500, 2)

    def tearDown(self):
        """각 테스트 메서드 실행 후에 호출됩니다."""
        self.cart.clear()

    def test_initial_items(self):
        """setUp에서 추가한 상품 확인"""
        self.assertEqual(self.cart.get_item_count(), 2)

    def test_add_item(self):
        """상품 추가 테스트"""
        self.cart.add_item("체리", 3000)
        self.assertEqual(self.cart.get_item_count(), 3)

    def test_remove_item(self):
        """상품 제거 테스트"""
        self.cart.remove_item("사과")
        self.assertEqual(self.cart.get_item_count(), 1)

    def test_total_price(self):
        """총 가격 계산 테스트"""
        # 사과 1000 * 3 + 바나나 1500 * 2 = 6000
        self.assertEqual(self.cart.get_total(), 6000)
```

**실행 결과:**
```
test_add_item ... ok
test_initial_items ... ok
test_remove_item ... ok
test_total_price ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

#### setUp vs setUpClass

| 메서드 | 호출 시점 | 용도 |
|--------|-----------|------|
| `setUp` | 각 테스트 메서드 **전마다** | 테스트마다 독립적인 환경 필요 시 |
| `tearDown` | 각 테스트 메서드 **후마다** | 테스트 후 리소스 정리 |
| `setUpClass` | 클래스의 **첫 테스트 전에 한 번** | 비용이 큰 초기화 (DB 연결, 파일 생성 등) |
| `tearDownClass` | 클래스의 **마지막 테스트 후에 한 번** | 공유 리소스 정리 |

`setUpClass`와 `tearDownClass`는 `@classmethod` 데코레이터를 붙여서 사용합니다. 파일 생성이나 데이터베이스 연결처럼 비용이 큰 작업을 한 번만 수행하고 여러 테스트에서 공유할 때 유용합니다.

```python
class TestFileOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """임시 파일을 한 번만 생성합니다."""
        cls.test_file = "/tmp/test_data.txt"
        with open(cls.test_file, "w") as f:
            f.write("테스트 데이터")

    @classmethod
    def tearDownClass(cls):
        """임시 파일을 삭제합니다."""
        import os
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
```

> **Tip:** `setUp`은 각 테스트의 독립성을 보장합니다. 하나의 테스트에서 장바구니에 상품을 추가해도, 다음 테스트에서는 `setUp`이 새로운 장바구니를 만들어 주므로 테스트 간 간섭이 없습니다. 이것은 테스트의 핵심 원칙 중 하나입니다.

---

### 21.4 테스트 먼저 요청하기 -- AI와 함께하는 TDD

**테스트 주도 개발(Test-Driven Development, TDD)**은 코드를 작성하기 **전에** 테스트를 먼저 작성하는 개발 방법론입니다. 바이브 코딩에서 TDD는 특히 강력합니다:

1. AI에게 "이 기능의 테스트를 먼저 작성해 줘"
2. AI가 테스트를 작성하면, 요구사항이 코드로 명확해짐
3. "이 테스트를 모두 통과하도록 구현해 줘"
4. AI가 테스트를 통과하는 구현을 작성

이 과정에서 테스트 코드가 일종의 **계약서** 역할을 합니다. "이렇게 동작해야 한다"는 것을 코드로 명확히 정의하기 때문에, AI가 엉뚱한 방향으로 구현하는 것을 방지합니다.

**예제 21-6: AI에게 테스트 먼저 요청하기**

다음은 "비밀번호 검증 함수"를 TDD 방식으로 만드는 과정입니다.

**AI에게 이렇게 요청합니다:**

```
비밀번호가 유효한지 검증하는 함수를 만들 건데,
테스트 코드를 먼저 작성해줘.
조건은: 8자 이상, 대문자 포함, 소문자 포함, 숫자 포함
```

**AI가 작성한 테스트 (1단계 -- 테스트 먼저):**

```python
# examples/python/chapter05/ex21_06_test_first.py
import unittest


class TestPasswordValidator(unittest.TestCase):
    """비밀번호 검증 함수의 테스트 (구현보다 먼저 작성!)"""

    def test_valid_password(self):
        """유효한 비밀번호는 True를 반환해야 합니다"""
        self.assertTrue(validate_password("MyPass123"))
        self.assertTrue(validate_password("HelloWorld99"))
        self.assertTrue(validate_password("Abcdefg1"))

    def test_too_short(self):
        """8자 미만이면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("Ab1"))
        self.assertFalse(validate_password("Pass1"))
        self.assertFalse(validate_password("Abcdef7"))  # 7자

    def test_no_uppercase(self):
        """대문자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("mypass123"))

    def test_no_lowercase(self):
        """소문자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("MYPASS123"))

    def test_no_digit(self):
        """숫자가 없으면 False를 반환해야 합니다"""
        self.assertFalse(validate_password("MyPassword"))

    def test_empty_password(self):
        """빈 문자열이면 False를 반환해야 합니다"""
        self.assertFalse(validate_password(""))

    def test_password_feedback(self):
        """검증 실패 시 피드백 메시지를 반환해야 합니다"""
        is_valid, messages = validate_password_with_feedback("abc")
        self.assertFalse(is_valid)
        self.assertTrue(any("8자 이상" in m for m in messages))

    def test_valid_password_feedback(self):
        """유효한 비밀번호의 피드백은 빈 리스트여야 합니다"""
        is_valid, messages = validate_password_with_feedback("MyPass123")
        self.assertTrue(is_valid)
        self.assertEqual(len(messages), 0)
```

이 테스트를 지금 실행하면 당연히 실패합니다. `validate_password` 함수가 아직 존재하지 않기 때문입니다. 이것이 TDD의 핵심입니다 -- **실패하는 테스트에서 시작**합니다.

**AI에게 다시 요청합니다:**

```
위 테스트를 모두 통과하도록 validate_password와
validate_password_with_feedback 함수를 구현해줘.
```

**AI가 작성한 구현 (2단계 -- 구현):**

```python
def validate_password(password):
    """비밀번호가 유효한지 검증합니다.

    조건: 8자 이상, 대문자 포함, 소문자 포함, 숫자 포함
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True


def validate_password_with_feedback(password):
    """비밀번호를 검증하고 피드백 메시지를 반환합니다."""
    messages = []

    if len(password) < 8:
        messages.append("8자 이상이어야 합니다")
    if not any(c.isupper() for c in password):
        messages.append("대문자를 포함해야 합니다")
    if not any(c.islower() for c in password):
        messages.append("소문자를 포함해야 합니다")
    if not any(c.isdigit() for c in password):
        messages.append("숫자를 포함해야 합니다")

    is_valid = len(messages) == 0
    return is_valid, messages
```

**실행 결과:**
```
test_empty_password ... ok
test_no_digit ... ok
test_no_lowercase ... ok
test_no_uppercase ... ok
test_password_feedback ... ok
test_too_short ... ok
test_valid_password ... ok
test_valid_password_feedback ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

모든 테스트가 통과했습니다! 테스트를 먼저 작성했기 때문에:

1. **요구사항이 명확**합니다 -- "8자 이상", "대문자 포함" 등의 조건이 코드로 표현되어 있습니다
2. **구현이 완전**합니다 -- 빈 문자열, 피드백 메시지 등 엣지 케이스까지 고려합니다
3. **AI의 구현을 검증**할 수 있습니다 -- 테스트가 통과하면 구현이 올바르다고 확신할 수 있습니다

> **Tip:** AI에게 TDD를 요청하는 프롬프트 패턴을 기억하세요. **"이 기능의 테스트를 먼저 작성해 줘"** 그리고 **"이 테스트를 모두 통과하도록 구현해 줘"** -- 이 두 문장이 바이브 코딩에서 TDD의 핵심입니다.

---

### 21.5 테스트 통과시키기 -- Red-Green-Refactor 사이클

TDD의 핵심 리듬은 **Red-Green-Refactor** 세 단계의 반복입니다:

```
Red     →     Green     →     Refactor
(실패)         (통과)          (개선)
  ↑                              |
  └──────────────────────────────┘
           (반복)
```

| 단계 | 의미 | 행동 |
|------|------|------|
| **Red** | 테스트가 실패하는 상태 | 테스트를 먼저 작성한다 |
| **Green** | 테스트가 통과하는 상태 | 최소한의 코드로 테스트를 통과시킨다 |
| **Refactor** | 코드를 개선하는 단계 | 테스트가 보호해 주니 안심하고 코드를 정리한다 |

**예제 21-7: Red-Green-Refactor 사이클 데모**

이 예제는 계산기(Calculator) 클래스를 TDD로 만드는 전체 과정을 보여줍니다.

```python
# examples/python/chapter05/ex21_07_red_green_refactor.py

# [1단계 Red] 빈 클래스 - 테스트가 실패합니다
class CalculatorV1:
    """버전 1: 빈 클래스 (아직 구현 없음)"""
    pass

# 이 상태에서 calc.add(2, 3)을 호출하면 AttributeError가 발생합니다!


# [2단계 Green] 최소한의 구현 - 테스트를 통과시킵니다
class CalculatorV2:
    """버전 2: 최소한의 구현"""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b


# [3단계 Refactor] 코드 개선 - 연산 이력 기능 추가
class CalculatorV3:
    """버전 3: 리팩토링된 버전 - 연산 이력 기록"""

    def __init__(self):
        self.history = []

    def _record(self, expression, result):
        """연산 이력을 기록합니다."""
        self.history.append(f"{expression} = {result}")

    def add(self, a, b):
        result = a + b
        self._record(f"{a} + {b}", result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record(f"{a} - {b}", result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record(f"{a} * {b}", result)
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        result = a / b
        self._record(f"{a} / {b}", result)
        return result

    def get_history(self):
        return self.history.copy()

    def clear_history(self):
        self.history.clear()
```

각 단계의 테스트 결과를 살펴보겠습니다:

```python
class TestCalculatorRefactored(unittest.TestCase):
    """Refactor 단계: 기존 테스트 + 새 기능 테스트"""

    def setUp(self):
        self.calc = CalculatorV3()

    # 기존 테스트는 여전히 통과해야 합니다!
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    # 새로 추가된 기능에 대한 테스트
    def test_history_recorded(self):
        """연산 이력이 기록되는지 확인"""
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], "1 + 2 = 3")
        self.assertEqual(history[1], "3 * 4 = 12")

    def test_clear_history(self):
        """이력 초기화 테스트"""
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)
```

**실행 결과:**
```
[1단계] Red - 테스트 실패
  실행: 1개 | 실패/에러: 1개
  결과: 실패! (예상대로)
  이유: CalculatorV1에 add() 메서드가 없습니다

[2단계] Green - 테스트를 통과시키는 구현
  실행: 5개 | 통과: 5개
  결과: 통과!

[3단계] Refactor - 코드 구조 개선
  실행: 7개 | 통과: 7개
  결과: 통과!
  기존 테스트 + 새 기능 테스트 모두 통과!
```

이 사이클의 핵심은 **기존 테스트가 리팩토링 후에도 여전히 통과한다**는 것입니다. 이것이 바로 테스트가 제공하는 "안전망"입니다.

> **Warning:** Refactor 단계에서 가장 중요한 원칙은 "기존 테스트를 절대 수정하지 않는 것"입니다. 기존 테스트가 실패한다면 리팩토링이 잘못된 것입니다. 테스트는 기능의 계약이므로, 기능이 바뀌지 않는 한 테스트도 바뀌면 안 됩니다.

---

### 21.6 리팩토링 -- 테스트가 보호해 주는 코드 개선

리팩토링이란 **외부 동작은 그대로 유지하면서** 내부 구조를 개선하는 것입니다. 테스트가 없으면 리팩토링은 두려운 작업입니다 -- "혹시 뭔가 깨뜨리지는 않을까?" 하지만 테스트가 있으면 안심하고 코드를 정리할 수 있습니다.

**예제 21-8: 리팩토링 후 테스트 확인**

다음은 학생 성적 관리 시스템을 리팩토링하는 과정입니다.

**리팩토링 전:** 모든 로직이 하나의 함수에 몰려 있습니다.

```python
# examples/python/chapter05/ex21_08_refactoring_test.py
def calculate_student_result_before(scores):
    """리팩토링 전: 한 함수에 모든 로직이 몰려 있는 코드"""
    if not scores:
        return {"average": 0, "grade": "F", "passed": False}

    total = 0
    for s in scores:
        total = total + s
    avg = total / len(scores)

    if avg >= 90:
        grade = "A"
    elif avg >= 80:
        grade = "B"
    elif avg >= 70:
        grade = "C"
    elif avg >= 60:
        grade = "D"
    else:
        grade = "F"

    passed = avg >= 60
    return {"average": round(avg, 1), "grade": grade, "passed": passed}
```

**리팩토링 후:** 역할별로 함수를 분리합니다.

```python
def calculate_average(scores):
    """점수 리스트의 평균을 계산합니다."""
    if not scores:
        return 0
    return round(sum(scores) / len(scores), 1)


def determine_grade(average):
    """평균 점수에 따른 학점을 결정합니다."""
    grade_thresholds = [
        (90, "A"), (80, "B"), (70, "C"), (60, "D"),
    ]
    for threshold, grade in grade_thresholds:
        if average >= threshold:
            return grade
    return "F"


def is_passed(average, passing_score=60):
    """통과 여부를 판단합니다."""
    return average >= passing_score


def calculate_student_result_after(scores):
    """리팩토링 후: 각 역할을 분리하여 깔끔해진 코드"""
    avg = calculate_average(scores)
    grade = determine_grade(avg)
    passed = is_passed(avg)
    return {"average": avg, "grade": grade, "passed": passed}
```

리팩토링에서 가장 중요한 것은 **"전후 결과가 동일한가?"**입니다. 테스트로 이를 보장합니다:

```python
class TestStudentResultConsistency(unittest.TestCase):
    """리팩토링 전후 결과 일관성 테스트"""

    def test_same_result_high_scores(self):
        """높은 점수: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [95, 88, 92, 100]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)

    def test_same_result_low_scores(self):
        """낮은 점수: 리팩토링 전후 결과가 동일해야 합니다"""
        scores = [40, 55, 30, 45]
        before = calculate_student_result_before(scores)
        after = calculate_student_result_after(scores)
        self.assertEqual(before, after)

    def test_same_result_empty(self):
        """빈 리스트: 리팩토링 전후 결과가 동일해야 합니다"""
        before = calculate_student_result_before([])
        after = calculate_student_result_after([])
        self.assertEqual(before, after)
```

그리고 분리된 각 함수도 개별적으로 테스트합니다:

```python
class TestRefactoredFunctions(unittest.TestCase):
    """리팩토링 후 분리된 함수들의 개별 테스트"""

    def test_average_normal(self):
        self.assertEqual(calculate_average([80, 90, 100]), 90.0)

    def test_average_empty(self):
        self.assertEqual(calculate_average([]), 0)

    def test_grade_a(self):
        self.assertEqual(determine_grade(95), "A")
        self.assertEqual(determine_grade(90), "A")

    def test_grade_f(self):
        self.assertEqual(determine_grade(50), "F")

    def test_passed(self):
        self.assertTrue(is_passed(60))
        self.assertTrue(is_passed(100))

    def test_failed(self):
        self.assertFalse(is_passed(59))

    def test_custom_passing_score(self):
        """커스텀 합격 점수 사용"""
        self.assertTrue(is_passed(70, passing_score=70))
        self.assertFalse(is_passed(69, passing_score=70))
```

**실행 결과:**
```
test_same_result_empty ... ok
test_same_result_high_scores ... ok
test_same_result_low_scores ... ok
test_average_empty ... ok
test_average_normal ... ok
test_custom_passing_score ... ok
test_failed ... ok
test_grade_a ... ok
test_grade_f ... ok
test_passed ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.001s

OK
```

리팩토링의 장점을 정리하면:

| 리팩토링 전 | 리팩토링 후 |
|-------------|-------------|
| 한 함수에 모든 로직 | 역할별로 함수 분리 |
| 테스트가 어려움 | 각 함수를 독립적으로 테스트 가능 |
| 수정 시 전체에 영향 | 해당 함수만 수정하면 됨 |
| 재사용 불가 | `determine_grade()` 등을 다른 곳에서도 사용 가능 |

> **Note:** AI에게 리팩토링을 요청할 때는 이렇게 말하세요: "이 함수가 너무 길어요. 역할별로 분리해 주되, 기존 테스트가 모두 통과하도록 해 줘." 테스트가 있으면 AI의 리팩토링 결과도 즉시 검증할 수 있습니다.

---

### 21.7 실전 TDD 실습 -- 문자열 유틸리티

이제 실전 예제로 TDD를 적용해 보겠습니다. 다양한 문자열 유틸리티 함수를 테스트 먼저 작성하고, 그 다음에 구현합니다.

**예제 21-9: TDD로 문자열 유틸리티 만들기**

```python
# examples/python/chapter05/ex21_09_string_utils_tdd.py
import unittest


# 구현된 함수들
def capitalize_words(text):
    """각 단어의 첫 글자를 대문자로 변환합니다."""
    if not text:
        return ""
    return " ".join(word.capitalize() for word in text.split())


def reverse_string(text):
    """문자열을 뒤집습니다."""
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    return text[::-1]


def is_palindrome(text):
    """회문(팰린드롬)인지 확인합니다. 대소문자와 공백을 무시합니다."""
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def count_vowels(text):
    """영문 모음(a, e, i, o, u)의 개수를 셉니다."""
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    vowels = set("aeiouAEIOU")
    return sum(1 for char in text if char in vowels)


def truncate(text, max_length, suffix="..."):
    """문자열을 지정된 길이로 자릅니다."""
    if not isinstance(text, str):
        raise TypeError("문자열만 입력 가능합니다")
    if max_length < len(suffix):
        raise ValueError(f"max_length는 {len(suffix)} 이상이어야 합니다")
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def snake_to_camel(text):
    """snake_case를 camelCase로 변환합니다."""
    if not text:
        return ""
    parts = text.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])
```

이 함수들에 대한 테스트를 살펴보겠습니다:

```python
class TestCapitalizeWords(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")

    def test_already_capitalized(self):
        self.assertEqual(capitalize_words("Hello World"), "Hello World")

    def test_all_uppercase(self):
        self.assertEqual(capitalize_words("HELLO WORLD"), "Hello World")

    def test_empty_string(self):
        self.assertEqual(capitalize_words(""), "")


class TestIsPalindrome(unittest.TestCase):

    def test_english_palindrome(self):
        self.assertTrue(is_palindrome("level"))
        self.assertTrue(is_palindrome("racecar"))

    def test_korean_palindrome(self):
        self.assertTrue(is_palindrome("토마토"))
        self.assertTrue(is_palindrome("기러기"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_case_insensitive(self):
        self.assertTrue(is_palindrome("Level"))

    def test_with_spaces(self):
        self.assertTrue(is_palindrome("nurses run"))


class TestTruncate(unittest.TestCase):

    def test_no_truncation_needed(self):
        self.assertEqual(truncate("hello", 10), "hello")

    def test_truncation(self):
        self.assertEqual(truncate("Hello World", 8), "Hello...")

    def test_custom_suffix(self):
        self.assertEqual(truncate("Hello World", 9, suffix="~"), "Hello Wo~")

    def test_too_small_max_length(self):
        with self.assertRaises(ValueError):
            truncate("Hello", 2, suffix="...")


class TestSnakeToCamel(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_multiple_words(self):
        self.assertEqual(snake_to_camel("my_variable_name"), "myVariableName")

    def test_single_word(self):
        self.assertEqual(snake_to_camel("hello"), "hello")
```

**실행 결과:**
```
test_all_uppercase ... ok
test_already_capitalized ... ok
test_basic ... ok
test_empty_string ... ok
test_case_insensitive ... ok
test_english_palindrome ... ok
test_korean_palindrome ... ok
test_not_palindrome ... ok
test_with_spaces ... ok
test_custom_suffix ... ok
test_no_truncation_needed ... ok
test_too_small_max_length ... ok
test_truncation ... ok
test_basic ... ok
test_multiple_words ... ok
test_single_word ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.002s

OK
```

6개 함수에 대해 16개의 테스트가 모두 통과합니다. 각 함수의 다양한 상황을 커버하기 때문에, 나중에 함수를 수정하더라도 이 테스트가 올바름을 보장합니다.

> **Tip:** 테스트를 작성할 때는 **정상 케이스뿐만 아니라 경계 케이스(edge case)**도 반드시 포함하세요. 빈 문자열, 한 글자, 매우 긴 문자열, 한국어 입력 등 다양한 상황을 테스트하면 훨씬 견고한 코드가 됩니다.

---

### 21.8 실전 TDD 실습 -- 데이터 검증기

더 실용적인 예제로, 실무에서 자주 필요한 **데이터 검증기**를 TDD로 만들어 보겠습니다.

**예제 21-10: TDD로 데이터 검증기 만들기**

이 예제는 이메일, 전화번호, 날짜를 검증하는 함수들을 테스트 주도로 개발합니다.

```python
# examples/python/chapter05/ex21_10_data_validator_tdd.py
import unittest
import re
from datetime import datetime


def validate_email(email):
    """이메일 주소가 유효한지 검증합니다.
    Returns: (is_valid: bool, message: str)
    """
    if not isinstance(email, str):
        return False, "이메일은 문자열이어야 합니다"
    if not email or email.strip() != email:
        return False, "이메일에 공백이 포함되어서는 안 됩니다"
    if " " in email:
        return False, "이메일에 공백이 포함되어서는 안 됩니다"

    at_count = email.count("@")
    if at_count == 0:
        return False, "이메일에 @가 포함되어야 합니다"
    if at_count > 1:
        return False, "이메일에 @가 하나만 있어야 합니다"

    local, domain = email.split("@")
    if not local:
        return False, "@ 앞에 사용자명이 필요합니다"
    if not domain:
        return False, "@ 뒤에 도메인이 필요합니다"
    if "." not in domain:
        return False, "도메인에 점(.)이 포함되어야 합니다"

    return True, "유효한 이메일입니다"


def validate_phone(phone):
    """한국 전화번호가 유효한지 검증합니다.
    Returns: (is_valid: bool, message: str)
    """
    if not isinstance(phone, str):
        return False, "전화번호는 문자열이어야 합니다"

    digits = re.sub(r"[\s\-]", "", phone)
    if not digits.isdigit():
        return False, "전화번호에는 숫자, 하이픈(-), 공백만 허용됩니다"
    if len(digits) < 10 or len(digits) > 11:
        return False, "전화번호는 10~11자리여야 합니다"

    valid_prefixes = ("010", "011", "016", "017", "018", "019",
                      "02", "031", "032", "033", "041", "042",
                      "043", "044", "051", "052", "053", "054",
                      "055", "061", "062", "063", "064")
    if not any(digits.startswith(prefix) for prefix in valid_prefixes):
        return False, "유효하지 않은 지역번호입니다"

    return True, "유효한 전화번호입니다"


def validate_date(date_str, fmt="%Y-%m-%d"):
    """날짜 문자열이 유효한지 검증합니다.
    Returns: (is_valid: bool, message: str)
    """
    if not isinstance(date_str, str):
        return False, "날짜는 문자열이어야 합니다"
    if not date_str.strip():
        return False, "날짜가 비어있습니다"

    try:
        parsed = datetime.strptime(date_str, fmt)
    except ValueError:
        return False, f"날짜 형식이 올바르지 않습니다 (올바른 형식: {fmt})"

    if parsed.year < 1900:
        return False, "연도는 1900년 이후여야 합니다"
    if parsed.year > 2100:
        return False, "연도는 2100년 이전이어야 합니다"

    return True, "유효한 날짜입니다"
```

이 검증 함수들에 대한 테스트를 살펴보겠습니다:

```python
class TestValidateEmail(unittest.TestCase):

    def test_valid_emails(self):
        """유효한 이메일 주소들"""
        valid_emails = [
            "user@example.com",
            "test@domain.co.kr",
            "hello.world@email.org",
        ]
        for email in valid_emails:
            is_valid, msg = validate_email(email)
            self.assertTrue(is_valid, f"'{email}'은 유효해야 합니다: {msg}")

    def test_missing_at(self):
        is_valid, msg = validate_email("userexample.com")
        self.assertFalse(is_valid)
        self.assertIn("@", msg)

    def test_no_domain(self):
        is_valid, msg = validate_email("user@")
        self.assertFalse(is_valid)

    def test_no_dot_in_domain(self):
        is_valid, msg = validate_email("user@example")
        self.assertFalse(is_valid)
        self.assertIn("점", msg)


class TestValidatePhone(unittest.TestCase):

    def test_valid_mobile_with_dash(self):
        is_valid, msg = validate_phone("010-1234-5678")
        self.assertTrue(is_valid, msg)

    def test_valid_mobile_no_dash(self):
        is_valid, msg = validate_phone("01012345678")
        self.assertTrue(is_valid, msg)

    def test_too_short(self):
        is_valid, msg = validate_phone("010-123")
        self.assertFalse(is_valid)

    def test_invalid_chars(self):
        is_valid, msg = validate_phone("010-abcd-5678")
        self.assertFalse(is_valid)


class TestValidateDate(unittest.TestCase):

    def test_valid_date(self):
        is_valid, msg = validate_date("2024-01-15")
        self.assertTrue(is_valid, msg)

    def test_valid_leap_year(self):
        is_valid, msg = validate_date("2024-02-29")
        self.assertTrue(is_valid, msg)

    def test_invalid_leap_year(self):
        is_valid, msg = validate_date("2023-02-29")
        self.assertFalse(is_valid)

    def test_invalid_format(self):
        is_valid, msg = validate_date("15/01/2024")
        self.assertFalse(is_valid)
        self.assertIn("형식", msg)

    def test_too_old(self):
        is_valid, msg = validate_date("1899-12-31")
        self.assertFalse(is_valid)
        self.assertIn("1900", msg)
```

그리고 종합 검증기 클래스까지 테스트합니다:

```python
class DataValidator:
    """여러 필드를 한 번에 검증하는 종합 검증기"""

    def __init__(self):
        self.errors = []

    def validate(self, data):
        self.errors = []
        if "email" in data:
            valid, msg = validate_email(data["email"])
            if not valid:
                self.errors.append(f"이메일: {msg}")
        if "phone" in data:
            valid, msg = validate_phone(data["phone"])
            if not valid:
                self.errors.append(f"전화번호: {msg}")
        if "birth_date" in data:
            valid, msg = validate_date(data["birth_date"])
            if not valid:
                self.errors.append(f"생년월일: {msg}")
        return len(self.errors) == 0, self.errors


class TestDataValidator(unittest.TestCase):

    def setUp(self):
        self.validator = DataValidator()

    def test_all_valid(self):
        data = {
            "email": "user@example.com",
            "phone": "010-1234-5678",
            "birth_date": "1990-05-15"
        }
        is_valid, errors = self.validator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_all_invalid(self):
        data = {
            "email": "invalid-email",
            "phone": "abc",
            "birth_date": "not-a-date"
        }
        is_valid, errors = self.validator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 3)

    def test_error_messages_are_descriptive(self):
        data = {"email": "bad", "phone": "bad"}
        is_valid, errors = self.validator.validate(data)
        self.assertFalse(is_valid)
        has_email_error = any("이메일" in e for e in errors)
        has_phone_error = any("전화번호" in e for e in errors)
        self.assertTrue(has_email_error)
        self.assertTrue(has_phone_error)
```

**실행 결과:**
```
test_valid_emails ... ok
test_missing_at ... ok
test_no_domain ... ok
test_no_dot_in_domain ... ok
test_valid_mobile_with_dash ... ok
test_valid_mobile_no_dash ... ok
test_too_short ... ok
test_invalid_chars ... ok
test_valid_date ... ok
test_valid_leap_year ... ok
test_invalid_leap_year ... ok
test_invalid_format ... ok
test_too_old ... ok
test_all_valid ... ok
test_all_invalid ... ok
test_error_messages_are_descriptive ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.003s

OK
```

이 예제에서 TDD의 가치를 확인할 수 있습니다:

1. **테스트가 명세서**: 이메일에 `@`가 없으면? 전화번호에 문자가 섞이면? 윤년 2월 29일은? 모든 케이스가 코드로 정의되어 있습니다
2. **에러 메시지 검증**: 단순히 "실패"만 확인하는 게 아니라, 에러 메시지에 "점"이나 "1900" 같은 유용한 정보가 포함되는지도 테스트합니다
3. **종합 테스트**: 개별 함수뿐만 아니라 여러 함수를 조합한 `DataValidator`까지 테스트하여 통합 동작을 확인합니다

> **Note:** 실무에서 입력 검증은 가장 중요한 보안 요소 중 하나입니다. TDD로 검증 함수를 개발하면, 빠뜨리기 쉬운 엣지 케이스(빈 문자열, 잘못된 타입, 경계값 등)를 체계적으로 처리할 수 있습니다.

---

### 21.9 테스트 커버리지

#### 테스트 커버리지란?

**테스트 커버리지(Test Coverage)**는 "전체 코드 중에서 테스트가 실행하는 코드의 비율"을 나타내는 지표입니다. 예를 들어 100줄의 코드 중 80줄이 테스트에 의해 실행된다면, 커버리지는 80%입니다.

```
커버리지 = (테스트가 실행한 코드 줄 수 / 전체 코드 줄 수) x 100%
```

#### 커버리지의 종류

| 종류 | 설명 | 예시 |
|------|------|------|
| **라인 커버리지** | 전체 코드 줄 중 실행된 줄의 비율 | 100줄 중 80줄 실행 = 80% |
| **브랜치 커버리지** | 모든 분기(if/else) 중 실행된 분기의 비율 | 10개 분기 중 7개 실행 = 70% |
| **함수 커버리지** | 전체 함수 중 호출된 함수의 비율 | 20개 함수 중 18개 호출 = 90% |

#### 커버리지 측정 방법

파이썬에서는 표준 라이브러리는 아니지만, 널리 사용되는 `coverage` 도구로 커버리지를 측정할 수 있습니다. 하지만 표준 라이브러리만으로도 기본적인 커버리지 개념을 이해하고 적용할 수 있습니다.

**직접 커버리지를 확인하는 방법:**

테스트가 어떤 경로를 실행하는지 직접 분석해 봅시다. 예제 21-4의 `parse_age` 함수를 다시 살펴보겠습니다:

```python
def parse_age(value):                    # 1. 함수 진입
    if not isinstance(value, str):       # 2. 타입 검사
        raise TypeError(...)             # 2a. TypeError 경로
    try:
        age = int(value)                 # 3. 변환 시도
    except ValueError:
        raise ValueError(...)            # 3a. ValueError 경로
    if age < 0:                          # 4. 음수 검사
        raise ValueError(...)            # 4a. 음수 에러 경로
    if age > 150:                        # 5. 상한 검사
        raise ValueError(...)            # 5a. 상한 에러 경로
    return age                           # 6. 정상 반환
```

이 함수에는 6개의 실행 경로가 있습니다. 우리의 테스트는 이 모든 경로를 실행할까요?

| 경로 | 테스트 | 커버 여부 |
|------|--------|-----------|
| 정상 반환 | `test_valid_age("25")` | 커버됨 |
| TypeError | `test_non_string_input(25)` | 커버됨 |
| ValueError (변환 실패) | `test_non_numeric_string("스물다섯")` | 커버됨 |
| ValueError (음수) | `test_negative_age("-5")` | 커버됨 |
| ValueError (상한) | `test_too_old("200")` | 커버됨 |

모든 경로가 테스트에 의해 실행되므로, 이 함수의 커버리지는 **100%**입니다.

#### 커버리지가 높다고 버그가 없는 건 아닙니다

커버리지는 중요한 지표이지만, 100% 커버리지가 곧 버그 없는 코드를 의미하지는 않습니다.

```python
def add(a, b):
    return a + b

# 이 테스트는 커버리지 100%이지만...
class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)  # 양수만 테스트
```

위 코드의 커버리지는 100%이지만, 음수나 소수점, 큰 수 등은 테스트하지 않습니다. 커버리지는 **최소한의 기준**이지, 충분한 기준은 아닙니다.

#### 효과적인 커버리지 전략

AI에게 다음과 같이 요청하면 커버리지를 높일 수 있습니다:

```
이 함수의 테스트를 작성해 줘.
정상 케이스뿐만 아니라 다음 상황도 테스트해 줘:
- 빈 입력
- 잘못된 타입
- 경계값 (최소, 최대)
- 예외 상황
```

일반적인 커버리지 목표:

| 수준 | 커버리지 | 의미 |
|------|----------|------|
| 최소 | 60% 이상 | 핵심 기능은 테스트됨 |
| 권장 | 80% 이상 | 대부분의 코드가 테스트됨 |
| 이상적 | 90% 이상 | 거의 모든 경로가 테스트됨 |

> **Warning:** 커버리지 100%를 목표로 삼기보다는, **중요한 비즈니스 로직과 에러 처리 경로**를 우선적으로 테스트하세요. 단순 getter/setter나 로그 출력 코드까지 100% 테버리지를 채우려고 하면 오히려 유지보수 비용만 늘어납니다.

---

### 정리

이번 장에서 배운 핵심 내용을 정리합니다.

**테스트의 가치:**

- 테스트 코드는 "내 코드가 맞는지" 자동으로 확인해 주는 안전망입니다
- 바이브 코딩에서 테스트는 AI가 생성한 코드를 검증하는 **신뢰의 도구**입니다
- 테스트가 있으면 안심하고 코드를 수정하고 개선할 수 있습니다

**unittest 핵심:**

| 구성 요소 | 설명 |
|-----------|------|
| `unittest.TestCase` | 테스트 클래스의 부모 클래스 |
| `test_` 메서드 | 테스트를 정의하는 메서드 (반드시 `test_`로 시작) |
| `assertEqual` 등 | 기대값과 실제값을 비교하는 assert 메서드 |
| `setUp/tearDown` | 각 테스트 전후에 실행되는 픽스처 |
| `assertRaises` | 예외 발생을 검증하는 메서드 |

**TDD의 세 박자:**

1. **Red** -- 실패하는 테스트를 먼저 작성합니다. "무엇을 만들 것인가"를 명확히 합니다
2. **Green** -- 테스트를 통과하는 최소한의 코드를 작성합니다. "일단 동작하게 만듭니다"
3. **Refactor** -- 테스트가 보호해 주니 안심하고 코드를 개선합니다. "더 좋은 코드로 바꿉니다"

**바이브 코딩에서의 TDD 프롬프트 패턴:**

```
1단계: "이 기능의 테스트를 먼저 작성해 줘"
2단계: "이 테스트를 모두 통과하도록 구현해 줘"
3단계: "테스트가 통과하는 상태에서 코드를 리팩토링해 줘"
```

> **Note:** 테스트 코드를 작성하는 것은 처음에는 번거롭게 느껴질 수 있습니다. 하지만 프로젝트가 커질수록, 그리고 AI와 더 많이 협업할수록, 테스트의 가치는 기하급수적으로 커집니다. "테스트 먼저"의 습관을 지금부터 들여 보세요. 미래의 여러분이 감사할 것입니다.

---

### 연습 문제

**연습 1: 기본 테스트 작성**

다음 함수에 대한 테스트를 작성하세요. 최소 5개의 테스트 메서드를 포함해야 합니다:

```python
def calculate_bmi(weight_kg, height_m):
    """체질량지수(BMI)를 계산합니다.
    BMI = 체중(kg) / 키(m)^2
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("체중과 키는 양수여야 합니다")
    return round(weight_kg / (height_m ** 2), 1)
```

힌트: 정상 케이스, 경계값, 예외 상황을 모두 테스트하세요.

---

**연습 2: TDD로 함수 만들기**

다음 요구사항에 대해 테스트를 먼저 작성한 후, 구현을 완성하세요:

> `format_currency(amount)` 함수는 숫자를 한국 원화 형식으로 변환합니다.
> - `format_currency(1000)` -> `"1,000원"`
> - `format_currency(1234567)` -> `"1,234,567원"`
> - `format_currency(0)` -> `"0원"`
> - 음수는 ValueError를 발생시킵니다

---

**연습 3: 리팩토링 연습**

다음 코드를 리팩토링하되, 리팩토링 전후 결과가 동일한지 확인하는 테스트를 먼저 작성하세요:

```python
def process_scores(names, scores):
    """학생별 등급을 매기고 결과를 반환합니다."""
    results = []
    for i in range(len(names)):
        if scores[i] >= 90:
            results.append({"name": names[i], "score": scores[i], "grade": "우수"})
        elif scores[i] >= 70:
            results.append({"name": names[i], "score": scores[i], "grade": "보통"})
        else:
            results.append({"name": names[i], "score": scores[i], "grade": "미흡"})
    return results
```

힌트: `zip()`을 활용하고, 등급 판정 로직을 별도 함수로 분리하세요.

---

**연습 4: 종합 실습**

AI에게 다음과 같이 요청하여 TDD 전체 사이클을 직접 경험해 보세요:

```
회원가입 폼 검증기를 만들고 싶어.
검증 항목: 이름(2~20자), 이메일, 비밀번호(8자 이상, 대소문자+숫자)
테스트 코드를 먼저 작성해 줘. unittest를 사용해 줘.
```

테스트를 받은 후 직접 구현을 해 보고, AI의 구현과 비교해 보세요.

---

### 다음 장 예고

**Chapter 22: 성능 최적화 기초**

코드가 올바르게 동작하는 것을 확인했다면, 다음 단계는 **빠르게 동작하게 만드는 것**입니다. 다음 장에서는 코드의 실행 시간을 측정하고, AI에게 "이 코드를 더 빠르게 만들어 줘"라고 요청하는 방법을 배웁니다. 시간 복잡도(Big-O), 프로파일링, 캐싱 등의 최적화 기법을 실습합니다.
