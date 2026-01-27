"""
예제 12-2: 각 줄 주석 추가 요청
================================
AI가 생성한 코드에 줄별 주석을 추가하도록 요청하는 예제입니다.

프롬프트: "각 줄마다 주석을 달아서 설명해줘"
→ 코드의 동작을 한 줄씩 이해할 수 있게 됩니다.
"""


# --- 주석 없는 원본 코드 ---
def caesar_cipher_original(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            result += char
    return result


# --- "각 줄마다 주석을 달아줘" 요청 후 개선된 코드 ---
def caesar_cipher_commented(text, shift):
    # 암호화된 결과를 저장할 빈 문자열
    result = ""

    # 입력 텍스트의 각 문자를 순회
    for char in text:
        # 알파벳 문자인 경우에만 암호화 수행
        if char.isalpha():
            # 대문자면 'A'(65), 소문자면 'a'(97)를 기준점으로 설정
            base = ord('A') if char.isupper() else ord('a')

            # 현재 문자를 기준점 기준 상대 위치로 변환 후 shift만큼 이동
            # % 26으로 알파벳 범위(0~25) 내에서 순환되도록 처리
            shifted = (ord(char) - base + shift) % 26

            # 이동된 위치를 다시 문자로 변환하여 결과에 추가
            result += chr(base + shifted)
        else:
            # 알파벳이 아닌 문자(공백, 숫자, 특수문자)는 그대로 유지
            result += char

    # 완성된 암호화 문자열 반환
    return result


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-2] 각 줄 주석 추가 요청")
    print("=" * 55)

    original_text = "Hello, Vibe Coding!"
    shift_amount = 3

    print(f"\n원본 텍스트: {original_text}")
    print(f"시프트 값:   {shift_amount}")
    print()

    # 두 함수 모두 동일한 결과를 냄
    result1 = caesar_cipher_original(original_text, shift_amount)
    result2 = caesar_cipher_commented(original_text, shift_amount)

    print(f"[주석 없는 버전] 암호화: {result1}")
    print(f"[주석 있는 버전] 암호화: {result2}")
    print()

    # 복호화 (음수 시프트)
    decrypted = caesar_cipher_commented(result2, -shift_amount)
    print(f"복호화 결과: {decrypted}")
    print()

    # 비교 표
    print("[비교: 주석 전 vs 후]")
    print("-" * 55)
    print("주석 없는 코드:")
    print('  shifted = (ord(char) - base + shift) % 26')
    print()
    print("주석 있는 코드:")
    print('  # 현재 문자를 기준점 기준 상대 위치로 변환 후 shift만큼 이동')
    print('  # % 26으로 알파벳 범위(0~25) 내에서 순환되도록 처리')
    print('  shifted = (ord(char) - base + shift) % 26')
    print()
    print("Tip: 주석이 있으면 나중에 코드를 다시 볼 때")
    print("     훨씬 빠르게 이해할 수 있습니다.")
