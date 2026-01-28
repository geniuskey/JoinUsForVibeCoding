# Chapter 20: 복잡한 프로젝트 관리

프로그래밍 실력이 늘어나면 자연스럽게 프로젝트의 규모도 커집니다. 처음에는 하나의 파일에 모든 코드를 작성했지만, 코드가 수백 줄을 넘어가면 "어디에 뭐가 있는지 모르겠다", "수정하면 다른 곳이 깨진다" 같은 문제가 발생합니다. 이때 필요한 것이 바로 **프로젝트 관리** 기술입니다.

바이브 코딩에서 AI는 프로젝트 구조를 설계하고, 코드를 모듈로 분리하고, 의존성을 관리하는 데 탁월한 도우미입니다. "이 코드를 모듈로 분리해줘", "프로젝트 구조를 만들어줘"라고 요청하면 전문적인 구조를 즉시 얻을 수 있습니다. 하지만 AI가 만든 구조를 **이해하고 활용하는 능력**은 여러분의 몫입니다.

이번 장에서는 파이썬 프로젝트를 체계적으로 관리하는 방법을 단계별로 배워보겠습니다.

---

### 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 표준 파이썬 프로젝트 디렉토리 구조를 이해하고 생성하기
- 하나의 큰 파일을 역할별 모듈로 분리하기
- `__init__.py`의 역할을 이해하고 패키지를 만들기
- 상대 임포트와 절대 임포트의 차이를 구분하기
- `requirements.txt`로 프로젝트 의존성을 관리하기
- 가상환경(`venv`)을 생성하고 활용하기
- `configparser`와 환경 변수로 설정 파일을 관리하기
- AI에게 프로젝트 구조 설계를 효과적으로 요청하기

---

### 20.1 프로젝트 구조 설계

#### 왜 프로젝트 구조가 중요한가?

코드를 작성하기 시작할 때 가장 먼저 해야 할 일은 **디렉토리 구조를 설계하는 것**입니다. 좋은 프로젝트 구조는 마치 잘 정리된 서재와 같습니다. 어떤 책(코드)이 어디에 있는지 직관적으로 알 수 있고, 새로운 책을 추가할 자리도 명확합니다.

프로젝트 구조가 나쁘면 다음과 같은 문제가 발생합니다:

| 문제 상황 | 원인 |
|-----------|------|
| "이 함수가 어디에 있지?" | 파일 분류 기준이 없음 |
| "설정 파일을 어디에 놓지?" | 디렉토리 구조가 없음 |
| "테스트를 어떻게 실행하지?" | 테스트 코드가 소스 코드와 섞여 있음 |
| "다른 사람이 이 코드를 못 읽겠대" | 일관된 구조가 없음 |

#### 표준 파이썬 프로젝트 구조

파이썬 커뮤니티에서 널리 사용하는 표준 프로젝트 구조가 있습니다. AI에게 "파이썬 프로젝트 구조를 만들어줘"라고 요청하면 대부분 이 구조를 기반으로 생성합니다.

**예제 20-1: 표준 프로젝트 구조 생성 및 출력**

```python
# examples/python/chapter05/ex20_01_project_structure.py
import os
import tempfile
import shutil


def create_project_structure(base_path, project_name):
    """표준 파이썬 프로젝트 디렉토리 구조를 생성합니다."""
    # 프로젝트 구조 정의: (경로, 파일인지 여부, 파일 내용)
    structure = [
        # 최상위 파일들
        ("README.md", True, f"# {project_name}\n\n프로젝트 설명을 여기에 작성합니다.\n"),
        ("setup.py", True, f'from setuptools import setup\n\nsetup(name="{project_name}")\n'),
        ("pyproject.toml", True, '[build-system]\nrequires = ["setuptools"]\n'),
        ("requirements.txt", True, "# 프로젝트 의존성\n"),
        (".gitignore", True, "__pycache__/\n*.pyc\n.env\nvenv/\n"),

        # 소스 코드 패키지
        (f"src/{project_name}/__init__.py", True, f'"""패키지: {project_name}"""\n\n__version__ = "0.1.0"\n'),
        (f"src/{project_name}/main.py", True, '"""메인 모듈"""\n\ndef main():\n    print("Hello!")\n'),
        (f"src/{project_name}/utils.py", True, '"""유틸리티 함수 모음"""\n'),
        (f"src/{project_name}/config.py", True, '"""설정 관리"""\n'),

        # 테스트
        ("tests/__init__.py", True, ""),
        ("tests/test_main.py", True, '"""메인 모듈 테스트"""\n'),
        ("tests/test_utils.py", True, '"""유틸리티 테스트"""\n'),

        # 문서
        ("docs/index.md", True, "# 문서 홈\n"),
        ("docs/installation.md", True, "# 설치 방법\n"),

        # 기타 디렉토리
        ("data/", False, None),
        ("scripts/", False, None),
    ]

    project_root = os.path.join(base_path, project_name)

    for path, is_file, content in structure:
        full_path = os.path.join(project_root, path)

        if is_file:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            os.makedirs(full_path, exist_ok=True)

    return project_root
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_01_project_structure.py
```

**결과:**

```
============================================================
예제 20-01: 표준 프로젝트 구조 생성 및 출력
============================================================

프로젝트 'my_awesome_app' 구조를 생성합니다...

------------------------------------------------------------
프로젝트 디렉토리 구조:
------------------------------------------------------------
my_awesome_app/
├── data/
├── docs/
│   ├── index.md
│   └── installation.md
├── scripts/
├── src/
│   └── my_awesome_app/
│       ├── __init__.py
│       ├── config.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
└── setup.py

------------------------------------------------------------
구조 요약: 7개 디렉토리, 12개 파일
------------------------------------------------------------

각 디렉토리의 역할:
  src/my_awesome_app/       → 핵심 소스 코드가 위치하는 패키지 디렉토리
  tests/                    → 테스트 코드 모음
  docs/                     → 프로젝트 문서
  data/                     → 데이터 파일 저장소
  scripts/                  → 유틸리티 스크립트 모음

프로젝트 구조가 성공적으로 생성되었습니다!
(임시 디렉토리 정리 완료)
```

#### 각 디렉토리와 파일의 역할

위 구조에서 각 요소가 하는 일을 하나씩 살펴보겠습니다.

**최상위 파일들:**

| 파일 | 역할 |
|------|------|
| `README.md` | 프로젝트 소개, 설치 방법, 사용법 등을 설명하는 문서 |
| `setup.py` | 패키지 설치를 위한 전통적 설정 파일 |
| `pyproject.toml` | 현대적 프로젝트 설정 파일 (PEP 621 표준) |
| `requirements.txt` | 프로젝트가 사용하는 외부 라이브러리 목록 |
| `.gitignore` | Git이 추적하지 않을 파일 패턴 |

**디렉토리:**

| 디렉토리 | 역할 |
|----------|------|
| `src/프로젝트명/` | 핵심 소스 코드. `__init__.py`가 있어 패키지로 동작 |
| `tests/` | 테스트 코드. 소스 코드와 분리하여 관리 |
| `docs/` | 프로젝트 문서 (API 문서, 사용 가이드 등) |
| `data/` | 데이터 파일 (CSV, JSON 등) |
| `scripts/` | 빌드, 배포 등 유틸리티 스크립트 |

> **Tip:** AI에게 프로젝트 구조를 요청할 때는 "파이썬 표준 프로젝트 구조로 `my_project`를 만들어줘. `src/` 레이아웃을 사용하고, 테스트와 문서 디렉토리도 포함해줘"처럼 구체적으로 요청하면 더 정확한 결과를 얻을 수 있습니다.

