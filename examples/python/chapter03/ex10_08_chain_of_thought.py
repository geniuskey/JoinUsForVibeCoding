"""
예제 10-8: 단계별 사고 요청하기 (Chain of Thought)
===================================================
"단계별로 생각해서" 또는 "step by step"을 요청하면
AI가 문제를 체계적으로 분해하여 해결합니다.

프롬프트:
  "주어진 텍스트에서 가장 자주 등장하는 단어 TOP 5를 찾아줘.
   다음 단계를 따라 구현해줘:
   1단계: 텍스트를 소문자로 변환
   2단계: 특수문자를 제거
   3단계: 단어별로 분리
   4단계: 불용어(stopwords) 제거
   5단계: 단어 빈도 계산
   6단계: 상위 5개 추출
   각 단계의 중간 결과를 출력해줘."
"""

import re
from collections import Counter


# 한국어 불용어 목록 (간이)
STOPWORDS_KO = {
    "은", "는", "이", "가", "을", "를", "의", "에", "에서",
    "와", "과", "로", "으로", "도", "만", "까지", "부터",
    "그", "이", "저", "것", "수", "등", "및", "더", "한",
}


def find_top_words_step_by_step(text, top_n=5):
    """
    텍스트에서 가장 자주 등장하는 단어 TOP N을 단계별로 찾습니다.

    Args:
        text: 분석할 텍스트
        top_n: 상위 몇 개를 추출할지 (기본값 5)
    Returns:
        list[tuple]: (단어, 빈도) 리스트
    """
    print(f"[원본 텍스트]\n  {text[:80]}...\n")

    # 1단계: 소문자 변환
    step1 = text.lower()
    print(f"[1단계] 소문자 변환:")
    print(f"  {step1[:80]}...\n")

    # 2단계: 특수문자 제거 (한글, 영문, 숫자, 공백만 남김)
    step2 = re.sub(r'[^\w\s가-힣]', '', step1)
    print(f"[2단계] 특수문자 제거:")
    print(f"  {step2[:80]}...\n")

    # 3단계: 단어별로 분리
    step3 = step2.split()
    print(f"[3단계] 단어 분리 (총 {len(step3)}개):")
    print(f"  {step3[:10]} ...\n")

    # 4단계: 불용어 제거
    step4 = [w for w in step3 if w not in STOPWORDS_KO and len(w) > 1]
    removed = len(step3) - len(step4)
    print(f"[4단계] 불용어 제거 ({removed}개 제거, {len(step4)}개 남음):")
    print(f"  {step4[:10]} ...\n")

    # 5단계: 빈도 계산
    step5 = Counter(step4)
    print(f"[5단계] 단어 빈도 계산 (고유 단어 {len(step5)}개):")
    for word, count in step5.most_common(8):
        bar = "#" * count
        print(f"  {word:<12} : {count:>3}회 {bar}")
    print()

    # 6단계: 상위 N개 추출
    step6 = step5.most_common(top_n)
    print(f"[6단계] 상위 {top_n}개 추출:")
    for rank, (word, count) in enumerate(step6, 1):
        print(f"  {rank}위: {word} ({count}회)")

    return step6


# ── 실행 ──
if __name__ == "__main__":
    sample_text = """
    바이브 코딩은 AI와 함께 프로그래밍하는 새로운 방식입니다.
    바이브 코딩에서는 프롬프트를 잘 작성하는 것이 중요합니다.
    프롬프트 엔지니어링은 AI에게 명확한 지시를 전달하는 기술입니다.
    좋은 프롬프트는 구체적이고 맥락을 포함해야 합니다.
    바이브 코딩을 통해 개발 생산성을 크게 높일 수 있습니다.
    AI 어시스턴트는 프롬프트의 품질에 따라 결과가 달라집니다.
    프롬프트를 작성할 때는 역할, 맥락, 형식을 지정해야 합니다.
    바이브 코딩의 핵심은 사람과 AI의 협업입니다.
    프롬프트 엔지니어링을 배우면 AI를 더 효과적으로 활용할 수 있습니다.
    함께 바이브 코딩을 배워봅시다!
    """

    print("=" * 60)
    print("단계별 사고(Chain of Thought) 데모")
    print("=" * 60)
    print()
    result = find_top_words_step_by_step(sample_text)
    print()
    print("최종 결과:", result)
