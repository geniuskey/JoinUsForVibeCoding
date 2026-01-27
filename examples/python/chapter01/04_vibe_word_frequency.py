# examples/python/chapter01/04_vibe_word_frequency.py
# 예제 3-4: [바이브 코딩] 단어 빈도 분석 AI에게 요청
#
# 프롬프트: "텍스트에서 단어 빈도를 분석하는 프로그램을 만들어줘.
#           빈도순으로 정렬하고, 막대 그래프로 보여줘.
#           불용어(the, is, a 등)는 제외해줘."
#
# 아래는 AI가 생성한 결과물입니다.

import re
from collections import Counter


# 영어 불용어 목록
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "being", "to", "of", "in", "for", "on", "with", "at", "by",
    "it", "and", "or", "but", "not", "that", "this", "from"
}


def analyze_word_frequency(text, top_n=10, exclude_stop_words=True):
    """
    텍스트의 단어 빈도를 분석하고 시각화합니다.

    Args:
        text: 분석할 텍스트
        top_n: 상위 N개 단어만 표시
        exclude_stop_words: 불용어 제외 여부
    Returns:
        빈도순 정렬된 (단어, 빈도) 리스트
    """
    # 소문자 변환 및 단어 추출 (정규표현식 사용)
    words = re.findall(r'[a-z]+', text.lower())

    # 불용어 필터링
    if exclude_stop_words:
        words = [w for w in words if w not in STOP_WORDS]

    # 빈도 계산 및 정렬
    counter = Counter(words)
    top_words = counter.most_common(top_n)

    return top_words


def display_bar_chart(word_counts, bar_char="█"):
    """단어 빈도를 막대 그래프로 출력합니다."""
    if not word_counts:
        print("  (표시할 데이터 없음)")
        return

    max_count = max(count for _, count in word_counts)
    max_word_len = max(len(word) for word, _ in word_counts)
    bar_width = 30

    for word, count in word_counts:
        bar_length = int((count / max_count) * bar_width)
        bar = bar_char * bar_length
        print(f"  {word:<{max_word_len}} | {bar} ({count})")


# 실행
sample_text = """
Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.
"""

print("=== 바이브 코딩: 단어 빈도 분석 (시각화 포함) ===")
print(f"입력 텍스트: {sample_text.strip()}")
print()

results = analyze_word_frequency(sample_text)

print("단어 빈도 (불용어 제외, 빈도순):")
display_bar_chart(results)
print()
print(f"총 {len(results)}개 단어 분석 완료")
