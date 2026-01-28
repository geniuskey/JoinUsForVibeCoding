# Chapter 27: 프로젝트 3 - 데이터 대시보드 CLI

데이터는 현대 비즈니스의 핵심 자산입니다. 수많은 데이터를 수집하고, 정제하고, 분석하여 의미 있는 인사이트를 도출하는 능력은 개발자에게 매우 중요한 역량입니다. 이번 프로젝트에서는 AI 어시스턴트와 함께 **터미널에서 동작하는 데이터 대시보드 CLI**를 단계적으로 만들어봅니다.

외부 라이브러리 없이 Python 표준 라이브러리만으로 CSV 데이터 로드, API 데이터 수집, 데이터 정제, 통계 분석, 그리고 깔끔한 테이블 출력까지 모든 기능을 직접 구현합니다. 바이브 코딩으로 AI와 대화하며 한 단계씩 프로젝트를 완성해나가는 과정을 경험해보세요.

---

## 학습 목표

이 프로젝트를 완성하면 다음을 할 수 있습니다:

- **프로젝트 구조**를 체계적으로 설계하고 자동 생성할 수 있다
- **CSV 파일**에서 데이터를 로드하고 기본 정보를 확인할 수 있다
- **API 데이터 수집** 패턴(캐싱, 재시도)을 구현할 수 있다
- **결측치, 이상치, 중복** 등 데이터 품질 문제를 탐지하고 처리할 수 있다
- 데이터를 **변환**하고 **파생 변수**를 생성할 수 있다
- **기본 통계**(평균, 중앙값, 표준편차, 상관계수)를 계산할 수 있다
- **그룹별 분석**과 **교차 분석**으로 비즈니스 인사이트를 도출할 수 있다
- 표준 라이브러리만으로 **깔끔한 테이블**을 터미널에 출력할 수 있다
- AI와 반복적으로 대화하며 프로젝트를 **점진적으로 완성**할 수 있다

---

## 27.1 프로젝트 개요

### 무엇을 만드는가?

이번 프로젝트에서 만드는 **데이터 대시보드 CLI**는 터미널에서 실행되는 데이터 분석 도구입니다. 판매 데이터를 수집하고, 정제하고, 분석하여 한눈에 볼 수 있는 보고서를 출력합니다.

```
[데이터 수집] --> [데이터 정제] --> [데이터 변환] --> [통계 분석] --> [테이블 출력]
   (CSV/API)     (결측치/이상치)   (파생변수/집계)   (평균/분포)    (대시보드)
```

### 프로젝트 요구사항

| 항목 | 설명 |
|------|------|
| **데이터 수집** | CSV 파일 로드 + API 데이터 수집 (시뮬레이션) |
| **데이터 정제** | 결측치, 이상치, 중복, 형식 오류 처리 |
| **데이터 변환** | 파생 변수 생성, 집계, 피벗 테이블 |
| **통계 분석** | 기본 통계, 백분위수, 상관관계, 그룹별 분석 |
| **CLI 출력** | 깔끔한 테이블 형식으로 터미널 출력 |
| **기술 제약** | Python 표준 라이브러리만 사용 (pandas, rich 사용 안 함) |

### 왜 표준 라이브러리만 사용하는가?

실무에서는 pandas, rich 같은 강력한 라이브러리를 사용합니다. 하지만 이 프로젝트에서는 의도적으로 표준 라이브러리만 사용합니다. 이유는 다음과 같습니다:

1. **기초 원리 이해**: 라이브러리가 내부에서 어떻게 동작하는지 직접 구현하며 이해합니다
2. **문제 해결 능력**: 라이브러리 없이도 문제를 해결하는 능력을 기릅니다
3. **바이브 코딩 실습**: AI에게 구체적으로 요청하여 원하는 코드를 얻는 연습을 합니다

> **Tip:** 프로젝트를 완성한 후에 pandas와 rich를 적용해보면, 표준 라이브러리로 구현한 내용이 이 라이브러리들을 이해하는 데 큰 도움이 됩니다.

---

## 27.2 개발 전략

이번 프로젝트는 5단계로 나누어 진행합니다. 각 단계마다 AI에게 구체적인 프롬프트를 작성하고, 결과를 확인한 뒤 다음 단계로 넘어갑니다.

```
Step 1: 프로젝트 구조 설정
  └─> Step 2: 데이터 수집
       └─> Step 3: 데이터 처리 (정제 + 변환)
            └─> Step 4: 통계 계산
                 └─> Step 5: CLI 출력 (테이블)
```

| 단계 | 내용 | 관련 예제 |
|------|------|----------|
| Step 1 | 프로젝트 구조 설정 | ex27_01, ex27_02 |
| Step 2 | 데이터 수집 | ex27_03, ex27_04 |
| Step 3 | 데이터 처리 | ex27_05, ex27_06 |
| Step 4 | 통계 계산 | ex27_07, ex27_08 |
| Step 5 | CLI 출력 | ex27_09 |

각 단계에서 AI에게 어떻게 프롬프트를 작성하는지, 결과를 어떻게 검증하는지 함께 살펴봅시다.

---

## 27.3 Step 1: 프로젝트 구조 설정

모든 좋은 프로젝트는 체계적인 구조에서 시작됩니다. 첫 번째 단계에서는 프로젝트 디렉토리를 자동으로 생성하고, 분석에 사용할 샘플 데이터를 만듭니다.

### AI에게 프롬프트 작성하기

프로젝트 구조를 만들기 위해 AI에게 다음과 같이 요청합니다:

```
프롬프트:
"데이터 대시보드 CLI 프로젝트를 위한 디렉토리 구조를 자동으로 생성하는
Python 스크립트를 작성해줘.

요구사항:
- data/ 아래에 raw, processed, cache 폴더
- collectors, processors, analyzers, visualizers 모듈 폴더
- config, tests, reports 폴더
- 각 모듈 폴더에 __init__.py 생성
- config/settings.py에 기본 설정 포함
- 최종 프로젝트 트리를 출력
- os 모듈만 사용하고 외부 라이브러리 사용 금지"
```

### 예제 27-01: 프로젝트 디렉토리 구조 생성

AI가 작성해준 코드는 `create_project_structure()` 함수로 전체 디렉토리와 초기 파일을 자동 생성합니다. 핵심 부분을 살펴봅시다.

**예제 27-01: 디렉토리 구조 자동 생성**

```python
# examples/python/chapter06/ex27_01_directory_structure.py

import os
import datetime


def create_project_structure(base_dir):
    """데이터 대시보드 프로젝트의 디렉토리 구조를 생성합니다."""

    # 프로젝트 디렉토리 구조 정의
    directories = [
        "data/raw",          # 원본 데이터 저장
        "data/processed",    # 정제된 데이터 저장
        "data/cache",        # API 캐시 데이터
        "collectors",        # 데이터 수집 모듈
        "processors",        # 데이터 처리 모듈
        "analyzers",         # 데이터 분석 모듈
        "visualizers",       # 시각화 모듈
        "reports",           # 보고서 출력 디렉토리
        "config",            # 설정 파일
        "tests",             # 테스트 코드
    ]

    # 초기 파일 정의 (파일 경로: 파일 내용)
    initial_files = {
        "config/settings.py": '''"""대시보드 설정 파일"""

DATA_DIR = "data"
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CACHE_DIR = "data/cache"
REPORT_DIR = "reports"
CHART_WIDTH = 50
CHART_FILL_CHAR = "\u2588"
''',
        "collectors/__init__.py": '"""데이터 수집 모듈"""\n',
        "processors/__init__.py": '"""데이터 처리 모듈"""\n',
        "analyzers/__init__.py": '"""데이터 분석 모듈"""\n',
        "visualizers/__init__.py": '"""시각화 모듈"""\n',
        "tests/__init__.py": '"""테스트 모듈"""\n',
        "dashboard.py": '''"""데이터 대시보드 CLI 메인 모듈"""
import sys

def main():
    print("=" * 50)
    print("  데이터 대시보드 CLI v1.0")
    print("=" * 50)

if __name__ == "__main__":
    main()
''',
    }

    # 디렉토리 생성
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"  [생성] {directory}/")

    # 파일 생성
    for file_path, content in initial_files.items():
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [생성] {file_path}")
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_01_directory_structure.py
```

**결과:**