#### `src/` 레이아웃 vs 플랫 레이아웃

파이썬 프로젝트에는 두 가지 주요 레이아웃이 있습니다:

```
# src/ 레이아웃 (권장)              # 플랫 레이아웃
my_project/                          my_project/
├── src/                             ├── my_project/
│   └── my_project/                  │   ├── __init__.py
│       ├── __init__.py              │   └── main.py
│       └── main.py                  ├── tests/
├── tests/                           └── setup.py
└── setup.py
```

`src/` 레이아웃이 권장되는 이유는:

1. **설치된 패키지와 소스 코드가 명확히 분리**됩니다
2. 테스트 시 실수로 로컬 소스를 임포트하는 것을 방지합니다
3. 패키지를 배포할 때 더 깔끔합니다

> **Note:** 소규모 프로젝트나 학습 목적이라면 플랫 레이아웃도 충분합니다. 프로젝트 규모가 커지면 `src/` 레이아웃으로 전환하는 것을 권장합니다.

---

### 20.2 모듈화와 코드 분리

#### 왜 모듈화가 필요한가?

하나의 파일에 모든 코드를 넣으면 처음에는 편하지만, 코드가 길어질수록 다음과 같은 문제가 생깁니다:

- **찾기 어려움**: 500줄짜리 파일에서 특정 함수를 찾으려면 스크롤을 한참 해야 합니다
- **충돌 발생**: 여러 사람이 같은 파일을 동시에 수정하면 Git 충돌이 빈번합니다
- **테스트 어려움**: 특정 기능만 테스트하고 싶어도 전체 파일을 로드해야 합니다
- **재사용 불가**: 한 파일의 함수를 다른 프로젝트에서 쓰기 어렵습니다

**모듈화**란 하나의 큰 파일을 **역할별로 여러 파일로 분리**하는 것입니다. 각 파일(모듈)은 하나의 명확한 책임을 가집니다.

#### 분리 전 vs 분리 후 비교

**예제 20-2: 모듈 분리 예시**

사용자 관리 프로그램을 예로 들어, 모든 코드가 한 파일에 있는 경우와 역할별로 분리한 경우를 비교합니다.

```python
# examples/python/chapter05/ex20_02_module_separation.py

# ============================================================
# [분리 전] 모든 것이 한 파일에 섞여 있는 코드
# ============================================================

# app.py - 모든 것이 한 파일에!

users = []  # 전역 변수

def register(name, email, age):
    # 검증 로직
    if not name or len(name) < 2:
        return "이름은 2자 이상이어야 합니다"
    if "@" not in email:
        return "올바른 이메일 형식이 아닙니다"
    if age < 0 or age > 150:
        return "올바른 나이를 입력하세요"

    # 비즈니스 로직
    user = {"name": name, "email": email, "age": age}
    users.append(user)

    # 출력 로직
    print(f"가입 완료: {name} ({email})")
    return user
```

이 코드의 문제점은 **검증, 비즈니스 로직, 출력이 모두 하나의 함수에 섞여 있다**는 것입니다. 검증 규칙만 테스트하고 싶어도 전체 등록 과정을 실행해야 합니다.

분리 후에는 각 역할을 담당하는 독립적인 클래스로 나눕니다:

```python
# --- validators.py 역할 ---
class Validators:
    """입력값 검증을 담당하는 모듈"""

    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            return False, "이름은 비어있을 수 없습니다"
        if len(name) < 2:
            return False, "이름은 2자 이상이어야 합니다"
        return True, "유효한 이름입니다"

    @staticmethod
    def validate_email(email):
        if not email or "@" not in email:
            return False, "올바른 이메일 형식이 아닙니다"
        if "." not in email.split("@")[1]:
            return False, "이메일 도메인이 올바르지 않습니다"
        return True, "유효한 이메일입니다"

    @staticmethod
    def validate_age(age):
        if not isinstance(age, int):
            return False, "나이는 정수여야 합니다"
        if age < 0 or age > 150:
            return False, "나이는 0~150 사이여야 합니다"
        return True, "유효한 나이입니다"


# --- models.py 역할 ---
class User:
    """사용자 데이터 모델"""

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    @property
    def category(self):
        if self.age < 19:
            return "미성년자"
        elif self.age < 65:
            return "성인"
        else:
            return "시니어"


# --- services.py 역할 ---
class UserService:
    """사용자 관련 비즈니스 로직"""

    def __init__(self):
        self._users = []

    def register(self, name, email, age):
        for validator, value in [
            (Validators.validate_name, name),
            (Validators.validate_email, email),
            (Validators.validate_age, age),
        ]:
            is_valid, message = validator(value)
            if not is_valid:
                return None, message

        user = User(name, email, age)
        self._users.append(user)
        return user, "등록 성공"


# --- formatters.py 역할 ---
class UserFormatter:
    """사용자 정보 출력 포맷 담당"""

    @staticmethod
    def format_user(user):
        return f"{user.name} ({user.email}) [{user.category}]"
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_02_module_separation.py
```

**결과:**

```
============================================================
[분리 전] 모든 코드가 한 파일에 있는 경우
============================================================

    # app.py - 모든 것이 한 파일에!
    ...
  문제점: 검증, 비즈니스 로직, 출력이 모두 섞여 있음
         테스트하기 어렵고, 수정 시 다른 부분에 영향을 줌

============================================================
[분리 후] 역할별로 모듈을 나눈 경우
============================================================

모듈 구조:
  validators.py        → 입력값 검증 (이름, 이메일, 나이)
  models.py            → 데이터 모델 정의 (User 클래스)
  services.py          → 비즈니스 로직 (등록, 검색)
  formatters.py        → 출력 포맷 담당

  장점:
    1. 각 모듈의 역할이 명확함
    2. 독립적으로 테스트 가능
    3. 수정 시 영향 범위가 제한됨
    4. 코드 재사용이 쉬움

============================================================
분리된 모듈 사용 데모
============================================================

--- 사용자 등록 테스트 ---
  성공: 김바이브 (vibe@example.com) [성인]
  성공: 이코딩 (coding@test.co.kr) [미성년자]
  성공: 박파이썬 (python@dev.io) [성인]
  실패: 이름은 비어있을 수 없습니다 ('', 'bad@email.com', 25)
  실패: 올바른 이메일 형식이 아닙니다 ('홍길동', 'no-at-sign', 25)
  실패: 나이는 0~150 사이여야 합니다 ('최개발', 'dev@good.com', -5)

--- 등록된 사용자 목록 ---
총 3명의 사용자:
  - 김바이브 (vibe@example.com) [성인]
  - 이코딩 (coding@test.co.kr) [미성년자]
  - 박파이썬 (python@dev.io) [성인]

모듈 분리 예시를 성공적으로 실행했습니다!
```

#### 모듈 분리의 원칙

코드를 모듈로 분리할 때 다음 원칙을 따릅니다:

**1. 단일 책임 원칙 (Single Responsibility Principle)**

각 모듈은 하나의 역할만 담당합니다.

```
validators.py  → 입력값 검증만
models.py      → 데이터 구조 정의만
services.py    → 비즈니스 로직만
formatters.py  → 출력 포맷만
```

**2. 높은 응집도, 낮은 결합도**

- **높은 응집도**: 관련된 기능은 같은 모듈에 모읍니다
- **낮은 결합도**: 모듈 간 의존성을 최소화합니다

