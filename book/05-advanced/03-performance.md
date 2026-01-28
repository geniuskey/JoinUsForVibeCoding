# Chapter 22: 성능 최적화

프로그램이 정확하게 동작하는 것은 기본입니다. 하지만 실제 서비스에서는 **얼마나 빠르게** 동작하는지도 매우 중요합니다. 같은 결과를 내더라도 1초 만에 끝나는 코드와 10분이 걸리는 코드는 완전히 다른 품질의 프로그램입니다. 이 장에서는 Python 코드의 성능을 측정하고, 병목 지점을 찾아내며, 체계적으로 최적화하는 방법을 배웁니다. 특히 AI 어시스턴트에게 최적화를 요청하는 효과적인 방법도 함께 알아봅니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- **성능 최적화**가 왜 중요한지 이해하고 설명할 수 있다
- `time.time()`과 `time.perf_counter()`로 **실행 시간을 측정**할 수 있다
- `timeit` 모듈로 **정밀한 벤치마크**를 수행할 수 있다
- `cProfile`로 **프로파일링**하여 병목 지점을 찾을 수 있다
- **빅오(Big-O) 표기법**을 이해하고 알고리즘 효율을 평가할 수 있다
- **자료구조 선택**, **제너레이터**, **캐싱** 등 일반적인 최적화 기법을 적용할 수 있다
- AI 어시스턴트에게 **최적화를 효과적으로 요청**할 수 있다

---

## 22.1 성능이 중요한 이유

프로그래밍을 처음 배울 때는 "작동하면 된다"고 생각하기 쉽습니다. 하지만 다음과 같은 상황을 생각해봅시다.

| 상황 | 느린 코드 | 빠른 코드 |
|------|----------|----------|
| 웹 페이지 응답 | 5초 대기 --> 사용자 이탈 | 0.3초 응답 --> 쾌적한 경험 |
| 데이터 분석 | 10만 건 처리에 1시간 | 10만 건 처리에 10초 |
| 배치 작업 | 야간 8시간 소요 --> 업무 지연 | 1시간 완료 --> 여유 확보 |
| 모바일 앱 | 배터리 빠르게 소모 | 효율적인 전력 사용 |

성능 문제는 사용자 경험, 비용, 생산성에 직접적인 영향을 미칩니다.

### 최적화의 황금 규칙

성능 최적화에는 유명한 격언이 있습니다.

```
"섣부른 최적화는 모든 악의 근원이다."
    — Donald Knuth
```

이 말은 처음부터 최적화에 집착하지 말라는 뜻입니다. 올바른 최적화 순서는 다음과 같습니다:

1. **먼저 정확하게 동작하는 코드를 작성한다** (Make it work)
2. **코드를 깔끔하게 정리한다** (Make it right)
3. **성능이 필요한 부분을 측정한다** (Measure)
4. **병목 지점을 찾아 최적화한다** (Make it fast)

> **Note:** 최적화의 첫 번째 규칙은 **"측정하라"**입니다. 감으로 "이 부분이 느릴 것 같다"고 추측하지 마세요. 실제로 측정해보면 예상과 다른 곳이 병목인 경우가 많습니다.

---

## 22.2 실행 시간 측정: time 모듈

성능 최적화의 첫 단계는 **현재 코드가 얼마나 걸리는지 정확히 측정하는 것**입니다. Python에서 가장 기본적인 시간 측정 방법은 `time` 모듈을 사용하는 것입니다.

### time.time() vs time.perf_counter()

Python의 `time` 모듈에는 두 가지 주요 타이머가 있습니다.

| 함수 | 설명 | 용도 |
|------|------|------|
| `time.time()` | 벽시계(wall clock) 시간 | 일반적인 시간 측정 |
| `time.perf_counter()` | 고해상도 성능 카운터 | 정밀한 성능 측정 |

`time.perf_counter()`는 더 높은 해상도를 제공하므로, 짧은 코드의 성능을 측정할 때 더 정확한 결과를 얻을 수 있습니다.

### 예제 22-1: 실행 시간 측정

반복문으로 합계를 구하는 방식과 수학 공식(가우스 공식)을 사용하는 방식의 성능을 비교해봅시다.

```python
# examples/python/chapter05/ex22_01_time_measure.py
import time


def slow_sum(n):
    """느린 방식: 반복문으로 합계 계산"""
    total = 0
    for i in range(n):
        total += i
    return total


def fast_sum(n):
    """빠른 방식: 수학 공식으로 합계 계산 (가우스 공식)"""
    return n * (n - 1) // 2


def measure_with_perf_counter(func, *args):
    """time.perf_counter()를 사용한 시간 측정 (고해상도 타이머)"""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed
```

이 코드는 두 가지 방식으로 1부터 천만까지의 합을 구합니다. `measure_with_perf_counter()` 함수로 각각의 소요 시간을 측정합니다.

**실행:**

```bash
$ python examples/python/chapter05/ex22_01_time_measure.py
```

**결과:**

```
============================================================
  실행 시간 측정: time.time() vs time.perf_counter()
============================================================

[ time.time() 사용 ]
----------------------------------------
반복문 합계:    49,999,995,000,000
소요 시간:    0.246285초
공식 합계:      49,999,995,000,000
소요 시간:    0.000005초

[ time.perf_counter() 사용 (더 정밀) ]
----------------------------------------
반복문 합계:    49,999,995,000,000
소요 시간:    0.241889초
공식 합계:      49,999,995,000,000
소요 시간:    0.000005초

[ 비교 결과 ]
----------------------------------------
반복문 방식:  0.241889초
공식 방식:    0.000005초
속도 향상:    52,965배 빠름

[ 타이머 해상도 비교 ]
----------------------------------------
time.time() 해상도:         0.0000000010초
time.perf_counter() 해상도: 0.0000000010초
```

같은 결과를 내는 두 함수인데, 수학 공식을 사용한 방식이 **약 5만 배** 이상 빠릅니다. 반복문은 천만 번의 덧셈을 수행하지만, 가우스 공식은 단 한 번의 곱셈과 나눗셈으로 같은 결과를 얻습니다.

> **Tip:** 성능 측정 시에는 `time.time()` 대신 `time.perf_counter()`를 사용하세요. 시스템 시계 조정의 영향을 받지 않으며 더 높은 해상도를 제공합니다.

### 시간 측정의 기본 패턴

시간 측정의 기본 패턴은 매우 간단합니다.

```python
import time

start = time.perf_counter()
# --- 측정하고 싶은 코드 ---
result = some_function()
# --- 여기까지 ---
end = time.perf_counter()

print(f"소요 시간: {end - start:.6f}초")
```