```
============================================================
  데이터 대시보드 프로젝트 구조 생성기
============================================================

프로젝트 경로: /tmp/dashboard-cli

디렉토리 생성 중...
  [생성] data/raw/
  [생성] data/processed/
  [생성] data/cache/
  [생성] collectors/
  [생성] processors/
  [생성] analyzers/
  [생성] visualizers/
  [생성] reports/
  [생성] config/
  [생성] tests/

초기 파일 생성 중...
  [생성] config/settings.py
  [생성] collectors/__init__.py
  [생성] processors/__init__.py
  [생성] analyzers/__init__.py
  [생성] visualizers/__init__.py
  [생성] tests/__init__.py
  [생성] README.md
  [생성] dashboard.py

------------------------------------------------------------
생성 완료!
  - 디렉토리: 10개 새로 생성
  - 파일: 8개 새로 생성

최종 프로젝트 구조:
├── README.md
├── analyzers/
│   └── __init__.py
├── collectors/
│   └── __init__.py
├── config/
│   └── settings.py
├── dashboard.py
├── data/
│   ├── cache/
│   ├── processed/
│   └── raw/
├── processors/
│   └── __init__.py
├── reports/
├── tests/
│   └── __init__.py
└── visualizers/
    └── __init__.py
```

이 코드의 핵심 포인트를 정리합니다:

- **`os.makedirs()`**: 중간 경로까지 한 번에 생성합니다 (`data/raw` 입력 시 `data`도 함께 생성)
- **`os.path.exists()`**: 이미 존재하는 파일/폴더를 덮어쓰지 않도록 체크합니다
- **트리 출력**: 재귀 함수로 디렉토리 구조를 시각적으로 보여줍니다

> **Note:** 프로젝트 구조를 코드로 자동 생성하면, 팀원 누구나 동일한 환경을 빠르게 구축할 수 있습니다. 이것은 실무에서도 자주 사용하는 패턴입니다.

### 예제 27-02: 샘플 데이터 생성

분석에 사용할 현실적인 판매 데이터가 필요합니다. AI에게 다음과 같이 요청합니다:

```
프롬프트:
"대시보드에서 분석할 현실적인 판매 데이터를 CSV로 생성해줘.

요구사항:
- 200건의 판매 데이터 (날짜, 상품명, 카테고리, 수량, 단가, 총액, 지역, 고객등급)
- random 시드 고정으로 재현 가능하게
- 한국 실정에 맞는 상품/가격/지역
- 데이터 정제 연습용으로 결측치, 이상치, 잘못된 날짜가 포함된 불량 버전도 생성
- csv 모듈 사용"
```

**예제 27-02: 샘플 판매 데이터 생성**

```python
# examples/python/chapter06/ex27_02_sample_data.py

import csv
import os
import random
import datetime


def generate_sales_data(num_records=200, seed=42):
    """현실적인 판매 데이터를 생성합니다."""

    random.seed(seed)

    # 상품 정보 (상품명, 카테고리, 가격 범위)
    products = [
        ("무선 키보드", "전자기기", 25000, 65000),
        ("블루투스 마우스", "전자기기", 15000, 45000),
        ("USB 허브", "전자기기", 12000, 35000),
        ("모니터 거치대", "사무용품", 20000, 55000),
        ("노트북 파우치", "액세서리", 15000, 40000),
        ("웹캠", "전자기기", 30000, 80000),
        ("마우스패드", "액세서리", 5000, 25000),
        ("헤드셋", "전자기기", 25000, 120000),
    ]

    regions = ["서울", "경기", "부산", "대구", "인천", "광주", "대전", "울산", "세종"]
    customer_grades = ["일반", "실버", "골드", "VIP"]

    records = []
    for i in range(num_records):
        product_name, category, min_price, max_price = random.choice(products)
        unit_price = round(random.randint(min_price, max_price) / 100) * 100
        quantity = random.choices(
            range(1, 21),
            weights=[30, 25, 15, 10, 8] + [1] * 15,
            k=1
        )[0]
        grade = random.choices(customer_grades, weights=[40, 30, 20, 10], k=1)[0]
        discount = {"일반": 0, "실버": 0.05, "골드": 0.10, "VIP": 0.15}[grade]
        total = int(unit_price * quantity * (1 - discount))

        records.append({
            "주문번호": f"ORD-{i+1:04d}",
            "날짜": (datetime.date(2025, 1, 1) +
                    datetime.timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d"),
            "상품명": product_name,
            "카테고리": category,
            "수량": quantity,
            "단가": unit_price,
            "총액": total,
            "지역": random.choice(regions),
            "고객등급": grade,
        })

    records.sort(key=lambda x: x["날짜"])
    return records
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_02_sample_data.py
```

**결과:**

```
============================================================
  판매 샘플 데이터 생성기
============================================================

[1단계] 정상 판매 데이터 생성 중...
파일 저장 완료: /tmp/dashboard-data/sales_clean.csv
  - 레코드 수: 200개
  - 파일 크기: 16,374 바이트

[2단계] 불량 데이터 포함 버전 생성 중...
파일 저장 완료: /tmp/dashboard-data/sales_raw.csv
  - 레코드 수: 200개
  - 파일 크기: 16,366 바이트

------------------------------------------------------------
데이터 미리보기 (처음 5건):
------------------------------------------------------------
    주문번호 |       날짜 |      상품명 |       수량 |       단가 |       총액 |       지역
--------------------------------------------------------------------------
ORD-0082 | 2025-01-01 |  노트북 파우치 |        1 |   24,400 |   23,180 |       광주
ORD-0156 | 2025-01-01 |  노트북 스탠드 |        3 |   46,500 |  139,500 |       대전
ORD-0005 | 2025-01-02 |   보조 배터리 |        1 |   41,400 |   41,400 |       대전
ORD-0131 | 2025-01-04 |   충전 케이블 |        1 |   13,800 |   11,730 |       서울
ORD-0133 | 2025-01-04 |   책상 정리함 |        2 |   19,300 |   38,600 |       울산

------------------------------------------------------------
데이터 요약:
------------------------------------------------------------
  총 주문 건수: 200건
  총 판매액: 25,419,630원
  총 판매 수량: 815개
  평균 주문액: 127,098원
  카테고리 수: 3개 (사무용품, 액세서리, 전자기기)
  지역 수: 9개
  기간: 2025-01-01 ~ 2025-06-30
```

이 코드에서 주목할 점은 다음과 같습니다:

- **`random.seed(42)`**: 시드를 고정하면 매번 같은 데이터가 생성되어 결과를 재현할 수 있습니다
- **`random.choices()`**: 가중치를 적용한 랜덤 선택으로 현실적인 분포를 만듭니다
- **`add_dirty_data()`**: 불량 데이터를 의도적으로 섞어 정제 연습용 데이터를 제공합니다

> **Tip:** 실제 프로젝트에서도 개발 초기에는 샘플 데이터로 시작합니다. AI에게 "현실적인 테스트 데이터를 만들어줘"라고 요청하면 개발 속도를 크게 높일 수 있습니다.

### Step 1 점검

이 단계에서 다음을 완성했는지 확인합니다:

- [x] 프로젝트 디렉토리가 체계적으로 생성되었는가?
- [x] 설정 파일과 초기 모듈이 만들어졌는가?
- [x] 정상 데이터와 불량 데이터 CSV가 생성되었는가?
- [x] 데이터 미리보기로 내용을 확인할 수 있는가?

---

## 27.4 Step 2: 데이터 수집

데이터 대시보드의 첫 번째 기능은 다양한 소스에서 데이터를 수집하는 것입니다. CSV 파일에서 직접 로드하는 방법과 API를 통해 수집하는 방법을 구현합니다.

### AI에게 CSV 로더 요청하기

```
프롬프트:
"CSV 파일을 로드하여 데이터를 분석할 수 있는 Python 모듈을 작성해줘.

기능:
1. csv.DictReader로 파일 로드 (딕셔너리 리스트 반환)
2. 데이터 기본 정보 출력 (레코드 수, 컬럼 수, 각 컬럼의 타입/결측치/고유값)
3. 처음/마지막 N개 레코드 미리보기
4. 숫자 컬럼의 기본 통계 (합계, 평균, 최솟값, 최댓값, 중앙값)

표준 라이브러리(csv, os)만 사용. 한국어 CSV(utf-8-sig) 지원."
```

### 예제 27-03: CSV 데이터 로더

CSV 로더는 데이터를 불러오고 기본적인 정보를 확인하는 모듈입니다. 핵심 함수들을 살펴봅시다.

**예제 27-03: CSV 데이터 로드 및 검사**