**3. AI에게 모듈 분리를 요청하는 프롬프트**

```
이 파일이 너무 커졌어. 다음 기준으로 모듈을 분리해줘:
1. 데이터 검증 함수 → validators.py
2. 데이터 모델 클래스 → models.py
3. 비즈니스 로직 → services.py
4. 출력/포맷 함수 → formatters.py
각 모듈이 독립적으로 import될 수 있도록 만들어줘.
```

> **Tip:** 모듈을 분리할 때 "이 모듈만 따로 테스트할 수 있는가?"를 기준으로 삼으세요. 독립적으로 테스트할 수 없다면 다른 모듈과의 결합도가 너무 높은 것입니다.

---

### 20.3 패키지 만들기: `__init__.py` 이해하기

#### 모듈과 패키지의 차이

파이썬에서 **모듈**은 하나의 `.py` 파일이고, **패키지**는 여러 모듈을 담고 있는 **디렉토리**입니다. 디렉토리가 패키지로 인식되려면 `__init__.py` 파일이 필요합니다.

```
# 모듈: 하나의 파일
utils.py            → import utils

# 패키지: __init__.py가 있는 디렉토리
mathtools/
├── __init__.py     → import mathtools
├── basic.py        → import mathtools.basic
└── advanced.py     → import mathtools.advanced
```

#### `__init__.py`의 네 가지 역할

`__init__.py`는 단순히 "이 디렉토리가 패키지다"라고 알려주는 것 이상의 역할을 합니다.

**예제 20-3: 패키지 만들기**

`mathtools`라는 수학 유틸리티 패키지를 만들어서 `__init__.py`의 역할을 실습합니다.

```python
# examples/python/chapter05/ex20_03_package_creation.py

# --- __init__.py 내용 ---
"""
mathtools 패키지
수학 관련 유틸리티 함수 모음입니다.
"""

__version__ = "1.0.0"
__author__ = "바이브 코더"

# 패키지에서 자주 사용하는 함수를 바로 임포트할 수 있게 설정
from .basic import add, subtract, multiply, divide
from .advanced import power, factorial, fibonacci

# 패키지 수준에서 공개할 이름 목록
__all__ = [
    "add", "subtract", "multiply", "divide",
    "power", "factorial", "fibonacci",
]

def info():
    """패키지 정보를 출력합니다."""
    print(f"mathtools v{__version__} by {__author__}")
    print(f"사용 가능한 함수: {', '.join(__all__)}")
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_03_package_creation.py
```

**결과:**

```
============================================================
예제 20-03: 패키지 만들기
============================================================

--- 생성된 패키지 구조 ---
mathtools/
    ├── stats/
    │       ├── __init__.py
    │       └── descriptive.py
    ├── __init__.py
    ├── advanced.py
    └── basic.py

--- __init__.py의 역할 ---
  1. 디렉토리를 파이썬 패키지로 인식하게 합니다
  2. 패키지 임포트 시 자동 실행되는 초기화 코드를 담습니다
  3. __all__ 변수로 공개 API를 정의합니다
  4. 하위 모듈의 함수를 패키지 수준에서 재노출(re-export)합니다

--- 패키지 임포트 시뮬레이션 ---

import mathtools
  mathtools.__version__ = '1.0.0'
  mathtools.__author__ = '바이브 코더'

mathtools.info() 호출:
  mathtools v1.0.0 by 바이브 코더
  사용 가능한 함수: add, subtract, multiply, divide, power, factorial, fibonacci

--- 기본 연산 (basic 모듈) ---
  mathtools.add(10, 3) = 13
  mathtools.subtract(10, 3) = 7
  mathtools.multiply(10, 3) = 30
  mathtools.divide(10, 3) = 3.3333

--- 고급 연산 (advanced 모듈) ---
  mathtools.power(2, 10) = 1024
  mathtools.factorial(5) = 120
  mathtools.fibonacci(10) = 55

--- 통계 서브패키지 (stats) ---
  데이터: [4, 8, 15, 16, 23, 42]
  mean([4, 8, 15, 16, 23, 42]) = 18.00
  median([4, 8, 15, 16, 23, 42]) = 15.5

--- 다양한 임포트 방식 ---
  import mathtools              # 패키지 전체 임포트
  from mathtools import add     # 특정 함수만 임포트
  from mathtools.basic import * # 모듈의 모든 함수 임포트
  from mathtools.stats import mean  # 서브패키지에서 임포트

패키지 만들기 예제를 성공적으로 실행했습니다!
(임시 디렉토리 정리 완료)
```

#### `__init__.py`의 역할 상세 설명

**역할 1: 패키지 인식 표시**

`__init__.py`가 있으면 파이썬이 해당 디렉토리를 패키지로 인식합니다. 파이썬 3.3 이상에서는 `__init__.py` 없이도 **네임스페이스 패키지**로 동작하지만, 명시적으로 만드는 것이 좋은 관행입니다.

**역할 2: 초기화 코드 실행**

`import mathtools`를 실행하면 `mathtools/__init__.py`가 자동으로 실행됩니다. 여기에 패키지 버전 정보, 초기 설정 등을 넣을 수 있습니다.

```python
# __init__.py
__version__ = "1.0.0"
__author__ = "바이브 코더"
```

**역할 3: 공개 API 정의 (`__all__`)**

`__all__` 변수는 `from mathtools import *`를 실행했을 때 어떤 이름이 임포트되는지를 결정합니다.

```python
__all__ = ["add", "subtract", "multiply", "divide"]
```

**역할 4: 편의 임포트 제공 (re-export)**

`__init__.py`에서 하위 모듈의 함수를 미리 임포트해두면, 사용자가 더 간결하게 사용할 수 있습니다.

```python
# __init__.py에서 re-export
from .basic import add, subtract

# 사용자는 이렇게 간결하게 사용 가능:
from mathtools import add    # mathtools.basic.add 대신
```

> **Note:** 빈 `__init__.py` 파일도 유효합니다. 패키지로 인식만 하면 되고 초기화 코드가 필요 없다면 빈 파일로 두면 됩니다. 실제로 `tests/__init__.py`는 대부분 비어 있습니다.

#### 서브패키지 구조

패키지 안에 또 다른 패키지를 넣을 수 있습니다. 이를 **서브패키지**라고 합니다.

```
mathtools/
├── __init__.py
├── basic.py
├── advanced.py
└── stats/              # 서브패키지
    ├── __init__.py
    └── descriptive.py
```

서브패키지를 임포트하는 방법:

```python
# 방법 1: 서브패키지에서 직접 임포트
from mathtools.stats import mean, median

# 방법 2: 서브패키지를 임포트한 뒤 사용
from mathtools import stats
result = stats.mean([1, 2, 3])

# 방법 3: 전체 경로로 접근
import mathtools.stats.descriptive
result = mathtools.stats.descriptive.mean([1, 2, 3])
```

---

### 20.4 상대 임포트와 절대 임포트

패키지 안에서 다른 모듈을 임포트할 때, **절대 임포트**와 **상대 임포트** 두 가지 방식을 사용할 수 있습니다.

#### 절대 임포트 (Absolute Import)

패키지의 최상위부터 전체 경로를 지정하는 방식입니다:

```python
# mathtools/advanced.py에서 basic 모듈 사용
from mathtools.basic import add        # 절대 경로
```

#### 상대 임포트 (Relative Import)

현재 모듈의 위치를 기준으로 상대적인 경로를 지정하는 방식입니다:

```python
# mathtools/advanced.py에서 basic 모듈 사용
from .basic import add                 # 같은 패키지의 basic 모듈
from ..utils import helper             # 상위 패키지의 utils 모듈
```

상대 임포트에서 사용하는 점(`.`)의 의미:

| 표기 | 의미 |
|------|------|
| `.` | 현재 패키지 (같은 디렉토리) |
| `..` | 부모 패키지 (상위 디렉토리) |
| `...` | 부모의 부모 패키지 (2단계 상위) |

#### 어떤 방식을 사용해야 할까?

| 상황 | 권장 방식 |
|------|-----------|
| 패키지 내부에서 같은 패키지 모듈 임포트 | 상대 임포트 (`from .basic import add`) |
| 외부 패키지나 표준 라이브러리 임포트 | 절대 임포트 (`import os`) |
| 프로젝트 최상위 스크립트에서 임포트 | 절대 임포트 |

```python
# mathtools/__init__.py 에서의 임포트 예시

# 같은 패키지의 모듈 → 상대 임포트 사용
from .basic import add, subtract, multiply, divide
from .advanced import power, factorial, fibonacci

# 외부 라이브러리 → 절대 임포트 사용
import os
import json
```

> **Warning:** 상대 임포트는 패키지 안에서만 사용할 수 있습니다. 최상위 스크립트(직접 실행하는 파일)에서는 상대 임포트를 사용할 수 없습니다. `python basic.py`처럼 직접 실행하는 파일에서 `from .advanced import power`를 사용하면 `ImportError`가 발생합니다.

---

### 20.5 의존성 관리: requirements.txt

#### 의존성이란?

프로젝트가 사용하는 외부 라이브러리를 **의존성(dependency)**이라고 합니다. 예를 들어 웹 서버를 만들 때 `flask`를 사용하고, 데이터베이스 연결에 `sqlalchemy`를 사용한다면, 이 두 라이브러리가 프로젝트의 의존성입니다.

의존성을 관리하지 않으면 다음과 같은 문제가 발생합니다:

- "내 컴퓨터에서는 되는데 다른 컴퓨터에서는 안 돼요" -- 필요한 라이브러리가 설치되지 않았기 때문
- "어제까지 잘 됐는데 오늘 갑자기 안 돼요" -- 라이브러리가 업데이트되면서 호환성이 깨졌기 때문

이를 해결하는 것이 `requirements.txt` 파일입니다.

**예제 20-4: requirements.txt 생성 및 파싱**

```python
# examples/python/chapter05/ex20_04_requirements_txt.py

def create_requirements_file(filepath, packages):
    """requirements.txt 파일을 생성합니다."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 프로젝트 의존성 목록\n")
        f.write("# pip install -r requirements.txt 명령으로 설치합니다\n\n")
        for pkg in packages:
            if "comment" in pkg:
                f.write(f"\n# {pkg['comment']}\n")
            f.write(f"{pkg['line']}\n")


def parse_requirements(filepath):
    """requirements.txt 파일을 파싱하여 패키지 정보를 추출합니다."""
    packages = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 패키지 이름과 버전 조건 파싱
            # ...
            packages.append({"name": name, "operator": op, "version": ver})
    return packages
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_04_requirements_txt.py
```

**결과:**

```
============================================================
예제 20-04: requirements.txt 생성 및 파싱
============================================================

--- 1단계: requirements.txt 생성 ---

  파일 생성 완료: requirements.txt

  생성된 파일 내용:
  ---------------------------------------------
  # 프로젝트 의존성 목록
  # pip install -r requirements.txt 명령으로 설치합니다

  # 웹 프레임워크
  flask==2.3.3
  flask-cors>=4.0.0

  # 데이터베이스 ORM
  sqlalchemy~=2.0.20
  alembic>=1.11.0

  # 데이터 검증
  pydantic==2.3.0

  # 환경 변수 관리
  python-dotenv>=1.0.0

  # HTTP 클라이언트
  requests>=2.31.0

  # 비동기 작업 큐
  celery>=5.3.0
  redis>=5.0.0

  # WSGI 서버 (배포용)
  gunicorn>=21.2.0
  ---------------------------------------------

--- 2단계: requirements.txt 파싱 ---

  파싱된 패키지 목록 (10개):
  패키지명             조건  버전         원본
  -------------------- ----- ------------ -------------------------
  flask                ==    2.3.3        flask==2.3.3
  flask-cors           >=    4.0.0        flask-cors>=4.0.0
  sqlalchemy           ~=    2.0.20       sqlalchemy~=2.0.20
  ...

--- 3단계: 의존성 분석 ---

  총 패키지 수: 10개
  버전 고정 (==): 2개  - 정확한 버전으로 재현 가능
  최소 버전 (>=): 6개  - 최소 호환 버전 보장
  호환 버전 (~=): 1개  - 마이너 버전 업데이트 허용
  버전 미지정:    0개  - 최신 버전 설치

--- 4단계: requirements-dev.txt 생성 ---

  개발용 의존성 파일 생성 완료: requirements-dev.txt

--- requirements.txt 활용 가이드 ---

  설치: pip install -r requirements.txt
  개발: pip install -r requirements-dev.txt
  생성: pip freeze > requirements.txt
  확인: pip list

requirements.txt 예제를 성공적으로 실행했습니다!
(임시 파일 정리 완료)
```

#### 버전 지정 방식 이해하기

`requirements.txt`에서 버전을 지정하는 다양한 방식이 있습니다:

| 표기 | 의미 | 예시 | 설명 |
|------|------|------|------|
| `==` | 정확한 버전 | `flask==2.3.3` | 이 버전만 설치 |
| `>=` | 최소 버전 | `requests>=2.31.0` | 2.31.0 이상 설치 |
| `<=` | 최대 버전 | `numpy<=1.25.0` | 1.25.0 이하 설치 |
| `~=` | 호환 버전 | `sqlalchemy~=2.0.20` | 2.0.x 범위 내 최신 버전 |
| `!=` | 제외 버전 | `django!=4.1.0` | 이 버전 제외 |
| (없음) | 최신 버전 | `beautifulsoup4` | 가장 최신 버전 설치 |

> **Tip:** **개발 환경**에서는 `>=`로 유연하게 관리하고, **배포 환경**에서는 `==`로 정확한 버전을 고정하는 것이 좋습니다. `pip freeze > requirements.txt` 명령으로 현재 설치된 모든 패키지의 정확한 버전을 기록할 수 있습니다.

#### 개발용 의존성 분리

프로덕션에서는 필요 없지만 개발 시에는 필요한 라이브러리가 있습니다 (예: 테스트 프레임워크, 코드 포맷터). 이런 것들은 별도 파일로 분리합니다.

```
# requirements.txt -- 프로덕션 의존성
flask==2.3.3
sqlalchemy~=2.0.20
requests>=2.31.0

# requirements-dev.txt -- 개발 의존성
-r requirements.txt    # 기본 의존성 포함
pytest>=7.4.0          # 테스트
pytest-cov>=4.1.0      # 테스트 커버리지
black==23.7.0          # 코드 포맷터
flake8>=6.0.0          # 린터
mypy>=1.5.0            # 타입 검사
```

`-r requirements.txt` 줄은 "requirements.txt에 있는 모든 패키지도 함께 설치하라"는 뜻입니다.

```bash
# 프로덕션 환경
$ pip install -r requirements.txt

# 개발 환경
$ pip install -r requirements-dev.txt
```

---

### 20.6 가상환경 활용

#### 왜 가상환경이 필요한가?

