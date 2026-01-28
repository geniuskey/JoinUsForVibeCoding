#!/usr/bin/env python3
"""
예제 24-01: 효과적인 프롬프트 템플릿
- string.Template을 활용한 프롬프트 템플릿 시스템
- 바이브 코딩에서 반복적으로 사용하는 프롬프트를 체계적으로 관리
"""

from string import Template
from datetime import datetime
import json
import textwrap


# ============================================================
# 1. 기본 프롬프트 템플릿 클래스
# ============================================================

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
        # Template 패턴에서 변수명 추출
        import re
        pattern = r'\$\{?([a-zA-Z_][a-zA-Z0-9_]*)\}?'
        return list(set(re.findall(pattern, self.template.template)))

    def __repr__(self):
        return f"PromptTemplate(name='{self.name}', vars={self.get_variables()})"


# ============================================================
# 2. 프롬프트 템플릿 라이브러리
# ============================================================

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

    def export_json(self) -> str:
        """템플릿 라이브러리를 JSON으로 내보내기"""
        data = {}
        for name, tmpl in self.templates.items():
            data[name] = {
                "description": tmpl.description,
                "template": tmpl.template.template,
                "variables": tmpl.get_variables(),
                "created_at": tmpl.created_at,
            }
        return json.dumps(data, ensure_ascii=False, indent=2)


# ============================================================
# 3. 미리 정의된 바이브 코딩용 프롬프트 템플릿들
# ============================================================

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

# 코드 리뷰 요청 템플릿
CODE_REVIEW = PromptTemplate(
    name="코드_리뷰",
    description="코드 리뷰를 요청하는 프롬프트",
    template_str=textwrap.dedent("""\
        다음 코드를 리뷰해 주세요:

        ## 파일: ${filename}
        ## 언어: ${language}

        ```${language}
        ${code}
        ```

        ## 리뷰 관점
        ${review_focus}

        다음 항목을 중심으로 검토해 주세요:
        1. 코드 품질 및 가독성
        2. 잠재적 버그
        3. 성능 이슈
        4. 보안 취약점
        5. 개선 제안
    """)
)

# 버그 수정 요청 템플릿
BUG_FIX = PromptTemplate(
    name="버그_수정",
    description="버그 수정을 요청하는 프롬프트",
    template_str=textwrap.dedent("""\
        다음 버그를 수정해 주세요:

        ## 증상
        ${symptom}

        ## 재현 방법
        ${reproduce_steps}

        ## 예상 동작
        ${expected}

        ## 실제 동작
        ${actual}

        ## 관련 코드
        ```${language}
        ${code}
        ```

        ## 환경
        - OS: ${os_info}
        - 버전: ${version}
    """)
)

# 리팩토링 요청 템플릿
REFACTORING = PromptTemplate(
    name="리팩토링",
    description="코드 리팩토링을 요청하는 프롬프트",
    template_str=textwrap.dedent("""\
        다음 코드를 리팩토링해 주세요:

        ## 대상 코드
        ```${language}
        ${code}
        ```

        ## 리팩토링 목표
        ${goal}

        ## 적용할 패턴/원칙
        ${patterns}

        ## 유지해야 할 사항
        - 기존 인터페이스(함수 시그니처) 유지
        - 동작 변경 없음
        - 테스트 통과 보장
    """)
)


# ============================================================
# 메인: 데모 실행
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  예제 24-01: 효과적인 프롬프트 템플릿 시스템")
    print("=" * 60)

    # 1. 프롬프트 라이브러리 생성 및 템플릿 등록
    library = PromptLibrary()
    library.add(FEATURE_REQUEST)
    library.add(CODE_REVIEW)
    library.add(BUG_FIX)
    library.add(REFACTORING)

    # 2. 등록된 템플릿 목록 출력
    print("\n📋 등록된 프롬프트 템플릿 목록:")
    print("-" * 40)
    for info in library.list_templates():
        print(f"  이름: {info['이름']}")
        print(f"  설명: {info['설명']}")
        print(f"  변수: {', '.join(info['변수'])}")
        print(f"  ---")

    # 3. 기능 구현 프롬프트 생성 예시
    print("\n" + "=" * 60)
    print("  [데모 1] 기능 구현 프롬프트 생성")
    print("=" * 60)

    feature_prompt = library.get("기능_구현").render(
        feature_name="사용자 로그인 시스템",
        description="이메일과 비밀번호로 로그인하는 기능을 구현합니다.",
        language="Python",
        framework="Flask",
        requirements="- 이메일 형식 검증\n- 비밀번호 해싱\n- JWT 토큰 발급"
    )
    print(feature_prompt)

    # 4. 코드 리뷰 프롬프트 생성 예시
    print("\n" + "=" * 60)
    print("  [데모 2] 코드 리뷰 프롬프트 생성")
    print("=" * 60)

    sample_code = '''\
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item["price"] * item["qty"]
    return total'''

    review_prompt = library.get("코드_리뷰").render(
        filename="cart.py",
        language="python",
        code=sample_code,
        review_focus="성능 최적화 및 에러 처리"
    )
    print(review_prompt)

    # 5. 커스텀 템플릿 추가 예시
    print("\n" + "=" * 60)
    print("  [데모 3] 커스텀 템플릿 추가 및 사용")
    print("=" * 60)

    custom = PromptTemplate(
        name="테스트_작성",
        description="테스트 코드 작성을 요청하는 프롬프트",
        template_str=textwrap.dedent("""\
            다음 함수에 대한 테스트 코드를 작성해 주세요:

            ## 대상 함수
            ```${language}
            ${function_code}
            ```

            ## 테스트 프레임워크: ${test_framework}

            ## 테스트 케이스
            ${test_cases}
        """)
    )
    library.add(custom)

    test_prompt = library.get("테스트_작성").render(
        language="python",
        function_code="def add(a, b):\n    return a + b",
        test_framework="unittest",
        test_cases="- 양수 + 양수\n- 음수 + 음수\n- 0 포함\n- 큰 수 연산"
    )
    print(test_prompt)

    # 6. JSON 내보내기
    print("\n" + "=" * 60)
    print("  [데모 4] 템플릿 라이브러리 JSON 내보내기 (일부)")
    print("=" * 60)

    exported = json.loads(library.export_json())
    # 첫 번째 템플릿만 간략히 표시
    first_key = list(exported.keys())[0]
    summary = {
        "이름": first_key,
        "설명": exported[first_key]["description"],
        "변수": exported[first_key]["variables"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    print(f"\n총 {len(exported)}개의 템플릿이 라이브러리에 등록되어 있습니다.")
    print("\n모범 사례: 자주 사용하는 프롬프트를 템플릿으로 관리하면")
    print("일관성 있고 효과적인 바이브 코딩이 가능합니다!")