```python
# examples/python/chapter06/ex27_03_csv_loader.py

import csv
import os


def load_csv(filepath):
    """CSV 파일을 로드하여 딕셔너리 리스트로 반환합니다."""

    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다 - {filepath}")
        return []

    records = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    return records


def inspect_data(records, name="데이터"):
    """데이터의 기본 정보를 출력합니다."""

    if not records:
        print("데이터가 비어 있습니다.")
        return

    print(f"\n총 레코드 수: {len(records):,}개")

    columns = list(records[0].keys())
    print(f"컬럼 수: {len(columns)}개")
    print(f"컬럼 목록: {', '.join(columns)}")

    # 각 컬럼별 정보
    print(f"\n{'컬럼명':>12s} | {'타입':>8s} | {'비어있음':>8s} | {'고유값':>8s} | 샘플값")
    print("-" * 75)

    for col in columns:
        values = [r[col] for r in records]
        non_empty = [v for v in values if v.strip() != ""]
        unique_count = len(set(values))

        # 숫자인지 판별
        numeric = True
        for v in non_empty[:10]:
            try:
                float(v.replace(",", ""))
            except ValueError:
                numeric = False
                break

        dtype = "숫자" if numeric else "문자열"
        empty_count = len(values) - len(non_empty)
        sample = non_empty[0] if non_empty else "(없음)"

        print(f"{col:>12s} | {dtype:>8s} | {empty_count:>8d} | "
              f"{unique_count:>8d} | {sample}")


def get_numeric_summary(records, column):
    """숫자 컬럼의 기본 통계를 출력합니다."""

    values = []
    for r in records:
        try:
            val = float(r[column].replace(",", ""))
            values.append(val)
        except (ValueError, AttributeError):
            continue

    if not values:
        print(f"'{column}' 컬럼에 유효한 숫자 데이터가 없습니다.")
        return

    values.sort()
    total = sum(values)
    mean = total / len(values)

    print(f"\n'{column}' 컬럼 통계:")
    print(f"  유효 데이터: {len(values):,}개")
    print(f"  합계: {total:,.0f}")
    print(f"  평균: {mean:,.0f}")
    print(f"  최솟값: {values[0]:,.0f}")
    print(f"  최댓값: {values[-1]:,.0f}")
    print(f"  중앙값: {values[len(values) // 2]:,.0f}")
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_03_csv_loader.py
```

**결과:**

```
============================================================
  CSV 데이터 로더
============================================================

샘플 CSV 파일 생성 중: /tmp/dashboard-data/sales_demo.csv
파일 크기: 7,365 바이트

CSV 파일 로드 중...
로드 완료: 100개 레코드

============================================================
  판매 데이터 기본 정보
============================================================

총 레코드 수: 100개
컬럼 수: 8개
컬럼 목록: 주문번호, 날짜, 상품명, 카테고리, 수량, 단가, 총액, 지역

         컬럼명 |       타입 |     비어있음 |      고유값 | 샘플값
---------------------------------------------------------------------------
        주문번호 |      문자열 |        0 |      100 | ORD-0001
          날짜 |      문자열 |        0 |       79 | 2025-03-04
         상품명 |      문자열 |        0 |        8 | 블루투스 마우스
        카테고리 |      문자열 |        0 |        3 | 전자기기
          수량 |       숫자 |        0 |       10 | 1
          단가 |       숫자 |        0 |      100 | 24506
          총액 |       숫자 |        0 |      100 | 24506
          지역 |      문자열 |        0 |        5 | 경기

'수량' 컬럼 통계:
  유효 데이터: 100개
  합계: 556
  평균: 6
  최솟값: 1
  최댓값: 10
  중앙값: 5

'단가' 컬럼 통계:
  유효 데이터: 100개
  합계: 2,953,856
  평균: 29,539
  최솟값: 7,488
  최댓값: 58,479
  중앙값: 27,062
```

이 코드의 핵심 개념을 정리합니다:

- **`csv.DictReader`**: 각 행을 딕셔너리로 읽어 컬럼명으로 접근할 수 있습니다
- **`utf-8-sig` 인코딩**: 엑셀에서 저장한 한국어 CSV의 BOM 마크를 자동 처리합니다
- **타입 판별**: 첫 10개 값을 `float()` 변환해보고 성공하면 숫자 컬럼으로 판단합니다

### 예제 27-04: API 데이터 수집

실제 대시보드는 실시간 데이터를 API에서 수집합니다. 네트워크 없이도 학습할 수 있도록 가상 API 서버를 만들어 수집 패턴을 실습합니다.

AI에게 다음과 같이 요청합니다:

```
프롬프트:
"실제 API 호출을 시뮬레이션하는 데이터 수집기를 작성해줘.

요구사항:
- MockAPIServer 클래스: 날씨/환율/주식 데이터를 가상으로 제공
- APICollector 클래스: 캐싱, 에러 처리, 재시도 기능
- JSON 파일로 결과 저장
- 표준 라이브러리만 사용 (json, os, hashlib, time)"
```

**예제 27-04: API 데이터 수집 시뮬레이션**

```python
# examples/python/chapter06/ex27_04_api_collector.py

import json
import os
import hashlib
import time


class APICollector:
    """API 데이터 수집기: 캐싱, 에러 처리, 재시도 기능을 포함합니다."""

    def __init__(self, cache_dir="/tmp/dashboard-data/cache"):
        self.api = MockAPIServer()  # 가상 API 서버
        self.cache_dir = cache_dir
        self.cache_ttl = 300  # 캐시 유효 시간 (초)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, endpoint, params):
        """요청에 대한 캐시 파일 경로를 생성합니다."""
        cache_key = f"{endpoint}_{json.dumps(params or {}, sort_keys=True)}"
        cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{cache_hash}.json")

    def _load_cache(self, cache_path):
        """캐시 파일에서 데이터를 로드합니다."""
        if not os.path.exists(cache_path):
            return None

        file_age = time.time() - os.path.getmtime(cache_path)
        if file_age > self.cache_ttl:
            return None  # 캐시 만료

        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def collect(self, endpoint, params=None, use_cache=True, max_retries=3):
        """API에서 데이터를 수집합니다."""

        # 1. 캐시 확인
        cache_path = self._get_cache_path(endpoint, params)
        if use_cache:
            cached = self._load_cache(cache_path)
            if cached is not None:
                print(f"  [캐시 적중] {endpoint}")
                return cached

        # 2. API 호출 (재시도 포함)
        for attempt in range(1, max_retries + 1):
            try:
                print(f"  [API 호출] {endpoint} (시도 {attempt}/{max_retries})")
                response = self.api.get(endpoint, params)

                if response["status"] == 200:
                    if use_cache:
                        self._save_cache(cache_path, response["data"])
                    return response["data"]
                else:
                    print(f"  [오류] {response.get('error')}")

            except Exception as e:
                print(f"  [예외] {e}")

            if attempt < max_retries:
                wait_time = attempt * 0.5
                print(f"  [대기] {wait_time}초 후 재시도...")
                time.sleep(wait_time)

        print(f"  [실패] 최대 재시도 횟수 초과: {endpoint}")
        return None
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_04_api_collector.py
```

**결과:**

```
============================================================
  API 데이터 수집기
============================================================

[1] 날씨 데이터 수집
----------------------------------------
  [API 호출] /api/weather/all (시도 1/3)
  저장 완료: /tmp/dashboard-data/api/weather.json

  수집된 날씨 데이터:
    서울: 27.8°C, 흐림, 습도 41%
    부산: 19.5°C, 맑음, 습도 87%
    대구: 26.8°C, 흐림, 습도 42%
    인천: 19.7°C, 흐림, 습도 78%
    광주: 29.3°C, 흐림, 습도 84%
    대전: 24.0°C, 맑음, 습도 57%

[2] 환율 데이터 수집
----------------------------------------
  [API 호출] /api/exchange (시도 1/3)
  저장 완료: /tmp/dashboard-data/api/exchange.json

  수집된 환율 데이터:
    USD (미국 달러): 1,355.88원
    EUR (유로): 1,415.97원
    JPY (일본 엔(100엔)): 913.81원
    CNY (중국 위안): 180.56원
    GBP (영국 파운드): 1,671.53원

[3] 주식 시세 수집
----------------------------------------
  [API 호출] /api/stock (시도 1/3)
  저장 완료: /tmp/dashboard-data/api/stocks.json

  수집된 주식 데이터:
    삼성전자 (005930): 71,029원 (-2,163, -3.05%)
    SK하이닉스 (000660): 144,898원 (-2,208, -1.52%)
    NAVER (035420): 225,541원 (-183, -0.08%)
    카카오 (035720): 41,423원 (+2,977, +7.19%)
    현대차 (005380): 205,142원 (-1,978, -0.96%)

[4] 캐시 동작 확인
----------------------------------------
  [캐시 적중] /api/weather/all
  -> 두 번째 호출 시 캐시에서 즉시 로드됨

============================================================
  수집 결과 요약
============================================================
  날씨 데이터: 6개 도시
  환율 데이터: 5개 통화
  주식 데이터: 5개 종목
  캐시 디렉토리: /tmp/dashboard-data/cache
  캐시 파일 수: 3개
```

API 수집기에서 배우는 핵심 패턴 세 가지를 정리합니다:

#### 1. 캐싱 패턴

```python
# 요청 URL + 파라미터를 해시하여 고유한 캐시 키 생성
cache_key = f"{endpoint}_{json.dumps(params, sort_keys=True)}"
cache_hash = hashlib.md5(cache_key.encode()).hexdigest()
```

같은 요청을 반복하지 않도록 결과를 파일에 저장합니다. 캐시 유효 시간(TTL)이 지나면 자동으로 새로 요청합니다.

#### 2. 재시도 패턴

