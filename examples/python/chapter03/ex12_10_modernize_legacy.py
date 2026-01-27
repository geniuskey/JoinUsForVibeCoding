"""
예제 12-10: 실습 — 레거시 코드 현대화
=======================================
오래된 스타일의 Python 코드를 현대적인 Python으로 업데이트하는 실습입니다.

프롬프트: "이 코드가 옛날 스타일이야. 최신 Python 스타일로 바꿔줘"
→ string %, .format(), 구식 패턴을 f-string, 타입 힌트, 최신 문법으로 변환합니다.
"""


# ====================================================================
# 개선 전: 옛날 스타일 Python (Python 2 시대 습관)
# ====================================================================
def run_legacy_version():
    """레거시 스타일 코드"""
    # 1. 문자열 포맷: % 연산자
    name = "김바이브"
    age = 25
    greeting = "안녕하세요, %s님! 나이는 %d세입니다." % (name, age)
    print(greeting)

    # 2. 문자열 결합: + 연산자
    items = ["사과", "바나나", "딸기"]
    result = ""
    for i in range(len(items)):
        result = result + str(i + 1) + ". " + items[i] + "\n"
    print(result)

    # 3. 딕셔너리 존재 확인: has_key 대체 패턴
    config = {"host": "localhost", "port": 8080}
    if config.has_key("host") if hasattr(config, 'has_key') else "host" in config:
        host = config["host"]
    else:
        host = "127.0.0.1"

    if config.has_key("timeout") if hasattr(config, 'has_key') else "timeout" in config:
        timeout = config["timeout"]
    else:
        timeout = 30
    print("서버: %s, 타임아웃: %d" % (host, timeout))

    # 4. 리스트 생성: 수동 루프
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_squares = []
    for n in numbers:
        if n % 2 == 0:
            even_squares.append(n * n)
    print("짝수의 제곱: %s" % str(even_squares))

    # 5. 파일 처리: 수동 close (시뮬레이션)
    print("파일 처리: 수동 open/close 패턴 (시뮬레이션)")

    # 6. None 비교
    value = None
    if value == None:
        print("값이 None입니다 (== 비교)")

    # 7. 타입 확인
    data = "hello"
    if type(data) == str:
        print("문자열 타입입니다 (type() == 비교)")


# ====================================================================
# 개선 후: 현대적인 Python 스타일 (Python 3.10+)
# ====================================================================
def run_modern_version():
    """최신 Python 스타일 코드"""
    # 1. 문자열 포맷: f-string
    name = "김바이브"
    age = 25
    greeting = f"안녕하세요, {name}님! 나이는 {age}세입니다."
    print(greeting)

    # 2. 문자열 결합: enumerate + f-string + join
    items = ["사과", "바나나", "딸기"]
    result = "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))
    print(result)
    print()

    # 3. 딕셔너리 존재 확인: .get() 메서드
    config = {"host": "localhost", "port": 8080}
    host = config.get("host", "127.0.0.1")
    timeout = config.get("timeout", 30)
    print(f"서버: {host}, 타임아웃: {timeout}")

    # 4. 리스트 생성: 리스트 컴프리헨션
    numbers = range(1, 11)
    even_squares = [n ** 2 for n in numbers if n % 2 == 0]
    print(f"짝수의 제곱: {even_squares}")

    # 5. 파일 처리: with 문 (컨텍스트 매니저)
    print("파일 처리: with 문 사용 (자동 close)")

    # 6. None 비교: is 연산자
    value = None
    if value is None:
        print("값이 None입니다 (is 비교)")

    # 7. 타입 확인: isinstance()
    data = "hello"
    if isinstance(data, str):
        print("문자열 타입입니다 (isinstance 사용)")


# --- 추가: 타입 힌트가 적용된 현대적 함수 ---
def calculate_bmi(weight_kg: float, height_m: float) -> dict[str, float | str]:
    """
    BMI를 계산합니다 (타입 힌트 포함).

    Args:
        weight_kg: 체중 (kg)
        height_m: 키 (m)

    Returns:
        BMI 값과 판정 결과를 담은 딕셔너리
    """
    bmi = weight_kg / (height_m ** 2)

    # match-case 대신 딕셔너리 기반 판정 (호환성 고려)
    if bmi < 18.5:
        category = "저체중"
    elif bmi < 25.0:
        category = "정상"
    elif bmi < 30.0:
        category = "과체중"
    else:
        category = "비만"

    return {"bmi": round(bmi, 1), "category": category}


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-10] 레거시 코드 현대화")
    print("=" * 55)

    print("\n[개선 전] 레거시 Python 스타일")
    print("-" * 40)
    run_legacy_version()

    print()
    print("[개선 후] 현대적 Python 스타일")
    print("-" * 40)
    run_modern_version()

    print()
    print("[추가] 타입 힌트 적용 함수 예시")
    print("-" * 40)
    result = calculate_bmi(70.0, 1.75)
    print(f"  BMI: {result['bmi']}, 판정: {result['category']}")

    print()
    print("[현대화 변환 요약]")
    print("-" * 55)
    conversions = [
        ("문자열 포맷", '"Hello %s" % name', 'f"Hello {name}"'),
        ("문자열 결합", 'result + str(i)', 'f"{i}. {item}"'),
        ("딕셔너리 접근", 'if "key" in d: d["key"]', 'd.get("key", default)'),
        ("리스트 생성", "for + append", "[x for x in ...]"),
        ("파일 처리", "f = open(); f.close()", "with open() as f:"),
        ("None 비교", "if x == None", "if x is None"),
        ("타입 확인", "type(x) == str", "isinstance(x, str)"),
        ("타입 힌트", "def func(x):", "def func(x: int) -> str:"),
    ]
    print(f"  {'항목':<14} {'레거시':<28} {'현대적'}")
    print(f"  {'-'*14} {'-'*28} {'-'*25}")
    for item, legacy, modern in conversions:
        print(f"  {item:<14} {legacy:<28} {modern}")

    print()
    print("Tip: AI에게 '최신 Python 스타일로 변환해줘'라고 요청하면")
    print("     f-string, 타입 힌트, 컨텍스트 매니저 등을 자동 적용합니다.")
