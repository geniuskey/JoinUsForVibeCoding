# examples/python/chapter01/06_hybrid_temperature.py
# 예제 3-6: [하이브리드] AI 초안 + 수동 개선
# 1단계: AI가 생성한 온도 변환기 초안
# 2단계: 개발자가 입력 검증 및 에러 처리를 수동으로 추가

# ─── 1단계: AI 생성 초안 (기본 기능) ───
def convert_temperature_draft(value, from_unit, to_unit):
    """AI가 생성한 초안: 기본 온도 변환"""
    if from_unit == "C" and to_unit == "F":
        return value * 9 / 5 + 32
    elif from_unit == "F" and to_unit == "C":
        return (value - 32) * 5 / 9
    elif from_unit == "C" and to_unit == "K":
        return value + 273.15
    elif from_unit == "K" and to_unit == "C":
        return value - 273.15
    elif from_unit == "F" and to_unit == "K":
        return (value - 32) * 5 / 9 + 273.15
    elif from_unit == "K" and to_unit == "F":
        return (value - 273.15) * 9 / 5 + 32
    elif from_unit == to_unit:
        return value
    else:
        return None


# ─── 2단계: 개발자가 개선한 버전 (검증 + 에러 처리) ───
VALID_UNITS = {"C": "섭씨(Celsius)", "F": "화씨(Fahrenheit)", "K": "켈빈(Kelvin)"}
ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67, "K": 0}


def convert_temperature(value, from_unit, to_unit):
    """개선된 버전: 입력 검증 + 에러 처리 추가"""
    # [수동 추가] 단위 유효성 검증
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if from_unit not in VALID_UNITS:
        raise ValueError(
            f"잘못된 입력 단위: '{from_unit}'. "
            f"가능한 단위: {', '.join(VALID_UNITS.keys())}"
        )
    if to_unit not in VALID_UNITS:
        raise ValueError(
            f"잘못된 출력 단위: '{to_unit}'. "
            f"가능한 단위: {', '.join(VALID_UNITS.keys())}"
        )

    # [수동 추가] 숫자 타입 검증
    if not isinstance(value, (int, float)):
        raise TypeError(f"숫자를 입력해야 합니다. 입력값: {value}")

    # [수동 추가] 절대 영도 이하 검증
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ValueError(
            f"절대 영도({ABSOLUTE_ZERO[from_unit]}{from_unit}) 이하의 "
            f"온도는 존재할 수 없습니다. 입력값: {value}{from_unit}"
        )

    # [AI 초안] 변환 로직
    result = convert_temperature_draft(value, from_unit, to_unit)
    return round(result, 2)


# ─── 테스트 실행 ───
print("=== 하이브리드 접근법: AI 초안 + 수동 개선 ===\n")

# 정상 변환 테스트
test_cases = [
    (100, "C", "F"),
    (212, "F", "C"),
    (0, "C", "K"),
    (300, "K", "C"),
]

print("[정상 변환 테스트]")
for value, from_u, to_u in test_cases:
    result = convert_temperature(value, from_u, to_u)
    print(f"  {value}{from_u} -> {result}{to_u}")

# 에러 처리 테스트 (수동 개선 부분)
print("\n[에러 처리 테스트 - 수동 개선 부분]")

error_cases = [
    ("잘못된 단위", 100, "X", "F"),
    ("절대 영도 이하", -300, "C", "F"),
    ("잘못된 타입", "뜨거움", "C", "F"),
]

for desc, *args in error_cases:
    try:
        convert_temperature(*args)
    except (ValueError, TypeError) as e:
        print(f"  {desc}: {e}")

print("\n" + "─" * 50)
print("하이브리드 접근법 요약:")
print("  AI 기여  -> 변환 공식 및 기본 구조 생성")
print("  사람 기여 -> 입력 검증, 에러 처리, 경계값 확인 추가")