```python
for attempt in range(1, max_retries + 1):
    try:
        response = self.api.get(endpoint, params)
        if response["status"] == 200:
            return response["data"]
    except Exception as e:
        print(f"  [예외] {e}")

    if attempt < max_retries:
        time.sleep(attempt * 0.5)  # 점진적 대기
```

네트워크 오류에 대비하여 최대 3회까지 재시도하며, 대기 시간을 점차 늘립니다.

#### 3. 에러 처리 패턴

API 응답의 상태 코드를 확인하고, 예외 발생 시에도 프로그램이 중단되지 않도록 `try-except`로 감쌉니다.

> **Warning:** 실제 API를 사용할 때는 반드시 API 키를 환경 변수에 저장하세요. 코드에 직접 작성하면 보안 위험이 있습니다. Chapter 23에서 배운 보안 원칙을 적용하세요.

### Step 2 점검

- [x] CSV 파일을 로드하고 기본 정보를 확인할 수 있는가?
- [x] 숫자 컬럼의 통계를 계산할 수 있는가?
- [x] API 수집 시 캐싱과 재시도가 동작하는가?
- [x] 수집된 데이터가 JSON 파일로 저장되는가?

---

## 27.5 Step 3: 데이터 처리

수집한 데이터를 바로 분석할 수는 없습니다. 현실 세계의 데이터에는 결측치, 이상치, 잘못된 형식 등 다양한 품질 문제가 존재합니다. 이 단계에서는 데이터를 정제(cleaning)하고 분석에 적합한 형태로 변환(transformation)합니다.

### 예제 27-05: 데이터 정제

AI에게 다음과 같이 요청합니다:

```
프롬프트:
"판매 데이터의 품질 문제를 탐지하고 처리하는 DataCleaner 클래스를 작성해줘.

탐지 기능:
- 결측치 (빈 값) 탐지
- 숫자 필드의 형식 오류 및 음수 값 탐지
- IQR 방법으로 이상치 탐지
- 날짜 형식 오류 탐지
- 중복 레코드 탐지

처리 기능:
- 결측치: 중앙값/기본값 대체 또는 행 삭제
- 형식 오류: 해당 행 제거
- 이상치: 상한값 초과 시 제거
- 중복: 첫 번째만 유지

정제 결과 보고서도 출력해줘."
```

**예제 27-05: 데이터 정제 도구**

```python
# examples/python/chapter06/ex27_05_data_cleaner.py

import copy


class DataCleaner:
    """데이터 정제 도구: 다양한 데이터 품질 문제를 탐지하고 처리합니다."""

    def __init__(self, records):
        self.original = records
        self.cleaned = copy.deepcopy(records)
        self.issues = []
        self.stats = {
            "총_레코드": len(records),
            "결측치": 0, "이상치": 0, "형식오류": 0,
            "중복": 0, "음수값": 0, "수정됨": 0, "제거됨": 0,
        }

    def detect_missing_values(self, required_fields):
        """결측치(빈 값)를 탐지합니다."""
        count = 0
        for i, record in enumerate(self.cleaned):
            for field in required_fields:
                if field in record and str(record[field]).strip() == "":
                    self.issues.append({
                        "행": i, "필드": field, "유형": "결측치", "값": record[field],
                    })
                    count += 1
        self.stats["결측치"] = count
        return count

    def detect_outliers(self, field):
        """IQR 방법으로 이상치를 탐지합니다."""
        values = []
        for record in self.cleaned:
            try:
                val = float(str(record.get(field, "")).strip())
                if val >= 0:
                    values.append(val)
            except ValueError:
                continue

        if len(values) < 4:
            return 0

        values.sort()
        n = len(values)
        q1 = values[n // 4]
        q3 = values[3 * n // 4]
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        count = 0
        for i, record in enumerate(self.cleaned):
            try:
                val = float(str(record.get(field, "")).strip())
                if val < lower_bound or val > upper_bound:
                    self.issues.append({
                        "행": i, "필드": field, "유형": "이상치", "값": str(val),
                    })
                    count += 1
            except ValueError:
                continue

        self.stats["이상치"] += count
        return count

    def fix_missing_values(self, field, strategy="median", default_value=None):
        """결측치를 처리합니다."""
        if strategy == "median":
            # 중앙값으로 대체
            values = []
            for r in self.cleaned:
                try:
                    values.append(float(str(r[field]).strip()))
                except (ValueError, KeyError):
                    pass
            if values:
                values.sort()
                median_val = values[len(values) // 2]
                for record in self.cleaned:
                    if str(record.get(field, "")).strip() == "":
                        record[field] = str(int(median_val))
                        self.stats["수정됨"] += 1

    def fix_duplicates(self, key_field="주문번호"):
        """중복 레코드를 제거합니다 (첫 번째만 유지)."""
        seen = set()
        unique = []
        for record in self.cleaned:
            key = record.get(key_field, "")
            if key not in seen:
                seen.add(key)
                unique.append(record)
            else:
                self.stats["제거됨"] += 1
        self.cleaned = unique
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_05_data_cleaner.py
```

**결과:**

```
============================================================
  데이터 정제 도구
============================================================

불량 데이터가 포함된 샘플 생성 중...
생성된 레코드: 52개

============================================================
  1단계: 데이터 품질 검사
============================================================

[검사] 결측치 탐지 중...
  발견: 6건

[검사] 숫자 필드 유효성 검사 중...
  형식 오류: 2건
  음수 값: 2건

[검사] '단가' 이상치 탐지 중 (IQR 방법)...
  Q1: 22,794, Q3: 34,253, IQR: 11,459
  정상 범위: 5,606 ~ 51,442
  발견: 2건

[검사] '수량' 이상치 탐지 중 (IQR 방법)...
  Q1: 2, Q3: 7, IQR: 5
  정상 범위: 0 ~ 14
  발견: 1건

[검사] '날짜' 날짜 유효성 검사 중...
  발견: 2건

[검사] 중복 레코드 탐지 중 (키: 주문번호)...
  발견: 2건

============================================================
  2단계: 데이터 정제
============================================================

결측치 처리...
숫자 오류 처리...
이상치 처리...
중복 제거...

============================================================
  데이터 정제 결과 보고서
============================================================

원본 데이터: 52개 레코드
정제 후 데이터: 44개 레코드

발견된 문제:
  결측치: 6건
  형식 오류: 4건
  음수 값: 2건
  이상치: 3건
  중복: 2건
  --------
  합계: 17건

처리 결과:
  수정된 값: 6건
  제거된 행: 8건
  데이터 손실률: 15.4%
```

데이터 정제에서 핵심 개념인 **IQR(사분위 범위) 이상치 탐지**를 설명합니다:

```
IQR = Q3 - Q1 (상위 25% 값 - 하위 25% 값)
하한 = Q1 - 1.5 * IQR
상한 = Q3 + 1.5 * IQR

이 범위 밖의 값 = 이상치
```

예를 들어, 단가 데이터에서:
- Q1(하위 25%) = 22,794원
- Q3(상위 25%) = 34,253원
- IQR = 11,459원
- 정상 범위: 5,606원 ~ 51,442원

9,999,999원 같은 값은 명백한 이상치로 탐지됩니다.

> **Note:** 데이터 정제 전략은 상황에 따라 다릅니다. 결측치를 중앙값으로 대체할 수도 있고, 해당 행을 삭제할 수도 있습니다. AI에게 "우리 데이터의 특성상 어떤 전략이 적합한지 분석해줘"라고 요청하면 좋습니다.

### 예제 27-06: 데이터 변환

정제된 데이터를 분석에 적합한 형태로 변환합니다. 파생 변수 생성, 집계, 피벗 테이블 같은 변환 작업을 수행합니다.

```
프롬프트:
"정제된 판매 데이터를 분석용으로 변환하는 모듈을 작성해줘.

기능:
1. 파생 변수 생성: 날짜에서 월/요일/분기 추출, 금액 구간 분류
2. 그룹별 집계: group_by + sum/mean/count
3. 피벗 테이블: 행/열 필드와 집계 함수 지정
4. 형식 변환: 딕셔너리 리스트 -> 컬럼 기반, 중첩 구조

collections.defaultdict 활용, 외부 라이브러리 없이."
```

**예제 27-06: 데이터 변환 도구**

