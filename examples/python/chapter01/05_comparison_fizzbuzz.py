# examples/python/chapter01/05_comparison_fizzbuzz.py
# 예제 3-5: [비교] 같은 문제, 다른 접근법 - FizzBuzz
# 전통적 코딩과 바이브 코딩으로 각각 구현한 결과를 비교합니다.

# ─── 방법 1: 전통적 코딩 ───
# 개발자가 조건문 로직을 직접 작성
def fizzbuzz_traditional(n):
    """전통적 방식: 직접 조건문 작성"""
    results = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            results.append("FizzBuzz")
        elif i % 3 == 0:
            results.append("Fizz")
        elif i % 5 == 0:
            results.append("Buzz")
        else:
            results.append(str(i))
    return results


# ─── 방법 2: 바이브 코딩 ───
# 프롬프트: "FizzBuzz를 만들어줘. 규칙을 쉽게 추가할 수 있게 해줘."
# AI가 생성한 코드: 확장 가능한 구조
def fizzbuzz_vibe(n, rules=None):
    """바이브 코딩 방식: 확장 가능한 규칙 기반 구조"""
    if rules is None:
        rules = [(3, "Fizz"), (5, "Buzz")]

    results = []
    for i in range(1, n + 1):
        output = ""
        for divisor, word in rules:
            if i % divisor == 0:
                output += word
        results.append(output if output else str(i))
    return results


# ─── 비교 실행 ───
print("=== FizzBuzz 비교: 전통적 코딩 vs 바이브 코딩 ===\n")

n = 20

# 전통적 방식 실행
print("[전통적 코딩] 결과:")
traditional = fizzbuzz_traditional(n)
print(", ".join(traditional))

print()

# 바이브 코딩 방식 실행 (기본 규칙)
print("[바이브 코딩] 기본 규칙 결과:")
vibe_basic = fizzbuzz_vibe(n)
print(", ".join(vibe_basic))

# 바이브 코딩 방식 실행 (규칙 확장)
print()
print("[바이브 코딩] 규칙 확장 (7=Jazz 추가) 결과:")
custom_rules = [(3, "Fizz"), (5, "Buzz"), (7, "Jazz")]
vibe_extended = fizzbuzz_vibe(n, rules=custom_rules)
print(", ".join(vibe_extended))

print()
print("─" * 50)
print("비교 요약:")
print("  전통적 코딩: 간단명료하지만 규칙 추가 시 코드 수정 필요")
print("  바이브 코딩:  확장 가능한 구조로 규칙 추가가 쉬움")
