"""
예제 12-7: 가독성 개선 요청
============================
중첩된 조건문을 얼리 리턴(early return) 패턴으로 개선하는 예제입니다.

프롬프트: "if문이 너무 깊게 중첩돼 있어. 가독성을 개선해줘"
→ 중첩 조건문을 얼리 리턴과 가드 절(guard clause)로 평탄화합니다.
"""


# --- 개선 전: 깊은 중첩 조건문 ---
def process_payment_before(user, amount, payment_method):
    """결제 처리 — 중첩 조건문 버전 (화살표 코드)"""
    result = {"success": False, "message": ""}

    if user is not None:
        if user.get("is_active"):
            if amount > 0:
                if amount <= user.get("balance", 0):
                    if payment_method in ["card", "bank", "point"]:
                        if payment_method == "point" and amount > user.get("points", 0):
                            result["message"] = "포인트가 부족합니다."
                        else:
                            # 실제 결제 처리
                            user["balance"] -= amount
                            result["success"] = True
                            result["message"] = f"{amount:,}원 결제 완료"
                    else:
                        result["message"] = "지원하지 않는 결제 수단입니다."
                else:
                    result["message"] = "잔액이 부족합니다."
            else:
                result["message"] = "결제 금액이 올바르지 않습니다."
        else:
            result["message"] = "비활성 계정입니다."
    else:
        result["message"] = "사용자 정보가 없습니다."

    return result


# --- "가독성을 개선해줘" 요청 후 개선된 코드 ---
def process_payment_after(user, amount, payment_method):
    """결제 처리 — 얼리 리턴 버전 (평탄한 구조)"""
    # 가드 절: 잘못된 입력을 빨리 걸러냄
    if user is None:
        return {"success": False, "message": "사용자 정보가 없습니다."}

    if not user.get("is_active"):
        return {"success": False, "message": "비활성 계정입니다."}

    if amount <= 0:
        return {"success": False, "message": "결제 금액이 올바르지 않습니다."}

    if amount > user.get("balance", 0):
        return {"success": False, "message": "잔액이 부족합니다."}

    valid_methods = ["card", "bank", "point"]
    if payment_method not in valid_methods:
        return {"success": False, "message": "지원하지 않는 결제 수단입니다."}

    if payment_method == "point" and amount > user.get("points", 0):
        return {"success": False, "message": "포인트가 부족합니다."}

    # 모든 검증을 통과한 경우 — 결제 처리
    user["balance"] -= amount
    return {"success": True, "message": f"{amount:,}원 결제 완료"}


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-7] 가독성 개선 요청 — 얼리 리턴")
    print("=" * 55)

    # 테스트 케이스 목록
    test_cases = [
        (None, 10000, "card", "사용자 없음"),
        ({"is_active": False, "balance": 50000}, 10000, "card", "비활성 계정"),
        ({"is_active": True, "balance": 50000}, -500, "card", "잘못된 금액"),
        ({"is_active": True, "balance": 5000}, 10000, "card", "잔액 부족"),
        ({"is_active": True, "balance": 50000}, 10000, "bitcoin", "잘못된 결제수단"),
        ({"is_active": True, "balance": 50000, "points": 3000}, 5000, "point", "포인트 부족"),
        ({"is_active": True, "balance": 50000}, 10000, "card", "정상 결제"),
    ]

    for i, (user, amount, method, description) in enumerate(test_cases, 1):
        # 각 테스트마다 새 사용자 딕셔너리 (원본 보존)
        user_copy1 = dict(user) if user else None
        user_copy2 = dict(user) if user else None

        result_before = process_payment_before(user_copy1, amount, method)
        result_after = process_payment_after(user_copy2, amount, method)

        status = "성공" if result_after["success"] else "실패"
        print(f"\n  테스트 {i}: {description}")
        print(f"    중첩 버전: {result_before['message']}")
        print(f"    얼리 리턴: {result_after['message']}")
        print(f"    결과 일치: {'예' if result_before == result_after else '아니오'}")

    print()
    print("[구조 비교]")
    print("-" * 55)
    print("  중첩 버전: 최대 6단계 깊이 (화살표 모양)")
    print("  얼리 리턴: 최대 1단계 깊이 (평탄한 구조)")
    print()
    print("Tip: '만약 ~가 아니면 빨리 빠져나간다'는 패턴을")
    print("     얼리 리턴(early return) 또는 가드 절(guard clause)이라 합니다.")
    print("     AI에게 '중첩을 줄여줘'라고 요청하면 적용됩니다.")
