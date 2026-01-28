"""
예제 20-03: 패키지 만들기
__init__.py를 사용한 파이썬 패키지 구조를 생성하고,
패키지의 임포트 동작을 시뮬레이션합니다.
"""

import os
import sys
import tempfile
import shutil


def create_package(base_dir):
    """여러 모듈로 구성된 패키지를 생성합니다."""

    package_dir = os.path.join(base_dir, "mathtools")

    # 패키지 디렉토리 생성
    os.makedirs(package_dir, exist_ok=True)

    # --- __init__.py ---
    # 패키지 초기화 파일: 이 파일이 있어야 파이썬이 디렉토리를 패키지로 인식합니다
    init_content = '''"""
mathtools 패키지
수학 관련 유틸리티 함수 모음입니다.
"""

__version__ = "1.0.0"
__author__ = "바이브 코더"

# 패키지에서 자주 사용하는 함수를 바로 임포트할 수 있게 설정
from .basic import add, subtract, multiply, divide
from .advanced import power, factorial, fibonacci

# 패키지 수준에서 공개할 이름 목록
__all__ = [
    "add", "subtract", "multiply", "divide",
    "power", "factorial", "fibonacci",
]

def info():
    """패키지 정보를 출력합니다."""
    print(f"mathtools v{__version__} by {__author__}")
    print(f"사용 가능한 함수: {', '.join(__all__)}")
'''

    # --- basic.py ---
    basic_content = '''"""
기본 사칙연산 모듈
"""

def add(a, b):
    """두 수를 더합니다."""
    return a + b

def subtract(a, b):
    """두 수를 뺍니다."""
    return a - b

def multiply(a, b):
    """두 수를 곱합니다."""
    return a * b

def divide(a, b):
    """두 수를 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b
'''

    # --- advanced.py ---
    advanced_content = '''"""
고급 수학 함수 모듈
"""

def power(base, exponent):
    """거듭제곱을 계산합니다."""
    return base ** exponent

def factorial(n):
    """팩토리얼을 계산합니다."""
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """피보나치 수열의 n번째 값을 반환합니다."""
    if n <= 0:
        raise ValueError("양수를 입력해주세요")
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b
'''

    # --- 서브패키지: mathtools/stats/__init__.py ---
    stats_dir = os.path.join(package_dir, "stats")
    os.makedirs(stats_dir, exist_ok=True)

    stats_init_content = '''"""
통계 서브패키지
"""
from .descriptive import mean, median
'''

    stats_descriptive_content = '''"""
기술통계 모듈
"""

def mean(numbers):
    """평균을 계산합니다."""
    if not numbers:
        raise ValueError("빈 리스트입니다")
    return sum(numbers) / len(numbers)

def median(numbers):
    """중앙값을 계산합니다."""
    if not numbers:
        raise ValueError("빈 리스트입니다")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]
'''

    # 파일 작성
    files = {
        os.path.join(package_dir, "__init__.py"): init_content,
        os.path.join(package_dir, "basic.py"): basic_content,
        os.path.join(package_dir, "advanced.py"): advanced_content,
        os.path.join(stats_dir, "__init__.py"): stats_init_content,
        os.path.join(stats_dir, "descriptive.py"): stats_descriptive_content,
    }

    for filepath, content in files.items():
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return package_dir


def print_package_tree(package_dir):
    """패키지 구조를 시각적으로 출력합니다."""
    base = os.path.basename(package_dir)
    print(f"{base}/")

    items = sorted(os.listdir(package_dir))
    for i, item in enumerate(items):
        full_path = os.path.join(package_dir, item)
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "

        if os.path.isdir(full_path):
            print(f"    {connector}{item}/")
            sub_items = sorted(os.listdir(full_path))
            for j, sub_item in enumerate(sub_items):
                sub_connector = "└── " if j == len(sub_items) - 1 else "├── "
                padding = "    " if is_last else "│   "
                print(f"    {padding}    {sub_connector}{sub_item}")
        else:
            print(f"    {connector}{item}")


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-03: 패키지 만들기")
    print("=" * 60)
    print()

    # 임시 디렉토리에 패키지 생성
    temp_dir = tempfile.mkdtemp()

    try:
        # 패키지 생성
        package_dir = create_package(temp_dir)

        # 패키지 구조 출력
        print("--- 생성된 패키지 구조 ---")
        print_package_tree(package_dir)
        print()

        # __init__.py의 역할 설명
        print("--- __init__.py의 역할 ---")
        print("  1. 디렉토리를 파이썬 패키지로 인식하게 합니다")
        print("  2. 패키지 임포트 시 자동 실행되는 초기화 코드를 담습니다")
        print("  3. __all__ 변수로 공개 API를 정의합니다")
        print("  4. 하위 모듈의 함수를 패키지 수준에서 재노출(re-export)합니다")
        print()

        # 패키지 임포트 시뮬레이션
        print("--- 패키지 임포트 시뮬레이션 ---")
        print()

        # sys.path에 임시 디렉토리 추가하여 임포트 가능하게 만듦
        sys.path.insert(0, temp_dir)

        # 패키지 임포트
        import mathtools

        print(f"import mathtools")
        print(f"  mathtools.__version__ = '{mathtools.__version__}'")
        print(f"  mathtools.__author__ = '{mathtools.__author__}'")
        print()

        # 패키지 정보 출력
        print("mathtools.info() 호출:")
        print("  ", end="")
        mathtools.info()
        print()

        # 기본 연산 사용
        print("--- 기본 연산 (basic 모듈) ---")
        print(f"  mathtools.add(10, 3) = {mathtools.add(10, 3)}")
        print(f"  mathtools.subtract(10, 3) = {mathtools.subtract(10, 3)}")
        print(f"  mathtools.multiply(10, 3) = {mathtools.multiply(10, 3)}")
        print(f"  mathtools.divide(10, 3) = {mathtools.divide(10, 3):.4f}")
        print()

        # 고급 연산 사용
        print("--- 고급 연산 (advanced 모듈) ---")
        print(f"  mathtools.power(2, 10) = {mathtools.power(2, 10)}")
        print(f"  mathtools.factorial(5) = {mathtools.factorial(5)}")
        print(f"  mathtools.fibonacci(10) = {mathtools.fibonacci(10)}")
        print()

        # 서브패키지 사용
        from mathtools.stats import mean, median
        data = [4, 8, 15, 16, 23, 42]
        print("--- 통계 서브패키지 (stats) ---")
        print(f"  데이터: {data}")
        print(f"  mean({data}) = {mean(data):.2f}")
        print(f"  median({data}) = {median(data):.1f}")
        print()

        # 다양한 임포트 방식 설명
        print("--- 다양한 임포트 방식 ---")
        print("  import mathtools              # 패키지 전체 임포트")
        print("  from mathtools import add     # 특정 함수만 임포트")
        print("  from mathtools.basic import * # 모듈의 모든 함수 임포트")
        print("  from mathtools.stats import mean  # 서브패키지에서 임포트")

        print()
        print("패키지 만들기 예제를 성공적으로 실행했습니다!")

    finally:
        # sys.path 정리
        if temp_dir in sys.path:
            sys.path.remove(temp_dir)
        # 임포트된 모듈 정리
        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith("mathtools"):
                del sys.modules[mod_name]
        # 임시 디렉토리 정리
        shutil.rmtree(temp_dir)
        print("(임시 디렉토리 정리 완료)")
