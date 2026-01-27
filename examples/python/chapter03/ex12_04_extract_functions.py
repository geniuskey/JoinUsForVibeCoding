"""
예제 12-4: 함수 분리 요청
==========================
하나의 거대한 함수를 여러 작은 함수로 분리하도록 AI에게 요청하는 예제입니다.

프롬프트: "이 함수가 너무 길어. 기능별로 함수를 분리해줘"
→ 하나의 함수가 하나의 역할만 담당하도록 분리합니다.
"""


# --- 개선 전: 모든 기능이 하나의 함수에 ---
def process_order_before(items, customer_name):
    """하나의 함수가 너무 많은 일을 합니다."""
    # 유효성 검사
    if not items:
        print("오류: 주문 항목이 비어 있습니다.")
        return None
    if not customer_name:
        print("오류: 고객 이름이 비어 있습니다.")
        return None

    # 가격 계산
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["quantity"]

    # 할인 적용
    if subtotal >= 50000:
        discount = subtotal * 0.1
    elif subtotal >= 30000:
        discount = subtotal * 0.05
    else:
        discount = 0

    total = subtotal - discount

    # 배송비 계산
    if total >= 30000:
        shipping = 0
    else:
        shipping = 3000

    final_total = total + shipping

    # 영수증 출력
    print(f"===== 주문 영수증 =====")
    print(f"고객: {customer_name}")
    print(f"-----------------------")
    for item in items:
        line_total = item["price"] * item["quantity"]
        print(f"  {item['name']} x{item['quantity']}: {line_total:,}원")
    print(f"-----------------------")
    print(f"소계:     {subtotal:>10,}원")
    if discount > 0:
        print(f"할인:     {-discount:>10,.0f}원")
    print(f"배송비:   {shipping:>10,}원")
    print(f"=======================")
    print(f"총액:     {final_total:>10,.0f}원")

    return final_total


# --- "기능별로 함수를 분리해줘" 요청 후 개선된 코드 ---
def validate_order(items, customer_name):
    """주문 유효성을 검사합니다."""
    if not items:
        print("오류: 주문 항목이 비어 있습니다.")
        return False
    if not customer_name:
        print("오류: 고객 이름이 비어 있습니다.")
        return False
    return True


def calculate_subtotal(items):
    """상품 소계를 계산합니다."""
    return sum(item["price"] * item["quantity"] for item in items)


def calculate_discount(subtotal):
    """금액에 따른 할인액을 계산합니다."""
    if subtotal >= 50000:
        return subtotal * 0.1
    elif subtotal >= 30000:
        return subtotal * 0.05
    return 0


def calculate_shipping(total_after_discount):
    """배송비를 계산합니다 (3만원 이상 무료배송)."""
    return 0 if total_after_discount >= 30000 else 3000


def print_receipt(customer_name, items, subtotal, discount, shipping, final_total):
    """영수증을 출력합니다."""
    print(f"===== 주문 영수증 =====")
    print(f"고객: {customer_name}")
    print(f"-----------------------")
    for item in items:
        line_total = item["price"] * item["quantity"]
        print(f"  {item['name']} x{item['quantity']}: {line_total:,}원")
    print(f"-----------------------")
    print(f"소계:     {subtotal:>10,}원")
    if discount > 0:
        print(f"할인:     {-discount:>10,.0f}원")
    print(f"배송비:   {shipping:>10,}원")
    print(f"=======================")
    print(f"총액:     {final_total:>10,.0f}원")


def process_order_after(items, customer_name):
    """주문을 처리합니다 (분리된 함수 활용)."""
    if not validate_order(items, customer_name):
        return None

    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal)
    total_after_discount = subtotal - discount
    shipping = calculate_shipping(total_after_discount)
    final_total = total_after_discount + shipping

    print_receipt(customer_name, items, subtotal, discount, shipping, final_total)
    return final_total


# ── 실행 ──
if __name__ == "__main__":
    print("=" * 55)
    print("[예제 12-4] 함수 분리 요청")
    print("=" * 55)

    order_items = [
        {"name": "키보드", "price": 25000, "quantity": 1},
        {"name": "마우스", "price": 15000, "quantity": 2},
    ]

    print("\n[개선 전] 하나의 큰 함수로 처리")
    print("-" * 30)
    result1 = process_order_before(order_items, "김바이브")

    print()
    print("[개선 후] 기능별로 분리된 함수로 처리")
    print("-" * 30)
    result2 = process_order_after(order_items, "김바이브")

    print()
    print("[함수 분리 결과]")
    print(f"  process_order_before → 1개 함수 (약 40줄)")
    print(f"  process_order_after  → 6개 함수 (각 5~15줄)")
    print()
    print("  분리된 함수 목록:")
    print("    1. validate_order()      — 유효성 검사")
    print("    2. calculate_subtotal()  — 소계 계산")
    print("    3. calculate_discount()  — 할인 계산")
    print("    4. calculate_shipping()  — 배송비 계산")
    print("    5. print_receipt()       — 영수증 출력")
    print("    6. process_order_after() — 전체 흐름 관리")
    print()
    print("Tip: 함수는 '하나의 함수 = 하나의 역할' 원칙을 따르세요.")
    print("     이름만 보고도 무엇을 하는 함수인지 알 수 있어야 합니다.")