```python
# examples/python/chapter06/ex27_06_data_transform.py

import datetime
from collections import defaultdict


def add_derived_columns(records):
    """파생 변수(새로운 컬럼)를 추가합니다."""

    for record in records:
        # 날짜 파생 변수
        date = datetime.datetime.strptime(record["날짜"], "%Y-%m-%d")
        record["월"] = date.month
        record["요일"] = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        record["분기"] = f"Q{(date.month - 1) // 3 + 1}"

        # 금액 구간 분류
        total = record["총액"]
        if total < 50000:
            record["금액구간"] = "소액"
        elif total < 200000:
            record["금액구간"] = "중액"
        else:
            record["금액구간"] = "고액"

        # 할인 금액 계산
        record["할인금액"] = int(record["단가"] * record["수량"] * record["할인율"])

    return records


def aggregate(records, group_by, agg_field, agg_func="sum"):
    """데이터를 그룹별로 집계합니다."""

    groups = defaultdict(list)
    for record in records:
        key = record[group_by]
        try:
            groups[key].append(float(record[agg_field]))
        except (ValueError, TypeError):
            pass

    result = {}
    for key, values in groups.items():
        if agg_func == "sum":
            result[key] = sum(values)
        elif agg_func == "mean":
            result[key] = sum(values) / len(values) if values else 0
        elif agg_func == "count":
            result[key] = len(values)

    return result


def create_pivot_table(records, row_field, col_field, value_field, agg_func="sum"):
    """피벗 테이블을 생성합니다."""

    pivot = defaultdict(lambda: defaultdict(list))
    col_values = set()

    for record in records:
        row_key = record[row_field]
        col_key = record[col_field]
        col_values.add(col_key)
        try:
            pivot[row_key][col_key].append(float(record[value_field]))
        except (ValueError, TypeError):
            pass

    # 집계 적용
    result = {}
    col_values = sorted(col_values)
    for row_key in sorted(pivot.keys()):
        result[row_key] = {}
        for col_key in col_values:
            values = pivot[row_key].get(col_key, [])
            if not values:
                result[row_key][col_key] = 0
            elif agg_func == "sum":
                result[row_key][col_key] = sum(values)
            elif agg_func == "count":
                result[row_key][col_key] = len(values)

    return result, col_values
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_06_data_transform.py
```

**결과:**

```
============================================================
  데이터 변환 도구
============================================================

원본 데이터: 150개 레코드, 10개 컬럼

------------------------------------------------------------
[변환] 파생 변수 생성 중...
  추가된 컬럼: 연도, 월, 요일, 분기, 금액구간, 할인금액, 건당단가
변환 후: 17개 컬럼

------------------------------------------------------------
[집계] 카테고리별 총 매출:
  전자기기:   11,609,275원
  사무용품:    4,295,692원
  액세서리:    2,581,279원

[집계] 월별 주문 건수:
   1월:   26건
   2월:   15건
   3월:   33건
   4월:   28건
   5월:   25건
   6월:   23건

[피벗] 카테고리 x 분기 매출:
       |         Q1 |         Q2 |         합계
---------------------------------------------
  사무용품 |  2,267,366 |  2,028,326 |  4,295,692
  액세서리 |    689,230 |  1,892,049 |  2,581,279
  전자기기 |  6,180,414 |  5,428,861 | 11,609,275
---------------------------------------------
    합계 |  9,137,010 |  9,349,236 | 18,486,246

[파생 변수 활용] 금액 구간별 분포:
  소액:   27건 ( 18.0%)
  중액:   98건 ( 65.3%)
  고액:   25건 ( 16.7%)
```

이 코드에서 특히 중요한 세 가지 변환 기법을 정리합니다:

#### 1. 파생 변수 생성

날짜 하나에서 월, 요일, 분기를 추출합니다. 이렇게 만든 파생 변수로 "월별 매출 추이", "요일별 판매 패턴" 같은 분석이 가능해집니다.

```python
date = datetime.datetime.strptime(record["날짜"], "%Y-%m-%d")
record["월"] = date.month
record["분기"] = f"Q{(date.month - 1) // 3 + 1}"
```

#### 2. 그룹별 집계

`defaultdict(list)`로 그룹을 만들고, `sum`, `mean`, `count` 등의 집계 함수를 적용합니다.

```python
groups = defaultdict(list)
for record in records:
    groups[record[group_by]].append(float(record[agg_field]))
```

#### 3. 피벗 테이블

행과 열을 지정하여 2차원 교차 분석을 수행합니다. 예를 들어 "카테고리(행) x 분기(열)" 피벗으로 각 카테고리의 분기별 매출을 한눈에 볼 수 있습니다.

> **Tip:** 피벗 테이블은 비즈니스 분석에서 가장 많이 사용되는 기법입니다. "카테고리별로 분기 매출을 비교하고 싶어"라고 AI에게 요청하면 피벗 테이블을 추천받을 수 있습니다.

### Step 3 점검

- [x] 결측치, 이상치, 중복을 자동으로 탐지하는가?
- [x] IQR 방법으로 이상치의 정상 범위를 계산하는가?
- [x] 정제 결과 보고서가 출력되는가?
- [x] 파생 변수가 정상적으로 생성되는가?
- [x] 그룹별 집계와 피벗 테이블이 동작하는가?

---

## 27.6 Step 4: 통계 계산

정제되고 변환된 데이터로 본격적인 통계 분석을 수행합니다. 기본 통계량부터 상관관계, 그룹별 분석, 파레토 분석까지 다양한 분석 기법을 구현합니다.

### 예제 27-07: 기본 통계

AI에게 다음과 같이 요청합니다:

```
프롬프트:
"표준 라이브러리의 statistics 모듈을 활용하여 기본 통계 분석 함수들을 작성해줘.

기능:
1. 기본 통계량: 평균, 중앙값, 표준편차, 분산, 최솟값, 최댓값, 범위
2. 백분위수 계산 (P10, P25, P50, P75, P90, P95, P99)
3. 최빈값 (Counter 활용)
4. 왜도(비대칭도) 계산
5. 피어슨 상관계수 계산
6. 분포 히스토그램 (텍스트 기반)

각 결과를 보기 좋게 출력하는 함수도 포함."
```

**예제 27-07: 기본 통계 분석**

```python
# examples/python/chapter06/ex27_07_basic_stats.py

import statistics
import math
from collections import Counter


def calculate_basic_stats(values, label="데이터"):
    """기본 통계량을 계산합니다."""

    n = len(values)
    mean = statistics.mean(values)
    median = statistics.median(values)
    stdev = statistics.stdev(values) if n >= 2 else 0
    variance = statistics.variance(values) if n >= 2 else 0

    return {
        "개수": n,
        "합계": sum(values),
        "평균": mean,
        "중앙값": median,
        "표준편차": stdev,
        "분산": variance,
        "최솟값": min(values),
        "최댓값": max(values),
        "범위": max(values) - min(values),
    }


def calculate_percentiles(values):
    """백분위수를 계산합니다."""

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    percentiles = {}
    for p in [10, 25, 50, 75, 90, 95, 99]:
        idx = int(n * p / 100)
        idx = min(idx, n - 1)
        percentiles[f"P{p}"] = sorted_vals[idx]

    return percentiles


def calculate_correlation(x_values, y_values):
    """두 변수 간의 피어슨 상관계수를 계산합니다."""

    n = len(x_values)
    if n != len(y_values) or n < 2:
        return 0

    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    covariance = sum((x - mean_x) * (y - mean_y)
                     for x, y in zip(x_values, y_values)) / (n - 1)

    std_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values) / (n - 1))
    std_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values) / (n - 1))

    if std_x == 0 or std_y == 0:
        return 0

    return covariance / (std_x * std_y)


def print_distribution(values, bins=10, label="분포"):
    """값의 분포를 텍스트 히스토그램으로 출력합니다."""

    min_val = min(values)
    max_val = max(values)
    bin_width = (max_val - min_val) / bins if max_val > min_val else 1

    bin_counts = [0] * bins
    for v in values:
        idx = int((v - min_val) / bin_width)
        idx = min(idx, bins - 1)
        bin_counts[idx] += 1

    max_count = max(bin_counts)

    print(f"\n  {label} (구간: {bins}개)")
    print(f"  {'구간':>16s} | {'빈도':>5s} | 분포")
    print(f"  {'-' * 16}-+{'-' * 6}-+{'-' * 30}")

    for i in range(bins):
        lower = min_val + i * bin_width
        upper = lower + bin_width
        count = bin_counts[i]
        bar_len = int(count / max_count * 25) if max_count > 0 else 0
        bar = "#" * bar_len

        print(f"  {lower:>7,.0f}~{upper:>7,.0f} | {count:>5d} | {bar}")
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_07_basic_stats.py
```

**결과:**

