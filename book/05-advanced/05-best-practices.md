# Chapter 24: 모범 사례와 패턴

지금까지 바이브 코딩의 다양한 기술과 도구를 배웠습니다. 하지만 기술을 아는 것과 잘 활용하는 것은 다른 문제입니다. 뛰어난 요리사가 레시피만 아는 것이 아니라 재료를 다루는 습관, 주방을 정리하는 루틴, 맛을 보는 감각까지 갖추고 있듯이, 능숙한 바이브 코더도 효과적인 워크플로우, 코드 품질 관리 습관, 문서화 패턴을 갖추고 있어야 합니다.

이 장에서는 바이브 코딩을 더 효과적으로 실천하기 위한 **모범 사례(Best Practices)**와 **반복적으로 활용할 수 있는 패턴**을 소개합니다. 프롬프트 템플릿 관리부터 코드 품질 자동 검사, 문서화 습관, 그리고 지속적인 학습 전략까지 폭넓게 다룹니다.

---

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다:

- 효과적인 바이브 코딩 **워크플로우**를 설계하고 실천할 수 있다
- 자주 하는 실수를 미리 알고 **예방**할 수 있다
- 바이브 코딩 **생산성 팁 10가지**를 일상에 적용할 수 있다
- **프롬프트 템플릿**을 체계적으로 관리하고 재사용할 수 있다
- 코드 리뷰 체크리스트와 린터로 **코드 품질**을 자동 관리할 수 있다
- 문서화 도구를 활용하여 **문서화 습관**을 정착시킬 수 있다
- 커뮤니티와 학습 자원을 활용하여 **지속적으로 성장**할 수 있다

---

## 24.1 효과적인 바이브 코딩 워크플로우

### 워크플로우란?

워크플로우(Workflow)란 작업을 수행하는 일련의 절차와 흐름입니다. 바이브 코딩에서도 효율적인 워크플로우를 갖추면 같은 시간에 더 높은 품질의 결과물을 만들 수 있습니다.

숙련된 바이브 코더의 워크플로우를 도식으로 표현하면 다음과 같습니다:

```
[1. 계획] ──→ [2. 프롬프트 작성] ──→ [3. AI 요청]
                                          │
                                          ↓
[6. 커밋] ←── [5. 품질 검사] ←── [4. 코드 리뷰]
    │
    ↓
[7. 다음 기능] ──→ ... (반복)
```

### 단계별 상세 설명

**단계 1: 계획 수립**

코드를 작성하기 전에 먼저 무엇을 만들지 명확히 정리합니다. 이 단계에서는 코드가 아니라 **자연어로 설계**합니다.

```
[계획 예시]
- 목표: 사용자 등록 기능 구현
- 입력: 이름, 이메일, 비밀번호
- 출력: 등록 성공/실패 메시지
- 제약: 이메일 중복 불가, 비밀번호 8자 이상
- 테스트: 정상 등록, 중복 이메일, 약한 비밀번호
```

**단계 2: 프롬프트 작성**

계획을 바탕으로 AI에게 전달할 프롬프트를 작성합니다. 이때 **템플릿**을 활용하면 일관성을 유지할 수 있습니다.

**단계 3: AI에게 요청**

작성한 프롬프트로 AI에게 코드 생성을 요청합니다. 한 번에 모든 기능을 요청하지 말고, **작은 단위로 나누어** 요청합니다.

**단계 4: 코드 리뷰**

AI가 생성한 코드를 반드시 검토합니다. "돌아가니까 괜찮겠지"라는 생각은 금물입니다.

**단계 5: 품질 검사**

린터, 포맷터, 테스트를 실행하여 코드 품질을 확인합니다.

**단계 6: 커밋**

품질 검사를 통과한 코드를 Git에 커밋합니다. 의미 있는 커밋 메시지를 작성합니다.

**단계 7: 반복**

다음 기능으로 넘어가 같은 과정을 반복합니다.

> **Tip:** 이 워크플로우에서 가장 중요한 것은 **단계를 건너뛰지 않는 것**입니다. 특히 "코드 리뷰"와 "품질 검사"를 생략하는 습관이 생기면, 나중에 큰 문제가 발생할 수 있습니다.

### 프롬프트 템플릿으로 워크플로우 체계화하기

반복적으로 사용하는 프롬프트를 **템플릿**으로 만들어 두면 일관성 있고 효율적인 바이브 코딩이 가능합니다. 다음 예제는 프롬프트 템플릿을 체계적으로 관리하는 시스템을 구현합니다.

**예제 24-1: 효과적인 프롬프트 템플릿**

```python
# examples/python/chapter05/ex24_01_prompt_templates.py
from string import Template
from datetime import datetime
import json
import textwrap


class PromptTemplate:
    """프롬프트 템플릿을 관리하는 클래스"""

    def __init__(self, name: str, template_str: str, description: str = ""):
        self.name = name
        self.template = Template(template_str)
        self.description = description
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def render(self, **kwargs) -> str:
        """템플릿에 변수를 대입하여 최종 프롬프트를 생성"""
        try:
            return self.template.safe_substitute(**kwargs)
        except (KeyError, ValueError) as e:
            return f"[오류] 템플릿 렌더링 실패: {e}"

    def get_variables(self) -> list:
        """템플릿에서 사용된 변수 목록 추출"""
        import re
        pattern = r'\$\{?([a-zA-Z_][a-zA-Z0-9_]*)\}?'
        return list(set(re.findall(pattern, self.template.template)))

    def __repr__(self):
        return f"PromptTemplate(name='{self.name}', vars={self.get_variables()})"


class PromptLibrary:
    """프롬프트 템플릿을 모아서 관리하는 라이브러리"""

    def __init__(self):
        self.templates: dict[str, PromptTemplate] = {}

    def add(self, template: PromptTemplate):
        """템플릿 추가"""
        self.templates[template.name] = template

    def get(self, name: str) -> PromptTemplate:
        """이름으로 템플릿 조회"""
        if name not in self.templates:
            raise KeyError(f"템플릿 '{name}'을(를) 찾을 수 없습니다.")
        return self.templates[name]

    def list_templates(self) -> list:
        """등록된 템플릿 목록 반환"""
        return [
            {"이름": t.name, "설명": t.description, "변수": t.get_variables()}
            for t in self.templates.values()
        ]
```

이 코드의 핵심을 살펴보겠습니다:

1. **`PromptTemplate` 클래스**: `string.Template`을 기반으로 변수가 포함된 프롬프트를 관리합니다. `render()` 메서드로 변수에 값을 대입하면 최종 프롬프트가 생성됩니다.
2. **`PromptLibrary` 클래스**: 여러 템플릿을 이름으로 등록하고 조회할 수 있는 라이브러리입니다.

