"""
예제 13-11: 실습 — 버그 5개 수정 완료
======================================
수정된 5개 버그:
  1. 존재하지 않는 상품 접근 → .get()으로 안전 접근
  2. 수량 미반영 → item["price"] * item["quantity"]
  3. 할인 계산 오류 → discount_percent / 100
  4. 변수명 오타 → sub_total → subtotal
  5. 목록에 없는 상품 → 존재 여부 확인 후 추가
"""

# === 수정된 쇼핑 카트 프로그램 ===

# 상품 목록 (이름: 가격)
products = {
    "사과": 1500,
    "우유": 2500,
    "빵": 3000,
    "계란": 5000,
    "치즈": 4500
}

# 쇼핑 카트
cart = []


def add_to_cart(product_name, qty):
    """상품을 카트에 추가"""
    # 수정 1 & 5: 상품 존재 여부 확인
    if product_name not in products:
        print(f"  ⚠️ '{product_name}'은(는) 상품 목록에 없습니다. 건너뜁니다.")
        return

    price = products[product_name]
    item = {
        "name": product_name,
        "price": price,
        "quantity": qty
    }
    cart.append(item)
    print(f"  '{product_name}' {qty}개 추가 (개당 {price:,}원)")


def calculate_total():
    """카트 총 금액 계산"""
    total = 0
    for item in cart:
        # 수정 2: 가격 × 수량으로 계산
        total += item["price"] * item["quantity"]
    return total


def apply_discount(total, discount_percent):
    """할인 적용"""
    # 수정 3: 할인율을 100으로 나누어 퍼센트 적용
    discount_amount = total * (discount_percent / 100)
    final_price = total - discount_amount
    return final_price


def print_receipt():
    """영수증 출력"""
    print("\n" + "=" * 40)
    print("           영수증")
    print("=" * 40)

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        # 수정 4: sub_total → subtotal (올바른 변수명)
        print(f"  {item['name']:8s} x{item['quantity']}  = {subtotal:>8,}원")

    total = calculate_total()
    print("-" * 40)
    print(f"  소계:                    {total:>8,}원")

    # 10% 할인 적용
    final = apply_discount(total, 10)
    print(f"  할인 (10%):              -{total - final:>7,}원")
    print(f"  최종 금액:               {final:>8,.0f}원")
    print("=" * 40)


# 실행
print("=== 쇼핑 시작 ===")
add_to_cart("사과", 3)
add_to_cart("우유", 2)
add_to_cart("빵", 1)
add_to_cart("커피", 1)        # 수정 5: 없는 상품 → 경고 메시지 출력

print_receipt()