이 패턴을 기억해두면 언제든 코드의 실행 시간을 빠르게 확인할 수 있습니다.

---

## 22.3 정밀한 벤치마크: timeit 모듈

`time.perf_counter()`는 간단한 측정에 유용하지만, 한 가지 문제가 있습니다. **한 번의 측정은 신뢰할 수 없습니다.** 시스템의 다른 프로세스, 가비지 컬렉션, CPU 캐시 상태 등에 의해 결과가 크게 달라질 수 있기 때문입니다.

`timeit` 모듈은 이 문제를 해결합니다. 코드를 **여러 번 반복 실행**하여 통계적으로 신뢰할 수 있는 결과를 제공합니다.

### timeit의 핵심 함수

| 함수 | 설명 | 반환값 |
|------|------|--------|
| `timeit.timeit(stmt, number)` | stmt를 number번 실행 | 총 소요 시간 (초) |
| `timeit.repeat(stmt, repeat, number)` | timeit을 repeat번 반복 | 각 실행의 시간 리스트 |

### 예제 22-2: timeit 사용법

문자열 연결 방법(+ 연산자, join, f-string)과 리스트 생성 방법(append, 리스트 컴프리헨션, map)의 성능을 `timeit`으로 정밀하게 비교합니다.

```python
# examples/python/chapter05/ex22_02_timeit_usage.py
import timeit


def method_concat_plus():
    """문자열 연결: + 연산자 사용"""
    result = ""
    for i in range(1000):
        result += str(i)
    return result


def method_concat_join():
    """문자열 연결: join() 사용"""
    return "".join(str(i) for i in range(1000))


def method_list_append():
    """리스트 생성: append() 사용"""
    result = []
    for i in range(10000):
        result.append(i * 2)
    return result


def method_list_comprehension():
    """리스트 생성: 리스트 컴프리헨션 사용"""
    return [i * 2 for i in range(10000)]
```

각 방법을 1000번씩, 5회 반복 측정하여 신뢰할 수 있는 결과를 얻습니다.

**실행:**

```bash
$ python examples/python/chapter05/ex22_02_timeit_usage.py
```

**결과:**

```
============================================================
  timeit 모듈을 활용한 정밀 성능 측정
============================================================

[ 테스트 1: 문자열 연결 방법 비교 ]
  (각 방법을 1000번씩, 5회 반복 측정)
--------------------------------------------------
  + 연산자            평균: 0.0665초  최소: 0.0639초
  join()           평균: 0.0543초  최소: 0.0539초
  f-string + join  평균: 0.0460초  최소: 0.0453초

  >>> 가장 빠른 방법: f-string + join

[ 테스트 2: 리스트 생성 방법 비교 ]
  (각 방법을 1000번씩, 5회 반복 측정)
--------------------------------------------------
  append()         평균: 0.2480초  최소: 0.2337초
  리스트 컴프리헨션        평균: 0.2091초  최소: 0.2067초
  map()            평균: 0.3517초  최소: 0.3432초

  >>> 가장 빠른 방법: 리스트 컴프리헨션

[ 정리 ]
--------------------------------------------------
  1. timeit.timeit()   : 총 실행 시간 반환 (간편 측정)
  2. timeit.repeat()   : 여러 번 반복 측정 (신뢰도 향상)
  3. min(times) 사용   : 최소값이 가장 신뢰할 수 있는 결과
  4. 리스트 컴프리헨션 > append() (일반적으로)
  5. join() > + 연산자 (문자열 연결 시)
```

결과를 분석하면 두 가지 중요한 교훈을 얻을 수 있습니다:

1. **문자열 연결**: `+` 연산자보다 `join()`이 빠르고, `f-string + join`이 가장 빠릅니다.
2. **리스트 생성**: `append()`보다 **리스트 컴프리헨션**이 빠릅니다.

> **Note:** `timeit.repeat()`의 결과에서는 **최소값(min)**을 기준으로 성능을 판단하는 것이 좋습니다. 평균값에는 가비지 컬렉션 등 외부 요인에 의한 지연이 포함될 수 있지만, 최소값은 "최적의 조건에서 이 코드가 이만큼 걸린다"는 것을 의미하기 때문입니다.

### timeit 간편 사용법

`timeit.timeit()`은 문자열로 된 코드를 직접 측정할 수도 있습니다.

```python
import timeit

# 간단한 표현식 직접 측정
elapsed = timeit.timeit(stmt="sorted(range(1000, 0, -1))", number=10000)
per_call = elapsed / 10000
print(f"1회 평균: {per_call * 1000:.4f}ms")
```

이 방식은 간단한 표현식의 성능을 빠르게 확인할 때 편리합니다.

> **Tip:** 터미널에서 `python -m timeit "표현식"` 명령으로 커맨드라인에서 바로 벤치마크를 할 수 있습니다. 예: `python -m timeit "[x**2 for x in range(100)]"`

---

## 22.4 프로파일링 기초: cProfile

시간 측정이 "이 코드가 얼마나 걸리는가?"에 대한 답이라면, 프로파일링은 **"이 코드의 어디가 느린가?"**에 대한 답입니다.

프로파일링은 프로그램의 각 함수가 **몇 번 호출**되었고, **얼마나 시간을 소비**했는지를 분석합니다. 이를 통해 최적화가 필요한 **병목 지점(bottleneck)**을 정확히 찾아낼 수 있습니다.

### cProfile 사용법

Python 표준 라이브러리의 `cProfile`은 가장 널리 사용되는 프로파일러입니다.

```python
import cProfile

# 방법 1: 함수 직접 프로파일링
cProfile.run('my_function()')

# 방법 2: 프로파일러 객체 사용 (더 세밀한 제어)
profiler = cProfile.Profile()
profiler.enable()
my_function()
profiler.disable()
```

### 예제 22-3: 프로파일링 결과 분석

데이터 처리 파이프라인(읽기 --> 필터링 --> 정렬 --> 통계 --> 포맷팅)을 프로파일링하여 어디가 가장 느린지 분석합니다.