```
============================================================
  기본 통계 분석
============================================================

데이터: 200개 판매 레코드

============================================================
  1. 기본 통계량
============================================================

  '총액' 통계
  ----------------------------------------
        개수:             200
        합계:      31,184,673
        평균:      155,923.36
       중앙값:      135,491.00
      표준편차:      109,940.35
       최솟값:           9,697
       최댓값:         551,430
        범위:         541,733

  '수량' 통계
  ----------------------------------------
        개수:             200
        합계:           1,123
        평균:            5.62
       중앙값:            6.00
      표준편차:            2.90

============================================================
  2. 총액 백분위수
============================================================

   P10:     39,066원 |==
   P25:     67,744원 |===
   P50:    135,552원 |=======
   P75:    211,428원 |===========
   P90:    313,792원 |=================
   P95:    381,906원 |====================
   P99:    508,932원 |===========================

============================================================
  3. 최빈값 (가장 많이 팔린)
============================================================

  상품별 판매 빈도 (상위 5개):
        USB 허브:   30건 ( 15.0%)
       노트북 파우치:   27건 ( 13.5%)
           헤드셋:   27건 ( 13.5%)
      블루투스 마우스:   25건 ( 12.5%)
         마우스패드:   25건 ( 12.5%)

============================================================
  4. 분포 특성
============================================================

  총액 왜도: 1.048
  -> 오른쪽으로 치우친 분포 (고액 주문이 적음)

============================================================
  5. 상관관계 분석
============================================================

  수량 vs 총액:  r =  0.6846 (중간 상관)
  단가 vs 총액:  r =  0.6043 (중간 상관)
  수량 vs 단가:  r = -0.0674 (약한 상관)
```

이 통계 분석에서 알 수 있는 핵심 인사이트를 정리합니다:

#### 통계 용어 이해하기

| 통계량 | 의미 | 이 데이터에서의 의미 |
|--------|------|---------------------|
| **평균** | 모든 값의 산술 평균 | 평균 주문액은 약 15만 6천원 |
| **중앙값** | 데이터의 정확한 가운데 값 | 절반의 주문은 13만 5천원 이하 |
| **표준편차** | 데이터가 평균에서 얼마나 흩어져 있는지 | 약 11만원의 편차 (큰 편) |
| **왜도** | 분포가 좌우 대칭인지 | +1.048: 오른쪽으로 치우침 (고액 주문이 적음) |
| **상관계수** | 두 변수의 관련성 (-1 ~ +1) | 수량과 총액은 중간 정도의 양의 상관 |

#### 상관계수 해석

```
|r| > 0.7  --> 강한 상관 (함께 움직이는 정도가 큼)
|r| > 0.3  --> 중간 상관 (어느 정도 관련 있음)
|r| < 0.3  --> 약한 상관 (거의 관련 없음)
```

수량과 단가의 상관계수가 -0.067로 약한 상관인 것은, 많이 사는 것과 비싼 것을 사는 것이 거의 관련 없다는 뜻입니다. 반면 수량과 총액은 0.685로 중간 상관이며, 이는 당연히 많이 사면 총액이 커지기 때문입니다.

> **Tip:** 통계 분석 결과를 해석할 때 AI에게 "이 상관계수 결과가 비즈니스적으로 어떤 의미인지 설명해줘"라고 요청하면 실무에 바로 활용할 수 있는 인사이트를 얻을 수 있습니다.

### 예제 27-08: 그룹별 분석

단순한 전체 통계를 넘어, 카테고리별, 지역별, 기간별로 데이터를 그룹화하여 더 깊은 인사이트를 도출합니다.

```
프롬프트:
"판매 데이터를 다양한 기준으로 그룹 분석하는 모듈을 작성해줘.

분석 항목:
1. 카테고리별 매출 통계 (건수, 합계, 평균, 표준편차)
2. 지역별 매출 분석 (비율 포함)
3. 고객등급별 분석 (객단가, 최고거래)
4. 교차 분석 (지역 x 카테고리)
5. 월별 성장률 분석
6. 파레토 분석 (80/20 법칙)
7. 카테고리별 Top 3 거래

statistics, collections.defaultdict 사용."
```

**예제 27-08: 그룹별 데이터 분석**

```python
# examples/python/chapter06/ex27_08_group_analysis.py

import statistics
from collections import defaultdict


def group_stats(data, group_field, value_field):
    """그룹별 통계를 계산합니다."""

    groups = defaultdict(list)
    for record in data:
        groups[record[group_field]].append(record)

    results = {}
    for group_name, records in groups.items():
        values = [r[value_field] for r in records]
        results[group_name] = {
            "건수": len(values),
            "합계": sum(values),
            "평균": statistics.mean(values),
            "중앙값": statistics.median(values),
            "최솟값": min(values),
            "최댓값": max(values),
            "표준편차": statistics.stdev(values) if len(values) >= 2 else 0,
        }

    return results


def growth_analysis(data, period_field="월", value_field="총액"):
    """기간별 성장률을 분석합니다."""

    period_totals = defaultdict(float)
    for record in data:
        period_totals[record[period_field]] += record[value_field]

    sorted_periods = sorted(period_totals.keys())

    results = []
    prev_value = None
    for period in sorted_periods:
        current = period_totals[period]
        growth = None
        if prev_value is not None and prev_value != 0:
            growth = (current - prev_value) / prev_value * 100
        results.append({"기간": period, "매출": current, "성장률": growth})
        prev_value = current

    return results


def pareto_analysis(data, group_field, value_field="총액"):
    """파레토 분석 (80/20 법칙)을 수행합니다."""

    group_totals = defaultdict(float)
    for record in data:
        group_totals[record[group_field]] += record[value_field]

    sorted_groups = sorted(group_totals.items(), key=lambda x: -x[1])
    grand_total = sum(v for _, v in sorted_groups)

    results = []
    cumulative = 0
    for name, total in sorted_groups:
        cumulative += total
        results.append({
            "항목": name,
            "매출": total,
            "비율": total / grand_total * 100,
            "누적비율": cumulative / grand_total * 100,
        })

    return results
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_08_group_analysis.py
```

**결과:**

```
============================================================
  그룹별 데이터 분석
============================================================

데이터: 300개 판매 레코드

============================================================
  1. 카테고리별 매출 통계
============================================================

    카테고리 |    건수 |           합계 |         평균 |       표준편차
-----------------------------------------------------------------
    사무용품 |    93 |   16,663,149 |    179,174 |    106,446
    액세서리 |    87 |    6,953,675 |     79,927 |     55,944
    전자기기 |   120 |   21,465,216 |    178,877 |    126,863

============================================================
  2. 지역별 매출 분석
============================================================

    지역 |    건수 |           합계 |     비율 |         평균
-------------------------------------------------------
    인천 |    70 |   10,853,033 |  24.1% |    155,043
    대구 |    56 |    9,226,241 |  20.5% |    164,754
    부산 |    63 |    9,207,583 |  20.4% |    146,152
    서울 |    61 |    8,475,479 |  18.8% |    138,942
    경기 |    50 |    7,319,704 |  16.2% |    146,394

============================================================
  5. 월별 매출 성장률
============================================================

   월 |           매출 |      성장률 | 추세
--------------------------------------------------
   1 |    6,990,558 |     -   |
   2 |    5,425,471 |   -22.4% | -- 크게 하락
   3 |    9,126,582 |   +68.2% | ++ 크게 상승
   4 |    7,063,585 |   -22.6% | -- 크게 하락
   5 |    7,853,178 |   +11.2% | ++ 크게 상승
   6 |    8,622,666 |    +9.8% | +  소폭 상승

============================================================
  6. 파레토 분석 (상품별 매출)
============================================================

  순위 |            상품명 |           매출 |     비율 |     누적 | 그래프
---------------------------------------------------------------------------
   1 |            헤드셋 |    7,650,889 |  17.0% |  17.0% | ########
   2 |        노트북 스탠드 |    6,943,140 |  15.4% |  32.4% | #######
   3 |        모니터 거치대 |    5,286,296 |  11.7% |  44.1% | #####
   4 |         무선 키보드 |    4,984,494 |  11.1% |  55.2% | #####
   5 |         USB 허브 |    4,718,133 |  10.5% |  65.6% | #####
   6 |         책상 정리함 |    4,433,713 |   9.8% |  75.5% | ####
   7 |       블루투스 마우스 |    4,111,700 |   9.1% |  84.6% | #### <-- 80%
   8 |        노트북 파우치 |    3,315,088 |   7.4% |  91.9% | ###
   9 |          마우스패드 |    1,934,309 |   4.3% |  96.2% | ##
  10 |         충전 케이블 |    1,704,278 |   3.8% | 100.0% | #
```

이 분석에서 도출할 수 있는 **비즈니스 인사이트**를 살펴봅시다:

#### 파레토 분석 (80/20 법칙)

파레토 분석은 "전체 매출의 80%를 차지하는 상위 항목"을 찾는 기법입니다. 결과를 보면:

- 상위 7개 상품(전체의 70%)이 전체 매출의 약 84.6%를 차지합니다
- 특히 헤드셋과 노트북 스탠드 2개 상품만으로 32.4%를 차지합니다
- 이 핵심 상품에 마케팅을 집중하면 효과적입니다

#### 성장률 분석

월별 매출 성장률을 보면:

```
성장률 = (현재 매출 - 이전 매출) / 이전 매출 * 100%
```

- 2월에 22.4% 하락 후, 3월에 68.2% 급등
- 4월 다시 22.6% 하락, 이후 5~6월 회복 추세
- 이런 패턴은 계절성이나 이벤트의 영향을 분석할 필요가 있습니다