미리 정의된 바이브 코딩용 템플릿의 예시를 살펴봅시다:

```python
# 기능 구현 요청 템플릿
FEATURE_REQUEST = PromptTemplate(
    name="기능_구현",
    description="새로운 기능 구현을 요청하는 프롬프트",
    template_str=textwrap.dedent("""\
        다음 기능을 구현해 주세요:

        ## 기능명: ${feature_name}

        ## 설명
        ${description}

        ## 기술 스택
        - 언어: ${language}
        - 프레임워크: ${framework}

        ## 요구사항
        ${requirements}

        ## 제약조건
        - 외부 라이브러리 최소화
        - 에러 처리 포함
        - 테스트 코드 포함
    """)
)
```

**실행:**

```bash
$ python examples/python/chapter05/ex24_01_prompt_templates.py
```

**결과 (일부):**

```
============================================================
  예제 24-01: 효과적인 프롬프트 템플릿 시스템
============================================================

등록된 프롬프트 템플릿 목록:
----------------------------------------
  이름: 기능_구현
  설명: 새로운 기능 구현을 요청하는 프롬프트
  변수: requirements, description, framework, feature_name, language
  ---
  이름: 코드_리뷰
  설명: 코드 리뷰를 요청하는 프롬프트
  변수: filename, code, review_focus, language
  ---
  이름: 버그_수정
  설명: 버그 수정을 요청하는 프롬프트
  변수: actual, code, expected, language, version, reproduce_steps, os_info, symptom
  ---

총 5개의 템플릿이 라이브러리에 등록되어 있습니다.
```

이렇게 자주 사용하는 프롬프트 패턴(기능 구현, 코드 리뷰, 버그 수정, 리팩토링, 테스트 작성)을 템플릿으로 만들어 두면, 매번 처음부터 프롬프트를 작성할 필요 없이 변수만 채워 넣으면 됩니다.

> **Note:** 프롬프트 템플릿은 개인 프로젝트에서뿐만 아니라 팀 프로젝트에서 특히 유용합니다. 팀원 모두가 동일한 템플릿을 사용하면 AI에 대한 요청 품질이 일관되게 유지됩니다.

---

## 24.2 자주 하는 실수와 해결법

바이브 코딩을 하다 보면 누구나 빠지기 쉬운 함정이 있습니다. 이 섹션에서는 가장 흔한 실수 7가지와 각각의 해결법을 정리합니다.

### 실수 1: 한 번에 너무 많이 요청하기

| 구분 | 내용 |
|------|------|
| **문제** | "로그인, 회원가입, 비밀번호 찾기, 프로필 관리를 모두 만들어줘" |
| **원인** | 요청 범위가 넓으면 AI가 각 기능의 완성도를 높이기 어렵습니다 |
| **해결** | 기능별로 나누어 요청합니다. "먼저 로그인 기능만 만들어줘" |

### 실수 2: AI 코드를 검토 없이 사용하기

| 구분 | 내용 |
|------|------|
| **문제** | AI가 생성한 코드를 읽지 않고 바로 프로젝트에 통합 |
| **원인** | AI를 과신하거나, 코드를 읽을 자신이 없어서 건너뜀 |
| **해결** | 최소한 "이 코드가 무엇을 하는지" 설명할 수 있어야 합니다 |

### 실수 3: 맥락 없이 요청하기

| 구분 | 내용 |
|------|------|
| **문제** | "정렬 함수 만들어줘" (어떤 데이터? 어떤 기준?) |
| **원인** | 머릿속에는 명확하지만 프롬프트에 담지 않음 |
| **해결** | 프로젝트 배경, 데이터 형식, 제약조건을 함께 명시 |

### 실수 4: 에러 메시지를 무시하기

| 구분 | 내용 |
|------|------|
| **문제** | 에러가 나면 코드를 통째로 다시 요청 |
| **원인** | 에러 메시지를 읽고 분석하는 습관이 없음 |
| **해결** | 에러 메시지를 AI에게 보여주며 "이 에러를 설명해줘"라고 요청 |

### 실수 5: 테스트 없이 넘어가기

| 구분 | 내용 |
|------|------|
| **문제** | "돌아가니까 됐어"라며 테스트를 작성하지 않음 |
| **원인** | 테스트 작성이 번거롭다고 느낌 |
| **해결** | AI에게 "이 함수에 대한 테스트 코드를 작성해줘"라고 요청하면 쉽게 생성 가능 |

### 실수 6: 버전 관리를 하지 않기

| 구분 | 내용 |
|------|------|
| **문제** | Git을 사용하지 않고 코드를 덮어씀 |
| **원인** | "아직 작은 프로젝트니까 괜찮아" |
| **해결** | 어떤 프로젝트든 첫날부터 Git을 사용합니다. 잘못된 변경을 되돌릴 수 있는 안전망입니다 |

### 실수 7: 문서화를 미루기

| 구분 | 내용 |
|------|------|
| **문제** | "나중에 한꺼번에 쓰겠다"며 문서화를 미룸 |
| **원인** | 문서화가 코딩보다 덜 중요하다고 생각 |
| **해결** | AI에게 docstring과 README를 함께 요청합니다. 코드와 문서를 동시에 작성하면 부담이 줄어듭니다 |

> **Warning:** 이 중에서 가장 위험한 실수는 **"AI 코드를 검토 없이 사용하기"**입니다. AI가 생성한 코드에는 보안 취약점, 비효율적인 로직, 잘못된 가정이 포함될 수 있습니다. 항상 코드를 이해하고 나서 사용하세요.

---

## 24.3 생산성 팁 10가지

바이브 코딩의 생산성을 높이는 실용적인 팁 10가지를 소개합니다.

### 팁 1: 프롬프트 라이브러리를 구축하라

앞의 예제 24-1에서 본 것처럼, 반복 사용하는 프롬프트를 템플릿으로 만들어 라이브러리에 등록해 두세요. 기능 구현, 코드 리뷰, 버그 수정, 리팩토링, 테스트 작성 등 상황별 템플릿이 있으면 매번 프롬프트를 처음부터 쓸 필요가 없습니다.

### 팁 2: "설명해줘"를 습관적으로 요청하라

AI에게 코드를 생성하게 한 뒤, 반드시 **"이 코드를 줄 단위로 설명해줘"**라고 요청하세요. 이 과정에서 코드를 이해하게 되고, 잠재적 문제도 발견할 수 있습니다.

### 팁 3: 작업 단위를 30분 이내로 유지하라

하나의 AI 요청에서 30분 이상 걸리는 작업은 너무 큰 것입니다. 기능을 더 작은 단위로 쪼개세요. 작은 성공을 빠르게 쌓아가는 것이 바이브 코딩의 핵심입니다.