파이썬에서 `pip install`로 패키지를 설치하면 기본적으로 **시스템 전체**에 설치됩니다. 이때 문제가 발생합니다:

```
프로젝트 A: flask==2.3.3 필요
프로젝트 B: flask==3.0.0 필요
→ 하나만 설치할 수 있으므로 둘 중 하나는 동작하지 않음!
```

**가상환경(Virtual Environment)**은 프로젝트마다 독립적인 파이썬 환경을 만들어, 각 프로젝트가 서로 다른 버전의 패키지를 사용할 수 있게 해줍니다.

#### 가상환경 생성 및 사용

```bash
# 1. 가상환경 생성
$ python -m venv venv

# 2. 가상환경 활성화
#    macOS/Linux:
$ source venv/bin/activate

#    Windows:
> venv\Scripts\activate

# 3. 활성화 확인 (프롬프트가 변경됨)
(venv) $ python --version
Python 3.11.5

# 4. 패키지 설치 (가상환경 내에서만 설치됨)
(venv) $ pip install flask==2.3.3
(venv) $ pip install -r requirements.txt

# 5. 설치된 패키지 확인
(venv) $ pip list

# 6. 현재 환경을 requirements.txt로 저장
(venv) $ pip freeze > requirements.txt

# 7. 가상환경 비활성화
(venv) $ deactivate
```

#### 가상환경 사용 워크플로우

새 프로젝트를 시작할 때의 전체 워크플로우는 다음과 같습니다:

```bash
# 1. 프로젝트 디렉토리 생성
$ mkdir my_project && cd my_project

# 2. Git 초기화
$ git init

# 3. 가상환경 생성
$ python -m venv venv

# 4. .gitignore에 가상환경 디렉토리 추가
$ echo "venv/" >> .gitignore

# 5. 가상환경 활성화
$ source venv/bin/activate

# 6. 필요한 패키지 설치
(venv) $ pip install flask requests

# 7. 의존성 기록
(venv) $ pip freeze > requirements.txt

# 8. 코드 작성 시작!
```

> **Warning:** 가상환경 디렉토리(`venv/`)는 절대 Git에 커밋하지 마세요. `.gitignore`에 `venv/`를 반드시 추가해야 합니다. 가상환경은 각자의 컴퓨터에서 `requirements.txt`를 기반으로 다시 생성하면 됩니다.

#### 다른 사람의 프로젝트를 받았을 때

```bash
# 1. 프로젝트 클론
$ git clone https://github.com/user/project.git
$ cd project

# 2. 가상환경 생성
$ python -m venv venv
$ source venv/bin/activate

# 3. 의존성 설치
(venv) $ pip install -r requirements.txt

# 4. 실행!
(venv) $ python main.py
```

이것이 `requirements.txt`가 중요한 이유입니다. 가상환경 자체는 공유하지 않지만, `requirements.txt`만 있으면 누구든 동일한 환경을 재현할 수 있습니다.

> **Tip:** AI에게 "이 프로젝트를 다른 사람이 쉽게 시작할 수 있도록 README에 설치 가이드를 추가해줘"라고 요청하면, 가상환경 생성부터 의존성 설치까지 단계별 안내 문서를 작성해 줍니다.

---

### 20.7 설정 파일 관리

#### 왜 설정을 코드에서 분리해야 하는가?

프로그램에서 데이터베이스 주소, 포트 번호, 비밀 키 같은 값을 코드에 직접 작성하면 문제가 생깁니다:

```python
# 나쁜 예: 설정값이 코드에 직접 들어 있음
db_url = "sqlite:///dev.db"        # 개발 환경
# db_url = "postgresql://..."      # 운영 환경 (주석 처리?!)
secret_key = "my-super-secret"     # 비밀 키가 코드에 노출!
```

이런 방식의 문제점:

- 환경을 바꿀 때마다 코드를 수정해야 합니다
- 비밀 정보가 Git에 노출됩니다
- 코드와 설정이 섞여서 관리가 어렵습니다

해결책은 **설정을 별도 파일로 분리**하는 것입니다.

#### configparser로 설정 파일 관리하기

**예제 20-5: 설정 파일 관리 (configparser)**

파이썬 표준 라이브러리인 `configparser`를 사용하면 INI 형식의 설정 파일을 쉽게 읽고 쓸 수 있습니다.

```python
# examples/python/chapter05/ex20_05_config_manager.py
import configparser
import os


def create_config(filepath):
    """기본 설정 파일(config.ini)을 생성합니다."""
    config = configparser.ConfigParser()

    # 기본 섹션 설정
    config["DEFAULT"] = {
        "debug": "false",
        "log_level": "INFO",
        "encoding": "utf-8",
    }

    # 앱 설정
    config["app"] = {
        "name": "바이브코딩앱",
        "version": "1.0.0",
        "port": "8000",
        "host": "localhost",
    }

    # 데이터베이스 설정
    config["database"] = {
        "engine": "sqlite",
        "name": "app.db",
        "pool_size": "5",
        "timeout": "30",
    }

    # 보안 설정
    config["security"] = {
        "session_timeout": "3600",
        "max_login_attempts": "5",
        "password_min_length": "8",
    }

    with open(filepath, "w", encoding="utf-8") as f:
        config.write(f)
    return config


class ConfigManager:
    """설정 파일을 관리하는 클래스입니다."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        if os.path.exists(filepath):
            self.config.read(filepath, encoding="utf-8")

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=0):
        return self.config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        return self.config.getboolean(section, key, fallback=fallback)

    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = str(value)

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            self.config.write(f)
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_05_config_manager.py
```

**결과:**

```
============================================================
예제 20-05: 설정 파일 관리 (configparser)
============================================================

--- 1단계: 설정 파일 생성 ---
  설정 파일이 생성되었습니다: config.ini

--- 2단계: 설정 파일 읽기 ---

  [app]
    name = 바이브코딩앱
    version = 1.0.0
    port = 8000
    host = localhost
    debug = false (기본값)
    log_level = INFO (기본값)
    encoding = utf-8 (기본값)

  [database]
    engine = sqlite
    name = app.db
    pool_size = 5
    timeout = 30
    ...

--- 3단계: 다양한 타입으로 읽기 ---

  문자열: app.name = '바이브코딩앱'
  정수:   database.pool_size = 5
  불리언: DEFAULT.debug = False
  기본값: app.없는키 = '기본값'

--- 4단계: 설정값 수정 ---

  app.port: '8000' -> '9000'
  app.debug: 'false' -> 'true'
  database.pool_size: '5' -> '10'
  새 섹션 [cache] 추가됨

  변경사항이 저장되었습니다.

--- 5단계: 변경된 설정 확인 ---

  app.port = 9000
  app.debug = True
  database.pool_size = 10
  cache.backend = memory
  cache.ttl = 300
  cache 섹션 존재: True

설정 파일 관리 예제를 성공적으로 실행했습니다!
(임시 파일 정리 완료)
```

#### config.ini 파일의 구조

```ini
# config.ini
[DEFAULT]
debug = false
log_level = INFO

[app]
name = 바이브코딩앱
version = 1.0.0
port = 8000

[database]
engine = sqlite
name = app.db
pool_size = 5
```

핵심 요소:

- **`[섹션명]`**: 설정을 그룹으로 분류합니다
- **`키 = 값`**: 설정값을 저장합니다
- **`[DEFAULT]`**: 모든 섹션에 공통으로 적용되는 기본값입니다
- **`#`으로 시작하는 줄**: 주석입니다

