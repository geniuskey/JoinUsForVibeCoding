"""
예제 14-8: 실습 — 실패 시 롤백하기
=====================================
새 기능을 추가했는데 기존 기능이 망가지는 상황을 시뮬레이션합니다.
이런 상황에서 Git을 활용해 안전하게 롤백하는 방법을 배웁니다.

시나리오:
  1. v0.4 계산기가 잘 동작하고 있음 (안정 버전)
  2. "고급 수학 함수(제곱근, 거듭제곱)"를 추가 요청
  3. AI가 생성한 코드에 버그 발생! (기존 사칙연산이 망가짐)
  4. git checkout으로 안정 버전으로 롤백
  5. 다시 요청하여 올바른 코드 획득
"""


# ── 안정 버전 (v0.4) ── 잘 동작하는 코드 ──────────

def calculator_v04():
    """v0.4 안정 버전: 사칙연산이 정상 동작합니다."""
    print("[v0.4 안정 버전] 사칙연산 테스트")

    tests = [
        ("10 + 3", 10 + 3, 13),
        ("10 - 3", 10 - 3, 7),
        ("10 * 3", 10 * 3, 30),
        ("10 / 3", round(10 / 3, 2), 3.33),
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if round(result, 2) == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} [{status}]")

    return all_passed


# ── 버그 버전 (v0.5-buggy) ── 실수로 기존 기능을 망가뜨림 ──

def add_buggy(a, b):
    """버그! 고급 함수 추가하면서 실수로 add를 덮어씀."""
    # 원래: return a + b
    # AI가 제곱근 기능 추가하면서 실수로 변경됨
    return a ** b  # 거듭제곱이 되어버림!


def subtract_buggy(a, b):
    """정상 동작"""
    return a - b


def sqrt_buggy(a):
    """새로 추가된 함수 — 이것 자체는 동작함"""
    if a < 0:
        raise ValueError("음수의 제곱근은 계산할 수 없습니다.")
    return a ** 0.5


def calculator_v05_buggy():
    """v0.5 버그 버전: 고급 함수 추가 후 기존 기능이 망가짐!"""
    print("[v0.5 버그 버전] 고급 수학 함수 추가 후 테스트")

    tests = [
        ("10 + 3", add_buggy(10, 3), 13),      # 10**3 = 1000 (버그!)
        ("10 - 3", subtract_buggy(10, 3), 7),   # 정상
        ("sqrt(16)", sqrt_buggy(16), 4.0),       # 새 기능 정상
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} (기대값: {expected}) [{status}]")

    return all_passed


# ── 수정 버전 (v0.5-fixed) ── 올바르게 다시 구현 ──

def add_fixed(a, b):
    """수정됨: 덧셈이 올바르게 동작합니다."""
    return a + b


def subtract_fixed(a, b):
    return a - b


def multiply_fixed(a, b):
    return a * b


def divide_fixed(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


def sqrt_fixed(a):
    """새 기능: 제곱근"""
    if a < 0:
        raise ValueError("음수의 제곱근은 계산할 수 없습니다.")
    return a ** 0.5


def power_fixed(a, b):
    """새 기능: 거듭제곱"""
    return a ** b


def calculator_v05_fixed():
    """v0.5 수정 버전: 기존 기능 유지 + 새 기능 추가"""
    print("[v0.5 수정 버전] 기존 기능 + 고급 수학 함수")

    tests = [
        ("10 + 3", add_fixed(10, 3), 13),
        ("10 - 3", subtract_fixed(10, 3), 7),
        ("10 * 3", multiply_fixed(10, 3), 30),
        ("10 / 2", divide_fixed(10, 2), 5.0),
        ("sqrt(16)", sqrt_fixed(16), 4.0),
        ("2 ** 10", power_fixed(2, 10), 1024),
    ]

    all_passed = True
    for expr, result, expected in tests:
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  {expr} = {result} [{status}]")

    return all_passed


# ── 메인: 전체 시나리오 시뮬레이션 ──

def main():
    print("=" * 60)
    print("  롤백 시나리오 시뮬레이션")
    print("  (새 기능 추가 → 버그 발생 → 롤백 → 재시도)")
    print("=" * 60)

    # 1단계: 안정 버전 확인
    print(f"\n{'─'*60}")
    print("단계 1: 현재 안정 버전 확인")
    print(f"{'─'*60}")
    v04_ok = calculator_v04()
    print(f"  결과: {'모든 테스트 통과!' if v04_ok else '문제 발견!'}")

    # 2단계: 새 기능 추가 (버그 발생!)
    print(f"\n{'─'*60}")
    print("단계 2: AI에게 고급 수학 함수 추가 요청")
    print("  프롬프트: '제곱근과 거듭제곱 기능을 추가해줘'")
    print(f"{'─'*60}")
    v05_ok = calculator_v05_buggy()
    print(f"  결과: {'모든 테스트 통과!' if v05_ok else '버그 발견! 기존 기능이 망가졌습니다!'}")

    # 3단계: 롤백
    print(f"\n{'─'*60}")
    print("단계 3: Git으로 안정 버전으로 롤백")
    print(f"{'─'*60}")
    print("  실행할 Git 명령어:")
    print("  $ git diff                     # 무엇이 변경되었는지 확인")
    print("  $ git stash                    # 현재 변경사항 임시 저장")
    print("  $ git checkout HEAD -- .       # 마지막 커밋 상태로 복원")
    print("  (또는)")
    print('  $ git checkout HEAD -- calculator.py  # 특정 파일만 복원')
    print("  → 안정 버전(v0.4)으로 되돌아감!")

    # 4단계: 다시 시도
    print(f"\n{'─'*60}")
    print("단계 4: AI에게 더 구체적으로 다시 요청")
    print("  프롬프트: '기존 add, subtract, multiply, divide 함수를 절대")
    print("  수정하지 말고, sqrt와 power 함수만 새로 추가해줘.'")
    print(f"{'─'*60}")
    v05_fixed_ok = calculator_v05_fixed()
    print(f"  결과: {'모든 테스트 통과!' if v05_fixed_ok else '아직 문제가 있습니다.'}")

    # 요약
    print(f"\n{'='*60}")
    print("  롤백 시나리오 요약")
    print(f"{'='*60}")
    print("  1. 새 기능 추가 시 기존 기능이 망가질 수 있다")
    print("  2. Git이 있으면 안전하게 이전 상태로 돌아갈 수 있다")
    print("  3. 롤백 후 더 구체적인 프롬프트로 재시도한다")
    print("  4. '기존 코드를 수정하지 말고'라는 조건을 명시한다")
    print(f"\n  핵심: 자주 커밋하고, 문제가 생기면 롤백하라!")


if __name__ == "__main__":
    main()
