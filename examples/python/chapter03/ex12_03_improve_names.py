"""
예제 12-3: 변수명 개선 요청
============================
의미 없는 변수명을 명확한 이름으로 개선하도록 AI에게 요청하는 예제입니다.

프롬프트: "변수명을 더 의미 있게 바꿔줘"
→ x, y, tmp 같은 이름을 width, height, buffer 같은 명확한 이름으로 변경합니다.
"""


# --- 개선 전: 의미 없는 변수명 ---
def calc_before(a, b, c, d):
    """무엇을 계산하는지 변수명만으로는 알 수 없음"""
    t = a * b
    t2 = c * d
    r = t + t2
    p = r * 0.1
    f = r + p
    return f


# --- "변수명을 더 의미 있게 바꿔줘" 요청 후 개선된 코드 ---
def calculate_total_price(item_price, item_quantity, shipping_fee, shipping_count):
    """주문 총액을 계산합니다 (상품 금액 + 배송비 + 세금 포함)."""
    item_subtotal = item_price * item_quantity
    shipping_subtotal = shipping_fee * shipping_count
    order_total_before_tax = item_subtotal + shipping_subtotal
    tax_amount = order_total_before_tax * 0.1
    final_total = order_total_before_tax + tax_amount
    return final_total


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-3] 변수명 개선 요청")
    print("=" * 55)

    # 테스트 데이터
    price = 15000       # 상품 단가
    qty = 3             # 수량
    ship_fee = 3000     # 배송비 단가
    ship_count = 1      # 배송 횟수

    print()
    print("[개선 전] calc_before(15000, 3, 3000, 1)")
    result_before = calc_before(price, qty, ship_fee, ship_count)
    print(f"  결과: {result_before:,.0f}원")
    print(f"  → 함수명과 변수명만으로는 의미 파악 불가")
    print()

    print("[개선 후] calculate_total_price(15000, 3, 3000, 1)")
    result_after = calculate_total_price(price, qty, ship_fee, ship_count)
    print(f"  결과: {result_after:,.0f}원")
    print(f"  → 함수명과 변수명으로 의미가 명확함")
    print()

    # 변수명 비교 표
    print("[변수명 비교표]")
    print("-" * 55)
    comparisons = [
        ("a", "item_price", "상품 단가"),
        ("b", "item_quantity", "상품 수량"),
        ("c", "shipping_fee", "배송비 단가"),
        ("d", "shipping_count", "배송 횟수"),
        ("t", "item_subtotal", "상품 소계"),
        ("t2", "shipping_subtotal", "배송비 소계"),
        ("r", "order_total_before_tax", "세전 합계"),
        ("p", "tax_amount", "세금"),
        ("f", "final_total", "최종 합계"),
    ]
    print(f"  {'개선 전':<10} {'개선 후':<25} {'의미'}")
    print(f"  {'-'*10} {'-'*25} {'-'*12}")
    for before, after, meaning in comparisons:
        print(f"  {before:<10} {after:<25} {meaning}")

    print()
    print("Tip: 변수명은 '6개월 후의 내가 봐도 이해할 수 있는가?'를")
    print("     기준으로 작성하세요.")
