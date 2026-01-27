"""
예제 10-7: Few-shot 예시 제공하기
==================================
입력/출력 예시를 미리 보여주면 AI가 패턴을 학습하여
정확한 코드를 생성합니다.

프롬프트:
  "다음 변환 규칙에 따라 문자열을 변환하는 함수를 작성해줘.

   입력 예시 → 출력 예시:
   'hello world' → 'Hello_World'
   'vibe coding is fun' → 'Vibe_Coding_Is_Fun'
   'ai assistant' → 'Ai_Assistant'

   규칙: 각 단어의 첫 글자를 대문자로 바꾸고 공백을 언더스코어로 연결"
"""


def convert_to_pascal_snake(text):
    """
    문자열을 PascalSnake 형식으로 변환합니다.

    각 단어의 첫 글자를 대문자로, 단어 사이는 언더스코어로 연결합니다.

    Args:
        text: 변환할 문자열
    Returns:
        변환된 문자열
    """
    words = text.strip().split()
    capitalized = [word.capitalize() for word in words]
    return "_".join(capitalized)


# ── Few-shot 예시들로 검증 ──
FEW_SHOT_EXAMPLES = [
    ("hello world", "Hello_World"),
    ("vibe coding is fun", "Vibe_Coding_Is_Fun"),
    ("ai assistant", "Ai_Assistant"),
]


def verify_with_examples(func, examples):
    """Few-shot 예시로 함수 결과를 검증합니다."""
    print(f"{'입력':<30} {'기대 출력':<25} {'실제 출력':<25} {'결과'}")
    print("-" * 90)

    all_passed = True
    for input_val, expected in examples:
        actual = func(input_val)
        passed = actual == expected
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"'{input_val}'  {'':<{27-len(input_val)}} "
              f"'{expected}'  {'':<{22-len(expected)}} "
              f"'{actual}'  {'':<{22-len(actual)}} "
              f"{status}")

    return all_passed


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 90)
    print("Few-shot 예시 제공하기")
    print("=" * 90)
    print()
    print("프롬프트에 포함한 입출력 예시:")
    for inp, out in FEW_SHOT_EXAMPLES:
        print(f"  '{inp}' → '{out}'")
    print()

    print("[Few-shot 예시로 검증]")
    all_ok = verify_with_examples(convert_to_pascal_snake, FEW_SHOT_EXAMPLES)
    print()

    # 추가 테스트 (예시에 없던 입력)
    additional = [
        ("prompt engineering basics", "Prompt_Engineering_Basics"),
        ("python", "Python"),
        ("machine learning model", "Machine_Learning_Model"),
    ]

    print("[추가 테스트 — 예시에 없던 입력]")
    verify_with_examples(convert_to_pascal_snake, additional)
    print()

    if all_ok:
        print("모든 Few-shot 예시가 통과했습니다!")
    else:
        print("일부 예시가 실패했습니다. 함수를 수정해야 합니다.")
