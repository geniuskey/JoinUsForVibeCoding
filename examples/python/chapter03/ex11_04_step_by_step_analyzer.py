# examples/python/chapter03/ex11_04_step_by_step_analyzer.py
# 예제 11-4: 단계별 기능 추가 대화
#
# 텍스트 분석기를 단계별로 만들어가는 과정을 보여줍니다.
# 1단계: 단어 수 세기 → 2단계: 문장 수 세기 → 3단계: 읽기 시간 계산

import sys


# ============================================================
# 샘플 텍스트
# ============================================================

SAMPLE_TEXT = """바이브 코딩은 AI와 함께 프로그래밍하는 새로운 방식입니다.
기존의 코딩은 개발자가 모든 코드를 직접 작성해야 했습니다. 하지만 바이브 코딩에서는
자연어로 원하는 것을 설명하면 AI가 코드를 생성합니다.

이 방식의 핵심은 대화입니다. 한 번에 완벽한 코드를 만들 필요가 없습니다.
AI와 대화하며 조금씩 개선해 나가면 됩니다. 마치 동료 개발자와 페어 프로그래밍을
하는 것처럼 말입니다.

바이브 코딩을 시작하려면 먼저 AI 도구를 설치해야 합니다. Claude Code나
GitHub Copilot 같은 도구를 사용할 수 있습니다. 도구가 준비되면 터미널을 열고
AI에게 첫 번째 프로그램을 요청해 보세요."""


# ============================================================
# [1단계 대화] "텍스트에서 단어 수를 세는 프로그램 만들어줘"
# ============================================================

def step1_word_count(text):
    """1단계: 단어 수 세기"""
    words = text.split()
    word_count = len(words)
    return word_count


# ============================================================
# [2단계 대화] "여기에 문장 수도 세어줘"
# ============================================================

def step2_sentence_count(text):
    """2단계: 문장 수 세기 (기존 기능 유지 + 확장)"""
    words = text.split()
    word_count = len(words)

    # 문장 구분자: . ! ?
    sentence_count = 0
    for char in text:
        if char in ".!?":
            sentence_count += 1

    return word_count, sentence_count


# ============================================================
# [3단계 대화] "읽기 시간도 계산해줘"
# ============================================================

def step3_full_analysis(text):
    """3단계: 읽기 시간 계산 (기존 기능 유지 + 확장)"""
    words = text.split()
    word_count = len(words)

    sentence_count = 0
    for char in text:
        if char in ".!?":
            sentence_count += 1

    # 한국어 평균 읽기 속도: 분당 약 500자
    char_count = len(text.replace(" ", "").replace("\n", ""))
    reading_time_seconds = (char_count / 500) * 60
    reading_time_min = int(reading_time_seconds // 60)
    reading_time_sec = int(reading_time_seconds % 60)

    # 평균 문장 길이
    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

    return {
        "단어 수": word_count,
        "문장 수": sentence_count,
        "글자 수(공백 제외)": char_count,
        "평균 문장 길이(단어)": round(avg_words_per_sentence, 1),
        "예상 읽기 시간": f"{reading_time_min}분 {reading_time_sec}초",
    }


# ============================================================
# 단계별 진행 과정 시연
# ============================================================

def demonstrate_steps():
    """단계별 개발 과정을 순서대로 보여줍니다"""
    text = SAMPLE_TEXT

    print("=" * 55)
    print("  텍스트 분석기 - 단계별 대화 개발 과정")
    print("=" * 55)

    # 분석 대상 텍스트 미리보기
    preview = text[:80].replace("\n", " ")
    print(f"\n  분석 대상 텍스트: \"{preview}...\"")
    print(f"  (전체 {len(text)}자)")

    # 1단계
    print("\n" + "─" * 55)
    print("  [1단계 대화]")
    print('  사용자: "텍스트에서 단어 수를 세는 프로그램 만들어줘"')
    print("─" * 55)
    wc = step1_word_count(text)
    print(f"  결과: 단어 수 = {wc}개")

    # 2단계
    print("\n" + "─" * 55)
    print("  [2단계 대화]")
    print('  사용자: "여기에 문장 수도 세어줘"')
    print("─" * 55)
    wc, sc = step2_sentence_count(text)
    print(f"  결과: 단어 수 = {wc}개, 문장 수 = {sc}개")

    # 3단계
    print("\n" + "─" * 55)
    print("  [3단계 대화]")
    print('  사용자: "읽기 시간도 계산해줘"')
    print("─" * 55)
    analysis = step3_full_analysis(text)

    print("\n  ┌─── 텍스트 분석 결과 ──────────────┐")
    for key, value in analysis.items():
        print(f"  │  {key}: {value}")
    print("  └────────────────────────────────────┘")

    # 교훈
    print("\n" + "─" * 55)
    print("  단계별 대화의 장점:")
    print("  • 각 단계에서 결과를 확인하고 방향을 조절할 수 있습니다")
    print("  • AI가 이전 코드 구조를 유지하면서 기능을 추가합니다")
    print("  • 문제가 생기면 해당 단계만 수정하면 됩니다")
    print("  • 최종 결과물이 점진적으로 완성됩니다")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--step1":
        print(f"단어 수: {step1_word_count(SAMPLE_TEXT)}개")
    elif len(sys.argv) > 1 and sys.argv[1] == "--step2":
        wc, sc = step2_sentence_count(SAMPLE_TEXT)
        print(f"단어 수: {wc}개, 문장 수: {sc}개")
    elif len(sys.argv) > 1 and sys.argv[1] == "--step3":
        result = step3_full_analysis(SAMPLE_TEXT)
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        demonstrate_steps()
