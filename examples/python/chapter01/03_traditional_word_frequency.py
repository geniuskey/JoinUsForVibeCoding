# examples/python/chapter01/03_traditional_word_frequency.py
# 예제 3-3: [전통적 코딩] 단어 빈도 분석 직접 구현
# 개발자가 문자열 처리 로직을 직접 작성

def count_words(text):
    """텍스트에서 단어 빈도를 분석한다"""
    # 소문자로 변환
    text = text.lower()

    # 구두점 제거
    punctuation = ".,!?;:\"'()-"
    for char in punctuation:
        text = text.replace(char, "")

    # 공백 기준으로 분리
    words = text.split()

    # 빈도 딕셔너리 구성
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency


# 테스트 텍스트
sample_text = """
Python is a great language. Python is easy to learn.
Many developers love Python because Python is versatile.
"""

print("=== 전통적 코딩: 단어 빈도 분석 ===")
print(f"입력 텍스트: {sample_text.strip()}")
print()

result = count_words(sample_text)
print("단어 빈도:")
for word, count in result.items():
    print(f"  {word}: {count}")
