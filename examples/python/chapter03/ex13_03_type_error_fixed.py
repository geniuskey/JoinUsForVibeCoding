"""
예제 13-3: TypeError — 문자열과 정수 결합 오류 (수정 완료)
==========================================================
수정 방법 3가지: str() 변환, f-string 사용, 쉼표 구분
"""

# 수정된 코드: f-string을 사용하여 타입 변환 문제 해결
product_name = "노트북"
price = 1500000
quantity = 3

total = price * quantity

# 방법 1: str()로 명시적 변환
print("상품: " + product_name)
print("수량: " + str(quantity) + "개")

# 방법 2: f-string 사용 (권장!)
print(f"총 금액: {total:,}원")

# 방법 3: print의 쉼표 구분 (자동 공백 추가됨)
print("결제 정보:", product_name, quantity, "개,", f"{total:,}원")