> **Note:** 그룹별 분석은 "어디에 집중해야 하는가?"라는 질문에 답합니다. 카테고리별, 지역별, 기간별로 데이터를 나눠보면 전체 평균만으로는 보이지 않는 패턴을 발견할 수 있습니다.

### Step 4 점검

- [x] 기본 통계량(평균, 중앙값, 표준편차)이 정확히 계산되는가?
- [x] 백분위수와 분포 히스토그램이 출력되는가?
- [x] 상관계수로 변수 간 관계를 파악할 수 있는가?
- [x] 카테고리/지역/기간별 그룹 분석이 동작하는가?
- [x] 파레토 분석으로 핵심 항목을 식별할 수 있는가?

---

## 27.7 Step 5: CLI 출력 - 테이블

마지막 단계입니다. 지금까지 수집, 정제, 분석한 결과를 터미널에서 보기 좋게 출력합니다. rich 같은 외부 라이브러리 없이, ANSI 이스케이프 코드와 유니코드 문자를 사용하여 깔끔한 테이블을 직접 구현합니다.

### ANSI 이스케이프 코드란?

터미널에서 텍스트에 색상과 스타일을 적용하는 특수 문자열입니다:

```python
# 형식: \033[코드m
"\033[1m"   # 굵게 (Bold)
"\033[31m"  # 빨간색
"\033[32m"  # 녹색
"\033[33m"  # 노란색
"\033[0m"   # 리셋 (기본으로 되돌림)

# 사용 예시
print("\033[1m\033[32m성공!\033[0m")  # "성공!"이 굵은 녹색으로 출력
```

### AI에게 테이블 클래스 요청하기

```
프롬프트:
"터미널에서 깔끔한 테이블을 출력하는 Table 클래스를 작성해줘.

요구사항:
- ANSI 색상 코드로 헤더/행/하이라이트 색상 지원
- 유니코드 박스 드로잉 문자로 테두리 (unicode, single, double 스타일)
- 컬럼별 너비, 정렬(좌/우/가운데) 설정
- 숫자 자동 포맷 (천 단위 콤마)
- 하단 합계 행 (footer)
- 행 하이라이트 기능
- rich 라이브러리 사용하지 않고 직접 구현"
```

### 예제 27-09: 테이블 출력

**예제 27-09: 테이블 출력 시스템**

```python
# examples/python/chapter06/ex27_09_table_output.py

import os


class Color:
    """ANSI 색상 코드를 관리합니다."""

    # 텍스트 색상
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"

    # 밝은 색상
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_CYAN = "\033[96m"

    # 스타일
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @classmethod
    def colorize(cls, text, color):
        """텍스트에 색상을 적용합니다."""
        return f"{color}{text}{cls.RESET}"


class Table:
    """터미널에서 깔끔한 테이블을 출력합니다."""

    # 유니코드 박스 드로잉 문자
    BORDER_UNICODE = {
        "tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518",
        "h": "\u2500", "v": "\u2502",
        "lj": "\u251c", "rj": "\u2524", "tj": "\u252c", "bj": "\u2534",
        "cj": "\u253c",
    }

    BORDER_SINGLE = {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "h": "-", "v": "|",
        "lj": "+", "rj": "+", "tj": "+", "bj": "+", "cj": "+",
    }

    def __init__(self, title=None, border_style="unicode"):
        self.title = title
        self.columns = []
        self.rows = []
        self.footer = None
        self.border = (self.BORDER_UNICODE if border_style == "unicode"
                       else self.BORDER_SINGLE)

    def add_column(self, name, width=None, align="right", color=None):
        """컬럼을 추가합니다."""
        if width is None:
            width = max(len(name) + 2, 8)
        self.columns.append({
            "name": name, "width": width,
            "align": align, "color": color,
        })

    def add_row(self, *values, highlight=False, color=None):
        """행을 추가합니다."""
        self.rows.append({
            "values": values, "highlight": highlight, "color": color,
        })

    def set_footer(self, *values):
        """하단 합계 행을 설정합니다."""
        self.footer = values

    def _format_cell(self, value, col_info, row_color=None):
        """셀 값을 포맷합니다."""
        width = col_info["width"]
        align = col_info["align"]
        color = row_color or col_info.get("color")

        if isinstance(value, (int, float)):
            text = f"{value:,.1f}" if isinstance(value, float) else f"{value:,}"
        else:
            text = str(value)

        if len(text) > width:
            text = text[:width - 2] + ".."

        if align == "right":
            text = text.rjust(width)
        elif align == "center":
            text = text.center(width)
        else:
            text = text.ljust(width)

        if color:
            text = Color.colorize(text, color)

        return text

    def render(self):
        """테이블을 렌더링합니다."""
        lines = []
        b = self.border

        # 제목
        if self.title:
            total_width = sum(c["width"] + 3 for c in self.columns) - 1
            title_line = Color.colorize(
                f" {self.title} ".center(total_width),
                Color.BOLD + Color.BRIGHT_CYAN
            )
            lines.append(title_line)

        # 상단 테두리 + 헤더 + 데이터 + 하단 테두리
        # ... (전체 코드는 예제 파일 참조)
        return "\n".join(lines)

    def print(self):
        """테이블을 출력합니다."""
        print(self.render())
```

이 Table 클래스를 사용하여 대시보드를 구성하는 방법을 살펴봅시다:

```python
# 월별 판매 현황 테이블 만들기
table = Table(title="월별 판매 현황")
table.add_column("월", width=6, align="center")
table.add_column("매출(만원)", width=12)
table.add_column("건수", width=8)
table.add_column("객단가", width=10)
table.add_column("전월비", width=8, align="center")

# 데이터 행 추가
table.add_row("1월", 4520, 156, 28974, "-")
table.add_row("2월", 3890, 134, 29030, "하락")
table.add_row("3월", 5210, 178, 29270, "상승")
table.add_row("5월", 6340, 215, 29488, "상승", highlight=True)  # 최고 매출

# 합계 행
table.set_footer("합계", 30810, 1046, 294550, "-")
table.print()
```

**실행:**

```bash
$ python examples/python/chapter06/ex27_09_table_output.py
```

**결과:**

```
                         월별 판매 현황
+--------+--------------+----------+------------+----------+
|   월   |   매출(만원)   |   건수   |    객단가    |   전월비   |
+--------+--------------+----------+------------+----------+
|  1월   |        4,520 |      156 |     28,974 |    -     |
|  2월   |        3,890 |      134 |     29,030 |  -하락   |
|  3월   |        5,210 |      178 |     29,270 |  +상승   |
|  4월   |        4,870 |      165 |     29,515 |  -하락   |
|  5월   |        6,340 |      215 |     29,488 |  +상승   |  <-- 최고 매출
|  6월   |        5,980 |      198 |     30,202 |  -하락   |
+--------+--------------+----------+------------+----------+
|  합계  |       30,810 |    1,046 |    294,550 |    -     |
+--------+--------------+----------+------------+----------+

                     카테고리별 실적 요약
+------------+----------+--------------+------------+----------+----------+
|   카테고리   |   상품수   |     총매출     |    평균단가   |   점유율   |   상태   |
+------------+----------+--------------+------------+----------+----------+
|   전자기기   |       45 |   15,800,000 |     48,200 |    52.3% |  +상승   |
|   사무용품   |       30 |    8,900,000 |     33,500 |    29.5% |  =유지   |
|   액세서리   |       25 |    5,500,000 |     18,700 |    18.2% |  -하락   |
+------------+----------+--------------+------------+----------+----------+
|    합계     |      100 |   30,200,000 |      -     |    100%  |    -     |
+------------+----------+--------------+------------+----------+----------+

                     지역별 매출 순위
+------+----------+--------------+--------+----------+
| 순위 |    지역   |      매출     |  건수  |   점유율   |
+------+----------+--------------+--------+----------+
|  1   |   서울   |   12,500,000 |     95 |    31.2% |
|  2   |   경기   |    9,800,000 |     76 |    24.5% |
|  3   |   부산   |    6,200,000 |     48 |    15.5% |
|  4   |   인천   |    5,800,000 |     44 |    14.5% |
|  5   |   대구   |    5,700,000 |     42 |    14.3% |
+------+----------+--------------+--------+----------+
```

> **Note:** 실제 터미널에서는 유니코드 박스 드로잉 문자(+-- 대신 기호)와 색상이 적용되어 훨씬 깔끔하게 보입니다. ANSI 코드를 지원하지 않는 환경에서는 `border_style="single"` 옵션으로 ASCII 테이블을 사용할 수 있습니다.

### Table 클래스의 핵심 설계

이 클래스의 구조를 분석하면 **빌더 패턴(Builder Pattern)**이 적용되어 있습니다:

```python
# 1. 테이블 생성
table = Table(title="제목")

# 2. 컬럼 정의 (빌더 패턴)
table.add_column("이름", width=10, align="center")
table.add_column("값", width=12, align="right")

# 3. 데이터 추가
table.add_row("항목1", 1234)
table.add_row("항목2", 5678, highlight=True)

# 4. 합계 추가 (선택적)
table.set_footer("합계", 6912)

# 5. 출력
table.print()
```