> **Note:** `configparser`는 모든 값을 **문자열**로 저장합니다. 정수, 불리언 등으로 읽으려면 `getint()`, `getboolean()` 등의 메서드를 사용해야 합니다. `getboolean()`은 `"true"`, `"yes"`, `"1"`, `"on"`을 `True`로, `"false"`, `"no"`, `"0"`, `"off"`를 `False`로 인식합니다.

---

### 20.8 환경별 설정 관리

실제 프로젝트에서는 **개발(development)**, **테스트(testing)**, **운영(production)** 등 여러 환경에서 같은 코드를 실행합니다. 각 환경마다 데이터베이스 주소, 디버그 모드, 포트 번호 등이 다릅니다.

**예제 20-6: 환경별 설정 관리**

클래스 상속을 사용하여 환경별 설정을 관리하는 패턴입니다.

```python
# examples/python/chapter05/ex20_06_env_config.py

class BaseConfig:
    """모든 환경에 공통인 기본 설정"""
    APP_NAME = "바이브코딩앱"
    APP_VERSION = "1.0.0"
    ENCODING = "utf-8"


class DevelopmentConfig(BaseConfig):
    """개발 환경 설정"""
    ENV_NAME = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///dev.db"
    PORT = 5000


class TestingConfig(BaseConfig):
    """테스트 환경 설정"""
    ENV_NAME = "testing"
    DEBUG = True
    LOG_LEVEL = "WARNING"
    DATABASE_URL = "sqlite:///test.db"
    PORT = 5001


class ProductionConfig(BaseConfig):
    """운영 환경 설정"""
    ENV_NAME = "production"
    DEBUG = False
    LOG_LEVEL = "ERROR"
    DATABASE_URL = "postgresql://user:pass@db-server:5432/prod_db"
    PORT = 8000


# 환경 이름으로 설정 클래스를 가져오는 매핑
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(env_name=None):
    """환경 이름에 맞는 설정 객체를 반환합니다."""
    if env_name is None:
        env_name = os.environ.get("APP_ENV", "development")
    config_class = CONFIG_MAP.get(env_name)
    if config_class is None:
        raise ValueError(f"알 수 없는 환경: '{env_name}'")
    return config_class()
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_06_env_config.py
```

**결과:**

```
============================================================
예제 20-06: 환경별 설정 관리
============================================================

--- 1단계: 클래스 기반 환경 설정 ---

  [development]
    DEBUG       = True
    LOG_LEVEL   = DEBUG
    DATABASE_URL= sqlite:///dev.db
    HOST:PORT   = localhost:5000
    RELOAD      = True
    CACHE       = False

  [testing]
    DEBUG       = True
    LOG_LEVEL   = WARNING
    DATABASE_URL= sqlite:///test.db
    HOST:PORT   = localhost:5001
    RELOAD      = False
    CACHE       = False

  [production]
    DEBUG       = False
    LOG_LEVEL   = ERROR
    DATABASE_URL= postgresql://user:pass@db-server:5432/prod_db
    HOST:PORT   = 0.0.0.0:8000
    RELOAD      = False
    CACHE       = True

--- 2단계: 환경 변수로 설정 전환 ---

  APP_ENV=development -> development 설정 로드됨
    DEBUG=True, PORT=5000
  APP_ENV=production -> production 설정 로드됨
    DEBUG=False, PORT=8000

--- 3단계: .env 파일 관리 ---

  파일: .env
  ----------------------------------------
    APP_NAME=바이브코딩앱
    APP_ENV=development
    APP_DEBUG=true
    APP_PORT=5000
    DATABASE_URL=sqlite:///dev.db
    SECRET_KEY="dev-secret-key-not-for-production"

환경별 설정 관리 예제를 성공적으로 실행했습니다!
(환경 변수 복구 및 임시 파일 정리 완료)
```

#### .env 파일과 환경 변수

운영 환경에서는 비밀번호 같은 민감한 정보를 `.env` 파일이나 환경 변수로 관리합니다.

```bash
# .env 파일 (절대 Git에 커밋하지 마세요!)
APP_NAME=바이브코딩앱
APP_ENV=development
APP_DEBUG=true
APP_PORT=5000
DATABASE_URL=sqlite:///dev.db
SECRET_KEY="dev-secret-key-not-for-production"
```

`.env` 파일 대신 `.env.example` 파일을 만들어 필요한 환경 변수를 문서화합니다:

```bash
# .env.example (Git에 커밋 가능)
APP_NAME=앱이름
APP_ENV=development
APP_DEBUG=true
APP_PORT=5000
DATABASE_URL=sqlite:///dev.db
SECRET_KEY=변경해주세요
```

#### 환경 설정 관리 모범 사례

예제 20-6에서 다루는 환경 설정 관리의 핵심 원칙을 정리합니다:

1. **`.env` 파일은 `.gitignore`에 추가하세요** -- 비밀 정보가 Git에 올라가면 안 됩니다
2. **`.env.example` 파일로 필요한 변수를 문서화하세요** -- 새로운 팀원이 어떤 환경 변수가 필요한지 알 수 있습니다
3. **운영 환경 비밀 정보는 환경 변수로 주입하세요** -- 클라우드 서비스나 CI/CD 도구에서 안전하게 관리합니다
4. **기본값을 항상 제공하여 설정 누락을 방지하세요** -- `os.environ.get("PORT", "8000")` 처럼 기본값을 지정합니다
5. **민감 정보는 로그에 출력하지 마세요** -- 비밀번호, API 키 등은 마스킹 처리합니다

> **Warning:** `.env` 파일에 데이터베이스 비밀번호, API 키, 시크릿 키 같은 민감한 정보가 들어가는 경우가 많습니다. 이 파일이 Git에 커밋되면 누구나 비밀 정보에 접근할 수 있습니다. `.gitignore`에 `.env`를 반드시 추가하고, 실수로 커밋하지 않았는지 `git status`로 항상 확인하세요.

---

### 20.9 실습: 멀티 모듈 계산기

지금까지 배운 프로젝트 관리 기술을 종합하여, 여러 모듈로 구성된 계산기를 만들어 보겠습니다.

**예제 20-7: 멀티 모듈 계산기**

이 예제는 하나의 파일에서 시연하지만, 실제 프로젝트에서는 각 클래스를 별도 파일로 분리합니다.