```python
# examples/python/chapter05/ex22_03_profiling.py
import cProfile
import io
import pstats


def read_data(size):
    """데이터 읽기 시뮬레이션"""
    data = []
    for i in range(size):
        data.append({"id": i, "value": i * 2.5, "name": f"item_{i}"})
    return data


def filter_data(data, threshold):
    """조건에 맞는 데이터 필터링"""
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(item)
    return result


def sort_data(data):
    """데이터 정렬"""
    return sorted(data, key=lambda x: x["value"], reverse=True)


def format_output(data):
    """결과 포맷팅 (의도적으로 느리게 구현)"""
    lines = []
    for item in data:
        line = ""
        line = line + "ID: " + str(item["id"])
        line = line + " | "
        line = line + "값: " + str(item["value"])
        line = line + " | "
        line = line + "이름: " + item["name"]
        lines.append(line)
    return "\n".join(lines)


def calculate_statistics(data):
    """통계 계산 (의도적으로 비효율적)"""
    total = sum(item["value"] for item in data)
    count = len(data)
    average = total / count if count > 0 else 0
    max_val = max(item["value"] for item in data)
    min_val = min(item["value"] for item in data)
    variance = sum((item["value"] - average) ** 2 for item in data) / count
    return {
        "total": total, "count": count, "average": average,
        "max": max_val, "min": min_val, "variance": variance,
    }


def process_pipeline(size=50000):
    """전체 데이터 처리 파이프라인"""
    data = read_data(size)
    filtered = filter_data(data, threshold=50000)
    sorted_data = sort_data(filtered)
    stats = calculate_statistics(sorted_data)
    output = format_output(sorted_data[:100])
    return stats, output
```

**실행:**

```bash
$ python examples/python/chapter05/ex22_03_profiling.py
```

**결과:**

```
======================================================================
  cProfile 프로파일링 분석
======================================================================

[1단계] 프로파일링 실행 중...
[2단계] 프로파일링 결과 분석

[ 누적 시간 기준 상위 15개 함수 ]
----------------------------------------------------------------------
         230112 function calls in 0.072 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.072    0.072 ex22_03_profiling.py:79(process_pipeline)
        1    0.030    0.030    0.034    0.034 ex22_03_profiling.py:18(read_data)
        1    0.000    0.000    0.022    0.022 ex22_03_profiling.py:55(calculate_statistics)
        2    0.005    0.002    0.013    0.006 {built-in method builtins.sum}
        1    0.007    0.007    0.009    0.009 ex22_03_profiling.py:26(filter_data)
        1    0.000    0.000    0.007    0.007 ex22_03_profiling.py:35(sort_data)
```

### 프로파일링 결과 읽는 방법

프로파일링 출력의 각 열이 의미하는 바를 정확히 이해하는 것이 중요합니다.

| 열 | 의미 | 설명 |
|----|------|------|
| `ncalls` | 호출 횟수 | 해당 함수가 몇 번 호출되었는가 |
| `tottime` | 자체 실행 시간 | 하위 함수 호출 시간을 **제외**한 순수 실행 시간 |
| `percall` | 호출당 시간 | tottime / ncalls |
| `cumtime` | 누적 시간 | 하위 함수 호출 시간을 **포함**한 총 시간 |
| `filename:lineno` | 위치 | 파일명:줄번호(함수명) |

위 결과를 분석하면:

- `read_data()`: 자체 시간(tottime) 0.030초로 **가장 큰 시간을 소비** --> 최적화 1순위
- `calculate_statistics()`: 누적 시간(cumtime) 0.022초 --> 내부에서 호출하는 `sum()`, `max()`, `min()`이 각각 데이터를 순회
- `filter_data()`: tottime 0.007초 --> 개선 여지 있음

> **Tip:** `tottime`이 가장 큰 함수가 최적화 우선순위 1위입니다. `cumtime`은 참고용으로 사용하세요. `cumtime`이 크더라도 그 함수 자체가 느린 것이 아니라, 그 안에서 호출하는 다른 함수가 느린 것일 수 있습니다.

### 프로파일링 결과를 보기 좋게 출력하기

`pstats` 모듈을 사용하면 프로파일링 결과를 다양한 기준으로 정렬하고 필터링할 수 있습니다.

```python
import pstats
import io

# 프로파일러 결과를 pstats로 분석
stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)

# 누적 시간 기준 상위 10개
stats.sort_stats("cumulative")
stats.print_stats(10)

# 자체 시간 기준 상위 10개
stats.sort_stats("tottime")
stats.print_stats(10)
```

주요 정렬 옵션:

| 옵션 | 기준 |
|------|------|
| `"cumulative"` | 누적 시간 |
| `"tottime"` | 자체 시간 |
| `"calls"` | 호출 횟수 |
| `"filename"` | 파일명 |

---

## 22.5 빅오(Big-O) 표기법 이해

**빅오 표기법**은 알고리즘의 성능을 데이터 크기(n)에 따라 표현하는 방법입니다. 코드 레벨의 미세한 최적화보다 **알고리즘 자체의 효율성**이 성능에 훨씬 큰 영향을 미칩니다.

### 주요 시간 복잡도

| 표기 | 이름 | 예시 | n=10,000일 때 연산 수 |
|------|------|------|---------------------|
| O(1) | 상수 시간 | 딕셔너리 조회 | 1 |
| O(log n) | 로그 시간 | 이진 검색 | ~13 |
| O(n) | 선형 시간 | 리스트 순회 | 10,000 |
| O(n log n) | 선형 로그 | 정렬 (sorted) | ~130,000 |
| O(n^2) | 이차 시간 | 이중 반복문 | 100,000,000 |
| O(2^n) | 지수 시간 | 재귀 피보나치 | 천문학적 |

데이터가 커질수록 시간 복잡도의 차이는 극적으로 벌어집니다.

```
데이터 1,000개일 때:
  O(n)  =       1,000 연산
  O(n²) =   1,000,000 연산  (1,000배 차이)

데이터 100,000개일 때:
  O(n)  =         100,000 연산
  O(n²) = 10,000,000,000 연산  (100,000배 차이!)
```

### 예제 22-4: O(n^2)에서 O(n)으로 개선하기

중복 찾기 알고리즘을 예로 들어 시간 복잡도 개선의 효과를 확인합니다.

```python
# examples/python/chapter05/ex22_04_big_o_improvement.py
def find_duplicates_brute_force(data):
    """
    O(n^2) 방식: 이중 반복문으로 중복 찾기
    모든 원소 쌍을 비교하므로 데이터가 커지면 매우 느립니다.
    """
    duplicates = []
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates


def find_duplicates_with_set(data):
    """
    O(n) 방식: 집합(set)을 사용한 중복 찾기
    한 번의 순회로 중복을 찾을 수 있습니다.
    """
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
```

O(n^2) 방식은 모든 원소 쌍을 비교하는 **이중 반복문**입니다. 데이터가 5,000개만 되어도 최대 약 1,250만 번의 비교를 수행해야 합니다. 반면 O(n) 방식은 `set`의 O(1) 탐색을 활용하여 **한 번의 순회**만으로 중복을 찾습니다.

**실행:**