### 팁 4: 코드 리뷰 체크리스트를 자동화하라

코드 리뷰를 사람의 기억에 의존하지 말고, 자동 검사 도구를 활용하세요. 예제 24-2에서 구현하는 것처럼 체크리스트를 코드로 만들면 매번 일관된 품질 검사가 가능합니다.

### 팁 5: 포맷팅은 도구에게 맡겨라

코드 스타일을 맞추는 데 시간을 쓰지 마세요. 자동 포맷팅 도구를 설정해 두면 저장할 때마다 자동으로 코드가 정리됩니다.

### 팁 6: Git 커밋은 자주, 작게 하라

"기능 완성 후 한 번에 커밋"이 아니라, 의미 있는 변경마다 커밋합니다. 작은 커밋은 문제 발생 시 원인을 찾기 쉽고, 롤백도 안전합니다.

```bash
# 나쁜 예: 하루치 작업을 한 번에 커밋
git commit -m "여러 기능 추가"

# 좋은 예: 기능별로 나누어 커밋
git commit -m "feat: 사용자 등록 함수 추가"
git commit -m "feat: 이메일 검증 로직 추가"
git commit -m "test: 사용자 등록 테스트 추가"
```

### 팁 7: AI에게 "더 나은 방법이 있을까?"라고 물어라

AI가 생성한 코드를 받은 뒤, 한 번 더 물어보세요: "이 코드를 개선할 수 있는 방법이 있을까?" 종종 더 효율적이거나 Pythonic한 대안을 제시합니다.

### 팁 8: 실패한 프롬프트도 기록하라

어떤 프롬프트가 원하는 결과를 주지 못했는지 기록해 두면, 다음에 같은 실수를 반복하지 않습니다.

```
[실패 기록 예시]
- 프롬프트: "로그인 기능 만들어줘"
- 문제: 보안 처리가 전혀 없었음
- 개선: "시니어 보안 개발자 역할로, 비밀번호 해싱과 입력 검증을 포함한 로그인 기능을 만들어줘"
```

### 팁 9: README를 먼저 작성하라

코드를 쓰기 전에 README를 먼저 작성하세요. 이것을 **README-Driven Development**라고 합니다. 프로젝트의 목표, 구조, 사용법을 먼저 정리하면 코드 설계가 더 명확해집니다.

### 팁 10: 매일 30분씩 학습 시간을 확보하라

바이브 코딩 기술은 빠르게 발전하고 있습니다. 매일 30분씩 새로운 AI 도구, 프롬프트 기법, 다른 사람의 사례를 살펴보면 꾸준히 성장할 수 있습니다.

> **Tip:** 10가지 팁을 한꺼번에 적용하려고 하지 마세요. 먼저 2~3가지를 선택하여 **습관으로 만든 후**, 나머지를 하나씩 추가해 나가는 것이 효과적입니다.

---

## 24.4 코드 품질 유지

코드 품질은 소프트웨어의 수명을 결정합니다. 바이브 코딩에서는 AI가 코드를 생성하기 때문에 품질 관리가 더욱 중요합니다. AI가 생성한 코드가 항상 완벽하지는 않으므로, 자동 검사 도구를 활용하여 일관된 품질을 유지해야 합니다.

### 코드 리뷰 자동 체크리스트

코드 리뷰를 할 때 매번 같은 항목을 기억에 의존하여 확인하는 것은 비효율적입니다. 체크리스트를 코드로 구현하면 자동으로 일관된 검사를 수행할 수 있습니다.

**예제 24-2: 코드 리뷰 체크리스트**

```python
# examples/python/chapter05/ex24_02_code_review_checklist.py
import ast
import re
import textwrap
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    """검사 결과의 심각도"""
    INFO = "정보"
    WARNING = "경고"
    ERROR = "오류"


@dataclass
class CheckResult:
    """개별 검사 결과"""
    rule: str           # 규칙 이름
    severity: Severity  # 심각도
    message: str        # 메시지
    line: int = 0       # 관련 줄 번호

    def __str__(self):
        loc = f" (줄 {self.line})" if self.line > 0 else ""
        return f"  [{self.severity.value}] {self.rule}: {self.message}{loc}"


class CodeReviewChecker:
    """코드 리뷰 체크리스트를 실행하는 검사기"""

    def __init__(self, source_code: str, filename: str = "<입력>"):
        self.source = source_code
        self.lines = source_code.split("\n")
        self.filename = filename
        self.report = ReviewReport(filename=filename)
        self._tree = None

    def run_all_checks(self) -> ReviewReport:
        """모든 검사 항목 실행"""
        if not self._parse_ast():
            return self.report

        self.check_function_length()     # 함수 길이 30줄 이내
        self.check_function_args()       # 매개변수 5개 이내
        self.check_docstrings()          # docstring 존재 여부
        self.check_naming_convention()   # PEP 8 네이밍
        self.check_bare_except()         # bare except 금지
        self.check_line_length()         # 줄 길이 100자 이내
        self.check_todo_comments()       # TODO/FIXME 확인

        return self.report
```

이 검사기는 Python의 `ast` 모듈을 사용하여 코드를 구조적으로 분석합니다. 각 검사 항목의 의미를 살펴보겠습니다:

| 검사 항목 | 기준 | 이유 |
|-----------|------|------|
| 함수 길이 | 30줄 이내 | 긴 함수는 이해하기 어렵고 유지보수가 힘듭니다 |
| 매개변수 수 | 5개 이내 | 너무 많은 매개변수는 함수 설계를 재고해야 한다는 신호입니다 |
| docstring | 모든 함수/클래스 | 문서화는 코드의 의도를 전달하는 핵심 수단입니다 |
| 네이밍 | PEP 8 준수 | 일관된 네이밍은 가독성을 높입니다 |
| bare except | 사용 금지 | 구체적 예외 타입 없이 모든 예외를 잡으면 디버깅이 어렵습니다 |
| 줄 길이 | 100자 이내 | 긴 줄은 읽기 어렵고 코드 리뷰가 힘듭니다 |
| TODO/FIXME | 확인 | 미완료 작업이 남아 있는지 파악합니다 |

**실행:**

```bash
$ python examples/python/chapter05/ex24_02_code_review_checklist.py
```

**결과 (문제가 있는 코드 검사):**