```python
# examples/python/chapter05/ex20_07_multi_module_calc.py

# [모듈 1] operations.py - 기본 연산 모듈
class BasicOperations:
    """기본 사칙연산을 제공합니다."""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return a / b


class AdvancedOperations:
    """고급 수학 연산을 제공합니다."""

    @staticmethod
    def power(base, exponent):
        return base ** exponent

    @staticmethod
    def factorial(n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("0 이상의 정수만 가능합니다")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


# [모듈 2] history.py - 계산 이력 관리 모듈
class CalculationHistory:
    """계산 이력을 관리합니다."""

    def __init__(self, max_size=100):
        self._history = []
        self._max_size = max_size

    def add_record(self, expression, result):
        record = {
            "expression": expression,
            "result": result,
            "index": len(self._history) + 1,
        }
        self._history.append(record)
        if len(self._history) > self._max_size:
            self._history.pop(0)
        return record

    def get_all(self):
        return list(self._history)

    def get_last(self, n=5):
        return self._history[-n:]

    @property
    def count(self):
        return len(self._history)


# [모듈 3] formatter.py - 출력 포맷 모듈
class ResultFormatter:
    """계산 결과를 다양한 형식으로 포맷합니다."""

    @staticmethod
    def format_result(expression, result):
        if isinstance(result, float) and result == int(result):
            return f"  {expression} = {int(result)}"
        return f"  {expression} = {result:.6g}" if isinstance(result, float) else f"  {expression} = {result}"


# [모듈 4] calculator.py - 메인 계산기 (모듈 통합)
class Calculator:
    """여러 모듈을 통합하는 메인 계산기 클래스"""

    OPERATORS = {
        "+": ("덧셈", BasicOperations.add),
        "-": ("뺄셈", BasicOperations.subtract),
        "*": ("곱셈", BasicOperations.multiply),
        "/": ("나눗셈", BasicOperations.divide),
        "**": ("거듭제곱", AdvancedOperations.power),
    }

    def __init__(self):
        self.history = CalculationHistory()
        self.formatter = ResultFormatter()

    def calculate(self, a, operator, b=None):
        try:
            if operator in self.OPERATORS:
                name, func = self.OPERATORS[operator]
                result = func(a, b)
                expression = f"{a} {operator} {b}"
            else:
                return self.formatter.format_error(f"알 수 없는 연산자: '{operator}'")

            self.history.add_record(expression, result)
            return self.formatter.format_result(expression, result)
        except (ZeroDivisionError, ValueError, TypeError) as e:
            return f"  오류: {e}"
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_07_multi_module_calc.py
```

**결과:**

```
============================================================
예제 20-07: 멀티 모듈 계산기
============================================================

--- 모듈 구조 ---

  operations.py        : 기본/고급 연산 함수 (BasicOperations, AdvancedOperations)
  history.py           : 계산 이력 관리 (CalculationHistory)
  formatter.py         : 결과 출력 포맷 (ResultFormatter)
  calculator.py        : 메인 계산기 - 모든 모듈 통합 (Calculator)

--- 사용 가능한 연산 ---
  사용 가능한 연산:
  [이항 연산]
       + : 덧셈
       - : 뺄셈
       * : 곱셈
       / : 나눗셈
      ** : 거듭제곱
       % : 나머지
      // : 정수나눗셈
  [단항 연산]
       ! : 팩토리얼
     abs : 절댓값

--- 기본 사칙연산 ---
  100 + 200 = 300
  500 - 123 = 377
  12 * 8 = 96
  100 / 3 = 33.3333

--- 고급 연산 ---
  2 ** 10 = 1024
  17 % 5 = 2
  17 // 5 = 3
  5! = 120
  10! = 3628800
  abs(-42) = 42

--- 오류 처리 ---
  오류: 0으로 나눌 수 없습니다
  오류: 0 이상의 정수만 가능합니다
  오류: 알 수 없는 연산자: '^'

--- 전체 계산 이력 ---
  [  1] 100 + 200 = 300
  [  2] 500 - 123 = 377
  [  3] 12 * 8 = 96
  [  4] 100 / 3 = 33.3333
  [  5] 2 ** 10 = 1024
  ...

--- 이력 통계 ---
  총 계산 횟수: 10회
  이력 초기화: 10건 삭제됨
  현재 이력 수: 0건

멀티 모듈 계산기 예제를 성공적으로 실행했습니다!
```

#### 모듈 분리 시 실제 파일 구조

이 계산기를 실제 프로젝트로 분리하면 다음과 같은 구조가 됩니다:

```
calculator/
├── src/
│   └── calculator/
│       ├── __init__.py         # 패키지 초기화
│       ├── operations.py       # BasicOperations, AdvancedOperations
│       ├── history.py          # CalculationHistory
│       ├── formatter.py        # ResultFormatter
│       └── calculator.py       # Calculator (메인 통합 클래스)
├── tests/
│   ├── __init__.py
│   ├── test_operations.py
│   ├── test_history.py
│   └── test_calculator.py
├── requirements.txt
└── README.md
```

각 모듈의 `import`는 다음과 같이 작성합니다:

```python
# calculator/calculator.py
from .operations import BasicOperations, AdvancedOperations
from .history import CalculationHistory
from .formatter import ResultFormatter

class Calculator:
    def __init__(self):
        self.history = CalculationHistory()
        self.formatter = ResultFormatter()
    # ...
```

> **Tip:** AI에게 "이 단일 파일 코드를 멀티 모듈 프로젝트로 분리해줘. 각 클래스를 별도 파일로 나누고, `__init__.py`에서 주요 클래스를 re-export해줘"라고 요청하면 자동으로 파일 구조까지 설계해 줍니다.

---

### 20.10 실습: 패키지로 배포 준비

프로젝트를 다른 사람과 공유하거나 PyPI에 배포하려면 `setup.py` 또는 `pyproject.toml` 파일이 필요합니다.

**예제 20-8: 패키지로 배포 준비**

```python
# examples/python/chapter05/ex20_08_package_setup.py

# pyproject.toml - 현대적인 파이썬 프로젝트 설정 파일
# PEP 518, PEP 621 표준을 따릅니다

# [build-system]
# requires = ["setuptools>=68.0", "wheel>=0.41"]
# build-backend = "setuptools.backends._legacy:_Backend"

# [project]
# name = "vibecoding_utils"
# version = "0.1.0"
# description = "바이브 코딩을 위한 유틸리티 패키지"
# readme = "README.md"
# license = {text = "MIT"}
# requires-python = ">=3.9"
```

**실행:**

```bash
$ python examples/python/chapter05/ex20_08_package_setup.py
```

**결과:**

```
============================================================
예제 20-08: 패키지로 배포 준비
============================================================

--- 1단계: 배포용 파일 생성 ---

  생성: setup.py (전통적 설치 스크립트)
  생성: pyproject.toml (현대적 프로젝트 설정)
  생성: MANIFEST.in (배포 포함 파일 목록)
  생성: LICENSE (MIT 라이선스)
  생성: README.md (프로젝트 설명)
  생성: src/vibecoding_utils/ (패키지 소스)
  생성: tests/ (테스트 코드)

--- 2단계: 생성된 프로젝트 구조 ---

  vibecoding_utils/
  ├── src/
  │   └── vibecoding_utils/
  │       ├── __init__.py
  │       └── cli.py
  ├── tests/
  │   ├── __init__.py
  │   └── test_main.py
  ├── LICENSE
  ├── MANIFEST.in
  ├── README.md
  ├── pyproject.toml
  └── setup.py

--- 5단계: setup.py vs pyproject.toml 비교 ---

  항목                 setup.py               pyproject.toml
  -------------------- ---------------------- ----------------------
  형식                 Python 코드            TOML 설정 파일
  표준                 전통적 방식            PEP 621 표준
  유연성               높음 (코드 실행)       제한적 (선언적)
  도구 설정            별도 파일 필요         통합 관리 가능
  권장 여부            레거시 지원용          신규 프로젝트 권장

--- 6단계: 배포 명령어 안내 ---

  개발 모드 설치:
    pip install -e .

  배포 패키지 빌드:
    python -m build

  PyPI에 업로드:
    python -m twine upload dist/*

패키지 배포 준비 예제를 성공적으로 실행했습니다!
(임시 파일 정리 완료)
```

#### setup.py vs pyproject.toml

| 항목 | `setup.py` | `pyproject.toml` |
|------|-----------|-----------------|
| 형식 | Python 코드 | TOML 설정 파일 |
| 표준 | 전통적 방식 | PEP 621 표준 |
| 유연성 | 높음 (코드 실행 가능) | 제한적 (선언적) |
| 도구 설정 | 별도 파일 필요 | 통합 관리 가능 |
| 권장 여부 | 레거시 지원용 | **신규 프로젝트 권장** |

