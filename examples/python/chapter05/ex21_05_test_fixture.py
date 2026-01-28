"""
예제 21-05: 픽스처 사용 (setUp, tearDown)
- setUp과 tearDown으로 테스트 전후 환경을 설정합니다
- setUpClass와 tearDownClass의 차이를 이해합니다
"""

import unittest
import tempfile
import os


# ============================================================
# 테스트할 클래스: 간단한 장바구니
# ============================================================
class ShoppingCart:
    """장바구니 클래스"""

    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        """상품을 장바구니에 추가합니다."""
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def remove_item(self, name):
        """상품을 장바구니에서 제거합니다."""
        self.items = [item for item in self.items if item["name"] != name]

    def get_total(self):
        """총 가격을 계산합니다."""
        return sum(item["price"] * item["quantity"] for item in self.items)

    def get_item_count(self):
        """상품 종류 수를 반환합니다."""
        return len(self.items)

    def clear(self):
        """장바구니를 비웁니다."""
        self.items = []


# ============================================================
# 테스트 클래스 1: setUp과 tearDown 사용
# ============================================================
class TestShoppingCart(unittest.TestCase):
    """장바구니 테스트 - setUp/tearDown 활용"""

    def setUp(self):
        """각 테스트 메서드 실행 전에 호출됩니다.
        테스트에 필요한 객체와 데이터를 준비합니다."""
        print(f"    [setUp] 장바구니 생성 및 샘플 상품 추가")
        self.cart = ShoppingCart()
        # 테스트용 상품 미리 추가
        self.cart.add_item("사과", 1000, 3)
        self.cart.add_item("바나나", 1500, 2)

    def tearDown(self):
        """각 테스트 메서드 실행 후에 호출됩니다.
        테스트에 사용한 리소스를 정리합니다."""
        print(f"    [tearDown] 장바구니 정리")
        self.cart.clear()

    def test_initial_items(self):
        """setUp에서 추가한 상품 확인"""
        self.assertEqual(self.cart.get_item_count(), 2)

    def test_add_item(self):
        """상품 추가 테스트"""
        self.cart.add_item("체리", 3000)
        self.assertEqual(self.cart.get_item_count(), 3)

    def test_remove_item(self):
        """상품 제거 테스트"""
        self.cart.remove_item("사과")
        self.assertEqual(self.cart.get_item_count(), 1)

    def test_total_price(self):
        """총 가격 계산 테스트"""
        # 사과 1000 * 3 + 바나나 1500 * 2 = 6000
        self.assertEqual(self.cart.get_total(), 6000)

    def test_clear_cart(self):
        """장바구니 비우기 테스트"""
        self.cart.clear()
        self.assertEqual(self.cart.get_item_count(), 0)
        self.assertEqual(self.cart.get_total(), 0)


# ============================================================
# 테스트 클래스 2: setUpClass와 tearDownClass 사용
# ============================================================
class TestFileOperations(unittest.TestCase):
    """파일 작업 테스트 - setUpClass/tearDownClass 활용"""

    @classmethod
    def setUpClass(cls):
        """테스트 클래스 전체에서 한 번만 호출됩니다.
        모든 테스트가 공유할 리소스를 준비합니다."""
        print("\n  [setUpClass] 임시 디렉토리 생성")
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.temp_dir, "test_data.txt")

        # 테스트용 파일 생성
        with open(cls.test_file, "w", encoding="utf-8") as f:
            f.write("안녕하세요\n")
            f.write("바이브 코딩\n")
            f.write("테스트 주도 개발\n")

        print(f"  [setUpClass] 임시 파일 생성: {cls.test_file}")

    @classmethod
    def tearDownClass(cls):
        """테스트 클래스의 모든 테스트가 끝난 후 한 번만 호출됩니다.
        공유 리소스를 정리합니다."""
        print(f"\n  [tearDownClass] 임시 파일 삭제")
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        if os.path.exists(cls.temp_dir):
            os.rmdir(cls.temp_dir)
        print(f"  [tearDownClass] 정리 완료")

    def test_file_exists(self):
        """파일이 존재하는지 확인"""
        self.assertTrue(os.path.exists(self.test_file))

    def test_file_content(self):
        """파일 내용 확인"""
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("바이브 코딩", content)

    def test_line_count(self):
        """파일의 줄 수 확인"""
        with open(self.test_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 3)

    def test_first_line(self):
        """첫 번째 줄 내용 확인"""
        with open(self.test_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        self.assertEqual(first_line, "안녕하세요")


if __name__ == "__main__":
    print("=" * 60)
    print("예제 21-05: 테스트 픽스처 (setUp / tearDown)")
    print("=" * 60)
    print()
    print("픽스처(Fixture)란?")
    print("  테스트 실행 전후에 필요한 환경을 설정하고 정리하는 코드입니다.")
    print()
    print("메서드 호출 순서:")
    print("  setUp    → 각 테스트 메서드 실행 전마다 호출")
    print("  tearDown → 각 테스트 메서드 실행 후마다 호출")
    print("  setUpClass    → 클래스의 첫 테스트 전에 한 번만 호출")
    print("  tearDownClass → 클래스의 마지막 테스트 후에 한 번만 호출")
    print()
    print("-" * 60)
    print("테스트 실행 결과:")
    print("-" * 60)

    unittest.main(verbosity=2)
