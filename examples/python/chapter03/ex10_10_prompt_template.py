"""
예제 10-10: 프롬프트 템플릿 활용
==================================
자주 사용하는 프롬프트를 템플릿화하면
일관된 품질의 결과를 반복적으로 얻을 수 있습니다.

프롬프트 템플릿:
  "함수 생성 템플릿을 만들어줘. 다음 변수를 채워 넣으면
   일관된 형식의 프롬프트가 생성되도록 해줘:
   - {function_name}: 함수 이름
   - {description}: 함수 설명
   - {parameters}: 매개변수 목록
   - {return_type}: 반환 타입
   - {constraints}: 제약조건"
"""


class PromptTemplate:
    """
    재사용 가능한 프롬프트 템플릿 클래스.

    템플릿 문자열에 {변수명} 형식의 플레이스홀더를 넣고,
    render() 메서드로 값을 채워 넣습니다.
    """

    def __init__(self, name, template):
        self.name = name
        self.template = template

    def render(self, **kwargs):
        """템플릿에 값을 채워 넣어 완성된 프롬프트를 반환합니다."""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"누락된 변수: {e}")

    def __repr__(self):
        return f"PromptTemplate('{self.name}')"


# ── 미리 정의된 템플릿들 ──

FUNCTION_TEMPLATE = PromptTemplate(
    name="함수 생성",
    template="""당신은 시니어 Python 개발자입니다.
다음 요구사항에 맞는 함수를 작성해주세요.

함수명: {function_name}
설명: {description}
매개변수: {parameters}
반환 타입: {return_type}
제약조건: {constraints}

코드에 타입 힌트와 docstring을 포함해주세요."""
)

CODE_REVIEW_TEMPLATE = PromptTemplate(
    name="코드 리뷰",
    template="""당신은 코드 리뷰 전문가입니다.
다음 코드를 검토하고 개선점을 제안해주세요.

언어: {language}
코드 목적: {purpose}
검토 초점: {focus}

```{language}
{code}
```

다음 관점에서 피드백을 주세요:
1. 코드 품질
2. 성능
3. 보안
4. 가독성"""
)

BUG_FIX_TEMPLATE = PromptTemplate(
    name="버그 수정",
    template="""다음 코드에서 버그를 찾아 수정해주세요.

증상: {symptom}
기대 동작: {expected}
실제 동작: {actual}

```python
{code}
```

수정된 코드와 함께 버그의 원인을 설명해주세요."""
)


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 60)
    print("프롬프트 템플릿 활용 데모")
    print("=" * 60)

    # 1. 함수 생성 템플릿
    print("\n[템플릿 1] 함수 생성")
    print("-" * 40)
    prompt1 = FUNCTION_TEMPLATE.render(
        function_name="calculate_discount",
        description="상품 가격과 할인율을 받아 할인된 가격을 계산",
        parameters="price: float, discount_rate: float (0~100)",
        return_type="float (할인된 가격)",
        constraints="할인율은 0~100 사이, 음수 가격 불허",
    )
    print(prompt1)

    # 2. 코드 리뷰 템플릿
    print("\n[템플릿 2] 코드 리뷰")
    print("-" * 40)
    prompt2 = CODE_REVIEW_TEMPLATE.render(
        language="python",
        purpose="사용자 비밀번호 검증",
        focus="보안 취약점",
        code='def check(pw):\n    return pw == "admin123"',
    )
    print(prompt2)

    # 3. 버그 수정 템플릿
    print("\n[템플릿 3] 버그 수정")
    print("-" * 40)
    prompt3 = BUG_FIX_TEMPLATE.render(
        symptom="빈 리스트 입력 시 ZeroDivisionError 발생",
        expected="빈 리스트일 경우 0.0 반환",
        actual="ZeroDivisionError 예외 발생",
        code="def average(nums):\n    return sum(nums) / len(nums)",
    )
    print(prompt3)

    # 4. 템플릿의 장점 요약
    print("\n" + "=" * 60)
    print("[프롬프트 템플릿의 장점]")
    print("  1. 일관성 — 매번 같은 구조로 요청")
    print("  2. 효율성 — 변수만 바꿔서 재사용")
    print("  3. 품질    — 검증된 프롬프트 구조 반복 활용")
    print("  4. 공유    — 팀원과 템플릿 공유 가능")