`pyproject.toml`이 현대적인 표준이며, 새로운 프로젝트에서는 이 파일을 사용하는 것이 권장됩니다. pytest, black, mypy 등 다양한 도구의 설정도 이 파일 하나에서 관리할 수 있어 편리합니다.

```toml
# pyproject.toml에서 도구 설정까지 통합 관리
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
```

#### 배포 워크플로우

패키지를 PyPI에 배포하는 전체 과정:

```bash
# 1. 개발 모드로 설치 (코드 수정이 즉시 반영됨)
$ pip install -e .

# 2. 테스트 실행
$ pytest

# 3. 배포 패키지 빌드
$ python -m build

# 4. TestPyPI에 먼저 업로드 (테스트용)
$ python -m twine upload --repository testpypi dist/*

# 5. 정식 PyPI에 업로드
$ python -m twine upload dist/*
```

> **Tip:** 처음 패키지를 배포할 때는 AI에게 "이 프로젝트를 PyPI에 배포할 수 있도록 `pyproject.toml`을 만들어줘. 프로젝트 이름은 `my-tool`이고, 파이썬 3.9 이상을 지원해야 해"라고 구체적으로 요청하면 됩니다.

---

### 20.11 AI와 함께하는 프로젝트 관리

이번 장에서 배운 모든 기술을 AI에게 요청하는 방법을 정리합니다.

#### 프로젝트 초기 설정 요청

```
새로운 파이썬 웹 프로젝트를 시작하려고 해.
다음 조건으로 프로젝트 구조를 만들어줘:
- 프로젝트 이름: my_blog
- src/ 레이아웃 사용
- 테스트, 문서, 설정 디렉토리 포함
- requirements.txt와 pyproject.toml 생성
- .gitignore에 파이썬 관련 패턴 포함
```

#### 모듈 분리 요청

```
app.py 파일이 500줄이 넘어서 관리가 어려워.
다음 기준으로 모듈을 분리해줘:
1. 라우팅 핸들러 → routes.py
2. 데이터 모델 → models.py
3. 데이터베이스 작업 → database.py
4. 유틸리티 함수 → utils.py
5. 설정 관리 → config.py
각 모듈 간 import 관계도 정리해줘.
```

#### 설정 관리 요청

```
프로젝트에 환경별 설정 관리를 추가해줘.
- 개발, 테스트, 운영 3가지 환경 지원
- .env 파일로 민감 정보 관리
- configparser 또는 클래스 상속 방식
- .env.example 파일도 함께 생성
```

---

### 정리

이번 장에서 배운 핵심 내용을 정리합니다.

**프로젝트 구조:**

- 표준 파이썬 프로젝트는 `src/`, `tests/`, `docs/` 등의 디렉토리로 구성됩니다
- `src/` 레이아웃을 사용하면 설치된 패키지와 소스 코드가 명확히 분리됩니다

**모듈화:**

- 하나의 큰 파일을 역할별 모듈로 분리하면 유지보수가 쉬워집니다
- 단일 책임 원칙: 각 모듈은 하나의 역할만 담당합니다
- 높은 응집도, 낮은 결합도가 좋은 모듈 설계의 핵심입니다

**패키지:**

- `__init__.py`가 있는 디렉토리가 파이썬 패키지입니다
- `__init__.py`는 패키지 인식, 초기화, API 정의, re-export 역할을 합니다
- 상대 임포트(`from .basic import add`)는 패키지 내부에서 사용합니다

**의존성 관리:**

- `requirements.txt`로 프로젝트 의존성을 기록합니다
- `==`는 정확한 버전 고정, `>=`는 최소 버전, `~=`는 호환 버전을 의미합니다
- 개발 의존성은 `requirements-dev.txt`로 분리합니다

**가상환경:**

- `python -m venv venv`로 프로젝트별 독립 환경을 만듭니다
- 가상환경 디렉토리는 `.gitignore`에 추가합니다

**설정 관리:**

- `configparser`로 INI 형식의 설정 파일을 관리합니다
- 환경별 설정은 클래스 상속 또는 `.env` 파일로 분리합니다
- 민감한 정보는 절대 코드에 직접 작성하지 않습니다

> **Note:** 프로젝트 관리는 코드 작성만큼 중요합니다. 잘 구조화된 프로젝트는 혼자 작업할 때도 효율적이지만, 다른 사람과 협업할 때 그 진가가 발휘됩니다. AI에게 "이 프로젝트의 구조를 설명해줘"라고 요청하면, 프로젝트 구조에 대한 문서화도 도움받을 수 있습니다.

---

### 연습 문제

**연습 1: 프로젝트 구조 설계**

"할 일 관리(TODO) 앱"을 만든다고 가정하고, 표준 파이썬 프로젝트 구조를 설계해 보세요. 다음 요소를 포함해야 합니다:
- 소스 코드 패키지 (`src/todo_app/`)
- 테스트 디렉토리 (`tests/`)
- `requirements.txt`, `.gitignore`, `README.md`

> **힌트:** AI에게 "할 일 관리 앱의 프로젝트 구조를 만들어줘"라고 요청하되, 각 디렉토리와 파일의 역할을 직접 설명할 수 있는지 확인해 보세요.

**연습 2: 모듈 분리 실습**

다음 코드를 `validators.py`, `models.py`, `services.py`로 분리해 보세요:

```python
# 현재: 모든 코드가 app.py에 있음
students = []

def add_student(name, grade):
    if not name or len(name) < 2:
        return "이름이 너무 짧습니다"
    if grade < 0 or grade > 100:
        return "성적은 0~100 사이여야 합니다"
    student = {"name": name, "grade": grade}
    students.append(student)
    print(f"등록 완료: {name}")
    return student
```

**연습 3: requirements.txt 작성**

웹 크롤링 프로젝트를 위한 `requirements.txt`와 `requirements-dev.txt`를 작성해 보세요. 다음 라이브러리가 필요합니다:
- 프로덕션: `requests`, `beautifulsoup4`, `lxml`
- 개발: `pytest`, `black`, `flake8`

**연습 4: 설정 파일 만들기**

`configparser`를 사용하여 다음 설정을 가진 `config.ini` 파일을 생성하는 코드를 작성해 보세요:
- `[app]` 섹션: 이름, 버전, 포트
- `[database]` 섹션: 엔진, 이름, 호스트
- `[logging]` 섹션: 레벨, 파일명

설정 파일을 읽어서 내용을 출력하는 코드도 함께 작성하세요.

**연습 5: 가상환경 워크플로우**

새 프로젝트를 시작하는 전체 워크플로우를 직접 실행해 보세요:
1. 프로젝트 디렉토리 생성
2. `git init`
3. `python -m venv venv`
4. 가상환경 활성화
5. 패키지 설치 (`pip install requests`)
6. `pip freeze > requirements.txt`
7. `.gitignore` 생성 (venv/ 포함)
8. 첫 커밋

---

### 다음 장 예고

**Chapter 21: 테스트와 품질 관리**

프로젝트 구조를 잡았으니, 이제 코드의 품질을 보장하는 방법을 배울 차례입니다. 다음 장에서는 **단위 테스트(Unit Test)**를 작성하는 방법, **TDD(테스트 주도 개발)**의 기본 개념, 그리고 AI에게 테스트 코드를 요청하는 기법을 다룹니다. "이 함수의 테스트를 만들어줘"라고 AI에게 요청하는 것만으로 코드의 신뢰성을 크게 높일 수 있습니다.