```
============================================================
  코드 리뷰 보고서: sample_module.py
============================================================

  --- 오류 (1건) ---
  [오류] 예외 처리: 맨(bare) except 사용 금지 - 구체적인 예외 타입을 명시하세요 (줄 17)

  --- 경고 (9건) ---
  [경고] 매개변수 수: 함수 '__init__'의 매개변수가 7개로 너무 많습니다 (최대 5개 권장) (줄 4)
  [경고] docstring: 'user_data'에 docstring이 없습니다 (줄 3)
  [경고] 네이밍 컨벤션: 클래스 'user_data'이(가) PascalCase가 아닙니다 (줄 3)
  [경고] 네이밍 컨벤션: 함수 'processData'이(가) snake_case가 아닙니다 (줄 13)
  ...

────────────────────────────────────────────────────────────
  검사 결과: 실패 | 총 15건 (오류: 1, 경고: 9, 정보: 5)
============================================================
```

**결과 (양호한 코드 검사):**

```
============================================================
  코드 리뷰 보고서: good_module.py
============================================================

  --- 정보 (3건) ---
  [정보] 함수 길이: 함수 'calculate_average': 5줄 (적절) (줄 13)
  [정보] 함수 길이: 함수 '__init__': 4줄 (적절) (줄 4)
  [정보] 함수 길이: 함수 'validate_email': 3줄 (적절) (줄 9)

────────────────────────────────────────────────────────────
  검사 결과: 통과 | 총 3건 (오류: 0, 경고: 0, 정보: 3)
============================================================
```

첫 번째 검사에서는 네이밍 컨벤션 위반, docstring 누락, bare except 사용 등 15건의 문제가 발견되었고, 두 번째 양호한 코드에서는 정보성 메시지만 3건 나왔습니다. 이처럼 자동화된 체크리스트를 사용하면 사람이 놓치기 쉬운 문제도 빠짐없이 발견할 수 있습니다.

### 자동 포맷팅으로 스타일 통일

코드 스타일을 수동으로 맞추는 것은 시간 낭비입니다. 자동 포맷팅 도구를 활용하면 코드 작성에만 집중할 수 있습니다.

**예제 24-3: 자동 포맷팅 설정**

```python
# examples/python/chapter05/ex24_03_auto_formatting.py
class CodeFormatter:
    """Python 코드를 자동으로 포맷팅하는 도구"""

    def __init__(self):
        self.indent_size = 4
        self.max_line_length = 79
        self.blank_lines_after_import = 2
        self.blank_lines_between_functions = 2
        self.blank_lines_between_methods = 1

    def format_source(self, source: str) -> str:
        """소스 코드 전체를 포맷팅"""
        lines = source.split("\n")
        formatted_lines = []

        for i, line in enumerate(lines):
            line = line.rstrip()        # 후행 공백 제거
            line = line.expandtabs(self.indent_size)  # 탭 → 스페이스
            formatted_lines.append(line)

        result = "\n".join(formatted_lines)
        result = re.sub(r'\n{4,}', '\n\n\n', result)  # 빈 줄 정리
        result = result.rstrip() + "\n"   # 파일 끝 빈 줄

        return result
```

이 포맷터는 다음과 같은 규칙을 적용합니다:

- 후행 공백(trailing whitespace) 제거
- 탭을 스페이스 4칸으로 변환
- 연속 빈 줄을 최대 2줄로 제한
- 파일 끝에 빈 줄 하나 보장

**실행:**

```bash
$ python examples/python/chapter05/ex24_03_auto_formatting.py
```

**결과 (일부):**

```
============================================================
  코드 구조 분석 보고서: messy_example.py
============================================================

  [코드 구조]
  - Import 문: 5개
  - 상수: 2개
    - MAX_SIZE
    - DEFAULT_NAME
  - 클래스: 1개
    - DataProcessor (메서드: __init__, process)
  - 함수: 2개
    - helper_function(x, y)
    - another_function()

  [포맷팅 검사 결과]
  발견된 문제: 10건
    - 줄 11: 탭 문자 사용 (스페이스 권장)
    - 줄 12: '=' 주위에 공백 필요
    ...

============================================================
  포맷팅 설정 요약
============================================================
  - 들여쓰기: 스페이스 4칸
  - 최대 줄 길이: 79자
  - import 후 빈 줄: 2줄
  - 함수 간 빈 줄: 2줄
  - 메서드 간 빈 줄: 1줄
```

> **Tip:** 실제 프로젝트에서는 `black`, `autopep8` 같은 전문 포맷터를 사용하는 것을 권장합니다. AI에게 "이 프로젝트에 black 포맷터를 설정해줘"라고 요청하면 `.pyproject.toml` 설정 파일까지 자동으로 생성할 수 있습니다.

### 린터로 잠재적 문제 발견

포맷팅이 코드의 "외모"를 다듬는 것이라면, 린터(Linter)는 코드의 "건강"을 검사하는 것입니다. 린터는 네이밍 규칙 위반, 복잡도 초과, 잘못된 예외 처리 등 잠재적 문제를 찾아냅니다.

**예제 24-4: 린터 체크**

```python
# examples/python/chapter05/ex24_04_linter_check.py
class PythonLinter:
    """AST + 줄 단위 검사를 통합한 Python 린터"""

    def __init__(self, source: str, filename: str = "<입력>"):
        self.source = source
        self.filename = filename

    def run(self) -> list[LintMessage]:
        """모든 린트 검사 실행"""
        all_messages = []

        # 1. AST 기반 검사 (네이밍, 복잡도, 예외 처리 등)
        try:
            ast_checker = ASTLintChecker(self.source)
            tree = ast.parse(self.source)
            ast_checker.visit(tree)
            all_messages.extend(ast_checker.messages)
        except SyntaxError as e:
            all_messages.append(LintMessage(
                code="F001", line=e.lineno or 0, column=e.offset or 0,
                message=f"구문 오류: {e.msg}", category="치명적"
            ))
            return all_messages

        # 2. 줄 단위 검사 (줄 길이, 공백, print 문 등)
        line_checker = LineLintChecker(self.source)
        line_checker.run_all()
        all_messages.extend(line_checker.messages)

        all_messages.sort(key=lambda m: (m.line, m.column))
        return all_messages
```

이 린터는 두 가지 수준의 검사를 수행합니다:

1. **AST 기반 검사**: 코드 구조를 분석하여 네이밍 규칙(N001, N002), 코드 복잡도(C001), 예외 처리(E001), 설계 문제(D001, S001) 등을 검사합니다.
2. **줄 단위 검사**: 줄 길이(L001), 후행 공백(L002), 탭 사용(L003), print 문(W001), 매직 넘버(W002) 등을 검사합니다.

**실행:**

```bash
$ python examples/python/chapter05/ex24_04_linter_check.py
```

**결과 (문제가 있는 코드):**

