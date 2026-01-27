"""
예제 18-09: 상품 정보 수집기
쇼핑몰 HTML에서 상품명, 가격, 평점 등의 정보를 추출합니다.
실제 이커머스 사이트의 구조를 모사한 HTML을 파싱합니다.
"""

from html.parser import HTMLParser

# 쇼핑몰을 모사한 HTML
SHOP_HTML = """<!DOCTYPE html>
<html>
<body>
    <h1>바이브 코딩 추천 장비</h1>

    <div class="product-list">
        <div class="product-card">
            <img src="/img/keyboard.jpg" alt="기계식 키보드">
            <h3 class="product-name">프로그래머 기계식 키보드</h3>
            <p class="product-price">89,000원</p>
            <p class="product-rating">★★★★★ (4.8/5.0, 리뷰 324개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>

        <div class="product-card">
            <img src="/img/monitor.jpg" alt="4K 모니터">
            <h3 class="product-name">32인치 4K 코딩 모니터</h3>
            <p class="product-price">450,000원</p>
            <p class="product-rating">★★★★☆ (4.5/5.0, 리뷰 189개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>

        <div class="product-card">
            <img src="/img/mouse.jpg" alt="인체공학 마우스">
            <h3 class="product-name">인체공학 버티컬 마우스</h3>
            <p class="product-price">55,000원</p>
            <p class="product-rating">★★★★☆ (4.3/5.0, 리뷰 567개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>

        <div class="product-card">
            <img src="/img/headset.jpg" alt="노이즈캔슬링 헤드셋">
            <h3 class="product-name">노이즈캔슬링 코딩 헤드셋</h3>
            <p class="product-price">199,000원</p>
            <p class="product-rating">★★★★★ (4.9/5.0, 리뷰 892개)</p>
            <span class="product-status out-of-stock">품절</span>
        </div>

        <div class="product-card">
            <img src="/img/desk.jpg" alt="전동 스탠딩 데스크">
            <h3 class="product-name">전동 높이조절 스탠딩 데스크</h3>
            <p class="product-price">320,000원</p>
            <p class="product-rating">★★★★☆ (4.6/5.0, 리뷰 156개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>

        <div class="product-card">
            <img src="/img/chair.jpg" alt="인체공학 의자">
            <h3 class="product-name">프리미엄 인체공학 의자</h3>
            <p class="product-price">680,000원</p>
            <p class="product-rating">★★★★★ (4.7/5.0, 리뷰 445개)</p>
            <span class="product-status in-stock">재고 있음</span>
        </div>
    </div>
</body>
</html>"""


class ProductParser(HTMLParser):
    """쇼핑몰 HTML에서 상품 정보를 추출하는 파서"""

    def __init__(self):
        super().__init__()
        self.products = []
        self.in_product = False
        self.current_product = {}
        self.current_class = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_value = attrs_dict.get("class", "")

        if tag == "div" and "product-card" in class_value:
            self.in_product = True
            self.current_product = {}

        if self.in_product:
            self.current_class = class_value
            # 이미지 정보 추출
            if tag == "img":
                self.current_product["image"] = attrs_dict.get("src", "")

    def handle_endtag(self, tag):
        if tag == "div" and self.in_product and self.current_product:
            # product-card div가 닫힐 때
            if "name" in self.current_product:
                self.products.append(self.current_product)
                self.in_product = False
                self.current_product = {}

    def handle_data(self, data):
        if not self.in_product or not data.strip():
            return

        text = data.strip()

        if "product-name" in self.current_class:
            self.current_product["name"] = text
        elif "product-price" in self.current_class:
            self.current_product["price_text"] = text
            # 숫자만 추출하여 정수로 변환
            price_num = text.replace(",", "").replace("원", "").strip()
            try:
                self.current_product["price"] = int(price_num)
            except ValueError:
                self.current_product["price"] = 0
        elif "product-rating" in self.current_class:
            self.current_product["rating_text"] = text
            # 평점 숫자 추출
            if "/" in text:
                try:
                    rating_part = text.split("(")[1].split("/")[0]
                    self.current_product["rating"] = float(rating_part)
                except (IndexError, ValueError):
                    self.current_product["rating"] = 0.0
            # 리뷰 수 추출
            if "리뷰" in text:
                try:
                    review_part = text.split("리뷰")[1].strip()
                    review_count = review_part.replace("개)", "").replace(",", "").strip()
                    self.current_product["reviews"] = int(review_count)
                except (IndexError, ValueError):
                    self.current_product["reviews"] = 0
        elif "product-status" in self.current_class:
            self.current_product["status"] = text
            self.current_product["in_stock"] = "in-stock" in self.current_class


# 실행
print("=" * 60)
print("예제 18-09: 상품 정보 수집기")
print("=" * 60)

parser = ProductParser()
parser.feed(SHOP_HTML)

print(f"\n총 {len(parser.products)}개의 상품을 수집했습니다.\n")

# 상품 목록 출력
print("--- 상품 목록 ---\n")
for i, product in enumerate(parser.products, 1):
    status = "✓ 구매가능" if product.get("in_stock") else "✗ 품절"
    print(f"  {i}. {product['name']}")
    print(f"     가격: {product.get('price_text', '-')}")
    print(f"     평점: {product.get('rating', '-')} / 5.0"
          f" (리뷰 {product.get('reviews', 0)}개)")
    print(f"     상태: {status}")
    print()

# 가격순 정렬
print("--- 가격순 정렬 (낮은 순) ---\n")
sorted_by_price = sorted(parser.products, key=lambda x: x.get("price", 0))
for product in sorted_by_price:
    print(f"  {product.get('price_text', '-'):>12}  {product['name']}")

# 평점순 정렬
print("\n--- 평점순 정렬 (높은 순) ---\n")
sorted_by_rating = sorted(parser.products,
                          key=lambda x: x.get("rating", 0),
                          reverse=True)
for product in sorted_by_rating:
    print(f"  {product.get('rating', 0)}/5.0  {product['name']}")

# 구매 가능한 상품만 필터링
print("\n--- 구매 가능한 상품 ---\n")
available = [p for p in parser.products if p.get("in_stock")]
print(f"  {len(available)}개 상품 구매 가능:")
for p in available:
    print(f"  - {p['name']} ({p.get('price_text', '-')})")

# 통계
print("\n--- 가격 통계 ---")
prices = [p.get("price", 0) for p in parser.products]
print(f"  최저가: {min(prices):,}원")
print(f"  최고가: {max(prices):,}원")
print(f"  평균가: {sum(prices) // len(prices):,}원")