```bash
$ python examples/python/chapter05/ex22_04_big_o_improvement.py
```

**결과:**

```
=================================================================
  알고리즘 개선: O(n^2) --> O(n) 중복 찾기
=================================================================

[ 정확성 검증 ]
--------------------------------------------------
입력 데이터: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
O(n^2) 결과:  [1, 3, 5]
O(n) set:    [1, 3, 5]
O(n) dict:   [1, 3, 5]
결과 일치:   예

[ 데이터 크기별 성능 비교 ]
-----------------------------------------------------------------
      크기 |  O(n^2) 이중루프 |     O(n) set |    O(n) dict |  속도향상
-----------------------------------------------------------------
     500 |     0.002974초 |   0.000068초 |   0.000048초 |     44배
   1,000 |     0.010732초 |   0.000102초 |   0.000490초 |    106배
   2,000 |     0.044720초 |   0.000837초 |   0.000460초 |     53배
   5,000 |     0.281743초 |   0.000309초 |   0.000926초 |    913배
```

데이터 5,000개에서 이미 **900배 이상**의 차이가 발생합니다. O(n^2)은 이 크기에서 0.28초가 걸리지만, O(n)은 불과 0.0003초만에 같은 결과를 냅니다.

> **Note:** 코드 레벨의 소소한 최적화(변수명 줄이기, 한 줄로 합치기 등)보다 **알고리즘 개선**이 훨씬 효과적입니다. O(n^2)을 O(n)으로 바꾸는 것만으로 수백~수천 배의 성능 향상을 얻을 수 있습니다.

### 빅오 판별법

코드의 시간 복잡도를 판별하는 간단한 방법입니다:

```
반복문 없음                    --> O(1)
단일 반복문 (n번)               --> O(n)
중첩 반복문 2개 (n x n)         --> O(n^2)
반복마다 절반으로 줄어듦           --> O(log n)
정렬 사용                      --> O(n log n)
재귀 호출이 2갈래로 분기           --> O(2^n)
```

---

## 22.6 자료구조 선택의 중요성

같은 작업이라도 **어떤 자료구조를 사용하느냐**에 따라 성능이 크게 달라집니다. Python에서 가장 흔히 비교되는 것이 **리스트(list)**와 **집합(set)**입니다.

### 리스트 vs 집합: 핵심 차이

| 연산 | list | set | dict |
|------|------|-----|------|
| 검색 (`in`) | O(n) | O(1) | O(1) |
| 추가 (`add/append`) | O(1) | O(1) | O(1) |
| 삭제 | O(n) | O(1) | O(1) |
| 순서 보장 | 예 | 아니오 | 예 (3.7+) |
| 중복 허용 | 예 | 아니오 | 키 불가 |

핵심 차이는 **검색 성능**입니다. 리스트에서 원소를 찾으려면 처음부터 하나씩 비교해야 하므로 O(n)이지만, 집합은 해시 테이블을 사용하므로 평균 O(1)입니다.

### 예제 22-5: 리스트 vs 집합 성능 비교

다양한 크기의 데이터에서 리스트, 집합, 딕셔너리의 검색 성능을 비교합니다.

```python
# examples/python/chapter05/ex22_05_list_vs_set.py
def search_in_list(data_list, targets):
    """리스트에서 검색 (O(n) per lookup)"""
    found = 0
    for target in targets:
        if target in data_list:
            found += 1
    return found


def search_in_set(data_set, targets):
    """집합에서 검색 (O(1) average per lookup)"""
    found = 0
    for target in targets:
        if target in data_set:
            found += 1
    return found
```

**실행:**

```bash
$ python examples/python/chapter05/ex22_05_list_vs_set.py
```

**결과:**

```
=================================================================
  리스트 vs 집합 vs 딕셔너리: 검색 성능 비교
=================================================================

[ 테스트 1: 검색(in 연산) 성능 비교 ]
-----------------------------------------------------------------
    데이터 크기 |    검색 수 |       list |        set |       dict |  배율
-----------------------------------------------------------------
     1,000 |   1,000 |   0.0036초 |   0.0000초 |   0.0000초 |    83배
     5,000 |   1,000 |   0.0180초 |   0.0001초 |   0.0001초 |   195배
    10,000 |   1,000 |   0.0393초 |   0.0001초 |   0.0001초 |   285배
    50,000 |   1,000 |   0.4365초 |   0.0004초 |   0.0003초 | 1,104배
```

데이터가 50,000개일 때 리스트 검색은 집합 검색보다 **1,100배 이상** 느립니다. 이 차이는 데이터가 커질수록 더욱 벌어집니다.

### 메모리 vs 속도 트레이드오프

집합과 딕셔너리는 해시 테이블을 사용하므로 리스트보다 **메모리를 더 사용**합니다. 하지만 검색 속도의 향상이 메모리 비용을 압도적으로 보상합니다.

```
100,000개 데이터:
  list: ~800 KB
  set:  ~4 MB (약 5배)
  dict: ~5 MB (약 6배)
```

메모리를 5배 더 사용하지만, 검색 속도는 1,000배 이상 빨라집니다. 대부분의 경우 이것은 훌륭한 트레이드오프입니다.

> **Tip:** "이 데이터에서 특정 값이 있는지 자주 확인해야 한다"면 리스트 대신 집합(set)을 사용하세요. `if x in my_list:` 를 `if x in my_set:` 로 바꾸는 것만으로 극적인 성능 향상을 얻을 수 있습니다.

---

## 22.7 제너레이터로 메모리 최적화

성능 최적화는 속도만의 문제가 아닙니다. **메모리 사용량**도 중요한 성능 지표입니다. 대용량 데이터를 처리할 때 모든 데이터를 메모리에 올려놓으면 메모리 부족(OOM) 오류가 발생할 수 있습니다.

**제너레이터(generator)**는 이 문제를 해결합니다. 값을 한 번에 하나씩 생성하는 **게으른 평가(lazy evaluation)** 방식으로, 메모리를 획기적으로 절약합니다.

### 리스트 vs 제너레이터

```python
# 리스트: 모든 값을 메모리에 저장
squares_list = [i ** 2 for i in range(1_000_000)]     # ~8 MB

# 제너레이터: 한 번에 하나씩 생성
squares_gen = (i ** 2 for i in range(1_000_000))       # ~200 bytes
```

대괄호(`[]`)를 소괄호(`()`)로 바꾸는 것만으로 메모리 사용량이 **40,000배** 이상 줄어듭니다.

### 예제 22-6: 제너레이터 활용

리스트 방식과 제너레이터 방식으로 데이터 파이프라인을 구성하여 메모리와 속도를 비교합니다.