```
============================================================
  린트 검사 결과: data_handler.py
============================================================

  [네이밍] (3건)
  N002 (줄 6, 열 0): 클래스 'data_handler'은(는) PascalCase로 작성해야 합니다
  N001 (줄 12, 열 4): 함수 'ProcessData'은(는) snake_case로 작성해야 합니다
  N001 (줄 33, 열 0): 함수 'UpdateCounter'은(는) snake_case로 작성해야 합니다

  [복잡도] (2건)
  C001 (줄 18, 열 24): 코드 중첩 깊이가 5단계로 너무 깊습니다 (최대 4단계 권장)
  C001 (줄 19, 열 28): 코드 중첩 깊이가 6단계로 너무 깊습니다 (최대 4단계 권장)

  [예외 처리] (1건)
  E001 (줄 28, 열 8): 맨(bare) except 사용 금지 - 구체적인 예외 타입을 명시하세요

  [구조] (1건)
  S002 (줄 34, 열 4): global 변수 'global_counter' 사용 - 함수 매개변수나 클래스 사용을 권장합니다

────────────────────────────────────────────────────────────
  총 9건의 린트 메시지가 발견되었습니다.
```

**결과 (깨끗한 코드):**

```
============================================================
  린트 검사 결과: clean_handler.py
============================================================

  모든 검사를 통과했습니다! 깨끗한 코드입니다.

────────────────────────────────────────────────────────────
  총 0건의 린트 메시지가 발견되었습니다.
============================================================
```

문제가 있는 코드에서는 네이밍 규칙 위반(클래스명이 PascalCase가 아님, 함수명이 snake_case가 아님), 코드 중첩 깊이 초과(5~6단계), bare except 사용, global 변수 사용 등 총 9건의 문제가 발견되었습니다. 반면 깨끗하게 작성된 코드는 모든 검사를 통과했습니다.

> **Note:** 린터가 지적하는 항목이 반드시 "버그"는 아닙니다. 하지만 이러한 경고를 무시하면 장기적으로 유지보수가 어려운 코드가 됩니다. "경고 0건"을 목표로 코드를 작성하는 습관을 들이세요.

### 품질 관리 3단계 흐름

코드 품질 관리를 체계적으로 하려면 다음 3단계를 순서대로 적용합니다:

```
[1단계: 포맷팅]          [2단계: 린팅]          [3단계: 리뷰]
자동 포맷터 적용    →    린터 검사 실행    →    체크리스트 확인
(외모 정리)              (건강 검진)             (종합 판단)
```

- **1단계 - 포맷팅**: 코드 스타일(들여쓰기, 공백, 줄 길이)을 자동으로 정리합니다
- **2단계 - 린팅**: 잠재적 문제(네이밍, 복잡도, 예외 처리)를 찾아냅니다
- **3단계 - 리뷰**: 비즈니스 로직의 정확성, 보안, 성능을 종합적으로 검토합니다

> **Tip:** 바이브 코딩에서 이 3단계를 AI에게 순차적으로 요청할 수 있습니다. "이 코드를 PEP 8에 맞게 포맷팅해줘" → "이 코드의 잠재적 문제를 찾아줘" → "보안과 성능 관점에서 리뷰해줘"

---

## 24.5 문서화 습관

좋은 코드는 자기 자신을 설명하지만, 좋은 프로젝트는 **문서로 설명**됩니다. 바이브 코딩에서는 AI가 문서화를 도와주기 때문에, 문서화의 부담이 크게 줄어듭니다.

### docstring: 함수와 클래스의 설명서

Python에서 **docstring**은 함수나 클래스 바로 아래에 작성하는 설명 문자열입니다. 코드의 의도를 전달하는 가장 중요한 문서화 수단입니다.

**예제 24-5: docstring 작성 도구**

```python
# examples/python/chapter05/ex24_05_docstring_writer.py
class DocstringInspector(ast.NodeVisitor):
    """AST를 순회하며 docstring 정보를 수집"""

    def __init__(self, source: str):
        self.source = source
        self.functions: list[FunctionInfo] = []
        self.classes: list[ClassInfo] = []

    def inspect(self):
        """소스 코드를 분석하여 모든 함수/클래스 정보 수집"""
        tree = ast.parse(self.source)
        self.visit(tree)
        return self


class DocstringGenerator:
    """Google 스타일 docstring 템플릿 생성기"""

    def generate_function_docstring(self, func: FunctionInfo) -> str:
        """함수/메서드용 docstring 생성"""
        parts = []
        parts.append(f'    """{func.name}에 대한 설명을 작성하세요')

        if func.args:
            parts.append("")
            parts.append("    Args:")
            for arg in func.args:
                type_hint = func.arg_types.get(arg, "")
                type_str = f" ({type_hint})" if type_hint else ""
                parts.append(f"        {arg}{type_str}: {arg}에 대한 설명")

        if func.has_return:
            parts.append("")
            parts.append("    Returns:")
            if func.return_type:
                parts.append(f"        {func.return_type}: 반환값에 대한 설명")

        if func.raises:
            parts.append("")
            parts.append("    Raises:")
            for exc in func.raises:
                parts.append(f"        {exc}: 예외 발생 조건 설명")

        parts.append('    """')
        return "\n".join(parts)
```

이 도구는 두 가지 일을 합니다:

1. **DocstringInspector**: 소스 코드를 분석하여 docstring이 있는 항목과 없는 항목을 파악합니다.
2. **DocstringGenerator**: docstring이 없는 함수/클래스에 대해 Google 스타일 docstring 템플릿을 자동으로 생성합니다.

**실행:**

```bash
$ python examples/python/chapter05/ex24_05_docstring_writer.py
```

**결과 (일부):**

```
============================================================
  Docstring 분석 보고서: user_manager.py
============================================================

  [통계]
  - 함수/메서드: 2/9개 docstring 있음
  - 클래스: 1/2개 docstring 있음
  - docstring 커버리지: 27.3%

  [docstring 누락 항목] (8건)
    - 메서드 'add_user' (줄 10)
    - 메서드 'find_user' (줄 16)
    - 함수 'calculate_statistics' (줄 36)
    - 클래스 'ReportGenerator' (줄 25)
    ...

  [자동 생성 docstring 템플릿]
  ──────────────────────────────────────────────────

  메서드 'add_user' (줄 10):
    """add_user에 대한 설명을 작성하세요

    Args:
        name (str): name에 대한 설명
        email (str): email에 대한 설명

    Returns:
        bool: 반환값에 대한 설명

    Raises:
        OverflowError: 예외 발생 조건 설명
    """
```

docstring 커버리지가 27.3%로 낮은 상태에서, 도구가 누락된 8건의 항목을 찾아내고 각각에 대한 템플릿을 자동으로 생성했습니다. 개발자는 이 템플릿의 "설명을 작성하세요" 부분만 채우면 됩니다.

