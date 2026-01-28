"""
예제 20-07: 실습 - 멀티 모듈 계산기
여러 기능을 모듈로 분리한 계산기를 하나의 파일에서 시연합니다.
실제 프로젝트에서는 각 클래스를 별도 파일로 분리합니다.
"""


# ============================================================
# [모듈 1] operations.py - 기본 연산 모듈
# ============================================================

class BasicOperations:
    """기본 사칙연산을 제공합니다."""

    @staticmethod
    def add(a, b):
        """덧셈"""
        return a + b

    @staticmethod
    def subtract(a, b):
        """뺄셈"""
        return a - b

    @staticmethod
    def multiply(a, b):
        """곱셈"""
        return a * b

    @staticmethod
    def divide(a, b):
        """나눗셈 (0으로 나누기 검사 포함)"""
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return a / b


class AdvancedOperations:
    """고급 수학 연산을 제공합니다."""

    @staticmethod
    def power(base, exponent):
        """거듭제곱"""
        return base ** exponent

    @staticmethod
    def modulo(a, b):
        """나머지 연산"""
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return a % b

    @staticmethod
    def floor_divide(a, b):
        """정수 나눗셈 (몫)"""
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return a // b

    @staticmethod
    def factorial(n):
        """팩토리얼 (n!)"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("0 이상의 정수만 가능합니다")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def absolute(a):
        """절댓값"""
        return abs(a)


# ============================================================
# [모듈 2] history.py - 계산 이력 관리 모듈
# ============================================================

class CalculationHistory:
    """계산 이력을 관리합니다."""

    def __init__(self, max_size=100):
        self._history = []
        self._max_size = max_size

    def add_record(self, expression, result):
        """계산 기록을 추가합니다."""
        record = {
            "expression": expression,
            "result": result,
            "index": len(self._history) + 1,
        }
        self._history.append(record)

        # 최대 크기 초과 시 오래된 기록 삭제
        if len(self._history) > self._max_size:
            self._history.pop(0)

        return record

    def get_all(self):
        """전체 이력을 반환합니다."""
        return list(self._history)

    def get_last(self, n=5):
        """최근 n개의 기록을 반환합니다."""
        return self._history[-n:]

    def clear(self):
        """이력을 초기화합니다."""
        count = len(self._history)
        self._history.clear()
        return count

    @property
    def count(self):
        """기록 수를 반환합니다."""
        return len(self._history)

    def search(self, keyword):
        """키워드로 이력을 검색합니다."""
        return [
            record for record in self._history
            if keyword in record["expression"]
        ]


# ============================================================
# [모듈 3] formatter.py - 출력 포맷 모듈
# ============================================================

class ResultFormatter:
    """계산 결과를 다양한 형식으로 포맷합니다."""

    @staticmethod
    def format_result(expression, result):
        """기본 결과 포맷"""
        if isinstance(result, float):
            # 소수점 이하가 0이면 정수로 표시
            if result == int(result):
                return f"  {expression} = {int(result)}"
            return f"  {expression} = {result:.6g}"
        return f"  {expression} = {result}"

    @staticmethod
    def format_history(records):
        """이력을 포맷합니다."""
        if not records:
            return "  (이력이 없습니다)"
        lines = []
        for record in records:
            result = record["result"]
            if isinstance(result, float) and result == int(result):
                result = int(result)
            lines.append(f"  [{record['index']:>3d}] {record['expression']} = {result}")
        return "\n".join(lines)

    @staticmethod
    def format_error(message):
        """오류 메시지를 포맷합니다."""
        return f"  오류: {message}"


# ============================================================
# [모듈 4] calculator.py - 메인 계산기 (모듈 통합)
# ============================================================

class Calculator:
    """여러 모듈을 통합하는 메인 계산기 클래스"""

    # 연산 기호와 함수를 매핑
    OPERATORS = {
        "+": ("덧셈", BasicOperations.add),
        "-": ("뺄셈", BasicOperations.subtract),
        "*": ("곱셈", BasicOperations.multiply),
        "/": ("나눗셈", BasicOperations.divide),
        "**": ("거듭제곱", AdvancedOperations.power),
        "%": ("나머지", AdvancedOperations.modulo),
        "//": ("정수나눗셈", AdvancedOperations.floor_divide),
    }

    FUNCTIONS = {
        "!": ("팩토리얼", AdvancedOperations.factorial),
        "abs": ("절댓값", AdvancedOperations.absolute),
    }

    def __init__(self):
        self.history = CalculationHistory()
        self.formatter = ResultFormatter()

    def calculate(self, a, operator, b=None):
        """계산을 수행하고 이력에 기록합니다."""
        try:
            if operator in self.OPERATORS:
                name, func = self.OPERATORS[operator]
                result = func(a, b)
                expression = f"{a} {operator} {b}"
            elif operator in self.FUNCTIONS:
                name, func = self.FUNCTIONS[operator]
                result = func(a)
                if operator == "!":
                    expression = f"{a}!"
                else:
                    expression = f"{operator}({a})"
            else:
                return self.formatter.format_error(
                    f"알 수 없는 연산자: '{operator}'"
                )

            self.history.add_record(expression, result)
            return self.formatter.format_result(expression, result)

        except (ZeroDivisionError, ValueError, TypeError) as e:
            return self.formatter.format_error(str(e))

    def show_history(self, n=None):
        """계산 이력을 출력합니다."""
        if n:
            records = self.history.get_last(n)
        else:
            records = self.history.get_all()
        return self.formatter.format_history(records)

    def show_available_operations(self):
        """사용 가능한 연산 목록을 출력합니다."""
        lines = ["  사용 가능한 연산:"]
        lines.append("  [이항 연산]")
        for op, (name, _) in self.OPERATORS.items():
            lines.append(f"    {op:>4s} : {name}")
        lines.append("  [단항 연산]")
        for op, (name, _) in self.FUNCTIONS.items():
            lines.append(f"    {op:>4s} : {name}")
        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("예제 20-07: 멀티 모듈 계산기")
    print("=" * 60)
    print()

    # 모듈 구조 설명
    print("--- 모듈 구조 ---")
    print()
    modules = {
        "operations.py": "기본/고급 연산 함수 (BasicOperations, AdvancedOperations)",
        "history.py": "계산 이력 관리 (CalculationHistory)",
        "formatter.py": "결과 출력 포맷 (ResultFormatter)",
        "calculator.py": "메인 계산기 - 모든 모듈 통합 (Calculator)",
    }
    for module, desc in modules.items():
        print(f"  {module:<20s} : {desc}")
    print()

    # 계산기 생성
    calc = Calculator()

    # 사용 가능한 연산 목록
    print("--- 사용 가능한 연산 ---")
    print(calc.show_available_operations())
    print()

    # 기본 사칙연산 테스트
    print("--- 기본 사칙연산 ---")
    print(calc.calculate(100, "+", 200))
    print(calc.calculate(500, "-", 123))
    print(calc.calculate(12, "*", 8))
    print(calc.calculate(100, "/", 3))
    print()

    # 고급 연산 테스트
    print("--- 고급 연산 ---")
    print(calc.calculate(2, "**", 10))
    print(calc.calculate(17, "%", 5))
    print(calc.calculate(17, "//", 5))
    print(calc.calculate(5, "!"))
    print(calc.calculate(10, "!"))
    print(calc.calculate(-42, "abs"))
    print()

    # 오류 처리 테스트
    print("--- 오류 처리 ---")
    print(calc.calculate(10, "/", 0))
    print(calc.calculate(-3, "!"))
    print(calc.calculate(1, "^", 2))
    print()

    # 이력 조회
    print("--- 전체 계산 이력 ---")
    print(calc.show_history())
    print()

    # 최근 이력 조회
    print("--- 최근 3개 이력 ---")
    print(calc.show_history(3))
    print()

    # 이력 검색
    print("--- 이력 검색: '!' 포함 ---")
    search_results = calc.history.search("!")
    print(ResultFormatter.format_history(search_results))
    print()

    # 이력 통계
    print("--- 이력 통계 ---")
    print(f"  총 계산 횟수: {calc.history.count}회")
    cleared = calc.history.clear()
    print(f"  이력 초기화: {cleared}건 삭제됨")
    print(f"  현재 이력 수: {calc.history.count}건")
    print()

    print("멀티 모듈 계산기 예제를 성공적으로 실행했습니다!")