```python
# examples/python/chapter05/ex22_06_generator_usage.py
def squares_list(n):
    """리스트로 제곱수 생성 - 모든 값을 메모리에 저장"""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result


def squares_generator(n):
    """제너레이터로 제곱수 생성 - 한 번에 하나씩 생성"""
    for i in range(n):
        yield i ** 2


def pipeline_list(data_size):
    """리스트 기반 파이프라인 - 각 단계에서 전체 리스트 생성"""
    data = [i for i in range(data_size)]
    filtered = [x for x in data if x % 2 == 0]
    transformed = [x ** 2 for x in filtered]
    result = transformed[:10]
    return result


def pipeline_generator(data_size):
    """제너레이터 기반 파이프라인 - 필요한 만큼만 처리"""
    data = (i for i in range(data_size))
    filtered = (x for x in data if x % 2 == 0)
    transformed = (x ** 2 for x in filtered)
    result = []
    for i, val in enumerate(transformed):
        if i >= 10:
            break
        result.append(val)
    return result
```

리스트 파이프라인은 각 단계에서 전체 데이터의 리스트를 만듭니다. 500만 개의 데이터를 처리하면 세 개의 중간 리스트가 메모리를 차지합니다. 반면 제너레이터 파이프라인은 필요한 10개의 결과만 생성하고 나머지는 계산하지 않습니다.

**실행:**

```bash
$ python examples/python/chapter05/ex22_06_generator_usage.py
```

**결과:**

```
============================================================
  제너레이터를 활용한 메모리 효율적 데이터 처리
============================================================

[ 테스트 1: 메모리 사용량 비교 ]
--------------------------------------------------
  1,000,000개의 제곱수:
    리스트 메모리:        8,448,728 bytes (8.1 MB)
    제너레이터 메모리:          208 bytes
    메모리 절약:       40,619배 적은 메모리 사용

[ 테스트 2: 데이터 파이프라인 성능 비교 ]
--------------------------------------------------

  데이터 크기:    100,000개 (상위 10개만 필요)
    리스트 방식:     0.0102초  결과: [0, 4, 16, 36, 64]...
    제너레이터 방식: 0.0000초  결과: [0, 4, 16, 36, 64]...
    속도 향상:       327.1배

  데이터 크기:  1,000,000개 (상위 10개만 필요)
    리스트 방식:     0.1266초
    제너레이터 방식: 0.0000초
    속도 향상:       2,775배

  데이터 크기:  5,000,000개 (상위 10개만 필요)
    리스트 방식:     0.7192초
    제너레이터 방식: 0.0000초
    속도 향상:       23,941배
```

500만 개의 데이터에서 상위 10개만 필요한 상황에서, 제너레이터는 리스트 방식보다 **약 24,000배** 빠릅니다. 리스트 방식은 500만 개를 모두 처리하지만, 제너레이터는 필요한 10개만 계산하고 멈추기 때문입니다.

### 제너레이터 체이닝

제너레이터의 강력한 기능 중 하나는 **체이닝(chaining)**입니다. 여러 처리 단계를 연결하되, 실제 계산은 최종 소비 시점에만 발생합니다.

```python
def to_upper(source):
    for line in source:
        yield line.upper()

def filter_errors(source):
    for line in source:
        if "ERROR" in line:
            yield line

# 제너레이터 체이닝
upper_stream = to_upper(log_lines)
error_stream = filter_errors(upper_stream)
error_count = sum(1 for _ in error_stream)
```

이 패턴은 대용량 로그 파일 처리, 스트리밍 데이터 분석 등에서 매우 유용합니다.

> **Note:** 제너레이터는 **한 번만 소비**할 수 있습니다. 같은 데이터를 여러 번 순회해야 한다면 리스트를 사용하세요. "한 번 순회하면서 처리하고 끝"인 경우에 제너레이터가 적합합니다.

### 제너레이터가 유용한 상황

| 상황 | 이유 |
|------|------|
| 대용량 파일 처리 | 파일 전체를 메모리에 올릴 필요 없음 |
| 무한 시퀀스 생성 | 필요한 만큼만 값을 생성 |
| 데이터 파이프라인 | 중간 결과를 저장하지 않음 |
| 일부만 필요한 경우 | 불필요한 계산을 생략 |
| 스트리밍 처리 | 실시간 데이터를 즉시 처리 |

---

## 22.8 캐싱으로 반복 계산 제거

**캐싱(caching)**은 한 번 계산한 결과를 저장해두고, 같은 입력이 다시 들어오면 저장된 결과를 재사용하는 기법입니다. 이를 **메모이제이션(memoization)**이라고도 합니다.

Python에서는 `functools.lru_cache` 데코레이터로 매우 쉽게 캐싱을 적용할 수 있습니다.

### lru_cache 기본 사용법

```python
import functools

@functools.lru_cache(maxsize=None)
def expensive_function(x):
    """비용이 큰 계산"""
    # ... 시간이 오래 걸리는 계산 ...
    return result
```

`@lru_cache`를 함수 위에 붙이기만 하면 됩니다. 이 함수가 동일한 인자로 호출되면 실제 계산 없이 캐시된 결과를 즉시 반환합니다.

### 예제 22-7: 피보나치 수열로 보는 캐싱의 위력

캐싱의 효과를 가장 극적으로 보여주는 예제는 피보나치 수열입니다.

```python
# examples/python/chapter05/ex22_07_caching.py
import functools


def fibonacci_naive(n):
    """캐싱 없는 피보나치 (지수적 시간 복잡도: O(2^n))"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fibonacci_cached(n):
    """lru_cache 적용 피보나치 (선형 시간 복잡도: O(n))"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)
```

캐싱 없는 피보나치는 같은 값을 반복적으로 계산합니다. 예를 들어 `fibonacci_naive(5)`를 구할 때 `fibonacci_naive(2)`가 **3번** 호출됩니다. `fibonacci_naive(35)`를 구할 때는 내부적으로 **약 3천만 번**의 재귀 호출이 발생합니다.

`@lru_cache`를 적용하면 각 값을 **딱 한 번만** 계산하고 나머지는 캐시에서 가져옵니다.

**실행:**

```bash
$ python examples/python/chapter05/ex22_07_caching.py
```

**결과:**