### Google 스타일 docstring의 구조

Python docstring에는 여러 스타일이 있지만, **Google 스타일**이 가장 읽기 쉽고 널리 사용됩니다:

```python
def calculate_bmi(weight: float, height: float) -> float:
    """체질량 지수(BMI)를 계산합니다.

    주어진 체중(kg)과 키(m)를 사용하여 BMI를 계산합니다.
    결과값은 소수점 한 자리로 반올림됩니다.

    Args:
        weight (float): 체중 (kg 단위, 양수)
        height (float): 키 (m 단위, 양수)

    Returns:
        float: 계산된 BMI 값 (소수점 1자리)

    Raises:
        ValueError: weight 또는 height가 0 이하인 경우
    """
    if weight <= 0 or height <= 0:
        raise ValueError("체중과 키는 양수여야 합니다")
    return round(weight / (height ** 2), 1)
```

docstring의 각 부분을 정리하면:

| 구성 요소 | 설명 | 필수 여부 |
|-----------|------|----------|
| 요약 줄 | 함수가 하는 일을 한 줄로 설명 | 필수 |
| 상세 설명 | 추가적인 동작 설명 | 선택 |
| Args | 매개변수 설명 | 매개변수가 있으면 필수 |
| Returns | 반환값 설명 | 반환값이 있으면 필수 |
| Raises | 발생 가능한 예외 | 예외가 있으면 필수 |

> **Tip:** AI에게 "이 함수에 Google 스타일 docstring을 추가해줘"라고 요청하면, 함수의 동작을 분석하여 적절한 docstring을 자동으로 생성합니다. 단, AI가 생성한 docstring이 실제 동작과 일치하는지 반드시 확인하세요.

### README: 프로젝트의 첫인상

README 파일은 프로젝트를 처음 접하는 사람이 가장 먼저 보는 문서입니다. 잘 작성된 README는 프로젝트의 목적, 설치 방법, 사용법을 빠르게 전달합니다.

**예제 24-6: README 템플릿**

```python
# examples/python/chapter05/ex24_06_readme_template.py
@dataclass
class ProjectInfo:
    """프로젝트 메타 정보"""
    name: str
    description: str
    version: str = "0.1.0"
    author: str = ""
    license_type: str = "MIT"
    python_version: str = "3.10+"
    repo_url: str = ""
    features: list = field(default_factory=list)
    install_steps: list = field(default_factory=list)
    usage_examples: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    directory_structure: dict = field(default_factory=dict)
    contributing: bool = True


class ReadmeGenerator:
    """README.md 파일을 자동으로 생성하는 도구"""

    def __init__(self):
        self.sections = [
            HeaderSection(),
            FeaturesSection(),
            InstallSection(),
            UsageSection(),
            DirectorySection(),
            DependenciesSection(),
            ContributingSection(),
            LicenseSection(),
        ]

    def generate(self, info: ProjectInfo) -> str:
        """프로젝트 정보를 바탕으로 README.md 내용 생성"""
        parts = []
        for section in self.sections:
            content = section.render(info)
            if content:
                parts.append(content)
        return "\n".join(parts)
```

이 도구는 `ProjectInfo` 데이터 클래스에 프로젝트 정보를 입력하면, 구조화된 README.md를 자동으로 생성합니다. 헤더, 주요 기능, 설치 방법, 사용법, 디렉토리 구조, 의존성, 기여 가이드, 라이선스 등의 섹션이 포함됩니다.

**실행:**

```bash
$ python examples/python/chapter05/ex24_06_readme_template.py
```

**결과 (생성된 README 일부):**

```markdown
# 바이브 코딩 도우미

> AI와 함께하는 코딩을 더 쉽고 효율적으로 만드는 CLI 도구

| 항목 | 내용 |
|------|------|
| 버전 | 1.0.0 |
| 작성자 | 바이브 코더 |
| 라이선스 | MIT |
| Python | 3.10+ |

## 주요 기능

- 프롬프트 템플릿 관리 및 자동 생성
- 코드 품질 자동 검사 (린팅, 포맷팅)
- docstring 자동 생성 및 검사
- 프로젝트 구조 분석 및 시각화
- 다국어 지원 (한국어, 영어)

## 설치 방법
...

[생성 통계]
  - 총 줄 수: 85줄
  - 섹션 수: 6개
  - 문자 수: 1,847자
```

### 문서화 체크리스트

프로젝트에서 유지해야 할 문서화 항목을 정리하면 다음과 같습니다:

| 문서 유형 | 대상 | 작성 시점 |
|-----------|------|----------|
| docstring | 모든 공개 함수/클래스 | 코드 작성 시 |
| README.md | 프로젝트 루트 | 프로젝트 시작 시 |
| 인라인 주석 | 복잡한 로직 | 코드 작성 시 |
| CHANGELOG | 버전별 변경사항 | 릴리스 시 |
| API 문서 | 외부 인터페이스 | 인터페이스 확정 시 |

> **Note:** README-Driven Development는 코드를 쓰기 전에 README를 먼저 작성하는 접근법입니다. AI에게 "이런 프로젝트의 README를 먼저 만들어줘"라고 요청한 후, 그 구조를 기반으로 코드를 작성하면 설계가 더 명확해집니다.

---

## 24.6 지속적인 학습

바이브 코딩은 빠르게 발전하는 분야입니다. AI 모델은 지속적으로 개선되고, 새로운 도구와 기법이 등장합니다. 따라서 한 번 배운 것에 만족하지 않고 꾸준히 학습하는 것이 중요합니다.

### 학습 로드맵

바이브 코딩 역량을 키우기 위한 단계별 학습 로드맵을 제시합니다:

```
[레벨 1: 입문]                     [레벨 2: 중급]
─────────────────────────    ─────────────────────────
- 기본 프롬프트 작성               - 프롬프트 엔지니어링 심화
- AI 응답 이해                    - 복잡한 프로젝트 관리
- 간단한 코드 생성                - 코드 리뷰 및 리팩토링
- CLI 기초 사용법                 - 테스트 주도 개발 적용

            │                              │
            ↓                              ↓

[레벨 3: 고급]                     [레벨 4: 전문가]
─────────────────────────    ─────────────────────────
- 시스템 설계 및 아키텍처          - 팀 바이브 코딩 리드
- 성능 최적화                     - 워크플로우 자동화 구축
- 보안 코딩                       - 커뮤니티 기여 및 멘토링
- CI/CD 파이프라인 구축           - 새로운 패턴 창조
```

### 효과적인 학습 전략

**전략 1: 매일 하나의 새로운 기법 시도하기**

