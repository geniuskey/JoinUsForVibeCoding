"""
예제 13-11: 실습 — 버그 5개 수정하기
=====================================
아래 코드에는 5개의 버그가 숨어 있습니다.
AI에게 도움을 요청하여 모든 버그를 찾고 수정해 보세요!

프로그램 목적: 쇼핑 카트 시스템
- 상품 목록에서 상품을 카트에 추가
- 카트의 총 금액을 계산
- 할인 적용 후 최종 금액 출력
"""

# === 버그가 5개 있는 쇼핑 카트 프로그램 ===

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
    # 버그 1: 딕셔너리 키 접근 방식 오류
    price = products[product_name]
    item = {
        "name": product_name,
        "price": price,
        "quantity": qty
    }
    cart.append(item)
    print(f"  '{product_name}' {qty}개 추가 (개당 {price}원)")


def calculate_total():
    """카트 총 금액 계산"""
    total = 0
    for item in cart:
        # 버그 2: 수량을 곱하지 않음
        total += item["price"]
    return total


def apply_discount(total, discount_percent):
    """할인 적용"""
    # 버그 3: 할인 계산 공식 오류 (할인율을 100으로 나누지 않음)
    discount_amount = total * discount_percent
    final_price = total - discount_amount
    return final_price


def print_receipt():
    """영수증 출력"""
    print("\n" + "=" * 40)
    print("         🛒 영수증")
    print("=" * 40)

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        # 버그 4: f-string 포맷 오류 — 변수명 오타
        print(f"  {item['name']:8s} x{item['quantity']}  = {sub_total:>8,}원")

    total = calculate_total()
    print("-" * 40)
    print(f"  소계:                    {total:>8,}원")

    # 10% 할인 적용
    final = apply_discount(total, 10)
    print(f"  할인 (10%):              -{total - final:>7,}원")
    print(f"  최종 금액:               {final:>8,}원")
    print("=" * 40)


# 실행
print("=== 쇼핑 시작 ===")
add_to_cart("사과", 3)
add_to_cart("우유", 2)
add_to_cart("빵", 1)
add_to_cart("커피", 1)        # 버그 5: 상품 목록에 없는 상품 추가 시도

print_receipt()