```
============================================================
  functools.lru_cache를 활용한 캐싱 최적화
============================================================

[ 테스트 1: 피보나치 수열 - 캐싱 효과 ]
-------------------------------------------------------

  캐싱 없는 피보나치 (O(2^n)):
    F(20) =        6,765  소요: 0.0008초
    F(25) =       75,025  소요: 0.0092초
    F(30) =      832,040  소요: 0.1082초
    F(35) =    9,227,465  소요: 1.1324초

  lru_cache 피보나치 (O(n)):
    F( 20) =                                    6,765  소요: 0.000021초
    F( 25) =                                   75,025  소요: 0.000003초
    F( 30) =                                  832,040  소요: 0.000001초
    F( 35) =                                9,227,465  소요: 0.000001초
    F(100) = 354224848179261915075...(21자리)  소요: 0.000019초
    F(200) = 280571172992510140037611932413...(42자리)  소요: 0.000032초
    F(500) = 139423224561697880139724382870...(105자리)  소요: 0.000683초

  캐시 통계:
    적중(hits):    504회
    미스(misses):  501회
    적중률:        50.1%
```

캐싱 없는 버전은 F(35)를 구하는 데 **1.13초**가 걸렸지만, 캐싱 적용 버전은 **0.000001초**(1마이크로초)만에 같은 결과를 냅니다. 게다가 캐싱 버전은 F(500)처럼 캐싱 없이는 사실상 계산 불가능한 큰 수도 순식간에 계산합니다.

### lru_cache의 주요 옵션

| 매개변수 | 설명 | 권장값 |
|---------|------|--------|
| `maxsize=None` | 무제한 캐시 | 메모리가 충분할 때 |
| `maxsize=128` | 최근 128개 저장 | 일반적인 경우 (기본값) |
| `maxsize=4` | 최근 4개만 저장 | 메모리가 제한적일 때 |

`maxsize`가 작으면 오래된 항목이 제거(LRU: Least Recently Used)되어 이전에 캐싱된 값도 다시 계산해야 할 수 있습니다.

### 캐시 상태 모니터링

```python
# 캐시 통계 확인
info = fibonacci_cached.cache_info()
print(f"적중: {info.hits}, 미스: {info.misses}")
print(f"적중률: {info.hits / (info.hits + info.misses) * 100:.1f}%")

# 캐시 초기화
fibonacci_cached.cache_clear()
```

> **Tip:** `cache_info()`로 적중률을 확인하세요. 적중률이 낮다면 캐싱의 효과가 적은 것이므로 다른 최적화 방법을 고려해야 합니다. 적중률이 50% 이상이면 캐싱의 효과가 있다고 볼 수 있습니다.

### 캐싱이 효과적인 상황

1. **같은 인자로 반복 호출**되는 함수 (피보나치, 팩토리얼 등)
2. **계산 비용이 큰** 함수 (복잡한 수학 연산, API 호출 등)
3. **입력의 종류가 제한적**인 경우 (가능한 입력이 적을수록 캐시 효율이 높음)

> **Warning:** `@lru_cache`는 인자가 **해시 가능(hashable)**해야 합니다. 리스트, 딕셔너리 등 변경 가능한(mutable) 객체는 인자로 사용할 수 없습니다. 이 경우 리스트를 튜플로 변환하거나, 수동으로 딕셔너리 캐시를 구현해야 합니다.

---

## 22.9 AI에게 최적화 요청하기

바이브 코딩에서 AI 어시스턴트는 성능 최적화의 강력한 도우미입니다. 하지만 "이 코드 빠르게 만들어줘"라는 막연한 요청보다는, 측정 데이터와 함께 **구체적으로 요청**하는 것이 훨씬 효과적입니다.

### 효과적인 최적화 요청 프롬프트

```
[역할]   당신은 Python 성능 최적화 전문가입니다.
[맥락]   아래 코드는 학생 10,000명의 성적 데이터를 처리합니다.
         현재 2초 이상 걸리며, 0.1초 이내로 줄여야 합니다.
[요청]   다음 코드의 성능 병목을 분석하고 최적화해주세요.
[제약]   결과의 정확성은 반드시 유지해야 합니다.
         사용 가능한 라이브러리: 표준 라이브러리만.
```

### 예제 22-8: 실습 - 느린 코드 최적화 (Before vs After)

실제 업무에서 흔히 발생하는 성능 문제를 가진 코드를 분석하고 최적화하는 전체 과정을 봅니다. 시나리오는 **학생 성적 데이터 처리 프로그램**입니다.

#### Before: 최적화 전 (느린 코드)

```python
# examples/python/chapter05/ex22_08_optimize_slow_code.py

# --- 최적화 전: 문제가 있는 코드 ---

def slow_get_average(student):
    """느린 평균 계산: 매번 과목 목록을 순회"""
    total = 0
    count = 0
    for subject in student["scores"]:
        total = total + student["scores"][subject]
        count = count + 1
    return total / count


def slow_find_top_students(students, n=10):
    """느린 상위 학생 찾기: 매번 전체를 정렬"""
    # 문제 1: 매 호출마다 평균을 다시 계산
    # 문제 2: 전체를 정렬한 후 상위 n개만 사용
    sorted_students = sorted(
        students,
        key=lambda s: slow_get_average(s),
        reverse=True,
    )
    return sorted_students[:n]


def slow_class_statistics(students):
    """느린 반별 통계: 비효율적인 반복"""
    classes = []
    # 문제 1: 반 목록을 비효율적으로 추출
    for s in students:
        if s["class"] not in classes:
            classes.append(s["class"])

    result = {}
    for cls in classes:
        # 문제 2: 매 반마다 전체 학생을 순회
        class_students = []
        for s in students:
            if s["class"] == cls:
                class_students.append(s)

        # 문제 3: 평균을 매번 다시 계산
        averages = []
        for s in class_students:
            avg = slow_get_average(s)
            averages.append(avg)

        # 문제 4: 수동으로 합계/최대/최소 계산
        total = 0
        for a in averages:
            total += a
        class_avg = total / len(averages)

        max_avg = averages[0]
        for a in averages:
            if a > max_avg:
                max_avg = a

        result[cls] = {"학생수": len(class_students), "평균": class_avg, "최고": max_avg}

    return result


def slow_find_failing_students(students, threshold=50):
    """느린 과락 학생 찾기: 중첩 반복"""
    failing = []
    for student in students:
        for subject, score in student["scores"].items():
            if score < threshold:
                # 문제: 이미 추가된 학생인지 비효율적으로 확인
                already_added = False
                for f in failing:
                    if f["id"] == student["id"]:
                        already_added = True
                        break
                if not already_added:
                    failing.append(student)
    return failing
```

이 코드에는 다섯 가지 주요 성능 문제가 있습니다:

1. **반복 계산**: 같은 학생의 평균을 여러 함수에서 반복적으로 계산
2. **비효율적 자료구조**: 리스트에서 선형 탐색으로 중복 확인 (`O(n)`)
3. **불필요한 순회**: 반 목록 추출, 반별 필터링에 전체 학생을 매번 순회
4. **수동 반복문**: `sum()`, `max()`, `min()` 같은 내장 함수 미사용
5. **비효율적 조기 종료 없음**: 과락 판정 시 모든 과목을 확인

#### After: 최적화 후 (빠른 코드)

```python
def fast_get_average(scores):
    """빠른 평균 계산: 내장 함수 활용"""
    return sum(scores.values()) / len(scores)


def fast_find_top_students(students_with_avg, n=10):
    """빠른 상위 학생 찾기: 미리 계산된 평균 사용"""
    sorted_students = sorted(
        students_with_avg,
        key=lambda s: s["average"],
        reverse=True,
    )
    return sorted_students[:n]


def fast_class_statistics(students_with_avg):
    """빠른 반별 통계: 한 번의 순회로 그룹핑"""
    class_groups = {}
    for s in students_with_avg:
        cls = s["class"]
        if cls not in class_groups:
            class_groups[cls] = []
        class_groups[cls].append(s["average"])

    result = {}
    for cls, averages in class_groups.items():
        result[cls] = {
            "학생수": len(averages),
            "평균": sum(averages) / len(averages),
            "최고": max(averages),
            "최저": min(averages),
        }
    return result


def fast_find_failing_students(students, threshold=50):
    """빠른 과락 학생 찾기: set + any() 활용"""
    failing = []
    seen_ids = set()
    for student in students:
        if student["id"] not in seen_ids:
            if any(score < threshold for score in student["scores"].values()):
                failing.append(student)
                seen_ids.add(student["id"])
    return failing


def fast_full_pipeline(students):
    """빠른 전체 파이프라인: 평균을 한 번만 계산"""
    # 핵심 최적화: 평균을 한 번만 계산하여 재사용
    students_with_avg = []
    for s in students:
        s_copy = s.copy()
        s_copy["average"] = fast_get_average(s["scores"])
        students_with_avg.append(s_copy)

    top = fast_find_top_students(students_with_avg, 10)
    stats = fast_class_statistics(students_with_avg)
    failing = fast_find_failing_students(students)
    return top, stats, failing
```

**실행:**

```bash
$ python examples/python/chapter05/ex22_08_optimize_slow_code.py
```

**결과:**

```
=================================================================
  실습: 느린 코드 최적화 (Before vs After)
=================================================================

=================================================================
  학생 수: 1,000명
=================================================================

  [ 실행 시간 비교 ]
        최적화 전: 0.0173초
        최적화 후: 0.0012초
        속도 향상: 14.3배

  [ 결과 정확성 검증 ]
    상위 학생 일치: 예
    반별 통계 일치: 예
    과락 학생 수:   느린 코드=808, 빠른 코드=808 (일치)

=================================================================
  학생 수: 5,000명
=================================================================

  [ 실행 시간 비교 ]
        최적화 전: 0.4289초
        최적화 후: 0.0085초
        속도 향상: 50.4배

=================================================================
  학생 수: 10,000명
=================================================================

  [ 실행 시간 비교 ]
        최적화 전: 2.0755초
        최적화 후: 0.0185초
        속도 향상: 112.3배

  [ 결과 정확성 검증 ]
    상위 학생 일치: 예
    반별 통계 일치: 예
    과락 학생 수:   느린 코드=8,122, 빠른 코드=8,122 (일치)
```

학생 10,000명 기준으로 **112배**의 성능 향상을 달성했습니다. 그리고 모든 결과가 정확히 일치합니다. 최적화가 정확성을 해치지 않는다는 것을 검증하는 것이 매우 중요합니다.

### 최적화 포인트 정리

이 예제에서 적용한 최적화 기법을 정리하면 다음과 같습니다.

| 번호 | 최적화 포인트 | Before | After | 효과 |
|------|-------------|--------|-------|------|
| 1 | 반복 계산 제거 | 평균을 매번 다시 계산 | 한 번 계산하여 재사용 | 가장 큰 효과 |
| 2 | 적절한 자료구조 | 리스트 선형 탐색 O(n) | set 상수 시간 O(1) | 대용량에서 극적 |
| 3 | 불필요한 순회 제거 | 반 목록 추출 + 반별 필터 각각 순회 | 한 번의 순회로 그룹핑 | 순회 횟수 감소 |
| 4 | 내장 함수 활용 | 수동 for 루프 | sum(), max(), min() | 코드 간결 + 빠름 |
| 5 | 조기 종료 | 모든 과목 확인 | any()로 첫 발견 시 종료 | 불필요한 비교 제거 |

> **Tip:** AI에게 최적화를 요청할 때는 이런 프롬프트가 효과적입니다:
> "이 코드를 최적화해줘. 현재 10,000건 데이터에서 2초 걸리는데, 0.1초 이내로 줄이고 싶어. **반복 계산 제거**, **적절한 자료구조 선택**, **내장 함수 활용** 관점에서 개선해줘. 최적화 전후의 결과가 동일한지 검증하는 코드도 포함해줘."

---

## 22.10 최적화 체크리스트

코드의 성능을 개선할 때 다음 체크리스트를 순서대로 확인하세요. 위에서부터 아래로 갈수록 영향력이 작아지지만, 모두 알아두면 유용합니다.

### 1단계: 알고리즘 개선 (가장 큰 효과)

- [ ] O(n^2)을 O(n) 또는 O(n log n)으로 개선할 수 있는가?
- [ ] 불필요한 중첩 반복문이 있는가?
- [ ] 같은 계산을 반복하고 있는가?

### 2단계: 자료구조 선택

- [ ] 검색이 빈번하면 리스트 대신 set 또는 dict를 사용하는가?
- [ ] 키-값 매핑이 필요하면 dict를 사용하는가?
- [ ] 순서가 불필요한 데이터는 set으로 관리하는가?

### 3단계: Python 기법 활용

- [ ] 리스트 컴프리헨션을 사용하는가?
- [ ] 내장 함수(sum, max, min, any, all)를 활용하는가?
- [ ] 대용량 데이터는 제너레이터를 사용하는가?
- [ ] 반복 호출 함수에 @lru_cache를 적용했는가?

### 4단계: 측정과 검증

- [ ] 최적화 전후의 성능을 측정했는가?
- [ ] 최적화 후 결과의 정확성을 검증했는가?
- [ ] 프로파일링으로 진짜 병목을 찾았는가?

---

## 정리

이 장에서 배운 성능 최적화의 핵심 내용을 정리합니다.

### 핵심 개념