바이브 코딩에서 새로운 프롬프트 기법, 새로운 도구 기능, 새로운 워크플로우를 매일 하나씩 시도해 보세요. 한 번에 많이 배우려고 하기보다 꾸준히 조금씩 시도하는 것이 효과적입니다.

```
[1주차 학습 계획 예시]
- 월: Few-shot 프롬프트 기법 연습
- 화: Chain of Thought 기법 적용해 보기
- 수: 린터 설정하고 기존 코드에 적용
- 목: docstring 자동 생성 도구 활용
- 금: 주간 회고 - 무엇을 배웠고, 무엇이 효과적이었는지 정리
```

**전략 2: 프로젝트 기반 학습**

단순히 기법을 학습하는 것보다 **실제 프로젝트에 적용**하면서 배우는 것이 훨씬 효과적입니다. 다음과 같은 미니 프로젝트를 추천합니다:

| 프로젝트 | 배울 수 있는 것 | 난이도 |
|----------|----------------|--------|
| 할일(TODO) 관리 앱 | CRUD, 파일 저장, CLI 설계 | 초급 |
| 블로그 생성기 | 마크다운 처리, HTML 변환 | 중급 |
| 데이터 분석 도구 | CSV 처리, 통계, 시각화 | 중급 |
| API 클라이언트 | HTTP 통신, JSON 파싱 | 중급 |
| 코드 품질 도구 | AST 분석, 린팅, 포맷팅 | 고급 |

**전략 3: 회고와 기록**

학습의 핵심은 **회고(Retrospective)**입니다. 매주 또는 매 프로젝트 종료 후 다음 질문에 답해 보세요:

- 이번에 새로 배운 것은 무엇인가?
- 어떤 프롬프트가 효과적이었고, 어떤 것이 아니었는가?
- 다음에 개선할 점은 무엇인가?
- 다른 사람에게 공유할 만한 팁이 있는가?

### 학습 자원 활용

바이브 코딩 실력을 키우기 위한 학습 자원을 유형별로 정리합니다:

| 유형 | 자원 | 활용 방법 |
|------|------|----------|
| 공식 문서 | AI 도구 공식 문서 (Claude, GPT 등) | 새로운 기능 및 API 변경사항 확인 |
| 블로그/글 | 기술 블로그, 개인 블로그 | 실전 사례와 노하우 학습 |
| 오픈소스 | GitHub 프로젝트 | 다른 사람의 코드와 구조 분석 |
| 커뮤니티 | 포럼, 디스코드, 슬랙 | 질문과 답변, 사례 공유 |
| 영상 | 유튜브, 강좌 플랫폼 | 시각적 학습, 라이브 코딩 참고 |

---

## 24.7 커뮤니티 활용

혼자 학습하는 것보다 커뮤니티에 참여하면 훨씬 빠르게 성장할 수 있습니다. 바이브 코딩 커뮤니티에서는 프롬프트 공유, 코드 리뷰, 문제 해결, 새로운 기법 토론이 활발하게 이루어집니다.

### 커뮤니티에서 얻을 수 있는 것

```
[커뮤니티 참여의 가치]

┌─────────────────────────────────────────────┐
│  다른 사람의 프롬프트를 보면서               │
│  → 새로운 프롬프트 작성법을 배운다           │
│                                              │
│  내 코드를 공유하고 피드백을 받으면서         │
│  → 몰랐던 문제점을 발견한다                  │
│                                              │
│  질문에 답변하면서                            │
│  → 내가 아는 것을 더 깊이 이해하게 된다      │
│                                              │
│  트렌드를 파악하면서                          │
│  → 새로운 도구와 기법을 빠르게 접한다        │
└─────────────────────────────────────────────┘
```

### 효과적인 커뮤니티 참여 방법

**방법 1: 질문 잘 하기**

좋은 질문은 좋은 답변을 이끌어냅니다. 질문할 때는 다음 구조를 따르세요:

```
[좋은 질문 구조]
1. 무엇을 하려고 했는가? (목표)
2. 어떻게 시도했는가? (프롬프트, 코드)
3. 무엇이 잘못되었는가? (에러 메시지, 예상과 다른 결과)
4. 어떤 환경인가? (Python 버전, OS, 도구 버전)
```

**방법 2: 배운 것 공유하기**

새로운 것을 배우면 블로그 글이나 커뮤니티 포스트로 정리하세요. "이런 문제를 이런 방식으로 해결했다"는 형태의 글이 가장 유용합니다. 글을 쓰는 과정에서 자신의 이해도 깊어집니다.

**방법 3: 오픈소스에 기여하기**

오픈소스 프로젝트에 기여하는 것은 실력을 키우는 가장 효과적인 방법 중 하나입니다. 처음에는 문서 수정, 오타 교정, 작은 버그 수정부터 시작하세요.

```
[오픈소스 기여 단계]
1단계: 문서 오류/오타 수정 (가장 쉬움)
2단계: 작은 버그 수정
3단계: 테스트 코드 추가
4단계: 새로운 기능 제안 및 구현
5단계: 코드 리뷰 참여
```

**방법 4: 스터디 그룹 운영하기**

2~5명 정도의 소규모 스터디 그룹을 운영하면 학습 동기가 유지되고, 다양한 관점에서 바이브 코딩을 배울 수 있습니다.

```
[주간 스터디 진행 예시]
- 각자 한 주간 만든 프로젝트 또는 코드 공유 (15분)
- 코드 리뷰 및 피드백 (20분)
- 이번 주 배운 프롬프트 기법 공유 (10분)
- 다음 주 목표 설정 (5분)
```

> **Tip:** 커뮤니티 참여는 "받기만 하는 것"이 아니라 "주고받는 것"입니다. 아직 초보라고 해도 자신만의 경험과 시행착오를 공유하면 다른 초보자에게 큰 도움이 됩니다.

---

## 24.8 모범 사례 종합: 바이브 코딩 체크리스트

이 장에서 배운 모범 사례를 하나의 체크리스트로 종합합니다. 프로젝트를 진행할 때 이 체크리스트를 참고하세요.

### 프로젝트 시작 시

```
[ ] README.md를 먼저 작성했는가?
[ ] 디렉토리 구조를 설계했는가?
[ ] Git 저장소를 초기화했는가?
[ ] .gitignore를 설정했는가?
[ ] 포맷팅 도구를 설정했는가?
[ ] 린터를 설정했는가?
```

### 기능 개발 시

```
[ ] 기능을 작은 단위로 나누었는가?
[ ] 프롬프트 템플릿을 활용하고 있는가?
[ ] AI 코드를 검토한 후 사용하고 있는가?
[ ] 테스트 코드를 함께 작성했는가?
[ ] docstring을 작성했는가?
[ ] 의미 있는 커밋 메시지를 작성했는가?
```

