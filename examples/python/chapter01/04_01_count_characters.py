# examples/python/chapter01/04_01_count_characters.py
# AI에게 요청한 결과물: 문자열의 글자 수를 세는 프로그램

def count_characters(text):
    """문자열의 각 글자 빈도를 세는 함수"""
    char_count = {}
    for char in text:
        if char == ' ':
            continue  # 공백은 건너뛰기
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count


def display_result(char_count):
    """결과를 보기 좋게 출력하는 함수"""
    print("=== 글자 빈도 분석 결과 ===")
    for char, count in sorted(char_count.items(), key=lambda x: x[1], reverse=True):
        bar = '*' * count
        print(f"  '{char}': {count}번 {bar}")
    print(f"\n총 고유 글자 수: {len(char_count)}개")


if __name__ == "__main__":
    text = "바이브 코딩은 재미있다"
    print(f"입력 문자열: \"{text}\"\n")
    result = count_characters(text)
    display_result(result)