| 개념 | 설명 | 핵심 도구/기법 |
|------|------|-------------|
| 시간 측정 | 코드 실행 시간을 정확히 측정 | `time.perf_counter()` |
| 벤치마크 | 반복 측정으로 신뢰성 있는 성능 데이터 확보 | `timeit.repeat()` |
| 프로파일링 | 함수별 시간 소비 분석, 병목 찾기 | `cProfile`, `pstats` |
| 빅오 표기법 | 알고리즘 효율성 평가 | O(1), O(n), O(n^2) |
| 자료구조 선택 | 적합한 자료구조로 성능 향상 | `set`, `dict` |
| 제너레이터 | 메모리 효율적 데이터 처리 | `yield`, 제너레이터 표현식 |
| 캐싱 | 반복 계산 결과 재사용 | `@lru_cache` |

### 최적화 순서

최적화는 다음 순서로 접근하세요:

```
1. 측정한다 (Measure)        -- "감"이 아니라 "데이터"로 판단
2. 병목을 찾는다 (Profile)    -- 프로파일링으로 진짜 원인 파악
3. 알고리즘을 개선한다        -- 가장 큰 효과
4. 자료구조를 바꾼다          -- set/dict 활용
5. Python 기법을 적용한다     -- 컴프리헨션, 내장 함수, 캐싱
6. 검증한다 (Verify)         -- 정확성과 성능 모두 확인
```

### 이 장에서 다룬 예제

| 예제 | 파일명 | 핵심 교훈 |
|------|--------|----------|
| 예제 22-1 | `ex22_01_time_measure.py` | time.time()과 perf_counter()로 시간 측정 |
| 예제 22-2 | `ex22_02_timeit_usage.py` | timeit으로 정밀 벤치마크 수행 |
| 예제 22-3 | `ex22_03_profiling.py` | cProfile로 병목 지점 찾기 |
| 예제 22-4 | `ex22_04_big_o_improvement.py` | O(n^2) --> O(n) 알고리즘 개선 |
| 예제 22-5 | `ex22_05_list_vs_set.py` | 리스트 vs 집합 검색 성능 비교 |
| 예제 22-6 | `ex22_06_generator_usage.py` | 제너레이터로 메모리 최적화 |
| 예제 22-7 | `ex22_07_caching.py` | lru_cache로 반복 계산 제거 |
| 예제 22-8 | `ex22_08_optimize_slow_code.py` | 종합 실습: Before/After 최적화 |

### AI에게 최적화를 요청하는 팁

AI 어시스턴트에게 성능 최적화를 요청할 때 다음 정보를 포함하세요:

1. **현재 성능 데이터**: "10,000건 처리에 2초 걸립니다"
2. **목표 성능**: "0.1초 이내로 줄이고 싶습니다"
3. **제약 조건**: "표준 라이브러리만 사용", "메모리 1GB 이내"
4. **정확성 요구**: "결과가 동일해야 합니다"
5. **프로파일링 결과**: "read_data()에서 전체 시간의 40%를 소비합니다"

> **Tip:** "빠르게 해줘"보다는 "프로파일링 결과 read_data()가 병목입니다. 이 함수를 리스트 컴프리헨션과 제너레이터를 활용하여 최적화해주세요."처럼 **측정 데이터 + 구체적 기법**을 함께 요청하면 AI가 훨씬 정확하고 효과적인 최적화 코드를 생성합니다.

---

## 연습 문제

### 연습 1: 시간 측정 실습

다음 두 함수의 실행 시간을 `time.perf_counter()`로 측정하고 비교하세요.

```python
# 방법 1: 문자열 포맷팅으로 숫자 리스트를 문자열로 변환
def format_with_loop(numbers):
    result = ""
    for n in numbers:
        result += str(n) + ", "
    return result[:-2]

# 방법 2: join 사용
def format_with_join(numbers):
    return ", ".join(str(n) for n in numbers)

numbers = list(range(100000))
# 두 함수의 실행 시간을 측정하고, 어느 쪽이 얼마나 빠른지 출력하세요.
```

### 연습 2: 자료구조 최적화

다음 코드는 두 리스트의 공통 원소를 찾습니다. `set`을 사용하여 최적화하세요.

```python
def find_common_slow(list1, list2):
    """O(n*m) 방식"""
    common = []
    for item in list1:
        if item in list2 and item not in common:
            common.append(item)
    return common

# set을 사용한 빠른 버전을 작성하세요.
# def find_common_fast(list1, list2):
#     ...
```

### 연습 3: 캐싱 적용

팩토리얼 함수에 `@lru_cache`를 적용하고, 캐싱 전후의 성능을 비교하세요.

```python
# 캐싱 없는 버전
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# @lru_cache를 적용한 버전을 작성하고,
# factorial(100)을 1000번 호출할 때의 시간을 비교하세요.
```

### 연습 4: AI에게 최적화 요청하기

다음 느린 코드를 AI 어시스턴트에게 최적화 요청하는 프롬프트를 작성해보세요. 이 장에서 배운 RCRF 구조와 측정 데이터를 포함하여 구체적으로 작성하세요.

```python
def count_word_frequency(text):
    """텍스트에서 단어 빈도를 계산 (비효율적 버전)"""
    words = text.split()
    frequency = []  # [(단어, 횟수)] 리스트
    for word in words:
        found = False
        for i, (w, count) in enumerate(frequency):
            if w == word:
                frequency[i] = (w, count + 1)
                found = True
                break
        if not found:
            frequency.append((word, 1))
    # 빈도순 정렬
    for i in range(len(frequency)):
        for j in range(i + 1, len(frequency)):
            if frequency[j][1] > frequency[i][1]:
                frequency[i], frequency[j] = frequency[j], frequency[i]
    return frequency
```

**힌트**: 이 코드에는 최소 세 가지 성능 문제가 있습니다. 어떤 자료구조와 내장 함수를 사용하면 개선할 수 있을까요?

---

## 다음 장 예고

다음 장 **"Chapter 23: 보안 기초"**에서는 안전한 코드를 작성하는 방법을 배웁니다. 입력 검증, SQL 인젝션 방어, 커맨드 인젝션 방지, 비밀 정보 관리 등 실제 개발에서 반드시 알아야 할 보안 기초를 실습합니다. 성능이 좋은 코드도 보안에 취약하면 무용지물이라는 점을 기억하세요.

- 입력 검증과 위생 처리
- SQL 인젝션과 커맨드 인젝션 방어
- 경로 탐색(Path Traversal) 방지
- 환경 변수와 .env 파일로 비밀 정보 관리
- AI에게 보안 코드 리뷰 요청하기