### 코드 품질

```
[ ] 포맷팅 도구를 실행했는가? (또는 자동 실행 설정)
[ ] 린터 경고가 0건인가?
[ ] 함수가 30줄을 넘지 않는가?
[ ] 매개변수가 5개를 넘지 않는가?
[ ] 네이밍 컨벤션(PEP 8)을 따르고 있는가?
[ ] bare except를 사용하지 않았는가?
```

### 학습과 성장

```
[ ] 새로운 기법을 시도해 보았는가?
[ ] 실패한 프롬프트를 기록했는가?
[ ] 배운 것을 공유했는가?
[ ] 다른 사람의 코드를 읽어보았는가?
[ ] 주간 회고를 작성했는가?
```

---

## 정리

이 장에서 배운 핵심 내용을 정리합니다.

### 핵심 개념 요약

| 주제 | 핵심 내용 |
|------|----------|
| 워크플로우 | 계획 → 프롬프트 → AI 요청 → 리뷰 → 품질 검사 → 커밋의 반복 |
| 자주 하는 실수 | 한 번에 많이 요청, 코드 미검토, 맥락 부재, 테스트 미작성 |
| 생산성 팁 | 프롬프트 라이브러리, "설명해줘" 습관, 작은 단위 개발, 실패 기록 |
| 코드 품질 | 자동 포맷팅 + 린터 + 코드 리뷰 체크리스트의 3단계 관리 |
| 문서화 | docstring(Google 스타일) + README(프로젝트 시작 시) + 인라인 주석 |
| 지속적 학습 | 매일 하나씩 새로운 기법 시도, 프로젝트 기반 학습, 회고와 기록 |
| 커뮤니티 | 질문 잘 하기, 배운 것 공유, 오픈소스 기여, 스터디 그룹 |

### 이 장에서 사용한 예제 파일

| 예제 | 파일 | 핵심 기능 |
|------|------|----------|
| 24-1 | `examples/python/chapter05/ex24_01_prompt_templates.py` | 프롬프트 템플릿 관리 시스템 |
| 24-2 | `examples/python/chapter05/ex24_02_code_review_checklist.py` | 자동 코드 리뷰 체크리스트 |
| 24-3 | `examples/python/chapter05/ex24_03_auto_formatting.py` | 코드 자동 포맷팅 도구 |
| 24-4 | `examples/python/chapter05/ex24_04_linter_check.py` | 통합 린터 검사기 |
| 24-5 | `examples/python/chapter05/ex24_05_docstring_writer.py` | docstring 검사 및 자동 생성 |
| 24-6 | `examples/python/chapter05/ex24_06_readme_template.py` | README 자동 생성 도구 |

### 기억할 명언

```
"좋은 코드는 자기 자신을 설명하지만,
 훌륭한 코드는 문서와 함께 설명한다."

"프롬프트를 한 번만 쓸 생각이라면 그냥 쓰세요.
 두 번 이상 쓸 거라면 템플릿으로 만드세요."

"완벽한 코드를 한 번에 만들려 하지 말고,
 동작하는 코드를 점점 더 좋게 만드세요."
```

---

## 연습 문제

### 연습 1: 나만의 프롬프트 라이브러리 만들기

예제 24-1의 `PromptLibrary` 클래스를 확장하여, 자신이 자주 사용하는 프롬프트 3가지를 템플릿으로 등록하세요.

**요구사항:**
- 최소 3개의 커스텀 템플릿 등록
- 각 템플릿에 적절한 변수 포함
- 템플릿 목록 출력 및 렌더링 테스트

**힌트:**
```python
my_template = PromptTemplate(
    name="내_템플릿",
    description="내가 자주 쓰는 프롬프트",
    template_str="여기에 ${변수}를 포함한 템플릿 작성"
)
```

### 연습 2: 코드 품질 개선

다음 코드에 예제 24-2의 `CodeReviewChecker`와 예제 24-4의 `PythonLinter`를 실행하여 문제를 찾고, 모든 경고가 0건이 될 때까지 코드를 개선하세요.

```python
class userData:
    def __init__(self, n, e, a, p, addr, comp):
        self.n = n
        self.e = e
        self.a = a
        self.p = p
        self.addr = addr
        self.comp = comp

    def ProcessUser(self):
        try:
            result = self.n + " (" + self.e + ")"
            return result
        except:
            return None
```

**목표:**
- 클래스명을 PascalCase로 변경
- 함수명을 snake_case로 변경
- 매개변수 수를 줄이기 (dataclass 또는 dict 활용)
- bare except를 구체적 예외로 변경
- 모든 함수/클래스에 docstring 추가

### 연습 3: README 자동 생성

예제 24-6의 `ReadmeGenerator`를 사용하여 여러분이 만든 (또는 만들 예정인) 프로젝트의 README.md를 생성하세요.

**요구사항:**
- `ProjectInfo`에 실제 프로젝트 정보 입력
- 최소 3개의 주요 기능 나열
- 사용법 예시 1개 이상 포함
- 디렉토리 구조 포함

### 연습 4: 주간 학습 계획 수립

이 장에서 배운 학습 전략을 바탕으로 자신만의 1주일 바이브 코딩 학습 계획을 수립하세요.

**포함 항목:**
- 매일 시도할 새로운 기법 1가지
- 만들어 볼 미니 프로젝트 1개
- 학습할 자원 (문서, 블로그, 영상) 목록
- 금요일 회고에서 답할 질문 3가지

### 연습 5: 코드 품질 자동화 파이프라인

예제 24-3(포맷터)과 예제 24-4(린터)를 조합하여, 소스 코드 파일을 입력받으면 "포맷팅 → 린팅 → 보고서 출력"을 한 번에 수행하는 통합 도구를 만들어 보세요.

**힌트:**
```python
def quality_pipeline(source: str, filename: str):
    """코드 품질 자동화 파이프라인"""
    # 1단계: 포맷팅
    formatter = CodeFormatter()
    formatted = formatter.format_source(source)

    # 2단계: 린팅
    linter = PythonLinter(formatted, filename)
    messages = linter.run()

    # 3단계: 보고서 출력
    print(f"포맷팅 완료, 린트 메시지 {len(messages)}건")
```

---

## 다음 장 예고

다음 Chapter 25부터는 **Part 6: 프로젝트**가 시작됩니다. 지금까지 배운 모든 기술을 총동원하여 실제로 동작하는 프로젝트를 처음부터 끝까지 만들어 봅니다. 첫 번째 프로젝트는 **CLI 할일 관리 앱**입니다. 프롬프트 작성, 코드 리뷰, 테스트, 문서화까지 이 장에서 배운 모범 사례를 실전에 적용하게 될 것입니다.