이 패턴은 복잡한 객체를 단계적으로 구성할 수 있게 해줍니다. 컬럼 수, 데이터 양, 스타일에 관계없이 동일한 방식으로 테이블을 만들 수 있습니다.

### Step 5 점검

- [x] ANSI 색상 코드로 텍스트에 색상을 적용할 수 있는가?
- [x] 유니코드/ASCII 두 가지 테두리 스타일을 지원하는가?
- [x] 숫자가 천 단위 콤마로 포맷되는가?
- [x] 행 하이라이트와 합계 행이 동작하는가?
- [x] 다양한 정렬(좌/우/가운데)이 적용되는가?

---

## 27.8 전체 프로젝트 통합

지금까지 만든 5개 모듈을 하나로 연결하면 완전한 데이터 대시보드가 됩니다. 전체 데이터 흐름을 다시 정리합니다:

```
1. 프로젝트 구조 생성 (ex27_01)
   └─> dashboard-cli/ 폴더 구조 자동 생성

2. 데이터 수집 (ex27_02 ~ ex27_04)
   ├─> CSV: 판매 데이터 200건 로드
   └─> API: 날씨/환율/주식 데이터 수집 (캐싱 포함)

3. 데이터 처리 (ex27_05 ~ ex27_06)
   ├─> 정제: 결측치 6건, 형식오류 4건, 이상치 3건, 중복 2건 처리
   └─> 변환: 7개 파생 변수 추가, 집계/피벗 수행

4. 통계 분석 (ex27_07 ~ ex27_08)
   ├─> 기본 통계: 평균 155,923원, 중앙값 135,491원
   ├─> 상관분석: 수량-총액 r=0.685 (중간 상관)
   ├─> 파레토: 상위 7개 상품이 매출의 84.6%
   └─> 성장률: 3월 +68.2% 최대 성장

5. CLI 출력 (ex27_09)
   └─> 월별/카테고리별/지역별 테이블 대시보드
```

### 통합 실행 예시

실제 대시보드를 실행한다면 다음과 같은 흐름이 됩니다:

```python
# dashboard.py (통합 실행)
from collectors.csv_loader import load_csv, inspect_data
from processors.cleaner import DataCleaner
from processors.transformer import add_derived_columns, aggregate
from analyzers.stats import calculate_basic_stats, group_stats
from analyzers.group import pareto_analysis, growth_analysis
from visualizers.table import Table, Color

def main():
    # 1. 데이터 로드
    data = load_csv("data/raw/sales.csv")
    inspect_data(data)

    # 2. 데이터 정제
    cleaner = DataCleaner(data)
    cleaner.detect_missing_values(["수량", "단가"])
    cleaner.detect_outliers("단가")
    cleaner.fix_missing_values("수량", strategy="median")
    cleaner.fix_duplicates()
    clean_data = cleaner.cleaned

    # 3. 데이터 변환
    transformed = add_derived_columns(clean_data)

    # 4. 분석
    cat_stats = group_stats(transformed, "카테고리", "총액")
    pareto = pareto_analysis(transformed, "상품명")

    # 5. 대시보드 출력
    table = Table(title="카테고리별 매출 현황")
    table.add_column("카테고리", width=10, align="center")
    table.add_column("건수", width=8)
    table.add_column("총매출", width=14)
    table.add_column("평균", width=12)

    for cat, stats in cat_stats.items():
        table.add_row(cat, stats["건수"], stats["합계"], stats["평균"])

    table.print()
```

---

## 27.9 바이브 코딩 회고

이 프로젝트를 통해 경험한 바이브 코딩의 핵심 패턴을 정리합니다.

### 효과적인 프롬프트 패턴

이 프로젝트에서 사용한 프롬프트의 공통 구조를 분석해봅시다:

| 요소 | 설명 | 예시 |
|------|------|------|
| **역할** | AI에게 기대하는 역할 | "데이터 정제 도구를 작성해줘" |
| **기능 목록** | 구체적인 기능 요구사항 | "1. 결측치 탐지 2. IQR 이상치 탐지 3. 중복 제거" |
| **기술 제약** | 사용할 기술과 제한 | "표준 라이브러리만, copy.deepcopy 사용" |
| **출력 형식** | 결과의 출력 형태 | "정제 결과 보고서 출력" |

### 단계적 개발의 장점

```
잘못된 방법: "데이터 대시보드 전체를 한 번에 만들어줘"
  --> AI가 전체를 한 번에 생성하면 수정이 어려움

올바른 방법: "Step 1: 프로젝트 구조부터 만들어줘"
  --> 단계별로 확인하며 진행하면 품질이 높아짐
```

각 단계에서 결과를 확인하고, 문제가 있으면 해당 부분만 수정 요청합니다. 이것이 바이브 코딩의 핵심인 **반복적(iterative) 개발**입니다.

### AI에게 추가 요청하기 좋은 것들

프로젝트를 더 발전시키고 싶다면 다음과 같이 요청해보세요:

```
"이 대시보드에 시계열 예측 기능을 추가해줘.
 지난 6개월 데이터로 다음 달 매출을 선형 회귀로 예측하고 싶어."

"대시보드 결과를 마크다운 보고서로 자동 저장하는 기능을 추가해줘."

"실시간으로 갱신되는 대시보드를 만들고 싶어.
 60초마다 데이터를 다시 로드하고 터미널을 clear한 뒤 다시 출력해줘."

"현재 텍스트 차트를 개선해서 막대 그래프와 꺾은선 그래프를
 터미널에 출력하는 기능을 추가해줘."
```

> **Tip:** 프로젝트가 완성된 후에도 AI와의 대화를 계속하면서 기능을 추가하는 것이 바이브 코딩의 매력입니다. "이 코드에 ~을 추가해줘"라고 요청하면 기존 코드와 자연스럽게 통합된 새 기능을 받을 수 있습니다.

---

## 27.10 정리

이번 프로젝트에서 배운 핵심 내용을 정리합니다.

### 기술 요약

| 단계 | 핵심 기술 | 사용한 모듈 |
|------|----------|------------|
| **구조 설정** | 디렉토리 생성, 파일 초기화 | `os`, `datetime` |
| **데이터 수집** | CSV 로드, API 패턴(캐싱/재시도) | `csv`, `json`, `hashlib`, `time` |
| **데이터 정제** | 결측치, 이상치(IQR), 중복 처리 | `copy`, `datetime` |
| **데이터 변환** | 파생 변수, 집계, 피벗 | `collections.defaultdict` |
| **통계 분석** | 기술 통계, 상관계수, 파레토 | `statistics`, `math`, `Counter` |
| **CLI 출력** | ANSI 색상, 유니코드 테이블 | `os` (터미널 감지) |

### 데이터 분석 개념 요약

```
수집 (Collection)
  CSV 파일, API, 데이터베이스 등에서 원본 데이터 확보

정제 (Cleaning)
  결측치, 이상치, 중복, 형식 오류를 탐지하고 처리
  "쓰레기가 들어가면 쓰레기가 나온다 (Garbage In, Garbage Out)"

변환 (Transformation)
  파생 변수 생성, 데이터 형식 변경, 집계/피벗

분석 (Analysis)
  기술 통계, 그룹별 비교, 상관관계, 추세 분석, 파레토 분석

시각화 (Visualization)
  테이블, 차트, 대시보드로 결과를 보기 쉽게 표현
```

### 프로젝트 확장 아이디어

이 프로젝트를 기반으로 더 발전시킬 수 있는 방향을 제시합니다:

1. **pandas 적용**: 이 프로젝트의 모든 기능을 pandas로 재구현하면 코드가 얼마나 간결해지는지 비교해보세요
2. **SQLite 연동**: CSV 대신 데이터베이스에서 데이터를 관리하면 대용량 처리가 가능합니다
3. **자동 보고서**: 분석 결과를 마크다운이나 HTML 보고서로 자동 생성
4. **스케줄링**: 매일 정해진 시간에 자동으로 데이터를 수집하고 보고서 생성
5. **웹 대시보드**: Flask나 Streamlit으로 웹 기반 대시보드로 확장

> **Tip:** 이 프로젝트에서 배운 데이터 분석 파이프라인(수집 -> 정제 -> 변환 -> 분석 -> 시각화)은 규모에 관계없이 모든 데이터 프로젝트에서 동일하게 적용됩니다. 작은 프로젝트에서 익힌 패턴이 큰 프로젝트의 기초가 됩니다.

---

### 다음 장에서는

Chapter 28에서는 **프로젝트 4 - 파일 동기화 도구**를 만들어봅니다. 파일 해시 비교, 변경 감지, 동기화 로직, 충돌 처리 등 시스템 프로그래밍의 핵심 개념을 바이브 코딩으로 구현합니다.
